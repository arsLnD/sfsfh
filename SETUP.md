# Telegram Giveaway Bot Setup Guide

## Prerequisites

- Python 3.8 or higher
- PostgreSQL database (optional, SQLite is used by default)
- Telegram Bot Token from [@BotFather](https://t.me/BotFather)

## Installation

1. **Clone the repository or navigate to the project directory**
   ```bash
   cd telegram-giveaway-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create environment configuration**
   ```bash
   cp .env.example .env
   ```

4. **Configure your bot settings**
   
   Edit the `.env` file and set your configuration:
   
   ```env
   # Required: Get this from @BotFather on Telegram
   BOT_TOKEN=your_bot_token_here
   
   # Optional: Database URL (SQLite is used by default)
   DATABASE_URL=sqlite://db.sqlite3
   
   # Optional: Your timezone
   TIMEZONE=Europe/Moscow
   
   # Optional: Owner user IDs (comma-separated)
   OWNERS=123456789,987654321
   ```

## Getting a Bot Token

1. Start a conversation with [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` command
3. Choose a name for your bot
4. Choose a username for your bot (must end with 'bot')
5. Copy the token provided by BotFather
6. Paste it in your `.env` file as `BOT_TOKEN`

## Database Setup

### SQLite (Default - No additional setup required)
The bot will automatically create an SQLite database file when you first run it.

### PostgreSQL (Production recommended)
1. Create a PostgreSQL database
2. Update the `DATABASE_URL` in your `.env` file:
   ```env
   DATABASE_URL=postgresql://username:password@host:port/database_name
   ```

## Running the Bot

1. **Start the bot**
   ```bash
   python app.py
   ```

2. **Verify the bot is running**
   - Send `/start` to your bot on Telegram
   - You should see the main menu

## Features Configuration

### Setting Up Channels for Giveaways

1. Add your bot as an administrator to your Telegram channel
2. If using "comments" type giveaways, also add the bot to the associated group
3. Use the bot's admin panel to add channels

### Admin Commands

- `/start` - Access main menu
- Create giveaways through the inline keyboard
- Manage active and created giveaways
- View results and statistics

## Giveaway Types

### Button Giveaways
- Users participate by clicking a button
- Optional CAPTCHA protection against bots
- Subscription verification to required channels

### Comment Giveaways
- Users participate by commenting with a keyword
- Requires both channel and associated group
- Automatic monitoring of new participants

## Troubleshooting

### Common Issues

1. **"Token is invalid" error**
   - Verify your BOT_TOKEN in the .env file
   - Make sure there are no extra spaces
   - Get a new token from @BotFather if needed

2. **Database connection errors**
   - Check your DATABASE_URL format
   - Ensure database server is running (for PostgreSQL/MySQL)
   - For SQLite, ensure the directory is writable

3. **Bot doesn't respond to commands**
   - Check if bot is running without errors
   - Verify bot token is correct
   - Make sure you're messaging the correct bot

4. **Channel subscription check not working**
   - Ensure bot is added as administrator to channels
   - Check channel IDs are correct
   - For comment giveaways, bot needs to be in both channel and group

### Debug Mode

Enable debug mode in your `.env` file:
```env
DEBUG=True
```

This will provide more detailed logging information.

## Production Deployment

### Using Webhook (Recommended for production)

1. Set up your webhook URL in `.env`:
   ```env
   WEBHOOK_URL=https://yourdomain.com/webhook
   WEBHOOK_PATH=/webhook
   ```

2. Modify `app.py` to use webhook instead of polling (see aiogram documentation)

### Environment Variables for Production

Make sure to set these environment variables on your server:
- `BOT_TOKEN`
- `DATABASE_URL`
- `TIMEZONE`
- `OWNERS`

### Database Migration

For production, use PostgreSQL:
```env
DATABASE_URL=postgresql://username:password@host:port/database_name
```

## Security Notes

- Never commit your `.env` file to version control
- Keep your bot token secure
- Use environment variables in production
- Regularly update your dependencies
- Consider using Redis for session storage in high-traffic scenarios

## Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Verify your configuration
3. Check the bot logs for error messages
4. Ensure all prerequisites are met