#!/usr/bin/env python3
"""
Quick Subscription Test - Test channel subscription for specific user and channel
"""

import asyncio
import sys

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


async def quick_test():
    """Quick test for specific user and channel"""

    try:
        from bot import bot
        from database import initialize_database
        from handlers.admin.functions_for_active_gives.check_channels_subscriptions import (
            check_single_channel_subscription,
            get_user_channel_status,
        )

        print("🚀 QUICK SUBSCRIPTION TEST")
        print("=" * 30)

        # Initialize database
        await initialize_database()

        # Test bot connection
        me = await bot.get_me()
        print(f"Bot: @{me.username}")

        # Get input from user
        print("\nEnter test parameters:")

        user_id = input("User ID to test: ").strip()
        if not user_id:
            print("❌ User ID required")
            return

        try:
            user_id = int(user_id)
        except ValueError:
            print("❌ Invalid user ID")
            return

        channel_id = input("Channel ID (e.g., @channel or -100xxxxxxxxx): ").strip()
        if not channel_id:
            print("❌ Channel ID required")
            return

        # Convert channel_id to int if it's numeric
        if channel_id.startswith("-") or (channel_id.isdigit()):
            try:
                channel_id = int(channel_id)
            except ValueError:
                pass

        print(f"\n🧪 Testing subscription:")
        print(f"User: {user_id}")
        print(f"Channel: {channel_id}")
        print("-" * 20)

        # Test 1: Get channel info
        try:
            chat = await bot.get_chat(channel_id)
            print(f"✅ Channel found: {chat.title}")
            print(f"   Type: {chat.type}")
            if hasattr(chat, "members_count"):
                print(f"   Members: {chat.members_count}")
        except Exception as e:
            print(f"❌ Cannot access channel: {e}")
            return

        # Test 2: Check bot permissions
        try:
            bot_member = await bot.get_chat_member(channel_id, me.id)
            print(f"✅ Bot status in channel: {bot_member.status}")

            if bot_member.status not in ["administrator", "creator", "member"]:
                print("⚠️  Bot may not have sufficient permissions")
        except Exception as e:
            print(f"❌ Cannot check bot status: {e}")
            return

        # Test 3: Check user subscription
        try:
            status = await get_user_channel_status(channel_id, user_id)
            is_subscribed = await check_single_channel_subscription(channel_id, user_id)

            print(f"\n📊 RESULTS:")
            print(f"User status: {status}")
            print(f"Is subscribed: {'✅ YES' if is_subscribed else '❌ NO'}")

            if status in ["member", "administrator", "creator"]:
                print("✅ User should be able to participate")
            elif status in ["left", "kicked", "restricted"]:
                print("❌ User cannot participate - not subscribed")
            elif status == "error":
                print("⚠️  Could not determine status - check bot permissions")

        except Exception as e:
            print(f"❌ Error checking user subscription: {e}")

        # Test 4: Additional diagnostics
        print(f"\n🔍 DIAGNOSTICS:")

        # Check if channel ID format is correct
        if isinstance(channel_id, str):
            if channel_id.startswith("@"):
                print("✅ Using username format (@channel)")
            elif channel_id.startswith("-100"):
                print("✅ Using supergroup ID format (-100xxxxxxxxx)")
            elif channel_id.startswith("-"):
                print("✅ Using group ID format (-xxxxxxxxx)")
            else:
                print("⚠️  Unusual channel ID format")
        else:
            if channel_id < 0:
                print("✅ Using numeric channel ID (negative)")
            else:
                print("⚠️  Positive channel ID (unusual for groups/channels)")

        print("\n💡 TIPS:")
        print("• If user status is 'error', check bot admin permissions")
        print("• If user status is 'left', user needs to rejoin channel")
        print("• Public channels: use @channelname")
        print("• Private channels/groups: use negative numeric ID")

        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False

    finally:
        if "bot" in locals():
            await bot.close()


def main():
    print("This script tests subscription for a specific user and channel")
    print("Make sure your bot is admin in the channel you want to test")
    print()

    try:
        result = asyncio.run(quick_test())
        if result:
            print("\n✅ Test completed successfully")
        else:
            print("\n❌ Test failed")
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
