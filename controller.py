import time
from config import led_colors

def segmentColorizer(bt_device, segments):
    ''' Used to control the LED lights based on spotify's segment objects
        provided by the spotify API'''

    for i in range(len(segments)):
        pitch, duration = max(segments[i]['pitches']), segments[i]['duration']

        if i == 0:
            play(sections[i]['start'])

        if pitch < len(led_colors):
            R=led_colors[segments[i]['pitches'].index(pitch)][0]
            G=led_colors[segments[i]['pitches'].index(pitch)][1]
            B=led_colors[segments[i]['pitches'].index(pitch)][2]

            bt_device.red.write(R)
            bt_device.green.write(G)
            bt_device.blue.write(G)
            time.sleep(duration)
