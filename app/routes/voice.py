from fastapi import APIRouter, UploadFile, File
import uuid
import io

from app.services.stt import speech_to_text
from app.services.tts import text_to_speech
from app.services.chatbot import get_response
from app.services.s3 import upload_to_s3
from app.services.database import save_conversation

router = APIRouter()

@router.post("/voice-chat")
async def voice_chat(file: UploadFile = File(...)):

    session_id = str(uuid.uuid4())
    
    # Audio bytes read karo
    audio_bytes = await file.read()
    
    # Input audio S3 pe upload karo
    input_buffer = io.BytesIO(audio_bytes)
    input_url = upload_to_s3(input_buffer, f"voice_input/{session_id}.webm", "audio/webm")
    
    # STT - temp file banana padega whisper ke liye
    import tempfile
    import os
    with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name
    
    text = speech_to_text(tmp_path)
    os.unlink(tmp_path)  # Whisper ke baad delete
    
    # Chatbot response
    response = get_response(text)
    
    # TTS - memory mein audio banao
    output_buffer = await text_to_speech(response)
    
    # Output audio S3 pe upload karo
    output_url = upload_to_s3(output_buffer, f"voice_output/{session_id}.mp3", "audio/mpeg")
    
    # MongoDB mein save karo
    save_conversation(session_id, text, response, input_url, output_url)
    
    return {
        "session_id": session_id,
        "user_text": text,
        "bot_text": response,
        "audio": output_url  # S3 ka direct URL
    }