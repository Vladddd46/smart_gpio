## Installation

### OpenWRT router
1. Connect to the OpenWRT server via SSH:
~~~
user@host:~@$ ssh root@192.168.1.3
root@192.168.1.3's password: 


BusyBox v1.36.1 (2024-09-04 10:39:36 UTC) built-in shell (ash)

  _______                     ________        __
 |       |.-----.-----.-----.|  |  |  |.----.|  |_
 |   -   ||  _  |  -__|     ||  |  |  ||   _||   _|
 |_______||   __|_____|__|__||________||__|  |____|
          |__| W I R E L E S S   F R E E D O M
 -----------------------------------------------------
 OpenWrt SNAPSHOT, r27299-66559946ac
 -----------------------------------------------------
root@OpenWrt:~# 

~~~ 
2. Install all required software to the OpenWRT server:
~~~
root@OpenWrt:~# opkg update
root@OpenWrt:~# opkg install git-http git coreutils-nohup nano
~~~
3. Clone the project to the OpenWRT server:
~~~
root@OpenWrt:~# git clone https://github.com/Vladddd46/smart_gpio.git
~~~
4. Add execute permission for the script:
~~~
root@OpenWrt:~# cd smart_gpio
root@OpenWrt:~# chmod +x scripts/start_web_server.sh
~~~
5. Add the script to autoload by inserting the following line before 'exit 0':
~~~
root@OpenWrt:~# nano /etc/rc.local
nohup /root/smart_gpio/scripts/start_web_server.sh > /dev/null 2>&1 &
~~~
If you want to write logs, use the following line instead:
~~~
root@OpenWrt:~# nano /etc/rc.local
mkdir -p /var/log/smart_gpio
DATE=`date +%d-%m-%y-%T`
nohup /root/smart_gpio/scripts/start_web_server.sh 2>&1  & tee -a /var/log/smart_gpio/start_web_server_${DATE}.log &
~~~
**WARNING:** Be careful using logs, you can use up all free disk space
6. Reboot the device:
~~~
root@OpenWrt:~# reboot
~~~

### Raspberry Pi Zero W relay server
1. Exctract microSD card from the device. Insert the card to the cardreader then open as a disk.
Edit the following file on the card:
~~~
user@host:~ nano /media/user/rootfs/etc/wpa_supplicant
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=UA

network={
	ssid="YourSSID"
	psk="YourPassword"
}
~~~
2. Insert the card to the device and then power it on
3. Open LuCi web interface on the OpenWRT router and find the raspberrypi IP 
4. Connect to the Raspbery Pi Zero W via SSH (password by default is "raspberry"):
~~~
user@host:~ ssh pi192.168.1.10
pi@192.168.1.10's password: 
Linux raspberrypi 5.10.17+ #1414 Fri Apr 30 13:16:27 BST 2021 armv6l

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Thu May 23 10:11:53 2024 from 192.168.1.212

SSH is enabled and the default password for the 'pi' user has not been changed.
This is a security risk - please login as the 'pi' user and type 'passwd' to set a new password.

pi@raspberrypi:~ $ 

~~~
5. Clone the project to the device:
~~~
pi@raspberrypi:~ $ git clone https://github.com/Vladddd46/smart_gpio.git
~~~
6. Add execute permission for the script:
~~~
pi@raspberrypi:~ cd smart_gpio
pi@raspberrypi:~ chmod +x scripts/start_relay_controller.sh
~~~
7. Add the script to autoload by inserting the following line before 'exit 0':
~~~
pi@raspberrypi:~ sudo nano /etc/rc.local
nohup /home/pi/smart_gpio/scripts/start_relay_controller.sh > /dev/null 2>&1 &
~~~
If you want to write logs, use the following line instead:
~~~
root@OpenWrt:~# nano /etc/rc.local
mkdir -p /var/log/smart_gpio
DATE=`date +%d-%m-%y-%T`
nohup /home/pi/smart_gpio/scripts/start_relay_controller.sh 2>&1  & tee -a /var/log/smart_gpio/start_relay_controller_${DATE}.log &
~~~
**WARNING:** Be careful using logs, you can use up all free disk space
8. Reboot the device:
~~~
pi@raspberrypi:~ sudo reboot
~~~