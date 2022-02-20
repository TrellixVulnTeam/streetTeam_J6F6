# %%
import json
import os
import datetime
import time as Time
from posixpath import commonpath, splitext
from bs4.element import NavigableString
from dateutil.parser import parse
from sys import excepthook
from bs4 import BeautifulSoup
import requests
import uuid
import re
from requests import exceptions 

# %% [markdown]
# Next decide which urls to scarpe and put them into an array so you can iterate through them

# %%

#URL's to be scrapped
url1 = 'https://www.thebigcatchatsaltcreek.com/entertainment.html'
url2 = ''
url3 = ''
url4 = ''
url5 = ''
url_array = [url1] 

# %% [markdown]
# Create a function that will iterate through the url_array and scrape webpage

# %%
#Properties
venue_name = 'Big Catch of Salt Creek'
band_name = ''
date_string = ''

# %%
def scape_urls(arr):
    for i in arr:
        response = requests.get(i).text
        soup = BeautifulSoup(response, 'lxml')

        for collumn in soup.find_all('div', class_ ='col-md-3'):

            title = collumn.find('h3', class_ ='mbr-fonts-style group-title mbr-black align-left display-2')
            if not title:
                #print('BROKEN')
                continue

            if 'Thursday' in title.text:
                #print('WORKING Thursday!!!')
                #Grab a single Show
                for single_Show in collumn.find_all('div', class_ ='col-md-12 menu-item'):
                #print(single_Show.text)
                    date_time = None
                    venue_name = "Big Catch of Salt Creek"
                    band_name = ''
                    time_string = '5:00PM'
                    date_string = ''
                

                    #Early Shows
                    try: 

                        #Band
                        band_Name = single_Show.find('p', class_ = 'box-text mbr-black mbr-fonts-style display-5').text
                        #print(band_Name)

                    except:
                        print('Band Error')
                        continue
                    
                    
                    try:
                        #Grab its information and organize it
                        #Date
                        date_Div = single_Show.find('h3', class_ = 'item-title mbr-fonts-style display-5').text
                        full_date = date_Div + ',' + ' ' + str(datetime.datetime.now().year)
                    
                    except:
                        print(f'Date Error: {venue_name}')
                        continue


                    try:
                        #Start Time
                        show_time = full_date + ' ' + '5:00PM'
                        date_time = parse(show_time)
                        date_string = '{:%b %d, %Y %-I:%M%p}'.format(date_time)
                        #print(date_time)

                    except:
                        print(f'Time Error: {venue_name}')
                        continue                   
                    
                    showDict = {}
                    showDict['venue'] = venue_name
                    showDict['band'] = band_Name
                    showDict['dateString'] = date_string      
                    shows.append(showDict)
                
            

            if 'Friday' in title.text:
                #print('WORKING Friday!!!')
                #Grab a single Show
                for single_Show in collumn.find_all('div', class_ ='col-md-12 menu-item'):
                #print(single_Show.text)
                    date_time = None
                    venue_name = "Big Catch of Salt Creek"
                    band_name = ''
                    time_string = '5pm'
                    date_string = ''
                

                    #Early Shows
                    try: 

                        #Band
                        band_Name = single_Show.find('p', class_ = 'box-text mbr-black mbr-fonts-style display-5').text
                        #print(band_Name)

                    except:
                        print(f'Friday Date Error: {venue_name}')
                        continue
                    
                    
                    try:
                        #Grab its information and organize it
                        #Date
                        date_Div = single_Show.find('h3', class_ = 'item-title mbr-fonts-style display-5').text
                        full_date = date_Div + ',' + ' ' + str(datetime.datetime.now().year)
                    
                    except:
                        print(f'Date Error 4: {venue_name}')
                        continue


                    try:
                        #Start Time
                        show_time = full_date + ' ' + '5:00PM'
                        date_time = parse(show_time)
                        date_string = '{:%b %d, %Y %-I:%M%p}'.format(date_time)
                        #print(date_time)

                    except:
                        print(f'Date Error 1: {venue_name}')
                        continue              
                    
                    showDict = {}
                    showDict['venue'] = venue_name
                    showDict['band'] = band_Name
                    showDict['dateString'] = date_string      
                    shows.append(showDict)
            
            if 'Saturday' in title.text:
                #print('WORKING Saturday!!!')
                #Grab a single Show
                for single_Show in collumn.find_all('div', class_ ='col-md-12 menu-item'):
                #print(single_Show.text)
                    date_time = None
                    venue_name = "Big Catch of Salt Creek"
                    band_name = ''
                    time_string = '5pm'
                    date_string = ''
                    
                    
                    try:
                        #Date
                        date_Div = single_Show.find('h3', class_ = 'item-title mbr-fonts-style display-5').text
                        full_date = date_Div + ',' + ' ' + str(datetime.datetime.now().year)

                        #print(full_date)
                    
                    except:
                        print(f'Date Error 2: {venue_name}')
                        continue


                    
                    try:
                        '''
                        This handles the two shows on Saturday. Had to seperate by string manipulation because of the single 'p' tag used to 
                        write both shows. Removed dashes, removed show start and end times as they are consistent, seperated strings
                        by '5pm' substring, added show times back in, made model for first show and appended, did same to second show,
                        and done.
                        '''
                        for text in single_Show.find_all('p', class_ ='box-text mbr-black mbr-fonts-style display-5'):
                            dual_show = " ".join(text.text.split()).replace('<br/>', ' ')
                            no_dash = dual_show.replace('-', ' ')
                            remove_3pm = no_dash.replace('3pm', '')
                            remove_8pm = remove_3pm.replace('8pm', '')
                            show12 = remove_8pm.partition("5pm")[0]
                            
                            show12_name = show12.replace('12pm ', '')
                            show_time = full_date + ' ' + '12PM'
                            date_time = parse(show_time)
                            date_string = '{:%b %d, %Y %-I:%M%p}'.format(date_time)

                            showDict = {}
                            showDict['venue'] = venue_name
                            showDict['band'] = show12_name
                            showDict['dateString'] = date_string      
                            shows.append(showDict)


                            show5_name = remove_8pm.partition("5pm ")[2]
                            show_time = full_date + ' ' + '5:00PM'
                            date_time = parse(show_time)
                            date_string = '{:%b %d, %Y %-I:%M%p}'.format(date_time)

                            showDict = {}
                            showDict['venue'] = venue_name
                            showDict['band'] = show5_name
                            showDict['dateString'] = date_string      
                            shows.append(showDict)
                        
                        #print(show5_name)

                    except:
                        print(f'Date Error 3: {venue_name}')
                        continue

                #print(shows)   


            if 'Sunday' in title.text:
                #print('SUN')
                #Grab a single Show
                for single_Show in collumn.find_all('div', class_ ='col-md-12 menu-item'):
                #print(single_Show.text)
                    date_time = None
                    venue_name = "Big Catch of Salt Creek"
                    band_name = ''
                    time_string = '5pm'
                    date_string = ''
                    
                    
                    try:
                        #Date
                        date_Div = single_Show.find('h3', class_ = 'item-title mbr-fonts-style display-5').text
                        full_date = date_Div + ',' + ' ' + str(datetime.datetime.now().year)

                        #print(full_date)
                    
                    except:
                        print(f'Date Error 5: {venue_name}')
                        continue

                    try:
                        '''
                        This handles the two shows on Sunday. Had to seperate by string manipulation because of the single 'p' tag used to 
                        write both shows. Removed dashes, removed show start and end times as they are consistent, seperated strings
                        by '4pm' substring, added show times back in, made model for first show and appended, did same to second show,
                        and done.
                        '''
                        for text in single_Show.find_all('p', class_ ='box-text mbr-black mbr-fonts-style display-5'):
                            dual_show = " ".join(text.text.split()).replace('<br/>', ' ')
                            no_dash = dual_show.replace('-', ' ')
                            remove_3pm = no_dash.replace('3:30pm', '')
                            remove_7pm = remove_3pm.replace('7pm', '')
                            show12 = remove_7pm.partition("4pm")[0]
                            
                            show12_name = show12.replace('12:30pm ', '')
                            show_time = full_date + ' ' + '12PM'
                            date_time = parse(show_time)
                            date_string = '{:%b %d, %Y %-I:%M%p}'.format(date_time)

                            showDict = {}
                            showDict['venue'] = venue_name
                            showDict['band'] = show12_name
                            showDict['dateString'] = date_string      
                            shows.append(showDict)


                            show4_name = remove_7pm.partition("4pm ")[2]
                            show_time = full_date + ' ' + '4:00PM'
                            date_time = parse(show_time)
                            date_string = '{:%b %d, %Y %-I:%M%p}'.format(date_time)

                            showDict = {}
                            showDict['venue'] = venue_name
                            showDict['band'] = show4_name
                            showDict['dateString'] = date_string      
                            shows.append(showDict)
                        
                        #print(show4_name)

                    except:
                        print(f'Model Error: {venue_name}')
                        continue


# %%
shows = []
scape_urls(url_array)

# %%
#Create JSON Structure
showDict = {}
showDict['shows'] = shows

#Save To json file
import OhmicityShared
save_path = OhmicityShared.ohmicity_shared.venue_data_path
file_name = venue_name + '.json'
complete_name = os.path.join(save_path, file_name)

file = open(complete_name, 'w')
file.write(json.dumps(showDict, indent = 2))
file.close()
print(f"{venue_name} Complete!")



