import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from news_fetcher import NewsFetcher

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
news_fetcher = NewsFetcher()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Hi! I am your news bot. Use /help to see available commands.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    help_text = """
Available commands:
/start - Start the bot
/help - Show this help message
/news - Get latest general news
/tech - Get latest tech news
    """
    await update.message.reply_text(help_text)

async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send latest general news."""
    await update.message.reply_text("Fetching latest news...")
    
    news_items = news_fetcher.get_news('general', 3)
    
    if not news_items:
        await update.message.reply_text("Sorry, no news available right now.")
        return
    
    for item in news_items:
        message = f"📰 *{item['title']}*\n\n{item['summary']}\n\n[Read more]({item['link']})"
        await update.message.reply_text(message, parse_mode='Markdown', disable_web_page_preview=True)

async def tech_news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send latest tech news."""
    await update.message.reply_text("Fetching latest tech news...")
    
    news_items = news_fetcher.get_news('tech', 3)
    
    if not news_items:
        await update.message.reply_text("Sorry, no tech news available right now.")
        return
    
    for item in news_items:
        message = f"💻 *{item['title']}*\n\n{item['summary']}\n\n[Read more]({item['link']})"
        await update.message.reply_text(message, parse_mode='Markdown', disable_web_page_preview=True)

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
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()