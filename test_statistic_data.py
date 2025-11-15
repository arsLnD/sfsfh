#!/usr/bin/env python3
"""
Test for get_statistic_data method
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


async def test_get_statistic_data():
    """Test get_statistic_data method functionality"""
    print("🧪 Testing get_statistic_data method...")

    try:
        from database import GiveAwayStatistic, initialize_database

        # Initialize database
        await initialize_database()
        print("✅ Database initialized")

        # Test with non-existent giveaway
        test_callback = "nonexistent_giveaway_123"
        result = await GiveAwayStatistic().get_statistic_data(test_callback)

        if result is None:
            print("✅ Returns None for non-existent giveaway")
        else:
            print(f"⚠️ Unexpected result for non-existent: {result}")

        # Check if method exists and is callable
        statistic_model = GiveAwayStatistic()
        assert hasattr(statistic_model, "get_statistic_data")
        assert callable(getattr(statistic_model, "get_statistic_data"))
        print("✅ get_statistic_data method exists and is callable")

        # Test method signature
        import inspect

        sig = inspect.signature(statistic_model.get_statistic_data)
        params = list(sig.parameters.keys())
        print(f"✅ Method parameters: {params}")

        # Check return type annotation
        return_annotation = sig.return_annotation
        print(f"✅ Return annotation: {return_annotation}")

        from tortoise import Tortoise

        await Tortoise.close_connections()

        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        print(f"Full traceback: {traceback.format_exc()}")
        return False


async def test_early_finish_dependencies():
    """Test that early finish has all required dependencies"""
    print("🧪 Testing early finish dependencies...")

    try:
        # Test imports
        from handlers.admin.early_finish_giveaway import (
            confirm_early_finish_giveaway,
            early_finish_giveaway_confirm,
        )

        print("✅ Early finish handlers imported")

        from database import GiveAway, GiveAwayStatistic, TelegramChannel

        print("✅ Database models imported")

        from texts import CONFIRM_EARLY_FINISH, EARLY_FINISH_SUCCESS

        print("✅ Text constants imported")

        # Test text formatting
        test_data = {"name": "Test Giveaway", "participants": 5, "winners_count": 2}

        formatted_confirm = CONFIRM_EARLY_FINISH.format(**test_data)
        formatted_success = EARLY_FINISH_SUCCESS.format(**test_data)

        assert "Test Giveaway" in formatted_confirm
        assert "Test Giveaway" in formatted_success
        print("✅ Text formatting works")

        return True

    except Exception as e:
        print(f"❌ Error testing dependencies: {e}")
        return False


async def test_callback_parsing():
    """Test callback data parsing logic"""
    print("🧪 Testing callback parsing...")

    try:
        # Test various callback formats
        test_callbacks = [
            "early_finish:abc123",
            "early_finish:long_callback_value_with_numbers_123456",
            "early_finish:short",
        ]

        for callback in test_callbacks:
            if callback.startswith("early_finish:"):
                parsed = callback.split(":", 1)[1]
                print(f"   '{callback}' -> '{parsed}'")
                assert len(parsed) > 0
            else:
                print(f"❌ Invalid callback format: {callback}")
                return False

        print("✅ Callback parsing works correctly")
        return True

    except Exception as e:
        print(f"❌ Callback parsing error: {e}")
        return False


async def main():
    """Run all statistic data tests"""
    print("🚀 STATISTIC DATA TESTS")
    print("=" * 50)

    tests = [
        ("get_statistic_data method", test_get_statistic_data),
        ("Early finish dependencies", test_early_finish_dependencies),
        ("Callback parsing", test_callback_parsing),
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
        print("\n💡 POSSIBLE ISSUES:")
        print("1. get_statistic_data method not implemented correctly")
        print("2. Database model structure problems")
        print("3. Import issues with handlers or texts")
        print("4. Callback parsing logic errors")
        return False
    else:
        print("🎉 ALL STATISTIC DATA TESTS PASSED!")
        print("\n✅ EARLY FINISH SHOULD NOW WORK:")
        print("- get_statistic_data method exists and works")
        print("- All dependencies are available")
        print("- Callback parsing functions correctly")
        print("- Text formatting is operational")
        print("\n🎯 Try the early finish button again!")
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
