import json
import csv
import scripts.client as cl
import helper.constants as CNT
import pandas as pd

class WriteData():
    def __init__(self, api_instance):
        self.api_instance = api_instance

    def write_playlist_csv(self, data, path, imp_keys):
        flattened_data = [api_instance.flatten_dict(item, include_keys = imp_keys) for item in data]

        flattened_keys = set()
        for item in flattened_data:
            flattened_keys.update(item.keys())

        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=flattened_keys)
            writer.writeheader()
            writer.writerows(flattened_data)
        
        return flattened_data

    def write_json(self, data, path):
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

class DataManipulation():
    def __init__(self):
        pass

    def read_data(self, data):
        playlist_data = pd.DataFrame(data)
        return playlist_data

    def get_artist_ids(self, data, col):
        data = self.read_data(data)
        artists = data[col].unique().tolist()

        split_fn = lambda x : x.split(":")[-1]

        return list(map(split_fn, artists))
    
    def get_track_ids(self, data, col):
        data = self.read_data(data)
        tracks = data[col].unique().tolist()

        return tracks

if __name__ == '__main__':
    api_instance = cl.API()

    playlist_data, playlist_keys = api_instance.get_spotify_data(api_type="PLAYLISTS")
    print(f"Keys: {playlist_keys}")

    write_data = WriteData(api_instance=api_instance)
    playlist_data = write_data.write_playlist_csv(playlist_data, CNT.PLAYLIST_CSV_PATH, CNT.PLAYLIST_KEYS)
    write_data.write_json(playlist_data, CNT.PLAYLIST_JSON_PATH)

    spotify_dml = DataManipulation()

    artist_data, artist_keys = api_instance.get_spotify_data(api_type="ARTISTS", input_data=spotify_dml.get_artist_ids(playlist_data, "track_album_artists_1_uri"))
    print(f"Keys: {artist_keys}")

    write_data.write_playlist_csv(artist_data, CNT.ARTIST_CSV_PATH, CNT.ARTIST_KEYS)
    write_data.write_json(artist_data, CNT.ARTIST_JSON_PATH)

    audio_data, audiio_keys = api_instance.get_spotify_data(api_type="AUDIO_FEATURES", input_data=spotify_dml.get_track_ids(playlist_data, "track_id"))
    print(f"Keys: {audiio_keys}")

    write_data.write_playlist_csv(audio_data, CNT.AUDIO_CSV_PATH, CNT.AUDIO_KEYS)
    write_data.write_json(audio_data, CNT.AUDIO_JSON_PATH)