# src/task_4/visualizer.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

class Visualizer:
    def __init__(self, df):
        """Initialize Visualizer with cleaned DataFrame."""
        self.df = df
        self.output_dir = 'plots'
        os.makedirs(self.output_dir, exist_ok=True)

    def plot_language_distribution(self):
        plt.figure(figsize=(8, 6))
        self.df['language'].value_counts().plot(kind='bar', color='skyblue')
        plt.title('Language Distribution of Reviews')
        plt.xlabel('Language')
        plt.ylabel('Number of Reviews')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/language_distribution.png')
        plt.close()
        print("✅ Language distribution plot saved.")

    def plot_sentiment_distribution_per_bank(self):
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=self.df, x='bank', y='sentiment_score')
        plt.title('Sentiment Score Distribution per Bank')
        plt.xlabel('Bank')
        plt.ylabel('Sentiment Score')
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/sentiment_distribution_per_bank.png')
        plt.close()
        print("✅ Sentiment distribution per bank plot saved.")

    def plot_sentiment_per_rating(self):
        plt.figure(figsize=(8, 6))
        sns.boxplot(data=self.df, x='rating', y='sentiment_score')
        plt.title('Sentiment Score per Rating')
        plt.xlabel('Rating')
        plt.ylabel('Sentiment Score')
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/sentiment_per_rating.png')
        plt.close()
        print("✅ Sentiment per rating plot saved.")

    def plot_rating_distribution_per_bank(self):
        plt.figure(figsize=(10, 6))
        sns.countplot(data=self.df, x='rating', hue='bank')
        plt.title('Rating Distribution per Bank')
        plt.xlabel('Rating')
        plt.ylabel('Count')
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/rating_distribution_per_bank.png')
        plt.close()
        print("✅ Rating distribution per bank plot saved.")

    def plot_theme_distribution_per_bank(self):
        plt.figure(figsize=(12, 8))
        sns.countplot(data=self.df, x='theme', hue='bank')
        plt.title('Theme Distribution per Bank')
        plt.xlabel('Theme')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/theme_distribution_per_bank.png')
        plt.close()
        print("✅ Theme distribution per bank plot saved.")

    def plot_sentiment_vs_theme(self):
        plt.figure(figsize=(12, 8))
        sns.boxplot(data=self.df, x='theme', y='sentiment_score')
        plt.title('Sentiment Score vs Theme')
        plt.xlabel('Theme')
        plt.ylabel('Sentiment Score')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/sentiment_vs_theme.png')
        plt.close()
        print("✅ Sentiment vs theme plot saved.")

    def plot_wordcloud_per_bank(self, bank_name):
        from wordcloud import WordCloud
        text = ' '.join(self.df[self.df['bank'] == bank_name]['review'].dropna().tolist())
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(f'WordCloud for {bank_name}')
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/wordcloud_{bank_name.lower().replace(" ", "_")}.png')
        plt.close()
        print(f"✅ WordCloud for {bank_name} saved.")
