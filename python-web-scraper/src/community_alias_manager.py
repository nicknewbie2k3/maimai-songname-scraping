#!/usr/bin/env python3
"""
Community Alias Backup/Restore Utility

This script helps preserve community-added aliases during pipeline updates.
Use this as an extra safety measure if needed.

Usage:
  python community_alias_manager.py backup    # Create backup before running pipeline
  python community_alias_manager.py restore   # Restore aliases after pipeline
  python community_alias_manager.py merge     # Merge backup aliases into current file
"""

import json
import sys
import os
from datetime import datetime

DATABASE_FILE = 'maimaiOneTypeDatabase_replaced.json'
BACKUP_FILE = 'community_aliases_backup.json'

def backup_aliases():
    """Extract and backup all community aliases from the database"""
    if not os.path.exists(DATABASE_FILE):
        print(f"Error: {DATABASE_FILE} not found!")
        return False
    
    with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract aliases from all songs
    community_aliases = {}
    total_songs = 0
    songs_with_aliases = 0
    
    for song in data:
        title = song.get('title')
        aliases = song.get('alias', [])
        
        if title:
            total_songs += 1
            if isinstance(aliases, list) and len(aliases) > 0:
                # Only backup if aliases are more than just the title
                if len(aliases) > 1 or (len(aliases) == 1 and aliases[0] != title):
                    community_aliases[title] = aliases
                    songs_with_aliases += 1
    
    # Save backup with timestamp
    backup_data = {
        'timestamp': datetime.now().isoformat(),
        'total_songs': total_songs,
        'songs_with_aliases': songs_with_aliases,
        'aliases': community_aliases
    }
    
    with open(BACKUP_FILE, 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Backup created: {BACKUP_FILE}")
    print(f"📊 Total songs: {total_songs}")
    print(f"📊 Songs with aliases: {songs_with_aliases}")
    print(f"📅 Timestamp: {backup_data['timestamp']}")
    return True

def restore_aliases():
    """Restore community aliases from backup into the database"""
    if not os.path.exists(BACKUP_FILE):
        print(f"Error: {BACKUP_FILE} not found! Run backup first.")
        return False
    
    if not os.path.exists(DATABASE_FILE):
        print(f"Error: {DATABASE_FILE} not found!")
        return False
    
    # Load backup
    with open(BACKUP_FILE, 'r', encoding='utf-8') as f:
        backup_data = json.load(f)
    
    # Load current database
    with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
        current_data = json.load(f)
    
    # Merge aliases
    merged_count = 0
    community_aliases = backup_data.get('aliases', {})
    
    for song in current_data:
        title = song.get('title')
        if title in community_aliases:
            # Restore the community aliases
            song['alias'] = community_aliases[title]
            merged_count += 1
    
    # Save updated database
    with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
        json.dump(current_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Aliases restored to {DATABASE_FILE}")
    print(f"📊 Songs updated: {merged_count}")
    print(f"📅 Backup from: {backup_data.get('timestamp', 'Unknown')}")
    return True

def merge_aliases():
    """Smart merge - adds community aliases without overwriting existing ones"""
    if not os.path.exists(BACKUP_FILE):
        print(f"Error: {BACKUP_FILE} not found! Run backup first.")
        return False
    
    if not os.path.exists(DATABASE_FILE):
        print(f"Error: {DATABASE_FILE} not found!")
        return False
    
    # Load backup
    with open(BACKUP_FILE, 'r', encoding='utf-8') as f:
        backup_data = json.load(f)
    
    # Load current database
    with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
        current_data = json.load(f)
    
    # Smart merge
    updated_count = 0
    community_aliases = backup_data.get('aliases', {})
    
    for song in current_data:
        title = song.get('title')
        if title in community_aliases:
            current_aliases = song.get('alias', [])
            backup_aliases = community_aliases[title]
            
            # Merge aliases, avoiding duplicates
            if isinstance(current_aliases, list) and isinstance(backup_aliases, list):
                merged_aliases = list(current_aliases)  # Start with current
                
                # Add backup aliases that aren't already present
                for alias in backup_aliases:
                    if alias not in merged_aliases:
                        merged_aliases.append(alias)
                
                # Only update if we added something
                if len(merged_aliases) > len(current_aliases):
                    song['alias'] = merged_aliases
                    updated_count += 1
    
    # Save updated database
    with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
        json.dump(current_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Aliases merged into {DATABASE_FILE}")
    print(f"📊 Songs updated: {updated_count}")
    return True

def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return
    
    command = sys.argv[1].lower()
    
    if command == 'backup':
        backup_aliases()
    elif command == 'restore':
        restore_aliases()
    elif command == 'merge':
        merge_aliases()
    else:
        print(f"Unknown command: {command}")
        print(__doc__)

if __name__ == '__main__':
    main()