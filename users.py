import json
import hashlib
from pathlib import Path
from typing import Dict, Optional

class UserManager:
    def __init__(self):
        self.users_file = Path("users.json")
        self._load_users()

    def _load_users(self):
        if self.users_file.exists():
            with open(self.users_file, "r") as f:
                self.users = json.load(f)
        else:
            self.users = {
                "admin": self._hash_password("admin123")  # Default admin account
            }
            self._save_users()

    def _save_users(self):
        with open(self.users_file, "w") as f:
            json.dump(self.users, f)

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_user(self, username: str, password: str) -> bool:
        if username not in self.users:
            return False
        return self.users[username] == self._hash_password(password)

    def add_user(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = self._hash_password(password)
        self._save_users()
        return True

    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        if not self.verify_user(username, old_password):
            return False
        self.users[username] = self._hash_password(new_password)
        self._save_users()
        return True 