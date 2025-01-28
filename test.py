import postgre.db as tct
import pandas as pd

tct = tct.db()
df = pd.DataFrame({ 'A': [1, 2, 3], 'B': [4, 5, 6] })
print(tct.execute_query('select * from test_table'))
#tct.upsert_table(df, 'test_table')