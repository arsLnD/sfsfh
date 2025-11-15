#!/usr/bin/env python3
"""
Test script to verify the Telegram Giveaway Bot setup
"""

import os
import sys
from pathlib import Path


def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")

    try:
        import aiogram

        print("✓ aiogram imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import aiogram: {e}")
        return False

    try:
        import tortoise

        print("✓ tortoise-orm imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import tortoise-orm: {e}")
        return False

    try:
        import pytz

        print("✓ pytz imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import pytz: {e}")
        return False

    try:
        from dotenv import load_dotenv

        print("✓ python-dotenv imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import python-dotenv: {e}")
        return False

    return True


def test_config():
    """Test configuration loading"""
    print("\nTesting configuration...")

    # Store original token
    original_token = os.environ.get("BOT_TOKEN", "")
    # Set a dummy token for testing
    os.environ["BOT_TOKEN"] = "test_token_123:dummy_token_for_testing_only"

    try:
        # Clear any cached config imports
        import sys

        config_modules = [key for key in sys.modules.keys() if key.startswith("config")]
        for module in config_modules:
            if module in sys.modules:
                del sys.modules[module]

        from config import bot_token, database_url, timezone_info

        print("✓ Configuration imported successfully")
        print(f"  - Bot token length: {len(bot_token)}")
        print(f"  - Database URL: {database_url}")
        print(f"  - Timezone: {timezone_info}")

        # Restore original token
        if original_token:
            os.environ["BOT_TOKEN"] = original_token

        return True
    except Exception as e:
        print(f"✗ Failed to import configuration: {e}")

        # Restore original token
        if original_token:
            os.environ["BOT_TOKEN"] = original_token

        return False


def test_database_models():
    """Test database models import"""
    print("\nTesting database models...")

    # Set test token to avoid bot initialization during database imports
    original_token = os.environ.get("BOT_TOKEN", "")
    os.environ["BOT_TOKEN"] = "test_token_123:dummy_token_for_testing_only"

    try:
        from database.models import (
            GiveAway,
            GiveAwayStatistic,
            TelegramChannel,
            TemporaryUsers,
        )

        print("✓ All database models imported successfully")

        # Restore original token
        if original_token:
            os.environ["BOT_TOKEN"] = original_token

        return True
    except Exception as e:
        print(f"✗ Failed to import database models: {e}")

        # Restore original token
        if original_token:
            os.environ["BOT_TOKEN"] = original_token

        return False


def test_handlers():
    """Test handlers structure"""
    print("\nTesting handlers structure...")

    # Check if handler files exist and have correct structure
    try:
        from pathlib import Path

        handler_files = [
            "handlers/start.py",
            "handlers/admin/create_give.py",
            "handlers/admin/save_giveaway.py",
        ]

        for handler_file in handler_files:
            if Path(handler_file).exists():
                print(f"✓ Handler file exists: {handler_file}")
            else:
                print(f"✗ Missing handler file: {handler_file}")
                return False

        # Test if we can read the handler files without importing them
        with open("handlers/start.py", "r", encoding="utf-8") as f:
            content = f.read()
            if "process_start" in content and "@dp.message_handler" in content:
                print("✓ Start handler has correct structure")
            else:
                print("✗ Start handler missing required components")
                return False

        print("✓ Handler structure test passed")
        return True

    except Exception as e:
        print(f"✗ Failed to test handlers: {e}")
        return False


def test_keyboards():
    """Test keyboards import"""
    print("\nTesting keyboards...")

    try:
        from keyboards import kb_admin_menu

        print("✓ Admin menu keyboard imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import keyboards: {e}")
        return False


def test_states():
    """Test FSM states import"""
    print("\nTesting FSM states...")

    try:
        from states import CreateGiveStates

        print("✓ FSM states imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import FSM states: {e}")
        return False


def test_file_structure():
    """Test if all required files exist"""
    print("\nTesting file structure...")

    required_files = [
        "app.py",
        "requirements.txt",
        "config/__init__.py",
        "config/py_config.py",
        "database/__init__.py",
        "database/settings.py",
        "handlers/__init__.py",
        "handlers/start.py",
        "keyboards/__init__.py",
        "states/__init__.py",
        ".env.example",
        "SETUP.md",
        "README.md",
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
            print(f"✗ Missing file: {file_path}")
        else:
            print(f"✓ Found: {file_path}")

    if missing_files:
        print(f"\n⚠️  Missing {len(missing_files)} required files")
        return False

    print("✓ All required files present")
    return True


def main():
    """Run all tests"""
    print("=" * 50)
    print("Telegram Giveaway Bot Setup Test")
    print("=" * 50)

    tests = [
        test_file_structure,
        test_imports,
        test_config,
        test_database_models,
        test_keyboards,
        test_states,
        test_handlers,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
            failed += 1
        print()

    print("=" * 50)
    print("Test Results:")
    print(f"✓ Passed: {passed}")
    print(f"✗ Failed: {failed}")

    if failed == 0:
        print("\n🎉 All tests passed! Your bot setup looks good.")
        print("\n🎉 All tests passed! Your bot setup looks good.")
        print("\nNext steps:")
        print("1. Copy .env.example to .env")
        print("2. Add your BOT_TOKEN to the .env file")
        print("3. Configure your database URL (optional)")
        print("4. Run: python app.py")
        print("\nFor more details, see SETUP.md")
        return True
    else:
        print(f"\n❌ {failed} tests failed. Please fix the issues above.")
        print("\nCommon solutions:")
        print("1. Run: pip install -r requirements.txt")
        print("2. Make sure all files are in the correct locations")
        print("3. Check for any missing dependencies")
        print("4. Ensure you have a valid BOT_TOKEN in your .env file")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
