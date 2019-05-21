import spotifyhandler
import controller
import bluetoothhandler as bth
from config import default_track_uri



class Lightify:
    def __init__(self,track_uri=None):
        spotify = spotifyhandler.spotify_auth()
        bt_device = bth.LEDController()
        track_uri = default_track_uri
        print(self.track_uri)
        analysis = None
        duration = None
        if bt_device and spotify and track_uri:
            self.prep()
            if analysis:
                self.lightItUp()
        else:
            print(f'Error. lol how useless is this message!?')


    def set_track_uri(self, track_uri):
        self.track_uri = input('Please input the spotify track uri: ')

    def prep(self):
        self.analysis = spotifyhandler.get_track_analysis(self.track_uri)
        self.duration = spotifyhandler.get_track_duration(self.track_uri)

        # Adds remaining time to last segment for segmenent colorizing
        duration_diff = self.durations[0]/1000 - self.durations[1]
        if duration_diff > 1:
            self.analysis['segments'][-1]['duration'] += duration_diff

    def lightItUp(self,mode='segments'):

        if mode == 'segments':
            controller.segmentColorizer(self.bt_device, analysis[segments])

        else:
            print(f'[*] Mode: {mode} is not recognized...')
            print(f'[*] Exiting ...')
            self.bt_device.peripheral.disconnect()
            sys.exit(1)




a = Lightify()
