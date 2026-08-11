import json
import os

song_db_path = os.path.join(os.path.dirname(__file__), '..', 'maimai-songDatabase.json')
one_type_path = os.path.join(os.path.dirname(__file__), 'maimaiOneTypeDatabase_nodup.json')
output_path = os.path.join(os.path.dirname(__file__), '..', 'maimaiFinal.json')

with open(song_db_path, 'r', encoding='utf-8') as f:
    song_db = json.load(f)

version_map = {}

for song in song_db['songs']:
    title = song['title']
    song_version = song.get('version', '')
    seen_types = set()
    for sheet in song['sheets']:
        sheet_type = sheet['type'].upper()
        if sheet_type not in seen_types:
            seen_types.add(sheet_type)
            sheet_version = sheet.get('version', '')
            key = (title, sheet_type)
            version_map[key] = sheet_version or song_version

with open(one_type_path, 'r', encoding='utf-8') as f:
    one_type_db = json.load(f)

import re
suffix_pattern = re.compile(r'\s+\[(STD|DX)\]$')
plain_space_suffix = re.compile(r' +\[(STD|DX)\]$')

matched = 0
unmatched = 0
unmatched_entries = []

for entry in one_type_db:
    chart_type = entry.get('chart_type', '')
    raw_title = entry.get('title', '')

    m = suffix_pattern.search(raw_title)
    if m:
        base_title = raw_title[:m.start()]
        if not base_title:
            m2 = plain_space_suffix.search(raw_title)
            if m2:
                base_title = raw_title[:m2.start()]
    elif entry.get('alias') and len(entry['alias']) > 0:
        base_title = entry['alias'][0]
    else:
        base_title = raw_title

    found = False
    key = (base_title, chart_type)
    if key in version_map:
        entry['version'] = version_map[key]
        found = True
    elif entry.get('alias'):
        for alias in entry['alias']:
            alias_key = (alias, chart_type)
            if alias_key in version_map:
                entry['version'] = version_map[alias_key]
                found = True
                break

    if found:
        matched += 1
    else:
        unmatched += 1
        unmatched_entries.append({
            'raw_title': raw_title,
            'base_title': base_title,
            'chart_type': chart_type
        })

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(one_type_db, f, ensure_ascii=False, indent=2)

print(f"Total entries: {len(one_type_db)}")
print(f"Matched: {matched}")
print(f"Unmatched: {unmatched}")
if unmatched_entries:
    with open(output_path.replace('maimaiFinal.json', 'unmatched_log.json'), 'w', encoding='utf-8') as f:
        json.dump(unmatched_entries, f, ensure_ascii=False, indent=2)
    print(f"Unmatched entries written to unmatched_log.json")
print(f"Output: {output_path}")
