import spotipy
import time
import sys
import spotipy.util
from config import *

scope = 'playlist-modify-public,user-read-playback-state,streaming'
redirect_uri = 'http://localhost/'
a = spotipy.util.prompt_for_user_token(username,scope, client_id, client_secret, redirect_uri)
#4gQBDT9n_WStK-lixihLunUhvQm0TLaIlB5JbSyjPAyCQCfY5ZOxAnFZqiLLYfeJPp5Al1YA7SZhUArl3pLREiACSRHw8WgK2-V9DEgw_sQZ6lpPK
sp = spotipy.Spotify(a)
analysis = sp.audio_analysis('2Z8WuEywRWYTKe1NybPQEW') # analysis for the song ride
#sp.start_playback(uris=['spotify:track:2Z8WuEywRWYTKe1NybPQEW'])
beats = analysis['beats']
sections = analysis['sections']
print([x['key'] for x in analysis['sections']])
sp.start_playback('7993c4c7caa8989983a7f6f519826aeb0c1eb3e9', uris = ["spotify:track:2Z8WuEywRWYTKe1NybPQEW"])


def sectionColorizer(key,duration):
    global beats
    if key == 10:
        print('\033[31m', end = '')
        timerFunc(duration, beatKeeper)
    elif key == 4:
        print('\033[32m', end = '')
        timerFunc(duration, beatKeeper)
    elif key == 3:
        print('\033[33m', end = '')
        timerFunc(duration, beatKeeper)
    elif key == 1:
        print('\033[34m', end = '')
        timerFunc(duration, beatKeeper)


def beatKeeper(arg=None):
    global beats
    """
    Updates the global beats list that holds beats, outputs a beat.
    """
    beat = beats[0]
    print(beat, len(beats))
    time.sleep(beat['duration'])
    beats.remove(beat)


def timerFunc(seconds,func,args=None):
    t_end = time.time() + seconds
    while time.time() < t_end:
        print(time.time()-t_end)
        func.__call__(args)

for section in sections:
    sectionColorizer(section['key'], section['duration'])
