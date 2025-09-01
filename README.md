# Telegram News Bot

A simple Telegram bot that fetches and delivers news from various RSS sources.

## Features

- Fetch latest general news
- Get tech news updates
- Simple command interface
- RSS feed parsing from multiple sources

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

- `/start` - Start the bot
- `/help` - Show available commands
- `/news` - Get latest general news (3 articles)
- `/tech` - Get latest tech news (3 articles)

## News Sources

- General: CNN, BBC World News
- Tech: TechCrunch, The Verge