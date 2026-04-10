from groq import Groq
from app.config import GROQ_API_KEY


client = Groq(api_key=GROQ_API_KEY)

def speech_to_text(audio_bytes):
    transcription = client.audio.transcriptions.create(
        file = ('audio.webm',audio_bytes),
        model = 'whisper-large-v3',
        language = 'en'
    )
    return transcription.text