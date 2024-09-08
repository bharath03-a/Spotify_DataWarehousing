import scripts.connection as SF_CNCT
import helper.db_constants as DB_CONST
import helper.constants as CNT

if __name__ == "__main__":
    """
    Main execution block for setting up the Snowflake environment and creating tables.

    - Connects to Snowflake using provided credentials.
    - Sets up the environment by creating the specified data warehouse, database, and schema if they do not exist.
    - Creates tables: Playlist, Artist, and Audio Features based on the schema provided in constants.
    """
    
    sf = SF_CNCT.SnowflakeConnector()

    try:
        print("Connecting to Snowflake...")
        sf.connect()
        
        print(f"Setting up environment with Warehouse: {DB_CONST.SF_WAREHOUSE}, "
              f"Database: {DB_CONST.SF_DATABASE}, Schema: {DB_CONST.SF_SCHEMA}...")
        sf.setup_env(dw_name=DB_CONST.SF_WAREHOUSE,
                     db_name=DB_CONST.SF_DATABASE,
                     schema_name=DB_CONST.SF_SCHEMA)
        
        print(f"Creating table '{DB_CONST.SF_PLAYLIST}'...")
        sf.create_table(dw_name=DB_CONST.SF_WAREHOUSE,
                        db_name=DB_CONST.SF_DATABASE,
                        schema_name=DB_CONST.SF_SCHEMA,
                        table_name=DB_CONST.SF_PLAYLIST,
                        table_schema=CNT.PLAYLIST_SCHEMA)
        print(f"Table '{DB_CONST.SF_PLAYLIST}' created successfully.")

        print(f"Creating table '{DB_CONST.SF_ARTIST}'...")
        sf.create_table(dw_name=DB_CONST.SF_WAREHOUSE,
                        db_name=DB_CONST.SF_DATABASE,
                        schema_name=DB_CONST.SF_SCHEMA,
                        table_name=DB_CONST.SF_ARTIST,
                        table_schema=CNT.ARTISTS_SCHEMA)
        print(f"Table '{DB_CONST.SF_ARTIST}' created successfully.")

        print(f"Creating table '{DB_CONST.SF_AUDIO}'...")
        sf.create_table(dw_name=DB_CONST.SF_WAREHOUSE,
                        db_name=DB_CONST.SF_DATABASE,
                        schema_name=DB_CONST.SF_SCHEMA,
                        table_name=DB_CONST.SF_AUDIO,
                        table_schema=CNT.AUDIO_FEATURES_SCHEMA)
        print(f"Table '{DB_CONST.SF_AUDIO}' created successfully.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        print("Closing Snowflake connection...")
        sf.close()
        print("Connection closed.")