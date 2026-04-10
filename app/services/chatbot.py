import requests
from app.config import CHATBOT_API

def get_response(text):
    try:
        res = requests.post(
            CHATBOT_API,
            json={
                "user_id": "voice_user",
                "query": text
            },
            timeout=30
        )
        print(f"API Status: {res.status_code}")
        print(f"API Response: {res.text}")
        
        return res.json()["response"]
    
    except Exception as e:
        print(f"Chatbot API Error: {e}")
        return "Sorry, kuch problem hai abhi."