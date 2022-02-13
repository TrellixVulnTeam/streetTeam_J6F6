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
url1 = 'https://www.sharkysonthepier.com/live-music'
url2 = ''
url3 = ''
url4 = ''
url5 = ''
url_array = [url1]

# %% [markdown]
# Create a function that will iterate through the url_array and scrape webpage

# %%
#Properties
venue_name = "Sharky's On the Pier"
band_name = ''
date_string = ''

# %%
response = requests.get(url1).text
soup = BeautifulSoup(response, 'lxml')
events = soup.find_all(class_='rs_event_detail')

for event in events:
    band_name = event.find(itemprop='name').text.strip()
    raw_date = event.find(class_='rsepro-event-from-block').b.text.split(' pm')[0] + 'pm'
    
    this_time = parse(raw_date)
    date_string = '{:%b %d, %Y %-I:%M%p}'.format(this_time)

# %%
def run():
    shows_array = []
    
    response = requests.get(url1).text
    soup = BeautifulSoup(response, 'lxml')
    events = soup.find_all(class_='rs_event_detail')

    for event in events:
        band_name = event.find(itemprop='name').text.strip()
        raw_date = event.find(class_='rsepro-event-from-block').b.text.split(' pm')[0] + 'pm'
        
        try:
            this_time = parse(raw_date)
            date_string = '{:%b %d, %Y %-I:%M%p}'.format(this_time)
        
        except:
            print(f'Date Error: {venue_name}')
            continue

        #Create model and add to array
        showDict = {}
        showDict['venue'] = venue_name
        showDict['band'] = band_name
        showDict['dateString'] = date_string
        shows_array.append(showDict)

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


# %%
run()

# %%



