from typing import List
import re

class LanguageModel:
    def __init__(self, locale, model_path, sample_rate=44100, tokenizer_path=''):
        self.locale = locale
        self.model_path = model_path
        self.sample_rate = sample_rate
        self.tokenizer_path = tokenizer_path

def get_supported_languages() -> List[LanguageModel]:
    return [
        LanguageModel('en-US', 'models/tts.onnx', 44100, 'models/tokenizer_en.json'),
        LanguageModel('es-ES', 'models/tts_es.onnx', 44100, 'models/tokenizer_es.json'),
        LanguageModel('fr-FR', 'models/tts_fr.onnx', 44100, 'models/tokenizer_fr.json')
    ]

def get_model_for_locale(locale: str) -> LanguageModel:
    langs = get_supported_languages()
    for lang in langs:
        if lang.locale == locale:
            return lang
    return LanguageModel('en-US', 'models/tts.onnx', 44100, 'models/tokenizer_en.json')

def detect_language(text: str) -> str:
    # Simple heuristic
    if re.search(r'\b(el|la|los|las|es|son|está)\b', text, re.IGNORECASE):
        return 'es-ES'
    elif re.search(r'\b(le|la|les|et|est|dans)\b', text, re.IGNORECASE):
        return 'fr-FR'
    else:
        return 'en-US'