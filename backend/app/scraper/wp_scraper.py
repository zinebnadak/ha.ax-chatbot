import requests
import json
from pathlib import Path
from datetime import datetime, timezone
from bs4 import BeautifulSoup


def clean(soup):
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    for tag in soup.select('[class*="sbi"]'):
        tag.decompose()
    return soup


def scraper(urls: dict, section: str, lang: str = "sv"):
    for url in urls[section][lang]:
        try:
            data = requests.get(url, timeout=15)
            data.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to scrape {url}: {e}")
            continue

        soup = BeautifulSoup(data.text, "html.parser")
        cleaned_soup = clean(soup)
        title = soup.title.text
        text = cleaned_soup.get_text(separator="\n", strip=True)
        url_label = url.rstrip("/").split("/")[-1]
        
        metadata_record = {
            "url": url,
            "section": section,
            "lang": lang,
            "scraped_at": datetime.now().isoformat(),
            "title": title,
            "text": text,
        }

        directory = Path(f"data/{section}/{lang}")
        directory.mkdir(parents=True, exist_ok=True)
        file_name = directory / f"{url_label}.json"

        with open (file_name, "w", encoding="utf-8") as f:
                json.dump(metadata_record, f, ensure_ascii=False, indent=2)
        print(f"Scraped {url} from {section}/{lang} to {file_name} - Text is {len(text)} chars.")


'''
https://www.ha.ax/wp-json/ , https://www.open.ax/wp-json/, https://bibliotek.ha.ax/wp-json/ - targeting the WP REST API in case needed
'''