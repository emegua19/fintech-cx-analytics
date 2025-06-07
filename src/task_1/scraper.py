import pandas as pd
from google_play_scraper import reviews, Sort
import os
from src.utils.config import Config

class Scraper:
    def __init__(self, config):
        """Initialize Scraper with app IDs from Config."""
        self.config = config
        self.app_ids = self.config.get_app_ids()

    def scrape_reviews(self, app_id, app_name, num_reviews=400):
        """Scrape reviews for a specific app from Google Play Store."""
        try:
            result, _ = reviews(
                app_id,
                lang='en',  # Prioritize English (some Amharic may still appear)
                country='et',  # Ethiopia
                sort=Sort.NEWEST,
                count=num_reviews
            )
            
            data = []
            for review in result:
                content = review['content']
                if content and content.strip():  # Skip empty reviews
                    data.append({
                        'review': content,
                        'rating': review['score'],
                        'date': review['at'].strftime('%Y-%m-%d'),
                        'bank': app_name,
                        'source': 'Google Play'
                    })
            return pd.DataFrame(data)
        except Exception as e:
            print(f"Error scraping {app_name}: {e}")
            return pd.DataFrame()

    def scrape_all_banks(self, num_reviews=400):
        """Scrape reviews for all banks and combine into a DataFrame."""
        all_reviews = []
        for app_name, app_id in self.app_ids.items():
            print(f"\nStarting scrape for {app_name}...")
            df = self.scrape_reviews(app_id, app_name, num_reviews)
            if not df.empty:
                all_reviews.append(df)
        
        if all_reviews:
            combined_df = pd.concat(all_reviews, ignore_index=True)
            print(f"\nTotal combined reviews: {len(combined_df)}")
            return combined_df
        else:
            print("\nNo reviews were scraped.")
            return pd.DataFrame()

    def save_raw_data(self, df, output_dir='data/raw', save_combined=True):
        """Save scraped reviews to CSV files per bank + optional combined CSV."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        if not df.empty:
            # Save per bank
            for bank in df['bank'].unique():
                bank_df = df[df['bank'] == bank]
                bank_file = os.path.join(output_dir, f"{bank.lower().replace(' ', '_')}_reviews_raw.csv")
                bank_df.to_csv(bank_file, index=False, encoding='utf-8')
                print(f"Saved {len(bank_df)} reviews to {bank_file}")
            
            # Optional: save combined CSV
            if save_combined:
                combined_file = os.path.join(output_dir, "all_banks_reviews_raw.csv")
                df.to_csv(combined_file, index=False, encoding='utf-8')
                print(f"\nSaved combined reviews CSV to {combined_file}")
            return True
        else:
            print("\nNo data to save.")
            return False

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
