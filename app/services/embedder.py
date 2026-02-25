import hashlib
from typing import List


def embed_text(text: str, size: int) -> List[float]:
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    vector: List[float] = []
    for i in range(size):
        value = digest[i % len(digest)]
        vector.append((value / 255.0) * 2 - 1)
    return vector
