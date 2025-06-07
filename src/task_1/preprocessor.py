import pandas as pd
import re
from src.utils.data_handler import DataHandler

class Preprocessor:
    def __init__(self, data_handler):
        """Initialize Preprocessor with DataHandler."""
        self.data_handler = data_handler

    def load_data(self, input_paths):
        """Load raw review data from multiple CSV files."""
        dfs = []
        for path in input_paths:
            df = self.data_handler.read_csv(path)
            if not df.empty:
                dfs.append(df)
        if dfs:
            return pd.concat(dfs, ignore_index=True)
        return pd.DataFrame(columns=['review', 'rating', 'date', 'bank', 'source'])

    def clean_data(self, df):
        """Preprocess reviews: remove duplicates, handle missing data, normalize."""
        # Create a copy to avoid modifying the original
        df = df.copy()

        # Handle missing data
        df.loc[:, 'review'] = df['review'].fillna('').astype(str)
        df.loc[:, 'rating'] = df['rating'].fillna(0).astype(int)
        df.loc[:, 'bank'] = df['bank'].fillna('Unknown')
        df.loc[:, 'source'] = df['source'].fillna('Google Play')

        # Normalize review text for duplicate detection (lowercase, strip, preserve Amharic)
        df.loc[:, 'review_normalized'] = df['review'].apply(
            lambda x: re.sub(r'[^\w\s\u1200-\u137F]', '', x.lower().strip()) if x else ''
        )

        # Normalize bank for consistency
        df.loc[:, 'bank'] = df['bank'].str.lower().str.strip()

        # Remove duplicates based on normalized review, date, and bank
        df = df.drop_duplicates(subset=['review_normalized', 'date', 'bank'], keep='first')

        # Update review column with normalized text
        df.loc[:, 'review'] = df['review_normalized']

        # Drop temporary normalized column
        df = df.drop(columns=['review_normalized'])

        # Normalize dates
        df.loc[:, 'date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%Y-%m-%d')

        return df

    def save_cleaned_data(self, df, output_path='data/processed/bank_reviews_cleaned.csv'):
        """Save cleaned DataFrame to CSV."""
        self.data_handler.write_csv(df, output_path)
        print(f"Saved {len(df)} cleaned reviews to {output_path}")
        return True

    def main(self):
        """Run the preprocessing pipeline for bank reviews."""
        # Define input CSV paths
        input_paths = [
            'data/raw/commercial_bank_of_ethiopia_reviews_raw.csv',
            'data/raw/bank_of_abyssinia_reviews_raw.csv',
            'data/raw/dashen_bank_reviews_raw.csv'
        ]

        # Load raw data
        print("Loading raw review data...")
        df = self.load_data(input_paths)
        if df.empty:
            print("Error: No data loaded from input CSVs.")
            return False

        # Print sample raw data
        print("\nRaw Data Sample (first 5 rows):\n")
        print(df.head().to_string())
        print("\n")

        # Clean data
        print("Cleaning data...")
        cleaned_df = self.clean_data(df)
        if cleaned_df.empty:
            print("Error: No data after cleaning.")
            return False

        # Print sample cleaned data
        print("\nCleaned Data Sample (first 5 rows):\n")
        print(cleaned_df.head().to_string())
        print("\n")

        # Save cleaned data
        output_path = 'data/processed/bank_reviews_cleaned.csv'
        print("Saving cleaned data...")
        success = self.save_cleaned_data(cleaned_df, output_path)
        if success:
            print(f"Preprocessing complete. Output saved to {output_path}")
            return True
        else:
            print("Error: Failed to save cleaned data.")
            return False

if __name__ == "__main__":
    data_handler = DataHandler()
    preprocessor = Preprocessor(data_handler)
    preprocessor.main()