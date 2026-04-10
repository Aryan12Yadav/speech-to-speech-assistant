# Voice Assistant

A university capstone project built by a student to explore how modern AI services can be combined to create a real-time speech-to-speech voice assistant. This project takes your voice as input, understands what you said, gets a smart reply from a chatbot, and speaks the reply back to you.

---

## What This Project Does

You open the web app, click the mic button, and speak. The app records your voice, sends it to the server, converts it to text, passes that text to a chatbot API, converts the chatbot reply back to speech, and plays it for you. All of this happens in a few seconds.

On top of that, every conversation is saved. The audio files go to AWS S3 and the text data goes to MongoDB Atlas so nothing is lost.

---

## How It Works - Full Workflow

```

User speaks into mic
↓
Browser records audio (WebM format)
↓
Audio sent to FastAPI server via POST /api/voice-chat
↓
Audio uploaded to AWS S3 (voice_input folder)
↓
Whisper AI converts audio to text (Speech to Text)
↓
Text sent to Chatbot API
↓
Chatbot returns a reply
↓
Edge TTS converts reply to audio (Text to Speech)
↓
Audio uploaded to AWS S3 (voice_output folder)
↓
MongoDB saves session_id, user_text, bot_text, audio URLs, timestamp
↓
S3 audio URL sent back to browser
↓
Browser plays the audio reply



## Tech Stack and Why I Used Each One

| Technology | Purpose | Why |
|---|---|---|
| FastAPI | Backend server | Fast, modern, async support |
| OpenAI Whisper | Speech to Text | Free, runs locally, good accuracy |
| Microsoft Edge TTS | Text to Speech | Free, natural Hindi voice |
| AWS S3 | Audio file storage | Reliable cloud storage |
| MongoDB Atlas | Conversation storage | Flexible, free tier available |
| Docker | Containerization | Easy deployment anywhere |
| Render | Cloud deployment | Free tier, supports Docker |

---

## Project Structure

```
speech-assistant/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # All environment variables loaded here
│   ├── services/
│   │   ├── stt.py           # Whisper speech to text logic
│   │   ├── tts.py           # Edge TTS text to speech logic
│   │   ├── chatbot.py       # Chatbot API call logic
│   │   ├── s3.py            # AWS S3 upload logic
│   │   └── database.py      # MongoDB save logic
│   ├── utils/
│   │   └── audio.py         # Audio helper functions
│   ├── routes/
│   │   └── voice.py         # API endpoint /voice-chat
│   ├── templates/
│   │   └── index.html       # Frontend HTML page
│   └── static/
│       ├── css/
│       │   └── style.css    # Styling
│       └── js/
│           └── app.js       # Frontend recording logic
├── .env                     # Secret credentials (never push to git)
├── .env.example             # Template for others to setup
├── .gitignore               # Files to ignore in git
├── .dockerignore            # Files to ignore in Docker
├── Dockerfile               # Docker build instructions
├── requirements.txt         # Python dependencies
└── README.md
```

---

## Environment Variables

Create a `.env` file in the root directory and fill in your credentials:

```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
MONGODB_DB=speech_assistant

AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=ap-south-1
S3_BUCKET_NAME=your_bucket_name

CHATBOT_API= **
VOICE=hi-IN-MadhurNeural
```


## Docker Setup

### Build the image

```bash
docker build -t speech-assistant .
```

### Run the container

```bash
docker run -p 8000:8000 --env-file .env speech-assistant
```

---

## Deployment on Render

1. Push your code to GitHub (make sure `.env` is in `.gitignore`)
2. Go to [render.com](https://render.com) and create a new Web Service
3. Connect your GitHub repository
4. Select **Docker** as the environment
5. Add all environment variables from your `.env` file in the Render dashboard
6. Click Deploy

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | / | Home page with mic interface |
| POST | /api/voice-chat | Accepts audio, returns text and audio URL |

### POST /api/voice-chat

Request - multipart form data with audio file

Response:
```json
{
  "session_id": "uuid-auto-generated",
  "user_text": "what is the price of land",
  "bot_text": "Aryan here. Main aapki help kar sakta hoon.",
  "audio": "https://your-bucket.s3.ap-south-1.amazonaws.com/voice_output/uuid.mp3"
}
```

---

## MongoDB Document Structure

Every conversation is saved in MongoDB with this structure:

```json
{
  "session_id": "uuid-auto-generated",
  "user_text": "what is the price of land",
  "bot_text": "Aryan here. Main aapki help kar sakta hoon.",
  "input_audio_url": "https://s3.../voice_input/uuid.webm",
  "output_audio_url": "https://s3.../voice_output/uuid.mp3",
  "timestamp": "2024-01-01T10:30:00"
}
```

---

## AWS S3 Structure

```
your-bucket/
├── voice_input/
│   └── uuid.webm    # User ka recorded audio
└── voice_output/
    └── uuid.mp3     # Bot ka generated audio
```

---

## Challenges I Faced

- Whisper by default detects wrong language, fixed by setting language parameter
- Browser records in WebM format not WAV, had to match this everywhere
- Edge TTS needs internet connection to generate audio
- S3 public access policy needed to be set manually for audio playback
- Starlette updated their TemplateResponse syntax which broke the home route

---

## Future Improvements

- Add user authentication
- Build a conversation history page
- Add support for multiple languages
- Improve UI with real-time waveform animation
- Add response streaming for faster replies

























