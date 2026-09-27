# Linux Server Configuration

1) Create a new user
```bash
adduser ubuntu
```
2) Give the permission to sudo
```bash
usermod -aG sudo ubuntu
```

3) Update all currently installed packages
```bash
apt update
apt -y upgrade
apt -y dist-upgrade
```
4) Allow user to login through ssh with the same private key that can be used to login as root:
```bash
mkdir -p /home/ubuntu/.ssh
cp /root/.ssh/authorized_keys /home/ubuntu/.ssh/
chmod 700 /home/ubuntu/.ssh
chmod 600 /home/ubuntu/.ssh/authorized_keys
chown -R ubuntu:ubuntu /home/ubuntu/.ssh
```
5) Change the SSH port from 22 to 2200
```bash
cat > /etc/ssh/sshd_config.d/00-hardening.conf <<'EOF'
Port 2200
PermitRootLogin no
PasswordAuthentication no
EOF
```
```bash
sshd -t
systemctl disable --now ssh.socket
systemctl enable --now ssh.service
systemctl restart ssh
```
6) Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and HTTPS (port 443)
```bash
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 2200/tcp
ufw status
ufw enable
```

7) Configure the local timezone to Europe/Moscow.
```bash
timedatectl set-timezone Europe/Moscow
```
8) Setup unattended-upgrades
```bash
apt install unattended-upgrades
```
```bash
dpkg-reconfigure -plow unattended-upgrades
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
vim /etc/fail2ban/jail.local
```
```bash
[sshd]
enabled = true
mode = normal
port = 2200
backend = systemd
```
```bash
systemctl enable fail2ban
systemctl restart fail2ban
systemctl status fail2ban
```

10) Reboot system
```bash
reboot
```
