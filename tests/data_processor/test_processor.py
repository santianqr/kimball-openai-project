import pytest
import pandas as pd
from src.data_processor.processor import DataProcessor


def test_process_data():
    file_path = "data/raw/Invoices_Year_2009-2010.csv"

    # Procesa los datos
    df = DataProcessor.process_data(file_path)

    # Verifica que el DataFrame no esté vacío
    assert not df.empty, "El DataFrame está vacío"

    # Verifica que las columnas esperadas estén presentes
    expected_columns = [
        "Invoice",
        "StockCode",
        "Description",
        "Quantity",
        "InvoiceDate",
        "Price",
        "Customer ID",
        "Country",
    ]
    assert all(
        column in df.columns for column in expected_columns
    ), "Faltan columnas en el DataFrame"

    # Verifica que no haya valores negativos en la columna 'Price'
    assert (df["Price"] >= 0).all(), "Hay valores negativos en la columna 'Price'"

    # Verifica que los tipos de datos sean correctos
    assert (
        df["Invoice"].dtype == object
    ), "El tipo de dato de la columna 'Invoice' no es str"
    assert (
        df["StockCode"].dtype == object
    ), "El tipo de dato de la columna 'StockCode' no es str"
    assert (
        df["Description"].dtype == object
    ), "El tipo de dato de la columna 'Description' no es str"
    assert (
        df["Quantity"].dtype == int
    ), "El tipo de dato de la columna 'Quantity' no es int"
    assert pd.api.types.is_datetime64_any_dtype(
        df["InvoiceDate"]
    ), "El tipo de dato de la columna 'InvoiceDate' no es datetime"
    assert (
        df["Price"].dtype == float
    ), "El tipo de dato de la columna 'Price' no es float"
    assert (
        df["Customer ID"].dtype == int
    ), "El tipo de dato de la columna 'Customer ID' no es int"
    assert (
        df["Country"].dtype == object
    ), "El tipo de dato de la columna 'Country' no es str"


if __name__ == "__main__":
    pytest.main()
