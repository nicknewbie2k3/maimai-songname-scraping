import json

def get_internal_level(sheets, typ, diff):
    for sheet in sheets:
        if sheet.get('type') == typ and sheet.get('difficulty') == diff:
            val = sheet.get('internalLevelValue')
            if val is not None:
                return str(val)
    return ""

def build_image_url(image_name):
    if not image_name:
        return ""
    return f"https://dp4p6x0xfi5o9.cloudfront.net/maimai/img/cover/{image_name}"

# Load the files
with open('../maimai-songDatabase.json', encoding='utf-8') as f:
    db = json.load(f)
with open('maimaiJsonFile.json', encoding='utf-8') as f:
    user = json.load(f)

db_songs = db['songs']

# Create a title-to-index mapping for existing songs
user_title_map = {}
for i, song in enumerate(user):
    title = song.get('title')
    if title:
        user_title_map[title] = i

# Mapping for difficulties
diffs = ['basic', 'advanced', 'expert', 'master', 'remaster']

added_count = 0
updated_count = 0

for song in db_songs:
    title = song.get('title')
    if not title:
        continue

    sheets = song.get('sheets', [])
    
    # Build song data from database
    song_data = {
        "artist": song.get("artist", ""),
        "catcode": song.get("category", ""),
        "dx_lev_bas": get_internal_level(sheets, "dx", "basic"),
        "dx_lev_adv": get_internal_level(sheets, "dx", "advanced"),
        "dx_lev_exp": get_internal_level(sheets, "dx", "expert"),
        "dx_lev_mas": get_internal_level(sheets, "dx", "master"),
        "dx_lev_remas": get_internal_level(sheets, "dx", "remaster"),
        "image_url": build_image_url(song.get("imageName")),
        "release": "000000",
        "lev_bas": get_internal_level(sheets, "std", "basic"),
        "lev_adv": get_internal_level(sheets, "std", "advanced"),
        "lev_exp": get_internal_level(sheets, "std", "expert"),
        "lev_mas": get_internal_level(sheets, "std", "master"),
        "lev_remas": get_internal_level(sheets, "std", "remaster"),
        "sort": "",
        "title": song.get("title", ""),
        "title_kana": "",
        "version": song.get("version", "")
    }
    
    if title in user_title_map:
        # Update existing song with missing fields
        user_index = user_title_map[title]
        existing_song = user[user_index]
        
        # Update fields that are empty or missing
        updated = False
        for key, value in song_data.items():
            if key in ['title']:  # Don't overwrite title
                continue
            if not existing_song.get(key) and value:  # Only update if existing is empty and new has value
                existing_song[key] = value
                updated = True
        
        if updated:
            updated_count += 1
    else:
        # Add completely new song
        user.append(song_data)
        added_count += 1

with open('maimaiJsonFile.json', 'w', encoding='utf-8') as f:
    json.dump(user, f, ensure_ascii=False, indent=2)

print(f"Added {added_count} new songs.")
print(f"Updated {updated_count} existing songs with missing data.")
print(f"Total changes: {added_count + updated_count}")