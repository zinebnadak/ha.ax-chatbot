from urls import URLS
from wp_scraper import scraper

# loop that calls scraper() once per (section, lang) pair in URLSs 

scraper(URLS, "home")