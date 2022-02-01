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
url1 = 'https://3dbrewing.com/events/'
url2 = ''
url3 = ''
url4 = ''
url5 = ''
url_array = [url1] 

# %% [markdown]
# Create a function that will iterate through the url_array and scrape webpage

# %%
#Properties
venue_name = '3 Daughters Brewing'
band_name = ''
date_string = ''
shows_array = []
venue_array = []

# %%
def scape_urls(arr):
    for i in arr:
        response = requests.get(i).text
        soup = BeautifulSoup(response, 'lxml')
        
        for single_Show in soup.find_all('div', class_='col event-post-container'):

        #Grab its information and organize it
            try:
                
                #Date
                date_Div = single_Show.find('h3', class_ = 'second-headline').text
                remove_EndTime = date_Div.split('-', 2)
                cleaned = remove_EndTime[0] + ' ' + remove_EndTime[1]

                try:
                    show_time = parse(cleaned)

                    if show_time < datetime.datetime.today():
                        show_time = show_time + relativedelta(years=1)

                    date_string = '{:%b %d, %Y %-I:%M%p}'.format(show_time)

                except:
                    print("Error parsing date")
                    continue


                #Band
                clean_Name = single_Show.find('h3', class_ = 'headline').text
                band_name = " ".join(clean_Name.split())

                try:
                    showDict = {}
                    showDict['venue'] = venue_name
                    showDict['band'] = band_name
                    showDict['dateString'] = date_string

                except:
                    print(venue_name + ': DATA MODEL ERROR')
                
                
                #Filter Data
                filter_array = [
                    'TRIVIA', 'Trivia', 'Food', 'Blood Drive', 'Total Wine', 'Beer', 'ABC', 'Bingo', 'Flower',
                    'DIY', 'National' 
                ]

                if any([x in band_name for x in filter_array]):
                    continue
                
                shows_array.append(showDict)
                

            except:
                print(f'Date Error: {venue_name}')
                continue

    
    #Export as JSON
    shows = {}
    shows['shows'] = shows_array

    #Save To json file
    save_path = '/Volumes/Work/Face2Face/Xity/Scrappers/Show Data/Venue Data'
    file_name = venue_name + '.json'
    complete_name = os.path.join(save_path, file_name)

    file = open(complete_name, 'w')
    file.write(json.dumps(shows, indent = 2))
    file.close()
    print(f"{venue_name} Complete!")

# %%
scape_urls(url_array)


