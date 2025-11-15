#!/usr/bin/env python3
"""
Script to translate remaining English texts to Russian in the bot
"""

import os
import re
from pathlib import Path


def translate_file(file_path: Path, translations: dict):
    """Apply translations to a file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # Apply translations
        for english, russian in translations.items():
            content = content.replace(english, russian)

        # Only write if content changed
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Updated: {file_path}")
            return True
        else:
            print(f"⏭️ No changes: {file_path}")
            return False

    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False


def main():
    print("🌍 TRANSLATING REMAINING ENGLISH TEXTS TO RUSSIAN")
    print("=" * 50)

    # Common English to Russian translations
    translations = {
        # Navigation buttons
        '"Back"': '"« Назад"',
        "'Back'": "'« Назад'",
        '"Cancel"': '"❌ Отмена"',
        "'Cancel'": "'❌ Отмена'",
        '"Continue"': '"Продолжить »"',
        "'Continue'": "'Продолжить »'",
        '"Edit"': '"✏️ Изменить"',
        "'Edit'": "'✏️ Изменить'",
        '"Delete"': '"🗑 Удалить"',
        "'Delete'": "'🗑 Удалить'",
        '"Confirm"': '"✅ Подтвердить"',
        "'Confirm'": "'✅ Подтвердить'",
        # Actions
        '"Start"': '"🚀 Запустить"',
        "'Start'": "'🚀 Запустить'",
        '"Stop"': '"⏹ Остановить"',
        "'Stop'": "'⏹ Остановить'",
        '"View"': '"👁 Просмотр"',
        "'View'": "'👁 Просмотр'",
        '"Add"': '"➕ Добавить"',
        "'Add'": "'➕ Добавить'",
        '"Remove"': '"🗑 Удалить"',
        "'Remove'": "'🗑 Удалить'",
        # Status messages
        '"Loading..."': '"⏳ Загрузка..."',
        "'Loading...'": "'⏳ Загрузка...'",
        '"Processing..."': '"⏳ Обработка..."',
        "'Processing...'": "'⏳ Обработка...'",
        '"Success!"': '"✅ Успешно!"',
        "'Success!'": "'✅ Успешно!'",
        '"Error!"': '"❌ Ошибка!"',
        "'Error!'": "'❌ Ошибка!'",
        # Common phrases
        '"Please wait"': '"Пожалуйста, подождите"',
        "'Please wait'": "'Пожалуйста, подождите'",
        '"Try again"': '"Попробуйте еще раз"',
        "'Try again'": "'Попробуйте еще раз'",
        '"Not found"': '"Не найдено"',
        "'Not found'": "'Не найдено'",
        '"Access denied"': '"Доступ запрещен"',
        "'Access denied'": "'Доступ запрещен'",
        # Menu items that might still be in English
        '"Main Menu"': '"Главное меню"',
        "'Main Menu'": "'Главное меню'",
        '"Settings"': '"Настройки"',
        "'Settings'": "'Настройки'",
        '"Help"': '"Справка"',
        "'Help'": "'Справка'",
        '"About"': '"О боте"',
        "'About'": "'О боте'",
        # Giveaway related
        '"Create Giveaway"': '"🎲 Создать розыгрыш"',
        "'Create Giveaway'": "'🎲 Создать розыгрыш'",
        '"Created Giveaways"': '"📝 Созданные розыгрыши"',
        "'Created Giveaways'": "'📝 Созданные розыгрыши'",
        '"Active Giveaways"': '"🎯 Активные розыгрыши"',
        "'Active Giveaways'": "'🎯 Активные розыгрыши'",
        '"Participants"': '"👥 Участники"',
        "'Participants'": "'👥 Участники'",
        '"Results"': '"🏆 Результаты"',
        "'Results'": "'🏆 Результаты'",
        '"Winners"': '"🏆 Победители"',
        "'Winners'": "'🏆 Победители'",
        # Channel related
        '"Channels"': '"📺 Каналы"',
        "'Channels'": "'📺 Каналы'",
        '"Add Channel"': '"➕ Добавить канал"',
        "'Add Channel'": "'➕ Добавить канал'",
        '"Manage Channels"': '"📺 Управление каналами"',
        "'Manage Channels'": "'📺 Управление каналами'",
        '"Subscribe"': '"Подписаться"',
        "'Subscribe'": "'Подписаться'",
        '"Subscribed"': '"Подписан"',
        "'Subscribed'": "'Подписан'",
        # Time and date
        '"Select date"': '"Выберите дату"',
        "'Select date'": "'Выберите дату'",
        '"Select time"': '"Выберите время"',
        "'Select time'": "'Выберите время'",
        '"Date"': '"Дата"',
        "'Date'": "'Дата'",
        '"Time"': '"Время"',
        "'Time'": "'Время'",
        # Media
        '"Photo"': '"🖼 Фото"',
        "'Photo'": "'🖼 Фото'",
        '"Video"': '"🎬 Видео"',
        "'Video'": "'🎬 Видео'",
        '"Media"': '"📎 Медиа"',
        "'Media'": "'📎 Медиа'",
        # Yes/No
        '"Yes"': '"✅ Да"',
        "'Yes'": "'✅ Да'",
        '"No"': '"❌ Нет"',
        "'No'": "'❌ Нет'",
        # Pagination
        '"Page"': '"Страница"',
        "'Page'": "'Страница'",
        '"Previous"': '"⬅️ Предыдущая"',
        "'Previous'": "'⬅️ Предыдущая'",
        '"Next"': '"➡️ Следующая"',
        "'Next'": "'➡️ Следующая'",
        # Error messages that might be in English
        '"Invalid format"': '"❌ Неверный формат"',
        "'Invalid format'": "'❌ Неверный формат'",
        '"Something went wrong"': '"❌ Что-то пошло не так"',
        "'Something went wrong'": "'❌ Что-то пошло не так'",
        '"Unknown error"': '"❌ Неизвестная ошибка"',
        "'Unknown error'": "'❌ Неизвестная ошибка'",
        # Admin panel
        '"Admin Panel"': '"🛠 Панель администратора"',
        "'Admin Panel'": "'🛠 Панель администратора'",
        '"Management"': '"Управление"',
        "'Management'": "'Управление'",
        '"Statistics"': '"📊 Статистика"',
        "'Statistics'": "'📊 Статистика'",
        # Calendar and time-related English text in aiogram_calendar
        '"Mo"': '"Пн"',
        "'Mo'": "'Пн'",
        '"Tu"': '"Вт"',
        "'Tu'": "'Вт'",
        '"We"': '"Ср"',
        "'We'": "'Ср'",
        '"Th"': '"Чт"',
        "'Th'": "'Чт'",
        '"Fr"': '"Пт"',
        "'Fr'": "'Пт'",
        '"Sa"': '"Сб"',
        "'Sa'": "'Сб'",
        '"Su"': '"Вс"',
        "'Su'": "'Вс'",
        # Month names (if any English ones exist)
        '"January"': '"Январь"',
        '"February"': '"Февраль"',
        '"March"': '"Март"',
        '"April"': '"Апрель"',
        '"May"': '"Май"',
        '"June"': '"Июнь"',
        '"July"': '"Июль"',
        '"August"': '"Август"',
        '"September"': '"Сентябрь"',
        '"October"': '"Октябрь"',
        '"November"': '"Ноябрь"',
        '"December"': '"Декабрь"',
        # Additional common phrases that might appear
        '"Enter"': '"Введите"',
        "'Enter'": "'Введите'",
        '"Send"': '"Отправить"',
        "'Send'": "'Отправить'",
        '"Save"': '"💾 Сохранить"',
        "'Save'": "'💾 Сохранить'",
        '"Load"': '"Загрузить"',
        "'Load'": "'Загрузить'",
        '"Reset"': '"🔄 Сбросить"',
        "'Reset'": "'🔄 Сбросить'",
        '"Refresh"': '"🔄 Обновить"',
        "'Refresh'": "'🔄 Обновить'",
        # Additional giveaway terms
        '"Giveaway"': '"Розыгрыш"',
        "'Giveaway'": "'Розыгрыш'",
        '"Contest"': '"Конкурс"',
        "'Contest'": "'Конкурс'",
        '"Prize"': '"Приз"',
        "'Prize'": "'Приз'",
        '"Winner"': '"Победитель"',
        "'Winner'": "'Победитель'",
        '"Participant"': '"Участник"',
        "'Participant'": "'Участник'",
        # Status and state related
        '"Active"': '"🎯 Активный"',
        "'Active'": "'🎯 Активный'",
        '"Inactive"': '"⏸ Неактивный"',
        "'Inactive'": "'⏸ Неактивный'",
        '"Draft"': '"📝 Черновик"',
        "'Draft'": "'📝 Черновик'",
        '"Finished"': '"✅ Завершен"',
        "'Finished'": "'✅ Завершен'",
        '"Running"': '"🏃 Выполняется"',
        "'Running'": "'🏃 Выполняется'",
        # File and keyboard-specific phrases
        '"admin_gives"': '"admin_gives"',  # Keep callback data unchanged
        '"admin_created_gives"': '"admin_created_gives"',
        '"admin_started_gives"': '"admin_started_gives"',
        # Log and debug messages (keep these in English for consistency with logs)
        # '"Debug"': '"Отладка"',
        # '"Info"': '"Информация"',
        # '"Warning"': '"Предупреждение"',
        # '"Error"': '"Ошибка"',
    }

    # Files to process (excluding test files and configuration)
    files_to_process = []

    # Add all Python files in handlers
    handlers_dir = Path("handlers")
    if handlers_dir.exists():
        for py_file in handlers_dir.rglob("*.py"):
            files_to_process.append(py_file)

    # Add all Python files in keyboards
    keyboards_dir = Path("keyboards")
    if keyboards_dir.exists():
        for py_file in keyboards_dir.rglob("*.py"):
            files_to_process.append(py_file)

    # Add other directories that might have text
    other_dirs = ["utils", "states", "database/models"]
    for dir_name in other_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            for py_file in dir_path.rglob("*.py"):
                files_to_process.append(py_file)

    # Process aiogram_calendar files separately (they might have English weekdays)
    calendar_dir = Path("aiogram_calendar")
    if calendar_dir.exists():
        calendar_translations = {
            '["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]': '["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]',
            "['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']": "['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']",
            '"Mo"': '"Пн"',
            '"Tu"': '"Вт"',
            '"We"': '"Ср"',
            '"Th"': '"Чт"',
            '"Fr"': '"Пт"',
            '"Sa"': '"Сб"',
            '"Su"': '"Вс"',
        }

        for py_file in calendar_dir.rglob("*.py"):
            if not py_file.name.startswith("test_"):
                translate_file(py_file, calendar_translations)

    # Process files
    updated_count = 0
    total_count = len(files_to_process)

    print(f"\n📁 Processing {total_count} files...")

    for file_path in files_to_process:
        # Skip test files and __pycache__
        if "test_" in file_path.name or "__pycache__" in str(file_path):
            continue

        if translate_file(file_path, translations):
            updated_count += 1

    print(f"\n📊 SUMMARY:")
    print(f"✅ Updated: {updated_count} files")
    print(f"📁 Total processed: {total_count} files")
    print(f"⏭️ No changes needed: {total_count - updated_count} files")

    if updated_count > 0:
        print(f"\n🎉 Successfully translated English texts to Russian!")
        print(f"🔧 Recommendation: Test the bot to ensure all texts display correctly")
    else:
        print(f"\n✅ All texts are already in Russian or no changes needed")

    print("\n💡 Note: Callback data and technical strings were kept unchanged")
    print("for compatibility reasons.")


if __name__ == "__main__":
    main()
