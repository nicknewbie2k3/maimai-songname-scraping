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
    return f"https://maimaidx-eng.com/maimai-mobile/img/Music/{image_name}"

# Load the files
with open('../maimai-songDatabase.json', encoding='utf-8') as f:
    db = json.load(f)
with open('maimaiJsonFile.json', encoding='utf-8') as f:
    user = json.load(f)

db_songs = db['songs']
user_titles = set(song.get('title') for song in user if 'title' in song)

# Mapping for difficulties
diffs = ['basic', 'advanced', 'expert', 'master', 'remaster']

added_count = 0

for song in db_songs:
    title = song.get('title')
    if not title or title in user_titles:
        continue

    sheets = song.get('sheets', [])
    # Build new song entry in the format of maimaiJsonFile.json
    new_song = {
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
    user.append(new_song)
    added_count += 1

with open('maimaiJsonFile.json', 'w', encoding='utf-8') as f:
    json.dump(user, f, ensure_ascii=False, indent=2)

print(f"Added {added_count} missing songs.")