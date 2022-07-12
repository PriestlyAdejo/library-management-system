import requests as reqs
from bs4 import BeautifulSoup as bs
import numpy as np
import pandas as pd
import regex as rgx
import fitz
from PIL import Image, ImageQt
import matplotlib.pyplot as plt
import json
"""
All info is on one page, don't need to use recusrion to find all required
URLS as well as checking file and class names/structures for each page.
"""
# Getting Initial Soup
base_url = 'https://www.compare-school-performance.service.gov.uk'
placeholder_url = '/schools-by-type?for=primary&step=default&table=schools&region=all-england'
page_selector = '&page=1'
full_url = 'https://www.compare-school-performance.service.gov.uk/schools-by-type?for=ofsted&step=default&table=schools&region=all-england&orderby=OFSTEDLASTINSP&orderdir=asc'
html_raw = reqs.get(full_url)
soup = bs(html_raw.content)

# Checking if find works
header_and_table = soup.find_all('div', attrs={'id': 'table-sticky-header-container'})
header_and_table = header_and_table[0].find('table', attrs={'id': 'establishment-list-view'})
body = header_and_table.find('tbody') # First tbody contains the table body
body_trs = body.find_all('tr', attrs = {'data-row-id': 'SchoolsResultsRow'})


"""
Do this after finding out whether a link in the main table is an ofsted link or not.
By this, I mean everything below this comment. I don't need to worry about no data cols here
those should be handled in the scope of the for and if loops in the main code.
"""
# Getting Ofsted Link From main table and creating ofsted soup
th_and_tds1 = body_trs[1] # 2nd row 
th_and_tds = th_and_tds1.find_all(['th', 'td'])
ofsted_link = th_and_tds[-1].find('a')['href']

# Do after finding ofsted page link
ofsted_html_raw = reqs.get(ofsted_link)
ofsted_page_soup = bs(ofsted_html_raw.content)

# Getting Ofsted document and page details
# Fucntion to find latest full inspection date
def find_full(ofstd_tmln):
    """
    Finds the latest full inspection given we've already found the ol for the page
    containing the ofsted timeline of inspections
    """
    all_lis = ofstd_tmln.find_all('li', attrs={'class': 'timeline__day'})
    # Collecting the lis that have 'full inspection' text
    full_inspections = []
    for lis in all_lis:
        values = lis.find('div', attrs={'class': 'event'})
        a_tag = values.find('a')
        if a_tag is None:
            print('No link detected')
        else:
            inspection_type = a_tag.contents[0].strip()
            t = 'Full inspection'
            if t in inspection_type:
                full_inspections.append(lis)
            else:
                print(f"Skip inspection: {inspection_type}")
                pass
    # First value in the list will be the latest full inspection
    return full_inspections[0] if len(full_inspections) >= 1 else []

# Function to get the ofsted pdf file and download its text and image data
def get_pdf_data(report_link_pdf):
    """
    USING PYMUPDF --- REFERENCE THIS WHEN TRYNIG TO SHOW DATA IN JUPYTER!!!
    This function uses pymupdf to get text from the ofsted pdf files using OCR
    as well as extracting image objects for each page. These are not image data,
    but its just the object/location of the image in memory.
    """
    res = reqs.get(report_link_pdf)
    doc = fitz.open(stream=res.content, filetype="pdf")

    pages = 0
    page_text_data = [] # Per page
    page_pix_data = [] # New object per page
    next_page = True
    while next_page:
        try: # USING PYMUPDF --- REFERENCE THIS WHEN TRYNIG TO SHOW DATA IN JUPYTER
            page_data = doc.load_page(pages)
            page_pix_data.append(page_data.get_pixmap())
            page_text_data.append(page_data.get_text('text'))
            # Update pages
            pages += 1
        except Exception as e:
            next_page = False
            e = e
            print(f"Last PDF Page Reached!, Reason: {e}")
    return page_text_data, page_pix_data

# Init Vals   
ofsted_timelines = ofsted_page_soup.find('ol', attrs={'class': 'timeline'})
full_inspections = find_full(ofsted_timelines)
# I'm using arrays to save vals incase I want to get multiple vals in future
placeholder = None
save_inspect = {'latest_full_pdf': {'link': placeholder, 'content': {'text': placeholder, 'img_data': placeholder},\
                'inspection_type': placeholder, 'inspection_outcome': placeholder, 'published_date': placeholder, 'inspection_date': placeholder}}

if len(full_inspections) == 0:
    inspection_date = 'None'
    published_date = 'None'
    report_link_pdf = 'None'
    inspection_type = 'None'
    inspection_outcome = 'None'
else:
    latest = full_inspections
    values = latest.find('div', attrs={'class': 'event'})
    link_values = values.find('span', attrs={'class': 'event__title'})

    inspection_date = values.find('p', attrs={'class': 'timeline__date'}).select('time')[0].contents[0]
    published_date = link_values.find('a').contents[-1].contents[0].split("-")[1].strip() # Always last value of contents
    
    report_link_pdf = link_values.find('a')['href']
    inspection_type = link_values.find('a').contents[0].strip()[:-1] if ":" in\
                     link_values.find('a').contents[0].strip() else link_values.find('a').contents[0].strip()
    inspection_outcome = latest.find('a').contents[1].contents[0].strip()
# Saving to dictionary
save_inspect['latest_full_pdf']['link'] = report_link_pdf
save_inspect['latest_full_pdf']['content']['text'] = get_pdf_data(report_link_pdf)[0]
save_inspect['latest_full_pdf']['content']['img_data'] = get_pdf_data(report_link_pdf)[1]
save_inspect['latest_full_pdf']['inspection_type'] = inspection_type
save_inspect['latest_full_pdf']['inspection_outcome'] = inspection_outcome
save_inspect['latest_full_pdf']['published_date'] = published_date
save_inspect['latest_full_pdf']['inspection_date'] = inspection_date


path_to_file = r"C:\Users\pries\OneDrive\Documents\Coding Projects\Library Management System\Library Management System\Library Management System\enums\data_and_scrapings\scripts\school_gov_data_4.json"
with open(path_to_file) as f:
    d = json.load(f)
    [print(key) for key in d.keys()]
    ofsted_rts = d["OFSTED_RATINGS_"]
    print(ofsted_rts)
