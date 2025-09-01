import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from news_fetcher import NewsFetcher
from user_data import UserDataManager
from scheduler import NewsScheduler

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
news_fetcher = NewsFetcher()
user_manager = UserDataManager()
scheduler = NewsScheduler(BOT_TOKEN)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user_id = update.effective_user.id
    username = update.effective_user.username
    
    user_manager.register_user(user_id, username)
    await update.message.reply_text('Hi! I am your news bot. Use /help to see available commands.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    help_text = """
Available commands:
/start - Start the bot
/help - Show this help message
/news - Get latest general news
/tech - Get latest tech news
/business - Get latest business news
/subscribe - Subscribe to news categories
/unsubscribe - Unsubscribe from categories
/mysubs - Show your subscriptions
    """
    await update.message.reply_text(help_text)

async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send latest general news."""
    try:
        await update.message.reply_text("Fetching latest news...")
        
        news_items = news_fetcher.get_news('general', 3)
        
        if not news_items:
            await update.message.reply_text("Sorry, no news available right now. Please try again later.")
            logger.warning("No news items returned for general category")
            return
        
        for item in news_items:
            try:
                message = f"📰 *{item['title']}*\n\n{item['summary']}\n\nSource: {item['source']}\n[Read more]({item['link']})"
                await update.message.reply_text(message, parse_mode='Markdown', disable_web_page_preview=True)
            except Exception as e:
                logger.error(f"Error sending news item: {e}")
                
    except Exception as e:
        logger.error(f"Error in news_command: {e}")
        await update.message.reply_text("Sorry, there was an error fetching news. Please try again later.")

async def tech_news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send latest tech news."""
    try:
        await update.message.reply_text("Fetching latest tech news...")
        
        news_items = news_fetcher.get_news('tech', 3)
        
        if not news_items:
            await update.message.reply_text("Sorry, no tech news available right now. Please try again later.")
            logger.warning("No news items returned for tech category")
            return
        
        for item in news_items:
            try:
                message = f"💻 *{item['title']}*\n\n{item['summary']}\n\nSource: {item['source']}\n[Read more]({item['link']})"
                await update.message.reply_text(message, parse_mode='Markdown', disable_web_page_preview=True)
            except Exception as e:
                logger.error(f"Error sending tech news item: {e}")
                
    except Exception as e:
        logger.error(f"Error in tech_news_command: {e}")
        await update.message.reply_text("Sorry, there was an error fetching tech news. Please try again later.")

async def subscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Subscribe to news categories."""
    try:
        user_id = update.effective_user.id
        available_categories = news_fetcher.get_available_categories()
        
        if not context.args:
            categories_text = ', '.join(available_categories)
            await update.message.reply_text(f"Please specify a category to subscribe to.\nAvailable: {categories_text}\nExample: /subscribe tech")
            return
        
        category = context.args[0].lower()
        
        if category not in available_categories:
            categories_text = ', '.join(available_categories)
            await update.message.reply_text(f"Invalid category. Available categories: {categories_text}")
            return
        
        user_manager.register_user(user_id, update.effective_user.username)
        
        if user_manager.add_subscription(user_id, category):
            await update.message.reply_text(f"✅ Successfully subscribed to {category} news!")
            logger.info(f"User {user_id} subscribed to {category}")
        else:
            await update.message.reply_text(f"❌ You're already subscribed to {category} news!")
            
    except Exception as e:
        logger.error(f"Error in subscribe_command: {e}")
        await update.message.reply_text("Sorry, there was an error processing your subscription. Please try again.")

async def unsubscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unsubscribe from news categories."""
    user_id = update.effective_user.id
    
    if not context.args:
        subs = user_manager.get_user_subscriptions(user_id)
        if subs:
            await update.message.reply_text(f"Please specify a category to unsubscribe from.\nYour subscriptions: {', '.join(subs)}\nExample: /unsubscribe tech")
        else:
            await update.message.reply_text("You have no active subscriptions.")
        return
    
    category = context.args[0].lower()
    
    if user_manager.remove_subscription(user_id, category):
        await update.message.reply_text(f"✅ Successfully unsubscribed from {category} news!")
    else:
        await update.message.reply_text(f"❌ You weren't subscribed to {category} news!")

async def mysubs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user's subscriptions."""
    user_id = update.effective_user.id
    subscriptions = user_manager.get_user_subscriptions(user_id)
    
    if subscriptions:
        subs_text = '\n'.join([f"• {sub}" for sub in subscriptions])
        await update.message.reply_text(f"📰 Your subscriptions:\n{subs_text}")
    else:
        await update.message.reply_text("You have no active subscriptions.\nUse /subscribe <category> to subscribe to news.")

async def business_news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send latest business news."""
    try:
        await update.message.reply_text("Fetching latest business news...")
        
        news_items = news_fetcher.get_news('business', 3)
        
        if not news_items:
            await update.message.reply_text("Sorry, no business news available right now. Please try again later.")
            logger.warning("No news items returned for business category")
            return
        
        for item in news_items:
            try:
                message = f"📈 *{item['title']}*\n\n{item['summary']}\n\nSource: {item['source']}\n[Read more]({item['link']})"
                await update.message.reply_text(message, parse_mode='Markdown', disable_web_page_preview=True)
            except Exception as e:
                logger.error(f"Error sending business news item: {e}")
                
    except Exception as e:
        logger.error(f"Error in business_news_command: {e}")
        await update.message.reply_text("Sorry, there was an error fetching business news. Please try again later.")

def main():
    """Run the bot."""
    if not BOT_TOKEN:
        logger.error("No bot token provided!")
        return
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("news", news_command))
    application.add_handler(CommandHandler("tech", tech_news_command))
    application.add_handler(CommandHandler("business", business_news_command))
    application.add_handler(CommandHandler("subscribe", subscribe_command))
    application.add_handler(CommandHandler("unsubscribe", unsubscribe_command))
    application.add_handler(CommandHandler("mysubs", mysubs_command))
    
    scheduler.start_scheduler()
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()