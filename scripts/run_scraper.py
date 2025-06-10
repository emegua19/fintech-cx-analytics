from src.utils.config import Config
from src.task_1.scraper import Scraper

# ------------------------
# Main section to run scraper
# ------------------------

if __name__ == "__main__":
    print("\n--- Starting Fintech Reviews Scraper ---\n")
    
    # Load config
    config = Config()
    
    # Initialize scraper
    scraper = Scraper(config)
    
    # Scrape all banks
    df = scraper.scrape_all_banks(num_reviews=400)
    
    # Save raw data
    scraper.save_raw_data(df)
    
    # EXTRA: display rows/columns per bank
    for bank in df['bank'].unique():
        print(f"\n----- Reviews for {bank} -----\n")
        print(df[df['bank'] == bank].head())  # First 5 rows
        
        print(f"\n----- {bank} Ratings Breakdown -----")
        print(df[df['bank'] == bank]['rating'].value_counts())
    
    # Optional: warn if any bank has <400
    review_counts = df['bank'].value_counts()
    for bank, count in review_counts.items():
        if count < 400:
            print(f"WARNING: Less than 400 reviews collected for {bank}!")
    print("\n--- Scraping process completed. ---\n")
