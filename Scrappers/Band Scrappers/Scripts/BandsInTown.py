# %%
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as BS

import time as time
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
import datetime
import os
import json

from OhmicityShared import ohmicity_shared

from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# %%

'''
LIST OF BANDS:

1: Selwyn Birchwood
2: Jah Movement
3: Ariella
4: Sarah Diamond
5: Scott Clay
6: NoFilter
'''

urls = [
    'https://www.bandsintown.com/a/8596214-selwyn-birchwood-band?', 'https://www.bandsintown.com/a/4009595-jah-movement?', 'https://www.bandsintown.com/a/1710060-ariella?',
    'https://www.bandsintown.com/a/8711265-scott-clay?', 'https://www.bandsintown.com/a/6309651-nofilter?', 'https://www.bandsintown.com/a/2470649'
    
]

band_name = '****************'

# %%
options = Options()
options.headless = False
driver = webdriver.Chrome(executable_path= '/Volumes/Work/Face2Face/Xity/streetTeam/Scrappers/chromedriver', options = options)

# %%
def runAll(url):
    links_array = []
    shows_array = []
    
    driver.get(url)

    band_name = driver.find_element(By.CLASS_NAME, 'sKZg4aYIueqDu5cAfZ_q').text.strip()

    time.sleep(2)
    show_more_button = driver.find_element(By.XPATH, ohmicity_shared.bit_more_shows_button)
    show_more_button.click()

    all_events = driver.find_element(By.CLASS_NAME, ohmicity_shared.bit_all_shows)

    '''div = all_events.find_element(By.TAG_NAME, 'div')'''
    links_tags = all_events.find_elements(By.TAG_NAME, 'a')

    for link in links_tags:
        links_array.append(link.get_property('href'))

    for link in links_array:
        driver.get(link)
        
        venue_name = driver.find_element(By.CLASS_NAME, 'PbHKFXY5zk12zpdE9vqk').text

        if any([x in venue_name.lower() for x in ohmicity_shared.venue_array]): 
                    pass
        else:
                    continue

        show_date = driver.find_element(By.CLASS_NAME, 'z0MsckJvCkH2k7G8LFq9').text
        show_time = driver.find_element(By.CLASS_NAME, 'EVShpiZDtLTTZpfAxHav').text
        raw_time = show_date + " " + show_time

        this_time = parse(raw_time)
        date_string = '{:%b %d, %Y %-I:%M%p}'.format(this_time)

        showDict = {}
        showDict['venue'] = venue_name
        showDict['band'] = band_name
        showDict['dateString'] = date_string
        shows_array.append(showDict)

    shows = {}
    shows['shows'] = shows_array

    save_path = ohmicity_shared.band_data_path
    file_name = band_name + '.json'
    complete_name = os.path.join(save_path, file_name)

    file = open(complete_name, 'w')
    file.write(json.dumps(shows, indent = 2))
    file.close()
    print(f"{band_name} Complete!")
    

    

# %%
print("Bands In Town Started")

for url in urls:
    runAll(url)

driver.quit()
print("Bands In Town Complete")


