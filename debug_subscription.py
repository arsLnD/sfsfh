#!/usr/bin/env python3
"""
Simple Channel Subscription Diagnostic Script
Helps debug why channel subscription checking might fail
"""

import asyncio
import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


async def debug_subscription():
    """Debug channel subscription issues"""

    try:
        from bot import bot
        from database import TelegramChannel, initialize_database

        print("🔍 CHANNEL SUBSCRIPTION DEBUG")
        print("=" * 40)

        # Initialize database
        await initialize_database()
        print("✅ Database initialized")

        # Test bot connection
        me = await bot.get_me()
        print(f"✅ Bot: @{me.username} (ID: {me.id})")

        # Get all channels from database
        channels = (
            await TelegramChannel().all().values("channel_id", "name", "owner_id")
        )

        if not channels:
            print("\n❌ No channels found in database!")
            print("Add channels through bot admin panel first")
            return

        print(f"\n📺 Found {len(channels)} channels:")

        # Test each channel
        for i, channel in enumerate(channels, 1):
            channel_id = channel["channel_id"]
            channel_name = channel["name"]

            print(f"\n{i}. Testing: {channel_name}")
            print(f"   Channel ID: {channel_id}")

            try:
                # Get channel info
                chat = await bot.get_chat(channel_id)
                print(f"   ✅ Channel accessible: {chat.title}")
                print(f"   Type: {chat.type}")

                # Check bot's permissions
                bot_member = await bot.get_chat_member(channel_id, me.id)
                print(f"   Bot status: {bot_member.status}")

                if bot_member.status in ["administrator", "creator"]:
                    print("   ✅ Bot has admin rights")
                else:
                    print("   ❌ Bot is not admin - this may cause issues")

                # Test with a sample user ID
                print("\n   Testing with sample user IDs:")
                test_users = [123456789, 987654321, me.id]

                for test_id in test_users:
                    try:
                        member = await bot.get_chat_member(channel_id, test_id)
                        print(f"   User {test_id}: {member.status}")
                    except Exception as e:
                        if "user not found" in str(e).lower():
                            print(f"   User {test_id}: not found")
                        else:
                            print(f"   User {test_id}: error - {e}")

            except Exception as e:
                print(f"   ❌ Error: {e}")

                if "chat not found" in str(e).lower():
                    print("   💡 Channel not found or bot has no access")
                elif "forbidden" in str(e).lower():
                    print("   💡 Bot lacks permissions")
                else:
                    print(f"   💡 Unknown error: {e}")

        print("\n" + "=" * 40)
        print("🛠️  TROUBLESHOOTING GUIDE")
        print("=" * 40)

        print("\n1. Common Issues:")
        print("   • Bot not added as admin to channel")
        print("   • Wrong channel ID in database")
        print("   • Channel was deleted or made private")
        print("   • Bot lacks 'View Members' permission")

        print("\n2. Solutions:")
        print("   • Add bot as admin in Telegram channel settings")
        print("   • Give bot 'View Members' permission")
        print("   • Verify channel IDs are correct")
        print("   • Use @channelname or -100xxxxxxxxx format")

        print("\n3. Valid Subscription Statuses:")
        print("   ✅ 'member' - regular subscriber")
        print("   ✅ 'administrator' - channel admin")
        print("   ✅ 'creator' - channel owner")
        print("   ❌ 'left' - user left channel")
        print("   ❌ 'kicked' - user was banned")
        print("   ❌ 'restricted' - user is restricted")

        # Test manual channel
        print("\n" + "=" * 40)
        print("🧪 MANUAL TEST")
        print("=" * 40)
        print("Enter channel to test manually:")
        print("Format: @channelname or -100xxxxxxxxx")

        manual_channel = input("Channel ID/username: ").strip()
        if manual_channel:
            print(f"\nTesting: {manual_channel}")
            try:
                chat = await bot.get_chat(manual_channel)
                print(f"✅ Found: {chat.title} ({chat.type})")

                # Test bot status
                bot_member = await bot.get_chat_member(manual_channel, me.id)
                print(f"Bot status: {bot_member.status}")

            except Exception as e:
                print(f"❌ Error: {e}")

        return True

    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback

        traceback.print_exc()
        return False

    finally:
        if "bot" in locals():
            await bot.close()


def main():
    print("🚀 Starting channel subscription debug...")

    try:
        asyncio.run(debug_subscription())
    except KeyboardInterrupt:
        print("\n\n⏹️  Debug interrupted")
    except Exception as e:
        print(f"\n❌ Failed: {e}")


if __name__ == "__main__":
    main()
