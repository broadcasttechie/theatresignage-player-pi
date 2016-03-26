#!/bin/bash

# curl -sL https://raw.githubusercontent.com/broadcasttechie/theatresignage-player-pi/master/install.sh | bash
# Theatre Signage Player installer
# 25th March 2016

echo "Installing Theatre Signage Player"


## Simple disk storage check. Naively assumes root partition holds all system data.
ROOT_AVAIL=$(df -k / | tail -n 1 | awk {'print $4'})
MIN_REQ="512000"

if [ $ROOT_AVAIL -lt $MIN_REQ ]; then
	echo "Insufficient disk space. Make sure you have at least 500MB available on the root partition."
	read -p "Use raspi-config to expand root fs and reboot."
	sudo raspi-config
	sudo reboot
	exit 1
fi



echo "Updating system"

sudo apt-get update
sudo apt-get upgrade

echo "Install some stuff"

sudo dpkg-reconfigure ssh

sudo apt-get install -y scrot git lsb-core fbi uzbl matchbox-window-manager supervisor x11-xserver-utils ttf-mscorefonts-installer xwit sqlite3 libnss3 python-pip python-dev python-simplejson python-imaging uzbl sqlite3 omxplayer x11-xserver-utils libx11-dev watchdog chkconfig

echo "Install Hamachi"
wget https://secure.logmein.com/labs/logmein-hamachi_2.1.0.139-1_armhf.deb
sudo dpkg -i logmein-hamachi_2.1.0.139-1_armhf.deb 
sudo hamachi login
sudo hamachi attach kristan@webbitpro.co.uk

echo "Configure ntp"
#http://raspberrypi.stackexchange.com/questions/266/how-can-i-keep-system-time
#https://www.raspberrypi.org/forums/viewtopic.php?f=91&t=16058
sudo echo "DAEMONS(!hwclock ntpd ntpdate)" >> /etc/rc.conf
sudo ln -sf /usr/share/zoneinfo/Europe/London /etc/localtime

echo "Python stuff"

sudo pip install Mako MarkupSafe PyHAML bottle bottle-haml hurry.filesize netifaces pytz requests sh==1.08 six uptime wsgiref werkzeug pyscreenshot


echo "Install player"
git clone https://github.com/broadcasttechie/theatresignage-player-pi.git "$HOME/ts"


echo "Configure player startup"
#http://blogs.wcode.org/2013/09/howto-boot-your-raspberry-pi-into-a-fullscreen-browser-kiosk/


sudo sed -i -e '$i \/etc/init.d/logmein-hamachi start' /etc/rc.local
sudo sed -i -e '$i \hamachi login \&\n' /etc/rc.local

sudo sed -i -e '$i \if \[ \-f /boot/xinitrc \]\; then' /etc/rc.local
sudo sed -i -e '$i \    \tln -fs /boot/xinitrc /home/pi/\.xinitrc;' /etc/rc.local
sudo sed -i -e '$i \su - pi -c startx \& ' /etc/rc.local
sudo sed -i -e '$i \fi\n' /etc/rc.local

sudo cp $HOME/ts/misc/xinitrc /boot/xinitrc

#TODO must prompt for server and channel number

sudo chmod a+x $HOME/ts/player.py
sudo chmod a+x $HOME/ts/server/server.py

echo "Configure supervisor"
echo "Adding Screenly to autostart (via Supervisord)"
#sudo ln -s "$HOME/ts/misc/supervisord.conf" /etc/supervisor/supervisord.conf
#sudo ln -s "$HOME/ts/misc/supervisord.conf" /etc/supervisord.conf
sudo ln -s "$HOME/ts/misc/supervisor_player.conf" /etc/supervisor/conf.d/player.conf
sudo ln -s "$HOME/ts/misc/supervisor_server.conf" /etc/supervisor/conf.d/server.conf
sudo supervisorctl reread


echo "Increasing swap space to 500MB..."
echo "CONF_SWAPSIZE=500" > "$HOME/dphys-swapfile"
sudo cp /etc/dphys-swapfile /etc/dphys-swapfile.bak
sudo mv "$HOME/dphys-swapfile" /etc/dphys-swapfile


echo "Enabling Watchdog..."
sudo modprobe bcm2708_wdog > /dev/null
sudo cp /etc/modules /etc/modules.bak
sudo sed '$ i\bcm2708_wdog' -i /etc/modules
sudo chkconfig watchdog on
sudo cp /etc/watchdog.conf /etc/watchdog.conf.bak
sudo sed -e 's/#watchdog-device/watchdog-device/g' -i /etc/watchdog.conf
sudo /etc/init.d/watchdog start


# Make sure we have proper framebuffer depth.
if grep -q framebuffer_depth /boot/config.txt; then
  sudo sed 's/^framebuffer_depth.*/framebuffer_depth=32/' -i /boot/config.txt
else
  echo 'framebuffer_depth=32' | sudo tee -a /boot/config.txt > /dev/null
fi

# Fix frame buffer bug
if grep -q framebuffer_ignore_alpha /boot/config.txt; then
  sudo sed 's/^framebuffer_ignore_alpha.*/framebuffer_ignore_alpha=1/' -i /boot/config.txt
else
  echo 'framebuffer_ignore_alpha=1' | sudo tee -a /boot/config.txt > /dev/null
fi

echo "Install boot splash"
#http://www.edv-huber.com/index.php/problemloesungen/15-custom-splash-screen-for-raspberry-pi-raspbian
sudo cp $HOME/ts/misc/asplashscreen /etc/init.d/asplashscreen
sudo cp $HOME/ts/misc/pi_loading.png /etc/splash.png
sudo chmod a+x /etc/init.d/asplashscreen
sudo insserv /etc/init.d/asplashscreen


echo "Quiet the boot process..."
sudo cp /boot/cmdline.txt /boot/cmdline.txt.bak
sudo sed 's/$/ quiet/' -i /boot/cmdline.txt

