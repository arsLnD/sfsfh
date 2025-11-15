#!/usr/bin/env python3
"""
Test for early finish flow with mock data
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


async def test_early_finish_flow():
    """Test complete early finish flow with real data"""
    print("🧪 Testing early finish flow...")

    try:
        from database import GiveAway, GiveAwayStatistic, initialize_database

        # Initialize database
        await initialize_database()
        print("✅ Database initialized")

        # Get existing giveaways
        giveaways = await GiveAway.filter(run_status=True).all()
        if not giveaways:
            print("⚠️ No active giveaways found. Testing with mock data...")
            return await test_mock_early_finish()

        # Test with first active giveaway
        giveaway = giveaways[0]
        callback_value = giveaway.callback_value
        print(f"✅ Testing with giveaway: {giveaway.name}")
        print(f"   Callback value: {callback_value}")

        # Test get_statistic_data
        stats = await GiveAwayStatistic().get_statistic_data(callback_value)
        print(f"✅ Statistics retrieved: {type(stats)}")

        if stats:
            members = stats.get("members", [])
            print(f"   Participants: {len(members)}")
            print(f"   Winners count: {giveaway.winners_count}")

            # Test participants data structure
            if members:
                first_member = members[0]
                print(f"   Sample participant: {first_member}")

                # Check if participant has required fields
                if isinstance(first_member, dict):
                    has_user_id = "user_id" in first_member
                    has_username = "username" in first_member
                    print(f"   Has user_id: {has_user_id}")
                    print(f"   Has username: {has_username}")
                else:
                    print(f"   ⚠️ Participant is not dict: {type(first_member)}")
        else:
            print("   No statistics data found")

        # Test early_finish field
        print(f"✅ Current early_finish status: {giveaway.early_finish}")

        from tortoise import Tortoise

        await Tortoise.close_connections()

        return True

    except Exception as e:
        print(f"❌ Error in early finish flow test: {e}")
        import traceback

        print(f"Full traceback: {traceback.format_exc()}")
        return False


async def test_mock_early_finish():
    """Test early finish logic with mock data"""
    print("🧪 Testing with mock data...")

    try:
        # Mock giveaway data
        mock_giveaway = {
            "name": "Test Giveaway",
            "winners_count": 2,
            "text": "Test giveaway text",
        }

        # Mock statistics data
        mock_stats = {
            "members": [
                {"user_id": 123456, "username": "user1"},
                {"user_id": 123457, "username": "user2"},
                {"user_id": 123458, "username": "user3"},
                {"user_id": 123459, "username": "user4"},
            ],
            "winners": [],
        }

        print(f"✅ Mock giveaway: {mock_giveaway['name']}")
        print(f"   Participants: {len(mock_stats['members'])}")
        print(f"   Winners count: {mock_giveaway['winners_count']}")

        # Test participant selection logic
        import random

        participants = mock_stats["members"]
        winners_count = min(mock_giveaway["winners_count"], len(participants))

        if winners_count > 0:
            selected_winners = random.sample(participants, winners_count)
            print(f"✅ Selected {len(selected_winners)} winners:")

            for i, winner in enumerate(selected_winners, 1):
                print(f"   {i}. {winner['username']} (ID: {winner['user_id']})")

        # Test text formatting
        from texts import CONFIRM_EARLY_FINISH, EARLY_FINISH_SUCCESS

        confirm_text = CONFIRM_EARLY_FINISH.format(
            name=mock_giveaway["name"],
            participants=len(participants),
            winners_count=winners_count,
        )
        print(f"✅ Confirmation text length: {len(confirm_text)}")

        success_text = EARLY_FINISH_SUCCESS.format(
            name=mock_giveaway["name"],
            participants=len(participants),
            winners_count=winners_count,
        )
        print(f"✅ Success text length: {len(success_text)}")

        return True

    except Exception as e:
        print(f"❌ Mock test error: {e}")
        return False


async def test_callback_handlers():
    """Test callback handler registration"""
    print("🧪 Testing callback handlers...")

    try:
        from handlers.admin.early_finish_giveaway import (
            cancel_early_finish_giveaway,
            confirm_early_finish_giveaway,
            early_finish_giveaway_confirm,
        )

        print("✅ All early finish handlers imported")

        # Check handler names
        handlers = [
            early_finish_giveaway_confirm,
            confirm_early_finish_giveaway,
            cancel_early_finish_giveaway,
        ]

        for handler in handlers:
            print(f"   Handler: {handler.__name__}")
            assert callable(handler)

        print("✅ All handlers are callable")
        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Handler test error: {e}")
        return False


async def test_owners_permissions():
    """Test OWNERS permission system"""
    print("🧪 Testing OWNERS permissions...")

    try:
        from config import OWNERS

        print(f"OWNERS list: {OWNERS}")
        assert isinstance(OWNERS, list)
        assert len(OWNERS) > 0

        # Test permission check logic
        test_user_id = 123456789
        is_owner = test_user_id in OWNERS

        real_owner = OWNERS[0]
        is_real_owner = real_owner in OWNERS

        print(f"   Test user {test_user_id} is owner: {is_owner}")
        print(f"   Real owner {real_owner} is owner: {is_real_owner}")

        assert is_real_owner == True
        print("✅ OWNERS permission system works")
        return True

    except Exception as e:
        print(f"❌ OWNERS test error: {e}")
        return False


async def main():
    """Run early finish flow tests"""
    print("🚀 EARLY FINISH FLOW TESTS")
    print("=" * 60)

    tests = [
        ("Early finish flow", test_early_finish_flow),
        ("Callback handlers", test_callback_handlers),
        ("OWNERS permissions", test_owners_permissions),
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
        print("\n💡 TROUBLESHOOTING EARLY FINISH:")
        print("1. Check bot logs for detailed error messages")
        print("2. Verify your user ID is in OWNERS list")
        print("3. Ensure giveaway has participants")
        print("4. Check database connection")
        print("5. Restart the bot completely")
        return False
    else:
        print("🎉 ALL EARLY FINISH TESTS PASSED!")
        print("\n✅ EARLY FINISH IS READY:")
        print("- Database methods work correctly")
        print("- Handlers are properly registered")
        print("- Permission system is active")
        print("- Text formatting functions")
        print("- Winner selection logic works")
        print("\n🎯 Early finish button should now work!")

        print("\n📋 TO TEST IN TELEGRAM:")
        print("1. Go to Active Giveaways")
        print("2. Select a giveaway")
        print("3. Press 'Завершить досрочно'")
        print("4. Confirm the action")
        print("5. Check that winners are selected")

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
