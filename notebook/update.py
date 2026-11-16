import glob
import json
import os
import random
INBOX_PATTERN = "notebook/*.txt"
JSON_FILENAME = "notebook/notebook_data.json"

def process_notebook_inbox():
    # Find all .txt files inside the dedicated inbox folder
    txt_files = sorted(glob.glob(INBOX_PATTERN))

    if not txt_files:
        print("No new .txt files found in notebook/inbox/. Nothing to update.")
        return

    # Load existing JSON dictionary if it exists
    if os.path.exists(JSON_FILENAME):
        with open(JSON_FILENAME, "r", encoding="utf-8") as f:
            notebook = json.load(f)
    else:
        notebook = {}

    # Determine the starting page number for new entries
    existing_keys = [int(k) for k in notebook.keys()] if notebook else [0]
    next_page_num = max(existing_keys) + 1

    # Process every discovered .txt file
    for txt_path in txt_files:
        print(f"Processing {txt_path}...")
        with open(txt_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        # Split pages using '---PAGE---' delimiter
        pages = raw_text.split("---PAGE---")
        for page_content in pages:
            # Preserve intentional HTML tags/comments for theory-crafters while formatting newlines
            content = page_content.split("\n")
            con = []
            for line in content:
                font_size = random.uniform(10.5, 12)
                left_offset = random.uniform(7, 19)
                tilt = random.uniform(-0.9, 0.5)
                spacing = random.uniform(-3, 2)

                style = (
                    f"font-size: {font_size}px; "
                    f"margin-left: {left_offset}px; "
                    f"margin-bottom: {spacing}px; "
                    f"transform: rotate({tilt}deg);"
                )
                con.append(f'<div style="{style}">{line}</div>\n')
            content = "<br>".join(con)
            cleaned_content = content.strip()
            notebook[str(next_page_num)] = cleaned_content
            next_page_num += 1

        # Delete the processed .txt file once extracted
        os.remove(txt_path)
        print(f"Deleted processed file: {txt_path}")

    # Save updated dictionary back to JSON
    with open(JSON_FILENAME, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=4, ensure_ascii=False)

    print(f"Successfully updated {JSON_FILENAME}!")

if __name__ == "__main__":
    process_notebook_inbox()