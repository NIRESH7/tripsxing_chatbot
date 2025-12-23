from .database import get_pool
from .azure_client import get_embedding
import json
import math

async def cosine_similarity(v1, v2):
    "Compute cosine similarity between two vectors."
    dot_product = sum(a * b for a, b in zip(v1, v2))
    magnitude1 = math.sqrt(sum(a * a for a in v1))
    magnitude2 = math.sqrt(sum(b * b for b in v2))
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)

    return dot_product / (magnitude1 * magnitude2)

async def find_similar_question(user_question: str, threshold: float = 0.75):
    """
    Find the most similar question in the database using LLM (GPT-4o-mini)
    since we don't have an embedding model.
    """
    from .azure_client import get_chat_response
    pool = await get_pool()
    
    async with pool.acquire() as conn:
        # Fetch all FAQs (okay for small dataset, limit to 50 for safety)
        rows = await conn.fetch("SELECT id, question, answer FROM faq_entries LIMIT 50")
        
        if not rows:
            return None, 0
            
        # Contextual Search Prompt
        faq_list = "\n".join([f"ID {row['id']}: Q: {row['question']} | A: {row['answer']}" for row in rows])
        
        messages = [
            {"role": "system", "content": "You are a strict database matcher. You have a list of FAQs. Your job is to determine if the user's question matches ANY of the FAQ questions semantically. If yes, return the ID of the match. If no, return 'NO_MATCH'. Do not answer the question yourself. Only return the ID or 'NO_MATCH'."},
            {"role": "user", "content": f"Here is the database:\n{faq_list}\n\nUser Question: '{user_question}'\n\nDoes this match any FAQ? Return only the ID (e.g., 'ID 1') or 'NO_MATCH'."}
        ]
        
        try:
            response = await get_chat_response(messages)
            print(f"DEBUG: LLM Match Response: {response}")
            
            if "NO_MATCH" in response:
                return None, 0
            
            # Extract ID
            import re
            match = re.search(r"ID\s*(\d+)", response, re.IGNORECASE)
            if match:
                matched_id = int(match.group(1))
                # Find the row
                for row in rows:
                    if row['id'] == matched_id:
                        # FOUND MATCH: Now Synthesize using the RAG Prompt
                        raw_answer = row['answer']
                        
                        from .prompts import RAG_SYSTEM_PROMPT_TEMPLATE, USER_MESSAGE_TEMPLATE
                        
                        # We pass the raw answer as the "SEARCH_RESULTS" or "Context"
                        system_message = RAG_SYSTEM_PROMPT_TEMPLATE.format(db_context=raw_answer)
                        user_message_content = USER_MESSAGE_TEMPLATE.format(user_question=user_question)
                        
                        messages = [
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": user_message_content}
                        ]
                        
                        # Generate natural response
                        final_response = await get_chat_response(messages, temperature=0.0)
                        return final_response, 1.0
                        
            return None, 0
            
        except Exception as e:
            print(f"Error in LLM matching: {e}")
            return None, 0

async def add_faq(question: str, answer: str, category: str = "general"):
    """
    Add a new FAQ entry to the database.
    """
    pool = await get_pool()
    embedding = await get_embedding(question)
    
    async with pool.acquire() as conn:
        # Check if vector col exists as vector type or jsonb
        # We'll just try to insert, relying on the driver to handle list -> vector/json conversion if properly set up,
        # otherwise we might need to json.dumps(embedding) if it's JSONB.
        # Best check: see init usage.
        
        # We'll try generic insert, if it fails due to type, we retry with json string.
        try:
             await conn.execute(
                "INSERT INTO faq_entries (question, answer, category, embedding) VALUES ($1, $2, $3, $4)",
                question, answer, category, embedding
            )
        except Exception:
            # Fallback for JSONB
            await conn.execute(
                "INSERT INTO faq_entries (question, answer, category, embedding) VALUES ($1, $2, $3, $4)",
                question, answer, category, json.dumps(embedding)
            )
