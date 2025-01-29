from src import db, processor, model
import pandas as pd

file_path = 'data/raw/Invoices_Year_2009-2010.csv'

#df = processor.process_data(file_path)
#print(df.head(5))
#df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

df = db.execute_query("SELECT * FROM invoices LIMIT 100")
print("Data from database")
print(df)

dim_product, dim_customer, dim_date, dim_country, fact_sales  = model.generate_model(df)
print(dim_product)

#db.upsert_table(df, 'invoices')