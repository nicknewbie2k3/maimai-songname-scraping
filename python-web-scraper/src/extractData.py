import json
import os

input_path = os.path.join(os.path.dirname(__file__), 'maimaiFullInfo.json')
output_path = os.path.join(os.path.dirname(__file__), 'maimaiExtractedInfo.json')

def extract_info():
    with open(input_path, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    extracted = []

    # FIX: Iterate over the messages list
    for song in data.get("messages", []):
        embeds = song.get('embeds', [])
        for embed in embeds:
            entry = {
                "title": embed.get("title", ""),
                "description": embed.get("description", "")
            }
            extracted.append(entry)

    with open(output_path, 'w', encoding='utf-8') as outfile:
        json.dump(extracted, outfile, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    extract_info()