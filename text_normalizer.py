import re
from typing import List

class TextSegment:
    def __init__(self, text, rate=1.0, pitch=0.0, volume=1.0, break_time=0.0):
        self.text = text
        self.rate = rate
        self.pitch = pitch
        self.volume = volume
        self.break_time = break_time

def parse_and_normalize_text(text: str, locale='en-US', dict_file=None) -> List[TextSegment]:
    # Load dictionary
    dict_map = {}
    if dict_file:
        try:
            with open(dict_file, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        dict_map[parts[0]] = ' '.join(parts[1:])
        except:
            pass

    segments = []
    # Parse <break> and <prosody>
    break_pattern = r'<break\s+time="([^"]+)"/>'
    prosody_pattern = r'<prosody\s+([^>]+)>(.*?)</prosody>'

    while text:
        break_match = re.search(break_pattern, text)
        prosody_match = re.search(prosody_pattern, text)

        if not break_match and not prosody_match:
            if text.strip():
                segments.append(TextSegment(normalize_segment(text, dict_map)))
            break

        # Find earliest match
        matches = [(break_match, 'break'), (prosody_match, 'prosody')]
        matches = [(m, t) for m, t in matches if m]
        if not matches:
            segments.append(TextSegment(normalize_segment(text, dict_map)))
            break

        matches.sort(key=lambda x: x[0].start())
        match, tag = matches[0]

        # Text before
        before = text[:match.start()]
        if before.strip():
            segments.append(TextSegment(normalize_segment(before, dict_map)))

        if tag == 'break':
            time_str = match.group(1)
            try:
                time_val = float(time_str.rstrip('s'))
            except:
                time_val = 1.0
            segments.append(TextSegment('', break_time=time_val))
        else:  # prosody
            attrs = match.group(1)
            content = match.group(2)
            rate = 1.0
            pitch = 0.0
            volume = 1.0
            for attr in attrs.split():
                if attr.startswith('rate='):
                    rate = float(attr.split('=')[1])
                elif attr.startswith('pitch='):
                    pitch = float(attr.split('=')[1])
                elif attr.startswith('volume='):
                    volume = float(attr.split('=')[1])
            segments.append(TextSegment(normalize_segment(content, dict_map), rate, pitch, volume))

        text = text[match.end():]

    if not segments:
        segments.append(TextSegment(normalize_segment(text, dict_map)))

    return segments

def normalize_segment(text: str, dict_map: dict) -> str:
    result = text
    # Apply dict
    for word, repl in dict_map.items():
        result = re.sub(r'\b' + re.escape(word) + r'\b', repl, result)
    # Remove other tags
    result = re.sub(r'<break[^>]*>', ' ', result)
    return result

def normalize_text(text: str, locale='en-US', dict_file=None) -> str:
    segments = parse_and_normalize_text(text, locale, dict_file)
    return ' '.join(seg.text for seg in segments).strip()