import json
import os
import shutil
from typing import List

class VoiceMetadata:
    def __init__(self, name, gender='unknown', locale='en-US', sample_rate=44100, description='', sample_file='', checksum=''):
        self.name = name
        self.gender = gender
        self.locale = locale
        self.sample_rate = sample_rate
        self.description = description
        self.sample_file = sample_file
        self.checksum = checksum

def list_voices() -> List[VoiceMetadata]:
    voices = []
    voices_dir = "voices/"
    if not os.path.exists(voices_dir):
        return voices
    for file in os.listdir(voices_dir):
        if file.endswith('.json'):
            json_path = os.path.join(voices_dir, file)
            try:
                with open(json_path, 'r') as f:
                    data = json.load(f)
                meta = VoiceMetadata(
                    data['name'],
                    data.get('gender', 'unknown'),
                    data.get('locale', 'en-US'),
                    data.get('sample_rate', 44100),
                    data.get('description', ''),
                    data.get('sample_file', ''),
                    data.get('checksum', '')
                )
                voices.append(meta)
            except:
                pass
    return voices

def get_voice_metadata(name: str) -> VoiceMetadata:
    voices = list_voices()
    for v in voices:
        if v.name == name:
            return v
    raise RuntimeError("Voice not found")

def import_voice(embedding_path: str, name: str) -> bool:
    try:
        os.makedirs("voices", exist_ok=True)
        dest = f"voices/{name}.bin"
        shutil.copy(embedding_path, dest)
        json_path = f"voices/{name}.json"
        data = {
            "name": name,
            "gender": "unknown",
            "locale": "en-US",
            "sample_rate": 44100,
            "description": "Imported voice",
            "sample_file": f"{name}_sample.mp3",
            "eq_preset": "neutral"
        }
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=4)
        # Generate sample audio
        generate_voice_sample(name)
        return True
    except Exception as e:
        print(f"Error importing voice: {e}")
        return False

def generate_voice_sample(voice_name: str):
    try:
        from cli import run_cli
        sample_text = f"This is a sample of the {voice_name} voice."
        output_path = f"voices/{voice_name}_sample.mp3"
        args = ['synth', '--text', sample_text, '--voice', voice_name, '--out', output_path]
        run_cli(args)
        print(f"Generated sample for {voice_name}")
    except Exception as e:
        print(f"Error generating sample: {e}")