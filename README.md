# 🎙️ Empathetic Text-to-Speech System with Emotion-Aware Voice Modulation

An advanced AI-powered text-to-speech system that analyzes text emotion and applies dynamic vocal parameter modulation and stuttering effects for empathetic speech synthesis. The system uses ElevenLabs API for high-quality voice generation with emotion-specific voice settings and real-time audio processing.

![Demo](https://img.shields.io/badge/Demo-Live-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green)
![ElevenLabs](https://img.shields.io/badge/ElevenLabs-API-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Key Features

### 🧠 **Intelligent Emotion Detection**
- **HuggingFace Transformers**: Uses DistilBERT for real-time sentiment analysis
- **Three Emotion Categories**: Positive, Negative, Neutral classification
- **Confidence Scoring**: Confidence levels for emotion accuracy
- **Automatic Processing**: Background analysis without user intervention

### 🗣️ **Emotion-Specific Speech Effects**
- **Stuttering for Sad Emotions**: Automatic stuttering effects for negative emotions (>70% confidence)
- **Dynamic Text Preprocessing**: Intelligent word selection for stuttering (emotional words + sentence beginnings)
- **Natural Patterns**: Creates realistic stuttering like "I-I-I feel re-re-really sad"

### 🎵 **Advanced Vocal Parameter Modulation**
- **Rate Control**: Speech speed modulation (0.5x to 2.0x)
- **Pitch Shifting**: Tonal adjustment (-12 to +12 semitones)
- **Volume Control**: Audio amplitude (-20dB to +20dB)
- **Real-time Processing**: Live audio modulation using Librosa

### 🎛️ **ElevenLabs Voice Settings Integration**
- **Stability**: Voice consistency (0.0 to 1.0)
- **Similarity Boost**: Adherence to original voice (0.0 to 1.0)
- **Style Exaggeration**: Voice style control (0.0 to 1.0)
- **Speed Control**: ElevenLabs native speed (0.25x to 4.0x)
- **Speaker Boost**: Enhanced similarity processing

### 🎨 **Interactive Web Interface**
- **Dual Control Sections**: Audio Processing + Voice Settings
- **Emotion Presets**: One-click presets for Positive, Negative, Neutral
- **Real-time Feedback**: Shows original vs processed text
- **Visual Indicators**: Clear display when stuttering is applied
- **Responsive Design**: Works on desktop and mobile

## 🧠 How Emotion Detection Works

### **Background Processing Pipeline:**

1. **Text Input** → User enters text in the interface
2. **Sentiment Analysis** → HuggingFace DistilBERT model analyzes the text:
   ```python
   # Uses: distilbert-base-uncased-finetuned-sst-2-english
   emotion, confidence = detect_emotion(text)
   # Returns: ('NEGATIVE', 0.89) or ('POSITIVE', 0.95)
   ```
3. **Emotion Mapping** → System maps emotion to specific voice settings:
   ```python
   # Automatic voice parameter selection based on emotion
   settings = map_emotion(emotion, confidence)
   ```
4. **Text Preprocessing** → For negative emotions (confidence > 70%):
   ```python
   # Applies stuttering to emotional words
   processed_text = add_stuttering_effects(text, emotion, confidence)
   ```
5. **ElevenLabs API Call** → Sends processed text + emotion-specific voice settings
6. **Audio Processing** → Additional local modulation for rate/pitch/volume

### **Emotion-to-Voice Mapping:**

| Emotion | Stability | Similarity | Style | Speed | Rate | Pitch | Volume | Stuttering |
|---------|-----------|------------|-------|-------|------|-------|--------|------------|
| **Positive** | 0.3 (varied) | 0.8 (high) | 0.2 (stylized) | 1.1x (faster) | 1.2x | +2 | +3dB | None |
| **Negative** | 0.2 (emotional) | 0.6 (lower) | 0.1 (subtle) | 0.8x (slower) | 0.85x | -2 | -3dB | **Applied** |
| **Neutral** | 0.5 (balanced) | 0.75 (standard) | 0.0 (natural) | 1.0x (normal) | 1.0x | 0 | 0dB | None |

## 🛠️ Technology Stack

- **Backend**: FastAPI, Python 3.8+, Uvicorn
- **AI/ML**: HuggingFace Transformers, PyTorch, DistilBERT
- **Audio Processing**: Librosa 0.10.1, SoundFile, Pydub, NumPy
- **TTS Engine**: ElevenLabs API v1
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Audio Formats**: MP3 (ElevenLabs) → WAV (Processing) → WAV (Output)

## 📋 Prerequisites

- **Python 3.8+** (Recommended: 3.11)
- **Conda Environment** (cyberwatchdog or similar)
- **ElevenLabs API Key** ([Get yours here](https://elevenlabs.io/))
- **FFmpeg** (for audio format conversion)
- **Modern Web Browser** (Chrome, Firefox, Safari, Edge)

## 🚀 Quick Start

### 1. **Clone Repository**
```bash
git clone https://github.com/Mukulguptaiit/darwix_hackathon.git
cd darwix_hackathon
```

### 2. **Environment Setup**
```bash
# Using Conda (Recommended)
conda create -n cyberwatchdog python=3.11
conda activate cyberwatchdog

# Install dependencies
pip install -r requirements.txt
```

### 3. **API Key Configuration**
```bash
# Create .env file
echo 'ELEVEN_API_KEY="your_elevenlabs_api_key_here"' > .env

# Or export directly
export ELEVEN_API_KEY="your_elevenlabs_api_key_here"
```

### 4. **Start the Server**
```bash
# Activate environment and start server
conda activate cyberwatchdog
uvicorn main:app --host 127.0.0.1 --port 8000
```

### 5. **Open Interface**
Open `interface.html` in your browser or visit:
```
file:///path/to/darwix_hackathon/interface.html
```

## 📖 Detailed Usage

### **Testing Emotion Detection & Stuttering:**

**Negative Emotion Examples (Will trigger stuttering):**
- *"I feel really sad and I just want to cry"*
- *"I can't handle this anymore, I need help"*
- *"I'm sorry, I think I really messed up"*

**Positive Emotion Examples:**
- *"I'm so excited about this amazing project!"*
- *"What a wonderful day, I feel fantastic!"*
- *"This is absolutely incredible, I love it!"*

**Neutral Examples:**
- *"The weather forecast shows rain tomorrow."*
- *"Please complete the assignment by Friday."*
- *"The meeting is scheduled for 3 PM."*

### **API Endpoints:**

#### **POST /speak**
Generate speech with emotion detection and modulation.

**Request Body:**
```json
{
  "text": "I feel really sad and I just want to cry",
  "rate": 0.8,
  "pitch": -2,
  "volume": -3,
  "stability": 0.2,
  "similarity_boost": 0.6,
  "style": 0.1,
  "speed": 0.8,
  "use_speaker_boost": true
}
```

**Response:**
```json
{
  "emotion": "NEGATIVE",
  "confidence": 0.89,
  "original_text": "I feel really sad and I just want to cry",
  "processed_text": "I-I-I fe-fe-feel re-re-really sa-sa-sad and I-I-I ju-ju-just wa-wa-want to cry",
  "stuttering_applied": true,
  "params": {
    "rate": 0.8,
    "pitch": -2,
    "volume": -3,
    "stability": 0.2,
    "similarity_boost": 0.6,
    "style": 0.1,
    "speed": 0.8,
    "use_speaker_boost": true
  },
  "audio_file": "final.wav"
}
```

#### **GET /audio**
Retrieve generated audio file.

## 🎛️ Interface Controls

### **Audio Processing Section:**
- **Rate Slider**: Controls local speech speed (0.5x - 2.0x)
- **Pitch Slider**: Adjusts pitch in semitones (-12 to +12)
- **Volume Slider**: Modifies volume in decibels (-20dB to +20dB)

### **ElevenLabs Voice Settings:**
- **Stability Slider**: Voice consistency (0.0 - 1.0)
- **Similarity Slider**: Voice adherence (0.0 - 1.0)
- **Style Slider**: Voice exaggeration (0.0 - 1.0)
- **Speed Slider**: ElevenLabs speed (0.25x - 4.0x)
- **Speaker Boost**: Toggle for enhanced similarity

### **Emotion Controls:**
- **🧠 Auto-Apply Emotion Settings**: Toggle to automatically override manual settings based on detected emotion
  - When **enabled**: System applies emotion-specific presets automatically (overrides all sliders)
  - When **disabled**: Uses your manual slider settings regardless of detected emotion
  - Requires >70% confidence for emotion override to activate

### **Emotion Presets:**
- **😊 Positive**: Energetic, faster, higher pitch (Happy & Energetic - Fast, High Pitch)
- **😢 Negative**: Subdued, slower, lower pitch + stuttering (Sad & Emotional - Slow, Low Stability)
- **😐 Neutral**: Balanced, natural settings (Balanced & Natural - Default Settings)

## 🔧 Configuration

### **Environment Variables:**
```bash
ELEVEN_API_KEY=your_elevenlabs_api_key
```

### **Model Configuration:**
The system uses DistilBERT for emotion detection:
- **Model**: `distilbert-base-uncased-finetuned-sst-2-english`
- **Task**: Binary sentiment classification (POSITIVE/NEGATIVE)
- **Device**: Automatically detects MPS (Apple Silicon) or CPU

### **Voice Selection:**
Default ElevenLabs voice: `EXAVITQu4vr4xnSDxMaL`
You can change this in `main.py`:
```python
ELEVEN_VOICE_ID = "your_preferred_voice_id"
```

## 🧪 Advanced Features

### **Stuttering Algorithm:**
```python
def add_stuttering_effects(text, emotion, confidence):
    if emotion == "NEGATIVE" and confidence > 0.7:
        # Target emotional words and sentence beginnings
        stutter_words = ['i', 'can', 'just', 'really', 'feel', 'think', 'know', 'want', 'need', 'sorry']
        
        # Apply stuttering pattern: "word" → "wo-wo-word"
        # Creates natural emotional speech effects
```

### **Emotion Mapping:**
```python
def map_emotion(emotion, confidence):
    # Dynamic parameter selection based on detected emotion
    # Integrates with both ElevenLabs API and local processing
```

### **Audio Pipeline:**
1. **Text** → **Emotion Detection** → **Stuttering** → **ElevenLabs TTS** 
2. **MP3 Audio** → **Format Conversion** → **Librosa Processing** 
3. **Rate/Pitch/Volume Modulation** → **Final WAV Output**

## 🐛 Troubleshooting

### **Common Issues:**

**Server won't start:**
```bash
# Check API key is set
echo $ELEVEN_API_KEY

# Verify conda environment
conda activate cyberwatchdog
which python
```

**Audio not playing:**
- Ensure server is running on port 8000
- Check browser console for CORS errors
- Verify audio file generation in project directory

**Stuttering not working:**
- Test with clearly negative text
- Check emotion detection confidence (needs >70%)
- Verify processed_text in API response

**ElevenLabs API errors:**
- Validate API key format (starts with `sk_`)
- Check API quota and billing
- Ensure internet connectivity

## 📊 Performance

- **Emotion Detection**: ~50ms per request
- **Audio Generation**: 1-3 seconds (depends on text length)
- **Audio Processing**: ~500ms for modulation
- **Total Pipeline**: 2-4 seconds end-to-end

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **ElevenLabs** for high-quality TTS API
- **HuggingFace** for transformer models
- **FastAPI** for the excellent web framework
- **Librosa** for audio processing capabilities

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review API documentation

---

**⚡ Ready to create empathetic AI voices? Start with the Quick Start guide above!**
