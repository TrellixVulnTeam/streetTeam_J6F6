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
url = "https://calendar.google.com/calendar/u/0/r"
page_source_array = []
time = Time
date_string = ''
venue_array = []
ex_array = [
    'Witch', 'Tampa Bay National Wildlife', 'Closed', 'CLOSED', 'closed', 'Sunday', 'Holiday',
    'Trivia', 'TRIVIA', 'Axe Throwing', "Magic Monday", 'Comedy', 'Yoga', 'Festival',
    'Beer Stein', 'Private', 'Birthday', 'Drag', 'Christmas', '8AM BREAKFAST', '$',
    'INDUSTRY NITE', "Captain's Rummer Wed", "GIRLS NIGHT OUT", 'Bingo', 'NFL',
    'MUSIC HALL', 'New World', 'CLOSED', 'Jugglin', 'Video Night', 'Karaoke', 'KARAOKE', 'TBD',
    'Murder Mystery', 'FOOTBALL', 'tentative', 'BRUNCH with Live Music', 'tribute', 'DJ', "GIRL'S NIGHT OUT",
    'presented', "Presented", 'Pool'
]

# %%
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)

    

# %% [markdown]
# Put in email address

# %%
Time.sleep(3)
email = 'f2ftestbench@gmail.com'
email_login = driver.find_element_by_xpath('//*[@id="identifierId"]')
email_login.send_keys(email)
next_button_1 = driver.find_element_by_xpath('//*[@id="identifierNext"]/div/button').click()



# %% [markdown]
# Put in password

# %%
Time.sleep(3)
password = '12908874.'
password_text_field = driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
password_text_field.send_keys(password)
next_button_2 = driver.find_element_by_xpath('//*[@id="passwordNext"]/div/button').click()
    

# %% [markdown]
# Get Page Sources

# %%
Time.sleep(3)
mattisons_city = driver.find_element_by_xpath('//*[@id="tkQpTb"]/div/div[11]/li/label/div[1]/div/div')
mattisons_city.click()
Time.sleep(2)
mattisons_river_html = driver.page_source
page_source_array.append(mattisons_river_html)
mattisons_city.click()
Time.sleep(2)
driver.quit()

# %%
def runMat():
    shows_array = []
    soup = BS(mattisons_river_html, 'lxml')
    days = soup.find_all('div', role ='rowgroup')

    for day in days:
        holder_date = day.find('div', role = 'link')
        if holder_date == None:
            continue
        event_date = holder_date['aria-label']
    
        date = event_date.strip(', today'); ''' !!!!!GOT DATE!!!!! '''
        
        event_discriptions = day.find_all('div', role ='row')
        for x in event_discriptions:
            name = x.find('div', role = 'button')

            if name == None:
                continue

            '''Green Iguana FIX'''
            if name.text == ' band': 
                continue

            
            '''!!!!!FILTER!!!!!!'''
            if any([x in name.text for x in ex_array]): 
                continue
            
            else:
                pres = x.find('div', role = 'presentation')
                raw_time = pres.find('div', role = 'gridcell')
                start_time = raw_time.text.split(sep=' ', maxsplit=1)[0]
                
                if 'pm' in start_time:
                    final_time = start_time

                elif 'am' in start_time:
                    final_time = start_time
                
                else:
                    final_time = start_time + 'pm'

                if 'All' in final_time:
                    final_time = '7pm'
                              
                show_date = date + " " + final_time

                band_name = ''
                split_name1 = name.text.split(sep=' |', maxsplit=1)[0]
                split_name1 = split_name1.split(sep=' @', maxsplit=1)[0]
                
                try:
                    '''Bahi Hut FIX'''
                    split_name1 = split_name1.split(sep='Music: ', maxsplit=1)[1]
                except:
                    pass
                
                split_name1 = split_name1.split(sep=' solo: ', maxsplit=1)[0]
                split_name2 = ''
                
                if split_name1 == None:
                    split_name2 = name.text.split(sep=' |', maxsplit=1)[0]
                    plit_name2 = split_name2.text.split(sep=' @', maxsplit=1)[0]
                    
                    try:
                        '''Bahi Hut FIX'''
                        split_name2 = split_name2.split(sep='Music: ', maxsplit=1)[1] 
                    except:
                        pass
                    
                    split_name2 = split_name2.split(sep=' solo: ', maxsplit=1)[0]
                    band_name = split_name2
                else:
                    band_name = split_name1

                if ' "Himself"' in band_name:
                    band_name = band_name.replace(' "Himself"', '')

                this_time = parse(show_date)
                date_string = '{:%b %d, %Y %-I:%M%p}'.format(this_time)

                try:
                    showDict = {}
                    showDict['venue'] = "Mattison's Riverwalk Grille"
                    showDict['band'] = band_name
                    showDict['dateString'] = date_string
                    shows_array.append(showDict)

                except AttributeError as ex:
                    print('Error', ex)

     #Export as JSON
    shows = {}
    shows['shows'] = shows_array

    #Save To json file
    save_path = OhmicityShared.ohmicity_shared.venue_data_path

    file_name = "Mattison's Riverwalk Grille" + '.json'
    complete_name = os.path.join(save_path, file_name)

    file = open(complete_name, 'w')
    file.write(json.dumps(shows, indent = 2))
    file.close()
    print("Mattison's Riverwalk Grille Complete!")

# %%
runMat()


