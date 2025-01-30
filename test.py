from src import db, processor, model, loader
import pandas as pd

file_path = 'data/raw/Invoices_Year_2009-2010.csv'

#df = processor.process_data(file_path)
#print(df.head(5))

#df = db.execute_query("SELECT * FROM dim_product where stock_code ilike '%?%'")
#print("Data from database")
#print(df)


#dim_product, dim_customer, dim_date, dim_country, fact_sales  = model.generate_model(df)
#print(dim_product)

#loader.upload_model(dim_product, dim_customer, dim_date, dim_country, fact_sales)
#print(db.execute_query("SELECT * FROM invoices LIMIT 100"))

df = db.execute_sql_file('src/utils/queries/retention_client.sql')
print(df)