#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime as dt

from noiseandsilence.noiseandsilence.data.data_sources import (UK_CHART_DATA_PATH, 
                                                               LYRICS_PATH,
                                                               RAW_SPOTIFY_DATA_PATH,
                                                               PARSED_SPOTIFY_DATA_PATH)
from noiseandsilence.noiseandsilence.utils import try_else_value

#############
# Get  Data #
#############

# UK Chart Data
uk_data = pd.read_pickle(UK_CHART_DATA_PATH)

# US Chart Data
# TODO

# Lyrics data
lyrics = pd.read_pickle(LYRICS_PATH, compression=None)

# Spotify data
raw_features = pd.read_pickle(RAW_SPOTIFY_DATA_PATH, compression=None)
parsed_features = pd.read_pickle(PARSED_SPOTIFY_DATA_PATH, compression=None)



######################
# Explore chart data #
######################
# From here we could do some statistical analysis on the data.
# For example, who spent the most weeks at number one, how many number one songs each artist has had, how many total weeks have they spent at number one.
uk_data.sort_values(by='weeks', ascending=False)






#######################
# Explore lyrics data #
#######################
dropped_lyrics = lyrics[lyrics['lyrics'].map(lambda s: len(s))==0]
print(dropped_lyrics[['title','artist']])




########################
# Explore Spotify data #
########################
# https://www.kaggle.com/aeryan/spotify-music-analysis/data
# https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/
# https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-analysis/


af_fields = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']

# Plots all metrics
plot_rows = (len(af_fields)+1)//2
fig, axes = plt.subplots(plot_rows,2)

rolling_lookback = 20

if len(af_fields) % 2 == 1:
    parsed_features['dummy'] = 0
    plot_fields = af_fields + ['dummy']
else:
    plot_fields = af_fields.copy()
    
col_1_fields = plot_fields[:plot_rows]
col_2_fields = plot_fields[plot_rows:]

for row,fld in enumerate(col_1_fields):
    df = parsed_features[['date',fld]].set_index('date')
    df['rolling_average'] = df.rolling(rolling_lookback).median()
    
    axes[row][0].step(df.index, df[fld].values)
    axes[row][0].step(df.index, df['rolling_average'].values)    
    axes[row][0].set_title(fld.replace('_', ' '))

for row,fld in enumerate(col_2_fields):
    df = parsed_features[['date',fld]].set_index('date')
    df['rolling_average'] = df.rolling(rolling_lookback).median()
    
    axes[row][1].step(df.index, df[fld].values)
    axes[row][1].step(df.index, df['rolling_average'].values)    
    axes[row][1].set_title(fld.replace('_', ' '))
    
plt.tight_layout()


# Interesting plots
    # Timeseries of values (smoothed?) comparing US vs UK
    # Distributions of metrics per decade
    # Dig into "outliers" - time signature and temp look interesting
    
    # Weeks at number one vs certain qualities of the music - are the outliers spending more or less time at numer 1?
    # Qualities of songs that reenter number 1
    
    # Number of words per second of song

        
