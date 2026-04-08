import json
import re

# Load the files
with open('maimaiJsonFile.json', encoding='utf-8') as f:
    maimai_json = json.load(f)

with open('maimaiModifiedInfo.json', encoding='utf-8') as f:
    modified_info = json.load(f)

# Build a lookup for modified info by title
mod_lookup = {entry['title']: entry for entry in modified_info}

# Helper function to find matching entry in modified_info
def find_matching_entry(title):
    # Try exact match first
    if title in mod_lookup:
        return mod_lookup[title]
    
    # Try without [STD] or [DX] tags
    base_title = re.sub(r'\s*\[(STD|DX)\]\s*$', '', title)
    if base_title != title and base_title in mod_lookup:
        return mod_lookup[base_title]
    
    # Try adding [STD] or [DX] tags if base title doesn't work
    std_title = f"{title} [STD]"
    dx_title = f"{title} [DX]"
    
    if std_title in mod_lookup:
        return mod_lookup[std_title]
    if dx_title in mod_lookup:
        return mod_lookup[dx_title]
    
    return None

STD_FIELDS = ['lev_bas', 'lev_adv', 'lev_exp', 'lev_mas', 'lev_remas']
DX_FIELDS  = ['dx_lev_bas', 'dx_lev_adv', 'dx_lev_exp', 'dx_lev_mas', 'dx_lev_remas']

# Track which songs from maimaiModifiedInfo.json were matched
matched_modified_songs = set()

for song in maimai_json:
    title = song.get('title')
    mod = find_matching_entry(title)
    
    if mod:
        # Track that this song from maimaiModifiedInfo.json was matched
        matched_modified_songs.add(mod['title'])
        
        # Add/replace version
        song['version'] = mod['version']

        # Add alias if it exists in modified info
        if 'alias' in mod:
            alias_string = mod['alias']
            # Split by "/" and clean up whitespace, remove empty strings
            aliases = [alias.strip() for alias in alias_string.split('/') if alias.strip()]
            song['alias'] = aliases

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

    # Handle image_url more intelligently
    if 'image_url' in song:
        current_url = song['image_url']
        
        # If there's a CloudFront URL embedded, extract just the clean CloudFront URL
        if 'https://dp4p6x0xfi5o9.cloudfront.net/maimai/img/cover/' in current_url:
            # Find the last occurrence of the CloudFront URL to get the cleanest version
            cloudfront_pattern = 'https://dp4p6x0xfi5o9.cloudfront.net/maimai/img/cover/'
            last_cloudfront_pos = current_url.rfind(cloudfront_pattern)
            if last_cloudfront_pos != -1:
                # Extract from the last CloudFront URL occurrence to the end
                clean_url = current_url[last_cloudfront_pos:] 
                song['image_url'] = clean_url
        # Only prepend maimaidx-eng prefix if URL doesn't already start with it and doesn't contain CloudFront
        elif not current_url.startswith('https://maimaidx-eng.com/maimai-mobile/img/Music/'):
            song['image_url'] = 'https://maimaidx-eng.com/maimai-mobile/img/Music/' + current_url

# Add songs from maimaiModifiedInfo.json that weren't matched with existing songs
added_songs = 0
for mod_song in modified_info:
    if mod_song['title'] not in matched_modified_songs:
        # Create a new song entry from the modified info
        new_song = {
            'title': mod_song['title'],
            'version': mod_song['version']
        }
        
        # Add alias if it exists
        if 'alias' in mod_song:
            alias_string = mod_song['alias']
            aliases = [alias.strip() for alias in alias_string.split('/') if alias.strip()]
            new_song['alias'] = aliases
        
        # Add STD difficulties
        if 'STD' in mod_song:
            for i, field in enumerate(STD_FIELDS):
                if i < len(mod_song['STD']):
                    new_song[field] = mod_song['STD'][i]
        
        # Add DX difficulties  
        if 'DX' in mod_song:
            for i, field in enumerate(DX_FIELDS):
                if i < len(mod_song['DX']):
                    new_song[field] = mod_song['DX'][i]
        
        # Add some default values that might be missing
        new_song.setdefault('artist', '')
        new_song.setdefault('catcode', '')
        new_song.setdefault('release', '000000')
        new_song.setdefault('sort', '')
        new_song.setdefault('title_kana', '')
        
        maimai_json.append(new_song)
        added_songs += 1

print(f"Added {added_songs} new songs from maimaiModifiedInfo.json that weren't in the base database")

# Save the updated file
with open('maimaiJsonFile.json', 'w', encoding='utf-8') as f:
    json.dump(maimai_json, f, ensure_ascii=False, indent=2)