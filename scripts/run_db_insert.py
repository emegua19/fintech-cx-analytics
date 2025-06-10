# scripts/run_db_insert.py
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Adjust path
from src.task_3.database_manager import DatabaseManager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Parameters
DB_NAME = "bank_reviews"
DB_USER = "postgres"
DB_PASSWORD = "y2g@post"
DB_HOST = "localhost"
DB_PORT = 5432

# Main pipeline
if __name__ == "__main__":
    print("\n--- Starting Database Insert ---\n")

    # Load cleaned reviews
    df = pd.read_csv("data/processed/bank_reviews_cleaned.csv")
    print(f"Loaded {len(df)} cleaned reviews.")

    # Initialize DatabaseManager
    db_manager = DatabaseManager(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)

    # Create tables
    db_manager.create_tables()

    # Insert banks
    bank_id_map = db_manager.insert_banks(df['bank'].unique())

    # Insert reviews
    db_manager.insert_reviews(df, bank_id_map)

    # Close connection
    db_manager.close()

    print("\n--- Database Insert Completed ---\n")
