import time
from collections import defaultdict, deque
from typing import Dict, Deque

class RateLimiter:
    def __init__(self, requests_per_minute: int = 10, requests_per_hour: int = 100):
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        
        # Store timestamps of requests per user
        self.user_requests: Dict[int, Deque[float]] = defaultdict(deque)
        self.cleanup_interval = 3600  # Clean up old records every hour
        self.last_cleanup = time.time()
    
    def is_allowed(self, user_id: int) -> tuple[bool, str]:
        """Check if user is allowed to make a request"""
        current_time = time.time()
        
        # Clean up old records periodically
        if current_time - self.last_cleanup > self.cleanup_interval:
            self._cleanup_old_records(current_time)
            self.last_cleanup = current_time
        
        user_requests = self.user_requests[user_id]
        
        # Remove requests older than 1 hour
        while user_requests and current_time - user_requests[0] > 3600:
            user_requests.popleft()
        
        # Check hourly limit
        if len(user_requests) >= self.requests_per_hour:
            return False, "You've reached the hourly limit of news requests. Please try again later."
        
        # Remove requests older than 1 minute
        minute_requests = 0
        temp_deque = deque(user_requests)
        while temp_deque and current_time - temp_deque[0] <= 60:
            minute_requests += 1
            temp_deque.popleft()
        
        # Check per-minute limit
        if minute_requests >= self.requests_per_minute:
            return False, "You're sending requests too quickly. Please wait a moment and try again."
        
        # Record this request
        user_requests.append(current_time)
        
        return True, ""
    
    def _cleanup_old_records(self, current_time: float):
        """Clean up records older than 1 hour"""
        users_to_remove = []
        
        for user_id, requests in self.user_requests.items():
            # Remove old requests
            while requests and current_time - requests[0] > 3600:
                requests.popleft()
            
            # If no recent requests, remove user from tracking
            if not requests:
                users_to_remove.append(user_id)
        
        for user_id in users_to_remove:
            del self.user_requests[user_id]
    
    def get_user_stats(self, user_id: int) -> Dict:
        """Get current rate limiting stats for a user"""
        current_time = time.time()
        user_requests = self.user_requests[user_id]
        
        # Count requests in last hour
        hour_count = sum(1 for req_time in user_requests if current_time - req_time <= 3600)
        
        # Count requests in last minute
        minute_count = sum(1 for req_time in user_requests if current_time - req_time <= 60)
        
        return {
            'requests_last_minute': minute_count,
            'requests_last_hour': hour_count,
            'minute_limit': self.requests_per_minute,
            'hour_limit': self.requests_per_hour
        }