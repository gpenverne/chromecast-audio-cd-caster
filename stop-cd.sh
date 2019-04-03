#/bin/bash

killall -9 ffmpeg
killall -9 ffmpeg
/usr/sbin/service icecast2 restart
/usr/bin/python3 /home/pi/audio/stop-cast.py
