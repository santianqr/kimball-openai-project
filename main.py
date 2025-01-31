from src import db, processor, model, loader, generator

print('🟢Starting ETL process')

# Define the file path for the raw data
file_path = "data/raw/Invoices_Year_2009-2010.csv"

# Clean and process the raw data
df = processor.process_data(file_path)

# Create the table invoices in PostgreSQL
db.upsert_table(df, "invoices")

# Execute a base SQL query and get the data to provide to the model
df_clean = db.execute_sql_file("src/utils/queries/base_query.sql")

# Generate the data model from the data (Kimball model)
dim_product, dim_customer, dim_date, dim_country, fact_sales = model.generate_model(
    df_clean
)

# Upload the generated data model to PostgreSQL
loader.upload_model(dim_product, dim_customer, dim_date, dim_country, fact_sales)

print('🟢ETL process completed')

print("🕒Now the aggregations of data, detailed comments on each file of queries")
# Aggregations 
df_agg_1 = db.execute_sql_file("src/utils/queries/growth_yoy_by_country.sql")
print("First aggregation of data")
print(df_agg_1)
df_agg_2 = db.execute_sql_file("src/utils/queries/cohort_analysis.sql")
print("Second aggregation of data")
print(df_agg_2)
df_agg_3 = db.execute_sql_file("src/utils/queries/classification_products.sql")
print("Third aggregation of data")
print(df_agg_3)


print("⚠️Now try the generator with some queries, the generator use the data from the database")
# BETA MODE: Generate the table from input of the user
# try: "top 10 products sold in December 2009"
user_query = "top 10 products sold in December 2009"
df_generated = generator.generate_table(user_query)
print(df_generated)


# print(db.execute_query("select table_name from information_schema.tables where table_schema='public'"))
