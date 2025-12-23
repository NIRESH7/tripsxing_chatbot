import asyncio
import os
import asyncpg
from dotenv import load_dotenv
import json
import math
from backend.azure_client import get_embedding

load_dotenv()

# PostgreSQL connection settings
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "2006")
DB_NAME = os.getenv("DB_NAME", "tripsxing_chatbot")


async def debug_matching():
    print(f"Connecting to database {DB_NAME}...")
    try:
        # Import the new logic
        from backend.faq_service import find_similar_question
        
        test_questions = [
            "What destinations does TripsXing offer?",
            "Can I cancel my trip?",
            "How do I pay?",
            "What is the weather in London?" # Should match nothing
        ]
        
        for q in test_questions:
            print(f"\n--------------------------------------------------")
            print(f"Testing Question: '{q}'")
            answer, score = await find_similar_question(q)
            
            if answer:
                print(f"✅ MATCH FOUND! (Score: {score})")
                print(f"Answer: {answer[:100]}...")
            else:
                print(f"❌ NO MATCH FOUND.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(debug_matching())
