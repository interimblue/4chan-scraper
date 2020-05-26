
"""
Created on 26/05/2020
4chan-scraper v0.2
@author: Andrew Ellul
"""

import requests
import logging
import json
import os
import datetime as dt
import sys
import time

#===============================================================================
#                           Setup
#===============================================================================

board = 'pol'
url = "https://a.4cdn.org/" + board + "/catalog.json"
datetime = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
dateMonth = dt.datetime.now().strftime("%Y-%m")
path = '4chan-data/' + dateMonth
filename = path +'/' + datetime + '_' + board + '.json'

### Logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s  %(message)s',
    datefmt='%Y-%m-%d_T_%H:%M:%S',
    filename='4chan_catalog_scraper_custom.log',
    level=logging.DEBUG
    )

start = time.time()

### Thread attributes that we wish to preserve - image and file related attributes are excluded to save space
### For full list of attributes, see: 
### https://github.com/4chan/4chan-API/blob/master/pages/Catalog.md
### https://github.com/4chan/4chan-API/blob/master/pages/Threads.md
desiredAttributes = [
    'no',
    'resto',
    'sticky',
    'closed',
    'now',
    'time',
    'name',
    'trip',
    'id',
    'capcode',
    'country',
    'country_name',
    'sub',
    'com',
    'tim',
    'replies',
    'images',
    'last_modified',
    'tag',
    'semantic_url',
    'unique_ips',
    'archived',
    'archived_on',
    'last_replies'  
]

if os.path.exists(path):
    logging.info("Directory %s exists, using existing directory" % path)
else:
    try:  
        logging.info("Directory %s not found, attepting to create directory" % path)
        os.makedirs(path)
    except OSError:  
        logging.error("Failed to create directory: %s" % path)
    else:  
        logging.info("Successfully created the directory %s. Proceeding to scrape..." % path)

#===============================================================================
#                               Request
#===============================================================================

### Iterate through the catalog (list of page objects containing thread arrays) and
### rebuild the thread objects containing only the attributes we are interested in
def filterCatalog(boardCatalog):
    logging.info("Filtering 4chan response...")
    customThreadCatalog = []
    customPage = {}

    ### Loop through each page
    for page in boardCatalog:
        customThreads = []

        ### Loop through each thread in page and create a new thread object containing
        ### exclusively the attributes we wish to collect
        for thread in page['threads']:
            customThread = {}
            for attribute in desiredAttributes:
                if attribute in thread:
                    customThread[attribute] = thread[attribute]

            customThreads.append(customThread)
        
        ### Create a page with the new thread list 
        customPage = { 
            'page': page['page'],
            'threads': customThreads
        }

        ### Add the new page to our customized catalog 
        customThreadCatalog.append(customPage)

    return customThreadCatalog

### Get the 4chan board catalog
try:
    boardCatalog = requests.get(url).json()
except Exception as e:
    logging.error("Fatal error when attempting to fetch 4chan data")
    logging.error(e)

### The thread JSON object contains many attributes we do not require. Therefore we filter these out
try:
    customThreadCatalogJsonArray = filterCatalog(boardCatalog)
except Exception as e:
    logging.error("Fatal error when filtering JSON response from 4chan")


#===============================================================================
#                           Storage
#===============================================================================

### Append serialized submission object to the end of the JSON file
try:
    logging.info("Writing filtered 4chan response to file...")
    with open(filename, 'w') as f:
        json.dump(customThreadCatalogJsonArray, f)
except Exception as e:
    logging.error("Fatal error when attempting to write filtered JSON response from 4chan to file")
    logging.error(e)

### Logging: Timing consolidation
end = time.time()
timeElasped = end-start 
logging.info('=============== Time elasped: %s ==============='% timeElasped)