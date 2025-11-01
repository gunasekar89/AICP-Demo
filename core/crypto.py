"""Hybrid classical + post-quantum cryptography helpers."""

from __future__ import annotations

import base64
import os
from typing import Dict


try:  # pragma: no cover - optional PQC backends
    from pqcrypto.kem.kyber512 import generate_keypair as kyber_keypair  # type: ignore
except Exception:  # pragma: no cover - fallback for environments without pqcrypto
    def kyber_keypair() -> tuple[bytes, bytes]:
        """Return deterministic pseudo keys for Kyber simulation."""

        return os.urandom(32), os.urandom(32)


try:  # pragma: no cover - optional signature backend
    from pqcrypto.sign.dilithium2 import generate_keypair as dilithium_keypair  # type: ignore
except Exception:  # pragma: no cover - fallback for environments without pqcrypto
    def dilithium_keypair() -> tuple[bytes, bytes]:
        """Return deterministic pseudo keys for Dilithium simulation."""

        return os.urandom(32), os.urandom(32)


def generate_hybrid_certificate(subject: str) -> str:
    """Create a pseudo PEM certificate containing PQC artefacts."""

    kyber_public, kyber_secret = kyber_keypair()
    dilithium_public, dilithium_secret = dilithium_keypair()
    body = {
        "subject": subject,
        "kyber_public": base64.b64encode(kyber_public).decode(),
        "dilithium_public": base64.b64encode(dilithium_public).decode(),
    }
    pem = "-----BEGIN HYBRID CERT-----\n"
    pem += base64.b64encode(str(body).encode()).decode()
    pem += "\n-----END HYBRID CERT-----"
    return pem


def decrypt_payload(ciphertext: bytes) -> bytes:
    """Mock decryptor used for demo logging."""

    return ciphertext[::-1]


def encrypt_payload(plaintext: bytes) -> bytes:
    """Mock encryptor using symmetric XOR to simulate post-quantum KEM usage."""

    key = kyber_keypair()[0]
    encrypted = bytes(b ^ key[i % len(key)] for i, b in enumerate(plaintext))
    return encrypted[::-1]


def certificate_metadata(cert_pem: str) -> Dict[str, str]:
    """Extract metadata from the hybrid certificate."""

    content = cert_pem.splitlines()[1]
    decoded = base64.b64decode(content.encode()).decode()
    return {"raw": decoded[:80] + "..."}
