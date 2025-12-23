from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from .database import db
from .azure_client import get_chat_response
import datetime

app = FastAPI()

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
    user_message = request.message
    
    # Construct history for OpenAI
    # System prompt
    system_message = {
        "role": "system",
        "content": "You are the TripsXing AI Assistant. Your goal is to help users with travel planning, trip ideas, and general travel questions. You are professional, enthusiastic, and knowledgeable. You can also calculate distances between locations when asked."
    }
    
    messages = [system_message]
    # Add context (simplified for now, ideally we pass full history)
    # If context is passed from frontend, append it.
    # Otherwise, we treat each request as fresh or rely on frontend to pass history.
    if request.context:
        messages.extend(request.context)
    
    messages.append({"role": "user", "content": user_message})

    try:
        response_text = await get_chat_response(messages)
        
        # Save to MongoDB
        chat_entry = {
            "user_message": user_message,
            "bot_response": response_text,
            "timestamp": datetime.datetime.utcnow()
        }
        await db.chats.insert_one(chat_entry)
        
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
