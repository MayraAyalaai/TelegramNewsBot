# Telegram News Bot

A comprehensive Telegram bot that fetches and delivers news from various RSS sources with advanced features.

## Features

- 📰 Multi-category news fetching (General, Tech, Business)
- 🔔 User subscription system with automated delivery
- ⏰ Scheduled news delivery (9 AM & 6 PM daily)
- 📊 Usage analytics and statistics tracking
- 🛡️ Rate limiting to prevent abuse
- 👑 Admin commands for bot management
- ⚙️ Configurable news sources via JSON

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file based on `.env.example`:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   ```

4. Get your bot token from @BotFather on Telegram

5. Run the bot:
   ```
   python main.py
   ```

## Available Commands

### User Commands
- `/start` - Start the bot and register
- `/help` - Show available commands
- `/news` - Get latest general news (3 articles)
- `/tech` - Get latest tech news (3 articles)
- `/business` - Get latest business news (3 articles)
- `/subscribe <category>` - Subscribe to news category
- `/unsubscribe <category>` - Unsubscribe from category
- `/mysubs` - Show your active subscriptions

### Admin Commands
- `/adminstats` - View bot usage statistics
- `/broadcast <message>` - Send message to all users
- `/userinfo <user_id>` - Get user information and stats

## News Sources

### General News
- CNN World News
- BBC World News
- Reuters World News

### Technology
- TechCrunch
- The Verge
- Ars Technica

### Business
- Bloomberg Markets
- Financial Times (configurable)

## Rate Limiting

- 10 requests per minute per user
- 100 requests per hour per user
- Automatic cleanup of old request records

## Configuration

Edit `config.json` to:
- Add/remove news sources
- Configure admin user IDs
- Adjust delivery schedules
- Set rate limiting parameters