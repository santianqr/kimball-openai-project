import pytest
import pandas as pd
from src import model


@pytest.fixture
def sample_data():
    data = {
        "Invoice": ["489434", "489435"],
        "StockCode": ["85048", "79323P"],
        "Description": ["15CM CHRISTMAS GLASS BALL 20 LIGHTS", "PINK CHERRY LIGHTS"],
        "Quantity": [12, 12],
        "InvoiceDate": ["12/01/2009 07:45", "12/01/2009 07:46"],
        "Price": [6.95, 6.75],
        "Customer ID": [13085, 13086],
        "Country": ["United Kingdom", "United Kingdom"],
    }
    df = pd.DataFrame(data)
    return df


def test_data_model(sample_data):
    df = sample_data.rename(
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

    dim_product = model.create_dim_product(df)
    dim_customer = model.create_dim_customer(df)
    dim_date = model.create_dim_date(df)
    dim_country = model.create_dim_country(df)
    fact_sales = model.create_fact_sales(
        df, dim_product, dim_customer, dim_date, dim_country
    )

    assert dim_product is not None
    assert dim_customer is not None
    assert dim_date is not None
    assert dim_country is not None
    assert fact_sales is not None
