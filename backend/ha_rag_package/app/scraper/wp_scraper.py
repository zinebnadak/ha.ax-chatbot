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
    
def extract_headings(soup):
    parts = []
    seen = set()
    tags = ["h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "a"]
    for heading in soup.find_all(tags):
        if heading.name in ("p", "li") and heading.find_parent(["p", "li"]):
            continue
        if heading.name == "a" and heading.find_parent(["h1", "h2", "h3", "h4", "h5", "h6", "p", "li"]):
            continue
        text = heading.get_text(separator=" ", strip=True)
        if not text:
            continue
        is_heading = heading.name.startswith("h")
        if not is_heading:
            if text in seen:
                continue
            seen.add(text)
        if is_heading:
            level = int(heading.name[1])
            parts.append(f"\n\n{'#' * level} {text}\n")
        else:
            parts.append(text)
    return "\n".join(parts)

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
        text = extract_headings(cleaned_soup)
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