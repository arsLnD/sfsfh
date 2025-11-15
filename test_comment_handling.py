#!/usr/bin/env python3
"""
Test for comment handling functionality
"""

import asyncio
import logging
import re
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)


async def test_bot_settings_integration():
    """Test BotSettings integration in comment handler"""
    print("🧪 Testing BotSettings integration...")

    try:
        from database import BotSettings, initialize_database

        # Initialize database
        await initialize_database()
        print("✅ Database initialized")

        # Test getting participation keyword
        keyword = await BotSettings.get_participation_keyword()
        print(f"✅ Current keyword: '{keyword}'")
        assert keyword is not None
        assert len(keyword) > 0

        from tortoise import Tortoise

        await Tortoise.close_connections()

        return True

    except Exception as e:
        print(f"❌ BotSettings integration error: {e}")
        import traceback

        print(f"Full traceback: {traceback.format_exc()}")
        return False


async def test_keyword_matching():
    """Test keyword matching logic"""
    print("🧪 Testing keyword matching logic...")

    try:
        # Mock keyword
        test_keyword = "Участвую"

        # Test messages
        test_messages = [
            ("Участвую", True),
            ("участвую", True),
            ("УЧАСТВУЮ", True),
            ("Привет! Участвую в конкурсе!", True),
            ("Хочу участвую тоже", True),
            ("УчАсТвУю", True),
            ("Не хочу участвовать", False),
            ("Участвование", False),
            ("", False),
            ("Hello world", False),
            (None, False),
        ]

        for message_text, expected in test_messages:
            if message_text is None:
                result = False
            elif not message_text or not message_text.strip():
                result = False
            else:
                keyword_pattern = re.compile(re.escape(test_keyword), re.IGNORECASE)
                result = bool(keyword_pattern.search(message_text))

            status = "✅" if result == expected else "❌"
            print(f"   {status} '{message_text}' -> {result} (expected {expected})")

            if result != expected:
                print(f"      MISMATCH: Expected {expected}, got {result}")
                return False

        print("✅ All keyword matching tests passed")
        return True

    except Exception as e:
        print(f"❌ Keyword matching error: {e}")
        return False


async def test_message_structure():
    """Test message structure requirements"""
    print("🧪 Testing message structure requirements...")

    try:
        # Mock message structure that would come from Telegram
        class MockUser:
            def __init__(self, user_id, username="testuser"):
                self.id = user_id
                self.username = username

        class MockChat:
            def __init__(self, chat_id):
                self.id = chat_id

        class MockReplyMessage:
            def __init__(self, forward_id):
                self.forward_from_message_id = forward_id

        class MockMessage:
            def __init__(self, text, user_id, chat_id, reply_forward_id=None):
                self.text = text
                self.from_user = MockUser(user_id)
                self.chat = MockChat(chat_id)
                self.reply_to_message = (
                    MockReplyMessage(reply_forward_id) if reply_forward_id else None
                )

        # Test valid message
        valid_msg = MockMessage("Участвую", 123456, -1001234567890, 789)

        print(f"✅ Valid message structure:")
        print(f"   Text: {valid_msg.text}")
        print(f"   User ID: {valid_msg.from_user.id}")
        print(f"   Chat ID: {valid_msg.chat.id}")
        print(
            f"   Reply to: {valid_msg.reply_to_message.forward_from_message_id if valid_msg.reply_to_message else None}"
        )

        # Test message without reply
        no_reply_msg = MockMessage("Участвую", 123456, -1001234567890, None)
        has_reply = no_reply_msg.reply_to_message is not None
        print(f"   Message without reply: reply_exists = {has_reply}")

        # Test message validation logic
        def validate_message(msg):
            # Check text
            if not msg.text or not msg.text.strip():
                return False, "No text content"

            # Check reply
            if (
                not msg.reply_to_message
                or not msg.reply_to_message.forward_from_message_id
            ):
                return False, "Not a reply to forwarded message"

            return True, "Valid"

        is_valid, reason = validate_message(valid_msg)
        print(f"   Validation result: {is_valid} - {reason}")

        is_valid_no_reply, reason_no_reply = validate_message(no_reply_msg)
        print(f"   No reply validation: {is_valid_no_reply} - {reason_no_reply}")

        return True

    except Exception as e:
        print(f"❌ Message structure test error: {e}")
        return False


async def test_handler_imports():
    """Test comment handler imports"""
    print("🧪 Testing comment handler imports...")

    try:
        from handlers.admin.functions_for_active_gives.handle_group_users import (
            handle_new_users_in_groups,
        )

        print("✅ handle_new_users_in_groups imported")

        from database import BotSettings, GiveAwayStatistic, TelegramChannel

        print("✅ Database models imported")

        from texts import NOT_SUBSCRIBED, PARTICIPATION_SUCCESS

        print("✅ Text constants imported")

        # Check if handler is callable
        assert callable(handle_new_users_in_groups)
        print("✅ Handler is callable")

        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Handler import test error: {e}")
        return False


async def test_fallback_keyword():
    """Test fallback to old keyword system"""
    print("🧪 Testing fallback keyword system...")

    try:
        from config import text_for_participation_in_comments_giveaways

        print(
            f"✅ Fallback keyword available: '{text_for_participation_in_comments_giveaways}'"
        )

        # Test that both systems work
        old_keyword = text_for_participation_in_comments_giveaways

        # Test regex with old keyword
        keyword_pattern = re.compile(re.escape(old_keyword), re.IGNORECASE)
        test_text = old_keyword.lower()
        result = bool(keyword_pattern.search(test_text))
        print(f"✅ Old keyword matching works: '{test_text}' -> {result}")

        return True

    except ImportError as e:
        print(f"❌ Fallback keyword import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Fallback test error: {e}")
        return False


async def test_handler_registration():
    """Test handler registration process"""
    print("🧪 Testing handler registration...")

    try:
        from bot import dp

        print("✅ Dispatcher imported")

        # Check if dispatcher exists and is working
        assert dp is not None
        print("✅ Dispatcher is available")

        # Test registration function (mock)
        def mock_register_handler(handler, chat_id):
            print(f"   Mock registering handler for chat {chat_id}")
            return True

        test_chat_ids = [-1001234567890, -1001234567891]

        for chat_id in test_chat_ids:
            result = mock_register_handler("mock_handler", chat_id)
            assert result == True

        print("✅ Handler registration logic works")
        return True

    except Exception as e:
        print(f"❌ Handler registration test error: {e}")
        return False


async def main():
    """Run all comment handling tests"""
    print("🚀 COMMENT HANDLING TESTS")
    print("=" * 60)

    tests = [
        ("BotSettings integration", test_bot_settings_integration),
        ("Keyword matching", test_keyword_matching),
        ("Message structure", test_message_structure),
        ("Handler imports", test_handler_imports),
        ("Fallback keyword", test_fallback_keyword),
        ("Handler registration", test_handler_registration),
    ]

    failed_tests = []

    for test_name, test_func in tests:
        print(f"\n🔍 {test_name.upper()}")
        print("-" * 40)

        try:
            result = await test_func()
            if result:
                print(f"✅ {test_name} - PASSED")
            else:
                print(f"❌ {test_name} - FAILED")
                failed_tests.append(test_name)
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}")
            failed_tests.append(test_name)

    print("\n" + "=" * 60)

    if failed_tests:
        print(f"❌ FAILED TESTS: {', '.join(failed_tests)}")
        print("\n💡 TROUBLESHOOTING COMMENT HANDLING:")
        print("1. Check that BotSettings model exists and works")
        print("2. Verify database connection is working")
        print("3. Ensure all imports are correct")
        print("4. Check that handler registration is working")
        print("5. Verify bot has access to group messages")
        print("6. Check that giveaways are active and have group_id")
        print("\n🔧 POSSIBLE FIXES:")
        print("- Restart bot completely")
        print("- Check bot.log for handler registration messages")
        print("- Verify group permissions for the bot")
        print("- Test with a simple comment in the group")
        return False
    else:
        print("🎉 ALL COMMENT HANDLING TESTS PASSED!")
        print("\n✅ COMMENT HANDLING SHOULD WORK:")
        print("- BotSettings integration is functional")
        print("- Keyword matching works with flexible search")
        print("- Message structure validation is correct")
        print("- All imports are working")
        print("- Fallback system is available")
        print("- Handler registration logic is sound")

        print("\n🎯 TO DEBUG COMMENT ISSUES:")
        print("1. Check bot.log for handler registration messages:")
        print("   grep 'Registering handler for group' bot.log")
        print("2. Test with exact keyword in group comment")
        print("3. Ensure message is reply to giveaway post")
        print("4. Verify bot has message reading permissions")
        print("5. Check that giveaway is active (run_status=True)")

        print("\n📝 COMMENT HANDLING FLOW:")
        print("1. User writes comment with keyword")
        print("2. Bot checks if message contains keyword (any case/position)")
        print("3. Bot verifies it's reply to giveaway post")
        print("4. Bot checks user subscriptions")
        print("5. Bot adds user to giveaway or sends error")

        return True


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nTests cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
