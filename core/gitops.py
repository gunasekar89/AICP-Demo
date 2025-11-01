"""GitOps simulation utilities for progressive deployment."""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ConfigChange:
    """Represents a GitOps configuration change event."""

    environment: str
    author: str
    summary: str
    timestamp: str


def record_change(environment: str, author: str, summary: str) -> ConfigChange:
    """Create a new configuration change event."""

    return ConfigChange(environment=environment, author=author, summary=summary, timestamp=dt.datetime.utcnow().isoformat())


def progressive_deploy(environments: List[str]) -> Dict[str, str]:
    """Return rollout states for each environment."""

    return {env: ("complete" if idx == 0 else "staging") for idx, env in enumerate(environments)}
