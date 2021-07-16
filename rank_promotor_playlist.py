#!/usr/bin/python

"""
Program that ranks provided promoter playlists.

Current functionality ranks the promoter playlists using RapCaviar as the primary indicator of success and breaks ties
using the number of followers of the promoter playlists.

Usage: python rank_promotor_playlist.py "promoter_id_list" indicator_id

"promoter_id_list" is a comma-separated list of promoter ids

Code by Margot Wagner (last updated 06/12/21)
"""

import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import operator

if len(sys.argv) != 3:
    print('Usage: python rank_promotor_playlist.py "promotor_id_list" indicator_id')
    exit()

# IDs
promoter_id_list = sys.argv[1] # TODO: CHANGE FROM STRING TO LIST OF STRINGS
indicator_id = sys.argv[2]

# Convert to list
promoter_id_list = promoter_id_list.split(',')

# Create dict of tracks with addition time
def track_addtimes(pl_tracks):
    """
    Function that takes in all playlist track information and creates dicts of track_ids and addition time

    :pl_tracks list of playlist track information
    
    :return dict of addition times per track
    """
    tracks_addtimes = {}

    for i in range(len(pl_tracks)):
        if pl_tracks[i]['track'] is not None: # Error checking
            tracks_addtimes[pl_tracks[i]['track']['id']] = pl_tracks[i]['added_at']
        
    return tracks_addtimes

# Number of tracks that appear on promoter playlist before 
def n_promotion_hits(indicator_addtimes, promoter_addtimes):
    """
    Finds the number of tracks that appear on the promoter playlist before the indicator playlist

    :indicator_addtimes dict of track addtimes for the indicator playlist
    :promoter_addtimes dict of track addtimes for the promoter playlist
    
    :return number of tracks that are on the promoter playlist before indicator
    """
    hits = 0
    for k in indicator_addtimes.keys():
        if (k in promoter_addtimes.keys()) and (promoter_addtimes[k] <= indicator_addtimes[k]):
            hits += 1
    return hits


# Load indicator tracks and get addtimes
with open(indicator_id+".json",) as f:
    indicator_tracks = json.load(f)
indicator_addtimes = track_addtimes(indicator_tracks)

# Load promoter tracks and get addtimes
promoter_playlist_stats = {}
for p_id in promoter_id_list:
    # Load tracks
    with open(p_id+".json",) as f:
        p_tracks = json.load(f)
    p_addtimes = track_addtimes(p_tracks)

    # Save addtimes as tuple in dict of promoter ids
    #promoter_playlist_stats[p_id] = [p_addtimes]

    # Add the number of hits to the promoter stats dict
    promoter_playlist_stats[p_id] = [n_promotion_hits(indicator_addtimes, p_addtimes)]

    # Add the number of followers in the promoter playlist to stats dict
    cid = '***************************'    # Authorize spotipy access with Client ID
    secret = '***************************'
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    promoter_followers = sp.playlist(p_id, fields='followers')
    promoter_playlist_stats[p_id].append(promoter_followers['followers']['total'])


sorted_stats = sorted(promoter_playlist_stats.items(), key=lambda t: (t[1][0], t[1][1]), reverse=True)
print()
print('Promoter playlist sorted by efficacy')
print('(Promoter playlist ID,', '[Indicator hits,', 'Followers])')
print()
for pl in sorted_stats:
    print(pl)



#print(sorted(promoter_playlist_stats.items(), key=operator.itemgetter(1,2)))
