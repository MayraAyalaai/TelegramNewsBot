import json
import os
from datetime import datetime, date
from typing import Dict

class StatsManager:
    def __init__(self, stats_file='bot_stats.json'):
        self.stats_file = stats_file
        self.stats = self.load_stats()
    
    def load_stats(self) -> Dict:
        """Load statistics from file"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self.get_default_stats()
        return self.get_default_stats()
    
    def get_default_stats(self) -> Dict:
        """Get default statistics structure"""
        return {
            'total_users': 0,
            'commands_used': {
                'start': 0,
                'help': 0,
                'news': 0,
                'tech': 0,
                'business': 0,
                'subscribe': 0,
                'unsubscribe': 0,
                'mysubs': 0
            },
            'daily_stats': {},
            'category_requests': {
                'general': 0,
                'tech': 0,
                'business': 0
            },
            'subscription_counts': {
                'general': 0,
                'tech': 0,
                'business': 0
            }
        }
    
    def save_stats(self):
        """Save statistics to file"""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except IOError as e:
            print(f"Error saving stats: {e}")
    
    def record_command_usage(self, command: str, user_id: int = None):
        """Record command usage"""
        today = date.today().isoformat()
        
        if command in self.stats['commands_used']:
            self.stats['commands_used'][command] += 1
        
        if today not in self.stats['daily_stats']:
            self.stats['daily_stats'][today] = {
                'commands': 0,
                'unique_users': set()
            }
        
        self.stats['daily_stats'][today]['commands'] += 1
        
        if user_id:
            if isinstance(self.stats['daily_stats'][today]['unique_users'], list):
                self.stats['daily_stats'][today]['unique_users'] = set(self.stats['daily_stats'][today]['unique_users'])
            self.stats['daily_stats'][today]['unique_users'].add(user_id)
            self.stats['daily_stats'][today]['unique_users'] = list(self.stats['daily_stats'][today]['unique_users'])
        
        self.save_stats()
    
    def record_news_request(self, category: str):
        """Record news category request"""
        if category in self.stats['category_requests']:
            self.stats['category_requests'][category] += 1
            self.save_stats()
    
    def record_subscription_change(self, category: str, subscribed: bool):
        """Record subscription changes"""
        if category in self.stats['subscription_counts']:
            if subscribed:
                self.stats['subscription_counts'][category] += 1
            else:
                self.stats['subscription_counts'][category] = max(0, self.stats['subscription_counts'][category] - 1)
            self.save_stats()
    
    def record_new_user(self):
        """Record new user registration"""
        self.stats['total_users'] += 1
        self.save_stats()
    
    def get_stats_summary(self) -> str:
        """Get formatted statistics summary"""
        total_commands = sum(self.stats['commands_used'].values())
        most_used_cmd = max(self.stats['commands_used'], key=self.stats['commands_used'].get)
        most_requested_category = max(self.stats['category_requests'], key=self.stats['category_requests'].get)
        
        summary = f"""📊 Bot Statistics Summary
        
👥 Total Users: {self.stats['total_users']}
🔧 Total Commands Used: {total_commands}
📈 Most Used Command: /{most_used_cmd} ({self.stats['commands_used'][most_used_cmd]} times)
📰 Most Requested Category: {most_requested_category} ({self.stats['category_requests'][most_requested_category]} requests)

📊 Command Usage:
"""
        
        for cmd, count in self.stats['commands_used'].items():
            summary += f"  /{cmd}: {count}\n"
        
        summary += f"\n📚 Category Requests:\n"
        for category, count in self.stats['category_requests'].items():
            summary += f"  {category}: {count}\n"
        
        summary += f"\n📝 Active Subscriptions:\n"
        for category, count in self.stats['subscription_counts'].items():
            summary += f"  {category}: {count}\n"
            
        return summary