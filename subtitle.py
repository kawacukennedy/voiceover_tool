from typing import List

class Timestamp:
    def __init__(self, word, start_time, end_time):
        self.word = word
        self.start_time = start_time
        self.end_time = end_time

def generate_timestamps(text: str, audio: list, phoneme_level=False) -> List[Timestamp]:
    import re
    words = re.findall(r'\b\w+\b', text)
    duration = len(audio) / 44100.0
    if not phoneme_level:
        timestamps = []
        word_duration = duration / len(words) if words else 0
        current_time = 0.0
        for word in words:
            timestamps.append(Timestamp(word, current_time, current_time + word_duration))
            current_time += word_duration
        return timestamps
    else:
        # Phoneme level
        all_phonemes = []
        for word in words:
            all_phonemes.extend(split_into_phonemes(word))
        phoneme_duration = duration / len(all_phonemes) if all_phonemes else 0
        timestamps = []
        current_time = 0.0
        for p in all_phonemes:
            timestamps.append(Timestamp(p, current_time, current_time + phoneme_duration))
            current_time += phoneme_duration
        return timestamps

def split_into_phonemes(word: str) -> List[str]:
    phonemes = []
    lower = word.lower()
    current = ''
    for c in lower:
        if c in 'aeiou':
            if current:
                phonemes.append(current)
                current = ''
            phonemes.append(c)
        else:
            current += c
    if current:
        phonemes.append(current)
    return phonemes

def export_srt(timestamps: List[Timestamp], output_path: str):
    with open(output_path, 'w') as f:
        for i, ts in enumerate(timestamps, 1):
            f.write(f"{i}\n")
            f.write(f"{ts.start_time:.3f} --> {ts.end_time:.3f}\n")
            f.write(f"{ts.word}\n\n")

def export_vtt(timestamps: List[Timestamp], output_path: str):
    with open(output_path, 'w') as f:
        f.write("WEBVTT\n\n")
        for ts in timestamps:
            f.write(f"{ts.start_time:.3f} --> {ts.end_time:.3f}\n")
            f.write(f"{ts.word}\n\n")

def export_chapters(timestamps: List[Timestamp], output_path: str, chapter_length_sec=300):
    with open(output_path, 'w') as f:
        f.write(";FFMETADATA1\n")
        current_time = 0.0
        chapter_num = 1
        end_time = timestamps[-1].end_time if timestamps else 0
        while current_time < end_time:
            chap_end = min(current_time + chapter_length_sec, end_time)
            f.write(f"[CHAPTER]\nTIMEBASE=1/1000\nSTART={int(current_time*1000)}\nEND={int(chap_end*1000)}\ntitle=Chapter {chapter_num}\n\n")
            current_time = chap_end
            chapter_num += 1

def align_timestamps(original: List[Timestamp], new_audio: list) -> List[Timestamp]:
    orig_duration = original[-1].end_time if original else 0
    new_duration = len(new_audio) / 44100.0
    ratio = new_duration / orig_duration if orig_duration > 0 else 1
    aligned = []
    for ts in original:
        aligned.append(Timestamp(ts.word, ts.start_time * ratio, ts.end_time * ratio))
    return aligned