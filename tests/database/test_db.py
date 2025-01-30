import pytest
import pandas as pd
from src.utils import db

@pytest.fixture
def dummy_data():
    data = {
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35]
    }
    df = pd.DataFrame(data)
    return df

def test_database_manager(dummy_data):
    # Crear la tabla test_table con datos dummy
    db.upsert_table(dummy_data, 'test_table')
    
    # Probar execute_query con SELECT * FROM test_table
    query_result = db.execute_query('SELECT * FROM test_table')
    assert query_result is not None, "El resultado de la consulta es None"
    assert not query_result.empty, "El DataFrame de resultado está vacío"
    assert list(query_result.columns) == ['id', 'name', 'age'], "Las columnas del DataFrame no son las esperadas"
    
    # Probar execute_sql_file con el archivo testing.sql
    sql_file_result = db.execute_sql_file('src/utils/queries/testing_query.sql')
    assert sql_file_result is not None, "El resultado de la consulta del archivo SQL es None"
    assert not sql_file_result.empty, "El DataFrame de resultado del archivo SQL está vacío"
    assert list(sql_file_result.columns) == ['id', 'name', 'age'], "Las columnas del DataFrame del archivo SQL no son las esperadas"

if __name__ == "__main__":
    pytest.main()