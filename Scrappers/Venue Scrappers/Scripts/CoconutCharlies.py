# %%
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as BS

import time as Time
import re
from dateutil.parser import parse
import datetime
import os
import json
import OhmicityShared

#For keyboard key programmatic control
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# %%
#Properties
url = "https://plugin.eventscalendar.co/widget.html?pageId=eog1c&compId=comp-kiumcfk0&viewerCompId=comp-kiumcfk0&siteRevision=230&viewMode=site&deviceType=desktop&locale=en&tz=America%2FNew_York&regionalLanguage=en&width=980&height=598&instance=RFhWqjMr3NMY4DCZtqXhI4QOJ-Z3kSXQmJvXwivrsgw.eyJpbnN0YW5jZUlkIjoiYWY1MTI0ZTgtMWQ3YS00YmVjLWExNmMtMzQ5YzI3ZDUzNGRlIiwiYXBwRGVmSWQiOiIxMzNiYjExZS1iM2RiLTdlM2ItNDliYy04YWExNmFmNzJjYWMiLCJzaWduRGF0ZSI6IjIwMjEtMTAtMzFUMDE6MDE6MDEuMTgyWiIsInZlbmRvclByb2R1Y3RJZCI6InByZW1pdW0iLCJkZW1vTW9kZSI6ZmFsc2UsImFpZCI6Ijk0MmVlMjA2LWI1OTctNDU2Ni1hMzE1LTI3YmJhMjZjZDY4MSIsInNpdGVPd25lcklkIjoiMTA0OWY1MjEtZGM2MS00ODdkLTgzNmQtMmM5N2UwMTljODdmIn0&currency=USD&currentCurrency=USD&commonConfig=%7B%22brand%22:%22wix%22,%22bsi%22:%2273584552-62d1-4a21-995a-a6d4f631f332%7C1%22,%22BSI%22:%2273584552-62d1-4a21-995a-a6d4f631f332%7C1%22%7D&vsi=8fcac177-1c1a-411b-ac18-9e14336e8e3a"
time = Time
shows_array = []
venue_array = []

# %%
def run():
    #Navigate Site with Selenium
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    Time.sleep(1)

    #Get Data with BeautifulSoup
    venue_name = "Coconut Charlie's Beach Bar & Grill"
    band_name = ''
    date_string = ''


    html = driver.page_source
    soup = BS(html)

    month = soup.find_all('div', class_='day ng-scope')

    for day in month:
        
        test_date = day.find('div', class_='aria-only ng-binding ng-scope')
        if not test_date:
            continue
        
        raw_date = test_date.text
        clean1 = raw_date.split(',')
        general_date = clean1[1] + ',' + clean1[2]
        
        for event in day.find_all('div', class_="ng-scope"):
            
            #Show Time
            test_time = event.find('span', class_='event-time ng-binding ng-scope')
            if not test_time:
                continue

            time = test_time.text
            full_date = general_date + ' ' + time

            date = parse(full_date)
            date_string = '{:%b %d, %Y %-I:%M%p}'.format(date)
            
            #Band
            test_band = event.find('span', class_='event-title-text ng-binding')
            if not test_band:
                continue
            band_name = test_band.text

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
    save_path = OhmicityShared.ohmicity_shared.venue_data_path
    file_name = venue_name + '.json'
    complete_name = os.path.join(save_path, file_name)

    file = open(complete_name, 'w')
    file.write(json.dumps(shows, indent = 2))
    file.close()
    print(f"{venue_name} Complete!")



# %%

run()



