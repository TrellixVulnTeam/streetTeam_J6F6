# %%
import json
import os
import datetime
from dateutil.relativedelta import relativedelta
import time as Time
from posixpath import commonpath, splitext
from bs4.element import NavigableString
from dateutil.parser import parse
from sys import excepthook
from bs4 import BeautifulSoup
import requests
import uuid
import re
from requests import exceptions 

# %% [markdown]
# Next decide which urls to scarpe and put them into an array so you can iterate through them

# %%

#URL's to be scrapped
url1 = 'https://www.skob.com/live-music/band-calendar'
url2 = ''
url3 = ''
url4 = ''
url5 = ''
url_array = [url1, url2, url3, url4, url5] 

# %% [markdown]
# Create a function that will iterate through the url_array and scrape webpage

# %%
#Properties
venue_name = 'Siesta Key Oyster Bar'
band_name = ''
date_string = ''

ex_array = [
    'GAME'
]

# %%
response = requests.get(url1).text
soup = BeautifulSoup(response, 'lxml')

# %%
events = soup.find_all(class_ = 'djev_item_content')

# %%
def scape_urls(arr):
    for i in arr:
        if i == '':
            continue
        
        response = requests.get(i).text
        soup = BeautifulSoup(response, 'lxml')

        for event in events:
            raw_band_name = event.find('h4').text.strip()

            '''!!! FILTER!!! '''
            if any([x in raw_band_name for x in ex_array]): 
                continue

            '''!!! Finds the first number in the string'''
            pattern = '\d+'
            numbers = re.findall(pattern, raw_band_name)

            try:
                band_name = raw_band_name.split(f' {numbers[0]}')[0]
            except:
                continue

            raw_date = event.find(class_="djev_time_from").text.strip() + f' {numbers[0]}pm'

            date = parse(raw_date)
            date_string = '{:%b %d, %Y %-I:%M%p}'.format(date)

            #Create model and add to array
            showDict = {}
            showDict['venue'] = venue_name
            showDict['band'] = band_name
            showDict['dateString'] = date_string
            shows_array.append(showDict)

# %%
shows_array = []
scape_urls(url_array)

# %%
#Export as JSON
shows = {}
shows['shows'] = shows_array

#Save To json file
save_path = '/Volumes/Work/Face2Face/Xity/Scrappers/Show Data/Venue Data'
file_name = venue_name + ' Website' + '.json'
complete_name = os.path.join(save_path, file_name)

file = open(complete_name, 'w')
file.write(json.dumps(shows, indent = 2))
file.close()
print(f"{venue_name} Complete!")



