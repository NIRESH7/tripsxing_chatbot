import asyncio
import asyncpg

async def test_connection():
    try:
        print("Testing PostgreSQL connection...")
        print("Database: tripsxing_chatbot")
        print("User: postgres")
        print("Password: 2006")
        print("-" * 50)
        
        conn = await asyncpg.connect(
            host="localhost",
            port=5432,
            user="postgres",
            password="2006",
            database="tripsxing_chatbot"
        )
        
        # Test query
        version = await conn.fetchval("SELECT version();")
        print("✅ Connection successful!")
        print(f"PostgreSQL Version: {version[:50]}...")
        
        # Check if chats table exists
        table_exists = await conn.fetchval("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'chats'
            );
        """)
        
        if table_exists:
            print("✅ Chats table exists!")
            count = await conn.fetchval("SELECT COUNT(*) FROM chats")
            print(f"   Total chat records: {count}")
        else:
            print("ℹ️  Chats table doesn't exist yet (will be created on server startup)")
        
        await conn.close()
        print("\n✅ Database connection test PASSED!")
        
    except asyncpg.InvalidCatalogNameError:
        print("❌ Error: Database 'tripsxing_chatbot' does not exist!")
        print("\nPlease create it using one of these methods:")
        print("1. pgAdmin: Right-click Databases → Create → Database → Name: tripsxing_chatbot")
        print("2. psql: CREATE DATABASE tripsxing_chatbot;")
    except asyncpg.InvalidPasswordError:
        print("❌ Error: Invalid password!")
    except asyncpg.ConnectionRefusedError:
        print("❌ Error: Could not connect to PostgreSQL!")
        print("   Make sure PostgreSQL is running.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())

