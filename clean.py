import pandas as pd
import chardet

file_path = 'data/raw/Invoices_Year_2009-2010.csv'

with open(file_path, 'rb') as rawdata:
    result = chardet.detect(rawdata.read(100000))

if result['encoding'] == 'ascii' or result['confidence'] < 0.9:
    encoding_to_use = 'latin1'
else:
    encoding_to_use = result['encoding']

df = pd.read_csv(file_path, encoding=encoding_to_use)
print(df.shape[0])


df.drop_duplicates(inplace=True)

df = df[~df['Customer ID'].astype(str).str.contains('TEST', case=False, na=False)]
df = df[~df['StockCode'].astype(str).str.contains('TEST', case=False, na=False)]

df['Price'].fillna(0, inplace=True)
df = df[df['Price'] >= 0]

df['Country'].fillna('No country', inplace=True)
df['Description'].fillna('No description', inplace=True)
df['Customer ID'].fillna(999999999, inplace=True)


df['Invoice'] = df['Invoice'].astype(str)
df['StockCode'] = df['StockCode'].astype(str)

df['Description'] = df['Description'].astype(str)
df['Quantity'] = df['Quantity'].astype(int)
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
df['Price'] = df['Price'].astype(float)
df['Customer ID'] = df['Customer ID'].astype(int)
df['Country'] = df['Country'].astype(str)

print(df.shape[0])
print(df.dtypes)
print(df)
