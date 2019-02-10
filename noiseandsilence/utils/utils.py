# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 16:41:03 2019

@author: gurpr
"""

from bs4 import BeautifulSoup
import urllib3
import os
import json
import requests
import dateutil.parser as dparser
import pandas as pd
import logging
import lyricsgenius
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from matplotlib import pyplot as plt
from datetime import datetime as dt



#########
# Utils #
#########

def try_else_value(fn, value=''):
    '''
    Wrapper for functions to return empty string if there is a failure
    '''
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except:
            return value
    return wrapper


# Web Scraping-------------------------------------------------
def get_soup_from_url(url, parser="html.parser"):
    '''
    Get soup from source URL
    :url: [string] source URL
    :parser: [string] optional parser argument for BeautifulSoup
    '''
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup
    

# UK data
def get_uk_chart_data(url, skip_end=None):
    '''
    Scrape all tables from the UK chart website,
    keep those which have the chart data.
    
    Inputs:
    -------
    :url: [string] URL of UK chart data source
    :skip_end: [int] number of rows to drop at the end (recent data is sometimes bad)
    
    Returns:
    --------
    :uk_data: [DataFrame] chart data of the form below
    
    index | date | title | artist | weeks
    '''
    # Tables we are interested in should have "artist" as a column
    dfs = pd.read_html(url, header=0)
    dfs = [df for df in dfs if 'artist' in df.columns.map(lambda s: s.lower())]
    df_cols = ['date', 'title', 'artist', 'weeks']
    
    for df in dfs:
        df.columns = df_cols
    
    uk_data = pd.concat(dfs, axis=0) # Merge into a single data set
    
    if skip_end:
        uk_data = uk_data.iloc[:-skip_end,:] # Temp errors in recent values
        
    uk_data['date'] = uk_data['date'].map(lambda d: dparser.parse(d)) # Clean dates
    return uk_data



# Genius API---------------------------------------------
genius = lyricsgenius.Genius("Pl-4LRcmLL5CYzDpJigA8ajNt_fPIoD_C4CaEkPjiJZaf2Hl2Fel7TmeRrLsaB8Y") # Client ID key authentication

def get_lyrics(title, artist):
    '''
    Given a song title and artist, return a string of the song lyrics
    Retrieves lyrics from genius.com using the genius API
    :title: [string]
    :artist: [string]
    '''
    song_object = genius.search_song(title, artist)
    lyrics = song_object.lyrics
    return lyrics


def add_lyrics_to_dataframe(df):
    '''
    Given a DataFrame containing title and artist, append column for lyrics as a string
    :df:
    '''
    lyrics = df.copy()
    lyrics['lyrics'] = list(map(try_else_value(get_lyrics,''), lyrics['title'], lyrics['artist']))
    return lyrics



# Spotify API----------------------------------------------
client_credentials_manager = SpotifyClientCredentials(client_id='104147f1450c43bcaa81c4d5cbe9c4dc', client_secret='cffefd0e770348a9b3615babfad0a644')
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_spotify_uri_from_title_and_artist(title, artist):
    '''
    Given a song title and artist, return a string of the spotify URI
    :title: [string]
    :artist: [string]
    '''
    query = title + ' ' + artist
    result = spotify.search(q=query, type='track')
    
    #TODO - check name is similar to input artist
    # result_artist = result['tracks']['items'][0]['artists'][0]['name']
    # compare artist with result_artist
    
    uri = result['tracks']['items'][0]['uri']
    return uri
    

def get_audio_features_from_uri(uri):
    '''
    Given a spotify uri, return a dict of audio features for the song
    :uri: [string]
    '''
    audio_features = spotify.audio_features([uri])[0]
    if audio_features is None:
        audio_features = {}
    return audio_features


def add_audio_features_to_dataframe(df):
    '''
    Given a DataFrame containing title and artist, append columns for uri and audio_features (af)
    :df:
    '''
    features = df.copy()
    features['uri'] = list(map(try_else_value(get_spotify_uri_from_title_and_artist,''), features['title'], features['artist']))
    features['af'] = features['uri'].map(try_else_value(get_audio_features_from_uri,{}))
    return features
