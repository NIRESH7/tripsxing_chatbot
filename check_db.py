import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def check_db():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["tripsxingchatbot"]
    chats_collection = db["chats"]
    
    count = await chats_collection.count_documents({})
    print(f"Total documents: {count}")
    
    cursor = chats_collection.find().sort("timestamp", -1).limit(5)
    async for doc in cursor:
        print(f"User: {doc['user_message']}")
        print(f"Bot: {doc['bot_response'][:100]}...")
        print("-" * 20)

if __name__ == "__main__":
    asyncio.run(check_db())
