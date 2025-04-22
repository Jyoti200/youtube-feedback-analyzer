import sqlite3
import pandas as pd

DATABASE_NAME = "comments_analysis.db"

def get_connection():
    """Create and return a new database connection"""
    return sqlite3.connect(DATABASE_NAME)

def initialize_db():
    """Initialize the database structure"""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sentiment_analysis (
                feature TEXT,
                sentiment_category TEXT,
                count INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

def save_to_db(sentiment_summary, feature="YouTube Comments"):
    """Save sentiment analysis results to the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        for category, count in sentiment_summary.items():
            cursor.execute("""
                INSERT INTO sentiment_analysis (feature, sentiment_category, count)
                VALUES (?, ?, ?)
            """, (feature, category, count))
        conn.commit()

def view_data():
    """View the stored data (for testing)"""
    with get_connection() as conn:
        df = pd.read_sql_query("SELECT * FROM sentiment_analysis", conn)
        print(df.head())

if __name__ == "__main__":
    initialize_db()
    test_summary = {"positive": 5, "neutral": 3, "negative": 2}
    save_to_db(test_summary)
    view_data()