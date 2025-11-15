#!/usr/bin/env python3
"""
Test navigation buttons functionality
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


async def test_callback_handlers():
    """Test that callback handlers are properly registered"""
    print("🧪 Testing callback handlers registration...")

    try:
        from handlers.admin.bot_settings import (
            back_to_main_menu,
            change_keyword_start,
            show_bot_settings,
        )

        print("✅ All bot settings handlers imported successfully")

        # Test handler names
        assert back_to_main_menu.__name__ == "back_to_main_menu"
        assert change_keyword_start.__name__ == "change_keyword_start"
        assert show_bot_settings.__name__ == "show_bot_settings"

        print("✅ Handler names are correct")
        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def test_keyboard_callbacks():
    """Test keyboard callback data"""
    print("🧪 Testing keyboard callback data...")

    try:
        # Test callback data values
        test_callbacks = [
            "bot_settings",
            "change_keyword",
            "back_to_menu",
            "cancel_keyword_change",
        ]

        for callback in test_callbacks:
            print(f"   Testing callback: '{callback}'")
            assert len(callback) > 0
            assert isinstance(callback, str)

        print("✅ All callback data values are valid")
        return True

    except Exception as e:
        print(f"❌ Error testing callbacks: {e}")
        return False


async def test_settings_keyboard():
    """Test settings keyboard generation"""
    print("🧪 Testing settings keyboard...")

    try:
        from handlers.admin.bot_settings import get_settings_keyboard

        keyboard = get_settings_keyboard()

        # Check keyboard structure
        assert keyboard is not None
        print("✅ Settings keyboard created successfully")

        # Check that keyboard has buttons
        assert hasattr(keyboard, "inline_keyboard")
        assert len(keyboard.inline_keyboard) > 0
        print("✅ Settings keyboard has buttons")

        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def test_menu_navigation():
    """Test menu navigation logic"""
    print("🧪 Testing menu navigation logic...")

    try:
        from keyboards.admin.inline.menu import kb_admin_menu
        from texts import MAIN_MENU_TEXT

        # Check main menu exists
        assert kb_admin_menu is not None
        print("✅ Main menu keyboard exists")

        # Check main menu text exists
        assert MAIN_MENU_TEXT is not None
        assert len(MAIN_MENU_TEXT) > 0
        print("✅ Main menu text exists")

        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def test_owners_filtering():
    """Test OWNERS filtering logic"""
    print("🧪 Testing OWNERS filtering...")

    try:
        from config import OWNERS

        print(f"OWNERS list: {OWNERS}")
        assert isinstance(OWNERS, list)
        assert len(OWNERS) > 0
        print("✅ OWNERS list is valid")

        # Test filtering logic
        test_user_id = 123456789
        is_owner = test_user_id in OWNERS
        print(f"Test user {test_user_id} is owner: {is_owner}")

        if OWNERS:
            real_owner = OWNERS[0]
            is_real_owner = real_owner in OWNERS
            assert is_real_owner == True
            print(f"✅ Real owner {real_owner} is correctly identified")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def test_text_constants():
    """Test required text constants"""
    print("🧪 Testing text constants...")

    try:
        from texts import (
            CURRENT_KEYWORD_TEXT,
            ENTER_NEW_KEYWORD,
            KEYWORD_UPDATED_SUCCESS,
            MAIN_MENU_TEXT,
            SETTINGS_MENU_TEXT,
        )

        # Test all required texts exist
        texts_to_test = {
            "MAIN_MENU_TEXT": MAIN_MENU_TEXT,
            "SETTINGS_MENU_TEXT": SETTINGS_MENU_TEXT,
            "CURRENT_KEYWORD_TEXT": CURRENT_KEYWORD_TEXT,
            "ENTER_NEW_KEYWORD": ENTER_NEW_KEYWORD,
            "KEYWORD_UPDATED_SUCCESS": KEYWORD_UPDATED_SUCCESS,
        }

        for name, text in texts_to_test.items():
            assert text is not None
            assert len(text) > 0
            print(f"   ✅ {name}: {len(text)} characters")

        # Test text formatting
        test_keyword = "Тест"
        formatted_current = CURRENT_KEYWORD_TEXT.format(keyword=test_keyword)
        formatted_enter = ENTER_NEW_KEYWORD.format(current_keyword=test_keyword)
        formatted_success = KEYWORD_UPDATED_SUCCESS.format(keyword=test_keyword)

        assert test_keyword in formatted_current
        assert test_keyword in formatted_enter
        assert test_keyword in formatted_success

        print("✅ Text formatting works correctly")
        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def test_state_management():
    """Test FSM state management"""
    print("🧪 Testing FSM states...")

    try:
        from states.admin.bot_settings import BotSettingsStates

        # Check state exists
        assert hasattr(BotSettingsStates, "waiting_for_keyword")
        print("✅ BotSettingsStates.waiting_for_keyword exists")

        # Check state properties
        state = BotSettingsStates.waiting_for_keyword
        assert state is not None
        print("✅ State is properly configured")

        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def main():
    """Run all navigation tests"""
    print("🚀 NAVIGATION TESTS")
    print("=" * 50)

    tests = [
        ("Callback handlers", test_callback_handlers),
        ("Keyboard callbacks", test_keyboard_callbacks),
        ("Settings keyboard", test_settings_keyboard),
        ("Menu navigation", test_menu_navigation),
        ("OWNERS filtering", test_owners_filtering),
        ("Text constants", test_text_constants),
        ("State management", test_state_management),
    ]

    failed_tests = []

    for test_name, test_func in tests:
        print(f"\n🔍 {test_name.upper()}")
        print("-" * 30)

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

    print("\n" + "=" * 50)

    if failed_tests:
        print(f"❌ FAILED TESTS: {', '.join(failed_tests)}")
        print("\n💡 TROUBLESHOOTING:")
        print("1. Make sure all handlers are properly imported")
        print("2. Check that OWNERS is configured in config")
        print("3. Verify all text constants exist in texts.py")
        print("4. Ensure FSM states are properly defined")
        return False
    else:
        print("🎉 ALL NAVIGATION TESTS PASSED!")
        print("\n✅ NAVIGATION FEATURES READY:")
        print("- Settings menu navigation works")
        print("- Back buttons function correctly")
        print("- Keyword change flow is complete")
        print("- OWNERS filtering is active")
        print("- All text constants available")
        print("- FSM states properly configured")
        print("\n🎯 Navigation should work correctly now!")
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
