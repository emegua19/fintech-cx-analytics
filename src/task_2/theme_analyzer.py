import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import os

class ThemeAnalyzer:
    def __init__(self, input_path='data/processed/bank_reviews_cleaned.csv'):
        self.input_path = input_path
        self.df = pd.DataFrame()

        # Define keyword groups manually for now
        self.theme_keywords = {
            "Account Access Issues": ["login", "log in", "sign in", "password", "access", "cannot login", "login failed", "authentication"],
            "Transaction Performance": ["transfer", "transaction", "delay", "processing", "send money", "receive", "failed transfer", "deposit", "withdraw"],
            "User Interface & Experience": ["app", "interface", "easy to use", "navigation", "crash", "bug", "slow", "responsive", "design"],
            "Customer Support": ["support", "help", "customer service", "no response", "call center", "contact", "agent", "feedback"],
            "Feature Requests": ["add feature", "would like", "suggestion", "need", "wish", "option", "upgrade", "additional"]
        }

    def load_data(self):
        try:
            df = pd.read_csv(self.input_path, encoding='utf-8')
            df = df[df['language'].isin(['english', 'bilingual'])]
            print(f"Loaded {len(df)} reviews for Thematic Analysis.")
            self.df = df
            return df
        except FileNotFoundError:
            print(f"Error: File {self.input_path} not found.")
            return pd.DataFrame()

    def extract_keywords_per_bank(self, top_n=20):
        """Extract and categorize TF-IDF keywords per bank."""
        results = {}
        for bank in self.df['bank'].unique():
            print(f"\n--- Extracting keywords for {bank} ---\n")
            bank_reviews = self.df[self.df['bank'] == bank]['review']

            tfidf = TfidfVectorizer(
                max_features=100,
                stop_words='english',
                ngram_range=(1, 3)
            )
            X = tfidf.fit_transform(bank_reviews)
            feature_names = tfidf.get_feature_names_out()
            scores = X.sum(axis=0).A1
            sorted_items = sorted(zip(scores, feature_names), reverse=True)

            top_keywords = [(word, round(score, 2)) for score, word in sorted_items[:top_n]]
            themed_keywords = self.group_keywords_by_theme(top_keywords)

            results[bank] = themed_keywords

            print(f"Grouped Themes for {bank}:")
            for theme, words in themed_keywords.items():
                print(f"\n{theme}:")
                for word, score in words:
                    print(f"  {word}: {score}")

        return results

    def group_keywords_by_theme(self, keywords):
        """Group keywords under predefined themes."""
        theme_map = {theme: [] for theme in self.theme_keywords.keys()}
        theme_map["Other"] = []

        for word, score in keywords:
            matched = False
            for theme, theme_words in self.theme_keywords.items():
                if any(k in word.lower() for k in theme_words):
                    theme_map[theme].append((word, score))
                    matched = True
                    break
            if not matched:
                theme_map["Other"].append((word, score))
        return theme_map

    def save_keywords(self, results, output_dir='data/analysis'):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for bank, theme_data in results.items():
            rows = []
            for theme, keywords in theme_data.items():
                for word, score in keywords:
                    rows.append({'theme': theme, 'keyword': word, 'score': score})
            df_keywords = pd.DataFrame(rows)
            file_name = f"{bank.lower().replace(' ', '_')}_themes_grouped.csv"
            output_path = os.path.join(output_dir, file_name)
            df_keywords.to_csv(output_path, index=False, encoding='utf-8')
            print(f"Saved themed keywords for {bank} to {output_path}")

    def run_pipeline(self):
        print("Loading data...")
        df = self.load_data()
        if df.empty:
            print("Error: No data to process.")
            return False

        print("Extracting and grouping keywords...")
        grouped_results = self.extract_keywords_per_bank()

        print("Saving results...")
        self.save_keywords(grouped_results)

        print("\n--- Thematic Analysis completed. ---")
        return True
