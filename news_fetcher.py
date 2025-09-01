import feedparser
import requests
import json
import os
from datetime import datetime

class NewsFetcher:
    def __init__(self, config_file='config.json'):
        self.config = self.load_config(config_file)
        self.feeds = self.build_feeds_dict()
    
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config: {e}")
        
        return {
            'news_sources': {
                'tech': [{'name': 'TechCrunch', 'url': 'https://techcrunch.com/feed/', 'active': True}],
                'general': [{'name': 'CNN', 'url': 'https://rss.cnn.com/rss/edition.rss', 'active': True}]
            },
            'max_articles_per_request': 5
        }
    
    def build_feeds_dict(self):
        """Build feeds dictionary from config"""
        feeds = {}
        for category, sources in self.config.get('news_sources', {}).items():
            feeds[category] = [source['url'] for source in sources if source.get('active', True)]
        return feeds
    
    def get_news(self, category='general', limit=None):
        """Fetch news from RSS feeds"""
        if category not in self.feeds:
            return []
        
        if limit is None:
            limit = self.config.get('max_articles_per_request', 5)
        
        all_entries = []
        
        for feed_url in self.feeds[category]:
            try:
                feed = feedparser.parse(feed_url)
                source_name = feed.feed.title if hasattr(feed.feed, 'title') else 'Unknown'
                
                for entry in feed.entries:
                    summary = getattr(entry, 'summary', '')
                    if len(summary) > 200:
                        summary = summary[:200] + '...'
                    
                    all_entries.append({
                        'title': entry.title,
                        'link': entry.link,
                        'summary': summary,
                        'published': getattr(entry, 'published', ''),
                        'source': source_name
                    })
            except Exception as e:
                print(f"Error fetching from {feed_url}: {e}")
        
        return sorted(all_entries, key=lambda x: x.get('published', ''), reverse=True)[:limit]
    
    def get_available_categories(self):
        """Get list of available news categories"""
        return list(self.feeds.keys())