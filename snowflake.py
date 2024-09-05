import helper.constants as CNT
import scripts.client as cl
import get_data as dml

class SnowFlakeSink:
    def __init__(self):
        self.spotify_api = cl.API()
        self.spotify_info = dml.DataManipulation()

    def clean_data(self, tag):
        if tag == "PLAYLISTS":
            playlist_data, _ = self.spotify_api.get_spotify_data(api_type="PLAYLISTS")
            data = [self.spotify_api.flatten_dict(item, include_keys = CNT.PLAYLIST_KEYS) for item in playlist_data]
            print(data[0])
        elif tag == "ARTISTS":
            pass
        else:
            pass

    def write_table(self):
        pass

    def update_table(self):
        pass

if __name__ == '__main__':
    sf_sink = SnowFlakeSink()
    sf_sink.clean_data("PLAYLISTS")