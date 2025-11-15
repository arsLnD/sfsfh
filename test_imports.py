#!/usr/bin/env python3
"""
Тест импортов для проверки корректности всех модулей
"""

import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)


def test_basic_imports():
    """Test basic Python and aiogram imports"""
    try:
        import asyncio
        import datetime
        import random
        import re
        import sqlite3

        logger.info("✅ Basic Python modules imported successfully")
    except ImportError as e:
        logger.error(f"❌ Basic imports failed: {e}")
        return False

    try:
        from aiogram import Bot, Dispatcher, types
        from aiogram.dispatcher import FSMContext
        from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

        logger.info("✅ Aiogram modules imported successfully")
    except ImportError as e:
        logger.error(f"❌ Aiogram imports failed: {e}")
        return False

    return True


def test_database_imports():
    """Test database-related imports"""
    try:
        from tortoise import Model, Tortoise, fields

        logger.info("✅ Tortoise ORM imported successfully")
    except ImportError as e:
        logger.error(f"❌ Tortoise imports failed: {e}")
        return False

    try:
        from database import initialize_database

        logger.info("✅ Database initialization module imported")
    except ImportError as e:
        logger.error(f"❌ Database initialization import failed: {e}")
        return False

    try:
        from database.models import (
            BotSettings,
            GiveAway,
            GiveAwayStatistic,
            TelegramChannel,
            TemporaryUsers,
        )

        logger.info("✅ All database models imported successfully")
    except ImportError as e:
        logger.error(f"❌ Database models import failed: {e}")
        return False

    return True


def test_bot_imports():
    """Test bot-related imports"""
    try:
        from bot import bot, dp

        logger.info("✅ Bot and dispatcher imported successfully")
    except ImportError as e:
        logger.error(f"❌ Bot imports failed: {e}")
        return False

    try:
        from config import OWNERS, bot_token, timezone_info

        logger.info("✅ Configuration imported successfully")
    except ImportError as e:
        logger.error(f"❌ Config imports failed: {e}")
        return False

    return True


def test_handler_imports():
    """Test handler imports"""
    try:
        from handlers.admin.bot_settings import BotSettingsStates

        logger.info("✅ Bot settings handler imported successfully")
    except ImportError as e:
        logger.error(f"❌ Bot settings handler import failed: {e}")
        return False

    try:
        from handlers.admin.early_finish_giveaway import (
            confirm_early_finish_giveaway,
            early_finish_giveaway_confirm,
        )

        logger.info("✅ Early finish handler imported successfully")
    except ImportError as e:
        logger.error(f"❌ Early finish handler import failed: {e}")
        return False

    try:
        from handlers.admin.functions_for_active_gives.handle_group_users import (
            handle_new_users_in_groups,
        )

        logger.info("✅ Group users handler imported successfully")
    except ImportError as e:
        logger.error(f"❌ Group users handler import failed: {e}")
        return False

    return True


def test_state_imports():
    """Test state imports"""
    try:
        from states.admin.bot_settings import BotSettingsStates

        logger.info("✅ Bot settings states imported successfully")
    except ImportError as e:
        logger.error(f"❌ Bot settings states import failed: {e}")
        return False

    try:
        from states import ActiveGivesStates, CreatedGivesStates, CreateGiveStates

        logger.info("✅ All admin states imported successfully")
    except ImportError as e:
        logger.error(f"❌ Admin states import failed: {e}")
        return False

    return True


def test_keyboard_imports():
    """Test keyboard imports"""
    try:
        from keyboards.admin.inline.menu import kb_admin_menu

        logger.info("✅ Admin menu keyboard imported successfully")
    except ImportError as e:
        logger.error(f"❌ Admin menu keyboard import failed: {e}")
        return False

    try:
        from keyboards.admin.inline.active_gives import kb_admin_active_gives

        logger.info("✅ Active gives keyboard imported successfully")
    except ImportError as e:
        logger.error(f"❌ Active gives keyboard import failed: {e}")
        return False

    return True


def test_text_imports():
    """Test text constants imports"""
    try:
        from texts import (
            CANCEL_ACTION,
            CONFIRM_EARLY_FINISH,
            CURRENT_KEYWORD_TEXT,
            EARLY_FINISH_SUCCESS,
            ENTER_NEW_KEYWORD,
            KEYWORD_UPDATED_SUCCESS,
            PARTICIPATION_KEYWORD,
            SETTINGS_MENU_TEXT,
        )

        logger.info("✅ All text constants imported successfully")
    except ImportError as e:
        logger.error(f"❌ Text constants import failed: {e}")
        return False

    return True


def test_all_imports():
    """Run all import tests"""
    logger.info("🚀 Starting import tests...")
    logger.info("=" * 50)

    tests = [
        ("Basic Python modules", test_basic_imports),
        ("Database modules", test_database_imports),
        ("Bot modules", test_bot_imports),
        ("Handler modules", test_handler_imports),
        ("State modules", test_state_imports),
        ("Keyboard modules", test_keyboard_imports),
        ("Text constants", test_text_imports),
    ]

    failed_tests = []

    for test_name, test_func in tests:
        logger.info(f"Testing {test_name}...")
        try:
            if test_func():
                logger.info(f"✅ {test_name} - PASSED")
            else:
                logger.error(f"❌ {test_name} - FAILED")
                failed_tests.append(test_name)
        except Exception as e:
            logger.error(f"❌ {test_name} - ERROR: {e}")
            failed_tests.append(test_name)

        logger.info("-" * 30)

    logger.info("=" * 50)

    if failed_tests:
        logger.error(f"❌ Failed tests: {', '.join(failed_tests)}")
        logger.error("❌ IMPORT TESTS FAILED!")
        return False
    else:
        logger.info("🎉 ALL IMPORT TESTS PASSED!")
        return True


if __name__ == "__main__":
    try:
        success = test_all_imports()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("Tests cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)
