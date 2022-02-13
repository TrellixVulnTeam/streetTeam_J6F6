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
url1 = 'https://www.marinajacks.com/events.html?start=0'
url2 = 'https://www.marinajacks.com/events.html?start=10'
url3 = 'https://www.marinajacks.com/events.html?start=20'
url4 = 'https://www.marinajacks.com/events.html?start=30'
url5 = 'https://www.marinajacks.com/events.html?start=40'
url_array = [url1, url2, url3, url4, url5]

# %% [markdown]
# Create a function that will iterate through the url_array and scrape webpage

# %%
#Properties
venue_name = 'Marina Jack'
band_name = ''
date_string = ''

# %%
def scape_urls(arr):
    for i in arr:
        response = requests.get(i).text
        soup = BeautifulSoup(response, 'lxml')

        events = soup.find('div', class_='eb-events-timeline' )
        
        for event in events.find_all('div', class_= re.compile('^eb-category-')):
            num_date = event.find('meta', itemprop = 'startDate')
            raw_date = str(num_date)
            meta_stripped = raw_date.replace('<meta content="', '')
            item_stripped = meta_stripped.replace('" itemprop="startDate"/>', '')
            remove_T = item_stripped.replace('T', ' ')
            
            try:
                #Date of show
                date = parse(remove_T)
                date_string = '{:%b %d, %Y %-I:%M%p}'.format(date)
            
            except:
                print(f'Date Error: {venue_name}')
                continue

            #Band Name
            raw_name = event.find_all('a')[0].text
            band_name = raw_name.replace('\u2019', "'")
            
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

