import sqlite3
import os

def reset_database():
    # Delete existing database
    if os.path.exists('email_history.db'):
        os.remove('email_history.db')
        print("Removed old database")
    
    # Create new connection
    conn = sqlite3.connect('email_history.db')
    cursor = conn.cursor()
    
    # Create table with all necessary columns
    cursor.execute('''
    CREATE TABLE email_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        email_content TEXT NOT NULL,
        prediction INTEGER NOT NULL,
        confidence REAL NOT NULL,
        timestamp TEXT NOT NULL,
        features TEXT,
        risk_score REAL
    )
    ''')
    
    conn.commit()
    conn.close()
    print("Created new database with correct structure")

if __name__ == "__main__":
    reset_database()
