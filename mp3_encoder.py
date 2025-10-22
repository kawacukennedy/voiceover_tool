from pydub import AudioSegment
import numpy as np

def encode_mp3(pcm: list, output_path: str, bitrate=320, title='', artist='', album=''):
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