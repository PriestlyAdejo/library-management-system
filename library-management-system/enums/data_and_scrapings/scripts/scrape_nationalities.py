import requests
from bs4 import BeautifulSoup
import os.path

"""
All info is on one page, don't need to use recusrion to find all required
URLS as well as checking file and class names/structures for each page.
"""
# Urls
url = 'www.gov.uk/government/publications/nationalities/list-of-nationalities'

def get_nationalities(url):
    """
    Gets a list of nationalities in alphabetic order and saves them to a list of
    in the 'data' folder as the script progresses. Will detect if the page itself 
    has changed and either give error, update file automatically (if it exists), or
    stop the script entirely.
    """

    # Creating Requests
    try: # If schema defined
        req = requests.get(url)
    except:
        try: # No SSL
            req = requests.get('http://' + url)
        except: # SSL
            req = requests.get('https://' + url)

    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    mydivs = soup.find_all("div", {"class": "govspeak"}) # Finds class containing all the tables
    nationalities = mydivs[0].find_all("td")

    # Final Nationalities Print
    # [print(nationalities[i].text.strip().replace("\xa0", "")) for i in range(len(nationalities))]

    # Final Nationalities Array
    full_list = [nationalities[i].text.strip().replace("\xa0", "") for i in range(len(nationalities))]
    full_list = [nationality for nationality in full_list if nationality != '']
    # print(full_list)

    # Converting each val to enum form
    full_list = [val.upper().replace(" ", "_").replace("(", "").replace(")", "") for val in full_list]
    print(full_list)
    
    # Saving nationalities to data 
    # Use config in future to save to data directory
    with open('nationalities.txt', mode='w', encoding='utf-8') as nationality_file:
        [nationality_file.write(full_list[i] + '\n') for i in range(0, len(full_list))]
    
get_nationalities(url)