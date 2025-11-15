#!/usr/bin/env python3
"""
Simple script to get real user ID for testing subscription issues
"""

import asyncio
import logging
import sys

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_user_id():
    """Interactive bot to get real user ID"""

    try:
        from bot import bot
        from database import initialize_database

        print("🤖 ПОЛУЧЕНИЕ ID ПОЛЬЗОВАТЕЛЯ")
        print("=" * 40)

        # Initialize database
        await initialize_database()

        # Test bot connection
        me = await bot.get_me()
        print(f"✅ Бот запущен: @{me.username}")
        print(f"📋 ID бота: {me.id}")

        print("\n📝 ИНСТРУКЦИЯ:")
        print("1. Запустите этот скрипт")
        print("2. Отправьте любое сообщение боту в личные сообщения")
        print("3. Скрипт покажет ваш ID пользователя")
        print("4. Используйте этот ID для тестирования подписки")
        print("5. Нажмите Ctrl+C для остановки")
        print("\n🚀 Бот готов к получению сообщений...\n")

        # Simple message handler
        from aiogram import Dispatcher, types
        from aiogram.contrib.fsm_storage.memory import MemoryStorage

        # Create new dispatcher for this test
        storage = MemoryStorage()
        dp = Dispatcher(bot, storage=storage)

        @dp.message_handler()
        async def get_user_info(message: types.Message):
            """Handler to get user info"""
            user = message.from_user
            chat = message.chat

            print(f"📨 Получено сообщение:")
            print(f"   👤 Пользователь: {user.first_name} {user.last_name or ''}")
            print(f"   🆔 ID пользователя: {user.id}")
            print(f"   📝 Username: @{user.username or 'не указан'}")
            print(f"   💬 Текст: {message.text}")
            print(f"   📱 Тип чата: {chat.type}")
            print("-" * 40)

            # Send response to user
            response = f"""
🔍 <b>Ваша информация:</b>

👤 <b>Имя:</b> {user.first_name} {user.last_name or ""}
🆔 <b>ID:</b> <code>{user.id}</code>
📝 <b>Username:</b> @{user.username or "не указан"}

💡 <b>Используйте ID {user.id} для тестирования подписки на каналы</b>

Команды для тестирования:
<code>python test_real_user_subscription.py</code>
<code>python quick_subscription_test.py</code>
            """

            await message.answer(response, parse_mode="HTML")

            logger.info(f"User info sent for user {user.id}")

        # Start polling
        from aiogram import executor

        async def on_startup(dp):
            print("✅ Бот запущен и готов получать сообщения!")

        async def on_shutdown(dp):
            print("🛑 Бот остановлен")

        try:
            executor.start_polling(
                dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown
            )
        except KeyboardInterrupt:
            print("\n✅ Скрипт остановлен пользователем")

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback

        traceback.print_exc()

    finally:
        if "bot" in locals():
            await bot.close()


def main():
    """Main function"""
    print("📱 ПОЛУЧЕНИЕ ID ПОЛЬЗОВАТЕЛЯ ДЛЯ ТЕСТИРОВАНИЯ")
    print("Этот скрипт поможет получить реальный ID пользователя")
    print("для тестирования проблем с подпиской на каналы\n")

    try:
        asyncio.run(get_user_id())
    except KeyboardInterrupt:
        print("\n⏹ Скрипт прерван пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")


if __name__ == "__main__":
    main()
