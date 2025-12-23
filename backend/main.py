from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from .database import get_pool, init_db, close_db
from .azure_client import get_chat_response
import datetime

app = FastAPI()

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    await init_db()

@app.on_event("shutdown")
async def shutdown_event():
    await close_db()

# CORS configuration
origins = [
    "http://localhost:5173",  # Vite default
    "http://localhost:5174",  # Vite fallback
    "http://localhost:5175",  # Vite fallback 2
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    context: list = [] # Previous messages

@app.get("/")
def read_root():
    return {"status": "TripsXing Chatbot API is running"}


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        user_message = request.message
        
        # ---------------------------------------------------------
        # UNIFIED SEARCH ENGINE LOGIC (Mock ElasticSearch)
        # ---------------------------------------------------------
        from .elasticsearch_mock import search
        from .prompts import RAG_SYSTEM_PROMPT_TEMPLATE, USER_MESSAGE_TEMPLATE

        # 1. Search across all indices (Federated Search)
        # print(f"DEBUG: Searching Engine for: '{user_message}'")
        
        hits_users = search("users", user_message)
        hits_bookings = search("bookings", user_message)
        hits_faq = search("faq", user_message)
        
        # Combine results
        all_hits = {
            "user_records": hits_users,
            "booking_records": hits_bookings,
            "knowledge_base": hits_faq
        }
        
        # 2. RAG Generation
        # Inject search results into the prompt
        system_message = RAG_SYSTEM_PROMPT_TEMPLATE.format(db_context=str(all_hits))
        user_msg_formatted = USER_MESSAGE_TEMPLATE.format(user_question=user_message)
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_msg_formatted}
        ]
        
        # Generate Answer
        response_text = await get_chat_response(messages, temperature=0.0)
        source = "search_engine_rag"
        score = 1.0 if (hits_users or hits_bookings or hits_faq) else 0.0

        # Save to PostgreSQL (chat history)
        try:
            pool = await get_pool()
            async with pool.acquire() as conn:
                await conn.execute(
                    "INSERT INTO chats (user_message, bot_response, timestamp) VALUES ($1, $2, $3)",
                    user_message,
                    response_text,
                    datetime.datetime.utcnow()
                )
        except Exception as e:
            print(f"Error saving chat history: {e}")
        
        return {
            "response": response_text,
            "source": source,
            "score": score
        }

    except Exception as e:
        import traceback
        error_msg = f"CRITICAL ERROR in /chat:\n{str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        with open("backend_error.log", "w") as f:
            f.write(error_msg)
            
        return {
            "response": f"Sorry, I encountered an internal error. Debug: {str(e)}",
            "source": "error",
            "score": 0.0
        }

@app.post("/faq/add")
async def add_faq_endpoint(item: dict):
    from .faq_service import add_faq
    try:
        await add_faq(item['question'], item['answer'], item.get('category', 'general'))
        return {"status": "success", "message": "FAQ added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
