import numpy as np
import os
import hashlib
from voice import get_voice_metadata

def load_embedding(voice_name: str) -> list:
    try:
        meta = get_voice_metadata(voice_name)
        path = f"voices/{voice_name}.bin"
        if not os.path.exists(path):
            raise RuntimeError("Embedding file not found")
        embedding = np.fromfile(path, dtype=np.float32).tolist()
        # Check checksum
        if meta.checksum:
            computed = hashlib.sha256(np.array(embedding, dtype=np.float32).tobytes()).hexdigest()
            if computed != meta.checksum:
                raise RuntimeError("Checksum mismatch")
        return embedding
    except Exception as e:
        print(f"Error loading embedding: {e}")
        return [0.5] * 256  # fallback

def morph_embeddings(emb1: list, emb2: list, blend: float) -> list:
    return [e1 * (1 - blend) + e2 * blend for e1, e2 in zip(emb1, emb2)]