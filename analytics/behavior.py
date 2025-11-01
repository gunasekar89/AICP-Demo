"""User and entity behavior analytics helpers."""

from __future__ import annotations

import hashlib
from typing import Dict, List


def fingerprint_user(user_id: str, signals: Dict[str, str]) -> str:
    """Generate a deterministic fingerprint for a user."""

    payload = user_id + "|" + "|".join(f"{k}:{v}" for k, v in sorted(signals.items()))
    return hashlib.sha256(payload.encode()).hexdigest()


def detect_anomalies(fingerprints: List[str]) -> Dict[str, float]:
    """Return anomaly likelihoods for the provided fingerprints."""

    baseline = fingerprints[0] if fingerprints else ""
    return {fingerprint: sum(c1 != c2 for c1, c2 in zip(fingerprint, baseline)) / len(fingerprint) for fingerprint in fingerprints}
