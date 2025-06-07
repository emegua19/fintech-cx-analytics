import pytest
import pandas as pd
from unittest.mock import patch
from src.task_1.preprocessor import Preprocessor
from src.utils.data_handler import DataHandler

@pytest.fixture
def data_handler():
    """Fixture to provide a DataHandler instance."""
    return DataHandler()

@pytest.fixture
def preprocessor(data_handler):
    """Fixture to provide a Preprocessor instance."""
    return Preprocessor(data_handler)

@pytest.fixture
def sample_data():
    """Fixture for sample review data including Amharic text and a duplicate."""
    return pd.DataFrame({
        'review': ['Great app!!', 'ጥሩ መተግበሪዤ', None, 'Great app!!'],  # Duplicate 'Great app!!'
        'rating': [5, 4, None, 5],
        'date': ['2025-06-01', '2025-06-02', 'invalid', '2025-06-01'],
        'bank': ['CBE', 'BOA', 'Dashen', 'CBE'],
        'source': ['Google Play', 'Google Play', 'Google Play', 'Google Play']
    })

def test_load_data(preprocessor, data_handler):
    """Test loading and combining multiple CSVs."""
    with patch.object(data_handler, 'read_csv') as mock_read:
        mock_read.side_effect = [
            pd.DataFrame({'review': ['Test review'], 'rating': [5], 'date': ['2025-06-01'], 'bank': ['CBE'], 'source': ['Google Play']}),
            pd.DataFrame({'review': ['Another review'], 'rating': [3], 'date': ['2025-06-02'], 'bank': ['BOA'], 'source': ['Google Play']})
        ]
        df = preprocessor.load_data(['data/raw/cbe.csv', 'data/raw/boa.csv'])
        assert len(df) == 2
        assert list(df.columns) == ['review', 'rating', 'date', 'bank', 'source']
        assert df['bank'].iloc[0] == 'CBE'
        assert df['bank'].iloc[1] == 'BOA'

def test_load_data_empty(preprocessor, data_handler):
    """Test loading empty or missing CSVs."""
    with patch.object(data_handler, 'read_csv', return_value=pd.DataFrame()):
        df = preprocessor.load_data(['data/raw/empty.csv'])
        assert df.empty
        assert list(df.columns) == ['review', 'rating', 'date', 'bank', 'source']

def test_clean_data(preprocessor, sample_data):
    """Test data cleaning: duplicates, missing data, normalization, Amharic handling."""
    cleaned_df = preprocessor.clean_data(sample_data)
    # Check duplicate removal
    assert len(cleaned_df) == 3  # Duplicate 'Great app!!' removed
    # Check missing data handling
    assert cleaned_df['review'].iloc[2] == ''
    assert cleaned_df['rating'].iloc[2] == 0
    assert cleaned_df['bank'].iloc[2] == 'dashen'
    assert cleaned_df['source'].iloc[2] == 'Google Play'
    # Check date normalization
    assert cleaned_df['date'].iloc[0] == '2025-06-01'
    assert pd.isna(cleaned_df['date'].iloc[2]) or cleaned_df['date'].iloc[2] == 'NaT'
    # Check text normalization and Amharic preservation
    assert cleaned_df['review'].iloc[0] == 'great app'
    assert cleaned_df['review'].iloc[1] == 'ጥሩ መተግበሪዤ'  # Amharic preserved

def test_save_cleaned_data(preprocessor, sample_data):
    """Test saving cleaned data to CSV."""
    with patch.object(preprocessor.data_handler, 'write_csv', return_value=True) as mock_write:
        result = preprocessor.save_cleaned_data(sample_data, 'data/processed/test.csv')
        assert result is True
        mock_write.assert_called_once()
        args, _ = mock_write.call_args
        df = args[0]
        assert list(df.columns) == ['review', 'rating', 'date', 'bank', 'source']