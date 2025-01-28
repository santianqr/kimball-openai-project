import pandas as pd

class model:
    
    @staticmethod
    def create_dim_product(df):
        dim_product = df[['StockCode', 'Description']].drop_duplicates().reset_index(drop=True)
        dim_product['ProductKey'] = dim_product.index + 1
        return dim_product[['ProductKey', 'StockCode', 'Description']]

    @staticmethod
    def create_dim_customer(df):
        dim_customer = df[['Customer ID', 'Country']].drop_duplicates().reset_index(drop=True)
        dim_customer['CustomerKey'] = dim_customer.index + 1
        return dim_customer[['CustomerKey', 'Customer ID', 'Country']]

    @staticmethod
    def create_dim_date(df):
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
        dim_date = df[['InvoiceDate']].drop_duplicates().reset_index(drop=True)
        dim_date['DateKey'] = dim_date.index + 1
        dim_date['Year'] = dim_date['InvoiceDate'].dt.year
        dim_date['Month'] = dim_date['InvoiceDate'].dt.month
        dim_date['Day'] = dim_date['InvoiceDate'].dt.day
        dim_date['Weekday'] = dim_date['InvoiceDate'].dt.weekday
        return dim_date[['DateKey', 'InvoiceDate', 'Year', 'Month', 'Day', 'Weekday']]

    @staticmethod
    def create_fact_sales(df, dim_product, dim_customer, dim_date):
        fact_sales = df.copy()
        # Merge with dimensions
        fact_sales = fact_sales.merge(dim_product, on=['StockCode', 'Description'], how='left')
        fact_sales = fact_sales.merge(dim_customer, on=['Customer ID', 'Country'], how='left')
        fact_sales = fact_sales.merge(dim_date, on=['InvoiceDate'], how='left')
        # Add calculated field
        fact_sales['TotalPrice'] = fact_sales['Quantity'] * fact_sales['Price']
        return fact_sales[['Invoice', 'ProductKey', 'CustomerKey', 'DateKey', 'Quantity', 'Price', 'TotalPrice']]

    @staticmethod
    def generate_model(df):
        dim_product = model.create_dim_product(df)
        dim_customer = model.create_dim_customer(df)
        dim_date = model.create_dim_date(df)
        fact_sales = model.create_fact_sales(df, dim_product, dim_customer, dim_date)
        return dim_product, dim_customer, dim_date, fact_sales
