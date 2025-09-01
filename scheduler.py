import asyncio
import schedule
import time
from datetime import datetime
import threading
from telegram import Bot
from news_fetcher import NewsFetcher
from user_data import UserDataManager

class NewsScheduler:
    def __init__(self, bot_token: str):
        self.bot = Bot(token=bot_token)
        self.news_fetcher = NewsFetcher()
        self.user_manager = UserDataManager()
        self.running = False
    
    async def send_scheduled_news(self, category: str = 'general'):
        """Send scheduled news to subscribed users"""
        try:
            news_items = self.news_fetcher.get_news(category, 2)
            
            if not news_items:
                return
            
            active_users = self.user_manager.get_all_active_users()
            
            for user_id_str in active_users:
                user_subscriptions = self.user_manager.get_user_subscriptions(int(user_id_str))
                
                if category in user_subscriptions:
                    try:
                        await self.bot.send_message(
                            chat_id=int(user_id_str),
                            text=f"📰 *Daily {category.title()} News Update*",
                            parse_mode='Markdown'
                        )
                        
                        for item in news_items:
                            message = f"• *{item['title']}*\n\n{item['summary']}\n\n[Read more]({item['link']})"
                            await self.bot.send_message(
                                chat_id=int(user_id_str),
                                text=message,
                                parse_mode='Markdown',
                                disable_web_page_preview=True
                            )
                            await asyncio.sleep(1)
                        
                    except Exception as e:
                        print(f"Error sending news to user {user_id_str}: {e}")
                        
        except Exception as e:
            print(f"Error in scheduled news delivery: {e}")
    
    def schedule_news_job(self):
        """Wrapper function for scheduled job"""
        asyncio.run(self.send_scheduled_news('general'))
        asyncio.run(self.send_scheduled_news('tech'))
    
    def start_scheduler(self):
        """Start the news scheduler"""
        schedule.every().day.at("09:00").do(self.schedule_news_job)
        schedule.every().day.at("18:00").do(self.schedule_news_job)
        
        self.running = True
        
        def run_schedule():
            while self.running:
                schedule.run_pending()
                time.sleep(60)
        
        scheduler_thread = threading.Thread(target=run_schedule, daemon=True)
        scheduler_thread.start()
        print("News scheduler started - will deliver news at 9:00 AM and 6:00 PM daily")
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        self.running = False
        schedule.clear()