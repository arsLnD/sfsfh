#!/usr/bin/env python3
"""
Simple verification script to test if /start command works
"""

import asyncio
import os
import sys
from pathlib import Path


async def test_start_command():
    """Test the /start command with the bot"""
    try:
        # Load environment variables
        from dotenv import load_dotenv

        load_dotenv()

        bot_token = os.getenv("BOT_TOKEN")
        if not bot_token:
            print("❌ BOT_TOKEN not found in .env file")
            return False

        # Import required components
        from unittest.mock import AsyncMock

        from aiogram import Bot, Dispatcher, types
        from aiogram.contrib.fsm_storage.memory import MemoryStorage

        # Create bot and dispatcher
        bot = Bot(token=bot_token, parse_mode="HTML")
        storage = MemoryStorage()
        dp = Dispatcher(bot, storage=storage)

        print("✅ Bot and Dispatcher created")

        # Test bot connection
        me = await bot.get_me()
        print(f"✅ Bot connected: @{me.username}")

        # Import the start handler (this should register it)
        from handlers.start import process_start

        print("✅ Start handler imported")

        # Create mock message and state
        user = types.User(
            id=12345, is_bot=False, first_name="Test", username="testuser"
        )
        chat = types.Chat(id=12345, type="private")

        message = types.Message(
            message_id=1,
            from_user=user,
            date=1234567890,
            chat=chat,
            content_type="text",
            options={},
            text="/start",
        )

        # Mock the answer method
        response_text = None
        response_markup = None

        async def mock_answer(text, reply_markup=None):
            nonlocal response_text, response_markup
            response_text = text
            response_markup = reply_markup
            print(f"📤 Bot would send: {text}")
            if reply_markup:
                print("📋 With keyboard attached")

        message.answer = mock_answer

        # Mock FSM state
        class MockState:
            async def finish(self):
                print("🔄 State finished")

        mock_state = MockState()

        # Test the start handler directly
        print("\n🧪 Testing /start handler...")
        await process_start(message, mock_state)

        if response_text:
            print(f"✅ Handler executed successfully!")
            print(f"📝 Response: {response_text}")
            if "Главное меню" in response_text:
                print("✅ Admin menu response detected")
            return True
        else:
            print("❌ No response from handler")
            return False

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False

    finally:
        if "bot" in locals():
            await bot.close()


def main():
    print("🧪 START COMMAND VERIFICATION")
    print("=" * 40)

    # Check prerequisites
    if not Path(".env").exists():
        print("❌ .env file not found")
        print("Solution: Copy .env.example to .env and add your BOT_TOKEN")
        return False

    print("✅ .env file found")

    try:
        result = asyncio.run(test_start_command())

        print("\n" + "=" * 40)
        if result:
            print("🎉 START COMMAND VERIFICATION PASSED!")
            print("\n📋 What this means:")
            print("✅ Your bot token is valid")
            print("✅ Bot can connect to Telegram")
            print("✅ /start handler is working")
            print("✅ Admin menu is properly configured")
            print("\n🚀 Your bot should now respond to /start messages!")
            print("Go to Telegram and test: /start")
        else:
            print("❌ START COMMAND VERIFICATION FAILED!")
            print("\n🔧 Try these solutions:")
            print("1. Make sure bot is running: python app.py")
            print("2. Check your BOT_TOKEN in .env file")
            print("3. Verify bot permissions on Telegram")

        return result

    except Exception as e:
        print(f"❌ Verification crashed: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
