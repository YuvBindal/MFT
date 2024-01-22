"""
Strategy to Develop Web Scraping Bot:
1. Make a google search with company name
2. Filter the google searches using a vocabulary list of popular social media providers
3. If found, open the link and then extract the respective information (for now just handles)
4. If none found in the first 2 pages (limited to 2 pages to avoid lag) then move to the next
"""

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import csv
import os
import time
from getpass import getpass
import requests
from pprint import pprint

start_time = time.time()

social_media_sites = [
    "https://www.facebook.com/",
    "https://twitter.com/",
    "https://www.instagram.com/",
    "https://www.linkedin.com/",
    "https://www.pinterest.com/",
    "https://www.snapchat.com/",
    "https://www.tiktok.com/",
    "https://www.reddit.com/",
    "https://www.youtube.com/",
    "https://www.whatsapp.com/",
    "https://www.tumblr.com/",
    "https://www.flickr.com/",
    "https://www.quora.com/",
    "https://medium.com/",
    "https://discord.com/",
    "https://telegram.org/",
    "https://www.viber.com/",
    "https://www.wechat.com/",
    "https://line.me/",
    "https://vk.com/",
    'https://sg.linkedin.com/company/'
]



# MAKING A GOOGLE QUERY AND EXTRACTING HEADINGS
def google_search(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve search results. Status code: {response.status_code}")
        return None
    
def extract_headings_and_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    
    results = []
    for heading in headings:
        heading_text = heading.text.strip()
        link = heading.find_parent('a')
        if link:
            url = link.get('href')
            results.append({'heading': heading_text, 'url': url})

    return results

################################################################################################################

def filter_social_media(searched_data):
    filtered_sites = []
    for entry in searched_data:
        if (not entry['url']):
            continue
        

        for social_handles in social_media_sites:
            if social_handles in entry['url']:
                #successfully found a site O(n^2)
                filtered_sites.append(entry)
    
    return filtered_sites


def get_social_media_urls(organization_name):
    # This function should perform the necessary steps to get social media URLs for a given organization name
    # You can use your existing functions like google_search and extract_headings_and_links here
    # Make sure to return the list of social media URLs
    html_content = google_search(organization_name)
    if html_content:
        extracted_data = extract_headings_and_links(html_content)
        social_handles = filter_social_media(extracted_data)
        return [entry['url'] for entry in social_handles]
    return []


def main():
    #MAKE A DATAPIPELINE THAT READS THE CSV COLUMNS AND ITERATIVELY SEARCHES

    dataset = pd.read_excel('/Users/yuvvvvv/MFT/Environmental Non-profits in South-east Asia.xlsx')
    pprint(dataset.columns)

    dataset['Social Medias'] = dataset['Name of organisation'].apply(get_social_media_urls)
    print(dataset)


    



        
        

if __name__ == "__main__":
    main()