<h1>Linux Server Configuration</h1>

Installed and configured all required software to turn a baseline Ubuntu Amazon Web Services server into a fully functional web application server, including Apache Web Server and PostgreSQL database server.

<b>Skills:</b> SSH, Linux, Apache, PostgreSQL

<h2>Setup Project:</h2>

1) Create a new user named grader
```
	adduser ubuntu
```
2) Give the grader the permission to sudo
```
	visudo  
	ubuntu ALL=(ALL:ALL) ALL
```
3) Update all currently installed packages
```
	sudo apt-get update
	sudo apt-get upgrade
	sudo apt-get dist-upgrade
```
4) Change the SSH port from 22 to 2200
```
	nano /etc/ssh/sshd_config
	Change Port from 22 to 2200
	Change PermitRootLogin from without-password to no
	Change PasswordAuthentication from no to yes
```	
Restart SSH Service:
```
	/etc/init.d/ssh restart
```
5) Allow user to login through ssh as grader with the same private key that can be used to login as root:
```
	mkdir /home/ubuntu/.ssh
	sudo cp ~/.ssh/authorized_keys /home/ubuntu/.ssh/
	chmod 700 /home/ubuntu/.ssh
	chmod 644 /home/ubuntu/.ssh/authorized_keys
	sudo chown -R ubuntu:ubuntu /home/ubuntu/.ssh
```

6) Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and HTTPS (port 443)
```
	sudo ufw allow 80/tcp
	sudo ufw allow 443/tcp
	sudo ufw allow 2200/tcp
	sudo ufw status
	sudo ufw allow 'Nginx Full'
	sudo ufw status
	sudo ufw enable
```

7) Configure the local timezone to UTC

    Type the below command and select the required time zone.
```
	sudo dpkg-reconfigure tzdata
```
8) Reboot system
```
	sudo reboot
```
9) Install LetsenCrypt Certbot
```
	sudo add-apt-repository ppa:certbot/certbot
	sudo apt-get update
	sudo apt-get install python-certbot-nginx
	sudo certbot --nginx -d [SITE]
	sudo certbot renew --dry-run
```

10) Install and configure Niginx to serve a Python mod_wsgi application

    Install Apache
```
	sudo apt-get install nginx
```
    Install mod_wsgi
```
	sudo apt-get install python-setuptools libapache2-mod-wsgi
```
    Restart Apache
```
	sudo service nginx restart
```
11) Install and configure PostgreSQL

    Install PostgreSQL:
```
	sudo apt-get install postgresql postgresql-contrib python-psycopg2 libpq-dev
```
12) Install pip3 and use python 3 defult:
```
	alias python=/usr/bin/python3
 	sudo apt-get install python-pip
 ```   

13) Check that no remote connections are allowed (default):
```
	sudo nano /etc/postgresql/9.3/main/pg_hba.conf
```

14) Create needed linux user for psql 
```    
	sudo adduser catalog
```
15) Change to default user postgres sudo su - postgre
```   
    sudo -u postgres -i
```
```
    Connect:
    psql
```
    Add postgres user and allw user to create database:
```
    CREATE USER catalog WITH PASSWORD 'PWD';
    ALTER USER catalog CREATEDB;
```
    Create database:
```    
    CREATE DATABASE catalog WITH OWNER catalog;
```
    Connect to the database catalog: 
```
    \c catalog
```
    Revoke all rights:
```
    REVOKE ALL ON SCHEMA public FROM public;

    Grant only access to the catalog role:

    GRANT ALL ON SCHEMA public TO catalog;
```
    Exit out of PostgreSQl and the postgres user:
```
    \q
```
16) install git
```
    sudo apt-get install git 
```
17) Download CARALOG project from GitHub
```
    cd
    sudo git clone https://github.com/MrJackJones/Shop_catalog.git
```
18) move site file to /
```
    cd /var/www 
    sudo mkdir FlaskAppv
    cd FlaskApp
    sudo mkdir FlaskApp
    cd FlaskApp
    cp -r ~/Shop_catalog/* .
```
19) change DB in database_setup.py, finalproject, lotsofmenus.py
```
    postgresql://catalog:PWD@localhost/catalog
```
20) rename finalproject.py 
```
    sudo mv finalproject.py __init__.py
```
21) edit path on file __init__.py for client_secrets.json
```
    /var/www/FlaskApp/FlaskApp/client_secrets.json
```
22) Inastall all package from requirements.txt, use:
```
    sudo pip install -r requirements.txt
```
23) run database_setup.py to create the database:
```
    sudo python database_setup.py
```
24) run lotsofmenus.py to populate the database:
```
    sudo python lotsofmenus.py
```
25) Configure and Enable a New Virtual Host
```   
    sudo nano /etc/apache2/sites-available/FlaskApp.conf
```
```
    <VirtualHost *:80>
            ServerName justmetoyou.ru
            ServerAdmin ajustmetoyou@yandex.ru
            WSGIScriptAlias / /var/www/FlaskApp/flaskapp.wsgi
            <Directory /var/www/FlaskApp/FlaskApp/>
                Order allow,deny
                Allow from all
            </Directory>
            Alias /static /var/www/FlaskApp/FlaskApp/static
            <Directory /var/www/FlaskApp/FlaskApp/static/>
                Order allow,deny
                Allow from all
            </Directory>
            ErrorLog /var/www/FlaskApp/error.log
            LogLevel warn
            CustomLog /var/www/FlaskApp/access.log combined
    </VirtualHost>
```
```
    sudo a2ensite FlaskApp
```
26) Create the .wsgi File
```
    cd /var/www/FlaskApp
    sudo nano flaskapp.wsgi 

    #!/usr/bin/python
    import sys
    import logging
    logging.basicConfig(stream=sys.stderr)
    sys.path.insert(0,"/var/www/FlaskApp/")

    from FlaskApp import app as application
    application.secret_key = 'super_secret_key'
```
27) Restart Apache
```
    sudo service apache2 restart
```
28) Navigate to SERVER_IP:5555 in your browser
