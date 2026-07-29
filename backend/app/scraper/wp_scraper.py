'''
Each URL in urls.py:
   1. GET raw HTML (requests)
   2. Strip known non-content tags/sections (subtractive, not selector-based)
   3. Get remaining text
   4. Wrap in a record (url, section, lang, content, content_length, scraped_at)
   5. Save as /data/{section}/{slug}.json

https://www.ha.ax/wp-json/ , https://www.open.ax/wp-json/, https://bibliotek.ha.ax/wp-json/ - targeting the WP REST API in case needed

'''


import requests
import json
from pathlib import Path
from datetime import datetime, timezone
from bs4 import BeautifulSoup

def clean(soup):

    return clean_soup

def scraper(urls: dict, section: str, lang: str = "sv"):

    print(f"Scraped {name} from {url} to {file_path} ({len(text)} chars)")



    