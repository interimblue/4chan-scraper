# 4chan Scraper

This is a simple 4chan scraper that utilises the 4chan API and outputs a json file with the filtered response.

Documentation for the API and its usage can be found here: https://github.com/4chan/4chan-API/

## TODO

1. Multiple board support
2. Option to store responses in 1 large file 

## Usage 

The repository contains two files
* `4chan_catalogue_scraper_simple.py`
* `4chan_catalogue_scraper_custom.py`

### Simple

The simple file is the most basic implementation needed to generate a response from the 4chan API. Run this script from the command-line to generate a JSON file containing the unfiltered response output. 

### Custom

The custom file is intended to filter out unnecessary clutter from the response (e.g. image dimensions) and to for use by a scheduler (e.g. a cron job). 

This script will generate a new file each time is run, batching the files into a separate folder per day. The result will be a file under `4chan-data/YYYY-MM/YYYY-MM-DD_HH-MM-SS_board.json`

## Scheduling and Logging 

Logging is logged to `4chan_catalogue_scraper_custom.log` 

To aid scheduling, the script will store each scrape `.json` file with a timestamp under a folder named with the year and month.
