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

