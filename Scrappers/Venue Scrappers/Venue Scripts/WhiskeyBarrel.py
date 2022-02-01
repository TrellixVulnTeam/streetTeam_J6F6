# %%
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as BS

import time as Time
import re
from dateutil.parser import parse
import datetime
from dateutil.relativedelta import relativedelta
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
url = "https://www.thewhiskeybarrelbar.com/events"
time = Time
venue_name = 'The Whiskey Barrel'
venue_array = []
shows = []
ex_array = [
    
]

# %%
def run():
    shows_array = []
    #Navigate Site with Selenium
    #Get List View
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    html = driver.page_source
    soup = BS(html, 'lxml')
    driver.quit()
    
    #Useful Selenium Commands
        #driver.find_element_by_class_name('').click()/or no .click()
        #driver.find_element_by_tag_name('').click()/or no .click()
        #driver.find_element_by_xpath('').click()/or no .click()
        #Time.sleep(Int)
    
    
    #Get Data with BeautifulSoup
    venue_name = 'The Whiskey Barrel'
    band_name = ''
    date_string = ''

    events = soup.find_all(class_='pm-calendar-event-content-right')
    
    for event in events:
        band_name = event.find('a').text
        raw_date = event.find('p').text

        this_time = parse(raw_date)
        date_string = '{:%b %d, %Y %-I:%M%p}'.format(this_time)

        try:
            show_time = parse(raw_date)

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
            print('Error: Whiskey Barrel')

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
run()


