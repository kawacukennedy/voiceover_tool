import librosa
import numpy as np
import hashlib

def extract_embedding(audio_path: str) -> list:
    # Load audio
    y, sr = librosa.load(audio_path, sr=16000, mono=True)

    # Preprocess: normalize, trim silence
    y = librosa.util.normalize(y)
    y, _ = librosa.effects.trim(y, top_db=20)

    # Minimum 30 seconds, but for demo, 5 seconds
    min_samples = 16000 * 5
    if len(y) < min_samples:
        raise ValueError("Audio too short. Need at least 5 seconds.")

    # Truncate to 30 seconds
    max_samples = 16000 * 30
    if len(y) > max_samples:
        y = y[:max_samples]

    # Compute MFCC features
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=256, n_fft=1024, hop_length=512)

    # Average over time to get embedding
    embedding = np.mean(mfcc, axis=1).tolist()

    return embedding

def validate_audio_length(audio_path: str) -> bool:
    y, sr = librosa.load(audio_path, sr=16000, mono=True)
    return len(y) >= 16000 * 30  # 30 seconds