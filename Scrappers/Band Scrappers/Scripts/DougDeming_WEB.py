# %%
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as BS
import requests

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
shows_array = []
url = "https://dougdeming.com/calendar?"
venue_name = ""
band_name = "Doug Deming & The Jewel Tones"

# %%
options = Options()
options.headless = False
driver = webdriver.Chrome(executable_path= '/Volumes/Work/Face2Face/Xity/streetTeam/Scrappers/chromedriver', options = options)

# %%
driver.get(url)

# %%
page1 = driver.page_source
driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[1]/div/div[1]/div/div[3]/div/div/div/div/div/section/div/section/div/nav/span[4]/a").click()
page2 = driver.page_source

# %%
driver.quit()

# %%
soup1 = BS(page1, 'lxml')
soup2 = BS(page2, 'lxml')

# %%
page1_shows = soup1.find_all('div', class_ = 'event-detail')
page2_shows = soup2.find_all('div', class_ = 'event-detail')

all_shows = page1_shows + page2_shows

# %%
for show in all_shows:
    venue_raw = show.find('a').text
    venue_name = venue_raw.split(',')[0]

    if any([x in venue_name.lower() for x in ohmicity_shared.venue_array]):  
        pass
    else:
        
        continue

    show_date = show.find('span', class_ = 'date').text
    show_date_time = show.find('span', class_ = 'time').text

    raw_date = show_date + ' ' + show_date_time

    this_time = parse(raw_date)
    date_string = '{:%b %d, %Y %-I:%M%p}'.format(this_time)

    showDict = {}
    showDict['venue'] = venue_name
    showDict['band'] = band_name
    showDict['dateString'] = date_string
    shows_array.append(showDict)

# %%
shows = {}
shows['shows'] = shows_array

save_path = ohmicity_shared.band_data_path
file_name = band_name + '.json'
complete_name = os.path.join(save_path, file_name)

file = open(complete_name, 'w')
file.write(json.dumps(shows, indent = 2))
file.close()
print(f"{band_name} Complete!")


