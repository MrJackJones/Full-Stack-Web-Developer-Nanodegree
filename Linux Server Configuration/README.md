# Linux Server Configuration

Installed and configured all required software to turn a baseline Ubuntu Amazon Web Services server into a fully functional web application server, including Apache Web Server and PostgreSQL database server.

<b>Skills:</b> SSH, Linux, Apache, PostgreSQL

## Setup Project:

1) Create a new user named grader
```bash
adduser ubuntu
```
2) Give the grader the permission to sudo
```bash
usermod -aG sudo ubuntu
```

3) Update all currently installed packages
```bash
apt-get update
apt-get upgrade
apt-get dist-upgrade
```
4) Change the SSH port from 22 to 2200
```bash
vim /etc/ssh/sshd_config
```
```bash
Change Port from 22 to 2200
Change PermitRootLogin from without-password to no
Change PasswordAuthentication from yes to no
```
5) Allow user to login through ssh as grader with the same private key that can be used to login as root:
```bash
mkdir /home/ubuntu/.ssh
cp ~/.ssh/authorized_keys /home/ubuntu/.ssh/
chmod 700 /home/ubuntu/.ssh
chmod 644 /home/ubuntu/.ssh/authorized_keys
chown -R ubuntu:ubuntu /home/ubuntu/.ssh
rm /root/.ssh/authorized_keys
```
Restart SSH Service:
```bash
/etc/init.d/ssh restart
```
6) Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and HTTPS (port 443)
```bash
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 2200/tcp
ufw status
ufw enable
```

7) Configure the local timezone to UTC.
```bash
dpkg-reconfigure tzdata
```
8) Setup unattended-upgrades
```bash
apt install unattended-upgrades
```
```bash
systemctl status unattended-upgrades
```
9) Setup fail2ban
```bash
apt install fail2ban
```
```bash
cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
```
```bash
journalctl -u ssh
```
```bash
vi /etc/fail2ban/jail.local
```
```bash
[sshd]

enabled = true
mode = aggressive
port    = ssh
logpath = %(sshd_log)s
backend = systemd
```
```bash
systemctl enable fail2ban
systemctl restart fail2ban
systemctl status fail2ban
```
```bash
tail -f /var/log/fail2ban.log
fail2ban-client status sshd
```

10) Reboot system
```bash
reboot
```
