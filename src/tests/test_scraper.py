import pytest
import pandas as pd
from unittest.mock import patch
from src.task_1.scraper import Scraper
from src.utils.config import Config

@pytest.fixture
def sample_reviews():
    """Sample data simulating google-play-scraper output."""
    return [
        {
            'content': 'Great app!',
            'score': 5,
            'at': pd.Timestamp('2025-06-06'),
        },
        {
            'content': 'Needs improvement.',
            'score': 3,
            'at': pd.Timestamp('2025-06-05'),
        }
    ]

@pytest.fixture
def scraper():
    """Fixture to create a Scraper instance."""
    config = Config()
    return Scraper(config)

@patch('src.task_1.scraper.reviews')
def test_scrape_reviews(mock_reviews, scraper, sample_reviews):
    """Test scrape_reviews returns a DataFrame with expected columns."""
    # Mock reviews() to return sample data + empty token
    mock_reviews.return_value = (sample_reviews, None)

    app_id = 'test.app.id'
    app_name = 'Test Bank'

    df = scraper.scrape_reviews(app_id, app_name, num_reviews=2)

    # Check DataFrame structure
    expected_columns = ['review', 'rating', 'date', 'bank', 'source']
    assert all(col in df.columns for col in expected_columns)

    # Check content
    assert len(df) == 2
    assert df.iloc[0]['review'] == 'Great app!'
    assert df.iloc[0]['rating'] == 5
    assert df.iloc[0]['bank'] == app_name
    assert df.iloc[0]['source'] == 'Google Play'

@patch('src.task_1.scraper.reviews')
def test_scrape_all_banks(mock_reviews, scraper, sample_reviews):
    """Test scrape_all_banks returns combined DataFrame."""
    # Mock reviews() to return sample data for each bank
    mock_reviews.return_value = (sample_reviews, None)

    df = scraper.scrape_all_banks(num_reviews=2)

    # Check structure
    expected_columns = ['review', 'rating', 'date', 'bank', 'source']
    assert all(col in df.columns for col in expected_columns)

    # Check that it contains reviews for all banks in config
    banks_in_config = scraper.app_ids.keys()
    banks_in_df = df['bank'].unique()

    for bank in banks_in_config:
        assert bank in banks_in_df

    # Check total rows
    expected_rows = len(sample_reviews) * len(banks_in_config)
    assert len(df) == expected_rows
