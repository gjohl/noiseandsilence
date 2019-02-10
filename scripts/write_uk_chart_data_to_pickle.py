#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 20:25:53 2019

@author: gurpr
"""

from noiseandsilence.noiseandsilence.utils import get_uk_chart_data
from noiseandsilence.noiseandsilence.data.data_sources import UK_URL, UK_CHART_DATA_PATH


# Get chart data
uk_data = get_uk_chart_data(url=UK_URL, skip_end=1)
uk_data.to_pickle(UK_CHART_DATA_PATH)
