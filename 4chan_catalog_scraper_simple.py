"""
Created on 26/05/2020
4chan-scraper v0.2
@author: Andrew Ellul
"""

import requests, json, os, datetime

### File save settings
board = 'pol'
filename = board + '.json'

### Get the 4chan board catalog JSON file and open it
url = "https://a.4cdn.org/" + board + "/catalog.json"
threadCatalog = requests.get(url).json()

### Append serialized submission object to the end of the JSON file
with open(filename, 'a+') as f:
    json.dump(threadCatalog, f)
