import json
import os

input_path = os.path.join(os.path.dirname(__file__), 'maimaiJsonFile.json')
output_path = os.path.join(os.path.dirname(__file__), 'maimaiDatabase.json')

STD_FIELDS = ['lev_bas', 'lev_adv', 'lev_exp', 'lev_mas', 'lev_remas']
DX_FIELDS  = ['dx_lev_bas', 'dx_lev_adv', 'dx_lev_exp', 'dx_lev_mas', 'dx_lev_remas']

def has_fields(song, fields):
    return any(song.get(f) is not None for f in fields)

def copy_fields(song, fields):
    return {f: song[f] for f in fields if f in song}

with open(input_path, 'r', encoding='utf-8') as f:
    songs = json.load(f)

result = []

for song in songs:
    std_exists = has_fields(song, STD_FIELDS)
    dx_exists = has_fields(song, DX_FIELDS)

    # If both STD and DX exist, split into two entries
    if std_exists and dx_exists:
        # STD version
        std_entry = song.copy()
        std_entry['title'] = f"{song['title']} [STD]"
        # Remove DX fields
        for f in DX_FIELDS:
            std_entry.pop(f, None)
        result.append(std_entry)

        # DX version
        dx_entry = song.copy()
        dx_entry['title'] = f"{song['title']} [DX]"
        # Remove STD fields
        for f in STD_FIELDS:
            dx_entry.pop(f, None)
        result.append(dx_entry)
    else:
        # Only one version exists, tag accordingly
        entry = song.copy()
        if dx_exists:
            entry['title'] = f"{song['title']} [DX]"
        elif std_exists:
            entry['title'] = f"{song['title']} [STD]"
        result.append(entry)

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)