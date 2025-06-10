from src.task_2.sentiment_analyzer import SentimentAnalyzer

def main():
    """Run the sentiment analysis pipeline."""
    print("Starting sentiment analysis process...")
    analyzer = SentimentAnalyzer()
    success = analyzer.main()
    if success:
        print("Process completed successfully.")
    else:
        print("Process failed. Check logs for details.")

if __name__ == "__main__":
    main()