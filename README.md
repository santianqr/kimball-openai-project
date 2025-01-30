# Betsson Project

## Project Documentation

### Overview
This project is a test for a data engineer position at Betsson. The goal is to process and clean the provided dataset to ensure data quality and consistency.

### Assumptions and Considerations
- **Negative Quantities**: Negative values in the `Quantity` column are assumed to be returns.
- **Negative Prices**: Negative values in the `Price` column are considered errors and have been cleaned.
- **Invoice and Stock Code**: The `Invoice` and `StockCode` columns are assumed to contain alphanumeric codes.
- **Test Data**: Test data entries have been identified and removed from the dataset.
- **Missing Descriptions or Countries**: Entries with missing `Description` or `Country` values have been set to "No description" and "No country" respectively.
- **Null Customer IDs**: Null values in the `Customer ID` column have been set to `999999999` to check for patterns later.
- **Null Prices**: Null values in the `Price` column have been set to `0`.
- **Invalid Stock Codes**: Entries with invalid stock codes such as `?` have been excluded from the dataset.

### Anomalies
- Negative quantities indicating returns.
- Negative prices considered as errors.
- Alphanumeric codes in `Invoice` and `StockCode`.
- Presence of test data.
- Missing descriptions, countries, and customer IDs.
- Null prices.
- Invalid stock codes.

### Data Cleaning Actions
- Removed entries with negative prices.
- Set missing descriptions and countries to "No description" and "No country".
- Set null customer IDs to `999999999`.
- Set null prices to `0`.
- Excluded entries with invalid stock codes.

### Directory Structure

BetssonProject/
├── .gitattributes
├── .gitignore
├── .pytest_cache/
│   ├── .gitignore
│   ├── CACHEDIR.TAG
│   └── v/
│       └── cache/
├── config.yaml
├── creds/
│   ├── __init__.py
│   ├── __pycache__/
│   └── creds.py
├── data/
│   ├── other/
│   └── raw/
│       └── ...
├── main.py
├── notebooks/
│   └── exploration.ipynb
├── README.md
├── requirements.txt
├── run.py
├── src/
│   ├── __init__.py
│   ├── __pycache__/
│   ├── data_loader/
│   │   ├── __init__.py
│   │   └── load_data.py
│   ├── data_modeling/
│   │   └── generate_model.py
│   ├── data_processor/
│   │   ├── __init__.py
│   │   └── process_data.py
│   ├── nlp_generator/
│   │   └── generate_table.py
│   └── utils/
│       ├── __init__.py
│       └── queries/
│           ├── base_query.sql
│           └── classification_products.sql
└── tests/
    ├── __init__.py
    ├── __pycache__/
    ├── data_modeling/
    │   └── test_modeling.py
    ├── data_processor/
    │   └── test_processor.py
    └── database/
        └── test_db.py
