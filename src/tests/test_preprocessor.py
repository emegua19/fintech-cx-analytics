import unittest
import pandas as pd
from unittest.mock import MagicMock
from src.task_1.preprocessor import Preprocessor, detect_language


class TestLanguageDetection(unittest.TestCase):
    def test_known_english(self):
        self.assertEqual(detect_language("This app is good."), "english")

    def test_known_amharic(self):
        self.assertEqual(detect_language("በጣም ጥሩ ነው"), "amharic")

    def test_bilingual(self):
        # Mixed English and Amharic (less than 50% Amharic characters)
        self.assertEqual(detect_language("This is በጣም good."), "bilingual")

    def test_unknown_short(self):
        self.assertEqual(detect_language("Hi"), "unknown")

    def test_empty_or_null(self):
        self.assertEqual(detect_language(""), "unknown")
        self.assertEqual(detect_language(None), "unknown")


class TestPreprocessor(unittest.TestCase):
    def setUp(self):
        # Sample mock DataHandler
        self.mock_data_handler = MagicMock()
        self.preprocessor = Preprocessor(self.mock_data_handler)

    def test_clean_data_basic(self):
        sample_data = pd.DataFrame({
            'review': ['Great app!', 'በጣም ጥሩ ነው', 'Great app!', None],
            'rating': [5, 4, 2, 3],
            'date': ['2024-01-01', '2024-01-02', 'invalid_date', '2024-01-03'],
            'bank': ['CBE', 'BOA', None, 'Dashen'],
            'source': ['Google Play', None, 'App Store', None]
        })

        cleaned_df = self.preprocessor.clean_data(sample_data)

        # Expect 2 valid rows (first 2 are valid)
        self.assertEqual(len(cleaned_df), 2)

        # Validate language detection result
        languages = cleaned_df['language'].tolist()
        self.assertIn('english', languages)
        self.assertIn('amharic', languages)

    def test_load_data_combines_files(self):
        df1 = pd.DataFrame({'review': ['Great'], 'rating': [5], 'date': ['2024-01-01'], 'bank': ['CBE'], 'source': ['Google Play']})
        df2 = pd.DataFrame({'review': ['Poor'], 'rating': [1], 'date': ['2024-01-02'], 'bank': ['BOA'], 'source': ['App Store']})

        self.mock_data_handler.read_csv.side_effect = [df1, df2, pd.DataFrame()]

        combined_df = self.preprocessor.load_data(['path1.csv', 'path2.csv', 'path3.csv'])
        self.assertEqual(len(combined_df), 2)
        self.assertIn('review', combined_df.columns)

    def test_save_cleaned_data(self):
        df = pd.DataFrame({'review': ['Great'], 'rating': [5], 'date': ['2024-01-01'], 'bank': ['cbe'], 'source': ['Google Play'], 'language': ['english']})
        self.mock_data_handler.write_csv.return_value = True

        result = self.preprocessor.save_cleaned_data(df, 'output.csv')
        self.mock_data_handler.write_csv.assert_called_once_with(df, 'output.csv')
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
