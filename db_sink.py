import helper.constants as CNT
import scripts.client as cl
import get_data as dml

import pandas as pd

class SnowFlakeSink:
    def __init__(self):
        self.spotify_api = cl.API()
        self.spotify_info = dml.DataManipulation()
        self.playlist_data = [self.spotify_api.flatten_dict(item, include_keys = CNT.PLAYLIST_KEYS) for item in self.spotify_api.get_spotify_data(api_type="PLAYLISTS")[0]]

    def clean_data(self, tag):
        if tag == "PLAYLISTS":
            data = self.playlist_data
            data_df = pd.DataFrame(data)
            print(data_df.columns)
        elif tag == "ARTISTS":
            artist_data, _ = self.spotify_api.get_spotify_data(api_type="ARTISTS", 
                                                               input_data=self.spotify_info.get_artist_ids(self.playlist_data, "track_album_artists_1_uri"))
            data = [self.spotify_api.flatten_dict(item, include_keys = CNT.ARTIST_KEYS) for item in artist_data]
            data_df = pd.DataFrame(data)
            print(data_df.columns)
        else:
            audio_data, _ = self.spotify_api.get_spotify_data(api_type="AUDIO_FEATURES", 
                                                              input_data=self.spotify_info.get_track_ids(self.playlist_data, "track_id"))
            data = [self.spotify_api.flatten_dict(item, include_keys = CNT.AUDIO_KEYS) for item in audio_data]
            data_df = pd.DataFrame(data)
            print(data_df.columns)

    def write_table(self):
        pass

    def update_table(self):
        pass

if __name__ == '__main__':
    sf_sink = SnowFlakeSink()
    sf_sink.clean_data("ARTISTS")