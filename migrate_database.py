#!/usr/bin/env python3
"""
Скрипт миграции базы данных для добавления новых полей
"""

import asyncio
import logging
import sqlite3
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("migration.log", encoding="utf-8"),
    ],
)

logger = logging.getLogger(__name__)


def get_database_path():
    """Get the path to the SQLite database"""
    db_path = Path("db.sqlite3")
    if not db_path.exists():
        raise FileNotFoundError(f"Database file not found: {db_path}")
    return str(db_path)


def backup_database():
    """Create a backup of the database before migration"""
    import shutil
    from datetime import datetime

    db_path = get_database_path()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"db_backup_{timestamp}.sqlite3"

    shutil.copy2(db_path, backup_path)
    logger.info(f"Database backup created: {backup_path}")
    return backup_path


def check_column_exists(cursor, table_name, column_name):
    """Check if a column exists in a table"""
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [column[1] for column in cursor.fetchall()]
    return column_name in columns


def migrate_giveaway_table(cursor):
    """Add early_finish column to giveaway table"""
    table_name = "giveaway"
    column_name = "early_finish"

    if not check_column_exists(cursor, table_name, column_name):
        logger.info(f"Adding {column_name} column to {table_name} table...")
        cursor.execute(
            f"ALTER TABLE {table_name} ADD COLUMN {column_name} INTEGER DEFAULT 0"
        )
        logger.info(f"✅ Column {column_name} added successfully")
    else:
        logger.info(f"Column {column_name} already exists in {table_name} table")


def create_bot_settings_table(cursor):
    """Create bot_settings table if it doesn't exist"""
    table_name = "bot_settings"

    # Check if table exists
    cursor.execute(
        """
        SELECT name FROM sqlite_master
        WHERE type='table' AND name=?
    """,
        (table_name,),
    )

    if not cursor.fetchone():
        logger.info(f"Creating {table_name} table...")
        cursor.execute("""
            CREATE TABLE bot_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                participation_keyword TEXT DEFAULT 'Участвую',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Insert default settings
        cursor.execute("""
            INSERT INTO bot_settings (participation_keyword)
            VALUES ('Участвую')
        """)

        logger.info(f"✅ Table {table_name} created successfully with default settings")
    else:
        logger.info(f"Table {table_name} already exists")


def run_migration():
    """Run the database migration"""
    try:
        # Create backup
        backup_path = backup_database()
        logger.info(f"Backup created: {backup_path}")

        # Connect to database
        db_path = get_database_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        logger.info("Starting database migration...")

        # Run migrations
        migrate_giveaway_table(cursor)
        create_bot_settings_table(cursor)

        # Commit changes
        conn.commit()
        logger.info("✅ All migrations completed successfully")

        # Verify changes
        logger.info("Verifying migration results...")

        # Check giveaway table
        cursor.execute("PRAGMA table_info(giveaway)")
        giveaway_columns = [column[1] for column in cursor.fetchall()]
        logger.info(f"Giveaway table columns: {giveaway_columns}")

        if "early_finish" in giveaway_columns:
            logger.info("✅ early_finish column verified in giveaway table")
        else:
            logger.error("❌ early_finish column not found in giveaway table")

        # Check bot_settings table
        cursor.execute("PRAGMA table_info(bot_settings)")
        settings_columns = [column[1] for column in cursor.fetchall()]
        logger.info(f"Bot_settings table columns: {settings_columns}")

        # Check default settings
        cursor.execute("SELECT * FROM bot_settings LIMIT 1")
        settings_row = cursor.fetchone()
        if settings_row:
            logger.info(
                f"✅ Default settings found: ID={settings_row[0]}, keyword='{settings_row[1]}'"
            )
        else:
            logger.warning("⚠️ No default settings found")

    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")
        import traceback

        logger.error(f"Full error details:\n{traceback.format_exc()}")
        return False

    finally:
        if "conn" in locals():
            conn.close()

    return True


async def test_tortoise_integration():
    """Test that Tortoise ORM works with the migrated database"""
    try:
        from database import BotSettings, GiveAway, initialize_database

        logger.info("Testing Tortoise ORM integration...")

        # Initialize database
        await initialize_database()
        logger.info("✅ Tortoise ORM initialized successfully")

        # Test BotSettings
        keyword = await BotSettings.get_participation_keyword()
        logger.info(f"✅ BotSettings test passed, current keyword: '{keyword}'")

        # Test GiveAway model (check if early_finish field works)
        giveaway_count = await GiveAway.all().count()
        logger.info(f"✅ GiveAway model test passed, found {giveaway_count} giveaways")

        # Close connections
        from tortoise import Tortoise

        await Tortoise.close_connections()

        return True

    except Exception as e:
        logger.error(f"❌ Tortoise integration test failed: {e}")
        import traceback

        logger.error(f"Full error details:\n{traceback.format_exc()}")
        return False


async def main():
    """Main migration function"""
    logger.info("🚀 Starting database migration process...")
    logger.info("=" * 60)

    # Run SQL migration
    success = run_migration()

    if success:
        logger.info("=" * 60)
        logger.info("🧪 Testing Tortoise ORM integration...")

        # Test Tortoise integration
        tortoise_success = await test_tortoise_integration()

        if tortoise_success:
            logger.info("=" * 60)
            logger.info("🎉 MIGRATION COMPLETED SUCCESSFULLY!")
            logger.info("=" * 60)
            logger.info("")
            logger.info("📋 WHAT WAS DONE:")
            logger.info("✅ Added 'early_finish' column to 'giveaway' table")
            logger.info("✅ Created 'bot_settings' table with default settings")
            logger.info("✅ Verified Tortoise ORM compatibility")
            logger.info("")
            logger.info("🔄 RESTART YOUR BOT to apply changes")
            return True
        else:
            logger.error("❌ Tortoise integration test failed")
            return False
    else:
        logger.error("❌ Migration failed")
        return False


if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        logger.info("Migration cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)
