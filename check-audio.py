#!/usr/local/bin/python3

import pychromecast
import sys
import os
import time
import urllib
import subprocess
import pygame
#import pychromecast


lockFile='/tmp/lock-audio'
import os
class StatusListener:
    def __init__(self, name, cast):
        self.name = name
        self.cast = cast

    def new_cast_status(self, status):
        print('[',time.ctime(),' - ', self.name,'] status chromecast change:')
        if not status.app_id:
            print('Turn off')
            #if os.path.isfile(lockFile):
            cdrom=pygame.cdrom.CD(0)
            cdrom.eject()
            subprocess.call("killall -9 ffmpeg", shell=True)
            subprocess.call("/usr/bin/eject /dev/sr0", shell=True)
            #urllib.request.urlopen("http://192.168.0.20/recipes/exec/audio?state=off").read()
        else:
            #if not os.path.isfile(lockFile):
            print('Turn on')
            #urllib.request.urlopen("http://192.168.0.20/recipes/exec/audio?state=on").read()
        print(status)
        time.sleep(3)



class StatusMediaListener:
    def __init__(self, name, cast):
        self.name = name
        self.cast= cast

    def new_media_status(self, status):
        print('Something is playing')
        if not os.path.isfile(lockFile):
            print('Turn on!')
            #urllib.request.urlopen("http://192.168.0.20/recipes/exec/audio?state=on").read()
            #urllib.request.urlopen("http://192.168.0.20/recipes/exec/audio?state=on").read()
            #urllib.request.urlopen("http://192.168.0.20/recipes/exec/audio?state=on").read()
        else:
            print('But already turned on')

        print('[',time.ctime(),' - ', self.name,'] status media change:')
        print(status)

        #while True:
        #    print(cast.status.app_id) 

def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)
def unlink(fname):
    os.unlink(fname)

def listener():
    print('Search chromecast...')
    chromecasts = pychromecast.get_chromecasts()
    chromecast = next(cc for cc in chromecasts if cc.device.friendly_name == "Cuisine")
#print([cc.device.friendly_name for cc in chromecasts])
#        cast = next(cc for cc in chromecasts if cc.device.friendly_name == "Home cinema")
    print('Found chromecast home cinema')
    listenerCast = StatusListener(chromecast.name, chromecast)
    chromecast.register_status_listener(listenerCast)
    listenerMedia = StatusMediaListener(chromecast.name, chromecast)
    chromecast.media_controller.register_status_listener(listenerMedia)
    input('Listening for Chromecast events...\n\n')


while True:
    try:
        listener()
    except:
        time.sleep(5)
        pass

def oldlistener():
    while True:
        print('List chromecasts')
#        chromecasts = pychromecast.get_chromecasts()
        chromecasts = pychromecast.get_chromecasts()
        chromecast = next(cc for cc in chromecasts
                  if cc.device.friendly_name == "Home cinema")
#print([cc.device.friendly_name for cc in chromecasts])
#        cast = next(cc for cc in chromecasts if cc.device.friendly_name == "Home cinema")
        print('Found chromecast home cinema')
        listenerCast = StatusListener(chromecast.name, chromecast)
        chromecast.register_status_listener(listenerCast)
        listenerMedia = StatusMediaListener(chromecast.name, chromecast)
        chromecast.media_controller.register_status_listener(listenerMedia)

#cast = pychromecast.get_chromecast(friendly_name="Home cinema")
#cast = pychromecast.get_chromecast(friendly_name='Google home')
        input('Listening for Chromecast events...\n\n')
        time.sleep(1)
        continue
        print(cast.status)
        if not cast.status:
           print('No cast status')
           time.sleep(5)
           continue

        if cast.status and cast.status.app_id:
            print('Something is playing')
            if not os.path.isfile(lockFile):
                print('Turn on!')
                urllib.request.urlopen("http://192.168.0.20/recipes/exec/audio?state=on").read()
                urllib.request.urlopen("http://192.168.0.20/recipes/exec/audio?state=on").read()
                urllib.request.urlopen("http://192.168.0.20/recipes/exec/audio?state=on").read()
            else:
                print('But already turned on')
        else:
            print('Nothing to do')
            if os.path.isfile(lockFile):
                print('Turn off')
                urllib.request.urlopen("http://192.168.0.20/recipes/exec/audio?state=off").read()
                urllib.request.urlopen("http://192.168.0.20/recipes/exec/audio?state=off").read()

        time.sleep(2)

