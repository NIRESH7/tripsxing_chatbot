import requests
import json

def test_chat():
    url = "http://localhost:8000/chat"
    payload = {"message": "Who is Niresh?"}
    
    print(f"Testing {url} with payload: {payload}")
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_chat()
