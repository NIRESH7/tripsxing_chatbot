import os
import asyncpg
from dotenv import load_dotenv
from .azure_client import get_chat_response

load_dotenv()

# Database Config
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "2006")
DB_NAME = os.getenv("DB_NAME", "tripsxing_chatbot")

async def get_pool():
    return await asyncpg.create_pool(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

async def generate_sql_query(user_question: str) -> str:
    """
    Generate a read-only SQL query from the user's question.
    """
    schema_info = """
    Tables:
    1. users (id, name, email, phone, joined_at)
    2. bookings (id, user_id, destination, trip_date, status)
    
    Relationships:
    - bookings.user_id references users.id
    """
    
    system_prompt = f"""
    You are a PostgreSQL expert. Your job is to convert natural language questions into SQL queries.
    
    Schema:
    {schema_info}
    
    Rules:
    1. Return ONLY the SQL query. No markdown, no explanation.
    2. Create ONLY READ-ONLY queries (SELECT). No INSERT, UPDATE, DELETE.
    3. If the question cannot be answered with the schema, return "NO_SQL".
    4. Use case-insensitive matching for names (e.g. ILIKE).
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Generate SQL for: {user_question}"}
    ]
    
    response = await get_chat_response(messages)
    
    # Clean up standard markdown code blocks if present
    response = response.replace("```sql", "").replace("```", "").strip()
    
    if "NO_SQL" in response:
        return None
        
    return response

async def execute_query(query: str):
    """
    Execute a read-only SQL query safely.
    """
    if not query.upper().startswith("SELECT"):
        return {"error": "Only SELECT queries are allowed for safety."}

    try:
        pool = await get_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(query)
            # Convert to list of dicts
            return [dict(row) for row in rows]
    except Exception as e:
        return {"error": str(e)}

async def process_data_question(user_question: str):
    """
    End-to-end handler: Text -> SQL -> Result -> Natural Language Answer
    """
    # 1. Generate SQL
    sql_query = await generate_sql_query(user_question)
    
    if not sql_query:
        return None, "I couldn't generate a database query for that."

    print(f"DEBUG SQL: {sql_query}")

    # 2. Execute Query
    results = await execute_query(sql_query)
    
    if isinstance(results, dict) and "error" in results:
         return None, f"Database Error: {results['error']}"
    
    if not results:
        return None, "I checked the database, but found no matching records."

    # 3. Summarize Results
    from .prompts import RAG_SYSTEM_PROMPT_TEMPLATE, USER_MESSAGE_TEMPLATE
    
    # Format the prompt with the SQL results acting as the "SEARCH_RESULTS"
    system_message = RAG_SYSTEM_PROMPT_TEMPLATE.format(db_context=str(results))
    user_message = USER_MESSAGE_TEMPLATE.format(user_question=user_question)

    summary_messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    
    final_answer = await get_chat_response(summary_messages, temperature=0.0) # Keep strictly factual
    return final_answer, "database_query"
