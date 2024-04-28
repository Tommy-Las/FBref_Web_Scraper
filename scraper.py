# Import libraries

import pandas as pd
import requests
from io import StringIO

pd.set_option('display.max_columns', None)

# Names of columns for later renaming 
standard_new_names = {"MP": "Matches Played", "PrgC": "Progressive Carries", "PrgP": "Progressive Passes", "PrgR":"Progressive Passes Received",
    "Gls.1": "Gls 90", "Ast.1": "Ast 90", "G+A.1": "G+A 90", "G-PK.1": "G-PK 90", "xG.1": "xG 90", "xAG.1": "xAG 90", "npxG.1": "npxG 90", "npxG+xAG.1": "npxG+xAG 90"
}
passing_new_names = {
    'Cmp': 'Total Passes Completed',
       'Att': 'Total Passes Attempted', 'Cmp%':'Total Passes Success %', 'TotDist': 'Total Passing Distance', 'PrgDist': 'Progressive Passing Distance', 'Cmp.1': 'Short Passes Completed',
       'Att.1': 'Short Passes Attenpted', 'Cmp%.1': 'Short Passes Success %',
       'Cmp.2': 'Medium Passes Completed', 'Att.2': 'Medium Passes Attempted', 'Cmp%.2': 'Medium Passes Success %', 'Cmp.3': 'Long Passes Completed', 'Att.3': 'Long Passes Attempted', 'Cmp%.3': 'Long Passes Success %',
       'KP': 'Key Passes', '1/3': 'Passes into Final Third', 'PPA': 'Passes into Penalty Area', 'CrsPA': 'Crosses into Penalty Area', 'PrgP': "Progressive Passes"
}
passtypes_new_names = {
    'Att': 'Total Passes Attempted',
       'Live': 'Live-ball Passes', 'Dead': 'Dead-ball Passes', 'FK': 'Free Kicks Passes', 'TB': 'Through Balls', 'Sw': 'Switches', 'Crs':'Crosses', 'TI': 'Throw Ins', 'CK': 'Corner Kicks', 
       'In': 'Corner Kicks Inward', 'Out': 'Corner Kick Outward', 'Str': 'Corner Kick Straight',
       'Cmp': 'Passes Completed', 'Off': 'Passes Offside', 'Blocks': 'Passes Blocked by Opponent'
}
defending_new_names = {
    'Tkl': 'Tackles',
       'TklW': 'Tackles Won', 'Def 3rd': 'Tackles Def 3rd', 'Mid 3rd': 'Tackles Mid 3rd', 'Att 3rd':'Tackles Att 3rd', 'Tkl.1': 'Dribblers Tackled', 'Att': 'Dribbles Challenged', 'Tkl%': '% Dribblers Tackled',
       'Lost': 'Challenges Lost', 'Blocks':'Total Blocks','Sh': 'Shots Blocked', 'Pass':'Passes Blocked', 'Int':'Interceptions', 'Tkl+Int':'Tackles+Interceptions', 'Clr':'Clearances', 'Err':'Defensive Errors'
}
# Function to scrape url and return the dataframe

def players_table_scraper(url):
    """Given a FBref URL, scrape the data and return a pandas dataframe 

    Args:
        url (string): URL of the FBref website we want to scrape

    Returns:
        pd.DataFrame: Dataframe of the data scraped
    """
    #Get the HTML using a GET Request, we replace the <-- and --> to read the 3rd table (players), the one we need 
    response = StringIO(requests.get(url).text.replace('<!--', '').replace('-->', ''))
    
    #using pandas, retrieve the tables and select the players table at index 2
    stats = pd.read_html(response, header=1)[2]
    
    return stats

# Function to rename column names
def column_rename(data, new_names):
    """rename columns from given dataset using a dictionary with the column names and its new names

    Args:
        data (pd.DataFrame): DataFrame that its columns are being renamed
        new_names (dict): dictionary where the keys are the current columns of the dataframe, and the values are the new names
    """
    
    data.rename(new_names, inplace = True, axis=1)


#Get data from four different pages
standard = players_table_scraper('https://fbref.com/en/comps/905/stats/Copa-de-la-Liga-Profesional-Stats')
passing = players_table_scraper('https://fbref.com/en/comps/905/passing/Copa-de-la-Liga-Profesional-Stats')
passtypes = players_table_scraper('https://fbref.com/en/comps/905/passing_types/Copa-de-la-Liga-Profesional-Stats')
defending = players_table_scraper('https://fbref.com/en/comps/905/defense/Copa-de-la-Liga-Profesional-Stats')

#Preprocessing of data

#Column renaming
column_rename(standard, standard_new_names)
column_rename(passing, passing_new_names)
column_rename(passtypes, passtypes_new_names)
column_rename(defending, defending_new_names)


# we want to join dataframes, we concatenate excluding the duplicate columns
all_data = pd.concat([standard, passing[passing.columns.difference(standard.columns)]], axis=1)
all_data = pd.concat([all_data, passtypes[passtypes.columns.difference(all_data.columns)]], axis=1)
all_data = pd.concat([all_data, defending[defending.columns.difference(all_data.columns)]], axis=1)

all_data.info()

all_data.to_csv("FBRef_2024_CopaDeLaLiga_MidfieldersAnalysis.csv", sep=',', encoding='UTF-8')


    