import json
import os
import re
from collections import defaultdict

# Where to store the "indices" (JSON files)
DATA_DIR = os.path.join(os.path.dirname(__file__), "data_indices")
os.makedirs(DATA_DIR, exist_ok=True)

def get_index_path(index_name):
    return os.path.join(DATA_DIR, f"{index_name}.json")

def load_index(index_name):
    path = get_index_path(index_name)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_index(index_name, data):
    path = get_index_path(index_name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def index_document(index_name, doc_id, doc_body):
    """
    Simulates: PUT /index_name/_doc/doc_id
    """
    data = load_index(index_name)
    data[str(doc_id)] = doc_body
    save_index(index_name, data)
    print(f"Indexed document {doc_id} into {index_name}")

def tokenize(text):
    if not text:
        return []
    # Simple tokenization: lowercase, remove non-alphanumeric
    text = str(text).lower()
    tokens = re.findall(r'\b\w+\b', text)
    return set(tokens) # Unique tokens for simple keyword matching

def search(index_name, query, size=3):
    """
    Simulates: POST /index_name/_search
    Performs a simple keyword score match.
    """
    data = load_index(index_name)
    if not data:
        return []

    query_tokens = tokenize(query)
    scored_results = []

    for doc_id, doc in data.items():
        score = 0
        # Search across all string fields values
        doc_text = " ".join([str(v) for v in doc.values()])
        doc_tokens = tokenize(doc_text)
        
        # Calculate overlap (Mock Scoring)
        overlap = query_tokens.intersection(doc_tokens)
        score = len(overlap)
        
        # Boost for exact substring match in specific fields (like 'name' or 'question')
        if 'name' in doc and query.lower() in str(doc['name']).lower():
            score += 5
        if 'question' in doc and query.lower() in str(doc['question']).lower():
            score += 5

        if score > 0:
            scored_results.append({
                "_id": doc_id,
                "_score": score,
                "_source": doc
            })

    # Sort by score descending
    scored_results.sort(key=lambda x: x["_score"], reverse=True)
    
    return scored_results[:size]
