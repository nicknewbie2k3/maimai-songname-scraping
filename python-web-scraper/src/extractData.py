import json
import os
import re

input_path = os.path.join(os.path.dirname(__file__), 'maimaiFullInfo.json')
output_path = os.path.join(os.path.dirname(__file__), 'maimaiExtractedInfo.json')

def extract_alias_from_description(description):
    """
    Extract alias information from description field.
    Looks for content within the first parentheses, typically after '-#' marker.
    
    Example input: "xi\n\n-# (Xaleid◆scopiX / xaleidscopix)\n\n**Category:** maimai..."
    Example output: "Xaleid◆scopiX / xaleidscopix"
    """
    if not description:
        return None
    
    # Pattern to find content within parentheses
    pattern = r'\(([^\)]+)\)'
    matches = re.findall(pattern, description)
    
    for match in matches:
        alias_content = match.strip()
        
        # Filter out common non-alias patterns (numbers, difficulty levels, etc.)
        if (len(alias_content) > 2 and 
            not alias_content.isdigit() and
            not re.match(r'^\d+\.\d+$', alias_content) and  # Skip decimal numbers like (7.9)
            not re.match(r'^\d+\+?$', alias_content)):      # Skip level numbers like (11) or (13+)
            
            return alias_content
    
    return None

def extract_info():
    with open(input_path, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    extracted = []
    aliases_found = 0

    # FIX: Iterate over the messages list
    for song in data.get("messages", []):
        embeds = song.get('embeds', [])
        for embed in embeds:
            entry = {
                "title": embed.get("title", ""),
                "description": embed.get("description", "")
            }
            
            # Extract alias from description if present
            description = embed.get("description", "")
            if description:
                alias = extract_alias_from_description(description)
                if alias:
                    entry["alias"] = alias
                    aliases_found += 1
                    print(f"Extracted alias for '{entry['title']}': {alias}")
            
            extracted.append(entry)

    print(f"\nTotal songs processed: {len(extracted)}")
    print(f"Total aliases extracted: {aliases_found}")

    with open(output_path, 'w', encoding='utf-8') as outfile:
        json.dump(extracted, outfile, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    extract_info()