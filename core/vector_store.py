"""Simple embedding store to mimic Weaviate/Chroma interactions."""

from __future__ import annotations

import math
from typing import Dict, List, Tuple


def embed(text: str) -> List[float]:
    """Create a deterministic embedding based on character ordinals."""

    base = [float((ord(char) % 32) / 32) for char in text[:32]]
    if len(base) < 32:
        base.extend([0.0] * (32 - len(base)))
    return base


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute cosine similarity for two vectors."""

    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a)) or 1.0
    norm_b = math.sqrt(sum(b * b for b in vec_b)) or 1.0
    return round(dot / (norm_a * norm_b), 3)


class VectorStore:
    """In-memory vector database with similarity search."""

    def __init__(self) -> None:
        self._store: Dict[str, Tuple[List[float], Dict[str, str]]] = {}

    def add(self, key: str, text: str, metadata: Dict[str, str]) -> None:
        """Insert a vector into the store."""

        self._store[key] = (embed(text), metadata)

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, str]]:
        """Perform cosine similarity search across stored vectors."""

        query_vec = embed(query)
        scored = [
            {
                "key": key,
                "score": cosine_similarity(query_vec, vector),
                "metadata": metadata,
            }
            for key, (vector, metadata) in self._store.items()
        ]
        scored.sort(key=lambda item: item["score"], reverse=True)
        return scored[:top_k]
