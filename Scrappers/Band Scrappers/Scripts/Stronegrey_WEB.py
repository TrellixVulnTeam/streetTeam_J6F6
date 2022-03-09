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
url = "https://www.stonegreyofficial.com/tour-dates"
venue_name = ""
band_name = "Stonegrey"

# %%
options = Options()
options.headless = False
driver = webdriver.Chrome(executable_path= '/Volumes/Work/Face2Face/Xity/streetTeam/Scrappers/chromedriver', options = options)

# %%
driver.get(url)

# %%
driver.switch_to.frame(driver.find_element(By.XPATH, '/html/body/div/div/div[3]/div/main/div/div/div/div[2]/div/div/div/div[3]/iframe'))

# %%
page1 = driver.page_source

# %%
driver.quit()

# %%
soup1 = BS(page1, 'lxml')

# %%
page1_shows = soup1.find_all('div', class_ = 'event text-font')

# %%
print(page1_shows)

# %%
len(page1_shows)

# %%
for show in page1_shows:
    venue_name = show.find('span').text
    
    if any([x in venue_name.lower() for x in ohmicity_shared.venue_array]):  
        pass
    else:
        continue
    if venue_name == "O'Brien's Wesley Chapel":
        continue

    raw_date = show.find('div', class_ = "when material-icon date ng-binding").text
    raw_time = show.find('div', class_ = "when material-icon time ng-binding ng-scope").text.split('-')[0]

    raw_date_time = raw_date + " " + raw_time

    this_time = parse(raw_date_time)
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


