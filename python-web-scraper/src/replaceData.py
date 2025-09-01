import json

# Load the files
with open('maimaiJsonFile.json', encoding='utf-8') as f:
    maimai_json = json.load(f)

with open('maimaiModifiedInfo.json', encoding='utf-8') as f:
    modified_info = json.load(f)

# Build a lookup for modified info by title
mod_lookup = {entry['title']: entry for entry in modified_info}

STD_FIELDS = ['lev_bas', 'lev_adv', 'lev_exp', 'lev_mas', 'lev_remas']
DX_FIELDS  = ['dx_lev_bas', 'dx_lev_adv', 'dx_lev_exp', 'dx_lev_mas', 'dx_lev_remas']

for song in maimai_json:
    title = song.get('title')
    if title in mod_lookup:
        mod = mod_lookup[title]
        # Add/replace version
        song['version'] = mod['version']

        # STD difficulties
        if 'STD' in mod:
            for i, field in enumerate(STD_FIELDS):
                if i < len(mod['STD']):
                    song[field] = mod['STD'][i]
                elif field in song:
                    song.pop(field)
            for i in range(len(mod['STD']), len(STD_FIELDS)):
                field = STD_FIELDS[i]
                if field in song:
                    song.pop(field)
        else:
            for field in STD_FIELDS:
                if field in song:
                    song.pop(field)

        # DX difficulties
        if 'DX' in mod:
            for i, field in enumerate(DX_FIELDS):
                if i < len(mod['DX']):
                    song[field] = mod['DX'][i]
                elif field in song:
                    song.pop(field)
            for i in range(len(mod['DX']), len(DX_FIELDS)):
                field = DX_FIELDS[i]
                if field in song:
                    song.pop(field)
        else:
            for field in DX_FIELDS:
                if field in song:
                    song.pop(field)

    # Prepend to image_url if present
    if 'image_url' in song and not song['image_url'].startswith('https://maimaidx-eng.com/maimai-mobile/img/Music/'):
        song['image_url'] = 'https://maimaidx-eng.com/maimai-mobile/img/Music/' + song['image_url']

# Save the updated file
with open('maimaiJsonFile.json', 'w', encoding='utf-8') as f:
    json.dump(maimai_json, f, ensure_ascii=False, indent=2)