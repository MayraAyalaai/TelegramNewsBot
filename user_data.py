import json
import os
from typing import Dict, List, Set

class UserDataManager:
    def __init__(self, data_file='users.json'):
        self.data_file = data_file
        self.users_data = self.load_data()
    
    def load_data(self) -> Dict:
        """Load user data from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def save_data(self):
        """Save user data to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.users_data, f, indent=2)
        except IOError as e:
            print(f"Error saving data: {e}")
    
    def register_user(self, user_id: int, username: str = None):
        """Register a new user"""
        user_id_str = str(user_id)
        if user_id_str not in self.users_data:
            self.users_data[user_id_str] = {
                'username': username,
                'subscriptions': [],
                'active': True,
                'last_news_time': None
            }
            self.save_data()
    
    def get_user_subscriptions(self, user_id: int) -> List[str]:
        """Get user's subscriptions"""
        user_id_str = str(user_id)
        if user_id_str in self.users_data:
            return self.users_data[user_id_str].get('subscriptions', [])
        return []
    
    def add_subscription(self, user_id: int, category: str):
        """Add a subscription for user"""
        user_id_str = str(user_id)
        if user_id_str in self.users_data:
            subscriptions = self.users_data[user_id_str].get('subscriptions', [])
            if category not in subscriptions:
                subscriptions.append(category)
                self.users_data[user_id_str]['subscriptions'] = subscriptions
                self.save_data()
                return True
        return False
    
    def remove_subscription(self, user_id: int, category: str):
        """Remove a subscription for user"""
        user_id_str = str(user_id)
        if user_id_str in self.users_data:
            subscriptions = self.users_data[user_id_str].get('subscriptions', [])
            if category in subscriptions:
                subscriptions.remove(category)
                self.users_data[user_id_str]['subscriptions'] = subscriptions
                self.save_data()
                return True
        return False
    
    def get_all_active_users(self) -> List[str]:
        """Get all active users"""
        return [uid for uid, data in self.users_data.items() 
                if data.get('active', True)]