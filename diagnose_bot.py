#!/usr/bin/env python3
"""
Bot Diagnostic Script - Identifies issues with bot setup and connection
"""

import asyncio
import os
import sys
from pathlib import Path


def check_env_file():
    """Check if .env file exists and has BOT_TOKEN"""
    print("=" * 50)
    print("CHECKING ENVIRONMENT CONFIGURATION")
    print("=" * 50)

    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found!")
        print("Solution: Copy .env.example to .env and add your BOT_TOKEN")
        return False

    print("✅ .env file exists")

    # Load environment variables
    try:
        from dotenv import load_dotenv

        load_dotenv()

        bot_token = os.getenv("BOT_TOKEN")
        if not bot_token:
            print("❌ BOT_TOKEN not set in .env file")
            print("Solution: Add BOT_TOKEN=your_token_here to .env file")
            return False

        if bot_token.strip() == "":
            print("❌ BOT_TOKEN is empty in .env file")
            return False

        print(f"✅ BOT_TOKEN found (length: {len(bot_token)})")

        # Basic token format check
        if ":" not in bot_token:
            print("⚠️  BOT_TOKEN format looks incorrect (should contain ':')")
            print("Example: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz")
            return False

        print("✅ BOT_TOKEN format looks correct")
        return True

    except ImportError:
        print("❌ python-dotenv not installed")
        print("Solution: pip install python-dotenv")
        return False
    except Exception as e:
        print(f"❌ Error loading .env: {e}")
        return False


def test_bot_token():
    """Test if bot token is valid by creating Bot instance"""
    print("\n" + "=" * 50)
    print("TESTING BOT TOKEN VALIDITY")
    print("=" * 50)

    try:
        from dotenv import load_dotenv

        load_dotenv()

        from aiogram import Bot
        from aiogram.utils.exceptions import Unauthorized, ValidationError

        bot_token = os.getenv("BOT_TOKEN")
        if not bot_token:
            print("❌ No BOT_TOKEN to test")
            return False

        print("Creating Bot instance...")
        bot = Bot(token=bot_token)
        print("✅ Bot instance created successfully")

        # Test bot connection
        async def test_connection():
            try:
                me = await bot.get_me()
                print(f"✅ Bot connection successful!")
                print(f"   Bot name: @{me.username}")
                print(f"   Bot ID: {me.id}")
                print(f"   Bot first name: {me.first_name}")
                await bot.close()
                return True
            except Unauthorized:
                print("❌ Bot token is invalid or unauthorized")
                await bot.close()
                return False
            except Exception as e:
                print(f"❌ Bot connection failed: {e}")
                await bot.close()
                return False

        return asyncio.run(test_connection())

    except ValidationError:
        print("❌ Invalid bot token format")
        return False
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Solution: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Error testing bot token: {e}")
        return False


def check_handlers():
    """Check if handlers are properly configured"""
    print("\n" + "=" * 50)
    print("CHECKING HANDLERS CONFIGURATION")
    print("=" * 50)

    try:
        # Set dummy token to avoid validation during import
        os.environ["BOT_TOKEN"] = "123456789:dummy_token_for_import_test_only"

        # Check if start handler exists
        start_handler_file = Path("handlers/start.py")
        if not start_handler_file.exists():
            print("❌ handlers/start.py not found")
            return False

        print("✅ Start handler file exists")

        # Check if handler has correct structure
        with open(start_handler_file, "r", encoding="utf-8") as f:
            content = f.read()

        if "@dp.message_handler" not in content:
            print("❌ Start handler missing @dp.message_handler decorator")
            return False

        if "commands=['start']" not in content and 'commands=["start"]' not in content:
            print("❌ Start handler missing commands=['start'] parameter")
            return False

        if "process_start" not in content:
            print("❌ Start handler missing process_start function")
            return False

        print("✅ Start handler structure looks correct")

        # Check keyboard import
        try:
            from keyboards import kb_admin_menu

            print("✅ Admin menu keyboard imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import admin menu keyboard: {e}")
            return False

        return True

    except Exception as e:
        print(f"❌ Error checking handlers: {e}")
        return False


def check_database():
    """Check database configuration"""
    print("\n" + "=" * 50)
    print("CHECKING DATABASE CONFIGURATION")
    print("=" * 50)

    try:
        from dotenv import load_dotenv

        load_dotenv()

        database_url = os.getenv("DATABASE_URL", "sqlite://db.sqlite3")
        print(f"✅ Database URL: {database_url}")

        # Test database models import
        os.environ["BOT_TOKEN"] = "123456789:dummy_token_for_import_test_only"

        from database.models import (
            GiveAway,
            GiveAwayStatistic,
            TelegramChannel,
            TemporaryUsers,
        )

        print("✅ Database models imported successfully")

        return True

    except Exception as e:
        print(f"❌ Database check failed: {e}")
        return False


def test_full_import():
    """Test importing the full application"""
    print("\n" + "=" * 50)
    print("TESTING FULL APPLICATION IMPORT")
    print("=" * 50)

    # Store original token
    original_token = os.environ.get("BOT_TOKEN")

    try:
        # Load real token
        from dotenv import load_dotenv

        load_dotenv()

        real_token = os.getenv("BOT_TOKEN")
        if not real_token:
            print("❌ No BOT_TOKEN set - cannot test full import")
            return False

        print("Attempting to import app module...")

        # Clear any cached imports
        modules_to_clear = [
            key
            for key in sys.modules.keys()
            if key.startswith(("app", "handlers", "config"))
        ]
        for module in modules_to_clear:
            if module in sys.modules:
                del sys.modules[module]

        import app

        print("✅ App module imported successfully")

        if hasattr(app, "bot") and app.bot:
            print("✅ Bot instance created successfully")
        else:
            print("❌ Bot instance not found in app module")
            return False

        if hasattr(app, "dp") and app.dp:
            print("✅ Dispatcher created successfully")
        else:
            print("❌ Dispatcher not found in app module")
            return False

        return True

    except Exception as e:
        print(f"❌ Failed to import app: {e}")
        return False
    finally:
        # Restore original token
        if original_token:
            os.environ["BOT_TOKEN"] = original_token


async def test_start_command():
    """Test the start command handler directly"""
    print("\n" + "=" * 50)
    print("TESTING START COMMAND HANDLER")
    print("=" * 50)

    try:
        from dotenv import load_dotenv

        load_dotenv()

        bot_token = os.getenv("BOT_TOKEN")
        if not bot_token:
            print("❌ No BOT_TOKEN to test")
            return False

        from unittest.mock import AsyncMock

        from aiogram import Bot
        from aiogram.types import Chat, Message, User

        # Create mock message
        user = User(id=12345, is_bot=False, first_name="Test", username="testuser")
        chat = Chat(id=12345, type="private")
        message = Message(
            message_id=1,
            from_user=user,
            date=1234567890,
            chat=chat,
            content_type="text",
            options={},
            text="/start",
        )

        # Mock the answer method
        message.answer = AsyncMock()

        # Import and test the handler
        from unittest.mock import MagicMock

        from aiogram.dispatcher import FSMContext
        from handlers.start import process_start

        # Create mock state
        mock_state = MagicMock()
        mock_state.finish = AsyncMock()

        print("Testing start handler function...")
        await process_start(message, mock_state)

        print("✅ Start handler executed without errors")
        print(f"✅ Message.answer was called: {message.answer.called}")

        if message.answer.called:
            call_args = message.answer.call_args
            print(f"✅ Response text: {call_args[1].get('text', 'No text provided')}")

        return True

    except Exception as e:
        print(f"❌ Start command handler test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def provide_solutions():
    """Provide common solutions"""
    print("\n" + "=" * 50)
    print("COMMON SOLUTIONS")
    print("=" * 50)

    print("1. GET BOT TOKEN:")
    print("   - Go to @BotFather on Telegram")
    print("   - Send /newbot and follow instructions")
    print("   - Copy the token to your .env file")
    print()

    print("2. INSTALL DEPENDENCIES:")
    print("   pip install -r requirements.txt")
    print()

    print("3. CONFIGURE ENVIRONMENT:")
    print("   - Copy .env.example to .env")
    print("   - Add your BOT_TOKEN to .env file")
    print("   - Format: BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz")
    print()

    print("4. RUN THE BOT:")
    print("   python app.py")
    print()

    print("5. TEST THE BOT:")
    print("   - Send /start to your bot on Telegram")
    print("   - Should receive the admin menu")


def main():
    """Run all diagnostic tests"""
    print("🔍 TELEGRAM GIVEAWAY BOT DIAGNOSTIC")
    print("This script will help identify why your bot isn't responding to /start")
    print()

    tests = [
        check_env_file,
        test_bot_token,
        check_database,
        check_handlers,
        test_full_import,
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)
        print()

    # Test async function
    try:
        print("Running async start command test...")
        result = asyncio.run(test_start_command())
        results.append(result)
    except Exception as e:
        print(f"❌ Async test failed: {e}")
        results.append(False)

    print("\n" + "=" * 50)
    print("DIAGNOSTIC SUMMARY")
    print("=" * 50)

    passed = sum(results)
    total = len(results)

    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")

    if all(results):
        print("\n🎉 All tests passed! Your bot should be working.")
        print("If it's still not responding:")
        print("1. Make sure you're messaging the correct bot")
        print("2. Try stopping and restarting: python app.py")
        print("3. Check the bot.log file for errors")
    else:
        print(f"\n❌ {total - passed} issues found. See solutions below:")
        provide_solutions()


if __name__ == "__main__":
    main()
