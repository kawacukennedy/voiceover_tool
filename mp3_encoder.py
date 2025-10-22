try:
    from pydub import AudioSegment
    USE_PYDUB = True
except ImportError:
    USE_PYDUB = False
    AudioSegment = None

try:
    import numpy as np
    USE_NUMPY = True
except ImportError:
    USE_NUMPY = False
    np = None

def encode_mp3(pcm: list, output_path: str, bitrate=320, title='', artist='', album=''):
    if not USE_NUMPY or not USE_PYDUB:
        print("NumPy or pydub not available, skipping MP3 encoding")
        return False
    # Convert to pydub
    audio = np.array(pcm, dtype=np.float32)
    audio = (audio * 32767).astype(np.int16)
    seg = AudioSegment(
        audio.tobytes(),
        frame_rate=44100,
        sample_width=2,
        channels=1
    )
    seg.export(output_path, format='mp3', bitrate=f'{bitrate}k', tags={'title': title, 'artist': artist, 'album': album})
    return True