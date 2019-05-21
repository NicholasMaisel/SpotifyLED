import spotipy.util
from config import *



redirect_uri = 'http://localhost/'
track_uri_short = '6qgiSeYw2abTYHrk98mn5h' #shine mondo cozmo
#track_uri_short = '07CoHGbyzrIfkNBK1PtHUv' #trophies
#track_uri_short = '3BUWNzPWz2mDbptZmGEXpB' #let it all workout
#track_uri_short = '1CDVadnneswMxi6gBqJTtC'
track_uri_long = 'spotify:track:'+ track_uri_short

def spotify_auth():
    # Authenticate with spotify service
    token = spotipy.util.prompt_for_user_token(username,scope, client_id, client_secret, redirect_uri)
    sp = spotipy.Spotify(token)

    return(sp)

def get_track_analysis(sp,track_uri, analysis_part=None):
    ''' Returns an analysis list with analysis parts such as
        beats, segments, sections, etc...'''

    if analysis_part:
        analysis = sp.audio_analysis(track_uri)[analysis_part]
    else:
        analysis = sp.audio_analysis(track_uri)

    return(analysis)

def get_track_duration(sp,track_uri,analysis):
    ''' Returns 'durations' that is used for various timing error that
        occur throughout lightify'''

    durations = [sp.audio_features(track_uri_short)[0]['duration_ms'],
                                sum([x['duration'] for x in analysis['sections']])]

    return(durations)
