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
url_array = [
    'https://www.reverbnation.com/shevonnephilidor/shows', 'https://www.reverbnation.com/diamonddixie/shows', 'https://www.reverbnation.com/selwynbirchwood/shows', ''
]



# %%
options = Options()
options.headless = True

driver = webdriver.Chrome(executable_path= '/Volumes/Work/Face2Face/Xity/streetTeam/Scrappers/chromedriver', options = options)
'''driver = webdriver.Chrome(ChromeDriverManager().install())'''

# %%
for url in url_array:
       showDict = {}
       shows = {}
       shows_array = []

       driver.get(url)
       soup = BS(driver.page_source, 'lxml')

       band_name = soup.find('h1').text.strip()
       whole = soup.find('div', class_= 'small-12 columns')

       all_shows = whole.find_all('div', class_='full-width py4 px1-for-medium-up relative clearfix show-card')

       for show in all_shows:
              venue_name = show.find('span', class_='row bold ellipsis ng-binding ng-scope').text.strip()
              
              if any([x in venue_name.lower() for x in ohmicity_shared.venue_array]): 
                     pass
              else:
                     continue

              '''DATE'''
              month_day = show.find('div', class_= 'ellipsis bold ng-binding').text.strip()
              show_time = show.find('span', class_= 'ng-binding ng-scope').text

              raw_time = month_day + " " + show_time
              this_time = parse(raw_time)
              date_string = '{:%b %d, %Y %-I:%M%p}'.format(this_time)

              showDict['venue'] = venue_name
              showDict['band'] = band_name
              showDict['dateString'] = date_string
              
              shows_array.append(showDict)
              shows['shows'] = shows_array



       # %%
       save_path = ohmicity_shared.band_data_path
       file_name = band_name + '.json'
       complete_name = os.path.join(save_path, file_name)

       file = open(complete_name, 'w')
       file.write(json.dumps(shows, indent = 2))
       file.close()
       print(f"{band_name} Complete!")

driver.quit()
print('Reverb Nation Complete!')

# %%



