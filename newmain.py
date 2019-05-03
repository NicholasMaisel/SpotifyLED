import spotipy
import time
import sys
import spotipy.util
from config import *
import threading
import bluepy


perif = bluepy.btle.Peripheral('3c:a3:08:be:e1:ff')

chars = [x for x in perif.getDescriptors()]
color_chars = [chars[36],chars[39],chars[42]]

scope = 'playlist-modify-public,user-read-playback-state,streaming'
redirect_uri = 'http://localhost/'
track_uri_short = '4RdRa3qq0GBSKjomxrkh5K'
track_uri_long = 'spotify:track:'+ track_uri_short

a = spotipy.util.prompt_for_user_token(username,scope, client_id, client_secret, redirect_uri)
sp = spotipy.Spotify(a)
analysis = sp.audio_analysis(track_uri_short) # analysis for the song ride
beats = analysis['beats']
segments = analysis['segments']
sections = analysis['sections']
durations = [sp.audio_features(track_uri_short)[0]['duration_ms'], sum([x['duration'] for x in sections])]
print(analysis['segments'][9]['duration'])

isPlaying = False

colors = ['\033[41m','\033[42m','\033[43m','\033[44m',
            '\033[45m','\033[46m','\033[31m','\033[93m','\033[93m',
            '\033[91m','\033[95m','\033[34m']

led_colors = [['\x00','\xff','\x00'],['\x80','\x00','\x80'],['\xff','\x00','\x00'],['\xff','\x00','\xff'],['\x80','\x00','\x00'],['\xff','\xff','\x00'],['\x00','\x00','\xff'],['\xff','\xff','\xff'],['\xfa','\x80','\x72'],['\x00','\xff','\xff'],['\x9a','\xcd','\x32'],['\xff','\xda','\xb9']]
#### WHY IS sectionColorizer starting on the non first section????


def play(starting_sections_time):
    global sp
    global isPlaying
    sp.start_playback( uris = [track_uri_long])
    time.sleep(starting_sections_time)


def sectionColorizer(sections):
    for i in range(len(sections)):
        key, duration = sections[i]['key'], sections[i]['duration']
        print(sections[i]['start'])
        if i == 0:
            play(sections[i]['start'])
        if key <= len(colors):
            color_chars[0].write(led_colors[key][0])
            color_chars[1].write(led_colors[key][1])
            color_chars[2].write(led_colors[key][2])
            timerFunc(duration-0.01, beatKeeper)


def segmentColorizer(segments):
    global colors
    for i in range(len(segments)):
        pitch, duration = max(segments[i]['pitches']), segments[i]['duration']

        if i == 0:
            play(sections[i]['start'])

        if pitch < len(colors):
            print(colors[segments[i]['pitches'].index(pitch)] + 'PAT IS GAY', end = '')
            print(pitch)
            time.sleep(duration)


def sectionLEDColorizer(sections):
    for i in range(len(sections)):
        key, duration = sections[i]['key'], sections[i]['duration']
        print(sections[i]['start'])
        if i == 0:
            play(sections[i]['start'])
        if key <= len(colors):
            print(colors[key], end = '')
            timerFunc(duration-0.01, beatKeeper)


def beatKeeper(arg=None):
    global beats
    """
    Updates the global beats list that holds beats, outputs a beat.
    """
    beat = beats[0]
    print(beat['pitches'], len(beats))
    time.sleep(beat['duration'])
    beats.remove(beat)


def timerFunc(seconds,func,args=None):
    t_end = time.time() + seconds
    while time.time() < t_end:
        print(t_end-time.time())
        func.__call__(args)

def lightify():
    global durations
    global sections
    global sp
    global segments

    duration_diff = durations[0]/1000 - durations[1]

    if duration_diff > 1:
        sections[-1]['duration'] += duration_diff
    #sectionColorizer(sections)
    segmentColorizer(segments)

lightify()
