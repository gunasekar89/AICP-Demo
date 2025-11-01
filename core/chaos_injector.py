"""Chaos engineering simulator to test resilience."""

from __future__ import annotations

import random
from typing import Dict


FAILURES = [
    "kafka_broker_down",
    "agent_timeout",
    "vector_store_latency",
    "policy_engine_backlog",
]


def inject_failure() -> Dict[str, str]:
    """Return a simulated failure event for observability testing."""

    failure = random.choice(FAILURES)
    impact = {
        "kafka_broker_down": "failover",
        "agent_timeout": "retry",
        "vector_store_latency": "scale_out",
        "policy_engine_backlog": "throttle",
    }[failure]
    return {"failure": failure, "mitigation": impact}
