import pandas as pd
import chardet

class CSVProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def detect_encoding(self):
        with open(self.file_path, 'rb') as rawdata:
            result = chardet.detect(rawdata.read(100000))
        if result['encoding'] == 'ascii' or result['confidence'] < 0.9:
            return 'latin1'
        return result['encoding']

    def load_data(self):
        encoding_to_use = self.detect_encoding()
        self.df = pd.read_csv(self.file_path, encoding=encoding_to_use)

    def clean_data(self):
        if self.df is None:
            raise ValueError("Data not loaded. Use load_data() before clean_data().")
        
        self.df.drop_duplicates(inplace=True)

        self.df = self.df[~self.df['Customer ID'].astype(str).str.contains('TEST', case=False, na=False)]
        self.df = self.df[~self.df['StockCode'].astype(str).str.contains('TEST', case=False, na=False)]

        self.df['Price'].fillna(0, inplace=True)
        self.df['Country'].fillna('No country', inplace=True)
        self.df['Description'].fillna('No description', inplace=True)
        self.df['Customer ID'].fillna(999999999, inplace=True)

        self.df = self.df[self.df['Price'] >= 0]

        self.df['Invoice'] = self.df['Invoice'].astype(str)
        self.df['StockCode'] = self.df['StockCode'].astype(str)
        self.df['Description'] = self.df['Description'].astype(str)
        self.df['Quantity'] = self.df['Quantity'].astype(int)
        self.df['InvoiceDate'] = pd.to_datetime(self.df['InvoiceDate'], errors='coerce')
        self.df['Price'] = self.df['Price'].astype(float)
        self.df['Customer ID'] = self.df['Customer ID'].astype(int)
        self.df['Country'] = self.df['Country'].astype(str)

    def process_csv(self):
        self.load_data()
        self.clean_data()
        return self.df
