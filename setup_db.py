import sqlite3
import os

def setup_database():
    # Remove old database
    if os.path.exists('email_history.db'):
        os.remove('email_history.db')
    
    # Create new database
    conn = sqlite3.connect('email_history.db')
    cursor = conn.cursor()
    
    # Create new table with all required columns
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS email_history (
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
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print("Database created successfully!")

if __name__ == "__main__":
    setup_database()
