import re
from typing import List

# Vocabularies
vocabs = {
    'en-US': {
        "the": 1, "a": 2, "an": 3, "and": 4, "or": 5, "but": 6, "in": 7, "on": 8, "at": 9, "to": 10,
        "for": 11, "of": 12, "with": 13, "by": 14, "is": 15, "are": 16, "was": 17, "were": 18, "be": 19, "been": 20,
        "have": 21, "has": 22, "had": 23, "do": 24, "does": 25, "did": 26, "will": 27, "would": 28, "can": 29, "could": 30,
        "should": 31, "may": 32, "might": 33, "must": 34, "shall": 35, "this": 36, "that": 37, "these": 38, "those": 39,
        "i": 40, "you": 41, "he": 42, "she": 43, "it": 44, "we": 45, "they": 46, "me": 47, "him": 48, "her": 49,
        "us": 50, "them": 51, "my": 52, "your": 53, "his": 54, "its": 55, "our": 56, "their": 57, "what": 58, "who": 59,
        "when": 60, "where": 61, "why": 62, "how": 63, "which": 64, "all": 65, "some": 66, "many": 67, "much": 68, "few": 69,
        "first": 70, "last": 71, "next": 72, "new": 73, "old": 74, "good": 75, "bad": 76, "big": 77, "small": 78, "long": 79,
        "short": 80, "high": 81, "low": 82, "right": 83, "left": 84, "up": 85, "down": 86, "here": 87, "there": 88, "now": 89,
        "then": 90, "before": 91, "after": 92, "yes": 93, "no": 94, "not": 95, "very": 96, "so": 97, "too": 98, "also": 99,
        "only": 100, "just": 101, "even": 102, "still": 103, "never": 104, "always": 105, "often": 106, "sometimes": 107, "usually": 108,
        "really": 109, "well": 110, "better": 111, "best": 112, "more": 113, "most": 114, "less": 115, "least": 116, "than": 117,
        "as": 118, "like": 119, "if": 120, "because": 121, "although": 122, "while": 123, "since": 124, "until": 125, "during": 126,
        "through": 127, "across": 128, "around": 129, "between": 130, "among": 131, "above": 132, "below": 133, "over": 134, "under": 135,
        "into": 136, "out": 137, "from": 138, "about": 139, "against": 140, "without": 141, "within": 142, "toward": 143, "away": 144,
        "back": 145, "forward": 146, "side": 147, "top": 148, "bottom": 149, "front": 150, "end": 151, "middle": 152, "center": 153,
        "outside": 154, "inside": 155, "near": 156, "far": 157, "close": 158, "open": 159, "full": 160, "empty": 161, "hot": 162,
        "cold": 163, "warm": 164, "cool": 165, "fast": 166, "slow": 167, "quick": 168, "easy": 169, "hard": 170, "simple": 171,
        "complex": 172, "important": 173, "necessary": 174, "possible": 175, "impossible": 176, "true": 177, "false": 178, "real": 179,
        "fake": 180, "same": 181, "different": 182, "other": 183, "own": 184, "free": 185, "busy": 186, "ready": 187, "sure": 188,
        "happy": 189, "sad": 190, "angry": 191, "afraid": 192, "excited": 193, "tired": 194, "hungry": 195, "thirsty": 196, "sick": 197,
        "healthy": 198, "young": 199, "old": 200
    },
    'es-ES': {
        "el": 1, "la": 2, "los": 3, "las": 4, "y": 5, "o": 6, "pero": 7, "en": 8, "sobre": 9, "a": 10,
        "para": 11, "de": 12, "con": 13, "por": 14, "es": 15, "son": 16, "era": 17, "eran": 18, "ser": 19, "estar": 20,
        "tener": 21, "tiene": 22, "tuvo": 23, "hacer": 24, "hace": 25, "hizo": 26, "irá": 27, "iría": 28, "puede": 29, "podría": 30,
        "debería": 31, "puede": 32, "podría": 33, "debe": 34, "deberá": 35, "este": 36, "ese": 37, "estos": 38, "esos": 39,
        "yo": 40, "tú": 41, "él": 42, "ella": 43, "ello": 44, "nosotros": 45, "ellos": 46, "me": 47, "lo": 48, "la": 49,
        "nos": 50, "los": 51, "mi": 52, "tu": 53, "su": 54, "nuestro": 55, "vuestro": 56, "sus": 57, "qué": 58, "quién": 59,
        "cuándo": 60, "dónde": 61, "por qué": 62, "cómo": 63, "cuál": 64, "todo": 65, "alguno": 66, "muchos": 67, "mucho": 68, "pocos": 69,
        "primero": 70, "último": 71, "siguiente": 72, "nuevo": 73, "viejo": 74, "bueno": 75, "malo": 76, "grande": 77, "pequeño": 78, "largo": 79,
        "corto": 80, "alto": 81, "bajo": 82, "derecho": 83, "izquierdo": 84, "arriba": 85, "abajo": 86, "aquí": 87, "allí": 88, "ahora": 89,
        "entonces": 90, "antes": 91, "después": 92, "sí": 93, "no": 94, "no": 95, "muy": 96, "así": 97, "también": 98, "solo": 99,
        "solo": 100, "incluso": 101, "aún": 102, "nunca": 103, "siempre": 104, "a menudo": 105, "a veces": 106, "generalmente": 107
    }
}

def get_vocab(locale: str) -> dict:
    return vocabs.get(locale, vocabs['en-US'])

def tokenize(text: str, locale='en-US') -> List[int]:
    vocab = get_vocab(locale)
    tokens = []
    words = re.findall(r'\b\w+\b', text.lower())
    for word in words:
        if locale == 'en-US':
            phonemes = grapheme_to_phoneme(word)
            for p in phonemes:
                tokens.append(vocab.get(p, 0))
        else:
            tokens.append(vocab.get(word, 0))
    return tokens

def grapheme_to_phoneme(word: str) -> List[str]:
    # Basic G2P for English
    phonemes = []
    word = word.lower()
    i = 0
    while i < len(word):
        if word[i:i+2] == 'th':
            phonemes.append('θ')
            i += 2
        elif word[i:i+2] == 'sh':
            phonemes.append('ʃ')
            i += 2
        elif word[i:i+2] == 'ch':
            phonemes.append('tʃ')
            i += 2
        elif word[i] in 'aeiou':
            phonemes.append(word[i])
            i += 1
        else:
            phonemes.append(word[i])
            i += 1
    return phonemes