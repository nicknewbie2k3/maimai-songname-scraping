import json
import os

input_path = os.path.join(os.path.dirname(__file__), 'maimaiDatabase.json')
output_path = os.path.join(os.path.dirname(__file__), 'maimaiOneTypeDatabase.json')

STD_FIELDS = ['lev_bas', 'lev_adv', 'lev_exp', 'lev_mas', 'lev_remas']
DX_FIELDS  = ['dx_lev_bas', 'dx_lev_adv', 'dx_lev_exp', 'dx_lev_mas', 'dx_lev_remas']

def convert_to_one_type(song):
    new_song = song.copy()
    chart_type = None

    # If DX fields exist, use them and set chart_type to DX
    if any(f in song for f in DX_FIELDS):
        chart_type = "DX"
        for std, dx in zip(STD_FIELDS, DX_FIELDS):
            if dx in song:
                new_song[std] = song[dx]
            elif std in new_song:
                # Remove STD field if DX doesn't have a value
                new_song.pop(std, None)
        # Remove all DX fields
        for dx in DX_FIELDS:
            new_song.pop(dx, None)
    else:
        chart_type = "STD"
        # Remove any DX fields just in case
        for dx in DX_FIELDS:
            new_song.pop(dx, None)

    new_song["chart_type"] = chart_type
    return new_song

with open(input_path, 'r', encoding='utf-8') as f:
    songs = json.load(f)

result = [convert_to_one_type(song) for song in songs]

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)