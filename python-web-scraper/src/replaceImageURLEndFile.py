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

# Helper function to get imageName for a title, trying with and without chart type tags
def get_image_name(title):
    # Try exact match first
    if title in title_to_image:
        return title_to_image[title]
    
    # Try without [STD] or [DX] tags
    import re
    base_title = re.sub(r'\s*\[(STD|DX)\]\s*$', '', title)
    if base_title != title and base_title in title_to_image:
        return title_to_image[base_title]
    
    return None

# 2. Load target file
with open(target_path, encoding='utf-8') as f:
    target = json.load(f)

# 3. Replace image_url in target (assuming field is 'image_url' and match by 'title')
# Ensure we completely replace the image_url, not append to existing malformed URLs
changed = 0
malformed_fixed = 0
extracted_fixed = 0

for song in target:
    title = song.get('title')
    old_url = song.get('image_url', '')
    
    # Try to get imageName using helper function (handles [STD]/[DX] tags)
    image_name = get_image_name(title)
    
    # Priority 1: Use database match if available
    if image_name:
        new_url = f"https://dp4p6x0xfi5o9.cloudfront.net/maimai/img/cover/{image_name}"
        song['image_url'] = new_url
        changed += 1
        
        # Count malformed URLs that were fixed
        if old_url and 'https://' in old_url[8:]:
            malformed_fixed += 1
    
    # Priority 2: Extract CloudFront URL from malformed URLs even without database match
    elif old_url and 'https://dp4p6x0xfi5o9.cloudfront.net/maimai/img/cover/' in old_url:
        # Extract the CloudFront URL from the malformed URL
        cloudfront_start = old_url.find('https://dp4p6x0xfi5o9.cloudfront.net/maimai/img/cover/')
        if cloudfront_start != -1:
            clean_url = old_url[cloudfront_start:]
            if clean_url != old_url:  # Only update if it was actually malformed
                song['image_url'] = clean_url
                changed += 1
                extracted_fixed += 1

# 4. Save output
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(target, f, ensure_ascii=False, indent=2)

print(f"Done. {changed} image URLs replaced ({malformed_fixed} from database matches, {extracted_fixed} extracted from malformed URLs). Output: {output_path}")