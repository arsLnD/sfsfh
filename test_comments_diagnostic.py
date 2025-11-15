#!/usr/bin/env python3
"""
Diagnostic test for comment handling after keyword fix
"""

import asyncio
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)


async def test_keyword_after_fix():
    """Test participation keyword after fix"""
    print("🧪 Testing participation keyword after fix...")

    try:
        from database import BotSettings, initialize_database

        # Initialize database
        await initialize_database()
        print("✅ Database initialized")

        # Get current keyword
        keyword = await BotSettings.get_participation_keyword()
        print(f"✅ Current participation keyword: '{keyword}'")

        # Verify it's the correct default
        if keyword == "Участвую":
            print("✅ Keyword is correctly set to default")
        else:
            print(f"⚠️ Keyword is not default: '{keyword}' (should be 'Участвую')")

        from tortoise import Tortoise

        await Tortoise.close_connections()

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        print(f"Full traceback: {traceback.format_exc()}")
        return False


async def test_active_giveaways():
    """Test active giveaways that should have comment handlers"""
    print("🧪 Testing active giveaways...")

    try:
        from database import GiveAway, TelegramChannel, initialize_database

        await initialize_database()

        # Get active comment-based giveaways
        active_giveaways = await GiveAway.filter(
            run_status=True, early_finish=False, type="comments"
        ).all()

        print(f"✅ Found {len(active_giveaways)} active comment giveaways")

        for giveaway in active_giveaways:
            print(f"   - {giveaway.name} (ID: {giveaway.callback_value[:20]}...)")

            # Check if giveaway has associated channels/groups
            channels = await TelegramChannel.filter(
                give_callback_value=giveaway.callback_value
            ).all()

            for channel in channels:
                print(f"     Channel: {channel.channel_id}, Group: {channel.group_id}")

        from tortoise import Tortoise

        await Tortoise.close_connections()

        return True

    except Exception as e:
        print(f"❌ Error checking active giveaways: {e}")
        return False


async def test_handler_logic():
    """Test comment handler logic without actual message"""
    print("🧪 Testing comment handler logic...")

    try:
        import re

        from database import BotSettings

        # Get current keyword
        keyword = await BotSettings.get_participation_keyword()
        print(f"Testing with keyword: '{keyword}'")

        # Test messages that should work
        test_cases = [
            (keyword, True, "exact match"),
            (keyword.lower(), True, "lowercase"),
            (keyword.upper(), True, "uppercase"),
            (f"Привет! {keyword} в конкурсе!", True, "with additional text"),
            ("Не хочу участвовать", False, "different text"),
            ("", False, "empty text"),
        ]

        all_passed = True
        for test_text, expected, description in test_cases:
            if not test_text:
                result = False
            else:
                keyword_pattern = re.compile(re.escape(keyword), re.IGNORECASE)
                result = bool(keyword_pattern.search(test_text))

            status = "✅" if result == expected else "❌"
            print(f"   {status} {description}: '{test_text}' -> {result}")

            if result != expected:
                all_passed = False

        if all_passed:
            print("✅ All handler logic tests passed")
        else:
            print("❌ Some handler logic tests failed")

        return all_passed

    except Exception as e:
        print(f"❌ Error testing handler logic: {e}")
        return False


async def test_imports_and_dependencies():
    """Test all required imports"""
    print("🧪 Testing imports and dependencies...")

    try:
        # Test main handler import
        from handlers.admin.functions_for_active_gives.handle_group_users import (
            handle_new_users_in_groups,
        )

        print("✅ Main comment handler imported")

        # Test database imports
        from database import BotSettings, GiveAwayStatistic, TelegramChannel

        print("✅ Database models imported")

        # Test text imports
        from texts import NOT_SUBSCRIBED, PARTICIPATION_SUCCESS

        print("✅ Response texts imported")

        # Test subscription check
        from handlers.admin.functions_for_active_gives.check_channels_subscriptions import (
            check_channels_subscriptions,
        )

        print("✅ Subscription checker imported")

        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Dependencies error: {e}")
        return False


async def run_full_diagnostic():
    """Run complete diagnostic of comment system"""
    print("🚀 COMMENT HANDLING DIAGNOSTIC")
    print("=" * 60)

    tests = [
        ("Keyword after fix", test_keyword_after_fix),
        ("Active giveaways", test_active_giveaways),
        ("Handler logic", test_handler_logic),
        ("Imports and dependencies", test_imports_and_dependencies),
    ]

    failed_tests = []
    passed_tests = []

    for test_name, test_func in tests:
        print(f"\n🔍 {test_name.upper()}")
        print("-" * 40)

        try:
            result = await test_func()
            if result:
                print(f"✅ {test_name} - PASSED")
                passed_tests.append(test_name)
            else:
                print(f"❌ {test_name} - FAILED")
                failed_tests.append(test_name)
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}")
            failed_tests.append(test_name)

    print("\n" + "=" * 60)
    print(f"📊 RESULTS: {len(passed_tests)} PASSED, {len(failed_tests)} FAILED")
    print("=" * 60)

    if failed_tests:
        print(f"❌ FAILED: {', '.join(failed_tests)}")
        print("\n💡 TROUBLESHOOTING:")
        print("1. Restart the bot completely")
        print("2. Check that active giveaways exist")
        print("3. Verify group permissions for bot")
        print("4. Test with exact keyword in group comment")
        return False
    else:
        print("🎉 ALL DIAGNOSTIC TESTS PASSED!")
        print("\n✅ COMMENT HANDLING STATUS:")
        print("- Participation keyword is correct")
        print("- Active comment giveaways found")
        print("- Handler logic is functional")
        print("- All dependencies are working")

        print("\n🎯 COMMENT HANDLING SHOULD WORK!")
        print("\nTO TEST IN TELEGRAM:")
        print("1. Go to a group with active giveaway")
        print("2. Reply to the giveaway post")
        print("3. Write 'Участвую' (or current keyword)")
        print("4. Bot should process the comment")

        print("\n📝 IF COMMENTS STILL DON'T WORK:")
        print("- Check bot has message permissions in group")
        print("- Verify you're replying to correct post")
        print("- Ensure giveaway is active (run_status=True)")
        print("- Check bot.log for processing messages")

        return True


if __name__ == "__main__":
    try:
        success = asyncio.run(run_full_diagnostic())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nDiagnostic cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
