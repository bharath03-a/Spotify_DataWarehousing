import os
import sys
import snowflake.connector

# setting the path to import the constants module
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

    def setup_env(self, dw_name, db_name, schema_name):
        dw_query = f"CREATE WAREHOUSE IF NOT EXISTS {dw_name}"
        db_query = f"CREATE DATABASE IF NOT EXISTS {db_name}"
        schema_query = f"""
                        CREATE SCHEMA IF NOT EXISTS {db_name}.{schema_name}
                        """
        
        self.execute_query(dw_query)
        self.execute_query(db_query)
        self.execute_query(schema_query)

        print(f"Created DataWarehouse: {dw_name}, Database: {db_name} and Schema: {schema_name}")

    def create_table(self, dw_name, db_name, schema_name, table_name, table_schema):
        self.use_env(dw_name, db_name, schema_name)
        table_query = f"CREATE OR REPLACE TABLE {table_name}{table_schema}"

        self.execute_query(table_query)

    def use_env(self, dw_name, db_name, schema_name):
        self.execute_query(f"""USE WAREHOUSE {dw_name}
                           USE DATABASE {db_name}
                           USE SCHEMA {schema_name}""")

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
