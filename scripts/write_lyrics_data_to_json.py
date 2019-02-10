# -*- coding: utf-8 -*-
"""
Scrape genius.com for lyrics of number 1 songs and write output to json

Use LyricsGenius library - https://github.com/johnwmillr/LyricsGenius
"""
import json
import logging
import pandas as pd
from noiseandsilence.noiseandsilence.utils import get_uk_chart_data, get_lyrics
from noiseandsilence.noiseandsilence.data.data_sources import UK_CHART_DATA_PATH, LYRICS_PATH, SEPARATOR


# Read chart data
uk_data = pd.read_pickle(UK_CHART_DATA_PATH)


# Get dict of lyrics for each song
song_artist_id = uk_data['title'] + SEPARATOR + uk_data['artist']

lyrics_dict = dict.fromkeys(song_artist_id.values)
total_iter = len(lyrics_dict)

for i, key in enumerate(lyrics_dict.keys()):
    split_key = key.split(SEPARATOR)
    title = split_key[0]
    artist = split_key[1]
    
    try: 
        lyrics = get_lyrics(title, artist)
        lyrics_dict[key] = lyrics
        logging.info('Success: Got lyrics for song {0} of {1} : {2}'.format(i, total_iter, key))
        
    except:
        lyrics_dict[key] = ''
        logging.warning('Failed to get lyrics for {0} of {1} : {2}'.format(i, total_iter, key))


# Write to json
jsonarray = json.dumps(lyrics_dict)  
with open(LYRICS_PATH, 'w') as outfile:
    json.dump(jsonarray, outfile)


