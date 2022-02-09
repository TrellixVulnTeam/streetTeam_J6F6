# %%
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup as BS

import time as time
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
import datetime
import os
import json
import time

from OhmicityShared import ohmicity_shared
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# %%
band_name = "Danielle Mohr"
url = "https://www.daniellemohrmusic.com/"
shows_array = []
shows = {}
venue_array = []

# %%
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.set_window_size(1500, 1500)
driver.get(url)

# %%
frame = driver.find_element(By.CLASS_NAME, '_49_rs')
actions = ActionChains(driver)
actions.move_to_element(frame).perform()


# %%
driver.switch_to.frame(driver.find_element(By.CLASS_NAME, '_49_rs'))

# %%
days = driver.find_elements(By.CLASS_NAME, 'events')


for day in days:
    day_events = day.find_elements(By.CLASS_NAME, 'ng-scope')
    
    for event in day_events:
        event.click()
        
        popup = event.find_element(By.CLASS_NAME, 'full-height')
        venue_name = popup.find_element(By.CSS_SELECTOR, '.popup-title').text
        date = popup.find_element(By.CSS_SELECTOR, '.popup-when').text
        day_time = popup.find_element(By.CSS_SELECTOR, '.popup-time').text.split('-')[0]
        
        raw_date = date + ' ' + day_time

        date = parse(raw_date)
        date_string = '{:%b %d, %Y %-I:%M%p}'.format(date)
        
        '''print(venue_name)
        print(band_name)
        print(date_string)
        print()'''

        time.sleep(0.5)
        showDict = {}
        showDict['venue'] = venue_name
        showDict['band'] = band_name
        showDict['dateString'] = date_string

        driver.find_element(By.XPATH, '//*[@id="weeks-container"]/div[1]/div[1]/div[1]').click()

        shows_array.append(showDict)
        shows['shows'] = shows_array
        break



# %%


# %%
shows = {}
shows['shows'] = shows_array

#Save To json file
save_path = ohmicity_shared.band_data_path
file_name = band_name + '.json'
complete_name = os.path.join(save_path, file_name)

file = open(complete_name, 'w')
file.write(json.dumps(shows, indent = 2))
file.close()
driver.quit()
print(f"{band_name} Complete!")


