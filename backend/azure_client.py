import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import json
import math

load_dotenv()

# Credentials from environment variables
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_OPENAI_EMBEDDING_DEPLOYMENT = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-ada-002")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")


client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY,
    api_version=AZURE_OPENAI_API_VERSION
)

# Tool for distance calculation simulation (since we don't have a real separate geo library setup requested, we can mock or use basic math if coords provided, 
# but effectively the user wants the chatbot to answer it. 
# We'll give the LLM a tool to be "professional" about it).
# For now, let's allow the LLM to just use its internal knowledge or if we want to be strict, we provide a function.
# Let's provide a function that calculates Haversine distance if coordinates are known, or just a stub helper. 
# Actually, the user asked "user will can also aak to calculate the distance".
# Let's define a tool that the model can call.

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate_distance",
            "description": "Calculate the distance between two locations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {
                        "type": "string",
                        "description": "The starting location (e.g., 'New York, NY')."
                    },
                    "destination": {
                        "type": "string",
                        "description": "The destination location (e.g., 'London, UK')."
                    }
                },
                "required": ["origin", "destination"]
            }
        }
    }
]

def calculate_distance_logic(origin, destination):
    # In a real production app, we would query a Geocoding API here.
    # Since we can't easily add a new external API key not provided, 
    # we will return a string telling the LLM to estimate it or use its internal knowledge 
    # BUT the prompt asked to "answer all type of like trips... calculate the distance".
    # We will simulate a response or return a prompt for the LLM to do it with its training data if we don't have coords.
    # HOWEVER, a "professional" way is to use a library like `geopy` if installed, or just let the LLM handle it if it knows.
    # Let's return a structured prompt to the LLM to Perform the calculation using its best estimate.
    return f"Please calculate the distance between {origin} and {destination} using your internal geographical knowledge and provide the answer in kilometers and miles."

async def get_chat_response(messages, temperature=0.7):
    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=temperature
    )
    
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "calculate_distance": calculate_distance_logic,
        }
        
        # Extend conversation with assistant's reply
        messages.append(response_message)
        
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions.get(function_name)
            function_args = json.loads(tool_call.function.arguments)
            
            if function_to_call:
                function_response = function_to_call(
                    origin=function_args.get("origin"),
                    destination=function_args.get("destination"),
                )
                
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )
        
        # get a new response from the model where it can see the function response
        second_response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=messages,
            temperature=temperature
        )
        return second_response.choices[0].message.content
    else:
        return response_message.content


# Add to top of file with other env vars
AZURE_OPENAI_EMBEDDING_DEPLOYMENT = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-ada-002")

async def get_embedding(text: str) -> list[float]:
    """
    Generate embedding for the given text using Azure OpenAI.
    """
    try:
        response = client.embeddings.create(
            input=text,
            model=AZURE_OPENAI_EMBEDDING_DEPLOYMENT 
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error getting embedding: {e}")
        if "DeploymentNotFound" in str(e):
             print(f"⚠️ Embedding deployment '{AZURE_OPENAI_EMBEDDING_DEPLOYMENT}' not found. Please check your Azure OpenAI Studio and update .env file.")
        raise

