import spotifyhandler
import controller
import bluetoothhandler as bth
from config import default_track_uri
import time



class Lightify:
    def __init__(self,track_uri=None):
        self.spotify = spotifyhandler.spotify_auth()
        self.bt_device = bth.LEDController()
        self.track_uri = default_track_uri
        self.analysis = None
        self.duration = None
        if self.bt_device and self.spotify and self.track_uri:
            self.prep()
            if self.analysis:
                self.lightItUp()
        else:
            print(f'Error. lol how useless is this message!?')


    def set_track_uri(self, track_uri):
        self.track_uri = input('Please input the spotify track uri: ')

    def play(starting_sections_time):
        sp.start_playback('spotify:track:' + self.track_uri)
        time.sleep(starting_sections_time)

    def prep(self):
        self.analysis = spotifyhandler.get_track_analysis(self.spotify,self.track_uri)
        self.duration = spotifyhandler.get_track_duration(self.spotify,self.track_uri, self.analysis)

        # Adds remaining time to last segment for segmenent colorizing
        duration_diff = self.durations[0]/1000 - self.durations[1]
        if duration_diff > 1:
            self.analysis['segments'][-1]['duration'] += duration_diff

    def lightItUp(self,mode='segments'):

        if mode == 'segments':
            controller.segmentColorizer(self.bt_device,self.play, analysis[segments])

        else:
            print(f'[*] Mode: {mode} is not recognized...')
            print(f'[*] Exiting ...')
            self.bt_device.peripheral.disconnect()
            sys.exit(1)




a = Lightify()
