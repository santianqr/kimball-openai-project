import psycopg2
import config
from psycopg2.extras import RealDictCursor

conn = config.Config()
db_conn = conn.get_database_config()

try:
    conn = psycopg2.connect(
        dbname=db_conn["name"],
        user=db_conn["user"],
        password=db_conn["password"],
        host=db_conn["host"],
        port=db_conn["port"],
    )
    print("Connected to the database")
except Exception as e:
    print(e)
    print("Database not connected")
finally:
    conn.close()
    print("Database connection closed")