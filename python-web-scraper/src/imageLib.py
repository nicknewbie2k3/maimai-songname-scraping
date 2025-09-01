import json
import os
import requests

# Paths
json_path = os.path.join(os.path.dirname(__file__), 'maimaiJsonFile.json')
image_folder = os.path.join(os.path.dirname(__file__), 'image')

# Create image folder if it doesn't exist
os.makedirs(image_folder, exist_ok=True)

# Load JSON data
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Referer": "https://maimaidx-eng.com/"
}

for song in data:
    image_url = song.get('image_url')
    if image_url and image_url.startswith('http'):
        filename = os.path.basename(image_url)
        save_path = os.path.join(image_folder, filename)
        # Skip if already downloaded
        if os.path.exists(save_path):
            continue
        try:
            response = requests.get(image_url, headers=headers, timeout=10)
            if response.status_code == 200:
                with open(save_path, 'wb') as img_file:
                    img_file.write(response.content)
                print(f"Downloaded: {filename}")
            else:
                print(f"Failed to download {filename}: HTTP {response.status_code}")
        except Exception as e:
            print(f"Error downloading {filename}: {e}")