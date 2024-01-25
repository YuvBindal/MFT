"""
Strategy to Develop Web Scraping Bot:
1. Make a google search with company name
2. Filter the google searches using a vocabulary list of popular social media providers
3. If found, open the link and then extract the respective information (for now just handles)
4. If none found in the first 2 pages (limited to 2 pages to avoid lag) then move to the next
5. Collate recent 3 posts from these websites and collate them into a seperate column
6. Scrape latest activity from the social media websites.
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
import os

start_time = time.time()
api_key = os.getenv("GOOGLE_CLOUD_API")


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

def get_first_link(organisation_name):
    html_content = google_search(organisation_name)
    if html_content:
        extracted_data = extract_headings_and_links(html_content)
        home_page = extracted_data[0]
        return home_page['url']
    return ''

def extract_textual_content_from_link(link):
    # Send an HTTP request to the URL
    response = requests.get(link)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all text from the page
        text = soup.get_text()
        text = soup.get_text().replace('\n', ' ')


        return text
    else:
        # Print an error message if the request was not successful
        print(f"Error: Unable to fetch the content from {link}. Status code: {response.status_code}")
        return None


def main():
    #MAKE A DATAPIPELINE THAT READS THE CSV COLUMNS AND ITERATIVELY SEARCHES
    countries = ['Malaysia','Indonesia','Cambodia','Brunei'] #COUNTRIES LEFT TO SEARCH 


    #Applies the social media scraper to each datafile
    for country in countries:
        file_path = f"./EnvNP_{country}.xlsx"
        print(file_path)
        print(pd.read_excel(file_path).columns)
        dataset = pd.read_excel(file_path)
        dataset['Social Medias'] = dataset['Name of organisation'].apply(get_social_media_urls)
        dataset.to_excel(file_path, index=False)
        print(dataset)

    #Extraction of Mission and other insights from company websites
    
    #Go to home page link, extract all textual content, feed it into a LLM, let the LLM extract the mission and description of what the company does.
    #Next step after the LLM generation is to make RAG system and feedback function to improve retreival quality

    #testing right now with just the SG data
    # dataset = pd.read_excel("./EnvNP_SG.xlsx")
    #dataset['Organisation_Link'] = dataset['Name of organisation'].apply(get_first_link)
   # print(dataset)

    #after generating links, extract textual content from it
   #dataset['Mission_Description'] = dataset['Organisation_Link'].apply()
    print(api_key)

    text = extract_textual_content_from_link('https://www.nss.org.sg/index.aspx')
    print(text) #works




    



        
        

if __name__ == "__main__":
    main()