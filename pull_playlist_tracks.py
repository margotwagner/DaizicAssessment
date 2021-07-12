#!/usr/bin/python

"""
Program that pulls the tracklist of a public Spotify API on a schedule (once a day) and stores the information as .json output.

Current functionality overwrites stored playlist tracks, so there is only one up-to-date .json tracklist per playlist

Currently the program continues and pulls the tracklist once a day until stopped by the user, but this could be updated
to stop after a certain number of days or on a certain date.

Code by Margot Wagner (last updated 06/12/21)
"""

import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import time

# Verify the correct number of command line inputs (does not currently check input validity)
if len(sys.argv) != 2:
    print('Usage: python pull_playllist_tracks.py playlist_id')
    exit()

cid = '5e14b21601344411b74f691d52e393a1'    # Client ID
secret = '5a9c00ad3dc94b9cbce775d72aeee699'

# Authorize spotipy access with Client ID
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def get_playlist_tracks(pl_id):
    """
    Extends spotipy playlist_tracks functionality to account for playlists with more than 100 songs
    :param pl_id (str) playlist id
    
    :return playlist tracks
    """
    results = sp.playlist_tracks(pl_id)
    pl_tracks = results['items']
    while results['next']:
        results = sp.next(results)
        pl_tracks.extend(results['items'])
    return pl_tracks

# Playlist id based on command line input
pl_id = 'spotify:playlist:' + sys.argv[1]

# Pull the tracklist once a day beginning immediately
while True:
    pl_tracks = get_playlist_tracks(pl_id)

    # Save tracklist as json output with playlist id name
    with open(str(sys.argv[1])+".json","w") as f:
        f.write(json.dumps(pl_tracks))

    print('Playlist', sys.argv[1], 'tracklist saved to json output for', time.ctime())
    
    time.sleep(24*60*60) # once a day
