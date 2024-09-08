import helper.constants as CNT
import helper.db_constants as SF_CNST
import scripts.client as cl
import get_data as dml
import scripts.connection as sf_cnct
import pandas as pd
from snowflake.connector.pandas_tools import write_pandas

class SnowFlakeSink:
    """
    SnowFlakeSink class is responsible for interacting with the Spotify API, cleaning data, and writing it to Snowflake.
    
    Attributes:
        spotify_api (API): An instance of the Spotify API client.
        spotify_info (DataManipulation): An instance of the data manipulation class.
        sf_connection (SnowflakeConnector): Connection object to interact with Snowflake.
        playlist_data (list): A list containing flattened playlist data retrieved from the Spotify API.
    """

    def __init__(self):
        """
        Initializes the SnowFlakeSink class by setting up the Spotify API, data manipulation instance, 
        and Snowflake connection. It also fetches the initial playlist data from Spotify and connects 
        to the Snowflake environment.
        """
        print("Initializing SnowFlakeSink...")
        self.spotify_api = cl.API()
        self.spotify_info = dml.DataManipulation()
        self.sf_connection = sf_cnct.SnowflakeConnector()

        print("Fetching playlist data from Spotify...")
        self.playlist_data = [self.spotify_api.flatten_dict(item, include_keys=CNT.PLAYLIST_KEYS)
                              for item in self.spotify_api.get_spotify_data(api_type="PLAYLISTS")[0]]

        print("Connecting to Snowflake...")
        self.sf_connection.connect()

        print(f"Using environment with Warehouse: {SF_CNST.SF_WAREHOUSE}, Database: {SF_CNST.SF_DATABASE}, Schema: {SF_CNST.SF_SCHEMA}")
        self.sf_connection.use_env(SF_CNST.SF_WAREHOUSE, SF_CNST.SF_DATABASE, SF_CNST.SF_SCHEMA)

    def clean_data(self, tag):
        """
        Cleans and processes data based on the provided tag (e.g., 'PLAYLISTS', 'ARTISTS', 'AUDIO_FEATURES').

        Args:
            tag (str): Specifies the type of data to clean.

        Returns:
            pd.DataFrame: A cleaned DataFrame ready to be written to Snowflake.
        """
        print(f"Cleaning data for tag: {tag}")
        
        if tag == "PLAYLISTS":
            data = self.playlist_data
            data_df = pd.DataFrame(data)
            data_df.rename(
                columns={"track_track": "track", "track_track_number": "track_number"},
                inplace=True
            )
            
            melted_df = data_df.copy()
            for config in CNT.PLAYLIST_MELT:
                melted_df = pd.melt(
                    melted_df,
                    id_vars=config['id_vars'],
                    value_vars=config['value_vars'],
                    var_name=config['var_name'],
                    value_name=config['value_name']
                )

            melted_df.drop(melted_df.filter(like='variable').columns, axis=1, inplace=True)
            
            playlist_sf = melted_df.loc[:, CNT.PLAYLIST_COLS]
            playlist_sf.dropna(subset = CNT.PLAYLIST_MELT_COLS, inplace=True)
            playlist_sf.columns = [col.upper() for col in playlist_sf.columns]

            return playlist_sf

        elif tag == "ARTISTS":
            artist_data, _ = self.spotify_api.get_spotify_data(api_type="ARTISTS", 
                                                               input_data=self.spotify_info.get_artist_ids(self.playlist_data, "track_album_artists_1_uri"))
            data = [self.spotify_api.flatten_dict(item, include_keys=CNT.ARTIST_KEYS) for item in artist_data]
            data_df = pd.DataFrame(data)
            
            data_df_melt = data_df.melt(id_vars=["followers_total", "name", "id", "popularity"], 
                                        value_vars=["genres_1", "genres_2", "genres_3"], 
                                        var_name="genre_type", 
                                        value_name="artist_genres")

            data_df_melt.dropna(subset = ["artist_genres"], inplace=True)
            data_df_melt.drop(["genre_type"], axis=1, inplace=True)
            data_df_melt.rename(columns={"followers_total": "followers_count"}, inplace=True)
            
            artists_sf = data_df_melt.loc[:, CNT.ARTIST_COLS]
            artists_sf.columns = [col.upper() for col in artists_sf.columns]

            return artists_sf

        else:
            audio_data, _ = self.spotify_api.get_spotify_data(api_type="AUDIO_FEATURES", 
                                                              input_data=self.spotify_info.get_track_ids(self.playlist_data, "track_id"))
            data = [self.spotify_api.flatten_dict(item, include_keys=CNT.AUDIO_KEYS) for item in audio_data]
            data_df = pd.DataFrame(data)
            audio_features = data_df.loc[:, CNT.AUDIO_COLS]
            audio_features.columns = [col.upper() for col in audio_features.columns]

            return audio_features

    def write_table(self, tag, table):
        """
        Writes the cleaned data to a Snowflake table.

        Args:
            tag (str): The type of data to be written (e.g., 'PLAYLISTS', 'ARTISTS', 'AUDIO_FEATURES').
            table (str): The name of the Snowflake table where the data should be written.
        """
        try:
            print(f"Cleaning and writing data for tag: {tag} to table: {table}")
            data_df = self.clean_data(tag)

            print(f"Writing data to {table}...")
            success, nchunks, nrows, _ = write_pandas(self.sf_connection.get_connection(), data_df, table.upper())

            if success:
                print(f"Data written successfully to {table}. Number of chunks: {nchunks}, Number of rows: {nrows}")
            else:
                print(f"Failed to write data to {table}.")
        
        except Exception as e:
            print(f"An error occurred while writing to the table {table}: {e}")

    def update_table(self):
        """
        Placeholder for future updates. This function will handle updating existing tables with new data.
        """
        print("Update table method not yet implemented.")

if __name__ == '__main__':
    """
    Main execution block:
    - Instantiates the SnowFlakeSink class.
    - Writes 'PLAYLISTS', 'ARTISTS', and 'AUDIO_FEATURES' data to the corresponding Snowflake tables.
    """
    
    print("Starting Snowflake Sink process...")
    
    sf_sink = SnowFlakeSink()
    
    sf_sink.write_table(tag="PLAYLISTS", table=SF_CNST.SF_PLAYLIST)

    sf_sink.write_table(tag="ARTISTS", table=SF_CNST.SF_ARTIST)
    
    sf_sink.write_table(tag="AUDIO_FEATURES", table=SF_CNST.SF_AUDIO)
    
    print("Process completed.")