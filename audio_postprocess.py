try:
    import numpy as np
    USE_NUMPY = True
except ImportError:
    USE_NUMPY = False
    np = None
from advanced_audio import apply_parametric_eq, apply_dithering

def postprocess_audio(audio: list, eq_preset='neutral', target_lufs=-16.0, dither_bits=16):
    if not USE_NUMPY:
        print("NumPy not available, skipping postprocessing")
        return
    # Normalize
    max_val = max(abs(x) for x in audio) if audio else 1.0
    if max_val > 0:
        audio[:] = [x / max_val for x in audio]

    # Apply effects
    if eq_preset == 'narration':
        apply_parametric_eq(audio, 300.0, 2.0, 1.0)
    elif eq_preset == 'podcast':
        apply_parametric_eq(audio, 5000.0, -1.0, 2.0)

    # Loudness normalization (simple)
    rms = np.sqrt(np.mean(np.array(audio)**2))
    if rms > 0:
        gain = 10**(target_lufs / 20) / (20 * np.log10(rms + 1e-6))
        audio[:] = [x * gain for x in audio]

    # Dithering
    apply_dithering(audio, dither_bits)

    # Limiter
    audio[:] = [max(-1.0, min(1.0, x)) for x in audio]