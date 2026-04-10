import edge_tts
import io
from app.config import VOICE

async def text_to_speech(text):
    communicate = edge_tts.Communicate(text, VOICE)
    audio_buffer = io.BytesIO()
    
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_buffer.write(chunk["data"])
    
    audio_buffer.seek(0)
    return audio_buffer