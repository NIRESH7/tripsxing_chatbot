import asyncio
import os
import asyncpg
from dotenv import load_dotenv
import json
from backend.azure_client import get_embedding

load_dotenv()

# PostgreSQL connection settings
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "2006")
DB_NAME = os.getenv("DB_NAME", "tripsxing_chatbot")

SAMPLE_QUESTIONS = [
    {
        "question": "What destinations does TripsXing offer?",
        "answer": "TripsXing offers curated travel experiences to destinations worldwide, including popular locations in Europe, Asia, Africa, and the Americas. Each trip is customized to match your preferences and budget.",
        "category": "services"
    },
    {
        "question": "How do I book a trip with TripsXing?",
        "answer": "Booking with TripsXing is easy! Simply chat with our AI assistant to describe your ideal trip, and we'll create a personalized itinerary. You can review, customize, and confirm your booking directly through our platform.",
        "category": "booking"
    },
    {
        "question": "What is the cancellation policy?",
        "answer": "TripsXing offers flexible cancellation up to 14 days before departure for a full refund. Cancellations within 7-14 days receive a 50% refund. For cancellations within 7 days, please contact our support team for case-by-case review.",
        "category": "policies"
    },
    {
        "question": "Do you offer group discounts?",
        "answer": "Yes! TripsXing offers special group rates for parties of 6 or more travelers. Contact our team for a customized group package and pricing.",
        "category": "pricing"
    },
    {
        "question": "What payment methods are accepted?",
        "answer": "We accept all major credit cards (Visa, Mastercard, American Express), PayPal, and bank transfers. Payment plans are available for trips over $2,000.",
        "category": "payment"
    }
]

async def init_faq_db():
    print(f"Connecting to database {DB_NAME}...")
    try:
        conn = await asyncpg.connect(
             host=DB_HOST,
             port=DB_PORT,
             user=DB_USER,
             password=DB_PASSWORD,
             database=DB_NAME
        )
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return

    try:
        # Try to create pgvector extension
        try:
             await conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
             print("✅ pgvector extension enabled")
             has_vector = True
        except Exception:
             print("⚠️ pgvector extension NOT available. Using JSONB for embeddings (slower but compatible).")
             has_vector = False

        # Create table
        print("Creating entries table...")
        if has_vector:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS faq_entries (
                    id SERIAL PRIMARY KEY,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    category TEXT,
                    embedding vector(1536),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        else:
             await conn.execute("""
                CREATE TABLE IF NOT EXISTS faq_entries (
                    id SERIAL PRIMARY KEY,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    category TEXT,
                    embedding JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        
        # Check if empty
        count = await conn.fetchval("SELECT COUNT(*) FROM faq_entries")
        if count == 0:
            print("Populating sample data...")
            for item in SAMPLE_QUESTIONS:
                # Skip actual embedding generation since model is missing
                # We will use LLM-based matching instead of vector search
                dummy_embedding = [0.0] * 1536 
                
                try:
                    if has_vector:
                         await conn.execute(
                            "INSERT INTO faq_entries (question, answer, category, embedding) VALUES ($1, $2, $3, $4)",
                            item['question'], item['answer'], item['category'], dummy_embedding
                        )
                    else:
                        await conn.execute(
                            "INSERT INTO faq_entries (question, answer, category, embedding) VALUES ($1, $2, $3, $4)",
                            item['question'], item['answer'], item['category'], json.dumps(dummy_embedding)
                        )
                    print(f"✅ Added: {item['question']}")
                except Exception as e:
                    print(f"❌ Failed to add item {item['question']}: {e}")
        else:
            print(f"Table already has {count} entries. Skipping initialization.")

        await conn.close()
        print("✅ FAQ database initialization complete!")

    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        await conn.close()

if __name__ == "__main__":
    asyncio.run(init_faq_db())
