import json
import csv
import scripts.client as cl
import helper.constants as CNT

class WriteData():
    def __init__(self, api_instance):
        self.api_instance = api_instance

    def write_csv(self, data):
        important_keys = {
            'added_at', 'added_by', 'id', 'type', 'track', 'album', 'album_type', 'name', 'release_date',
            'release_date_precision', 'uri', 'artists', 'total_tracks', 'disc_number', 'track_number', 
            'duration_ms', 'popularity'
        }

        flattened_data = [api_instance.flatten_dict(item, include_keys = important_keys) for item in data]

        flattened_keys = set()
        for item in flattened_data:
            flattened_keys.update(item.keys())

        with open(CNT.CSV_PATH, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=flattened_keys)
            writer.writeheader()
            writer.writerows(flattened_data)

    def write_json(self, data):
        with open(CNT.JSON_PATH, "w") as f:
            json.dump(data, f, indent=4)
    
if __name__ == '__main__':
    api_instance = cl.API()

    data, keys = api_instance.get_data()
    print(f"Data: {json.dumps(data, indent=4)}")
    print(f"Keys: {keys}")

    write_data = WriteData(api_instance=api_instance)
    write_data.write_csv(data)
    write_data.write_json(data)