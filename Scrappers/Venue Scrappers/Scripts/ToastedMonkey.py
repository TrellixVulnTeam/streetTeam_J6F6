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
from selenium.webdriver.support import expected_conditions

# %%
#Properties
url = "https://thetoastedmonkey.com/calendar/"
time = Time
venue_name = 'Toasted Monkey'
venue_array = []
shows_array = []
ex_array = [
    'XMAS'
]

# %%
def run():
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=chrome_options, executable_path='/Volumes/Work/Face2Face/Xity/streetTeam/Scrappers/chromedriver')
    driver.get(url)

    driver.switch_to.frame('timely_initiated_0f')
    driver.find_element_by_xpath('/html/body/timely-calendar/div/div/div[3]/button').click()
    
    WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="cdk-overlay-0"]/div/div/a[4]')))
    driver.find_element_by_xpath('//*[@id="cdk-overlay-0"]/div/div/a[4]').click()

    Time.sleep(2)

    html = driver.page_source
    driver.quit()
    soup = BS(html, 'lxml')

    events = soup.find_all(class_='timely-agenda-event-header')
    
    for event in events:
        band_name = event.find(class_='timely-agenda-event-title-text timely-title-text').text
        
        '''Removes the space at the end from the band_name'''
        band_name = band_name.replace(' ', '', 1)
        length = len(band_name)
        band_name = band_name[:length-1]

        '''!!!! FILTER !!!!'''
        if any([x in band_name for x in ex_array]): 
                continue

        raw_date = event.find(class_='timely-agenda-event-time ng-star-inserted').text
        raw_date = raw_date.replace(' @', '')

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
            print('Error: Toasted Monkey')
    
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




