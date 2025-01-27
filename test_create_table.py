from sqlalchemy import create_engine
import pandas as pd
import config.config as config

conn = config.Config()
db_conn = conn.get_database_config()

db_name=db_conn["name"]
db_user=db_conn["user"]
db_password=db_conn["password"]
db_host=db_conn["host"]
db_port=db_conn["port"]

engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

df = pd.DataFrame({
    'column1': [1, 2, 3, 4],
    'column2': ['A', 'B', 'C', 'D'],
    'column3': [0.1, 0.2, 0.3, 0.4]
})

table_name = 'test_table'
df.to_sql(table_name, con=engine, if_exists='append', index=False, chunksize=1000)

print("Data uploaded successfully to PostgreSQL RDS.")

query = f"SELECT COUNT(*) FROM test_table"
result = pd.read_sql(query, con=engine)
print(result)
