import json
import os

def get_internal_level(sheets, typ, diff):
    """Extract internal level from sheets data"""
    for sheet in sheets:
        if sheet.get('type') == typ and sheet.get('difficulty') == diff:
            val = sheet.get('internalLevelValue')
            if val is not None:
                return str(val)
    return ""

# File paths (update if needed)
database_path = os.path.join(os.path.dirname(__file__), '..', 'maimai-songDatabase.json')
target_path = os.path.join(os.path.dirname(__file__), 'maimaiOneTypeDatabase.json')
output_path = os.path.join(os.path.dirname(__file__), 'maimaiOneTypeDatabase_replaced.json')

# 1. Load song database
with open(database_path, encoding='utf-8') as f:
    db = json.load(f)
db_songs = db['songs']

# Build comprehensive mappings from database
title_to_song_data = {}
for song in db_songs:
    title = song.get('title')
    if title:
        sheets = song.get('sheets', [])
        title_to_song_data[title] = {
            'imageName': song.get('imageName', ''),
            'artist': song.get('artist', ''),
            'category': song.get('category', ''),
            'version': song.get('version', ''),
            'bpm': song.get('bpm', ''),
            'dx_lev_bas': get_internal_level(sheets, "dx", "basic"),
            'dx_lev_adv': get_internal_level(sheets, "dx", "advanced"),
            'dx_lev_exp': get_internal_level(sheets, "dx", "expert"),
            'dx_lev_mas': get_internal_level(sheets, "dx", "master"),
            'dx_lev_remas': get_internal_level(sheets, "dx", "remaster"),
            'lev_bas': get_internal_level(sheets, "std", "basic"),
            'lev_adv': get_internal_level(sheets, "std", "advanced"),
            'lev_exp': get_internal_level(sheets, "std", "expert"),
            'lev_mas': get_internal_level(sheets, "std", "master"),
            'lev_remas': get_internal_level(sheets, "std", "remaster"),
        }

# 2. Load target file
with open(target_path, encoding='utf-8') as f:
    target = json.load(f)

# Create a title-to-index mapping for existing songs
target_title_map = {}
for i, song in enumerate(target):
    title = song.get('title')
    if title:
        target_title_map[title] = i

# 3. Process existing songs - replace image URLs and merge missing data
image_changed = 0
data_updated = 0
maimaidx_converted = 0
new_songs_added = 0
aliases_preserved = 0

for song in target:
    title = song.get('title')
    if not title:
        continue
        
    current_image_url = song.get('image_url', '')
    
    # Handle image URL replacement (FORCE REPLACE)
    if title in title_to_song_data and title_to_song_data[title]['imageName']:
        # Always update image URL from database, regardless of existing value
        new_url = f"https://dp4p6x0xfi5o9.cloudfront.net/maimai/img/cover/{title_to_song_data[title]['imageName']}"
        song['image_url'] = new_url
        image_changed += 1
        image_updated = True
    elif 'maimaidx' in current_image_url and 'img/Music/' in current_image_url:
        # Convert maimaidx URLs to CloudFront as fallback
        filename = current_image_url.split('img/Music/')[-1]
        if filename:
            song['image_url'] = f"https://dp4p6x0xfi5o9.cloudfront.net/maimai/img/cover/{filename}"
            image_changed += 1
            maimaidx_converted += 1
            image_updated = True
    
    # Handle data merging from database (ONLY FILL EMPTY FIELDS)
    if title in title_to_song_data:
        db_data = title_to_song_data[title]
        song_updated = False
        
        # Map database fields to target fields
        field_mappings = {
            'artist': db_data['artist'],
            'catcode': db_data['category'],
            'version': db_data['version']
        }
        
        # Add level mappings
        level_mappings = {
            'dx_lev_bas': db_data['dx_lev_bas'],
            'dx_lev_adv': db_data['dx_lev_adv'],
            'dx_lev_exp': db_data['dx_lev_exp'],
            'dx_lev_mas': db_data['dx_lev_mas'],
            'dx_lev_remas': db_data['dx_lev_remas'],
            'lev_bas': db_data['lev_bas'],
            'lev_adv': db_data['lev_adv'],
            'lev_exp': db_data['lev_exp'],
            'lev_mas': db_data['lev_mas'],
            'lev_remas': db_data['lev_remas']
        }
        field_mappings.update(level_mappings)
        
        # Only update fields that are missing or empty string
        for field, db_value in field_mappings.items():
            current_value = song.get(field)
            # Only update if field doesn't exist, is None, or is empty string, and DB has a value
            if (current_value is None or current_value == '') and db_value:
                song[field] = db_value
                song_updated = True
        
        # Special handling for aliases - PRESERVE existing aliases, don't overwrite them
        # This ensures community-added aliases are kept during updates
        existing_aliases = song.get('alias', [])
        if isinstance(existing_aliases, list) and len(existing_aliases) > 0:
            # Keep existing aliases - don't overwrite with database data
            aliases_preserved += 1
        elif db_data.get('artist'):  # Only add basic alias if no aliases exist
            song['alias'] = [title]
            song_updated = True
        
        if song_updated:
            data_updated += 1

# 4. Add completely new songs from database that don't exist in target
# Only add songs that have actual chart data (at least one difficulty level)
for title, db_data in title_to_song_data.items():
    if title not in target_title_map:
        # Check if song has any chart data
        has_chart_data = any([
            db_data['dx_lev_bas'],
            db_data['dx_lev_adv'], 
            db_data['dx_lev_exp'],
            db_data['dx_lev_mas'],
            db_data['dx_lev_remas'],
            db_data['lev_bas'],
            db_data['lev_adv'],
            db_data['lev_exp'],
            db_data['lev_mas'],
            db_data['lev_remas']
        ])
        
        # Only add songs with actual chart data
        if has_chart_data:
            # Create new song entry
            new_song = {
                "title": title,
                "artist": db_data['artist'],
                "catcode": db_data['category'],
                "version": db_data['version'],
                "dx_lev_bas": db_data['dx_lev_bas'],
                "dx_lev_adv": db_data['dx_lev_adv'],
                "dx_lev_exp": db_data['dx_lev_exp'],
                "dx_lev_mas": db_data['dx_lev_mas'],
                "dx_lev_remas": db_data['dx_lev_remas'],
                "lev_bas": db_data['lev_bas'],
                "lev_adv": db_data['lev_adv'],
                "lev_exp": db_data['lev_exp'],
                "lev_mas": db_data['lev_mas'],
                "lev_remas": db_data['lev_remas'],
                "image_url": f"https://dp4p6x0xfi5o9.cloudfront.net/maimai/img/cover/{db_data['imageName']}" if db_data['imageName'] else "",
                "release": "000000",
                "sort": "",
                "title_kana": "",
                "alias": [title],
                "chart_type": "DX" if db_data['dx_lev_bas'] else "STD"
            }
            target.append(new_song)
            new_songs_added += 1

# 5. Save output
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(target, f, ensure_ascii=False, indent=2)

# 6. Report results
print(f"Done! Comprehensive database merge and URL replacement completed.")
print(f"")
print(f"Image URL Updates:")
print(f"  - {maimaidx_converted} maimaidx URLs converted to CloudFront")
print(f"  - {image_changed - maimaidx_converted} URLs updated from database mapping") 
print(f"  - {image_changed} total image URLs updated")
print(f"")
print(f"Data Updates:")
print(f"  - {data_updated} existing songs updated with missing data")
print(f"  - {aliases_preserved} songs had existing aliases preserved (community data protected)")
print(f"  - {new_songs_added} new songs added from database (only songs with chart data)")
print(f"") 
print(f"Total changes: {image_changed + data_updated + new_songs_added}")
print(f"Community aliases protected: {aliases_preserved} songs")
print(f"Note: Songs without chart constants are excluded and should be parsed from final result")
print(f"Output: {output_path}")