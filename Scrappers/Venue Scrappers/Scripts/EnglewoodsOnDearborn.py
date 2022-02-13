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

#For keyboard key programmatic control
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# %%
#Properties
idk = "https://www.englewoodsondearborn.com/music-calendar"
time = Time

venue_name = 'Englewoods On Dearborn'
band_name = ''
date_string = ''

shows = []
venue_array = []

ex_array = [
    '2022', 'Closed'
]

# %%
def run():
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=chrome_options, executable_path='/Users/nathanhedgeman/Documents/Scrappers/chromedriver')
    driver.get(idk)
    Time.sleep(3)
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="comp-jqsjus6s"]/iframe'))
    html = driver.page_source
    driver.quit()
    soup = BS(html, 'lxml')
    events = soup.find_all('table', class_='day ng-scope')

    for event in events:
        name = event.find(class_="event-title link-container event-title-font break-words")
        band_name = name.text.strip()
        
        if any([x in band_name for x in ex_array]):
            continue

        raw_date = event.find(class_='when material-icon date ng-binding').text.strip()
        raw_time = event.find(class_='when material-icon time ng-binding ng-scope').text.strip().split(sep='-', maxsplit=1)[0]
        show_date = raw_date + ' ' + raw_time

        final_date = parse(show_date)
        date_string = '{:%b %d, %Y %-I:%M%p}'.format(final_date)

        try:
            showDict = {}
            showDict['band'] = band_name
            showDict['dateString'] = date_string
            shows.append(showDict)

        except:
            print('ENGLEWOOD ON DEARBORN: ERROR')
    
    #Save To json file
    '''
    '''
    venDict = {}
    venDict['venueName'] = venue_name
    venDict['shows'] = shows

    venue_array = [venDict]
    finalDict = {}
    finalDict['venue'] = venue_array

    #Save To json file
    import OhmicityShared
    save_path = OhmicityShared.ohmicity_shared.venue_data_path
    file_name = venue_name + '.json'
    complete_name = os.path.join(save_path, file_name)

    file = open(complete_name, 'w')
    file.write(json.dumps(finalDict, indent = 2))
    file.close()
    print(f"{venue_name} Complete!")

# %%
run()


