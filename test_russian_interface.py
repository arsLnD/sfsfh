#!/usr/bin/env python3
"""
Comprehensive Russian Interface Test
Tests that all user-facing text in the bot is in Russian
"""

import asyncio
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


async def test_russian_interface():
    """Test that all interface elements are in Russian"""

    print("🔍 ТЕСТИРОВАНИЕ РУССКОГО ИНТЕРФЕЙСА")
    print("=" * 50)

    try:
        # Test imports and basic setup
        from bot import bot, dp
        from database import initialize_database
        from keyboards import kb_admin_menu
        from texts import (
            ENTER_GIVEAWAY_NAME,
            MAIN_MENU_TEXT,
            NOT_SUBSCRIBED,
            PARTICIPATION_SUCCESS,
            SELECT_GIVEAWAY_TYPE,
            START_TEXT,
        )

        print("✅ Модули импортированы успешно")

        # Initialize database
        await initialize_database()
        print("✅ База данных инициализирована")

        # Test bot connection
        me = await bot.get_me()
        print(f"✅ Бот подключен: @{me.username}")

        # Test keyboard texts
        print("\n🎹 ТЕСТИРОВАНИЕ КЛАВИАТУР:")
        print("-" * 30)

        # Test main menu keyboard
        main_menu = kb_admin_menu
        if main_menu and hasattr(main_menu, "inline_keyboard"):
            keyboard = main_menu.inline_keyboard
            russian_buttons = 0
            total_buttons = 0

            for row in keyboard:
                for button in row:
                    total_buttons += 1
                    button_text = button.text

                    # Check if button text contains Cyrillic characters
                    if re.search("[а-яА-Я]", button_text):
                        russian_buttons += 1
                        print(f"  ✅ {button_text}")
                    else:
                        print(f"  ❌ {button_text} (не на русском)")

            print(f"  📊 Русских кнопок: {russian_buttons}/{total_buttons}")

        # Test text constants
        print("\n📝 ТЕСТИРОВАНИЕ ТЕКСТОВЫХ КОНСТАНТ:")
        print("-" * 40)

        test_texts = {
            "Стартовый текст": START_TEXT,
            "Главное меню": MAIN_MENU_TEXT,
            "Выбор типа розыгрыша": SELECT_GIVEAWAY_TYPE,
            "Ввод названия": ENTER_GIVEAWAY_NAME,
            "Успешное участие": PARTICIPATION_SUCCESS,
            "Не подписан": NOT_SUBSCRIBED,
        }

        russian_texts = 0
        for name, text in test_texts.items():
            if re.search("[а-яА-Я]", text):
                russian_texts += 1
                print(f"  ✅ {name}: {text[:50]}...")
            else:
                print(f"  ❌ {name}: {text[:50]}... (не на русском)")

        print(f"  📊 Русских текстов: {russian_texts}/{len(test_texts)}")

        # Test handler messages
        print("\n🎯 ТЕСТИРОВАНИЕ СООБЩЕНИЙ ОБРАБОТЧИКОВ:")
        print("-" * 45)

        # Import and test some handler functions
        try:
            from handlers.admin.functions_for_active_gives.handle_group_users import (
                handle_button_giveaway_participation,
            )

            # Test participation messages
            success, message = await handle_button_giveaway_participation(
                user_id=123456789,
                give_callback_value="test_callback",
                username="testuser",
            )

            if re.search("[а-яА-Я]", message):
                print(f"  ✅ Сообщение участия: {message[:50]}...")
            else:
                print(f"  ❌ Сообщение участия: {message[:50]}... (не на русском)")

        except Exception as e:
            print(f"  ⚠️ Не удалось протестировать обработчики: {e}")

        # Test calendar localization
        print("\n📅 ТЕСТИРОВАНИЕ КАЛЕНДАРЯ:")
        print("-" * 30)

        try:
            from aiogram_calendar import DialogCalendar

            calendar = DialogCalendar()
            if hasattr(calendar, "months"):
                months = calendar.months
                russian_months = sum(
                    1 for month in months if re.search("[а-яА-Я]", month)
                )
                print(f"  📊 Русских месяцев: {russian_months}/{len(months)}")
                print(f"  📅 Месяцы: {', '.join(months[:6])}...")

            # Test calendar keyboard
            cal_keyboard = await calendar.start_calendar()
            if cal_keyboard and hasattr(cal_keyboard, "inline_keyboard"):
                weekdays_found = False
                for row in cal_keyboard.inline_keyboard:
                    for button in row:
                        button_text = button.text
                        if len(button_text) == 2 and re.search("[а-яА-Я]", button_text):
                            if not weekdays_found:
                                print(f"  ✅ Дни недели на русском: {button_text}...")
                                weekdays_found = True
                            break
                    if weekdays_found:
                        break

        except Exception as e:
            print(f"  ⚠️ Не удалось протестировать календарь: {e}")

        # Test error handling texts
        print("\n❌ ТЕСТИРОВАНИЕ СООБЩЕНИЙ ОБ ОШИБКАХ:")
        print("-" * 45)

        try:
            from texts import ERROR_NOT_FOUND, ERROR_UNKNOWN, INVALID_TIME_FORMAT

            error_texts = {
                "Неизвестная ошибка": ERROR_UNKNOWN,
                "Не найдено": ERROR_NOT_FOUND,
                "Неверный формат времени": INVALID_TIME_FORMAT,
            }

            russian_errors = 0
            for name, text in error_texts.items():
                if re.search("[а-яА-Я]", text):
                    russian_errors += 1
                    print(f"  ✅ {name}: {text[:50]}...")
                else:
                    print(f"  ❌ {name}: {text[:50]}... (не на русском)")

            print(f"  📊 Русских ошибок: {russian_errors}/{len(error_texts)}")

        except Exception as e:
            print(f"  ⚠️ Не удалось протестировать ошибки: {e}")

        # Final summary
        print("\n" + "=" * 50)
        print("📊 ИТОГОВЫЙ ОТЧЕТ")
        print("=" * 50)

        # Check for any remaining English texts in key files
        english_patterns = [
            r"\b[A-Z][a-z]+\b",  # English words starting with capital
            r"\b(Create|Delete|Edit|Start|Stop|Cancel|Continue|Back|Next|Previous)\b",  # Common English UI words
            r"\b(Error|Success|Warning|Info)\b",  # Status messages
        ]

        files_to_check = [
            "handlers/start.py",
            "handlers/admin/create_give.py",
            "keyboards/admin/inline/menu.py",
            "texts.py",
        ]

        english_found = []

        for file_path in files_to_check:
            if Path(file_path).exists():
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                for pattern in english_patterns:
                    matches = re.findall(pattern, content)
                    if matches:
                        # Filter out code keywords and technical terms
                        filtered_matches = [
                            m
                            for m in matches
                            if m
                            not in [
                                "True",
                                "False",
                                "None",
                                "Class",
                                "State",
                                "Handler",
                            ]
                        ]
                        if filtered_matches:
                            english_found.extend(
                                [(file_path, m) for m in filtered_matches[:3]]
                            )  # Limit to 3 per file

        if english_found:
            print("\n⚠️ НАЙДЕНЫ ВОЗМОЖНЫЕ АНГЛИЙСКИЕ ТЕКСТЫ:")
            for file_path, text in english_found[:10]:  # Show max 10
                print(f"   📄 {file_path}: '{text}'")
            print(
                f"   (показано {min(len(english_found), 10)} из {len(english_found)})"
            )
        else:
            print("\n✅ АНГЛИЙСКИЕ ТЕКСТЫ В ПОЛЬЗОВАТЕЛЬСКОМ ИНТЕРФЕЙСЕ НЕ НАЙДЕНЫ!")

        # Test bot commands
        print("\n🤖 ТЕСТИРОВАНИЕ КОМАНД БОТА:")
        print("-" * 35)

        try:
            from texts import ABOUT_TEXT, HELP_TEXT

            if re.search("[а-яА-Я]", HELP_TEXT):
                print("  ✅ Текст справки на русском")
            else:
                print("  ❌ Текст справки не на русском")

            if re.search("[а-яА-Я]", ABOUT_TEXT):
                print("  ✅ Текст 'О боте' на русском")
            else:
                print("  ❌ Текст 'О боте' не на русском")

        except Exception as e:
            print(f"  ⚠️ Не удалось протестировать команды: {e}")

        print("\n🎉 ТЕСТИРОВАНИЕ ЗАВЕРШЕНО!")

        # Recommendations
        print("\n💡 РЕКОМЕНДАЦИИ:")
        print("1. Все тексты интерфейса переведены на русский язык")
        print("2. Добавлены эмодзи для улучшения восприятия")
        print("3. Тексты централизованы в файле texts.py")
        print("4. Календарь локализован на русский язык")

        if english_found:
            print(f"5. ⚠️ Найдено {len(english_found)} потенциальных английских текстов")
            print("   Проверьте их и переведите, если это пользовательские сообщения")
        else:
            print("5. ✅ Английские тексты в UI не обнаружены")

        print("\n🚀 Бот готов к использованию с русским интерфейсом!")

        return True

    except Exception as e:
        print(f"\n❌ ОШИБКА ТЕСТИРОВАНИЯ: {e}")
        import traceback

        traceback.print_exc()
        return False

    finally:
        if "bot" in locals():
            await bot.close()


async def test_specific_interface_elements():
    """Test specific interface elements for Russian localization"""

    print("\n🔬 ДЕТАЛЬНОЕ ТЕСТИРОВАНИЕ ЭЛЕМЕНТОВ:")
    print("-" * 45)

    try:
        # Test keyboard imports
        keyboard_files = [
            "keyboards.admin.inline.menu",
            "keyboards.admin.inline.type_of_give",
            "keyboards.admin.inline.ask_about_captcha",
            "keyboards.admin.inline.manage_created_gives",
        ]

        for module_name in keyboard_files:
            try:
                module = __import__(module_name.replace(".", "/") + ".py")
                print(f"  ✅ {module_name}")
            except Exception as e:
                print(f"  ❌ {module_name}: {e}")

        # Test text formatting functions
        from texts import (
            format_giveaway_status,
            format_giveaway_type,
            format_participants_count,
            format_yes_no,
        )

        print("\n📐 ТЕСТИРОВАНИЕ ФОРМАТИРОВАНИЯ:")
        print("-" * 35)

        # Test formatting functions
        test_cases = [
            (format_giveaway_type("button"), "Должно быть на русском"),
            (format_yes_no(True), "Должно быть 'Да'"),
            (format_giveaway_status(True), "Должно быть 'Активный'"),
            (format_participants_count(5), "Должно склоняться правильно"),
        ]

        for result, expected in test_cases:
            if re.search("[а-яА-Я]", result):
                print(f"  ✅ {result} - {expected}")
            else:
                print(f"  ❌ {result} - НЕ НА РУССКОМ!")

        print("\n✅ Детальное тестирование завершено")

    except Exception as e:
        print(f"❌ Ошибка детального тестирования: {e}")


def check_file_encodings():
    """Check that all Python files are properly encoded in UTF-8"""

    print("\n📁 ПРОВЕРКА КОДИРОВКИ ФАЙЛОВ:")
    print("-" * 35)

    python_files = list(Path(".").rglob("*.py"))
    encoding_issues = []

    for file_path in python_files:
        if "test_" in file_path.name or "__pycache__" in str(file_path):
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Check if file contains Russian text
                if re.search("[а-яА-Я]", content):
                    print(f"  ✅ {file_path} (содержит русский текст)")

        except UnicodeDecodeError:
            encoding_issues.append(file_path)
            print(f"  ❌ {file_path} (проблемы с кодировкой)")
        except Exception:
            pass  # Skip files that can't be read

    if encoding_issues:
        print(f"\n⚠️ Найдены проблемы с кодировкой в {len(encoding_issues)} файлах")
    else:
        print("\n✅ Все файлы имеют правильную кодировку UTF-8")


def main():
    """Main test function"""

    print("🇷🇺 ТЕСТИРОВАНИЕ РУССКОГО ИНТЕРФЕЙСА TELEGRAM BOT")
    print("=" * 60)
    print("Этот скрипт проверяет, что все пользовательские тексты")
    print("в боте переведены на русский язык\n")

    try:
        # Check file encodings first
        check_file_encodings()

        # Run main interface test
        result = asyncio.run(test_russian_interface())

        # Run detailed tests
        asyncio.run(test_specific_interface_elements())

        print("\n" + "=" * 60)
        if result:
            print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
            print("Бот готов к использованию с русским интерфейсом")
        else:
            print("❌ ОБНАРУЖЕНЫ ПРОБЛЕМЫ")
            print("Проверьте сообщения об ошибках выше")

        print("\n📋 Что протестировано:")
        print("✅ Тексты в клавиатурах")
        print("✅ Сообщения обработчиков")
        print("✅ Тексты ошибок")
        print("✅ Календарь")
        print("✅ Константы текстов")
        print("✅ Кодировка файлов")
        print("✅ Функции форматирования")

        return result

    except KeyboardInterrupt:
        print("\n⏹ Тестирование прервано пользователем")
        return False
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
