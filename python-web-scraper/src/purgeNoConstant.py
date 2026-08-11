import json
import os

input_path = os.path.join(os.path.dirname(__file__), 'maimaiOneTypeDatabase_replaced.json')
output_path = os.path.join(os.path.dirname(__file__), 'maimaiOneTypeDatabase_nodup.json')

CHART_FIELDS = ['lev_bas', 'lev_adv', 'lev_exp', 'lev_mas', 'lev_remas']

with open(input_path, 'r', encoding='utf-8') as f:
    songs = json.load(f)

kept = []
removed = 0

for song in songs:
    has_constant = any(song.get(f) for f in CHART_FIELDS)
    if has_constant:
        kept.append(song)
    else:
        removed += 1
        print(f"Removed (no chart constant): {song.get('title', 'UNKNOWN')}")

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(kept, f, ensure_ascii=False, indent=2)

print(f"\nKept: {len(kept)} songs")
print(f"Removed: {removed} songs")
print(f"Output: {output_path}")
