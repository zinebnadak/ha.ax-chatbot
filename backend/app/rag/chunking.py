import json 
from pathlib import Path 

def load_page(file_path: Path) -> dict:
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file) 


page_path = Path("/Users/zizo/ha.ax-chatbot/data/bibliotek/en/about-the-library.json")
print(load_page(page_path))
