import json
import os

# File paths (update if needed)
database_path = os.path.join(os.path.dirname(__file__), '..', 'maimai-songDatabase.json')
target_path = os.path.join(os.path.dirname(__file__), 'mar2026update.json')
output_path = os.path.join(os.path.dirname(__file__), 'mar2026update_replaced.json')

# 1. Load song database
with open(database_path, encoding='utf-8') as f:
    db = json.load(f)
db_songs = db['songs']

# Build a mapping from title to imageName
title_to_image = {song.get('title'): song.get('imageName') for song in db_songs if song.get('title') and song.get('imageName')}

# 2. Load target file
with open(target_path, encoding='utf-8') as f:
    target = json.load(f)

# 3. Replace image_url in target (assuming field is 'image_url' and match by 'title')
changed = 0
for song in target:
    title = song.get('title')
    if title in title_to_image:
        song['image_url'] = f"https://dp4p6x0xfi5o9.cloudfront.net/maimai/img/cover/{title_to_image[title]}"
        changed += 1

# 4. Save output
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(target, f, ensure_ascii=False, indent=2)

print(f"Done. {changed} image URLs replaced. Output: {output_path}")