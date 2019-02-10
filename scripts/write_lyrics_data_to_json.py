# -*- coding: utf-8 -*-
"""
Scrape genius.com for lyrics of number 1 songs and pickle output

Use LyricsGenius library - https://github.com/johnwmillr/LyricsGenius
"""

import pandas as pd
from noiseandsilence.noiseandsilence.utils import add_lyrics_to_dataframe
from noiseandsilence.noiseandsilence.data.data_sources import UK_CHART_DATA_PATH, LYRICS_PATH


# Read chart data
uk_data = pd.read_pickle(UK_CHART_DATA_PATH)

# Get lyrics
lyrics_df = add_lyrics_to_dataframe(uk_data)

# Pickle
COMPRESSION=None
lyrics_df.to_pickle(LYRICS_PATH, compression=COMPRESSION)
