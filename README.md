# 🎙️ Empathetic Text-to-Speech System

An advanced AI-powered text-to-speech system that analyzes text emotion and applies vocal parameter modulation for empathetic speech synthesis. The system uses ElevenLabs API for high-quality voice generation and applies real-time audio processing for emotional voice modulation.

![Demo](https://img.shields.io/badge/Demo-Live-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- **🧠 Emotion Detection**: Automatic sentiment analysis of input text using HuggingFace transformers
- **🎵 Vocal Parameter Modulation**: Real-time control of three key speech parameters:
  - **Rate**: Speech speed (0.5x to 2.0x)
  - **Pitch**: Tonal height (-12 to +12 semitones)
  - **Volume**: Audio amplitude (-20dB to +20dB)
- **🎨 Interactive Web Interface**: Beautiful, responsive UI with real-time sliders
- **🚀 FastAPI Backend**: High-performance async API with CORS support
- **🔄 Real-time Processing**: Live audio generation and modulation
- **📱 Responsive Design**: Works on desktop and mobile devices

## 🛠️ Technology Stack

- **Backend**: FastAPI, Python 3.8+
- **AI/ML**: HuggingFace Transformers, PyTorch
- **Audio Processing**: Librosa, SoundFile, Pydub
- **TTS Engine**: ElevenLabs API
- **Frontend**: Vanilla HTML5, CSS3, JavaScript
- **Audio Format**: WAV (high quality)

## 📋 Prerequisites

- Python 3.8 or higher
- **ElevenLabs API key** (Get yours at [ElevenLabs](https://elevenlabs.io/))
- FFmpeg (for audio processing)
- Modern web browser

> **⚠️ IMPORTANT**: This repository contains a placeholder for the ElevenLabs API key. You MUST replace it with your own API key before running the application.

### Get Your ElevenLabs API Key

1. Sign up at [ElevenLabs](https://elevenlabs.io/)
2. Go to your profile settings
3. Generate an API key
4. Copy the API key (starts with `sk_...`)

### Install FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/empathetic-tts.git
cd empathetic-tts
```

### 2. Set Up Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure ElevenLabs API

**⚠️ REQUIRED**: You must set your own ElevenLabs API key before running the application.

**Option 1: Environment Variable (Recommended)**
```bash
# On macOS/Linux:
export ELEVEN_API_KEY="your_elevenlabs_api_key_here"

# On Windows (Command Prompt):
set ELEVEN_API_KEY=your_elevenlabs_api_key_here

# On Windows (PowerShell):
$env:ELEVEN_API_KEY="your_elevenlabs_api_key_here"
```

**Option 2: Create a .env file**
```bash
# Create .env file in project root
echo "ELEVEN_API_KEY=your_elevenlabs_api_key_here" > .env
```

Then install python-dotenv and load it:
```bash
pip install python-dotenv
```

Add to main.py:
```python
from dotenv import load_dotenv
load_dotenv()
```

> **🔒 Security Note**: Never commit your actual API key to version control. The API key in this repository has been replaced with an environment variable for security.

### 5. Verify API Key Setup
```bash
# Test if your API key is set correctly
python -c "import os; print('API Key set:', 'Yes' if os.getenv('ELEVEN_API_KEY') else 'No')"
```

### 6. Run the Application
```bash
uvicorn main:app --reload
```

### 7. Access the Interface
Open your browser and navigate to:
```
http://127.0.0.1:8000/
```

## 🎯 Usage

### Web Interface

1. **Enter Text**: Type or paste your text in the input area
2. **Choose Preset**: Click on emotion presets (Positive, Neutral, Negative) or use custom settings
3. **Adjust Parameters**: Use sliders to fine-tune:
   - **Rate**: Control speech speed
   - **Pitch**: Adjust voice pitch (higher/lower)
   - **Volume**: Set audio volume level
4. **Generate**: Click "Generate Speech" to create audio
5. **Play**: Audio will auto-play when ready

### API Endpoints

#### POST /speak
Generate speech with custom parameters:

```bash
curl -X POST "http://127.0.0.1:8000/speak" \
-H "Content-Type: application/json" \
-d '{
  "text": "Hello, this is a test!",
  "rate": 1.2,
  "pitch": 2,
  "volume": 3
}'
```

**Response:**
```json
{
  "emotion": "POSITIVE",
  "confidence": 0.95,
  "params": {
    "rate": 1.2,
    "pitch": 2,
    "volume": 3
  },
  "audio_file": "final.wav"
}
```

#### GET /audio
Download the generated audio file:
```bash
curl "http://127.0.0.1:8000/audio" -o output.wav
```

## 🎛️ Parameter Reference

### Rate (Speed)
- **Range**: 0.5 - 2.0
- **Default**: 1.0 (normal speed)
- **Examples**:
  - 0.5x: Very slow, deliberate speech
  - 0.8x: Slightly slower, thoughtful
  - 1.2x: Faster, energetic
  - 2.0x: Very fast, excited

### Pitch (Semitones)
- **Range**: -12 to +12 semitones
- **Default**: 0 (original pitch)
- **Examples**:
  - -12: One octave lower (deeper voice)
  - -2: Slightly lower, sad/serious tone
  - +2: Slightly higher, happy/excited tone
  - +12: One octave higher (chipmunk effect)

### Volume (Decibels)
- **Range**: -20dB to +20dB
- **Default**: 0dB (original volume)
- **Examples**:
  - -20dB: Very quiet, whisper-like
  - -3dB: Slightly quieter
  - +3dB: Slightly louder
  - +20dB: Much louder (may cause distortion)

## 🎨 Emotion Presets

| Emotion | Rate | Pitch | Volume | Description |
|---------|------|-------|--------|-------------|
| **Positive** | 1.2x | +2 | +3dB | Happy, energetic, upbeat |
| **Neutral** | 1.0x | 0 | 0dB | Normal, balanced speech |
| **Negative** | 0.85x | -2 | -3dB | Sad, slower, subdued |

## 📁 Project Structure

```
empathetic-tts/
├── main.py              # FastAPI backend application
├── interface.html       # Web interface
├── test_stretch.py      # Audio testing utility
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── final.wav           # Generated audio output
├── neutral.wav         # Base TTS audio (before modulation)
└── stretched.wav       # Test audio file
```

## 🔧 Configuration

### ElevenLabs Settings
The application uses environment variables for security:

```python
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")  # Your API key from environment
ELEVEN_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # Change voice ID if desired
```

**Important**: The original hardcoded API key has been removed from this repository for security reasons. You must provide your own API key via environment variable.

### Available Voices
Visit [ElevenLabs Voice Lab](https://elevenlabs.io/voice-lab) to browse available voices and get voice IDs.

### Model Configuration
The system uses `distilbert-base-uncased-finetuned-sst-2-english` for emotion detection. To use a different model:

```python
clf = pipeline("sentiment-analysis", model="your-preferred-model")
```

## 🐛 Troubleshooting

### Common Issues

1. **"ModuleNotFoundError"**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`

2. **"Audio not playing"**
   - Check if FFmpeg is installed
   - Verify ElevenLabs API key is valid
   - Check browser console for errors

3. **"API connection failed"**
   - **Verify ElevenLabs API key is set correctly**
   - Check `echo $ELEVEN_API_KEY` to verify environment variable
   - Ensure API key starts with `sk_` and is valid
   - Verify server is running on port 8000
   - Check firewall settings
   - Ensure CORS is properly configured

4. **"Audio quality issues"**
   - Adjust volume to avoid clipping
   - Use moderate pitch adjustments (-6 to +6)
   - Check input text length (very long text may timeout)

### Debug Mode
Run with debug logging:
```bash
uvicorn main:app --reload --log-level debug
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [ElevenLabs](https://elevenlabs.io/) for high-quality TTS API
- [HuggingFace](https://huggingface.co/) for transformer models
- [Librosa](https://librosa.org/) for audio processing
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Search existing [GitHub Issues](https://github.com/yourusername/empathetic-tts/issues)
3. Create a new issue with detailed description

---

**Made with ❤️ for the AI community**
