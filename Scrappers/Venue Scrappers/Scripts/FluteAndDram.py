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
# Next decide which urls to scrape and put them into an array so you can iterate through them

# %%

#URL's to be scrapped
url1 = 'https://flutendram.com/events/'
url2 = ''
url3 = ''
url4 = ''
url5 = ''
url_array = [url1] 

# %% [markdown]
# Create a function that will iterate through the url_array and scrape webpage

# %%
#Properties
venue_name = "Flute & Dram"
band_name = ''
date_string = ''

ex_array = [
    'Party', 'Fundraiser', 'Holiday', 'Christmas', 'New Years'
]

# %%
def scape_urls(arr):
    for i in arr:
        response = requests.get(i).text
        soup = BeautifulSoup(response, 'lxml')

        for single_Show in soup.find_all('div', class_='stevent-wrap'):

            try:
                #Grab its information and organize it
                #Date
                date_Div = single_Show.find('div', class_ = 'stevent-date')
                month = date_Div.find('div', class_ = 'date-top')
                day = date_Div.find('div', class_ = 'date-middle')
                year = datetime.date.year
                month_And_Day_And_Year = month.text + " " + day.text + "," + " " + datetime.datetime.now().strftime("%Y")

                #Band
                band_name = single_Show.find('div', class_ = 'stevent-title').h3.text

                if any([x in band_name for x in ex_array]): 
                    continue

                #Start Time
                start_Time = single_Show.find('div', class_ = 'stevent-starttime').text
                remove_Words_Time = start_Time.replace('Starts at ', '')
                remove_Space_Time = remove_Words_Time.replace(' ', '')

                whole_Date = month_And_Day_And_Year + " " + remove_Space_Time
                
                try:
                    show_time = parse(whole_Date)

                    if show_time < datetime.datetime.today():
                        show_time = show_time + relativedelta(years=1)

                    date_string = '{:%b %d, %Y %-I:%M%p}'.format(show_time)

                except:
                    print("Error parsing date")
                    continue


                try:
                    showDict = {}
                    showDict['venue'] = venue_name
                    showDict['band'] = band_name
                    showDict['dateString'] = date_string
                    shows_array.append(showDict)

                except:
                    print(venue_name + ': DATA MODEL ERROR')


            except:
                print(f'Date Error: {venue_name}')
                continue


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



