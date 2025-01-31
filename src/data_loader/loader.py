from src.utils import db
import pandas as pd


class DataLoader:
    """
    A utility class to upload data tables to PostgreSQL.
    """

    @staticmethod
    def upload_model(
        dim_product: pd.DataFrame,
        dim_customer: pd.DataFrame,
        dim_date: pd.DataFrame,
        dim_country: pd.DataFrame,
        fact_sales: pd.DataFrame,
    ) -> str:
        """
        Uploads multiple data tables to PostgreSQL.

        Args:
            dim_product (pd.DataFrame): Data for the dim_product table.
            dim_customer (pd.DataFrame): Data for the dim_customer table.
            dim_date (pd.DataFrame): Data for the dim_date table.
            dim_country (pd.DataFrame): Data for the dim_country table.
            fact_sales (pd.DataFrame): Data for the fact_sales table.

        Returns:
            str: Success or error message.
        """
        try:
            
            db.upsert_table(dim_product, "dim_product")
            print("✅ dim_product table uploaded successfully.")
            db.upsert_table(dim_customer, "dim_customer")
            print("✅ dim_customer table uploaded successfully.")
            db.upsert_table(dim_date, "dim_date")
            print("✅ dim_date table uploaded successfully.")
            db.upsert_table(dim_country, "dim_country")
            print("✅ dim_country table uploaded successfully.")
            print("🕒 Creating the fact_sales table, be patient")
            db.upsert_table(fact_sales, "fact_sales")
            print("✅ fact_sales table uploaded successfully.")

            return (
                "✅ Data upload successful: All tables have been loaded into PostgreSQL."
            )
        except Exception as e:
            return f"❌ Error uploading data to PostgreSQL: {str(e)}"
