#Linux Server Configuration

Installed and configured all required software to turn a baseline Ubuntu Amazon Web Services server into a fully functional web application server, including Apache Web Server and PostgreSQL database server.

<b>Skills:</b> SSH, Linux, Apache, PostgreSQL

## Setup Project:

1) Create a new user named grader
```bash
adduser ubuntu
```
2) Give the grader the permission to sudo
```bash
visudo  
ubuntu ALL=(ALL:ALL) ALL
```
3) Update all currently installed packages
```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get dist-upgrade
```
4) Change the SSH port from 22 to 2200
```bash

Change Port from 22 to 2200
Change PermitRootLogin from without-password to no
Change PasswordAuthentication from yes to no
```
Restart SSH Service:
```bash
/etc/init.d/ssh restart
```
5) Allow user to login through ssh as grader with the same private key that can be used to login as root:
```bash
mkdir /home/ubuntu/.ssh
sudo cp ~/.ssh/authorized_keys /home/ubuntu/.ssh/
chmod 700 /home/ubuntu/.ssh
chmod 644 /home/ubuntu/.ssh/authorized_keys
sudo chown -R ubuntu:ubuntu /home/ubuntu/.ssh
```

6) Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and HTTPS (port 443)
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 2200/tcp
sudo ufw status
sudo ufw enable
```

7) Configure the local timezone to UTC

    Type the below command and select the required time zone.
```bash
sudo dpkg-reconfigure tzdata
```
8) Reboot system
```bash
sudo reboot
```
9) Install and configure Niginx 
```bash
sudo apt-get install nginx
```
10) Add policy to ufw.
```bash
sudo ufw allow 'Nginx Full'
```
11) Install LetsenCrypt Certbot
```bash
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
sudo apt-get install python-certbot-nginx
sudo certbot --nginx -d [SITE]
sudo certbot renew --dry-run
```
12) Enable site
```bash
ln -s /etc/nginx/sites-available/communication.levellab.ru /etc/nginx/sites-enabled/
nginx -t
```
13) Install and configure PostgreSQL.
```bash
sudo apt-get install postgresql postgresql-contrib python-psycopg2 libpq-dev
```
14) Configure PostgreSQL.
```bash
su - postgres
createdb [DB_NAME]
psql -s [DB_NAME]
create user [USER_NAME] password '[USER_PASSWORD]';
GRANT ALL PRIVILEGES ON DATABASE [DB_NAME] TO [USER_NAME];
```
Open the file pg_hba.conf for Ubuntu it will be in /etc/postgresql/9.x/main and add this line:
```bash
local   all             [USER_NAME]                                trust

```
Restart the server
```bash
sudo service postgresql restart
```
15) Restore PostgreSQL backup:
```bash
psql [DB_NAME] [USER_NAME] < [BACKUP_NAME].dump
```
16) Install git
```bash
sudo apt-get install git 
```
17) Install and configure Niginx to serve a Python mod_wsgi application
```bash
sudo apt-get install python-setuptools libapache2-mod-wsgi
sudo service nginx restart
```

18) Install lib for PostgreSQL
```bash
sudo apt-get install postgresql-contrib python-psycopg2 libpq-dev
```
19) Install pip3 and use python 3 defult:
```bash
alias python=/usr/bin/python3
sudo apt-get install python-pip
 ```

## BackUP
1. Backup PostgreSQL
```bash
pg_dump -U [USER_NAME] [DB_NAME]  -f [BACKUP_NAME].dump
```
