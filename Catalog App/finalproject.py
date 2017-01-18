from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, flash
from flask import session as login_session
from flask import make_response
from werkzeug.utils import secure_filename

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Shop, MenuItem, User

from oauth2client import client
from oauth2client.client import FlowExchangeError
from oauth2client.client import flow_from_clientsecrets

import httplib2
import json
import random
import string
import requests
import os


app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']
APPLICATION_NAME = "Shop Application"

engine = create_engine('sqlite:///shopbase.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = set(['jpg'])

app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() \
                               in ALLOWED_EXTENSIONS


# Login
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code, now compatible with Python3
    request.get_data()
    code = request.data.decode('utf-8')

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Submit request, parse response - Python3 compatible
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('User is already connected'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; ' \
              'height: 300px;border-radius: ' \
              '150px;-webkit-border-radius: ' \
              '150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print(login_session.get('access_token'))
    return output


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=1).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Show all shops
@app.route('/')
@app.route('/shop/')
def showShop():
    shop = session.query(Shop).all()
    if 'username' not in login_session:
        return render_template('publicshop.html', shop=shop)
    else:
        return render_template('shop.html', shop=shop)


# Show a shop menu
@app.route('/shop/<int:shop_id>/')
@app.route('/shop/<int:shop_id>/menu/')
def showMenu(shop_id):
    shop = session.query(Shop).filter_by(id=shop_id).one()
    creator = getUserInfo(shop.user_id)
    items = session.query(MenuItem).filter_by(
        shop_id=shop_id).all()
    if 'username' not in login_session \
            or creator.id != login_session['user_id']:
        return render_template('publicmenu.html',
                               items=items, shop=shop, )
    else:
        return render_template('menu.html',
                               items=items, shop=shop, )


@app.route('/shop/<int:shop_id>/menu/JSON')
def shopMenuJSON(shop_id):
    shop = session.query(Shop).filter_by(id=shop_id).one()
    items = session.query(MenuItem).filter_by(
        shop_id=shop_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/shop/<int:shop_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(shop_id, menu_id):
    Menu_Item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(Menu_Item=Menu_Item.serialize)


@app.route('/shop/JSON')
def shopsJSON():
    shops = session.query(Shop).all()
    return jsonify(shops=[r.serialize for r in shops])


# Create a new shop
@app.route('/shop/new/', methods=['GET', 'POST'])
def newShop():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newShop = Shop(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(newShop)
        flash('New shop %s Successfully Created' % newShop.name)
        session.commit()
        return redirect(url_for('showShop'))
    else:
        return render_template('newShop.html')


# Edit a shop
@app.route('/shop/<int:shop_id>/edit/', methods=['GET', 'POST'])
def editShop(shop_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedShop = session.query(Shop).filter_by(id=shop_id).one()
    if editedShop.user_id != login_session['user_id']:
        return "<script>function myFunction() " \
               "{alert('You are not authorized to edit this shop." \
               " Please create your own shop in order to edit.');}" \
               "</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedShop.name = request.form['name']
            flash('Shop Successfully Edited %s' % editedShop.name)
            return redirect(url_for('showShop'))
    else:
        return render_template('editShop.html', shop=editedShop)


# Delete a shop
@app.route('/shop/<int:shop_id>/delete/', methods=['GET', 'POST'])
def deleteShop(shop_id):
    if 'username' not in login_session:
        return redirect('/login')
    shopToDelete = session.query(Shop).filter_by(id=shop_id).one()
    if shopToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() " \
               "{alert('You are not authorized to edit this shop." \
               " Please create your own shop in order to edit.');}" \
               "</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(shopToDelete)
        flash('%s Successfully Deleted' % shopToDelete.name)
        session.commit()
        return redirect(url_for('showShop', shop_id=shop_id))
    else:
        return render_template('deleteShop.html', shop=shopToDelete)


# Create a new menu item
@app.route('/shop/<int:shop_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(shop_id):
    if 'username' not in login_session:
        return redirect('/login')
    shop = session.query(Shop).filter_by(id=shop_id).one()
    if login_session['user_id'] != shop.user_id:
        return "<script>function myFunction() " \
               "{alert('You are not authorized to edit this shop." \
               " Please create your own shop in order to edit.');}" \
               "</script><body onload='myFunction()''>"
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'],
                           description=request.form['description'],
                           image=request.form['image'],
                           price=request.form['price'],
                           shop_id=shop_id,
                           user_id=shop.user_id)
        session.add(newItem)
        session.commit()
        flash('New Menu %s Item Successfully Created' % (newItem.name))
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['image']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file', filename=filename))
        return redirect(url_for('showShop', shop_id=shop_id))
    else:
        return render_template('newmenuitem.html', shop_id=shop_id)


# Edit a menu item
@app.route('/shop/<int:shop_id>/menu/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editMenuItem(shop_id, menu_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    shop = session.query(Shop).filter_by(id=shop_id).one()
    if login_session['user_id'] != shop.user_id:
        return "<script>function myFunction() " \
               "{alert('You are not authorized to edit this shop." \
               " Please create your own shop in order to edit.');}" \
               "</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['image']:
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['image']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('upload_file', filename=filename))
        session.add(editedItem)
        session.commit()
        flash('Menu Item Successfully Edited')
        return redirect(url_for('showMenu', shop_id=shop_id))
    else:
        return render_template('editmenuitem.html',
                               shop_id=shop_id,
                               menu_id=menu_id,
                               item=editedItem)


# Delete a menu item
@app.route('/shop/<int:shop_id>/menu/<int:menu_id>/delete',
           methods=['GET', 'POST'])
def deleteMenuItem(shop_id, menu_id):
    if 'username' not in login_session:
        return redirect('/login')
    shop = session.query(Shop).filter_by(id=shop_id).one()
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if login_session['user_id'] != shop.user_id:
        return "<script>function myFunction() " \
               "{alert('You are not authorized to edit this shop." \
               " Please create your own shop in order to edit.');}" \
               "</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('showMenu', shop_id=shop_id))
    else:
        return render_template('deleteMenuItem.html', item=itemToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='127.0.0.1', port=5555)
