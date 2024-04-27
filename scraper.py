# Import libraries

import pandas as pd
import requests
from io import StringIO  

# Function to scrape url and return the dataframe

def players_table_scraper(url):
    #Get the HTML using a GET Request, we replace the <-- and --> to read the 3rd table (players), the one we need 
    response = StringIO(requests.get(url).text.replace('<!--', '').replace('-->', ''))
    
    #using pandas, retrieve the tables and select the players table at index 2
    stats = pd.read_html(response, header=1)[2]
    
    return stats


#Get data from four different pages
standard = players_table_scraper('https://fbref.com/en/comps/905/stats/Copa-de-la-Liga-Profesional-Stats')
passing = players_table_scraper('https://fbref.com/en/comps/905/passing/Copa-de-la-Liga-Profesional-Stats')
passtypes = players_table_scraper('https://fbref.com/en/comps/905/passing_types/Copa-de-la-Liga-Profesional-Stats')
defending = players_table_scraper('https://fbref.com/en/comps/905/defense/Copa-de-la-Liga-Profesional-Stats')

print(standard.head())



    