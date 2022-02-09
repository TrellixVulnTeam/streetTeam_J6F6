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
url = 'https://www.bandsintown.com/a/2470649'

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)

# %%
links_array = []
shows_array = []
total_array = []

band_name = 'Sara Diamond'

# %%
venue_array = [
    '210', "Blue Rooster", 'Burger-ish', "River Roo", "Cage Brewing", "Cask & Ale", "Cask and Ale", "Coconut", "Cottonmouth", "Daiquiri Deck Raw Bar Siesta Key", "Darwin Brewing", "Del Frisco", "Dockside", "Drunken Clam",
    "Englewoods On Dearborn", "Floridian Social Club", "Flute & Dram", "Gator Club", "Gilligan", "Green Iguana", "Hideaway", "Independent Bar St Petersburg", "Independent Bar and Cafe Tampa", "Island Time Bar and Grill",
    "Joyland", "Mad Hatters", "Marina Jack", "Mattison's City Grille", "Mattison's Riverwalk Grille", "Motorworks Brewing", "New World Brewery", "O'Brien", "Pete's Place North", "Ringside Cafe", "Ruby's Elixir",
    "SandBar", "Hard Rock", "Sharky", "Siesta Key Oyster Bar", "Skipper", "St Pete Side Lot", "Stottlemyer", "Straggler", "TJ Carney", "Tamiami Tap", "The Castle", "The Pub Tampa Bay", "The Tavern At Bayboro",
    "Whiskey Barrel", "Whiskey Wings - St Peterburg", "Toasted Monkey", "White Elephant Pub", "Wild Rover Brewery", 
]

# %%
show_more_button = driver.find_element(By.CLASS_NAME, '_1GaeyllMT79LYiH-6HrT56')
show_more_button.click()

# %%
all_events = driver.find_element(By.CLASS_NAME, 'qznXLxZY-XWcgeMFMR1So')

div = all_events.find_element(By.TAG_NAME, 'div')
links_tags = div.find_elements(By.TAG_NAME, 'a')

for link in links_tags:
    links_array.append(link.get_property('href'))

# %% [markdown]
# links_array now filled with links to scrape

# %%
for link in links_array:
    driver.get(link)
    
    venue_div = driver.find_element(By.CLASS_NAME, '_2wsU7P2Nq0F2Ewki3qdVwK')
    venue_link = venue_div.find_element(By.TAG_NAME, 'a')
    venue_name = venue_link.text

    if any([x in venue_name for x in ohmicity_shared.venue_array]): 
                pass
    else:
                continue

    show_date = driver.find_element(By.CLASS_NAME, '_1TLOSkbytCU0xipvsRNoDv').text
    show_time = driver.find_element(By.CLASS_NAME, '_1iK6x88EqsupILFxTvC9ip').text
    raw_time = show_date + " " + show_time

    this_time = parse(raw_time)
    date_string = '{:%b %d, %Y %-I:%M%p}'.format(this_time)

    showDict = {}
    showDict['venue'] = venue_name
    showDict['band'] = band_name
    showDict['dateString'] = date_string
    shows_array.append(showDict)

    

    

# %%
driver.quit()
shows = {}
shows['shows'] = shows_array



# %%
save_path = ohmicity_shared.band_data_path
file_name = band_name + '.json'
complete_name = os.path.join(save_path, file_name)

file = open(complete_name, 'w')
file.write(json.dumps(shows, indent = 2))
file.close()
print(f"{band_name} Complete!")


