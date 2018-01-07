# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 19:46:20 2018

@author: edu
"""

import urllib.request
import urllib.parse


url_endpoint = "http://localhost:3001/?"
params = {'url': '', 'short-link': ''}
url = url_endpoint + urllib.parse.urlencode(params)

with urllib.request.urlopen(url) as f:
    print(f.read().decode('utf-8'))