import pandas as pd


class DataModel:
    """
    A utility class for creating a Data warehouse Kimball Model with dimension and fact tables from raw sales data.
    """

    @staticmethod
    def create_dim_product(df: pd.DataFrame) -> pd.DataFrame:
        """
        Creates the product dimension table.

        Args:
            df (pd.DataFrame): Raw sales data.

        Returns:
            pd.DataFrame: Dimension table for products.
        """
        dim_product = (
            df[["stock_code", "description"]].drop_duplicates().reset_index(drop=True)
        )
        dim_product["product_id"] = dim_product.index + 1
        return dim_product[["product_id", "stock_code", "description"]]

    @staticmethod
    def create_dim_customer(df: pd.DataFrame) -> pd.DataFrame:
        """
        Creates the customer dimension table.

        Args:
            df (pd.DataFrame): Raw sales data.

        Returns:
            pd.DataFrame: Dimension table for customers.
        """
        dim_customer = (
            df[["customer_id", "country"]].drop_duplicates().reset_index(drop=True)
        )
        dim_customer["customer_id"] = dim_customer.index + 1
        return dim_customer[["customer_id", "country"]]

    @staticmethod
    def create_dim_date(df: pd.DataFrame) -> pd.DataFrame:
        """
        Creates the date dimension table.

        Args:
            df (pd.DataFrame): Raw sales data.

        Returns:
            pd.DataFrame: Dimension table for dates.
        """
        df["invoice_date"] = pd.to_datetime(df["invoice_date"])
        dim_date = df[["invoice_date"]].drop_duplicates().reset_index(drop=True)
        dim_date["date_id"] = dim_date.index + 1
        dim_date["year"] = dim_date["invoice_date"].dt.year
        dim_date["month"] = dim_date["invoice_date"].dt.month
        dim_date["day"] = dim_date["invoice_date"].dt.day
        dim_date["weekday"] = dim_date["invoice_date"].dt.weekday
        return dim_date[["date_id", "invoice_date", "year", "month", "day", "weekday"]]

    @staticmethod
    def create_dim_country(df: pd.DataFrame) -> pd.DataFrame:
        """
        Creates the country dimension table.

        Args:
            df (pd.DataFrame): Raw sales data.

        Returns:
            pd.DataFrame: Dimension table for countries.
        """
        dim_country = df[["country"]].drop_duplicates().reset_index(drop=True)
        dim_country["country_id"] = dim_country.index + 1
        return dim_country[["country_id", "country"]]

    @staticmethod
    def create_fact_sales(
        df: pd.DataFrame,
        dim_product: pd.DataFrame,
        dim_customer: pd.DataFrame,
        dim_date: pd.DataFrame,
        dim_country: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Creates the fact sales table by merging with dimension tables.

        Args:
            df (pd.DataFrame): Raw sales data.
            dim_product (pd.DataFrame): Product dimension table.
            dim_customer (pd.DataFrame): Customer dimension table.
            dim_date (pd.DataFrame): Date dimension table.
            dim_country (pd.DataFrame): Country dimension table.

        Returns:
            pd.DataFrame: Fact sales table.
        """
        fact_sales = df.copy()
        fact_sales = fact_sales.merge(
            dim_product, on=["stock_code", "description"], how="left"
        )
        fact_sales = fact_sales.merge(
            dim_customer, on=["customer_id", "country"], how="left"
        )
        fact_sales = fact_sales.merge(dim_date, on=["invoice_date"], how="left")
        fact_sales = fact_sales.merge(dim_country, on=["country"], how="left")
        fact_sales["total_price"] = fact_sales["quantity"] * fact_sales["unit_price"]
        return fact_sales[
            [
                "invoice",
                "product_id",
                "customer_id",
                "date_id",
                "country_id",
                "quantity",
                "unit_price",
                "total_price",
            ]
        ]

    @staticmethod
    def generate_model(df: pd.DataFrame) -> tuple:
        """
        Processes raw sales data to create dimension tables and a fact sales table.

        Args:
            df (pd.DataFrame): Raw sales data.

        Returns:
            tuple: (dim_product, dim_customer, dim_date, dim_country, fact_sales)
        """
        df = df.rename(
            columns={
                "Invoice": "invoice",
                "StockCode": "stock_code",
                "Description": "description",
                "Quantity": "quantity",
                "InvoiceDate": "invoice_date",
                "Price": "unit_price",
                "Customer ID": "customer_id",
                "Country": "country",
            }
        )

        dim_product = DataModel.create_dim_product(df)
        print("✅ Product Dimension Table Created:")
        print(dim_product.head(5))

        dim_customer = DataModel.create_dim_customer(df)
        print("✅ Customer Dimension Table Created:")
        print(dim_customer.head(5))

        dim_date = DataModel.create_dim_date(df)
        print("✅ Date Dimension Table Created:")
        print(dim_date.head(5))

        dim_country = DataModel.create_dim_country(df)
        print("✅ Country Dimension Table Created:")
        print(dim_country.head(5))

        fact_sales = DataModel.create_fact_sales(
            df, dim_product, dim_customer, dim_date, dim_country
        )
        print("✅ Fact Sales Table Created:")
        print(fact_sales.head(5))

        return dim_product, dim_customer, dim_date, dim_country, fact_sales
