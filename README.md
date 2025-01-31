# Project Documentation

### Overview
This project is a test for a Data Engineer position at Betsson. The objective is to build a Kimball Model from raw invoice data spanning 2009 to 2010. The project involves data cleaning, transformation, and aggregation, adhering to best practices in data engineering.

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

### Environment Variables

This project uses OpenAI and Amazon RDS PostgreSQL. The environment variables required for these services are stored in the `config.yaml` file. Note that these variables have a validity period of 1 month.

### Project Structure

```plaintext
BetssonProject/
├── .gitattributes
├── .gitignore
├── .pytest_cache/
│   ├── .gitignore
│   ├── CACHEDIR.TAG
│   └── README.md
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
│   │   └── loader.py
│   ├── data_modeling/
│   │   └── model.py
│   ├── data_processor/
│   │   ├── __init__.py
│   │   └── process_data.py
│   ├── nlp_generator/
│   │   └── generate_table.py
│   └── utils/
│       ├── __init__.py
│       └── queries/
│           ├── base_query.sql
│           ├── classification_products.sql
│           ├── cohort_analysis.sql
│           ├── growth_yoy_by_country.sql
│           └── testing_query.sql
└── tests/
    ├── __init__.py
    ├── __pycache__/
    ├── data_modeling/
    │   └── test_model.py
    ├── data_processor/
    │   └── test_processor.py
    └── database/
        └── test_db.py
```

### Notebooks
- **[notebooks/exploration.ipynb](notebooks/exploration.ipynb)**: Contains exploratory data analysis and data cleaning steps.

### Scripts
- **[main.py](main.py)**: Main script to run the project.
- **[run.py](run.py)**: Script to execute the project.

### Configuration
- **[config.yaml](config.yaml)**: Configuration file for the project and credentials.

### Requirements
- **[requirements.txt](requirements.txt)**: List of dependencies required for the project.

### Virtual Environment
- **venv/**: Virtual environment directory.

### Tests
- **[tests/data_processor/test_processor.py](tests/data_processor/test_processor.py)**: Contains tests for the data processing functions.
- **[tests/data_modeling/test_model.py](tests/data_modeling/test_model.py)**: Contains tests for the data warehouse kimball model.
- **[tests/database/test_db.py](tests/database/test_db.py)**: Contains tests for the database functions.

### Data Processing
- **[src/data_processor](src/data_processor)**: Contains the data processing/cleaning logic.
  - **[src/data_processor/process_data.py](src/data_processor/process_data.py)**: Main data processing functions.

### Data Loading
- **[src/data_loader](src/data_loader)**: Contains the data loading logic.
  - **[src/data_loader/loader.py](src/data_loader/loader.py)**: Class to upload the dataframes generated from the Kimball model to PostgreSQL.

### Kimball Model Generation
- **[src/data_modeling/model.py](src/data_modeling/model.py)**: Contains the class to generate a Kimball model from raw data.
  - **Class `KimballModel`**: This class takes a raw data DataFrame and applies transformations to create a Kimball data warehouse model.

### NLP Generation
- **[src/nlp_generator](src/nlp_generator)**: Contains the NLP generation logic.
  - **[src/nlp_generator/generate_table.py](src/nlp_generator/generate_table.py)**: Contains the `NLPGenerator` class.
    - **Class `NLPGenerator`**: This class takes natural language input and internally generates queries based on the loaded Kimball model, returning a DataFrame.

### Utilities
- **[src/utils](src/utils)**: Contains utility functions to database management and SQL queries to uso.
  - **[src/utils/queries](src/utils/queries)**: Contains SQL query files with it owns comments.

### Running the Project

To run the project, follow these steps:

1. **Ensure Python is Installed**: Make sure you have Python 3.8 or higher installed on your system.

2. **Install Dependencies**: Install the required dependencies using the following command:

  ```sh
  pip install -r requirements.txt
  ```

  Alternatively, you can install them manually:

  ```sh
  pip install pandas==2.1.1 numpy==1.26.0 psycopg2-binary==2.9.9 pyyaml==6.0.1 chardet==5.2.0 sqlalchemy==2.0.21 langchain-openai pytest black==23.3.0
  ```

3. **Run the Project**: You can run the project using one of the following options:

  - Execute the `run.py` script:

    ```sh
    python run.py
    ```

  - Run the `main.py` script:

    ```sh
    python main.py
    ```

  - Open and execute the main Jupyter Notebook `main_notebook.ipynb`.