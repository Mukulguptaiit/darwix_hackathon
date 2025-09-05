import os
import requests
import librosa, soundfile as sf
import numpy as np
from pydub import AudioSegment
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

# Load Hugging Face emotion classifier (tiny, fast model)
clf = pipeline("sentiment-analysis")

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")  # Set your ElevenLabs API key as environment variable
ELEVEN_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # pick any ElevenLabs voice

if not ELEVEN_API_KEY:
    raise ValueError("Please set your ELEVEN_API_KEY environment variable")

app = FastAPI()

# Enable CORS
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins (simpler for demo)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def serve_interface():
    return FileResponse("interface.html", media_type="text/html")

@app.get("/audio")
def get_audio():
    import os
    if os.path.exists("final.wav"):
        return FileResponse(
            "final.wav", 
            media_type="audio/wav",
            headers={"Cache-Control": "no-cache, no-store, must-revalidate"}
        )
    else:
        return {"error": "Audio file not found"}

class InputText(BaseModel):
    text: str
    rate: float = 1.0  # Speed (0.5 to 2.0)
    pitch: float = 0.0  # Pitch in semitones (-12 to +12)
    volume: float = 0.0  # Volume in dB (-20 to +20)

# --- Step 1: Detect emotion ---
def detect_emotion(text):
    res = clf(text)[0]   # {'label': 'POSITIVE', 'score': 0.99}
    label = res['label'].upper()
    return label, res['score']

# --- Step 2: Map emotion to params ---
def map_emotion(emotion, confidence):
    params = {'rate': 1.0, 'pitch': 0.0, 'volume': 0.0}
    if emotion == "POSITIVE":
        params['rate'] = 1.2
        params['pitch'] = +2
        params['volume'] = +3
    elif emotion == "NEGATIVE":
        params['rate'] = 0.85
        params['pitch'] = -2
        params['volume'] = -3
    else:  # NEUTRAL
        params['rate'] = 1.0
        params['pitch'] = 0.0
        params['volume'] = 0.0
    return params

# --- Step 3: Call ElevenLabs API ---
def elevenlabs_tts(text, out_file="raw.wav"):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVEN_VOICE_ID}"
    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
    }
    response = requests.post(url, headers=headers, json=data)
    with open(out_file, "wb") as f:
        f.write(response.content)
    return out_file

# --- Step 4: Modify audio locally ---
def modulate_audio(inp, out, rate=1.0, pitch=0.0, volume=0.0):
    """
    Modulate audio with rate (speed), pitch, and volume changes
    """
    y, sr = librosa.load(inp, sr=None)
    
    # Pitch shift (in semitones) - using effects module
    if pitch != 0.0:
        y = librosa.effects.pitch_shift(y, sr=sr, n_steps=pitch)
    
    # Time stretch (rate change) using phase vocoder
    if rate != 1.0:
        # Use librosa's phase vocoder for time stretching
        D = librosa.stft(y)
        D_stretched = librosa.phase_vocoder(D, rate=rate)
        y = librosa.istft(D_stretched)
    
    # Volume adjustment (in dB)
    if volume != 0.0:
        gain = 10 ** (volume / 20.0)
        y = y * gain
    
    # Normalize to prevent clipping
    y = y / np.max(np.abs(y)) * 0.98
    
    sf.write(out, y, sr)
    return out

# --- FastAPI endpoint ---
@app.post("/speak")
def speak(data: InputText):
    text = data.text
    emotion, conf = detect_emotion(text)
    
    # Use user-provided parameters instead of emotion-based ones
    base_file = elevenlabs_tts(text, "neutral.wav")
    final_file = modulate_audio(base_file, "final.wav",
                                rate=data.rate,
                                pitch=data.pitch,
                                volume=data.volume)
    return {
        "emotion": emotion,
        "confidence": conf,
        "params": {
            "rate": data.rate,
            "pitch": data.pitch,
            "volume": data.volume
        },
        "audio_file": final_file
    }