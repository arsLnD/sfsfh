import asyncio
import logging
import sys

from aiogram import executor
from bot import bot, dp, logger
from config import bot_token
from database import initialize_database
from tortoise import Tortoise, run_async


async def on_startup(dispatcher):
    """Bot startup handler"""
    logger.info("Bot is starting up...")

    try:
        # Start giveaway monitoring
        from handlers.admin.functions_for_active_gives.monitoring_giveaways import (
            manage_active_giveaways,
        )

        asyncio.create_task(manage_active_giveaways())
        logger.info("Giveaway monitoring started")

    except Exception as e:
        logger.error(f"Failed to start bot services: {e}")
        raise


async def on_shutdown(dispatcher):
    """Bot shutdown handler"""
    logger.info("Bot is shutting down...")

    # Close bot session
    if bot:
        await bot.close()

    # Close database connections
    await Tortoise.close_connections()

    logger.info("Bot shutdown complete")


def main():
    """Main function to run the bot"""
    if not bot_token:
        logger.error("BOT_TOKEN is not set. Please check your .env file")
        sys.exit(1)

    if not bot or not dp:
        logger.error("Bot or Dispatcher not initialized. Check your configuration.")
        sys.exit(1)

    # Initialize database
    run_async(initialize_database())
    logger.info("Database initialized successfully")

    # Import all handlers (this registers them with the dispatcher)
    import handlers

    logger.info("All handlers imported and registered")
    logger.info("Starting bot polling...")

    try:
        executor.start_polling(
            dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown
        )
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot encountered an error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
