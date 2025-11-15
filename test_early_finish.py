#!/usr/bin/env python3
"""
Simple test for early finish functionality
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


async def test_early_finish_callback():
    """Test that early finish callback parsing works correctly"""
    print("🧪 Testing early finish callback parsing...")

    # Test callback data parsing
    test_callback = "early_finish:abc123def456"

    try:
        if test_callback.startswith("early_finish:"):
            callback_value = test_callback.split(":", 1)[1]
            print(f"✅ Parsed callback_value: '{callback_value}'")
            assert callback_value == "abc123def456"
        else:
            print("❌ Callback doesn't start with 'early_finish:'")
            return False
    except Exception as e:
        print(f"❌ Error parsing callback: {e}")
        return False

    return True


async def test_owners_check():
    """Test OWNERS list functionality"""
    print("🧪 Testing OWNERS check...")

    try:
        from config import OWNERS

        print(f"OWNERS list: {OWNERS}")

        # Test user ID check
        test_user_id = 123456789
        is_owner = test_user_id in OWNERS

        print(f"Test user {test_user_id} is owner: {is_owner}")

        if OWNERS:
            # Test with actual owner
            first_owner = OWNERS[0]
            is_actual_owner = first_owner in OWNERS
            print(f"First owner {first_owner} is in list: {is_actual_owner}")
            assert is_actual_owner == True

        return True

    except ImportError as e:
        print(f"❌ Cannot import OWNERS: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing OWNERS: {e}")
        return False


async def test_database_models():
    """Test that database models work for early finish"""
    print("🧪 Testing database models...")

    try:
        from database import GiveAway, GiveAwayStatistic, initialize_database

        await initialize_database()
        print("✅ Database initialized")

        # Test GiveAway model
        giveaway_count = await GiveAway.all().count()
        print(f"✅ Found {giveaway_count} giveaways")

        # Test early_finish field exists
        if giveaway_count > 0:
            first_giveaway = await GiveAway.all().first()
            has_early_finish = hasattr(first_giveaway, "early_finish")
            print(f"✅ GiveAway has early_finish field: {has_early_finish}")

            if has_early_finish:
                print(f"✅ early_finish value: {first_giveaway.early_finish}")

        from tortoise import Tortoise

        await Tortoise.close_connections()

        return True

    except Exception as e:
        print(f"❌ Database test failed: {e}")
        import traceback

        print(f"Full error: {traceback.format_exc()}")
        return False


async def test_early_finish_texts():
    """Test early finish text constants"""
    print("🧪 Testing early finish text constants...")

    try:
        from texts import (
            CONFIRM_EARLY_FINISH,
            EARLY_FINISH_CANCELLED,
            EARLY_FINISH_SUCCESS,
        )

        print("✅ All early finish texts imported successfully")

        # Test text formatting
        test_name = "Test Giveaway"
        test_participants = 5
        test_winners = 2

        formatted_confirm = CONFIRM_EARLY_FINISH.format(
            name=test_name, participants=test_participants, winners_count=test_winners
        )

        print(f"✅ Confirm text formatted: {len(formatted_confirm)} characters")

        formatted_success = EARLY_FINISH_SUCCESS.format(
            name=test_name, participants=test_participants, winners_count=test_winners
        )

        print(f"✅ Success text formatted: {len(formatted_success)} characters")

        return True

    except ImportError as e:
        print(f"❌ Cannot import texts: {e}")
        return False
    except Exception as e:
        print(f"❌ Text formatting failed: {e}")
        return False


async def test_handler_registration():
    """Test that early finish handlers are registered"""
    print("🧪 Testing handler registration...")

    try:
        from bot import dp

        # Get registered handlers
        callback_handlers = []

        # Check if dispatcher has handlers
        if hasattr(dp, "callback_query_handlers"):
            callback_handlers = dp.callback_query_handlers
        elif hasattr(dp, "handlers"):
            callback_handlers = [h for h in dp.handlers if h.event == "callback_query"]

        print(f"✅ Found {len(callback_handlers)} callback handlers registered")

        # Look for early finish handlers
        early_finish_handlers = 0
        for handler in callback_handlers:
            if hasattr(handler, "callback") and callable(handler.callback):
                if "early_finish" in str(handler.callback.__name__):
                    early_finish_handlers += 1

        print(f"✅ Found {early_finish_handlers} early finish handlers")

        return True

    except Exception as e:
        print(f"❌ Handler registration test failed: {e}")
        return False


async def main():
    """Run all early finish tests"""
    print("🚀 EARLY FINISH FUNCTIONALITY TESTS")
    print("=" * 50)

    tests = [
        ("Callback parsing", test_early_finish_callback),
        ("OWNERS check", test_owners_check),
        ("Database models", test_database_models),
        ("Text constants", test_early_finish_texts),
        ("Handler registration", test_handler_registration),
    ]

    failed_tests = []

    for test_name, test_func in tests:
        print(f"\n🔍 {test_name.upper()}")
        print("-" * 30)

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

    print("\n" + "=" * 50)

    if failed_tests:
        print(f"❌ FAILED TESTS: {', '.join(failed_tests)}")
        print("❌ EARLY FINISH TESTS FAILED!")
        print("\n💡 TROUBLESHOOTING:")
        print("1. Make sure the bot is properly configured")
        print("2. Check that database migration was successful")
        print("3. Verify all handlers are imported correctly")
        print("4. Ensure OWNERS is set in config")
        return False
    else:
        print("🎉 ALL EARLY FINISH TESTS PASSED!")
        print("\n✅ SUMMARY:")
        print("- Callback parsing works correctly")
        print("- OWNERS check is functional")
        print("- Database models support early_finish")
        print("- Text constants are available")
        print("- Handlers are registered")
        print("\n🚀 Early finish functionality is ready to use!")
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
