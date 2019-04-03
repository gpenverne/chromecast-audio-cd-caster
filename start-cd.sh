#!/bin/bash

killall -9 ffmpeg
killall -9 ffmpeg
/usr/bin/ffmpeg  -f libcdio -ss 0 -i /dev/cdrom -acodec libmp3lame -ab 48k -bufsize 15 -ac 1 -content_type audio/mpeg -f mp3  icecast://source:SOURCE_PASSWORD@192.168.0.31:8000/raspi &
/usr/bin/python3 /home/pi/audio/cast.py

