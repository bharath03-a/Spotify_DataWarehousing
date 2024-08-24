import json
import csv
import scripts.client as cl
import helper.constants as CNT

api_instance = cl.API()
    
token = api_instance.get_access_token()
print(f"Access Token: {token}")

data, keys = api_instance.get_data()
print(f"Data: {len(data)}")
print(f"Keys: {keys}")

unimportant_keys = {
        'explicit', 'primary_color', 'preview_url', 'video_thumbnail', 
        'height', 'width', 'images', 'available_markets', 'spotify', 
        'uri', 'is_local', 'external_urls', 'external_ids'
    }

flattened_data = [api_instance.flatten_dict(item, exclude_keys=unimportant_keys) for item in data]

flattened_keys = set()
for item in flattened_data:
    flattened_keys.update(item.keys())

with open("./data/spotify_playlist.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=flattened_keys)
    writer.writeheader()
    writer.writerows(flattened_data)