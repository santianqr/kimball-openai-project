import pandas as pd
import chardet


class processor:

    @staticmethod
    def detect_encoding(file_path):
        with open(file_path, "rb") as rawdata:
            result = chardet.detect(rawdata.read(100000))
        if result["encoding"] == "ascii" or result["confidence"] < 0.9:
            return "latin1"
        return result["encoding"]

    @staticmethod
    def load_data(file_path):
        encoding_to_use = processor.detect_encoding(file_path)
        return pd.read_csv(file_path, encoding=encoding_to_use)

    @staticmethod
    def clean_data(df):
        if df is None or df.empty:
            raise ValueError("DataFrame is empty. Provide a valid DataFrame.")

        df.drop_duplicates(inplace=True)

        df = df[~df["Customer ID"].astype(str).str.contains("TEST", case=False, na=False)]
        df = df[~df["StockCode"].astype(str).str.contains("TEST", case=False, na=False)]

        df["Price"].fillna(0, inplace=True)
        df["Country"].fillna("No country", inplace=True)
        df["Description"].fillna("No description", inplace=True)
        df["Customer ID"].fillna(999999999, inplace=True)
        
        df = df[~df["StockCode"].astype(str).str.match(r"^[^a-zA-Z0-9]+$", na=False)]
        df = df[df["Price"] >= 0]

        df["Invoice"] = df["Invoice"].astype(str)
        df["StockCode"] = df["StockCode"].astype(str)
        df["Description"] = df["Description"].astype(str)
        df["Quantity"] = df["Quantity"].astype(int)
        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
        df["Price"] = df["Price"].astype(float)
        df["Customer ID"] = df["Customer ID"].astype(int)
        df["Country"] = df["Country"].astype(str)

        return df

    @staticmethod
    def process_data(file_path):
        df = processor.load_data(file_path)
        return processor.clean_data(df)
