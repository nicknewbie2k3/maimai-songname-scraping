import json
import os

# File paths
database_path = os.path.join(os.path.dirname(__file__), '..', 'maimai-songDatabase.json')
target_path = os.path.join(os.path.dirname(__file__), 'maimaiOneTypeDatabase.json')
output_path = os.path.join(os.path.dirname(__file__), 'maimaiOneTypeDatabase_replaced.json')

# 1. Load song database for image mappings only
with open(database_path, encoding='utf-8') as f:
    db = json.load(f)
db_songs = db['songs']

# Build image name mapping from database
title_to_image_name = {}
for song in db_songs:
    title = song.get('title')
    image_name = song.get('imageName')
    if title and image_name:
        title_to_image_name[title] = image_name

# 2. Load input file (source of truth for most data)
with open(target_path, encoding='utf-8') as f:
    target = json.load(f)

# 3. Load existing output file to preserve alias modifications (if exists)
existing_aliases = {}
if os.path.exists(output_path):
    with open(output_path, encoding='utf-8') as f:
        existing_output = json.load(f)
    
    # Build mapping of preserved aliases by title
    for song in existing_output:
        title = song.get('title')
        alias = song.get('alias')
        if title and alias:
            existing_aliases[title] = alias
    print(f"Found existing output file - preserving {len(existing_aliases)} songs with custom aliases")
else:
    print(f"No existing output file found - using input file aliases")

# 4. Process songs: update image URLs from input, preserve aliases from output
image_changed = 0
maimaidx_converted = 0
aliases_preserved = 0

for song in target:
    title = song.get('title')
    if not title:
        continue
        
    # Preserve aliases from existing output file if available
    if title in existing_aliases:
        song['alias'] = existing_aliases[title]
        aliases_preserved += 1
        
    current_image_url = song.get('image_url', '')
    
    # Priority 1: Update from database mapping (if available)
    if title in title_to_image_name:
        new_url = f"https://dp4p6x0xfi5o9.cloudfront.net/maimai/img/cover/{title_to_image_name[title]}"
        song['image_url'] = new_url
        image_changed += 1
    # Priority 2: Convert existing maimaidx URLs to CloudFront as fallback
    elif 'maimaidx' in current_image_url and 'img/Music/' in current_image_url:
        filename = current_image_url.split('img/Music/')[-1]
        if filename:
            song['image_url'] = f"https://dp4p6x0xfi5o9.cloudfront.net/maimai/img/cover/{filename}"
            image_changed += 1
            maimaidx_converted += 1

# 5. Save output
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(target, f, ensure_ascii=False, indent=2)

# 6. Report results
print(f"Image URL replacement completed with alias preservation.")
print(f"")
print(f"Results:")
print(f"  - {image_changed - maimaidx_converted} URLs updated from database mapping")
print(f"  - {maimaidx_converted} maimaidx URLs converted to CloudFront") 
print(f"  - {image_changed} total image URLs updated")
print(f"  - {aliases_preserved} custom aliases preserved from existing output file")
print(f"")
print(f"Input: {target_path}")
print(f"Output: {output_path}")
print(f"Strategy: Image URLs from input + preserved aliases from output")