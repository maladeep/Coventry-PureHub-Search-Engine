#import os  # Module for interacting with the operating system
import time  # Module for time-related operations
import ujson  # Module for working with JSON data
from random import randint  # Module for generating random numbers
from typing import Dict, List, Any  # Type hinting imports

import requests  # Library for making HTTP requests
from bs4 import BeautifulSoup  # Library for parsing HTML data
from selenium import webdriver  # Library for browser automation
from selenium.common.exceptions import NoSuchElementException  # Exception for missing elements
from webdriver_manager.chrome import ChromeDriverManager  # Driver manager for Chrome (We are using Chromium based )



# Delete files if present
# try:
#     os.remove('Authors_URL.txt')
#     os.remove('scraper_results.json')
# except OSError:
#     pass

def write_authors(list1, file_name):
     # Function to write authors' URLs to a file
    with open(file_name, 'w', encoding='utf-8') as f:
        for i in range(0, len(list1)):
            f.write(list1[i] + '\n')


def initCrawlerScraper(seed,max_profiles=500):
    # Initialize driver for Chrome
    webOpt = webdriver.ChromeOptions()
    webOpt.add_experimental_option('excludeSwitches', ['enable-logging'])
    webOpt.add_argument('--ignore-certificate-errors')
    webOpt.add_argument('--incognito')
    webOpt.headless = True
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=webOpt)
    driver.get(seed)  # Start with the original link

    Links = []  # Array with pureportal profiles URL
    pub_data = []  # To store publication information for each pureportal profile

    nextLink = driver.find_element_by_css_selector(".nextLink").is_enabled()  # Check if the next page link is enabled
    print("Crawler has begun...")
    while (nextLink):
        page = driver.page_source
        # XML parser to parse each URL
        bs = BeautifulSoup(page, "lxml")  # Parse the page source using BeautifulSoup

        # Extracting exact URL by spliting string into list
        for link in bs.findAll('a', class_='link person'):
            url = str(link)[str(link).find('https://pureportal.coventry.ac.uk/en/persons/'):].split('"')
            Links.append(url[0])
            
        # Click on Next button to visit next page
        try:
            if driver.find_element_by_css_selector(".nextLink"):
                element = driver.find_element_by_css_selector(".nextLink")
                driver.execute_script("arguments[0].click();", element)
            else:
                nextLink = False
        except NoSuchElementException:
            break
            
        # Check if the maximum number of profiles is reached
        if len(Links) >= max_profiles:
            break
            
    print("Crawler has found ", len(Links), " pureportal profiles")
    write_authors(Links, 'Authors_URL.txt') # Write the authors' URLs to a file

    print("Scraping publication data for ", len(Links), " pureportal profiles...")
    count = 0
    for link in Links:
        # Visit each link to get data
        time.sleep(1)  # Delay of 1 second to hit next data
        driver.get(link)
        try:
            if driver.find_elements_by_css_selector(".portal_link.btn-primary.btn-large"):
                element = driver.find_elements_by_css_selector(".portal_link.btn-primary.btn-large")
                for a in element:
                    if "research output".lower() in a.text.lower():
                        driver.execute_script("arguments[0].click();", a)
                        driver.get(driver.current_url)
                        # Get name of Author
                        name = driver.find_element_by_css_selector("div[class='header person-details']>h1")
                        r = requests.get(driver.current_url)
                        # Parse all the data via BeautifulSoup
                        soup = BeautifulSoup(r.content, 'lxml')

                        # Extracting publication name, publication url, date and CU Authors
                        table = soup.find('ul', attrs={'class': 'list-results'})
                        if table != None:
                            for row in table.findAll('div', attrs={'class': 'result-container'}):
                                data = {}
                                data['name'] = row.h3.a.text
                                data['pub_url'] = row.h3.a['href']
                                date = row.find("span", class_="date")

                                rowitem = row.find_all(['div'])
                                span = row.find_all(['span'])
                                data['cu_author'] = name.text
                                data['date'] = date.text
                                print("Publication Name :", row.h3.a.text)
                                print("Publication URL :", row.h3.a['href'])
                                print("CU Author :", name.text)
                                print("Date :", date.text)
                                print("\n")
                                pub_data.append(data)
            else:
                # Get name of Author
                name = driver.find_element_by_css_selector("div[class='header person-details']>h1")
                r = requests.get(link)
                # Parse all the data via BeautifulSoup
                soup = BeautifulSoup(r.content, 'lxml')
                # Extracting publication name, publication url, date and CU Authors
                table = soup.find('div', attrs={'class': 'relation-list relation-list-publications'})
                if table != None:
                    for row in table.findAll('div', attrs={'class': 'result-container'}):
                        data = {}
                        data["name"] = row.h3.a.text
                        data['pub_url'] = row.h3.a['href']
                        date = row.find("span", class_="date")
                        rowitem = row.find_all(['div'])
                        span = row.find_all(['span'])
                        data['cu_author'] = name.text
                        data['date'] = date.text
                        print("Publication Name :", row.h3.a.text)
                        print("Publication URL :", row.h3.a['href'])
                        print("CU Author :", name.text)
                        print("Date :", date.text)
                        print("\n")
                        pub_data.append(data)
        except Exception:
            continue

    print("Crawler has scrapped data for ", len(pub_data), " pureportal publications")
    driver.quit()
    # Writing all the scraped results in a file with JSON format
    with open('scraper_results.json', 'w') as f:
        ujson.dump(pub_data, f)


initCrawlerScraper('https://pureportal.coventry.ac.uk/en/organisations/coventry-university/persons/', max_profiles=500)



