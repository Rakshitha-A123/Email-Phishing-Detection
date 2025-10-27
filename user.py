import json
import os

class UserManager:
    def __init__(self):
        self.users_file = 'users.json'
        self.load_users()
    
    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}
            self.save_users()
    
    def save_users(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f)
    
    def add_user(self, username, password):
        if username in self.users:
            return False
        self.users[username] = password
        self.save_users()
        return True
    
    def verify_user(self, username, password):
        return username in self.users and self.users[username] == password