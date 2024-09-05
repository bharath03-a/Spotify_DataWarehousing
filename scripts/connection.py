import os
import sys
import snowflake.connector

# Setting the path to import the constants module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import helper.db_constants as CNT

class SnowflakeConnector:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = snowflake.connector.connect(
                user=CNT.SF_USER,
                password=CNT.SF_PASSWORD,
                account=CNT.SF_ACCOUNT
            )
            self.cursor = self.connection.cursor()
            print("Successfully connected to Snowflake.")
        except Exception as e:
            print(f"Error connecting to Snowflake: {e}")
            raise

    def execute_query(self, query):
        if not self.cursor:
            raise Exception("Not connected to Snowflake.")
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error executing query: {e}")
            raise

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Snowflake connection closed.")


if __name__ == "__main__":
    sf = SnowflakeConnector()
    try:
        sf.connect()
        result = sf.execute_query("SELECT CURRENT_VERSION()")
        print(result)
    finally:
        sf.close()
