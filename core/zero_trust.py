"""Zero-trust enforcement simulation with SPIFFE/SPIRE and OpenZiti concepts."""

from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass
from typing import Dict, Tuple

from .crypto import generate_hybrid_certificate


@dataclass
class WorkloadIdentity:
    """Represents a SPIFFE identity document for workloads."""

    spiffe_id: str
    trust_domain: str
    cert_pem: str

    def as_dict(self) -> Dict[str, str]:
        """Return the identity as a dictionary for logging."""

        return {"spiffe_id": self.spiffe_id, "trust_domain": self.trust_domain, "certificate": self.cert_pem[:40] + "..."}


class ZeroTrustGateway:
    """Simulate an OpenZiti-style policy enforcement point."""

    def __init__(self, trust_domain: str = "example.org") -> None:
        self.trust_domain = trust_domain
        self._policies: Dict[str, Tuple[str, str]] = {}

    def register_workload(self, service_name: str) -> WorkloadIdentity:
        """Issue a SPIFFE ID and hybrid certificate for the workload."""

        serial = secrets.token_hex(4)
        spiffe_id = f"spiffe://{self.trust_domain}/{service_name}/{serial}"
        cert = generate_hybrid_certificate(subject=service_name)
        self._policies[service_name] = (spiffe_id, cert)
        return WorkloadIdentity(spiffe_id=spiffe_id, trust_domain=self.trust_domain, cert_pem=cert)

    def authorize(self, caller: str, callee: str) -> bool:
        """Validate service-to-service access using pre-shared enrolment."""

        return caller in self._policies and callee in self._policies

    def sign_request(self, workload: str, payload: str) -> str:
        """Create a deterministic signature proving workload authenticity."""

        if workload not in self._policies:
            raise ValueError(f"Workload {workload} not registered")
        spiffe_id, cert = self._policies[workload]
        digest = hashlib.sha256((spiffe_id + cert + payload).encode()).hexdigest()
        return digest

    def verify_signature(self, workload: str, payload: str, signature: str) -> bool:
        """Verify a signature by recomputing the expected digest."""

        expected = self.sign_request(workload, payload)
        return secrets.compare_digest(expected, signature)
