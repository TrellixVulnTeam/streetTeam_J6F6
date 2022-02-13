# %%
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as BS

import time as Time
import re
from dateutil import parser
import datetime
import os
import json

#For keyboard key programmatic control
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# %%
#Properties
url = "https://blueroostersrq.com/music/list"
shows = []
venue_array = []

# %%
def run():
    #Navigate Site with Selenium
    #Get List View
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    driver.set_window_size(1500, 1500)
    Time.sleep(3)
    #Useful Selenium Commands
        #driver.find_element_by_class_name('').click()/or no .click()
        #driver.find_element_by_tag_name('').click()/or no .click()
        #driver.find_element_by_xpath('').click()/or no .click()
        #Time.sleep(Int)
    
    #Clicks the Find Events button to load more than 5 shows
    driver.find_element_by_xpath('/html/body/div/div[2]/div/div/div/div[1]/article/div/div/div[2]/div[2]/form/div[1]/div/div/div[3]/input').click()
    Time.sleep(5)
    
    #Get Data with BeautifulSoup
    venue_name = "Blue Rooster"
    band_name = ''
    date_string = ''

    html = driver.page_source
    soup = BS(html, 'lxml')
    
    events = soup.find('div', class_ ='tribe-events-loop')
    
    for event in events.select('div[class*="type-tribe_events"]'):
        #Get Band Name
        name = event.find('a').text
        
        if not name:
            continue
        
        strip_name = name.strip()
        
        #Band Name Fixes
        alFuller_clean = strip_name.replace('\u2019s Famous', '')
        truality_clean = alFuller_clean.replace('Sunday Gospel Buffet Brunch with ', '')
        trualityALT_clean = truality_clean.replace('Sunday Gospel Brunch Buffet with ', '')
        idol_clean = trualityALT_clean.replace('American Idol Finalist ', '')
        
        clean_name = idol_clean
        band_name = clean_name
        
            
        #Get Start Time
        raw_date = event.find('span', class_='tribe-event-date-start').text
        drop_string = raw_date.replace(' @', '')
        date = parser.parse(drop_string)
        date_string = '{:%b %d, %Y %-I:%M%p}'.format(date)

        try:
            showDict = {}
            showDict['band'] = band_name
            showDict['dateString'] = date_string
            shows.append(showDict)

        except AttributeError as ex:
            print('Error', ex)


    driver.quit
    
    #Create JSON Structure
    venDict = {}
    venDict['venueName'] = venue_name
    venDict['shows'] = shows
    
    venue_array = [venDict]
    finalDict = {}
    finalDict['venue'] = venue_array

    #Save To json file
    save_path = '/Users/nathanhedgeman/Documents/Scrappers/Show Data'
    file_name = venue_name + '.json'
    complete_name = os.path.join(save_path, file_name)

    file = open(complete_name, 'w')
    file.write(json.dumps(finalDict, indent = 2))
    file.close()
    print("Complete!")

# %%
run()

# %%



