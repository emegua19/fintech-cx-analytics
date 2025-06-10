# src/task_3/database_manager.py

import psycopg2
import pandas as pd

class DatabaseManager:
    def __init__(self, db_name, user, password, host='localhost', port=5432):
        """Initialize DatabaseManager with connection parameters."""
        self.conn = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.conn.cursor()
        print("Connected to PostgreSQL database.")

    def create_tables(self):
        """Create banks and reviews tables."""
        banks_table_sql = """
        CREATE TABLE IF NOT EXISTS banks (
            bank_id SERIAL PRIMARY KEY,
            bank_name VARCHAR(255) UNIQUE NOT NULL
        );
        """

        reviews_table_sql = """
        CREATE TABLE IF NOT EXISTS reviews (
            review_id SERIAL PRIMARY KEY,
            bank_id INT REFERENCES banks(bank_id),
            review TEXT,
            rating INT,
            review_date DATE,
            source VARCHAR(100),
            sentiment_label VARCHAR(50),
            sentiment_score FLOAT,
            theme VARCHAR(100)
        );
        """

        self.cursor.execute(banks_table_sql)
        self.cursor.execute(reviews_table_sql)
        self.conn.commit()
        print("Tables created (if not exist).")

    def insert_banks(self, bank_names):
        """Insert banks and return bank_id mapping."""
        bank_id_map = {}
        for bank_name in bank_names:
            self.cursor.execute("""
                INSERT INTO banks (bank_name)
                VALUES (%s)
                ON CONFLICT (bank_name) DO NOTHING
                RETURNING bank_id;
            """, (bank_name,))
            
            result = self.cursor.fetchone()
            if result is not None:
                bank_id_map[bank_name] = result[0]
            else:
                self.cursor.execute("SELECT bank_id FROM banks WHERE bank_name = %s", (bank_name,))
                bank_id_map[bank_name] = self.cursor.fetchone()[0]

        self.conn.commit()
        print("Banks inserted/verified.")
        return bank_id_map

    def insert_reviews(self, df, bank_id_map):
        """Insert reviews from DataFrame."""
        inserted_count = 0
        for _, row in df.iterrows():
            self.cursor.execute("""
                INSERT INTO reviews (
                    bank_id, review, rating, review_date, source, sentiment_label, sentiment_score, theme
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                bank_id_map[row['bank']],
                row['review'],
                row['rating'],
                row['date'],
                row['source'],
                row.get('sentiment_label', None),
                row.get('sentiment_score', None),
                row.get('theme', None)
            ))
            inserted_count += 1

        self.conn.commit()
        print(f"{inserted_count} reviews inserted into reviews table.")

    def close(self):
        """Close DB connection."""
        self.cursor.close()
        self.conn.close()
        print("PostgreSQL connection closed.")
