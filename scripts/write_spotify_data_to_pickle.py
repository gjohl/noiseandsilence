# -*- coding: utf-8 -*-
"""
Get spotify URI for each number 1 song and retrieve audio features.
Write the output to a dataframe and pickle it.
"""

import pandas as pd
from noiseandsilence.noiseandsilence.utils import add_audio_features_to_dataframe
from noiseandsilence.noiseandsilence.data.data_sources import (UK_CHART_DATA_PATH, 
                                                               RAW_SPOTIFY_DATA_PATH,
                                                               PARSED_SPOTIFY_DATA_PATH)
                                                            

# Read chart data
uk_data = pd.read_pickle(UK_CHART_DATA_PATH)


#Get features data and pickle
COMPRESSION = None
features = add_audio_features_to_dataframe(uk_data)
features.to_pickle(RAW_SPOTIFY_DATA_PATH, compression=COMPRESSION)


# Parse and clean data
AF_FIELDS = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']

# Drop empty data columns
parsed_features = features[features['af'].map(lambda d: len(d)!=0)]
dropped_features = features[features['af'].map(lambda d: len(d)==0)]

for fld in AF_FIELDS:
    parsed_features.loc[:,fld] = parsed_features['af'].map(lambda d: d[fld])
    
parsed_features = parsed_features.sort_values(by='date')
parsed_features.to_pickle(PARSED_SPOTIFY_DATA_PATH, compression=COMPRESSION)
