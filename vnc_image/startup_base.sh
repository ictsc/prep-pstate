#!/bin/sh

apt-get update

##Add user
useradd -m -s /bin/bash ictsc-admin
echo "ictsc-admin:iCtsC2O18" | chpasswd
gpasswd -a ictsc-admin sudo

## ip forwording
echo 'net.ipv4.ip_forward=1' >> /etc/sysctl.conf
echo "1" > /proc/sys/net/ipv4/ip_forward

## NAPT
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
iptables -A FORWARD -i eth1 -o eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT

## NAPT permanent
iptables-save > iptables.dat
echo 'iptables-restore < /root/iptables.dat' >> /etc/rc.local

## install the desktop for ubuntu
apt-get -y install xubuntu-desktop

## VNC server
apt-get -y install tightvncserver
mkdir /home/ubuntu/.vnc
chown ubuntu:ubuntu /home/ubuntu/.vnc

## vnc port setting
-A INPUT -p tcp --dport 5901 -j ACCEPT

## vncserver@\:1.service
cat << EOF > /etc/systemd/system/vncserver@:1.service
[Unit]
Description = VNC Server

[Service]
Type=forking
# Clean any existing files in /tmp/.X11-unix environment
ExecStartPre=/bin/sh -c '/usr/bin/vncserver -kill %i > /dev/null 2>&1 || :'
ExecStart=/sbin/runuser -l ubuntu -c "/usr/bin/vncserver %i"
PIDFile=/home/ubuntu/.vnc/%H%i.pid
ExecStop=/bin/sh -c '/usr/bin/vncserver -kill %i > /dev/null 2>&1 || :'
EOF


cat << EOF > /home/ubuntu/.vnc/xstartup
#!/bin/sh

# Uncomment the following two lines for normal desktop:
# unset SESSION_MANAGER
# exec /etc/X11/xinit/xinitrc

[ -x /etc/vnc/xstartup ] && exec /etc/vnc/xstartup
[ -r $HOME/.Xresources ] && xrdb $HOME/.Xresources
xsetroot -solid grey
vncconfig -iconic &
x-terminal-emulator -geometry 1280x1024 -ls -title "$VNCDESKTOP Desktop" &
x-window-manager &
exec xfce4-session &
EOF

chmod 744 /home/ubuntu/.vnc/xstartup
chown ubuntu:ubuntu /home/ubuntu/.vnc/xstartup