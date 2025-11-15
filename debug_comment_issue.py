#!/usr/bin/env python3
"""
Debug script for comment participation issues
This script helps identify why users might get "not subscribed" messages
"""

import asyncio
import logging
import sys
from datetime import datetime

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("comment_debug.log", encoding="utf-8"),
    ],
)

logger = logging.getLogger(__name__)


async def debug_comment_participation():
    """Debug comment-based participation issues"""

    print("🐛 ОТЛАДКА ПРОБЛЕМ С УЧАСТИЕМ ЧЕРЕЗ КОММЕНТАРИИ")
    print("=" * 60)

    try:
        from bot import bot
        from config import text_for_participation_in_comments_giveaways
        from database import GiveAway, TelegramChannel, initialize_database
        from handlers.admin.functions_for_active_gives.check_channels_subscriptions import (
            check_channels_subscriptions,
            check_single_channel_subscription,
        )

        # Initialize database
        await initialize_database()

        # Get bot info
        me = await bot.get_me()
        print(f"✅ Бот: @{me.username} (ID: {me.id})")

        # Get all channels
        channels = (
            await TelegramChannel()
            .all()
            .values(
                "channel_id",
                "name",
                "owner_id",
                "give_callback_value",
                "group_id",
                "post_id",
            )
        )

        if not channels:
            print("❌ Каналы в базе данных не найдены!")
            return

        print(f"\n📺 КАНАЛЫ В БАЗЕ ДАННЫХ: {len(channels)}")
        print("-" * 40)

        for i, channel in enumerate(channels, 1):
            print(f"{i}. Канал: {channel['name']}")
            print(f"   📺 ID канала: {channel['channel_id']}")
            print(f"   👥 ID группы: {channel['group_id']}")
            print(f"   📝 ID поста: {channel['post_id']}")
            print(f"   👤 Владелец: {channel['owner_id']}")
            print(f"   🎲 ID розыгрыша: {channel['give_callback_value']}")

            # Test channel access
            try:
                chat = await bot.get_chat(channel["channel_id"])
                print(f"   ✅ Канал доступен: {chat.title}")

                # Check bot status in channel
                bot_member = await bot.get_chat_member(channel["channel_id"], me.id)
                print(f"   🤖 Статус бота: {bot_member.status}")

                if bot_member.status in ["administrator", "creator"]:
                    print(f"   ✅ Бот имеет права администратора")
                else:
                    print(f"   ⚠️ Бот не администратор - могут быть проблемы")

            except Exception as e:
                print(f"   ❌ Ошибка доступа к каналу: {e}")

            print()

        # Get active giveaways
        giveaways = (
            await GiveAway()
            .filter(run_status=True)
            .all()
            .values("callback_value", "name", "type", "owner_id", "over_date")
        )

        print(f"🎯 АКТИВНЫЕ РОЗЫГРЫШИ: {len(giveaways)}")
        print("-" * 30)

        if not giveaways:
            print("   Нет активных розыгрышей")
        else:
            for giveaway in giveaways:
                print(f"   🎲 {giveaway['name']}")
                print(f"   📝 Тип: {giveaway['type']}")
                print(f"   🔗 ID: {giveaway['callback_value']}")
                print(f"   👤 Владелец: {giveaway['owner_id']}")
                print(f"   📅 Окончание: {giveaway['over_date']}")
                print()

        # Test subscription check for different user scenarios
        print("🧪 ТЕСТИРОВАНИЕ ПРОВЕРКИ ПОДПИСКИ")
        print("-" * 40)

        print(
            f"💬 Ключевое слово для участия: '{text_for_participation_in_comments_giveaways}'"
        )
        print()

        # Test cases
        test_users = [
            {"id": me.id, "name": "Бот (должен быть подписан)"},
            {"id": 123456789, "name": "Тестовый пользователь 1"},
            {"id": 987654321, "name": "Тестовый пользователь 2"},
        ]

        for user in test_users:
            user_id = user["id"]
            user_name = user["name"]

            print(f"👤 Тестируем: {user_name} (ID: {user_id})")

            for channel in channels:
                channel_id = channel["channel_id"]
                channel_name = channel["name"]

                try:
                    # Test individual channel subscription
                    is_subscribed = await check_single_channel_subscription(
                        channel_id, user_id
                    )
                    status_emoji = "✅" if is_subscribed else "❌"

                    print(f"   📺 {channel_name}: {status_emoji}")

                    # Get detailed status if possible
                    try:
                        member_info = await bot.get_chat_member(channel_id, user_id)
                        print(f"      📊 Статус: {member_info.status}")
                    except Exception as status_error:
                        error_msg = str(status_error).lower()
                        if "member not found" in error_msg:
                            print(f"      📊 Статус: не найден в канале")
                        elif "participant_id_invalid" in error_msg:
                            print(f"      📊 Статус: недействительный ID пользователя")
                        else:
                            print(f"      📊 Статус: ошибка - {status_error}")

                except Exception as e:
                    print(f"   📺 {channel_name}: ❌ Ошибка - {e}")

            # Test full giveaway subscription check
            if giveaways:
                for giveaway in giveaways:
                    try:
                        can_participate = await check_channels_subscriptions(
                            give_callback_value=giveaway["callback_value"],
                            user_id=user_id,
                        )

                        result_emoji = "✅" if can_participate else "❌"
                        print(f"   🎲 Розыгрыш '{giveaway['name']}': {result_emoji}")

                    except Exception as e:
                        print(f"   🎲 Розыгрыш '{giveaway['name']}': ❌ Ошибка - {e}")

            print()

        # Simulate comment processing
        print("🎭 СИМУЛЯЦИЯ ОБРАБОТКИ КОММЕНТАРИЯ")
        print("-" * 40)

        if channels and giveaways:
            # Use first channel for simulation
            test_channel = channels[0]
            test_giveaway = giveaways[0]

            print(
                f"📺 Тестовый канал: {test_channel['name']} (ID: {test_channel['channel_id']})"
            )
            print(f"👥 ID группы: {test_channel['group_id']}")
            print(f"📝 ID поста: {test_channel['post_id']}")
            print(f"🎲 Розыгрыш: {test_giveaway['name']}")

            # Simulate message data
            print(f"\n💬 Симуляция сообщения:")
            print(f"   Текст: '{text_for_participation_in_comments_giveaways}'")
            print(f"   ID группы: {test_channel['group_id']}")
            print(f"   Ответ на пост: {test_channel['post_id']}")

            # Check if group data exists
            group_channels = [
                ch for ch in channels if ch["group_id"] == test_channel["group_id"]
            ]
            print(f"   📊 Каналов для этой группы: {len(group_channels)}")

            for ch in group_channels:
                print(f"      - {ch['name']} (post_id: {ch['post_id']})")

        # Check common issues
        print("🔍 ПРОВЕРКА ЧАСТЫХ ПРОБЛЕМ")
        print("-" * 30)

        issues_found = []

        # Check 1: Bot permissions
        for channel in channels:
            try:
                bot_member = await bot.get_chat_member(channel["channel_id"], me.id)
                if bot_member.status not in ["administrator", "creator"]:
                    issues_found.append(
                        f"Бот не администратор в канале {channel['name']}"
                    )
            except:
                issues_found.append(f"Нет доступа к каналу {channel['name']}")

        # Check 2: Group IDs exist
        for channel in channels:
            if channel["type"] == "comments" and not channel["group_id"]:
                issues_found.append(
                    f"Отсутствует ID группы для канала {channel['name']}"
                )

        # Check 3: Post IDs exist
        for channel in channels:
            if not channel["post_id"]:
                issues_found.append(
                    f"Отсутствует ID поста для канала {channel['name']}"
                )

        if issues_found:
            print("❌ Найдены проблемы:")
            for issue in issues_found:
                print(f"   • {issue}")
        else:
            print("✅ Критических проблем не найдено")

        # Recommendations
        print(f"\n💡 РЕКОМЕНДАЦИИ ДЛЯ РЕШЕНИЯ ПРОБЛЕМ:")
        print("-" * 45)
        print("1. Убедитесь, что бот добавлен как администратор во всех каналах")
        print("2. Дайте боту право 'Просмотр участников' в настройках канала")
        print("3. Проверьте, что ID группы корректно указан в базе данных")
        print("4. Убедитесь, что ID поста совпадает с реальным ID поста в канале")
        print("5. Протестируйте с реальным ID пользователя, который подписан на канал")
        print("6. Проверьте логи в файле comment_debug.log для детальной информации")

        print(f"\n📋 ИНСТРУКЦИИ ДЛЯ ДАЛЬНЕЙШЕГО ТЕСТИРОВАНИЯ:")
        print("-" * 50)
        print("1. Получите реальный ID пользователя:")
        print("   - Запустите бота: python app.py")
        print("   - Пользователь должен написать /start боту")
        print("   - ID появится в логах")

        print("\n2. Протестируйте подписку с реальным ID:")
        print(f"   python quick_subscription_test.py")

        print("\n3. Убедитесь, что пользователь:")
        print("   - Подписан на все указанные каналы")
        print("   - Пишет комментарий с точным текстом")
        print("   - Отвечает на правильный пост")

        return True

    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        logger.error(f"Critical error in debug: {e}")
        import traceback

        traceback.print_exc()
        return False

    finally:
        if "bot" in locals():
            await bot.close()


async def test_message_processing():
    """Test how messages would be processed"""

    print(f"\n🔄 ТЕСТИРОВАНИЕ ОБРАБОТКИ СООБЩЕНИЙ")
    print("-" * 40)

    try:
        from unittest.mock import AsyncMock, MagicMock

        from aiogram import types
        from config import text_for_participation_in_comments_giveaways
        from handlers.admin.functions_for_active_gives.handle_group_users import (
            handle_new_users_in_groups,
        )

        # Mock user
        user = types.User(
            id=123456789, is_bot=False, first_name="Тест", username="testuser"
        )

        # Mock chat (group)
        chat = types.Chat(
            id=-1003180113623,  # Use real group ID from database
            type="supergroup",
            title="Test Group",
        )

        # Mock replied message
        reply_msg = MagicMock()
        reply_msg.forward_from_message_id = 12345  # This should match post_id

        # Mock participation message
        message = MagicMock()
        message.text = text_for_participation_in_comments_giveaways
        message.from_user = user
        message.chat = chat
        message.reply_to_message = reply_msg
        message.reply = AsyncMock()

        print(f"🎭 Тестовое сообщение:")
        print(f"   👤 Пользователь: {user.first_name} (@{user.username})")
        print(f"   💬 Текст: '{message.text}'")
        print(f"   📱 Группа: {chat.title} (ID: {chat.id})")
        print(f"   🔄 Ответ на пост: {reply_msg.forward_from_message_id}")

        # Process message
        print(f"\n⚙️ Обработка сообщения...")
        await handle_new_users_in_groups(message)

        # Check if bot replied
        if message.reply.called:
            args = message.reply.call_args
            reply_text = args[0][0] if args and args[0] else "Нет текста"
            print(f"✅ Бот ответил: {reply_text}")
        else:
            print(f"❌ Бот не ответил на сообщение")

    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        import traceback

        traceback.print_exc()


def main():
    """Main debug function"""

    print("🐛 ОТЛАДЧИК ПРОБЛЕМ С УЧАСТИЕМ В РОЗЫГРЫШАХ ЧЕРЕЗ КОММЕНТАРИИ")
    print("Этот скрипт поможет выявить причины проблем с проверкой подписки")
    print()

    try:
        # Run main debug
        result = asyncio.run(debug_comment_participation())

        # Test message processing
        asyncio.run(test_message_processing())

        print(f"\n" + "=" * 60)
        print("🏁 ОТЛАДКА ЗАВЕРШЕНА")
        print("=" * 60)

        if result:
            print("✅ Базовая проверка прошла успешно")
        else:
            print("❌ Обнаружены серьезные проблемы")

        print(f"\n📄 Детальные логи сохранены в файл: comment_debug.log")
        print(f"🔧 Используйте информацию выше для устранения проблем")

        return result

    except KeyboardInterrupt:
        print(f"\n⏹ Отладка прервана пользователем")
        return False
    except Exception as e:
        print(f"\n❌ Критическая ошибка отладки: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
