import os
import sys
import pandas as pd
import psycopg2
from src.task_3.database_manager import DatabaseManager
import pytest

# Adjust sys.path to include the project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope="session")
def db_manager():
    """Fixture to set up and tear down the test database and manager."""
    db_name = "test_bank_reviews"
    user = "postgres"
    password = "y2g@post"
    host = "localhost"
    port = 5432

    # Create test database
    conn = psycopg2.connect(dbname="postgres", user=user, password=password, host=host, port=port)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cursor.execute(f"CREATE DATABASE {db_name}")
    cursor.close()
    conn.close()

    # Initialize DatabaseManager
    db = DatabaseManager(db_name, user, password, host, port)
    db.create_tables()
    yield db  # Provide the database manager to tests

    # Teardown: Drop tables and database
    db.cursor.execute("DROP TABLE IF EXISTS reviews, banks CASCADE")
    db.conn.commit()
    db.close()
    conn = psycopg2.connect(dbname="postgres", user=user, password=password, host=host, port=port)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cursor.close()
    conn.close()

@pytest.fixture
def sample_df():
    """Fixture to provide a sample DataFrame for testing."""
    data = {
        'bank': ['Bank A', 'Bank B'],
        'review': ['Great service!', 'Poor experience'],
        'rating': [5, 2],
        'date': ['2025-06-10', '2025-06-09'],
        'source': ['Website', 'App'],
        'sentiment_label': ['Positive', 'Negative'],
        'sentiment_score': [0.9, 0.2],
        'theme': ['Service', 'Support']
    }
    return pd.DataFrame(data)

def test_connection(db_manager):
    """Test if database connection is established."""
    assert db_manager.conn is not None
    assert db_manager.cursor is not None

def test_create_tables(db_manager):
    """Test if tables are created successfully."""
    db_manager.cursor.execute("SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'banks')")
    banks_exists = db_manager.cursor.fetchone()[0]
    db_manager.cursor.execute("SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'reviews')")
    reviews_exists = db_manager.cursor.fetchone()[0]
    assert banks_exists
    assert reviews_exists

def test_insert_banks(db_manager):
    """Test inserting banks and retrieving bank_id mapping."""
    bank_names = ["Bank A", "Bank B"]
    bank_id_map = db_manager.insert_banks(bank_names)
    assert len(bank_id_map) == 2
    assert "Bank A" in bank_id_map
    assert "Bank B" in bank_id_map

    # Verify data in banks table
    db_manager.cursor.execute("SELECT bank_name FROM banks")
    names = [row[0] for row in db_manager.cursor.fetchall()]
    assert "Bank A" in names
    assert "Bank B" in names

def test_insert_reviews(db_manager, sample_df):
    """Test inserting reviews from a DataFrame."""
    bank_id_map = db_manager.insert_banks(sample_df['bank'].unique())
    db_manager.insert_reviews(sample_df, bank_id_map)

    # Verify data in reviews table
    db_manager.cursor.execute("SELECT bank_id, review, rating FROM reviews")
    results = db_manager.cursor.fetchall()
    assert len(results) == 2
    assert (bank_id_map['Bank A'], 'Great service!', 5) in results
    assert (bank_id_map['Bank B'], 'Poor experience', 2) in results