# %%
import json
import os
import datetime
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
url1 = 'https://www.packinghousecafe.com/events'
url2 = ''
url3 = ''
url4 = ''
url5 = ''
url_array = [url1, url2, url3, url4, url5] 

# %% [markdown]
# Create a function that will iterate through the url_array and scrape webpage

# %%
#Properties
venue_name = "Jr's Old Packinghouse"
band_name = ''
date_string = ''


'''The website does have show times, this array holds the days for 6 oclock show time'''
six_time = [
    "Tuesday", "Wednesday", "Thursday"
]

ex_array = [
    'New Year',
]

# %%
response = requests.get(url1).text
soup = BeautifulSoup(response, 'lxml')

events = soup.find(id = "events")
shows = events.find_all('li')

for show in shows:
    raw_date = show.find('p').text.strip()

    if any([x in raw_date for x in six_time]): 
        raw_time = '6:00PM'
    else:
        raw_time = '7:00PM'

    raw_date = raw_date + f' {raw_time}'

    date = parse(raw_date)
    date_string = '{:%b %d, %Y %-I:%M%p}'.format(date)


    band_name = show.find('h3').text.strip()

# %%
def scape_urls(arr):
    for i in arr:
        if i == '':
            continue
        
        response = requests.get(i).text
        soup = BeautifulSoup(response, 'lxml')

        events = soup.find(id = "events")
        shows = events.find_all('li')

        for show in shows:
            raw_date = show.find('p').text.strip()

            if any([x in raw_date for x in six_time]): 
                raw_time = '6:00PM'
            else:
                raw_time = '7:00PM'

            raw_date = raw_date + f' {raw_time}'

            date = parse(raw_date)
            date_string = '{:%b %d, %Y %-I:%M%p}'.format(date)

            band_name = show.find('h3').text.strip()

            '''!!!FILTER!!!'''
            if any([x in band_name for x in ex_array]): 
                continue


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
import OhmicityShared
save_path = OhmicityShared.ohmicity_shared.venue_data_path

file_name = venue_name + '.json'
complete_name = os.path.join(save_path, file_name)

file = open(complete_name, 'w')
file.write(json.dumps(shows, indent = 2))
file.close()
print(f"{venue_name} Complete!")


