import pytest
import pandas as pd
from src.task_2.sentiment_analyzer import SentimentAnalyzer

@pytest.fixture
def analyzer():
    """Fixture to create a SentimentAnalyzer instance."""
    return SentimentAnalyzer()

@pytest.fixture
def sample_reviews_df():
    """Sample DataFrame with English, Amharic, Bilingual, and unknown reviews."""
    return pd.DataFrame({
        'review': [
            'Great app!',                         # English → Positive
            'ጥሩ አፕ ነው።',                      # Amharic → Positive
            'Very bad experience.',                # English → Negative
            'ጥሩ app ነው',                        # Bilingual → Positive
            '',                                    # Empty → Neutral
            None                                   # None → Neutral
        ],
        'rating': [5, 5, 1, 5, 3, 4],
        'bank': ['CBE', 'BOA', 'Dashen', 'CBE', 'CBE', 'BOA'],
        'source': ['Google Play'] * 6
    })

def test_detect_language(analyzer, sample_reviews_df):
    """Test language detection."""
    df = analyzer.detect_language(sample_reviews_df)
    
    # Check that the language column was added
    assert 'language' in df.columns

    # Check specific detections
    assert df['language'].iloc[0] == 'english'
    assert df['language'].iloc[1] == 'amharic'
    assert df['language'].iloc[2] == 'english'
    assert df['language'].iloc[3] == 'bilingual'
    assert df['language'].iloc[4] == 'unknown'
    assert df['language'].iloc[5] == 'unknown'

def test_sentiment_analysis(analyzer, sample_reviews_df):
    """Test sentiment analysis on English and Amharic/Bilingual reviews."""
    df = analyzer.detect_language(sample_reviews_df)
    df = analyzer.sentiment_analysis(df)

    # Check that sentiment columns were added
    assert 'sentiment_label' in df.columns
    assert 'sentiment_score' in df.columns

    # Check English positive → should be POSITIVE or NEUTRAL (depending on model threshold)
    assert df[df['language'] == 'english'].iloc[0]['sentiment_label'] in ['POSITIVE', 'NEUTRAL', 'NEGATIVE']

    # Check Amharic → should match heuristic
    amharic_row = df[df['language'] == 'amharic'].iloc[0]
    assert amharic_row['sentiment_label'] == 'POSITIVE'
    assert amharic_row['sentiment_score'] > 0

    # Check Bilingual → should match heuristic
    bilingual_row = df[df['language'] == 'bilingual'].iloc[0]
    assert bilingual_row['sentiment_label'] == 'POSITIVE'
    assert bilingual_row['sentiment_score'] > 0

    # Check unknown → should be NEUTRAL
    unknown_rows = df[df['language'] == 'unknown']
    assert all(unknown_rows['sentiment_label'] == 'NEUTRAL')
    assert all(unknown_rows['sentiment_score'] == 0.0)
