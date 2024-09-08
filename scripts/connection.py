import os
import sys
import snowflake.connector

# Setting the path to import the constants module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import helper.db_constants as CNT

class SnowflakeConnector:
    """
    A class to manage Snowflake connections and operations.
    """

    def __init__(self):
        """
        Initializes the SnowflakeConnector instance. Sets the connection and cursor to None.
        """
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        Connects to the Snowflake database using credentials from the db_constants module.
        Prints a success message upon connection or an error message if the connection fails.
        """
        try:
            print("Attempting to connect to Snowflake...")
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
        """
        Executes the provided SQL query using the Snowflake cursor.
        
        :param query: The SQL query to be executed.
        :return: The results of the query as a list of tuples.
        :raises Exception: If the query execution fails or the cursor is not available.
        """
        if not self.cursor:
            raise Exception("Not connected to Snowflake.")
        try:
            print(f"Executing query: {query}")
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            print(f"Query executed successfully. Result: {result}")
            return result
        except Exception as e:
            print(f"Error executing query: {e}")
            raise

    def setup_env(self, dw_name, db_name, schema_name):
        """
        Creates the data warehouse, database, and schema if they do not exist.
        
        :param dw_name: Name of the data warehouse to be created.
        :param db_name: Name of the database to be created.
        :param schema_name: Name of the schema to be created.
        """
        print(f"Setting up environment: Data Warehouse '{dw_name}', Database '{db_name}', Schema '{schema_name}'")
        dw_query = f"CREATE WAREHOUSE IF NOT EXISTS {dw_name}"
        db_query = f"CREATE DATABASE IF NOT EXISTS {db_name}"
        schema_query = f"""CREATE SCHEMA IF NOT EXISTS {db_name}.{schema_name}"""
        
        self.execute_query(dw_query)
        self.execute_query(db_query)
        self.execute_query(schema_query)

        print(f"Environment setup complete: Data Warehouse: {dw_name}, Database: {db_name}, Schema: {schema_name}")

    def create_table(self, dw_name, db_name, schema_name, table_name, table_schema):
        """
        Creates a table in the specified data warehouse, database, and schema.
        
        :param dw_name: Name of the data warehouse to be used.
        :param db_name: Name of the database to be used.
        :param schema_name: Name of the schema to be used.
        :param table_name: Name of the table to be created.
        :param table_schema: The schema of the table to be created.
        """
        print(f"Creating table '{table_name}' in {dw_name}.{db_name}.{schema_name}")
        self.use_env(dw_name, db_name, schema_name)
        table_query = f"CREATE OR REPLACE TABLE {table_name}{table_schema}"

        self.execute_query(table_query)
        print(f"Table '{table_name}' created successfully.")

    def use_env(self, dw_name, db_name, schema_name):
        """
        Switches the environment to use the specified warehouse, database, and schema.
        
        :param dw_name: Name of the data warehouse to switch to.
        :param db_name: Name of the database to switch to.
        :param schema_name: Name of the schema to switch to.
        """
        print(f"Switching to environment: Data Warehouse '{dw_name}', Database '{db_name}', Schema '{schema_name}'")
        self.execute_query(f"USE WAREHOUSE {dw_name}")
        self.execute_query(f"USE DATABASE {db_name}")
        self.execute_query(f"USE SCHEMA {schema_name}")
        print("Environment switched successfully.")

    def get_connection(self):
        """
        Returns the Snowflake connection object.
        
        :return: The Snowflake connection object.
        """
        if self.connection is None:
            raise Exception("Connection not established.")
        return self.connection

    def close(self):
        """
        Closes the Snowflake connection and cursor. Prints a message indicating that the connection is closed.
        """
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
        print(f"Snowflake version: {result}")
    finally:
        sf.close()
