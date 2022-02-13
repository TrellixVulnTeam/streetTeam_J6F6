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
url1 = 'https://www.sandbartikigrille.com/events/'
url2 = ''
url3 = ''
url4 = ''
url5 = ''
url_array = [url1, url2, url3, url4, url5] 
show_array = []

# %% [markdown]
# Create a function that will iterate through the url_array and scrape webpage

# %%
#Properties
venue_name = 'SandBar Tiki & Grille'
band_name = ''
date_string = ''

# %%
def run():
    shows_array = []
    response = requests.get(url1).text
    soup = BeautifulSoup(response, 'lxml')
    month_year = soup.find(class_='col-auto col-m-auto month-title').text.split()
    days = soup.find_all('td', class_='eventful')

    for day in days:
        day_number = day.text.strip().split()[0]
        

        single_shows = day.find_all(class_='live-music')
        for show in single_shows:
            raw_time = show.text.split('-',1)[0]

            if 'p' in raw_time:
                start_time = raw_time + 'm'
            
            else:
                start_time = raw_time + 'pm'
            
            show_time = f'{month_year[0]} {day_number}, {month_year[1]} {start_time}'
            
            try:
                date = parse(show_time)
                date_string = '{:%b %d, %Y %-I:%M%p}'.format(date)
            
            except:
                print(f'Date Error: {venue_name}')
                continue
            
            band_name = show.text.split(' ', 1)[1]
            
            
            if '22 N' in band_name:
                band_name = '22N'

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


