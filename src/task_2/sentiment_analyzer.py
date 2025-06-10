import pandas as pd
from transformers import pipeline
from langdetect import detect, LangDetectException
import torch
import re

class SentimentAnalyzer:
    def __init__(self):
        """Initialize SentimentAnalyzer with DistilBERT model."""
        self.sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            device=0 if torch.cuda.is_available() else -1
        )

    def load_data(self, input_path='data/processed/bank_reviews_cleaned.csv'):
        """Load preprocessed review data from CSV."""
        try:
            df = pd.read_csv(input_path, encoding='utf-8')
            if df.empty:
                print("Warning: No data loaded from input CSV.")
                return pd.DataFrame()
            return df
        except FileNotFoundError:
            print(f"Error: File {input_path} not found.")
            return pd.DataFrame()

    def detect_language(self, df):
        """Detect language of each review, prioritizing Amharic for bilingual cases."""
        def detect_lang(text):
            try:
                if not text or pd.isna(text) or text.strip() == '' or len(text.strip()) < 5:
                    return 'unknown'
                if re.search(r'[\u1200-\u137F]', text):
                    return 'bilingual' if len(re.sub(r'[^\u1200-\u137F]', '', text)) < len(text) * 0.5 else 'amharic'
                lang = detect(text)
                if lang == 'en':
                    return 'english'
                return lang
            except LangDetectException:
                return 'unknown'

        df['language'] = df['review'].apply(detect_lang)
        return df

    def sentiment_analysis(self, df):
        """Compute sentiment scores and categorize as positive, negative, or neutral."""
        def get_sentiment(text):
            if not text or pd.isna(text) or text.strip() == '':
                return {'label': 'neutral', 'score': 0.0}
            try:
                result = self.sentiment_pipeline(
                    text[:512],
                    clean_up_tokenization_spaces=False  # ✅ Fix for future transformers versions
                )[0]
                score = result['score'] if result['label'] == 'POSITIVE' else -result['score']
                label = 'positive' if score > 0.1 else 'negative' if score < -0.1 else 'neutral'
                return {'label': label, 'score': score}
            except Exception as e:
                print(f"Sentiment error for English text '{text[:50]}...': {e}")
                return {'label': 'neutral', 'score': 0.0}

        def get_amharic_sentiment(text):
            positive_words = ['ጥሩ', 'አሪፍ', 'በጣም ጥሩ', 'ተደሰትኩ', 'አመሰግናለሁ']
            negative_words = ['መጥፎ', 'አይሰራም', 'ችግር', 'ተስፋ ቆሟል', 'ቅሬታ']
            pos_count = sum(word in text for word in positive_words)
            neg_count = sum(word in text for word in negative_words)

            if pos_count > neg_count:
                return {'label': 'positive', 'score': 0.7}
            elif neg_count > pos_count:
                return {'label': 'negative', 'score': -0.7}
            else:
                return {'label': 'neutral', 'score': 0.0}

        df['sentiment_label'] = 'neutral'
        df['sentiment_score'] = 0.0

        english_mask = df['language'] == 'english'
        if english_mask.any():
            results = df.loc[english_mask, 'review'].apply(get_sentiment)
            df.loc[english_mask, 'sentiment_label'] = results.apply(lambda x: x['label'])
            df.loc[english_mask, 'sentiment_score'] = results.apply(lambda x: x['score'])
            print(f"Processed sentiment for {english_mask.sum()} English reviews.")

        amharic_mask = df['language'].isin(['amharic', 'bilingual'])
        if amharic_mask.any():
            results = df.loc[amharic_mask, 'review'].apply(get_amharic_sentiment)
            df.loc[amharic_mask, 'sentiment_label'] = results.apply(lambda x: x['label'])
            df.loc[amharic_mask, 'sentiment_score'] = results.apply(lambda x: x['score'])
            print(f"Processed sentiment for {amharic_mask.sum()} Amharic/Bilingual reviews.")

        return df

    def aggregate_sentiment(self, df):
        """Aggregate sentiment scores by bank and rating."""
        if df.empty:
            print("Warning: No data to aggregate.")
            return pd.DataFrame()

        agg_df = df.groupby(['bank', 'rating']).agg({
            'sentiment_score': ['mean', 'count']
        }).reset_index()
        agg_df.columns = ['bank', 'rating', 'mean_sentiment_score', 'review_count']
        agg_df = agg_df.sort_values(by=['bank', 'rating']).reset_index(drop=True)
        return agg_df

    def save_results(self, df, agg_df, output_path='data/processed/sentiment_results.csv'):
        """Save sentiment analysis results to CSV."""
        try:
            df.to_csv(output_path, index=False, encoding='utf-8')
            agg_output_path = output_path.replace('.csv', '_aggregated.csv')
            agg_df.to_csv(agg_output_path, index=False, encoding='utf-8')
            print(f"Saved detailed results to {output_path}")
            print(f"Saved aggregated results to {agg_output_path}")
            return True
        except Exception as e:
            print(f"Error saving results: {e}")
            return False

    def main(self):
        """Run the sentiment analysis pipeline."""
        print("Loading preprocessed data...")
        df = self.load_data()
        if df.empty:
            print("Error: No data to process.")
            return False

        print("Detecting review languages...")
        df = self.detect_language(df)
        print(f"Language distribution:\n{df['language'].value_counts().to_string()}\n")
        df['language'].value_counts().to_csv('data/processed/language_distribution.csv')
        print("Saved language distribution to data/processed/language_distribution.csv\n")

        print("Performing sentiment analysis...")
        df = self.sentiment_analysis(df)

        print("\nSample Sentiment Results (first 5 rows):\n")
        sample_df = df[['review', 'bank', 'rating', 'language', 'sentiment_label', 'sentiment_score']].head(5)
        print(sample_df.to_string(index=False))
        print("\n")

        print("Aggregating sentiment by bank and rating...")
        agg_df = self.aggregate_sentiment(df)
        print("\nAggregated Sentiment Results:\n")
        print(agg_df.to_string(index=False))
        print("\n")

        print(f"Total reviews processed: {len(df)}\n")

        print("Saving results...")
        success = self.save_results(df, agg_df)
        if success:
            print("Sentiment analysis complete.")
            return True
        return False
