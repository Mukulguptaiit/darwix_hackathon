import os
import io
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
    # Audio processing parameters
    rate: float = 1.0  # Speed (0.5 to 2.0)
    pitch: float = 0.0  # Pitch in semitones (-12 to +12)
    volume: float = 0.0  # Volume in dB (-20 to +20)
    # ElevenLabs voice settings
    stability: float = 0.5  # Stability (0.0 to 1.0)
    similarity_boost: float = 0.75  # Similarity (0.0 to 1.0)
    style: float = 0.0  # Style exaggeration (0.0 to 1.0)
    use_speaker_boost: bool = True  # Speaker boost (True/False)
    speed: float = 1.0  # ElevenLabs speed (0.25 to 4.0)
    # Emotion override setting
    use_emotion_override: bool = False  # Whether to override settings based on emotion

# --- Step 1: Detect emotion ---
def detect_emotion(text):
    res = clf(text)[0]   # {'label': 'POSITIVE', 'score': 0.99}
    label = res['label'].upper()
    return label, res['score']

# --- Step 1.5: Add stuttering for sad emotions ---
def add_stuttering_effects(text, emotion, confidence):
    """
    Add stuttering effects to text for negative emotions
    """
    if emotion == "NEGATIVE" and confidence > 0.7:
        import re
        # Words that commonly get stuttered when sad
        stutter_words = ['i', 'can', 'just', 'really', 'feel', 'think', 'know', 'want', 'need', 'sorry']
        
        words = text.split()
        modified_words = []
        
        for word in words:
            word_lower = word.lower().strip('.,!?;:')
            # Add stuttering to emotional words and beginning of sentences
            if (word_lower in stutter_words or 
                len(modified_words) == 0 or  # First word
                modified_words[-1].endswith('.') or modified_words[-1].endswith('!')):
                
                # Create stuttering effect by repeating first syllable
                if len(word_lower) > 2:
                    first_part = word_lower[0]
                    if word_lower[1] in 'aeiou':  # If second letter is vowel, take first letter
                        stutter = f"{first_part}-{first_part}-{word}"
                    else:  # Take first consonant cluster
                        first_part = word_lower[:2]
                        stutter = f"{first_part}-{first_part}-{word}"
                    modified_words.append(stutter)
                else:
                    modified_words.append(word)
            else:
                modified_words.append(word)
        
        return ' '.join(modified_words)
    
    return text

# --- Step 2: Map emotion to TTS settings ---
def map_emotion(emotion, confidence):
    """Map emotion to TTS parameters"""
    
    # Base settings
    settings = {
        'rate': 1.0,    # Speech rate multiplier
        'pitch': 1.0,   # Pitch multiplier  
        'volume': 1.0,  # Volume multiplier
        'stability': 0.5,
        'similarity_boost': 0.75,
        'style': 0.0,
        'use_speaker_boost': True,
        'speed': 1.0    # ElevenLabs speed parameter
    }
    
    if emotion == "POSITIVE":
        # Happy/excited: balanced rate, neutral pitch, louder volume, more stable
        settings.update({
            'rate': 1.0,
            'pitch': 1.0,  # neutral pitch (0 semitones in frontend)
            'volume': 1.1,  # +3dB volume boost
            'stability': 0.7,
            'similarity_boost': 0.5,
            'style': 0.2,
            'speed': 0.9
        })
    elif emotion == "NEGATIVE":
        # Sad/depressed: slower, lower pitch, quieter, with stuttering
        settings.update({
            'rate': 0.8,
            'pitch': 0.9,
            'volume': 0.8,
            'stability': 0.2,  # Lower stability for more emotional variation
            'similarity_boost': 0.6,
            'style': 0.1,
            'speed': 0.8  # Slower speech for sad emotions
        })
    # LABEL_1 (neutral) keeps base settings
    
    return settings

# --- Step 3: Call ElevenLabs API ---
# --- Step 3: ElevenLabs TTS ---
def elevenlabs_tts(text, voice_id="21m00Tcm4TlvDq8ikWAM", voice_settings=None):
    """
    Convert text to speech using ElevenLabs API
    
    Args:
        text (str): Text to convert
        voice_id (str): ElevenLabs voice ID 
        voice_settings (dict): Voice configuration settings
    
    Returns:
        bytes: Audio data in MP3 format
    """
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    # Default voice settings
    default_settings = {
        "stability": 0.5,
        "similarity_boost": 0.75,
        "style": 0.0,
        "use_speaker_boost": True,
        "speed": 1.0
    }
    
    # Merge with provided settings
    if voice_settings:
        default_settings.update(voice_settings)
    
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": default_settings
    }
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVEN_API_KEY
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"ElevenLabs API error: {response.status_code}, {response.text}")

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
    
    # Apply stuttering effects for sad emotions
    processed_text = add_stuttering_effects(text, emotion, conf)
    
    # Get base parameters from user input
    rate = data.rate
    pitch = data.pitch
    volume = data.volume
    voice_settings = {
        "stability": data.stability,
        "similarity_boost": data.similarity_boost,
        "style": data.style,
        "use_speaker_boost": data.use_speaker_boost,
        "speed": data.speed
    }
    
    # Apply emotion-based overrides if enabled and confidence is high
    emotion_overridden = False
    if data.use_emotion_override and conf > 0.7:
        emotion_settings = map_emotion(emotion, conf)
        
        # Override audio processing parameters
        rate = emotion_settings['rate']
        pitch = emotion_settings['pitch']
        volume = emotion_settings['volume']
        
        # Override voice settings
        voice_settings = {
            "stability": emotion_settings['stability'],
            "similarity_boost": emotion_settings['similarity_boost'],
            "style": emotion_settings['style'],
            "use_speaker_boost": emotion_settings['use_speaker_boost'],
            "speed": emotion_settings['speed']
        }
        emotion_overridden = True
    
    # Generate audio using ElevenLabs
    try:
        audio_bytes = elevenlabs_tts(processed_text, voice_settings=voice_settings)
        
        # Convert MP3 to WAV for processing
        audio_segment = AudioSegment.from_mp3(io.BytesIO(audio_bytes))
        base_file = "temp_base.wav"
        audio_segment.export(base_file, format="wav")
        
        # Apply audio modulation
        final_file = modulate_audio(base_file, "final.wav",
                                    rate=rate,
                                    pitch=pitch,
                                    volume=volume)
        
        return {
            "emotion": emotion,
            "confidence": conf,
            "original_text": text,
            "processed_text": processed_text,
            "stuttering_applied": processed_text != text,
            "emotion_overridden": emotion_overridden,
            "applied_params": {
                "rate": rate,
                "pitch": pitch,
                "volume": volume
            },
            "applied_voice_settings": voice_settings,
            "user_params": {
                "rate": data.rate,
                "pitch": data.pitch,
                "volume": data.volume,
                "stability": data.stability,
                "similarity_boost": data.similarity_boost,
                "style": data.style,
                "use_speaker_boost": data.use_speaker_boost,
                "speed": data.speed
            },
            "audio_file": final_file
        }
    except Exception as e:
        return {"error": str(e)}