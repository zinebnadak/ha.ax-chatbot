import json 
from pathlib import Path 
import re

def load_page(file_path: Path) -> dict:
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file) 

def split_into_sections(text: str) -> list[str]:
    sections = re.split(r"(?m)^#{1,6}\s+", text) # beginning of a line, between 1 and 6 # symbols and one or more spaces

    cleaned_sections = [
        section.strip()
        for section in sections
        if section.strip()
    ]

    return [
        section
        for section in cleaned_sections
        if len(section.split()) >= 5
    ]

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
    sentences = re.split(r"(?<=[.!?])\s+|\n+", text.strip()) # The pattern means:split after ./!/? followed by whitespace, or on any run of newlines / line-broken text 
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

def chunk_all_pages(pages: list[dict]) -> tuple[list[dict], list[dict]]:
    all_parents = []
    all_children = []

    for page in pages:
        sections = split_into_sections(page["text"])
        parents = create_parent_chunks(sections, page)

        all_parents.extend(parents)

        for parent in parents: 
            children = create_child_chunks(parent)
            all_children.extend(children)
        
    return all_parents, all_children




# Count prints 
data_folder = Path("data")
pages = load_pages(data_folder)

parents, children = chunk_all_pages(pages)
print(parents)
print(children)

print(f"Pages: {len(pages)}")
print(f"Parents: {len(parents)}")
print(f"Children: {len(children)}")

print(pages)
