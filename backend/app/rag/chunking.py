import json 
from pathlib import Path 

def load_page(file_path: Path) -> dict:
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file) 

def split_into_sections(text: str) -> list[str]:
    sections = text.split("## ")
    return sections


# Testing
page_path = Path("/Users/zizo/ha.ax-chatbot/data/bibliotek/en/about-the-library.json")
page = load_page(page_path)

title = page["title"]
text = page["text"]
sections = split_into_sections(text)
for section in sections:
    print("SECTION:")
    print(section)
    print()