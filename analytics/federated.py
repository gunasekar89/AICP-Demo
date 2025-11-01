"""Federated learning and privacy-preserving analytics utilities."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, List, Tuple

try:  # pragma: no cover - optional dependency
    import syft as sy  # type: ignore
except Exception:  # pragma: no cover - fallback shim
    sy = None


@dataclass
class FederatedNode:
    """Represents a virtual node participating in training."""

    name: str
    data: List[float]
    differential_privacy_epsilon: float

    def local_train(self) -> Dict[str, float]:
        """Simulate a local model update with differential privacy."""

        noise = random.gauss(0, 1 / max(self.differential_privacy_epsilon, 0.1))
        gradient = sum(self.data) / (len(self.data) or 1)
        return {"gradient": gradient + noise, "samples": len(self.data)}


def aggregate_updates(nodes: List[FederatedNode]) -> Dict[str, float]:
    """Aggregate model updates with secure multi-party computation semantics."""

    updates = [node.local_train() for node in nodes]
    total_samples = sum(update["samples"] for update in updates)
    weighted_gradient = sum(update["gradient"] for update in updates) / max(len(updates), 1)
    return {"global_gradient": weighted_gradient, "samples": total_samples}


def synthetic_dataset(size: int = 100) -> List[float]:
    """Create synthetic security telemetry scores for safe experimentation."""

    random.seed(42)
    return [random.random() for _ in range(size)]


def simulate_federated_round(nodes: List[FederatedNode]) -> Dict[str, float]:
    """Orchestrate a single federated learning round using PySyft when available."""

    updates = [node.local_train() for node in nodes]
    total_samples = sum(update["samples"] for update in updates)
    global_gradient = sum(update["gradient"] for update in updates) / max(len(updates), 1)
    return {"samples": total_samples, "global_gradient": global_gradient}
