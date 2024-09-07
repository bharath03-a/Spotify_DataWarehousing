import helper.constants as CNT
import helper.db_constants as SF_CNST
import scripts.client as cl
import get_data as dml
import scripts.connection as sf_cnct
import pandas as pd
from snowflake.connector.pandas_tools import write_pandas

class SnowFlakeSink:
    def __init__(self):
        self.spotify_api = cl.API()
        self.spotify_info = dml.DataManipulation()
        self.sf_connection = sf_cnct.SnowflakeConnector()
        self.playlist_data = [self.spotify_api.flatten_dict(item, include_keys = CNT.PLAYLIST_KEYS) for item in self.spotify_api.get_spotify_data(api_type="PLAYLISTS")[0]]
        self.sf_connection.connect()
        self.sf_connection.use_env(SF_CNST.SF_WAREHOUSE, SF_CNST.SF_DATABASE, SF_CNST.SF_SCHEMA)

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
            data_df_melt = data_df.melt(id_vars=["followers_total", "name", "id", "popularity"], 
                                        value_vars=["genres_1", "genres_2", "genres_3"], 
                                        var_name="genre_type", 
                                        value_name="artist_genres")
            
            data_df_melt.dropna(subset=["artist_genres"], inplace=True)
            data_df_melt.drop(["genre_type"], axis=1, inplace=True)
            data_df_melt.rename(
                columns={ "followers_total" : "followers_count"},
                inplace=True)
            
            artists_sf = data_df_melt.loc[:, CNT.ARTIST_COLS]
            return artists_sf
        else:
            audio_data, _ = self.spotify_api.get_spotify_data(api_type="AUDIO_FEATURES", 
                                                              input_data=self.spotify_info.get_track_ids(self.playlist_data, "track_id"))
            data = [self.spotify_api.flatten_dict(item, include_keys = CNT.AUDIO_KEYS) for item in audio_data]
            data_df = pd.DataFrame(data)
            audio_features = data_df.loc[:, CNT.AUDIO_COLS]
            
            return audio_features

    def write_table(self, tag, table):
        try:
            data_df = self.clean_data(tag)
            success, nchunks, nrows, _ = write_pandas(self.sf_connection.cursor, data_df, table)

            if success:
                print(f"Data written successfully to {table}. Number of chunks: {nchunks}, Number of rows: {nrows}")
            else:
                print(f"Failed to write data to {table}.")
        
        except Exception as e:
            print(f"An error occurred while writing to the table {table}: {e}")

    def update_table(self):
        # TODO document why this method is empty
        pass

if __name__ == '__main__':
    sf_sink = SnowFlakeSink()
    sf_sink.clean_data("ARTISTS")