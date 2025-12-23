import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL connection settings
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "2006")
DB_NAME = os.getenv("DB_NAME", "tripsxing_chatbot")

# Connection pool
_pool = None

async def get_pool():
    """Get or create database connection pool"""
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            min_size=1,
            max_size=10
        )
    return _pool

async def init_db():
    """Initialize database and create chats table if it doesn't exist"""
    try:
        pool = await get_pool()
        async with pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS chats (
                    id SERIAL PRIMARY KEY,
                    user_message TEXT NOT NULL,
                    bot_response TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            # Create index on timestamp for faster queries
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_chats_timestamp 
                ON chats(timestamp DESC)
            """)
            print(f"✅ Database connected: {DB_NAME}")
            print("✅ Chats table initialized")
    except asyncpg.InvalidCatalogNameError:
        print(f"❌ ERROR: Database '{DB_NAME}' does not exist!")
        print(f"   Please create it using: CREATE DATABASE {DB_NAME};")
        raise
    except asyncpg.InvalidPasswordError:
        print(f"❌ ERROR: Invalid PostgreSQL password!")
        raise
    except Exception as e:
        print(f"❌ ERROR connecting to database: {e}")
        raise

async def close_db():
    """Close database connection pool"""
    global _pool
    if _pool:
        await _pool.close()
        _pool = None
