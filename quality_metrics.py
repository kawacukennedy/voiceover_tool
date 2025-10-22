import math
from typing import NamedTuple

class QualityReport(NamedTuple):
    has_clipping: bool
    snr_db: float
    peak_level: float
    rms_level: float

def analyze_audio_quality(audio: list) -> QualityReport:
    if not audio:
        return QualityReport(False, 0.0, 0.0, 0.0)
    peak = max(abs(x) for x in audio)
    rms = math.sqrt(sum(x**2 for x in audio) / len(audio))
    snr = 20 * math.log10(peak / rms) if rms > 0 else 0
    clipping = peak >= 1.0
    return QualityReport(clipping, snr, peak, rms)