import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from creds import creds

class DatabaseManager:
    """
    A utility class to manage database connections and execute queries in PostgreSQL.
    """
    
    _conn_config = creds.get_database_config()

    @classmethod
    def _connect(cls):
        """
        Establishes a connection to the PostgreSQL database.

        Returns:
            tuple: A connection object and a cursor object.
        """
        try:
            conn = psycopg2.connect(
                dbname=cls._conn_config["name"],
                user=cls._conn_config["user"],
                password=cls._conn_config["password"],
                host=cls._conn_config["host"],
                port=cls._conn_config["port"]
            )
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            return conn, cursor
        except Exception as e:
            print(f"❌ Error connecting to the database: {e}")
            return None, None

    @classmethod
    def execute_query(cls, query: str) -> pd.DataFrame | None:
        """
        Executes a SQL query.
        
        - If the query is a SELECT or starts with "WITH", returns a DataFrame.
        - Otherwise, commits changes to the database.

        Args:
            query (str): The SQL query to execute.

        Returns:
            pd.DataFrame | None: Query results as a DataFrame if applicable.
        """
        conn, cursor = cls._connect()
        if not conn or not cursor:
            return None

        try:
            cursor.execute(query)
            
            if query.strip().upper().startswith(("SELECT", "WITH")):
                result = cursor.fetchall()
                return pd.DataFrame(result)
            else:
                conn.commit()
                print("✅ Query executed successfully")
                return None
        except Exception as e:
            print(f"❌ Error executing query: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
            print("🔒 Connection closed")

    @classmethod
    def execute_sql_file(cls, file_path: str) -> pd.DataFrame | None:
        """
        Reads and executes a SQL query from a file.

        Args:
            file_path (str): Path to the SQL file.

        Returns:
            pd.DataFrame | None: Query results as a DataFrame if applicable.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                query = file.read()

            print(f"📄 Executing SQL file: {file_path}...")
            return cls.execute_query(query)
        except Exception as e:
            print(f"❌ Error reading or executing SQL file '{file_path}': {e}")
            return None

    @classmethod
    def upsert_table(cls, df: pd.DataFrame, table_name: str) -> None:
        """
        Inserts or updates a table in the database using Pandas DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing the data to be inserted.
            table_name (str): The name of the target database table.
        """
        engine = None
        try:
            engine = create_engine(
                f'postgresql://{cls._conn_config["user"]}:{cls._conn_config["password"]}'
                f'@{cls._conn_config["host"]}:{cls._conn_config["port"]}/{cls._conn_config["name"]}'
            )
            df.to_sql(table_name, con=engine, if_exists='append', index=False, chunksize=1000)
            print(f"✅ Data inserted into table '{table_name}' successfully")
        except Exception as e:
            print(f"❌ Error inserting data into table '{table_name}': {e}")
        finally:
            if engine:
                engine.dispose()
                print("🔒 Database engine disposed")
