import asyncio
import os
import asyncpg
from dotenv import load_dotenv
from backend.elasticsearch_mock import index_document

load_dotenv()

# DB Config
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "2006")
DB_NAME = os.getenv("DB_NAME", "tripsxing_chatbot")

async def get_conn():
    return await asyncpg.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

async def run_indexing():
    conn = await get_conn()
    print("Starting Indexing Process...")

    # 1. Index USERS
    print("\n--- Indexing Users ---")
    users = await conn.fetch("SELECT * FROM users")
    for row in users:
        doc = dict(row)
        # Convert datetime objects to string for JSON serialization
        if 'joined_at' in doc: doc['joined_at'] = str(doc['joined_at'])
        
        index_document("users", doc['id'], doc)

    # 2. Index BOOKINGS
    print("\n--- Indexing Bookings ---")
    bookings = await conn.fetch("SELECT * FROM bookings")
    for row in bookings:
        doc = dict(row)
        if 'trip_date' in doc: doc['trip_date'] = str(doc['trip_date'])
        if 'created_at' in doc: doc['created_at'] = str(doc['created_at'])
        
        # Enrich booking with user name for better search logic
        user_name = await conn.fetchval("SELECT name FROM users WHERE id=$1", doc['user_id'])
        doc['user_name'] = user_name
        
        index_document("bookings", doc['id'], doc)

    # 3. Index FAQ (Knowledge Base)
    print("\n--- Indexing Knowledge Base ---")
    faqs = await conn.fetch("SELECT * FROM knowledge_base") # Assuming we renamed it or standard faq_entries
    # Fallback if table name is 'faq_entries' in current DB state
    if not faqs:
         try:
             faqs = await conn.fetch("SELECT * FROM faq_entries")
         except:
             print("Warning: No FAQ table found.")
    
    for row in faqs:
        doc = dict(row)
        if 'created_at' in doc: doc['created_at'] = str(doc['created_at'])
        # Clean up vector/binary fields if present
        if 'embedding' in doc: del doc['embedding'] 
        
        index_document("faq", doc['id'], doc)

    await conn.close()
    print("\n✅ Indexing Complete! Data is now in 'backend/data_indices/'")

if __name__ == "__main__":
    asyncio.run(run_indexing())
