#!/usr/bin/env bash
## Change the password for ubuntu user
echo "ubuntu:@@VNC_SERVER_PASSWORD@@" | chpasswd

## Interface setting
echo 'auto eth1' >> /etc/network/interfaces
echo 'iface eth1 inet static' >> /etc/network/interfaces
echo 'address 192.168.0.254' >> /etc/network/interfaces
echo 'netmask 255.255.255.0' >> /etc/network/interfaces
service networking restart

## VNC server settings
echo @@VNC_SERVER_PASSWORD@@ | vncpasswd -f > "/home/ubuntu/.vnc/passwd"
chmod 700 /home/ubuntu/.vnc/passwd
chown ubuntu:ubuntu /home/ubuntu/.vnc/passwd

systemctl daemon-reload
systemctl start vncserver@\:1.service
systemctl enable vncserver@\:1.service