import sqlite3
from datetime import datetime
import json
from contextlib import contextmanager

class EmailHistory:
    def __init__(self):
        self.db_file = 'email_history.db'
    
    @contextmanager
    def _get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            yield conn
        finally:
            if conn:
                conn.close()
    
    def add_entry(self, user_id, email_content, prediction, confidence, features, risk_score=0):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Convert features to string if it's not already
                if isinstance(features, (list, dict)):
                    features = json.dumps(features)
                
                cursor.execute('''
                INSERT INTO email_history 
                (user_id, email_content, prediction, confidence, timestamp, features, risk_score)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    user_id,
                    email_content,
                    1 if prediction else 0,
                    float(confidence),
                    datetime.now().isoformat(),
                    features,
                    float(risk_score)
                ))
                
                conn.commit()
                return True
            
        except Exception as e:
            print(f"Error adding entry to database: {str(e)}")
            return False
    
    def get_user_history(self, user_id):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                SELECT id, email_content, prediction, confidence, timestamp, features, risk_score 
                FROM email_history 
                WHERE user_id = ? 
                ORDER BY timestamp DESC
                ''', (user_id,))
                
                history = cursor.fetchall()
                return history
            
        except Exception as e:
            print(f"Error retrieving history: {str(e)}")
            return []
    
    def clear_user_history(self, user_id):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM email_history WHERE user_id = ?', (user_id,))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error clearing history: {str(e)}")
            return False