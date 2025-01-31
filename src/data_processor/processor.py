import pandas as pd
import chardet


class DataProcessor:
    """
    A utility class for detecting file encoding, loading, and cleaning data.
    """

    @staticmethod
    def _detect_encoding(file_path: str) -> str:
        """
        Detects the encoding of a given file.

        Args:
            file_path (str): Path to the file.

        Returns:
            str: The detected encoding type.
        """
        try:
            print("Detecting encoding")
            with open(file_path, "rb") as rawdata:
                result = chardet.detect(rawdata.read(100000))

            if result["encoding"] == "ascii" or result["confidence"] < 0.9:
                return "latin1"
            return result["encoding"]
        except Exception as e:
            raise ValueError(f"❌ Error detecting file encoding: {e}")

    @staticmethod
    def _load_data(file_path: str) -> pd.DataFrame:
        """
        Loads a CSV file into a DataFrame, ensuring proper encoding detection.

        Args:
            file_path (str): Path to the CSV file.

        Returns:
            pd.DataFrame: Loaded data.
        """
        try:
            encoding_to_use = DataProcessor._detect_encoding(file_path)
            print(f"Encoding to use: {encoding_to_use}")
            return pd.read_csv(
                file_path,
                encoding=encoding_to_use,
                dtype={"Customer ID": str},
                low_memory=False,
            )
        except Exception as e:
            raise ValueError(f"❌ Error loading data from file: {e}")

    @staticmethod
    def _clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans a DataFrame by removing duplicates, filtering invalid entries,
        and standardizing data types.

        Args:
            df (pd.DataFrame): Raw data.

        Returns:
            pd.DataFrame: Cleaned data.
        """
        if df is None or df.empty:
            raise ValueError("❌ DataFrame is empty. Provide a valid DataFrame.")

        try:
            print("🗄️ Data to be proccesed:")
            print(df.head())
            # Remove duplicates
            print("Removing duplicates")
            df.drop_duplicates(inplace=True)

            # Remove test entries
            print("Removing test entries")
            df = df[
                ~df["Customer ID"]
                .astype(str)
                .str.contains("TEST", case=False, na=False)
            ]
            df = df[
                ~df["StockCode"].astype(str).str.contains("TEST", case=False, na=False)
            ]

            # Fill missing values
            print("Filling missing values")
            df["Price"].fillna(0, inplace=True)
            df["Country"].fillna("No country", inplace=True)
            df["Description"].fillna("No description", inplace=True)
            df["Customer ID"].fillna(999999999, inplace=True)

            # Remove invalid entries
            print("Removing invalid entries like price < 0")
            df = df[
                ~df["StockCode"].astype(str).str.match(r"^[^a-zA-Z0-9]+$", na=False)
            ]
            df = df[df["Price"] >= 0]

            # Ensure correct data types
            print("Ensuring correct data types")
            df["Invoice"] = df["Invoice"].astype(str)
            df["StockCode"] = df["StockCode"].astype(str)
            df["Description"] = df["Description"].astype(str)
            df["Quantity"] = df["Quantity"].astype(int)
            df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
            df["Price"] = df["Price"].astype(float)
            df["Customer ID"] = df["Customer ID"].astype(int)
            df["Country"] = df["Country"].astype(str)

            return df
        except Exception as e:
            raise ValueError(f"❌ Error cleaning data: {e}")

    @staticmethod
    def process_data(file_path: str) -> pd.DataFrame:
        """
        Loads and cleans data from a CSV file.

        Args:
            file_path (str): Path to the CSV file.

        Returns:
            pd.DataFrame: Processed data.
        """
        try:
            df = DataProcessor._load_data(file_path)
            return DataProcessor._clean_data(df)
        except Exception as e:
            raise ValueError(f"❌ Error processing data: {e}")
