#!/usr/bin/env python3
"""
Channel Subscription Test Script
Test if channel subscription checking works correctly
"""

import asyncio
import logging
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_channel_subscription():
    """Test channel subscription checking functionality"""

    try:
        # Load environment variables
        from dotenv import load_dotenv

        load_dotenv()

        # Import required modules
        from bot import bot
        from database import GiveAway, TelegramChannel, initialize_database
        from handlers.admin.functions_for_active_gives.check_channels_subscriptions import (
            check_channels_subscriptions,
            check_single_channel_subscription,
            get_user_channel_status,
        )

        print("🔍 CHANNEL SUBSCRIPTION TEST")
        print("=" * 50)

        # Initialize database
        await initialize_database()
        print("✅ Database initialized")

        # Test bot connection
        me = await bot.get_me()
        print(f"✅ Bot connected: @{me.username}")

        # Get test data
        print("\n📋 Getting test data from database...")

        # Get all channels
        channels = (
            await TelegramChannel()
            .all()
            .values("channel_id", "name", "owner_id", "give_callback_value")
        )

        if not channels:
            print("❌ No channels found in database!")
            print("💡 Add some channels through the bot admin panel first")
            return False

        print(f"Found {len(channels)} channels:")
        for i, channel in enumerate(channels, 1):
            print(f"  {i}. {channel['name']} (ID: {channel['channel_id']})")

        # Get test user ID
        print("\n👤 Enter test user information:")
        try:
            test_user_id = input(
                "Enter user ID to test (or press Enter for demo): "
            ).strip()
            if not test_user_id:
                test_user_id = "123456789"  # Demo user ID
            test_user_id = int(test_user_id)
        except ValueError:
            print("❌ Invalid user ID")
            return False

        print(f"Testing with user ID: {test_user_id}")

        # Test each channel individually
        print(f"\n🧪 Testing individual channel subscriptions...")

        for channel in channels:
            channel_id = channel["channel_id"]
            channel_name = channel["name"]

            print(f"\n📡 Testing channel: {channel_name} ({channel_id})")

            # Test single channel subscription
            status = await get_user_channel_status(channel_id, test_user_id)
            is_subscribed = await check_single_channel_subscription(
                channel_id, test_user_id
            )

            print(f"   Status: {status}")
            print(f"   Subscribed: {'✅' if is_subscribed else '❌'}")

            if status == "error":
                print("   ⚠️  Possible issues:")
                print("   - Channel doesn't exist")
                print("   - Bot is not admin in channel")
                print("   - Bot doesn't have permission to check members")
                print("   - Channel ID is incorrect")

        # Test giveaway subscription check
        giveaways = await GiveAway().all().values("callback_value", "name", "owner_id")

        if giveaways:
            print(f"\n🎁 Testing giveaway subscription checks...")

            for giveaway in giveaways:
                print(f"\nTesting giveaway: {giveaway['name']}")

                is_eligible = await check_channels_subscriptions(
                    give_callback_value=giveaway["callback_value"], user_id=test_user_id
                )

                print(f"   User eligible: {'✅' if is_eligible else '❌'}")
        else:
            print("\n❌ No giveaways found in database")

        # Manual channel test
        print(f"\n🔧 Manual channel test:")
        manual_channel = input(
            "Enter channel ID or @username to test (or press Enter to skip): "
        ).strip()

        if manual_channel:
            try:
                if not manual_channel.startswith("@") and not manual_channel.startswith(
                    "-"
                ):
                    manual_channel = int(manual_channel)

                print(f"Testing manual channel: {manual_channel}")

                status = await get_user_channel_status(manual_channel, test_user_id)
                is_subscribed = await check_single_channel_subscription(
                    manual_channel, test_user_id
                )

                print(f"   Status: {status}")
                print(f"   Subscribed: {'✅' if is_subscribed else '❌'}")

            except ValueError:
                print("❌ Invalid channel format")

        print(f"\n✅ Channel subscription test completed!")
        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False

    finally:
        if "bot" in locals():
            await bot.close()


def print_troubleshooting_tips():
    """Print troubleshooting tips"""
    print("\n🔧 TROUBLESHOOTING TIPS:")
    print("=" * 30)
    print("1. Common subscription check issues:")
    print("   - Bot is not admin in the channel")
    print("   - Channel ID is incorrect (should be negative for supergroups)")
    print("   - Channel doesn't exist or was deleted")
    print("   - Bot doesn't have 'View Members' permission")
    print()
    print("2. Valid subscription statuses:")
    print("   - 'member' - regular channel member")
    print("   - 'administrator' - channel admin")
    print("   - 'creator' - channel owner")
    print()
    print("3. Invalid statuses (not subscribed):")
    print("   - 'left' - user left the channel")
    print("   - 'kicked' - user was banned")
    print("   - 'restricted' - user is restricted")
    print()
    print("4. Bot setup requirements:")
    print("   - Add bot as admin to channels")
    print("   - Give bot 'View Members' permission")
    print("   - Use correct channel IDs in database")
    print()
    print("5. Channel ID formats:")
    print("   - Public channels: @channelname or -100xxxxxxxxx")
    print("   - Private channels: -100xxxxxxxxx (always negative)")
    print("   - Groups: -xxxxxxxxx (negative)")


async def debug_channel_permissions():
    """Debug channel permissions for the bot"""

    try:
        from bot import bot
        from database import TelegramChannel, initialize_database

        await initialize_database()

        print("\n🛠️  DEBUGGING CHANNEL PERMISSIONS")
        print("=" * 40)

        # Get bot info
        me = await bot.get_me()
        print(f"Bot: @{me.username} (ID: {me.id})")

        # Get all channels from database
        channels = await TelegramChannel().all().values("channel_id", "name")

        for channel in channels:
            channel_id = channel["channel_id"]
            channel_name = channel["name"]

            print(f"\n📡 Channel: {channel_name} ({channel_id})")

            try:
                # Try to get chat info
                chat_info = await bot.get_chat(channel_id)
                print(f"   ✅ Chat accessible: {chat_info.title}")
                print(f"   Type: {chat_info.type}")
                print(
                    f"   Members count: {getattr(chat_info, 'members_count', 'Unknown')}"
                )

                # Try to get bot's status in the chat
                bot_member = await bot.get_chat_member(channel_id, me.id)
                print(f"   Bot status: {bot_member.status}")

                if hasattr(bot_member, "can_read_all_group_messages"):
                    print(
                        f"   Can read messages: {bot_member.can_read_all_group_messages}"
                    )

            except Exception as e:
                print(f"   ❌ Error accessing channel: {e}")

                error_msg = str(e).lower()
                if "chat not found" in error_msg:
                    print("   💡 Channel not found or bot has no access")
                elif "forbidden" in error_msg:
                    print("   💡 Bot is not a member or lacks permissions")
                else:
                    print(f"   💡 Unknown error: {e}")

    except Exception as e:
        print(f"❌ Debug failed: {e}")


def main():
    """Main function"""

    print("🧪 TELEGRAM CHANNEL SUBSCRIPTION TESTER")
    print("This script helps debug channel subscription checking")
    print()

    # Check prerequisites
    if not Path(".env").exists():
        print("❌ .env file not found")
        print("Solution: Copy .env.example to .env and add your BOT_TOKEN")
        return False

    print("Choose test mode:")
    print("1. Test user subscription to channels")
    print("2. Debug bot permissions in channels")
    print("3. Show troubleshooting tips")

    try:
        choice = input("\nEnter choice (1-3): ").strip()

        if choice == "1":
            asyncio.run(test_channel_subscription())
        elif choice == "2":
            asyncio.run(debug_channel_permissions())
        elif choice == "3":
            print_troubleshooting_tips()
        else:
            print("❌ Invalid choice")
            return False

        print_troubleshooting_tips()
        return True

    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        return True
    except Exception as e:
        print(f"\nTest failed: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
