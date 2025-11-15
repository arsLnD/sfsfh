#!/usr/bin/env python3
"""
Real User Subscription Test - Test subscription checking with actual user data
"""

import asyncio
import logging
import sys

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("subscription_test.log", encoding="utf-8"),
    ],
)

logger = logging.getLogger(__name__)


async def test_real_user_subscription():
    """Test subscription checking with real user data"""

    try:
        from bot import bot
        from database import TelegramChannel, initialize_database
        from handlers.admin.functions_for_active_gives.check_channels_subscriptions import (
            check_channels_subscriptions,
            check_single_channel_subscription,
            get_user_channel_status,
        )

        print("🔍 ТЕСТ ПРОВЕРКИ ПОДПИСКИ РЕАЛЬНОГО ПОЛЬЗОВАТЕЛЯ")
        print("=" * 60)

        # Initialize database
        await initialize_database()
        logger.info("Database initialized")

        # Test bot connection
        me = await bot.get_me()
        print(f"✅ Бот: @{me.username} (ID: {me.id})")
        logger.info(f"Bot connected: @{me.username}")

        # Get channels from database
        channels = (
            await TelegramChannel()
            .all()
            .values("channel_id", "name", "owner_id", "give_callback_value")
        )

        if not channels:
            print("❌ Нет каналов в базе данных!")
            return False

        print(f"\n📺 Найдено каналов: {len(channels)}")
        for channel in channels:
            print(f"   - {channel['name']} (ID: {channel['channel_id']})")

        # Get user ID to test
        print(f"\n👤 ВВОД ДАННЫХ ПОЛЬЗОВАТЕЛЯ:")
        print("-" * 35)

        # In real scenario, we'd get this from user input
        # For now, let's use a test approach
        print("Введите ID пользователя для тестирования:")
        print("(или оставьте пустым для автоматического теста)")

        try:
            user_input = input("User ID: ").strip()
            if user_input:
                test_user_id = int(user_input)
                print(f"Тестируем пользователя ID: {test_user_id}")
            else:
                # Use bot's own ID for testing
                test_user_id = me.id
                print(f"Используем ID бота для теста: {test_user_id}")
        except (ValueError, EOFError):
            test_user_id = me.id
            print(f"Используем ID бота для теста: {test_user_id}")

        logger.info(f"Testing user ID: {test_user_id}")

        # Test each channel individually
        print(f"\n🔍 ДЕТАЛЬНАЯ ПРОВЕРКА КАНАЛОВ:")
        print("-" * 40)

        all_subscribed = True

        for i, channel in enumerate(channels, 1):
            channel_id = channel["channel_id"]
            channel_name = channel["name"]

            print(f"\n{i}. Канал: {channel_name}")
            print(f"   ID: {channel_id}")

            logger.info(f"Testing channel {channel_id} for user {test_user_id}")

            # Test 1: Get user status
            try:
                status = await get_user_channel_status(channel_id, test_user_id)
                print(f"   📊 Статус: {status}")
                logger.info(f"User {test_user_id} status in {channel_id}: {status}")

                if status in ["member", "administrator", "creator"]:
                    print(f"   ✅ Подписан ({status})")
                elif status in ["left", "kicked", "restricted"]:
                    print(f"   ❌ Не подписан ({status})")
                    all_subscribed = False
                elif status in ["not_found", "not_member"]:
                    print(f"   ❌ Не найден в канале ({status})")
                    all_subscribed = False
                else:
                    print(f"   ⚠️ Неопределенный статус ({status})")
                    all_subscribed = False

            except Exception as e:
                print(f"   ❌ Ошибка получения статуса: {e}")
                logger.error(f"Error getting status: {e}")
                all_subscribed = False

            # Test 2: Single channel subscription check
            try:
                is_subscribed = await check_single_channel_subscription(
                    channel_id, test_user_id
                )
                print(
                    f"   🔍 Проверка подписки: {'✅ Подписан' if is_subscribed else '❌ Не подписан'}"
                )
                logger.info(f"Single subscription check result: {is_subscribed}")

                if not is_subscribed:
                    all_subscribed = False

            except Exception as e:
                print(f"   ❌ Ошибка проверки подписки: {e}")
                logger.error(f"Error checking subscription: {e}")
                all_subscribed = False

        # Test full giveaway subscription check
        print(f"\n🎁 ПРОВЕРКА УЧАСТИЯ В РОЗЫГРЫШАХ:")
        print("-" * 40)

        for channel in channels:
            if channel["give_callback_value"]:
                giveaway_id = channel["give_callback_value"]
                owner_id = channel["owner_id"]

                print(f"\nРозыгрыш: {giveaway_id}")

                try:
                    can_participate = await check_channels_subscriptions(
                        give_callback_value=giveaway_id, user_id=test_user_id
                    )

                    print(
                        f"   {'✅ Может участвовать' if can_participate else '❌ НЕ может участвовать'}"
                    )
                    logger.info(
                        f"Giveaway participation check for {giveaway_id}: {can_participate}"
                    )

                    if not can_participate:
                        all_subscribed = False

                except Exception as e:
                    print(f"   ❌ Ошибка проверки участия: {e}")
                    logger.error(f"Error checking giveaway participation: {e}")
                    all_subscribed = False

        # Summary
        print(f"\n" + "=" * 60)
        print("📋 ИТОГОВЫЙ РЕЗУЛЬТАТ")
        print("=" * 60)

        if all_subscribed:
            print("🎉 ПОЛЬЗОВАТЕЛЬ МОЖЕТ УЧАСТВОВАТЬ ВО ВСЕХ РОЗЫГРЫШАХ!")
            print("✅ Все проверки пройдены успешно")
        else:
            print("❌ ПОЛЬЗОВАТЕЛЬ НЕ МОЖЕТ УЧАСТВОВАТЬ")
            print("💡 Возможные причины:")
            print("   • Пользователь не подписан на один или несколько каналов")
            print("   • Пользователь покинул канал")
            print("   • Пользователь был заблокирован в канале")
            print("   • Неверный ID пользователя")
            print("   • Технические проблемы с API Telegram")

        # Recommendations
        print(f"\n💡 РЕКОМЕНДАЦИИ:")
        print("-" * 20)

        if not all_subscribed:
            print("1. Проверьте, что пользователь действительно подписан на все каналы")
            print("2. Убедитесь, что бот имеет права администратора в каналах")
            print("3. Проверьте, что у бота есть право 'Просмотр участников'")
            print("4. Убедитесь, что ID пользователя корректный")
        else:
            print("1. Все проверки прошли успешно!")
            print("2. Система проверки подписки работает корректно")

        # Debug information
        print(f"\n🔧 ОТЛАДОЧНАЯ ИНФОРМАЦИЯ:")
        print(f"   📝 Лог файл: subscription_test.log")
        print(f"   🤖 ID бота: {me.id}")
        print(f"   👤 ID тестируемого пользователя: {test_user_id}")
        print(f"   📺 Количество каналов: {len(channels)}")

        return all_subscribed

    except Exception as e:
        print(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        logger.error(f"Critical error: {e}")
        import traceback

        logger.error(f"Full traceback: {traceback.format_exc()}")
        traceback.print_exc()
        return False

    finally:
        if "bot" in locals():
            await bot.close()


async def simulate_comment_participation():
    """Simulate comment-based participation to debug the issue"""

    print(f"\n🎭 СИМУЛЯЦИЯ УЧАСТИЯ ЧЕРЕЗ КОММЕНТАРИЙ")
    print("=" * 50)

    try:
        from unittest.mock import AsyncMock, MagicMock

        from aiogram import types
        from handlers.admin.functions_for_active_gives.handle_group_users import (
            handle_new_users_in_groups,
        )

        # Create mock user
        user = types.User(
            id=12345,
            is_bot=False,
            first_name="Test",
            last_name="User",
            username="testuser",
        )

        # Create mock chat (group)
        chat = types.Chat(id=-1003180113623, type="supergroup", title="Test Group")

        # Create mock reply message
        reply_message = types.Message(
            message_id=100,
            from_user=user,
            date=1234567890,
            chat=chat,
            content_type="text",
            options={},
            forward_from_message_id=12345,  # This should match post_id in database
        )

        # Create mock participation message
        message = types.Message(
            message_id=101,
            from_user=user,
            date=1234567890,
            chat=chat,
            content_type="text",
            options={},
            text="Участвую",
            reply_to_message=reply_message,
        )

        # Mock the reply method
        message.reply = AsyncMock()

        print(
            f"👤 Симуляция пользователя: {user.first_name} (@{user.username}, ID: {user.id})"
        )
        print(f"💬 Сообщение: '{message.text}'")
        print(f"📱 Группа: {chat.title} (ID: {chat.id})")
        print(f"🔄 Ответ на сообщение ID: {reply_message.forward_from_message_id}")

        logger.info(f"Simulating comment participation for user {user.id}")

        # Process the message
        await handle_new_users_in_groups(message)

        # Check if reply was called
        if message.reply.called:
            call_args = message.reply.call_args
            reply_text = call_args[0][0] if call_args[0] else "No text"
            print(f"📤 Ответ бота: {reply_text}")
            logger.info(f"Bot replied: {reply_text}")
        else:
            print(f"🔇 Бот не отправил ответ")
            logger.warning("Bot did not reply to participation message")

    except Exception as e:
        print(f"❌ Ошибка симуляции: {e}")
        logger.error(f"Simulation error: {e}")
        import traceback

        traceback.print_exc()


def main():
    """Main test function"""

    print("🧪 ТЕСТИРОВАНИЕ ПРОВЕРКИ ПОДПИСКИ ПОЛЬЗОВАТЕЛЕЙ")
    print("Этот скрипт поможет выявить проблемы с проверкой подписки на каналы")
    print()

    try:
        # Run real user subscription test
        result = asyncio.run(test_real_user_subscription())

        # Run comment participation simulation
        asyncio.run(simulate_comment_participation())

        print(f"\n" + "=" * 60)
        if result:
            print("✅ ТЕСТ ПРОЙДЕН: Система проверки подписки работает корректно")
        else:
            print("❌ ТЕСТ НЕ ПРОЙДЕН: Обнаружены проблемы с проверкой подписки")

        print(f"\n📋 Для решения проблемы:")
        print("1. Проверьте лог файл: subscription_test.log")
        print("2. Убедитесь, что бот администратор во всех каналах")
        print("3. Проверьте права бота: 'Просмотр участников'")
        print("4. Используйте реальный ID пользователя для тестирования")

        return result

    except KeyboardInterrupt:
        print("\n⏹ Тестирование прервано пользователем")
        return False
    except Exception as e:
        print(f"\n❌ Критическая ошибка тестирования: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
