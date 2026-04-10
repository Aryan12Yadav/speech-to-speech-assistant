from pymongo import MongoClient
from app.config import MONGODB_URI, MONGODB_DB
from datetime import datetime

# MongoDB se connection banta hai
client = MongoClient(MONGODB_URI)

# Database select hoti hai
db = client[MONGODB_DB]

# Collection select hoti hai (table jaisi hoti hai SQL mein)
collection = db["conversations"]

def save_conversation(session_id, user_text, bot_text, input_audio_url, output_audio_url):
    doc = {
        "session_id": session_id,
        "user_text": user_text,
        "bot_text": bot_text,
        "input_audio_url": input_audio_url,
        "output_audio_url": output_audio_url,
        "timestamp": datetime.utcnow()
    }
    result = collection.insert_one(doc)
    print(f"Saved to MongoDB: {result.inserted_id}")