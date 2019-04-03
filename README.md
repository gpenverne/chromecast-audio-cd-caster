# Stream an audio cd to a chromecast

We will use an icecast server, to install it:
```bash
$ sudo apt-get install icecast2
```
Icecast2 server will broadcast the audio feed

And we need ffmpeg, which will stream audio cd to icecast2 feed:
```bash
$ sudo apt-get install ffmpeg
```

Some configuration, for icecast2: edit the ``/etc/icecast2/icecast.xml`` file, and check the authentication part:
```xml
    <authentication>
        <!-- Sources log in with username 'source' -->
        <source-password>YOUR_PASSWORD</source-password>
        <!-- Relays log in with username 'relay' -->
        <relay-password>YOUR_PASSWORD</relay-password>

        <!-- Admin logs in with the username given below -->
        <admin-user>admin</admin-user>
        <admin-password>YOUR_PASSWORD</admin-password>
    </authentication>
```
And the hostname and socket part:
```xml
<hostname>localhost</hostname>

<!-- You may have multiple <listener> elements -->
<listen-socket>
    <port>8000</port>
    <!-- <bind-address>127.0.0.1</bind-address> -->
    <!-- <shoutcast-mount>/stream</shoutcast-mount> -->
</listen-socket>
```
You can see the full config file in the [Chromecast-audio-cd-caster repo](https://github.com/gpenverne/chromecast-audio-cd-caster)

To stream using ffmpeg, simply use:
```bash
/usr/bin/ffmpeg  -f libcdio -ss 0 -i /dev/cdrom -acodec libmp3lame -ab 48k -bufsize 15 -ac 1 -content_type audio/mpeg -f mp3  icecast://source:YOUR_PASSWORD@192.168.0.31:8000/raspi
```
(Don't forget to replace 192.168.0.31 by your raspberry pi local ip)

You have now a feed readable from http://192.168.0.31:8000/raspi

### How to cast?
To cast what you want to a chromecast, have a look on [Pychromecast](https://github.com/balloob/pychromecast)
Of course, you need python3:
```bash
$ sudo apt-get install python3
```

And a tiny python script:
```python
import time
import pychromecast
import urllib.request

stream_url = 'http://192.168.0.31:8000/raspi'
chromecasts = pychromecast.get_chromecasts()
cast = next(cc for cc in chromecasts if cc.device.friendly_name == "Salon")
cast.wait()
print(cast.device)
print(cast.status)
mc = cast.media_controller
while urllib.request.urlopen(stream_url).getcode() != 200:
    print('Waiting for stream up')
    time.sleep(1)

mc.play_media(stream_url, 'audio/mp3')
mc.block_until_active()
print(mc.status)
mc.play()
```

And ... it's a kind of magic:
```bash
$ /usr/bin/ffmpeg  -f libcdio -ss 0 -i /dev/cdrom -acodec libmp3lame -ab 48k -bufsize 15 -ac 1 -content_type audio/mpeg -f mp3  icecast://source:SOURCE_PASSWORD@192.168.0.31:8000/raspi & /usr/bin/python3 /home/pi/audio/cast.py
```

### Bonus: autostart on cd insertion
We will use an udev rule, for example in a ``/etc/udev/rules.d/99-cd-audio-processing.rules`` rule:
```
SUBSYSTEM=="block", KERNEL=="sr0", ACTION=="change", RUN+="/home/pi/audio/start-cd.sh &"
```

Reboot, and you're ready :)

