import feedparser
import requests
from datetime import datetime

class NewsFetcher:
    def __init__(self):
        self.feeds = {
            'tech': [
                'https://techcrunch.com/feed/',
                'https://www.theverge.com/rss/index.xml'
            ],
            'general': [
                'https://rss.cnn.com/rss/edition.rss',
                'https://feeds.bbci.co.uk/news/world/rss.xml'
            ]
        }
    
    def get_news(self, category='general', limit=5):
        """Fetch news from RSS feeds"""
        if category not in self.feeds:
            return []
        
        all_entries = []
        
        for feed_url in self.feeds[category]:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries:
                    all_entries.append({
                        'title': entry.title,
                        'link': entry.link,
                        'summary': getattr(entry, 'summary', '')[:200] + '...',
                        'published': getattr(entry, 'published', ''),
                        'source': feed.feed.title if hasattr(feed.feed, 'title') else 'Unknown'
                    })
            except Exception as e:
                print(f"Error fetching from {feed_url}: {e}")
        
        return sorted(all_entries, key=lambda x: x.get('published', ''), reverse=True)[:limit]