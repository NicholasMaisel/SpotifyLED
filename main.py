import spotipy
import time
import sys
import spotipy.util
from config import *
import threading
import bluepy






scope = 'playlist-modify-public,user-read-playback-state,streaming'
redirect_uri = 'http://localhost/'

track_uri_short = '6qgiSeYw2abTYHrk98mn5h' #shine mondo cozmo
#track_uri_short = '07CoHGbyzrIfkNBK1PtHUv' #trophies
#track_uri_short = '3BUWNzPWz2mDbptZmGEXpB' #let it all workout
#track_uri_short = '1CDVadnneswMxi6gBqJTtC' 
track_uri_long = 'spotify:track:'+ track_uri_short
perif = bluepy.btle.Peripheral('3c:a3:08:be:e1:ff')

chars = [x for x in perif.getDescriptors()]
color_chars = [chars[36],chars[39],chars[42]]

a = spotipy.util.prompt_for_user_token(username,scope, client_id, client_secret, redirect_uri)
sp = spotipy.Spotify(a)
analysis = sp.audio_analysis(track_uri_short) 
beats = analysis['beats']
segments = analysis['segments']
sections = analysis['sections']
tatums = analysis['tatums']
durations = [sp.audio_features(track_uri_short)[0]['duration_ms'], sum([x['duration'] for x in sections])]
print(analysis['segments'][9]['duration'])

isPlaying = False

colors = ['\033[41m','\033[42m','\033[43m','\033[44m',
            '\033[45m','\033[46m','\033[31m','\033[93m','\033[93m',
            '\033[91m','\033[95m','\033[34m']

'''led_colors = [[b'\x00',b'\xff',b'\x00'],[b'\x80',b'\x00',b'\x80'],[b'\xff',b'\x00',b'\x00'],[b'\xff',b'\x00',b'\xff'],[b'\x80',b'\x00',b'\x00'],[b'\xff',b'\xff',b'\x00'],[b'\x00',b'\x00',b'\xff'],[b'\xff',b'\xff',b'\xff'],[b'\xfa',b'\x80',b'\x72'],[b'\x00',b'\xff',b'\xff'],[b'\x9a',b'\xcd',b'\x32'],[b'\xff',b'\xda',b'\xb9']]'''

led_colors = [[b'\x45',b'\x62',b'\x45'],[b'\x55',b'\x45',b'\x55'],[b'\x62',b'\x45',b'\x45'],[b'\x62',b'\x45',b'\x62'],[b'\x55',b'\x45',b'\x45'],[b'\x62',b'\x62',b'\x45'],[b'\x45',b'\x45',b'\x62'],[b'\x50',b'\x60',b'\x70'],[b'\xfa',b'\x55',b'\x72'],[b'\x45',b'\x62',b'\x62'],[b'\x35',b'\x60',b'\x42'],[b'\x42',b'\x22',b'\x79']]

#### WHY IS sectionColorizer starting on the non first section????


def play(starting_sections_time):
    global sp
    global isPlaying
    sp.start_playback( uris = [track_uri_long])
    time.sleep(starting_sections_time)


def sectionLEDColorizer(sections):
    for i in range(len(sections)):
        key, duration = sections[i]['key'], sections[i]['duration']
        print(sections[i]['start'])
        if i == 0:
            play(sections[i]['start'])
        if key <= len(colors):
            color_chars[0].write(led_colors[key][0])
            color_chars[1].write(led_colors[key][1])
            color_chars[2].write(led_colors[key][2])
            time.sleep(duration)
            
def tatumLEDColorizer(tatums):
    global colors
    index = 0
    for i in range(len(tatums)):
        if i == 0:
            play(sections[i]['start'])
        duration = tatums[i]['duration']
        color_chars[0].write(led_colors[index % len(led_colors)][0])
        color_chars[1].write(led_colors[index % len(led_colors)][1])
        color_chars[2].write(led_colors[index % len(led_colors)][2])
        index += 1 
        time.sleep(duration)


		



def segmentLEDColorizer(segments):
    global colors
    for i in range(len(segments)):
        pitch, duration = max(segments[i]['pitches']), segments[i]['duration']

        if i == 0:
            play(sections[i]['start'])

        if pitch < len(led_colors):
            colorR=led_colors[segments[i]['pitches'].index(pitch)][0]
            colorG=led_colors[segments[i]['pitches'].index(pitch)][1]
            colorB=led_colors[segments[i]['pitches'].index(pitch)][2]
			
            color_chars[0].write(colorR)
            color_chars[1].write(colorG)
            color_chars[2].write(colorB)
            time.sleep(duration)
            #color_chars[0].write(b'\x00')
            #color_chars[1].write(b'\x00')
            #color_chars[2].write(b'\x00')
            #time.sleep(0.06)
            




def segmentColorizer(segments):
    global colors
    for i in range(len(segments)):
        pitch, duration = max(segments[i]['pitches']), segments[i]['duration']

        if i == 0:
            play(sections[i]['start'])

        if pitch < len(colors):
            print(colors[segments[i]['pitches'].index(pitch)] + '-------------', end = '')
            print(pitch)
            time.sleep(duration)


def sectionColorizer(sections):
    for i in range(len(sections)):
        key, duration = sections[i]['key'], sections[i]['duration']
        print(sections[i]['start'])
        if i == 0:
            play(sections[i]['start'])
        if key <= len(colors):
            print(colors[key], end = '')
            timerFunc(duration-0.01, beatKeeper)



print(beats)
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
    #sectionLEDColorizer(sections)
    #segmentColorizer(segments)
    segmentLEDColorizer(segments)
    #tatumLEDColorizer(tatums)
    perif.disconnect()

lightify()

