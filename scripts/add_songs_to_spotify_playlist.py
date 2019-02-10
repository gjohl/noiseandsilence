# -*- coding: utf-8 -*-
"""
Add parsed songs to my spotify playlist to verify they are correct
"""

import pandas as pd
from noiseandsilence.noiseandsilence.data.data_sources import PARSED_SPOTIFY_DATA_PATH
import spotipy
from spotipy.util import prompt_for_user_token

# Data we currently have from spotify
parsed_features = pd.read_pickle(PARSED_SPOTIFY_DATA_PATH, compression=None)

# My credentials for the playlist to add to
username = '1159158208'
track_ids = list(parsed_features['uri'].values)
playlist_id = '04s5Qdkd5yESXmgRJHF04r'

# Write to playlist
scope = 'playlist-modify-public'
token = prompt_for_user_token(username, scope, client_id='104147f1450c43bcaa81c4d5cbe9c4dc', client_secret='cffefd0e770348a9b3615babfad0a644', redirect_uri=r'https://example.com/callback')

sp = spotipy.Spotify(auth=token)
sp.trace = False

# Max 100 tracks per call so break it up
total_ids = len(track_ids)

for k, tid in enumerate(track_ids):
    print('Adding track {0} of {1}'.format(k, total_ids))
    results = sp.user_playlist_add_tracks(username, playlist_id, [tid])

