import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from creds import creds

class db:
    def __init__(self):
        self.conn_config = creds.Creds().get_database_creds()

    def _connect(self):
        try:
            conn = psycopg2.connect(
                dbname=self.conn_config["name"],
                user=self.conn_config["user"],
                password=self.conn_config["password"],
                host=self.conn_config["host"],
                port=self.conn_config["port"]
            )
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            return conn, cursor
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return None, None

    def execute_query(self, query):
        conn, cursor = self._connect()
        if not conn or not cursor:
            return None

        try:
            cursor.execute(query)
            if query.strip().upper().startswith("SELECT"):
                result = cursor.fetchall()
                return pd.DataFrame(result)
            else:
                conn.commit()
                print("Non-SELECT query executed successfully")
                return None
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
            print("Database connection closed")

    def upsert_table(self, df, table_name):
        engine = None
        try:
            engine = create_engine(
                f'postgresql://{self.conn_config["user"]}:{self.conn_config["password"]}@{self.conn_config["host"]}:{self.conn_config["port"]}/{self.conn_config["name"]}'
            )
            df.to_sql(table_name, con=engine, if_exists='append', index=False, chunksize=1000)
            print(f"Data inserted into table '{table_name}' successfully")
        except Exception as e:
            print(f"Error inserting data into table '{table_name}': {e}")
        finally:
            if engine:
                engine.dispose()
                print("Database engine disposed")
