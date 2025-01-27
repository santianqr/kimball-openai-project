import psycopg2
from psycopg2.extras import RealDictCursor

DB_NAME = 'postgres'
DB_USER = 'postgres'

try:
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
    print("Connected to the database")
except Exception as e:
    print(e)
    print("Database not connected")