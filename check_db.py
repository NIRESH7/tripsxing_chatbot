import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL connection settings
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "2006")
DB_NAME = os.getenv("DB_NAME", "tripsxing_chatbot")

async def check_db():
    try:
        # Connect to PostgreSQL
        conn = await asyncpg.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        
        # Count total chats
        count = await conn.fetchval("SELECT COUNT(*) FROM chats")
        print(f"Total chat records: {count}")
        print("-" * 50)
        
        # Get last 5 chats
        rows = await conn.fetch("""
            SELECT user_message, bot_response, timestamp 
            FROM chats 
            ORDER BY timestamp DESC 
            LIMIT 5
        """)
        
        for row in rows:
            print(f"User: {row['user_message']}")
            print(f"Bot: {row['bot_response'][:100]}...")
            print(f"Time: {row['timestamp']}")
            print("-" * 50)
        
        await conn.close()
        print("\nDatabase connection successful!")
        
    except Exception as e:
        print(f"Error connecting to database: {e}")
        print("\nMake sure:")
        print("1. PostgreSQL is running")
        print("2. Database 'tripsxing_chatbot' exists")
        print("3. Username and password are correct")
        print("4. The chats table exists (it will be created automatically on first run)")

if __name__ == "__main__":
    asyncio.run(check_db())
