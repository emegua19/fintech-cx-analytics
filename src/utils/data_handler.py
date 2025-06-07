import pandas as pd
import os

class DataHandler:
    def __init__(self):
        """Initialize DataHandler for CSV operations."""
        pass

    def read_csv(self, path):
        """Read CSV file into a DataFrame."""
        try:
            df = pd.read_csv(path, encoding='utf-8')
            print(f"Loaded CSV from {path} ({len(df)} rows).")
            return df
        except Exception as e:
            print(f"Error reading {path}: {e}")
            return pd.DataFrame(columns=['review', 'rating', 'date', 'bank', 'source'])

    def write_csv(self, df, path):
        """Write DataFrame to CSV file."""
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            df.to_csv(path, index=False, encoding='utf-8')
            print(f"Saved CSV to {path} ({len(df)} rows).")
            return True
        except Exception as e:
            print(f"Error writing to {path}: {e}")
            return False
