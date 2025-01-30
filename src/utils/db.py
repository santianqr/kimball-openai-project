import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from creds import creds

class db:
    conn_config = creds.get_database_config()

    @classmethod
    def _connect(cls):
        try:
            conn = psycopg2.connect(
                dbname=cls.conn_config["name"],
                user=cls.conn_config["user"],
                password=cls.conn_config["password"],
                host=cls.conn_config["host"],
                port=cls.conn_config["port"]
            )
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            return conn, cursor
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return None, None

    @classmethod
    def execute_query(cls, query):
        """
        Ejecuta una consulta SQL.
        - Si es una consulta SELECT o comienza con "WITH", devuelve un DataFrame con los resultados.
        - Si es otra consulta (INSERT, UPDATE, DELETE), solo la ejecuta y confirma cambios.
        """
        conn, cursor = cls._connect()
        if not conn or not cursor:
            return None

        try:
            cursor.execute(query)
            
            # Manejo especial para consultas con CTE (WITH)
            if query.strip().upper().startswith(("SELECT", "WITH")):
                result = cursor.fetchall()
                return pd.DataFrame(result)  # Convertir a DataFrame
            else:
                conn.commit()
                print("✅ Query ejecutada con éxito")
                return None
        except Exception as e:
            print(f"❌ Error ejecutando la consulta: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
            print("🔒 Conexión cerrada")

    @classmethod
    def execute_sql_file(cls, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                query = file.read()

            print(f"📄 Ejecutando consulta desde {file_path}...")
            return cls.execute_query(query)

        except Exception as e:
            print(f"❌ Error leyendo o ejecutando el archivo SQL {file_path}: {e}")
            return None


    @classmethod
    def upsert_table(cls, df, table_name):
        engine = None
        try:
            engine = create_engine(
                f'postgresql://{cls.conn_config["user"]}:{cls.conn_config["password"]}@{cls.conn_config["host"]}:{cls.conn_config["port"]}/{cls.conn_config["name"]}'
            )
            df.to_sql(table_name, con=engine, if_exists='append', index=False, chunksize=1000)
            print(f"Data inserted into table '{table_name}' successfully")
        except Exception as e:
            print(f"Error inserting data into table '{table_name}': {e}")
        finally:
            if engine:
                engine.dispose()
                print("Database engine disposed")
