import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import os
import regex as re

"""
In this case, all the url data for the languages is inserted into the file via javascript. I cba to deal
with that so I found their xlsx version. Will be getting data using pandas then converting to text.
"""
# Urls
filename = 'data.xlsx'

def get_languages(filename, filepath):
    """
    Filename and Filepath must be string input into the function.
    """

    # Reading xlsx
    fullpath = os.path.join(filepath, filename)
    languages_df = pd.read_excel(fullpath, 'Sheet 1')
    languages_df = languages_df.iloc[1:-1, 0]
    languages_df = languages_df.dropna()
    #print(languages_df.head(30))

    # Cleaning the data
    do = True
    convert_to_enum = lambda x: str(x).upper().replace("/", "_").replace(" (", "_").replace(")", "").replace(" ", "_") if x is not None else do == False
    totals = lambda x: x.endswith('TOTAL')
    languages_df = languages_df.map(convert_to_enum)
    languages_arr = np.array(languages_df.values)
    def findWholeWord(w):
        return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search
    print(languages_arr)
    
    # Saving languages to data 
    # Use config in future to save to data directory
    with open('languages.txt', mode='w', encoding='utf-8') as languages_file:
        [languages_file.write(languages_arr[i] + '\n') for i in range(0, len(languages_arr))]
    
get_languages(filename, r'C:\Users\pries\OneDrive\Documents\Coding Projects\Library Management System\Library Management System\Library Management System\enums\data_and_scrapings\scripts')