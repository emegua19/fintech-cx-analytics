import unittest
import pandas as pd
import os
from src.task_2.theme_analyzer import ThemeAnalyzer

class TestThemeAnalyzer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a temporary small sample dataset
        cls.test_file = 'test_data.csv'
        sample_data = {
            'bank': ['Bank A', 'Bank A', 'Bank B'],
            'review': [
                "App crashes frequently and login fails.",
                "Transfer failed and support didn't help.",
                "I love the new interface but wish it had dark mode."
            ],
            'language': ['english', 'english', 'english']
        }
        pd.DataFrame(sample_data).to_csv(cls.test_file, index=False)

        # Setup analyzer instance
        cls.analyzer = ThemeAnalyzer(input_path=cls.test_file)
        cls.analyzer.theme_keywords = {
            "Account Access Issues": ["login", "sign in", "authentication"],
            "Transaction Performance": ["transfer", "transaction", "failed"],
            "User Interface & Experience": ["app", "interface", "crash", "mode"],
            "Customer Support": ["support", "help"],
            "Feature Requests": ["wish", "feature"]
        }

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_file):
            os.remove(cls.test_file)

    def test_load_data(self):
        df = self.analyzer.load_data()
        self.assertFalse(df.empty)
        self.assertEqual(len(df), 3)

    def test_extract_keywords(self):
        self.analyzer.load_data()
        results = self.analyzer.extract_keywords_per_bank(top_n=10)
        self.assertIn("Bank A", results)
        self.assertIn("Transaction Performance", results["Bank A"])
        self.assertTrue(any("transfer" in kw[0] for kw in results["Bank A"]["Transaction Performance"]))

    def test_grouping_logic(self):
        keywords = [('login fails', 0.9), ('transfer failed', 1.2), ('dark mode', 0.8), ('unknownword', 0.5)]
        grouped = self.analyzer.group_keywords_by_theme(keywords)
        self.assertIn("Account Access Issues", grouped)
        self.assertIn("Other", grouped)
        self.assertEqual(len(grouped["Other"]), 1)

if __name__ == '__main__':
    unittest.main()
