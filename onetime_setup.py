import scripts.connection as SF_CNCT
import helper.db_constants as DB_CONST
import helper.constants as CNT

# Include Table creation too
if __name__ == "__main__":
    sf = SF_CNCT.SnowflakeConnector()
    try:
        sf.connect()
        sf.setup_env(dw_name=DB_CONST.SF_WAREHOUSE,
                     db_name=DB_CONST.SF_DATABASE,
                     schema_name=DB_CONST.SF_SCHEMA)
    finally:
        sf.close()