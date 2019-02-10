#!/usr/bin/env python
# coding: utf-8

'''
# # Disruption Research
# ## Author: Gurpreet Johl, 2019

# # Proposal
# "Music these days is all about X, Y, Z; in my day it was different". But was it?
# In this research piece, I aim to identify trends in the topics of popular music across time and place, and what this tells us more broadly about the society in which the music was created and consumed. Has there been a marked shift in the language and themes of popular music? If so, does this reflect the social and political atmosphere? Does it reflect changing demographics in listeners? Or the musicians themselves? By applying a rigorous approach to answering *whether* music has changed, we can then consider *how* and even *why* it has changed, and the wider implications.
# 
# I propose to take a quantitative approach to analysing the most popular songs in a time period utilising a field of machine learning called natural language processing (NLP). Using this, we can analyse the words used in songs to answer questions such as how wide is the vocabulary used in a song, [or of a particular artist](https://pudding.cool/2017/02/vocabulary/). We can go further and apply a technique called sentiment analysis to classify text in to subject matters. We can compare the frequency of subject matters over time to gain an insight into changes in the prevailing mood.
# 
# I will take lists of number one songs in a particular country (e.g. the US Hot 100 Billboard chart) as a measure of what was popular at a given point in time. I then take the lyrics of each song as the raw data for my analysis. Applying sentiment analysis to the text, we can classify the subject matter to pick out, say, the top 3 topics in that song. We can then map out how the frequency of these subjects evolves over time. We can also compare subjects cross-sectionally; at a given point in time, how does the frequency of topics compare between countries.
# 
# There are a number of additional avenues of research that could be interesting to explore using this data set and approach. For example, how *repetitive* is a song, are there notable difference between songs in different chart positions (i.e. the number 1 vs the number 100 song).
# 
# 

# ## Pipeline for quant analysis
# - Find lists of number one songs in various countries - start with US and UK
# - Scrape lyrics for each of those songs
# - Analyse data
#   - preprocess text
#   - analyse number of unique words
#   - apply sentiment analysis
# - Collate point-in-time data on frequency of topics
# - Plot charts (or Tableau visualisations?) of interesting results
# 

# ## About the author
# I currently work as a quantitative researcher for a large systematic hedge fund. In other words, I spend my days trawling through large amounts of data to find useful and interesting things which, in this case, we then use to trade financial markets. In even fewer words, I'm basically a nerd who chomps through numbers all day and does some maths with them. And I bloody love it.
# 
# I'm a self-taught guitarist and have been playing for well over 10 years, and been playing well for some of those years. I also dabble at piano and play in a band in London.
# 
# I graduated longer ago than my boyish looks would suggest with a Masters of Engineering from Oxford University.
# 

# # Web Scraping

# ## Chart info

# We will first focus on scraping data for two countries: US and UK. I'll attempt to keep the framework as generic as possible so that adding other countries in future does not add much extra effort.

# As an aside, an interesting [Washington Post article](https://www.washingtonpost.com/news/arts-and-entertainment/wp/2018/07/05/billboards-charts-used-to-be-our-barometer-for-music-success-are-they-meaningless-in-the-streaming-age/?noredirect=on&utm_term=.ef671ea4d164) on the relevance (or lack thereof) of charts on popularity.
# 

# Sources of info:
# - US (1940/1958-2019): https://en.wikipedia.org/wiki/List_of_Billboard_number-one_singles
# - UK (1952-2019): https://www.officialcharts.com/chart-news/all-the-number-1-singles__7931/

# Following https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe as an intro
'''
# In[1]:


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


from noiseandsilence.noiseandsilence.utils import try_else_value

##################
# Get Chart Data #
##################

# UK -------------------------------------------------------------------------------
uk_url = 'https://www.officialcharts.com/chart-news/all-the-number-1-singles__7931/'
uk_data = get_uk_chart_data(url=uk_url, skip_end=1)

# From here we could do some statistical analysis on the data.
# For example, who spent the most weeks at number one, how many number one songs each artist has had, how many total weeks have they spent at number one.
uk_data.sort_values(by='weeks', ascending=False)

# Get soup from UK URL
soup = get_soup_from_url(uk_url)
site_as_of_date = dparser.parse(soup.find_all('p')[0].text,fuzzy=True) # Date of site update


# US -------------------------------------------------------------------------------
# TODO
# Get all links

def get_us_chart_data(url):
    '''
    TODO
    '''
    pass
    us_data = None
    return us_data


for u in soup.find_all('a'):
    print(u.get('href'))



###################
# Get lyrics data #
###################


#################################
# Song metrics from spotify API #
#################################
# https://www.kaggle.com/aeryan/spotify-music-analysis/data
# https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/
# https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-analysis/

features = pd.read_pickle(pickle_path, compression=None)
parsed_features = pd.read_pickle(parsed_pickle_path, compression=None)


########################
# Explore Spotify data #
########################

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

        
