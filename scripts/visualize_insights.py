import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os

plt.style.use('seaborn-v0_8-muted')

def load_data():
    df = pd.read_csv("data/processed/sentiment_results.csv")
    return df

def plot_sentiment_distribution(df):
    plt.figure(figsize=(6, 4))
    sns.countplot(data=df, x='sentiment_label', palette='Set2')
    plt.title("Sentiment Distribution")
    plt.xlabel("Sentiment")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("plots/sentiment_distribution.png")
    plt.close()

def plot_rating_distribution(df):
    plt.figure(figsize=(6, 4))
    sns.countplot(data=df, x='rating', palette='Set3')
    plt.title("Rating Distribution")
    plt.xlabel("Rating")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("plots/rating_distribution.png")
    plt.close()

def plot_sentiment_vs_rating(df):
    plt.figure(figsize=(6, 4))
    sns.boxplot(data=df, x='rating', y='sentiment_score', palette='coolwarm')
    plt.title("Sentiment Score by Rating")
    plt.xlabel("Rating")
    plt.ylabel("Sentiment Score")
    plt.tight_layout()
    plt.savefig("plots/sentiment_vs_rating.png")
    plt.close()

def plot_wordcloud_per_bank(df):
    banks = df['bank'].unique()
    for bank in banks:
        text = " ".join(df[df['bank'] == bank]['review'].dropna().astype(str).values)
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        plt.figure(figsize=(8, 4))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(f"Word Cloud - {bank}")
        plt.tight_layout()
        plt.savefig(f"plots/wordcloud_{bank.lower()}.png")
        plt.close()

def plot_theme_bar_chart():
    import glob
    import os

    csv_files = glob.glob("data/analysis/*_themes.csv")

    for file in csv_files:
        df_theme = pd.read_csv(file)
        bank_name = os.path.basename(file).replace("_themes.csv", "").replace("_", " ").title()
        plt.figure(figsize=(8, 4))
        sns.barplot(data=df_theme.head(10), x='score', y='keyword', palette='viridis')
        plt.title(f"Top Keywords - {bank_name}")
        plt.xlabel("TF-IDF Score")
        plt.ylabel("Keyword")
        plt.tight_layout()
        plt.savefig(f"plots/themes_{bank_name.lower().replace(' ', '_')}.png")
        plt.close()

def plot_sentiment_trend(df):
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    trend_df = df.dropna(subset=['date']).copy()
    trend_df['date'] = trend_df['date'].dt.to_period('M').dt.to_timestamp()

    plt.figure(figsize=(10, 5))
    sns.lineplot(data=trend_df, x='date', y='sentiment_score', hue='bank', marker="o")
    plt.title("Monthly Sentiment Score Trend by Bank")
    plt.xlabel("Month")
    plt.ylabel("Average Sentiment Score")
    plt.legend(title="Bank")
    plt.tight_layout()
    plt.savefig("plots/sentiment_trend_by_bank.png")
    plt.close()

def plot_sentiment_comparison(df):
    avg_sentiment = df.groupby('bank')['sentiment_score'].mean().sort_values(ascending=False)
    plt.figure(figsize=(6, 4))
    sns.barplot(x=avg_sentiment.values, y=avg_sentiment.index, palette='cool')
    plt.title("Average Sentiment Score by Bank")
    plt.xlabel("Average Sentiment")
    plt.ylabel("Bank")
    plt.tight_layout()
    plt.savefig("plots/sentiment_comparison_by_bank.png")
    plt.close()

def run_all():
    if not os.path.exists("outputs/plots"):
        os.makedirs("plots")

    df = load_data()
    plot_sentiment_distribution(df)
    plot_rating_distribution(df)
    plot_sentiment_vs_rating(df)
    plot_wordcloud_per_bank(df)
    plot_theme_bar_chart()
    plot_sentiment_trend(df)
    plot_sentiment_comparison(df)
    print("All 7 plots generated in plots/")

if __name__ == '__main__':
    run_all()
