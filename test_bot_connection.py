#!/usr/bin/env python3
"""
Simple Bot Connection Test - Tests if bot token is valid and bot responds
"""

import asyncio
import os
import sys
from pathlib import Path


async def test_bot_connection():
    """Test bot connection and /start command response"""
    try:
        # Load environment variables
        from dotenv import load_dotenv

        load_dotenv()

        bot_token = os.getenv("BOT_TOKEN")

        if not bot_token:
            print("❌ BOT_TOKEN not found in .env file")
            print("Solution: Add BOT_TOKEN=your_token_here to .env file")
            return False

        print(f"✅ Found BOT_TOKEN (length: {len(bot_token)})")

        # Import aiogram components
        from aiogram import Bot, Dispatcher, types
        from aiogram.contrib.fsm_storage.memory import MemoryStorage

        # Create bot instance
        bot = Bot(token=bot_token, parse_mode="HTML")
        storage = MemoryStorage()
        dp = Dispatcher(bot, storage=storage)

        print("✅ Bot and Dispatcher created successfully")

        # Test bot connection
        try:
            me = await bot.get_me()
            print(f"✅ Bot connection successful!")
            print(f"   Bot name: @{me.username}")
            print(f"   Bot ID: {me.id}")
            print(f"   Bot first name: {me.first_name}")
        except Exception as e:
            print(f"❌ Bot connection failed: {e}")
            await bot.close()
            return False

        # Register a simple start handler
        @dp.message_handler(commands=["start"])
        async def test_start_handler(message: types.Message):
            await message.answer(
                "✅ Bot is working! This is a test response.", reply_markup=None
            )
            print(f"✅ Received /start from user {message.from_user.id}")

        print("✅ Test handler registered")

        # Test the handler registration
        handlers = dp.message_handlers.handlers
        start_handlers = [
            h for h in handlers if hasattr(h, "filters") and "start" in str(h.filters)
        ]

        if start_handlers:
            print(f"✅ Found {len(start_handlers)} start command handler(s)")
        else:
            print("⚠️  No start handlers found registered")

        print("\n" + "=" * 50)
        print("🚀 MANUAL TEST INSTRUCTIONS")
        print("=" * 50)
        print("1. Keep this script running")
        print("2. Go to Telegram and find your bot")
        print("3. Send /start to your bot")
        print("4. You should receive: '✅ Bot is working! This is a test response.'")
        print("5. Check this console for confirmation messages")
        print("6. Press Ctrl+C to stop the test")
        print("=" * 50)

        # Start polling
        from aiogram import executor

        async def on_startup(dp):
            print("🤖 Test bot started and ready to receive messages!")

        async def on_shutdown(dp):
            print("🛑 Test bot stopped")
            await bot.close()

        try:
            executor.start_polling(
                dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown
            )
        except KeyboardInterrupt:
            print("\n✅ Test stopped by user")
            await bot.close()
            return True

    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Solution: pip install -r requirements.txt")
        return False

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def check_prerequisites():
    """Check if all prerequisites are met"""
    print("🔍 CHECKING PREREQUISITES")
    print("=" * 50)

    # Check .env file
    if not Path(".env").exists():
        print("❌ .env file not found")
        print("Solution: Copy .env.example to .env and add your BOT_TOKEN")
        return False
    print("✅ .env file found")

    # Check requirements
    try:
        import aiogram
        import dotenv

        print("✅ Required packages installed")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Solution: pip install -r requirements.txt")
        return False

    return True


def main():
    """Main function"""
    print("🤖 TELEGRAM BOT CONNECTION TEST")
    print("This will test if your bot token works and can receive messages")
    print()

    if not check_prerequisites():
        sys.exit(1)

    print("\n🚀 Starting connection test...")

    try:
        asyncio.run(test_bot_connection())
    except KeyboardInterrupt:
        print("\n✅ Test completed")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
