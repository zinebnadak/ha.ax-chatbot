import json 
from pathlib import Path 
import re

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

def split_parent_text(text: str, max_words: int = 100) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip()) # The pattern means: split at whitespace immediately after ., !, or ?
    children = []
    current = ""

    for sentence in sentences:
        possible_child = f"{current} {sentence}".strip()

        if current and len(possible_child.split()) > max_words: # A child needs to have full sentences that are in total less than 100 words.
            children.append(current)
            current = sentence
        else:
            current = possible_child

    if current:
        children.append(current)

    return children

def create_child_chunks(parent: dict) -> list[dict]:
    child_texts = split_parent_text(parent["text"])
    children = []

    for index, child_text in enumerate(child_texts):
        child = {
            "id": f"{parent['id']}_child-{index}",
            "parent_id": parent["id"],
            "text": child_text,
        }
        children.append(child)
        
    return children

def load_pages(data_folder: Path) -> list[dict]:
    pages = []

    for file_path in data_folder.rglob("*.json"):  #rglob() searches a folder and all folders inside it for files file paths ending with .json
        page = load_page(file_path)
        pages.append(page)

    return pages 

print(load_pages(Path("/Users/zizo/ha.ax-chatbot/data")))

'''
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


all_children = []

for parent in parents:
    children = create_child_chunks(parent)
    all_children.extend(children)

for child in all_children:
    print(child)
'''