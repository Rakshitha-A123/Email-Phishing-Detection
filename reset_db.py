import sqlite3
import os

def reset_database():
    # Delete existing database if it exists
    if os.path.exists('email_history.db'):
        os.remove('email_history.db')
    
    # Create new database connection
    conn = sqlite3.connect('email_history.db')
    cursor = conn.cursor()
    
    # Create table with correct structure
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS email_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        email_content TEXT NOT NULL,
        prediction INTEGER NOT NULL,
        confidence REAL NOT NULL,
        timestamp TEXT NOT NULL,
        features TEXT
    )
    ''')
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("Database has been reset successfully!")

if __name__ == "__main__":
    reset_database()
