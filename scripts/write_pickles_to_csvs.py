# -*- coding: utf-8 -*-
"""
Write pickles as csvs for easier viewing and editing for manual error checking
"""

import  pandas as pd
from noiseandsilence.noiseandsilence.data.data_sources import RAW_SPOTIFY_DATA_PATH, LYRICS_PATH

# Read pickles
lyrics_df = pd.read_pickle(LYRICS_PATH)
raw_spotify_df = pd.read_pickle(RAW_SPOTIFY_DATA_PATH)

# Write csvs
lyrics_df.to_csv(LYRICS_PATH+'.csv')
raw_spotify_df.to_csv(RAW_SPOTIFY_DATA_PATH+'.csv')
