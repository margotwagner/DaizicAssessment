# SpotifyPromotions

SpotifyPromotions is a data science project looking to understand 3rd party Spotify playlist promotion.

## Usage

pull_playlist_tracks.py     Python program to pull the tracklist of a public Spotify API once a day and stores the information in a json format.
Usage: 'Usage: python pull_playllist_tracks.py playlist_id'

rank_promotor_playlist.py   Python program that uses the tracklists of an indicator playlist (ie RapCaviar) to rank the provided list of promoter playlists. It prints out the ranking to standard output. Current functionality ranks the promoter playlists using RapCaviar as the primary indicator of success and breaks ties using the number of followers of the promoter playlists.
Usage: python rank_promotor_playlist.py "promoter_id_list" indicator_id
"promoter_id_list" is a comma-separated list of promoter ids

Tracklists are currently already uploaded for the RapCaviar and the provided promoter playlist but can be remade using the pull_playlist_tracks.py program. 
