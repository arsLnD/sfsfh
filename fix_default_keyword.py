#!/usr/bin/env python3
"""
Скрипт для исправления ключевого слова по умолчанию
"""

import asyncio
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)


async def fix_default_keyword():
    """Fix the default participation keyword"""
    try:
        from database import BotSettings, initialize_database

        logger.info("🔧 Fixing default participation keyword...")

        # Initialize database
        await initialize_database()

        # Get current keyword
        current_keyword = await BotSettings.get_participation_keyword()
        logger.info(f"Current keyword: '{current_keyword}'")

        # Set correct default keyword
        correct_keyword = "Участвую"
        success = await BotSettings.set_participation_keyword(correct_keyword)

        if success:
            # Verify the change
            new_keyword = await BotSettings.get_participation_keyword()
            logger.info(f"✅ Keyword updated successfully: '{new_keyword}'")
        else:
            logger.error("❌ Failed to update keyword")

        # Close connections
        from tortoise import Tortoise

        await Tortoise.close_connections()

        return success

    except Exception as e:
        logger.error(f"❌ Error fixing keyword: {e}")
        return False


async def main():
    """Main function"""
    logger.info("🚀 Starting keyword fix...")

    success = await fix_default_keyword()

    if success:
        logger.info("🎉 Keyword fixed successfully!")
        logger.info("The default participation keyword is now set to 'Участвую'")
    else:
        logger.error("❌ Failed to fix keyword")

    return success


if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        sys.exit(0 if result else 1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)
