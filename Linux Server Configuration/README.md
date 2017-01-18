Linux Server Configuration

Installed and configured all required software to turn a baseline Ubuntu Amazon Web Services server into a fully functional web application server, including Apache Web Server and PostgreSQL database server.

Skills: SSH, Linux, Apache, PostgreSQL

Setup Project:

1) Create a new user named grader

    adduser grader

2) Give the grader the permission to sudo

    visudo
    grader ALL=(ALL:ALL) ALL

3) Update all currently installed packages

    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get dist-upgrade

4) Change the SSH port from 22 to 2200

    nano /etc/ssh/sshd_config
    Change Port from 22 to 2200
    Change PermitRootLogin from without-password to no
    Change PasswordAuthentication from no to yes

    Restart SSH Service:
    /etc/init.d/ssh restart

5) Allow user to login through ssh as grader with the same private key that can be used to login as root:

   su grader
   mkdir ~/.ssh
   chmod 777 ~/.ssh
   sudo cp /root/.ssh/authorized_keys ~/.ssh/
   sudo chown grader:grader ~/.ssh/authorized_keys



6) Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123)

#Allow incoming TCP packets on port 2200 (SSH) $ sudo ufw allow 2200/tcp
#Allow incoming TCP packets on port 80 (HTTP)
#Allow incoming UDP packets on port 123 (NTP)

    sudo ufw enable
    sudo ufw allow 80/tcp
    sudo ufw allow 123/udp
    sudo ufw allow 2200/tcp


7) Configure the local timezone to UTC

#Type the below command and select the required time zone.

    sudo dpkg-reconfigure tzdata

8) Reboot system

    sudo reboot

9) Install and configure Apache to serve a Python mod_wsgi application

Install Apache

    sudo apt-get install apache2

Install mod_wsgi

    sudo apt-get install python-setuptools libapache2-mod-wsgi

Restart Apache

    sudo service apache2 restart

10) Install and configure PostgreSQL

Install PostgreSQL:

    sudo apt-get install postgresql postgresql-contrib python-psycopg2 libpq-dev

11) Install pip3 and use python 3 defult:

    alias python=/usr/bin/python3
    sudo apt-get install python-pip
    

12) Check that no remote connections are allowed (default):
    sudo nano /etc/postgresql/9.3/main/pg_hba.conf


13) Create needed linux user for psql 
    
    sudo adduser catalog

14) Change to default user postgres sudo su - postgre
    
    sudo -u postgres -i

    Connect:

    psql
    
    Add postgres user and allw user to create database:

    CREATE USER catalog WITH PASSWORD 'PWD';
    ALTER USER catalog CREATEDB;

    Create database:
    
    CREATE DATABASE catalog WITH OWNER catalog;

    Connect to the database catalog 

    \c catalog

    Revoke all rights:

    REVOKE ALL ON SCHEMA public FROM public;

    Grant only access to the catalog role:

    GRANT ALL ON SCHEMA public TO catalog;

    Exit out of PostgreSQl and the postgres user:

    \q
    exit

15) install git

    sudo apt-get install git 

16) Download CARALOG project from GitHub

    cd
    sudo git clone https://github.com/MrJackJones/Shop_catalog.git

17) move site file to /

    cd /var/www 
    sudo mkdir FlaskAppv
    cd FlaskApp
    sudo mkdir FlaskApp
    cd FlaskApp
    cp -r ~/Shop_catalog/* .

18) change DB in database_setup.py, finalproject, lotsofmenus.py

    postgresql://catalog:PWD@localhost/catalog

19) rename finalproject.py 

    sudo mv finalproject.py __init__.py

20) edit path on file __init__.py for client_secrets.json

    /var/www/FlaskApp/FlaskApp/client_secrets.json

21) Inastall all package from requirements.txt, use:

    sudo pip install -r requirements.txt

22) run database_setup.py to create the database:

    sudo python database_setup.py

23) run lotsofmenus.py to populate the database:

    sudo python lotsofmenus.py

24) Configure and Enable a New Virtual Host
    
    sudo nano /etc/apache2/sites-available/FlaskApp.conf

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

    sudo a2ensite FlaskApp

25) Create the .wsgi File

    cd /var/www/FlaskApp
    sudo nano flaskapp.wsgi 

    #!/usr/bin/python
    import sys
    import logging
    logging.basicConfig(stream=sys.stderr)
    sys.path.insert(0,"/var/www/FlaskApp/")

    from FlaskApp import app as application
    application.secret_key = 'super_secret_key'

26) Restart Apache

    sudo service apache2 restart

27) Navigate to localhost:5555 in your browser