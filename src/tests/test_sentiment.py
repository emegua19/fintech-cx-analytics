import pytest
import pandas as pd
from src.task_2.sentiment_analyzer import SentimentAnalyzer

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'review': [
            'Great app, very helpful!',          # English, Positive
            'Bad service, not happy.',           # English, Negative
            'ጥሩ መተግበሪያ ነው።',                  # Amharic, Positive
            'ችግር አለ። አልተሳካም።',                  # Amharic, Negative
            'Good but could be better.',         # English, Neutral/Positive
            'አሪፍ ነው፤ እናመሰግናለን።'               # Amharic, Positive
        ],
        'bank': ['cbe', 'boa', 'cbe', 'dashen', 'boa', 'cbe'],
        'rating': [5, 1, 5, 1, 3, 5]
    })

def test_detect_language(sample_df):
    analyzer = SentimentAnalyzer()
    df = analyzer.detect_language(sample_df)
    
    assert 'language' in df.columns
    assert set(df['language']).issubset({'english', 'amharic', 'bilingual'})
    print("\nLanguage detection passed.\n")
    print(df[['review', 'language']])

def test_sentiment_analysis(sample_df):
    analyzer = SentimentAnalyzer()
    df = analyzer.detect_language(sample_df)
    df = analyzer.sentiment_analysis(df)

    assert 'sentiment_label' in df.columns
    assert 'sentiment_score' in df.columns
    assert df['sentiment_label'].isin(['positive', 'neutral', 'negative']).all()
    assert df['sentiment_score'].apply(lambda x: isinstance(x, float)).all()
    print("\nSentiment analysis passed.\n")
    print(df[['review', 'language', 'sentiment_label', 'sentiment_score']])

def test_aggregation(sample_df):
    analyzer = SentimentAnalyzer()
    df = analyzer.detect_language(sample_df)
    df = analyzer.sentiment_analysis(df)
    agg_df = analyzer.aggregate_sentiment(df)

    assert not agg_df.empty
    assert set(agg_df.columns) == {'bank', 'rating', 'mean_sentiment_score', 'review_count'}
    print("\nAggregation passed.\n")
    print(agg_df)

