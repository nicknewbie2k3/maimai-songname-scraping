import json
import os
import re

input_path = os.path.join(os.path.dirname(__file__), 'maimaiExtractedInfo.json')
output_path = os.path.join(os.path.dirname(__file__), 'maimaiModifiedInfo.json')

def extract_title(item):
    # Try to get title from field, else from description's first line
    if item.get('title'):
        return item['title']
    desc = item.get('description', '')
    first_line = desc.split('\n', 1)[0].strip()
    return first_line

def extract_version(desc):
    # Example: **Version:** ORANGE PLUS
    m = re.search(r"\*\*Version:\*\*\s*([^\n]+)", desc)
    return m.group(1).strip() if m else ""

def extract_difficulties(desc, diff_type):
    # Find the line that starts with **STD:** or **DX:**
    lines = desc.split('\n')
    for line in lines:
        if line.strip().startswith(f"**{diff_type}:**"):
            # Extract all numbers inside parentheses (e.g., (4.0))
            return re.findall(r"\(([\d\.]+)\)", line)
    return None

def main():
    with open(input_path, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    result = []
    for item in data:
        desc = item.get('description', '')
        title = extract_title(item)
        version = extract_version(desc)
        std = extract_difficulties(desc, "STD")
        dx = extract_difficulties(desc, "DX")
        entry = {"title": title, "version": version}
        
        # Add alias if it exists
        if item.get('alias'):
            entry["alias"] = item['alias']
            
        if std:
            entry["STD"] = std
        if dx:
            entry["DX"] = dx
        result.append(entry)

    with open(output_path, 'w', encoding='utf-8') as outfile:
        json.dump(result, outfile, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()