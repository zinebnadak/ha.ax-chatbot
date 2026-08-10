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

def split_parent_text(text: str, max_words: int = 100) -> list[str]:
    words = text.split()
    children = []

    for start in range(0,len(words), max_words):
        child_words = words[start:start + max_words]
        children.append(" ".join(child_words))
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

first_parent = parents[0]
child_texts = split_parent_text(first_parent["text"])

for child_text in child_texts:
    print("CHILD:")
    print(child_text)
    print()

children = create_child_chunks(parents[0])
for child in children:
    print(child)