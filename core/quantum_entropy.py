"""Quantum entropy simulator to seed PQC operations."""

from __future__ import annotations

import math
import os
import random
from typing import List


def harvest_entropy(samples: int = 256) -> List[int]:
    """Harvest random noise values to mimic QRNG output."""

    return [random.SystemRandom().randint(0, 255) for _ in range(samples)]


def entropy_strength(entropy_pool: List[int]) -> float:
    """Calculate Shannon entropy of the simulated pool."""

    if not entropy_pool:
        return 0.0
    counts = {}
    for value in entropy_pool:
        counts[value] = counts.get(value, 0) + 1
    total = len(entropy_pool)
    entropy = 0.0
    for count in counts.values():
        p = count / total
        entropy -= p * math.log(p, 2)
    return round(entropy, 3)


def export_seed(entropy_pool: List[int]) -> bytes:
    """Transform the entropy pool into a deterministic seed."""

    return bytes(entropy_pool)
