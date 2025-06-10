import pandas as pd
import re
from langdetect import detect, LangDetectException

# Expand this list based on your real-world dataset
KNOWN_SENTIMENT_WORDS = {
    'good', 'bad', 'great', 'nice', 'love', 'hate', 'ok', 'perfect', 'poor', 'worst',
    'Top', 'best', 'cool', 'sweet', 'fast', 'week', 'slow', 'buggy', 'fake', 'messy', 'Fine',
    'Fair', 'Basic', 'አሪፍ', 'ጥሩ', 'በጣም ጥሩ', 'መልካም', 'መጥፎ', 'በጣም መጥፎ', 'ከፍተኛ', 'ምርጥ',
    'አሪፍ', 'ቀርፋፋ', 'ደካማ', 'የውሸት', 'እሺ', 'ፍትሃዊ', 'መሠረታዊ'
}

def detect_language(text):
    try:
        if not text or pd.isna(text):
            return 'unknown'

        text_clean = text.strip().lower()
        if not text_clean:
            return 'unknown'

        # If very short and not known sentiment word, ignore
        if len(text_clean) < 5 and text_clean not in KNOWN_SENTIMENT_WORDS:
            return 'unknown'

        # Check for Amharic script
        if re.search(r'[\u1200-\u137F]', text_clean):
            amharic_chars = len(re.findall(r'[\u1200-\u137F]', text_clean))
            if amharic_chars / len(text_clean) > 0.5:
                return 'amharic'
            else:
                return 'bilingual'

        # Fallback to langdetect
        lang = detect(text_clean)
        if lang == 'en':
            return 'english'
        return lang
    except LangDetectException:
        return 'unknown'


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
        """Preprocess reviews: remove duplicates, handle missing data, normalize, detect language."""
        # Create a copy
        df = df.copy()

        # Handle missing data
        df.loc[:, 'review'] = df['review'].fillna('').astype(str)
        df.loc[:, 'rating'] = df['rating'].fillna(0).astype(int)
        df.loc[:, 'bank'] = df['bank'].fillna('Unknown')
        df.loc[:, 'source'] = df['source'].fillna('Google Play')

        # Normalize review text for duplicate detection
        df.loc[:, 'review_normalized'] = df['review'].apply(
            lambda x: re.sub(r'[^\w\s\u1200-\u137F]', '', x.lower().strip()) if x else ''
        )

        # Normalize bank
        df.loc[:, 'bank'] = df['bank'].str.lower().str.strip()

        # Remove duplicates
        df = df.drop_duplicates(subset=['review_normalized', 'date', 'bank'], keep='first')

        # Update review column
        df.loc[:, 'review'] = df['review_normalized']
        df = df.drop(columns=['review_normalized'])

        # Normalize dates
        df.loc[:, 'date'] = pd.to_datetime(df['date'], errors='coerce')

        # Drop rows where date is invalid
        df = df[df['date'].notnull()]

        # Force datetime again to ensure .dt works
        df.loc[:, 'date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

        # Filter out invalid ratings (must be 1-5)
        df = df[df['rating'].between(1, 5)]

        # Detect language
        print("Detecting language...")
        df['language'] = df['review'].apply(detect_language)

        # Filter only selected languages
        df = df[df['language'].isin(['english', 'amharic', 'bilingual'])]

        # Language distribution
        print("\nLanguage distribution after filtering:")
        print(df['language'].value_counts())

        return df


    def save_cleaned_data(self, df, output_path='data/processed/bank_reviews_cleaned.csv'):
        """Save cleaned DataFrame to CSV."""
        self.data_handler.write_csv(df, output_path)
        print(f"Saved {len(df)} cleaned reviews to {output_path}")
        return True

    def main(self, output_path='data/processed/bank_reviews_cleaned.csv'):
        """Run the preprocessing pipeline for bank reviews."""
        input_paths = [
            'data/raw/commercial_bank_of_ethiopia_reviews_raw.csv',
            'data/raw/bank_of_abyssinia_reviews_raw.csv',
            'data/raw/dashen_bank_reviews_raw.csv'
        ]

        print("Loading raw review data...")
        df = self.load_data(input_paths)
        if df.empty:
            print("Error: No data loaded from input CSVs.")
            return False

        print("\nRaw Data Sample (first 5 rows):\n")
        print(df.head().to_string())
        print("\n")

        print("Cleaning data...")
        cleaned_df = self.clean_data(df)
        if cleaned_df.empty:
            print("Error: No data after cleaning.")
            return False
        
        # Print sample cleaned data with language
        print("\nCleaned Data Sample (first 5 rows including language):\n")
        print(cleaned_df[['review', 'rating', 'date', 'bank', 'source', 'language']].head().to_string())
        print("\n")

        print("Saving cleaned data...")
        success = self.save_cleaned_data(cleaned_df)
        if success:
            print(f"Preprocessing complete. Output saved to {output_path}")
            return True
        else:
            print("Error: Failed to save cleaned data.")
            return False
