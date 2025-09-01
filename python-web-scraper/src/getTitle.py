import json

# Load the song database from the correct path
with open('../maimai-songDatabase.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    songs = data['songs']

# Use a set to track unique imageNames
seen_images = set()
output = []

for song in songs:
    title = song.get('title')
    image_name = song.get('imageName')
    if image_name and image_name not in seen_images:
        output.append({'title': title, 'imageName': image_name})
        seen_images.add(image_name)

# Write the result to maimai-songName.json in the same directory as the database
with open('../maimai-songName.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)