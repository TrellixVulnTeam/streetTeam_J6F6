# %%
import json
import os
import datetime
from dateutil.relativedelta import relativedelta
from posixpath import commonpath, splitext
from bs4.element import NavigableString
from dateutil.parser import parse
from sys import excepthook
from bs4 import BeautifulSoup
import requests
import uuid
import re
from requests import exceptions

# %%
#From local file
#with open('GoTonight.html') as html_file:
#    soup = BeautifulSoup(html_file, 'lxml')

#From Website
source = requests.get('https://gotonight.com/venues/venue/?id=365').text
soup = BeautifulSoup(source, 'lxml')

# %%
#Removes italic text (usually text on top of show dates)
for i in soup('i'):
    i.decompose()
    
#Removes emphisised text (usually text on bottom of show dates)
for em in soup('em'):
    em.decompose()

# %%
#Data Model Properties
venue_name = "White Elephant Pub"
band_name = "**********"
date_string = ''
shows_array = []

# %%
#Grab a container or container type
table = soup.find('table', class_ = 'events-table')
tbody = table.find('tbody')

# %%
#Venue Name
for eventauto in tbody.find_all('tr', class_ = 'eventauto'):
    string_array = []
    a = eventauto

    temp_band = ''
    if not a.a:
        temp_band = a.b

    if not a.b:
        temp_band = a.a

    band_name = temp_band.text

#Show Time
    for b in eventauto.find_all('td')[1]:
        #Make every line of text a string
        text = str(b.string)

        #Remove white space from strings
        strip = text.strip()

        #Append each string into an array for easy access
        string_array.append(strip)

#Multiple remove loops because Python ends the loop once the condition is met... STUPID!!!
    for i in string_array:
        if i == '' or i == 'None':
            string_array.remove(i)
    
    for i in string_array:
        if i == '' or i == 'None':
            string_array.remove(i)

#Clean Up Date String
    raw_date = string_array[0] + ' ' + string_array[1]
    remove_from_date = '(pn|pm|am|"an"|p.m.|a.m.|mon, |tue, |wed, |thu, |fri, |sat, |sun, )'
    cleaned_date = re.sub(rf'{remove_from_date}', '', raw_date, flags=re.IGNORECASE) #the 'f' and {} were needed for string interpolation

    fixed_midnight = re.compile(re.escape('midnight'), re.IGNORECASE)
    fixed = fixed_midnight.sub('12am', cleaned_date)

    stupidity1 = fixed.replace('Pat Walsh / TrinityON80 ', '')
    split = stupidity1.split('-', 1)[0]
    stripped = split.strip()
    add_pm = ''

    if stripped == '':
        continue
    else:
        add_pm = stripped + 'pm'

#Parse Date
    try:
        #print(add_pm)
        show_time = parse(add_pm)

        if show_time < datetime.datetime.today():
            show_time = show_time + relativedelta(years=1)

        date_string = '{:%b %d, %Y %-I:%M%p}'.format(show_time)
    
    except:
        print(venue_name + ': GT PARSE TIME ERROR')
        continue

#Create Model and Add it to the Array
    try:
        showDict = {}
        showDict['venue'] = venue_name
        showDict['band'] = band_name
        showDict['dateString'] = date_string
        shows_array.append(showDict)

    except:
        print(venue_name + ': DATA MODEL ERROR')


# %%
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




