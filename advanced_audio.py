import math

def apply_parametric_eq(audio: list, freq: float, gain: float, q: float):
    # Simple placeholder
    pass

def apply_dithering(audio: list, bits: int):
    import random
    for i in range(len(audio)):
        noise = (random.random() - 0.5) / (1 << bits)
        audio[i] += noise