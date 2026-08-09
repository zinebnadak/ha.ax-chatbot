import json 
from pathlib import Path 

def load_page(file_path: Path) -> dict:
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file) 

def split_into_sections(text: str) -> list[str]:
    sections = text.split("## ")
    return sections

def create_parent_chunks(sections: list[str], page: dict) -> list[dict]:
    parents = [] # a list of dicts

    for index, section in enumerate(sections):
        parent = {
            "id": f"{page['url']}_parent-{index}",
            "text": section.strip(),
            "title": page["title"],
            "url": page["url"],
            "lang": page["lang"],
        }
        parents.append(parent)
    
    return parents

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

parents = create_parent_chunks(sections, page)
for parent in parents:
    print(parent)
    print()