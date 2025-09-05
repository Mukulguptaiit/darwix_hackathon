import librosa
import soundfile as sf
import numpy as np

def modulate_audio(input_file, output_file, rate=1.0, pitch=0.0, volume=0.0):
    """
    Modulate audio with rate (speed), pitch, and volume changes
    """
    y, sr = librosa.load(input_file, sr=None)
    
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
    
    sf.write(output_file, y, sr)
    return output_file

# Test the function
input_wav = "neutral.wav"
output_wav = "stretched.wav"

# Test with rate=1.2 (20% faster), pitch=+2 semitones, volume=+3dB
result = modulate_audio(input_wav, output_wav, rate=1.2, pitch=2.0, volume=3.0)
print(f"Saved modulated audio to {result}")

# Test parameters for different emotions
print("\nExample parameters for different emotions:")
print("POSITIVE: rate=1.2, pitch=+2, volume=+3")
print("NEGATIVE: rate=0.85, pitch=-2, volume=-3")
print("NEUTRAL: rate=1.0, pitch=0, volume=0")