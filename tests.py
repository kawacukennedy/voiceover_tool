import pytest
from text_normalizer import parse_and_normalize_text
from tokenizer import tokenize
from voice import list_voices, import_voice
import os
import tempfile

def test_parse_and_normalize_text():
    segments = parse_and_normalize_text("Hello world!")
    assert len(segments) == 1
    assert segments[0].text == "Hello world!"

def test_tokenize():
    tokens = tokenize("Hello world", "en-US")
    assert isinstance(tokens, list)

def test_list_voices():
    voices = list_voices()
    assert isinstance(voices, list)

def test_import_voice():
    # Create dummy embedding
    with tempfile.NamedTemporaryFile(suffix='.bin', delete=False) as f:
        f.write(b'\x00' * 1024)  # dummy 256 floats
        temp_path = f.name
    try:
        result = import_voice(temp_path, 'test_voice')
        assert result == True
        voices = list_voices()
        names = [v.name for v in voices]
        assert 'test_voice' in names
    finally:
        os.unlink(temp_path)
        # Clean up
        if os.path.exists('voices/test_voice.bin'):
            os.unlink('voices/test_voice.bin')
        if os.path.exists('voices/test_voice.json'):
            os.unlink('voices/test_voice.json')
        if os.path.exists('voices/test_voice_sample.mp3'):
            os.unlink('voices/test_voice_sample.mp3')

if __name__ == "__main__":
    pytest.main([__file__])