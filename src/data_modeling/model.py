import pandas as pd

class model:

    @staticmethod
    def create_dim_product(df):
        """ Crea la dimensión de productos """
        dim_product = df[['stock_code', 'description']].drop_duplicates().reset_index(drop=True)
        dim_product['product_id'] = dim_product.index + 1  # Clave primaria
        return dim_product[['product_id', 'stock_code', 'description']]

    @staticmethod
    def create_dim_customer(df):
        """ Crea la dimensión de clientes """
        dim_customer = df[['customer_id', 'country']].drop_duplicates().reset_index(drop=True)
        dim_customer['customer_id'] = dim_customer.index + 1  # Clave primaria
        return dim_customer[['customer_id', 'country']]

    @staticmethod
    def create_dim_date(df):
        """ Crea la dimensión de fechas """
        df['invoice_date'] = pd.to_datetime(df['invoice_date'])
        dim_date = df[['invoice_date']].drop_duplicates().reset_index(drop=True)
        dim_date['date_id'] = dim_date.index + 1  # Clave primaria
        dim_date['year'] = dim_date['invoice_date'].dt.year
        dim_date['month'] = dim_date['invoice_date'].dt.month
        dim_date['day'] = dim_date['invoice_date'].dt.day
        dim_date['weekday'] = dim_date['invoice_date'].dt.weekday
        return dim_date[['date_id', 'invoice_date', 'year', 'month', 'day', 'weekday']]

    @staticmethod
    def create_dim_country(df):
        """ Crea la dimensión de países """
        dim_country = df[['country']].drop_duplicates().reset_index(drop=True)
        dim_country['country_id'] = dim_country.index + 1  # Clave primaria
        return dim_country[['country_id', 'country']]

    @staticmethod
    def create_fact_sales(df, dim_product, dim_customer, dim_date, dim_country):
        """ Crea la tabla de hechos de ventas """
        fact_sales = df.copy()

        # Merge con dimensiones
        fact_sales = fact_sales.merge(dim_product, on=['stock_code', 'description'], how='left')
        fact_sales = fact_sales.merge(dim_customer, on=['customer_id', 'country'], how='left')
        fact_sales = fact_sales.merge(dim_date, on=['invoice_date'], how='left')
        fact_sales = fact_sales.merge(dim_country, on=['country'], how='left')


        # Cálculo del precio total
        fact_sales['total_price'] = fact_sales['quantity'] * fact_sales['unit_price']

        return fact_sales[['invoice', 'product_id', 'customer_id', 'date_id', 'country_id', 'quantity', 'unit_price', 'total_price']]

    @staticmethod
    def generate_model(df):
        """ Renombra columnas y genera todas las dimensiones y la tabla de hechos """
        # Renombrar las columnas para estandarizar
        df = df.rename(columns={
            'Invoice': 'invoice',
            'StockCode': 'stock_code',
            'Description': 'description',
            'Quantity': 'quantity',
            'InvoiceDate': 'invoice_date',
            'Price': 'unit_price',
            'Customer ID': 'customer_id',
            'Country': 'country'
        })

        # Crear dimensiones
        dim_product = model.create_dim_product(df)
        dim_customer = model.create_dim_customer(df)
        dim_date = model.create_dim_date(df)
        dim_country = model.create_dim_country(df)

        # Crear la tabla de hechos
        fact_sales = model.create_fact_sales(df, dim_product, dim_customer, dim_date, dim_country)

        return dim_product, dim_customer, dim_date, dim_country, fact_sales
