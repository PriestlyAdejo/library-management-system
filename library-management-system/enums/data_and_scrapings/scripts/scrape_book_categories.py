import requests as reqs
from bs4 import BeautifulSoup as bs
import numpy as np
import pandas as pd
import regex as rgx
import re

# Making Function to Scrape book categories from z-library/b-ok.cc
base_url = 'https://b-ok.cc/'
categories_url = 'https://b-ok.cc/category-list'

def get_book_categories(base_url, categories_url):
    """
    This code will be a basis for the script that gets all the data required for a book items
    and will scrape from multiple websites to get information. This will be for a mainly online library
    so majority of the books will be in online formats.
    """

    """
    Data will be split into non-fiction, and fiction
    """

    
    # Init html and data
    
    raw_html = reqs.get(categories_url)
    soup = bs(raw_html.content)
    # print(soup.prettify())

    # Testing
    """ 
    first_cat = soup.select('div.subcategories-container')[0]
    f_type = 'fiction-or-non-fiction' # All parent categories can have both
    f_name = first_cat.find('h3')['data-name']
    f_link = first_cat.find('a')['href']

    list_items = first_cat.find_all('li')
    l_type = list_items[17]['data-type'] # Fiction or Non-Fiction
    l_name = list_items[17]['data-name'] # Actual Category Name
    l_link = list_items[17].find('a')['href']
    # Need to get rid of suggest widget
    print(l_link)"""

    # Using For Loop to get data
    parent_cats = soup.select('div.subcategories-container')
    data_sv = {'Fiction': {}, 'Non-Fiction': {}}

    # _F means category is fiction
    # _NF means category is non-fiction
    # _F_NF means category can either be fiction or non-fiction

    for parent in parent_cats:
        p_type = 'fiction-or-non-fiction'
        p_name = parent.find('h3')['data-name']
        p_link = parent.find('a')['href']
        data_sv['Fiction'][f'{p_name.upper()}_F_NF'] = {'link': base_url[:-1] + p_link} #, 'sub-cats': {'link': '', 'content': []}}
        data_sv['Non-Fiction'][f'{p_name.upper()}_F_NF'] = {'link': base_url[:-1] + p_link} #, 'sub-cats': {'link': '', 'content': []}}

        list_items = parent.find_all('li')
        for idx, list_item in enumerate(list_items):
            if not list_item.find('button'):
                # print(f"\n {idx} \n")
                l_type = list_item['data-type'] 
                l_name = list_item['data-name'] 
                l_link = list_item.find('a')['href']

                # Checking if sub category is non-fiction or fiction
                if l_type == 'fiction':
                    data_sv['Fiction'][f'{p_name.upper()}_F_NF'][f'{l_name.upper()}_F'] = {'link': base_url[:-1] + l_link}
                else:
                    data_sv['Non-Fiction'][f'{p_name.upper()}_F_NF'][f'{l_name.upper()}_NF'] = {'link': base_url[:-1] + l_link} 
            else:
                continue # Button has no attrs

    # Getting all categories from dict and saving to text file and json
    import pprint as pp
    # pp.pprint(data_sv, width=20)
    # Saving to json
    import json
    with open('book_categories.json', 'w') as j_obj:
        json.dump(data_sv, j_obj, sort_keys = True)
    
    replace_chars = '()&.,-:'
    check_first = True
    for i in data_sv:
        print(i.strip().upper())
        if check_first:
            check_first = False
            with open('book_categories.txt', 'w') as file:
                file.write(i + '\n')
        else:
            with open('book_categories.txt', 'a') as file:
                file.write(i + '\n')

        for i2 in data_sv[f'{i}']:
            if i2 != 'link':    
                i2_alpha_numeric = re.sub(r"[^\w\s]", '', i2)
                i2_underscored = re.sub(r"\s+", '_', i2_alpha_numeric)
                print(i2_underscored)
                with open('book_categories.txt', 'a') as file:
                    file.write(i2_underscored + '\n')
            else:
                continue
            for i3 in data_sv[f'{i}'][f'{i2}']:
                if i3 != 'link':
                    i3_alpha_numeric = re.sub(r"[^\w\s]", '', i3)
                    i3_underscored = re.sub(r"\s+", '_', i3_alpha_numeric)
                    print(i3_underscored)
                    with open('book_categories.txt', 'a') as file:
                        file.write(i3_underscored + '\n')
                else:
                    continue
        

if __name__ == '__main__':
    get_book_categories(base_url, categories_url)
