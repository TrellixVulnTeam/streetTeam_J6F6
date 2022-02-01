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
url = "https://calendar.google.com/calendar/u/0/r"
page_source_array = []
time = Time
date_string = ''
venue_name = ''
venue_array = []
ex_array = [
    'Witch', 'Tampa Bay National Wildlife', 'Closed', 'CLOSED', 'closed', 'Sunday', 'Holiday',
    'Trivia', 'TRIVIA', 'Axe Throwing', "Magic Monday", 'Comedy', 'Yoga', 'Festival',
    'Beer Stein', 'Private', 'Birthday', 'Drag', 'Christmas', '8AM BREAKFAST', '$',
    'INDUSTRY NITE', "Captain's Rummer Wed", "GIRLS NIGHT OUT", 'Bingo', 'NFL',
    'MUSIC HALL', 'New World', 'CLOSED', 'Jugglin', 'Video Night', 'Karaoke', 'KARAOKE', 'TBD',
    'Murder Mystery', 'FOOTBALL', 'tentative', 'BRUNCH with Live Music', 'tribute', 'DJ', "GIRL'S NIGHT OUT",
    'presented', "Presented", 'Pool', 'Taco Truck', 'taco truck', 'superbowl', 'Food', 'Grill', 'BBQ', 'Podcast'
    
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
Time.sleep(4)
keys_brewing = driver.find_element_by_xpath('//*[@id="tkQpTb"]/div/div[1]/li/label/div[1]/div/div')
keys_brewing.click()
Time.sleep(2)
keys_brewing_html = driver.page_source
page_source_array.append(keys_brewing_html)
keys_brewing.click()

ale_and_witch = driver.find_element_by_xpath('//*[@id="tkQpTb"]/div/div[2]/li/label/div[1]/div/div')
ale_and_witch.click()
Time.sleep(2)
ale_and_witch_html = driver.page_source
page_source_array.append(ale_and_witch_html)
ale_and_witch.click()

bahi_hut = driver.find_element_by_xpath('//*[@id="tkQpTb"]/div/div[3]/li/label/div[1]/div/div')
bahi_hut.click()
Time.sleep(2)
bahi_hut_html = driver.page_source
page_source_array.append(bahi_hut_html)
bahi_hut.click()

dockside = driver.find_element_by_xpath('//*[@id="tkQpTb"]/div/div[4]/li/label/div[1]/div/div')
dockside.click()
Time.sleep(2)
dockside_html = driver.page_source
page_source_array.append(dockside_html)
dockside.click()

drunken_clam = driver.find_element_by_xpath('//*[@id="tkQpTb"]/div/div[5]/li/label/div[1]/div/div')
drunken_clam.click()
Time.sleep(2)
drunken_clam_html = driver.page_source
page_source_array.append(drunken_clam_html)
drunken_clam.click()

gilligans = driver.find_element_by_xpath('//*[@id="tkQpTb"]/div/div[6]/li/label/div[1]/div/div')
gilligans.click()
Time.sleep(2)
gilligans_html = driver.page_source
page_source_array.append(gilligans_html)
gilligans.click()

green_iguana = driver.find_element_by_xpath('//*[@id="tkQpTb"]/div/div[7]/li/label/div[1]/div/div')
green_iguana.click()
Time.sleep(2)
green_iguana_html = driver.page_source
page_source_array.append(green_iguana_html)
green_iguana.click()

island_time = driver.find_element_by_xpath('//*[@id="tkQpTb"]/div/div[8]/li/label/div[1]/div/div')
island_time.click()
Time.sleep(2)
island_time_html = driver.page_source
page_source_array.append(island_time_html)
island_time.click()

mattisons_city = driver.find_element_by_xpath('//*[@id="tkQpTb"]/div/div[9]/li/label/div[1]/div/div')
mattisons_city.click()
Time.sleep(2)
mattisons_city_html = driver.page_source
page_source_array.append(mattisons_city_html)
mattisons_city.click()

mattisons_river = driver.find_element_by_xpath('//*[@id="tkQpTb"]/div/div[10]/li/label/div[1]/div/div')
mattisons_river.click()
Time.sleep(2)
mattisons_river_html = driver.page_source
page_source_array.append(mattisons_river_html)
mattisons_river.click()

motorworks = driver.find_element_by_xpath('//*[@id="tkQpTb"]/div/div[11]/li/label/div[1]/div/div')
motorworks.click()
Time.sleep(2)
motorworks_html = driver.page_source
page_source_array.append(mattisons_river_html)
motorworks.click()

new_world = driver.find_element_by_xpath('//*[@id="tkQpTb"]/div/div[12]/li/label/div[1]/div/div')
new_world.click()
Time.sleep(2)
new_world_html = driver.page_source
page_source_array.append(new_world_html)
new_world.click()

tj_carney = driver.find_element_by_xpath('//*[@id="tkQpTb"]/div/div[13]/li/label/div[1]/div/div')
tj_carney.click()
Time.sleep(2)
tj_carney_html = driver.page_source
page_source_array.append(tj_carney_html)
tj_carney.click()

wild_rover = driver.find_element_by_xpath('//*[@id="tkQpTb"]/div/div[14]/li/label/div[1]/div/div')
wild_rover.click()
Time.sleep(2)
wild_rover_html = driver.page_source
page_source_array.append(wild_rover_html)
wild_rover.click()

woodys = driver.find_element_by_xpath('//*[@id="tkQpTb"]/div/div[15]/li/label/div[1]/div/div')
woodys.click()
Time.sleep(2)
woodys_html = driver.page_source
page_source_array.append(woodys_html)
woodys.click()

Time.sleep(2)
driver.quit()

# %%
def run(venue_source, venue_name):
    shows_array = []
    soup = BS(venue_source, 'lxml')
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
                
                if venue_name == '3 Keys Brewing':
                    try:
                        split_name1 = split_name1.split(sep = '/ ', maxsplit=1)[1]
                    except:
                        print(split_name1)
                        pass
                
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
                    showDict['venue'] = venue_name
                    showDict['band'] = band_name
                    showDict['dateString'] = date_string
                    shows_array.append(showDict)

                except AttributeError as ex:
                    print('Error', ex)

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
run(ale_and_witch_html, "Ale and the Witch")
run(keys_brewing_html, "3 Keys Brewing")
run(dockside_html, "Dockside")
run(gilligans_html, "Gilligan's Island Bar & Grill")
run(mattisons_city_html, "Mattison's City Grille")
run(woodys_html, "Woody's River Roo")
run(bahi_hut_html, "Bahi Hut")
run(drunken_clam_html, "Drunken Clam")
run(green_iguana_html, "Green Iguana - South Westshore")
run(island_time_html, "Island Time Bar and Grill")
run(mattisons_river_html, "Mattison's Riverwalk Grille")
run(motorworks_html, "Motorworks Brewing")
run(new_world_html, "New World Brewery")
run(wild_rover_html, "Wild Rover Brewery")
run(tj_carney_html, "TJ Carney's")


