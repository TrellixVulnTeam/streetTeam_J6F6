# %%
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
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
url = "https://www.seminolehardrocktampa.com/events#d_event%20type=Live%20Performance&d_v=1"
time = Time
venue_name = 'Seminole Hard Rock Hotel & Casino'
shows_array = []
venue_array = []

ex_array = [
    'DJ', 'Drag'
]

# %%
def run():
    chrome_options = Options()
    '''chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')'''
    driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
    driver.get(url)

    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="section-1"]/li[2]/div')))
        
    except:
        print("Page not loaded yet")

    html = driver.page_source
    driver.quit()
    
    soup = BS(html, 'lxml')
    year = datetime.datetime.now().date().strftime('%Y')
    year_to_check = '2022'
    all_data = soup.find(class_='pagination-list active')

    all_shows = all_data.find_all('li')

    for show in all_shows:
        event_type = show.find(class_='listCCard__place__venue').text
        
        if 'Hard Rock Event Center' in event_type:
            continue
        
        if 'Hard Rock Event Center' in event_type:
            continue

        band_name = show.find('h2').text

        if any([x in band_name for x in ex_array]): 
                continue

        show_data = show.find(class_="listCCard__time__wrap")

        check_date = show_data.text.split(' |')[0].strip()
        
        if year_to_check in check_date:
            good_date = check_date.split(', ',1)[1]
            show_time = show_data.text.split(' |')[1].strip().split(' -')[0]

            if show_time == 'Noon':
                show_time = '12:00PM'

            full_time = f'{good_date} {show_time}'

            try:
                this_time = parse(full_time)
                date_string = '{:%b %d, %Y %-I:%M%p}'.format(this_time)
            
            except:
                continue
            
        else:
            show_date = show_data.text.split(' |')[0].split(',')[1].strip()
            show_time = show_data.text.split(' |')[1].strip().split(' -')[0]
            
            if show_time == 'Noon':
                show_time = '12:00PM'

            full_time = f'{show_date}, {year} {show_time}'

            try:
                this_time = parse(full_time)
                date_string = '{:%b %d, %Y %-I:%M%p}'.format(this_time)
            
            except:
                continue

        try:
            showDict = {}
            showDict['venue'] = venue_name
            showDict['band'] = band_name
            showDict['dateString'] = date_string
            shows_array.append(showDict)

        except:
            print('Error making dictionary')

    #Save To json file
    '''
    '''
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


