import os
import json

# Paths
ARTICLES_DIR = 'articles'
JSON_PATH = 'index.json'

def update_index():
    # 1. Load existing JSON index if it exists, otherwise start fresh
    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            try:
                index_data = json.load(f)
            except json.JSONDecodeError:
                index_data = {}
    else:
        index_data = {}

    # 2. Scan articles folder
    if os.path.exists(ARTICLES_DIR):
        files = os.listdir(ARTICLES_DIR)
        for filename in files:
            if filename.endswith('.txt'):
                # Get article name without extension (e.g., 'test1')
                article_name = filename[:-4]
                with open("articles/"+filename) as file:
                    content = file.read().replace("\n", "<br>")
                # If it's not already in the index, add it
                if article_name not in index_data:
                    index_data[article_name] = content
                    print(f"Added new article to index: {article_name}")

    # 3. Save back to index.json
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=4)
    print("Index updated successfully!")

if __name__ == "__main__":
    update_index()