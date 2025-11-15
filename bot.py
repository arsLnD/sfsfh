import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import ValidationError
from config import bot_token

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
try:
    if not bot_token:
        raise ValueError("BOT_TOKEN is not set. Please check your .env file")

    bot = Bot(token=bot_token, parse_mode="HTML")
    logger.info("Bot initialized successfully")
except ValidationError:
    logger.error("Invalid bot token provided. Please check your BOT_TOKEN in .env file")
    bot = None
except Exception as e:
    logger.error(f"Failed to initialize bot: {e}")
    bot = None

# Create storage and dispatcher
storage = MemoryStorage()
if bot:
    dp = Dispatcher(bot, storage=storage)
else:
    dp = None
    logger.error("Dispatcher not created due to bot initialization failure")
