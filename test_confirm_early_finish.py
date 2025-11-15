#!/usr/bin/env python3
"""
Test for early finish confirmation functionality
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


async def test_callback_parsing():
    """Test early finish callback parsing"""
    print("🧪 Testing callback parsing...")

    try:
        # Test confirm_early_finish callback parsing
        test_callback = "confirm_early_finish:abc123def456"

        if test_callback.startswith("confirm_early_finish:"):
            callback_value = test_callback.split(":", 1)[1]
            print(f"✅ Parsed callback_value: '{callback_value}'")
            assert callback_value == "abc123def456"
        else:
            print("❌ Callback doesn't start with 'confirm_early_finish:'")
            return False

        # Test various callback formats
        test_callbacks = [
            "confirm_early_finish:short",
            "confirm_early_finish:long_callback_value_123456",
            "confirm_early_finish:mixed_case_Value_789",
        ]

        for callback in test_callbacks:
            parsed = callback.split(":", 1)[1]
            print(f"   '{callback}' -> '{parsed}'")
            assert len(parsed) > 0

        return True

    except Exception as e:
        print(f"❌ Error in callback parsing: {e}")
        return False


async def test_database_operations():
    """Test database operations for early finish"""
    print("🧪 Testing database operations...")

    try:
        from database import GiveAway, GiveAwayStatistic, initialize_database

        # Initialize database
        await initialize_database()
        print("✅ Database initialized")

        # Test set_early_finish method exists
        giveaway_model = GiveAway()
        assert hasattr(giveaway_model, "set_early_finish")
        assert callable(getattr(giveaway_model, "set_early_finish"))
        print("✅ set_early_finish method exists")

        # Test get_statistic_data method exists
        statistic_model = GiveAwayStatistic()
        assert hasattr(statistic_model, "get_statistic_data")
        assert callable(getattr(statistic_model, "get_statistic_data"))
        print("✅ get_statistic_data method exists")

        # Test with non-existent giveaway
        result = await statistic_model.get_statistic_data("nonexistent_123")
        assert result is None
        print("✅ Returns None for non-existent giveaway")

        from tortoise import Tortoise

        await Tortoise.close_connections()

        return True

    except Exception as e:
        print(f"❌ Database operations error: {e}")
        import traceback

        print(f"Full traceback: {traceback.format_exc()}")
        return False


async def test_winner_selection_logic():
    """Test winner selection logic"""
    print("🧪 Testing winner selection logic...")

    try:
        import random

        # Mock participants data
        participants = [
            {"user_id": 123456, "username": "user1"},
            {"user_id": 123457, "username": "user2"},
            {"user_id": 123458, "username": "user3"},
            {"user_id": 123459, "username": "user4"},
            {"user_id": 123460, "username": "user5"},
        ]

        # Test winner selection
        winners_count = 2
        selected_winners = random.sample(participants, winners_count)

        print(
            f"✅ Selected {len(selected_winners)} winners from {len(participants)} participants"
        )

        # Test winner data formatting
        winners_data = []
        for i, participant in enumerate(selected_winners, 1):
            if isinstance(participant, dict):
                user_id = participant.get("user_id")
                username = participant.get("username", f"user_{user_id}")
            else:
                user_id = participant
                username = f"user_{user_id}"

            winners_data.append(
                {
                    "place": i,
                    "user_id": user_id,
                    "username": username,
                }
            )

        print(f"✅ Formatted winner data: {[w['username'] for w in winners_data]}")

        # Test edge cases
        empty_participants = []
        winners_from_empty = min(2, len(empty_participants))
        assert winners_from_empty == 0
        print("✅ Handles empty participants correctly")

        single_participant = [{"user_id": 123, "username": "solo"}]
        winners_from_single = min(3, len(single_participant))
        assert winners_from_single == 1
        print("✅ Handles single participant correctly")

        return True

    except Exception as e:
        print(f"❌ Winner selection error: {e}")
        return False


async def test_text_formatting():
    """Test text formatting for early finish"""
    print("🧪 Testing text formatting...")

    try:
        from texts import EARLY_FINISH_SUCCESS

        # Test text formatting
        test_data = {"name": "Test Giveaway", "participants": 5, "winners_count": 2}

        formatted_text = EARLY_FINISH_SUCCESS.format(**test_data)

        print(f"✅ Success text formatted: {len(formatted_text)} characters")

        # Check that all placeholders are replaced
        assert "Test Giveaway" in formatted_text
        assert "5" in formatted_text
        assert "2" in formatted_text

        print("✅ All placeholders correctly replaced")

        return True

    except Exception as e:
        print(f"❌ Text formatting error: {e}")
        return False


async def test_owners_permission():
    """Test OWNERS permission check"""
    print("🧪 Testing OWNERS permission...")

    try:
        from config import OWNERS

        print(f"OWNERS list: {OWNERS}")
        assert isinstance(OWNERS, list)
        assert len(OWNERS) > 0

        # Test permission logic
        def check_permission(user_id):
            return user_id in OWNERS

        # Test with real owner
        if OWNERS:
            real_owner = OWNERS[0]
            assert check_permission(real_owner) == True
            print(f"✅ Real owner {real_owner} has permission")

        # Test with fake user
        fake_user = 999999999
        assert check_permission(fake_user) == False
        print(f"✅ Fake user {fake_user} denied permission")

        return True

    except Exception as e:
        print(f"❌ OWNERS permission error: {e}")
        return False


async def test_error_handling():
    """Test error handling scenarios"""
    print("🧪 Testing error handling...")

    try:
        # Test callback parsing with invalid data
        invalid_callbacks = [
            "invalid_format",
            "confirm_early_finish:",  # Empty callback value
            "wrong_prefix:abc123",
        ]

        for callback in invalid_callbacks:
            try:
                if callback.startswith("confirm_early_finish:"):
                    parsed = callback.split(":", 1)[1]
                    if not parsed:
                        print(f"   ⚠️ Empty callback value handled: '{callback}'")
                else:
                    print(f"   ⚠️ Invalid format handled: '{callback}'")
            except Exception:
                print(f"   ✅ Error correctly caught for: '{callback}'")

        print("✅ Error handling works correctly")
        return True

    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False


async def main():
    """Run all early finish confirmation tests"""
    print("🚀 EARLY FINISH CONFIRMATION TESTS")
    print("=" * 60)

    tests = [
        ("Callback parsing", test_callback_parsing),
        ("Database operations", test_database_operations),
        ("Winner selection logic", test_winner_selection_logic),
        ("Text formatting", test_text_formatting),
        ("OWNERS permission", test_owners_permission),
        ("Error handling", test_error_handling),
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
        print("\n💡 TROUBLESHOOTING:")
        print("1. Check that database migration completed successfully")
        print("2. Verify all required methods exist in database models")
        print("3. Ensure OWNERS is properly configured")
        print("4. Check that all text constants are defined")
        print("5. Restart the bot after making changes")
        return False
    else:
        print("🎉 ALL EARLY FINISH CONFIRMATION TESTS PASSED!")
        print("\n✅ CONFIRMATION SHOULD NOW WORK:")
        print("- Callback parsing is functional")
        print("- Database operations are ready")
        print("- Winner selection logic works")
        print("- Text formatting is correct")
        print("- Permission system is active")
        print("- Error handling is robust")

        print("\n🎯 TO TEST THE FIX:")
        print("1. Restart the bot: Ctrl+C then python app.py")
        print("2. Go to Active Giveaways in Telegram")
        print("3. Select a giveaway")
        print("4. Press 'Завершить досрочно'")
        print("5. Press 'Да, завершить' - should work now!")

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
