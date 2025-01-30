from src import db, processor, model, loader, generator
import pandas as pd

# Define the file path for the raw data
file_path = 'data/raw/Invoices_Year_2009-2010.csv'

# Clean and process the raw data
df = processor.process_data(file_path)

# Create the table invoices in PostgreSQL
db.upsert_table(df, 'invoices')

# Execute a base SQL query and get the data to provide to the model
df_raw = db.execute_sql_file('src/utils/queries/base_query.sql')

# Generate the data model from the data (Kimball model)
dim_product, dim_customer, dim_date, dim_country, fact_sales = model.generate_model(df_raw)

# Upload the generated data model to PostgreSQL
loader.upload_model(dim_product, dim_customer, dim_date, dim_country, fact_sales)

# BETA MODE: Generate the table from input of the user
generator.generate_table("top 10 productos mas vendidos en diciembre 2009")