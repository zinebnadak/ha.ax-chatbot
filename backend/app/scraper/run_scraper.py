from urls import URLS
from wp_scraper import scraper

def scrape_all(urls: dict):
    for section, langs in urls.items():
        for lang in langs:
            print(f"\n=== Scraping section '{section}' & lang '{lang}' ===")
            scraper(urls, section, lang)

if __name__ == "__main__":
    scrape_all(URLS)
