from src import db, processor, model, loader
import pandas as pd

file_path = 'data/raw/Invoices_Year_2009-2010.csv'

#df = processor.process_data(file_path)
#print(df.head(5))

df = db.execute_query("SELECT * FROM fact_sales LIMIT 5")
print("Data from database")
print(df)

#dim_product, dim_customer, dim_date, dim_country, fact_sales  = model.generate_model(df)
#print(dim_product)

#loader.upload_model(dim_product, dim_customer, dim_date, dim_country, fact_sales)
#db.upsert_table(df, 'invoices')


#print(db.execute_query("SELECT * FROM dim_product LIMIT 100"))

#df = db.execute_sql_file('query1.sql')
#print(df)