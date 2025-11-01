"""Reinforcement learning inspired firewall tuning simulation."""

from __future__ import annotations

import random
from typing import Dict, List


class FirewallOptimizer:
    """Simple Q-learning style adaptive firewall policy tuner."""

    def __init__(self) -> None:
        self.q_table: Dict[str, float] = {}
        self.learning_rate = 0.2
        self.discount = 0.9

    def step(self, state: str, action: str, reward: float) -> None:
        """Update the Q-value for a given state/action pair."""

        key = f"{state}:{action}"
        current = self.q_table.get(key, 0.0)
        updated = current + self.learning_rate * (reward + self.discount * max(self.q_table.values() or [0]) - current)
        self.q_table[key] = round(updated, 3)

    def recommend(self, state: str) -> str:
        """Return the best known action for the provided state."""

        actions = ["allow", "monitor", "block"]
        scored = {action: self.q_table.get(f"{state}:{action}", 0.0) for action in actions}
        return max(scored, key=scored.get)

    def simulate_episode(self, telemetry: List[float]) -> Dict[str, str]:
        """Run an optimisation episode to update firewall posture."""

        for score in telemetry:
            state = "high" if score > 0.7 else "medium" if score > 0.4 else "low"
            action = random.choice(["allow", "monitor", "block"])
            reward = 1.0 if (state == "high" and action == "block") else 0.1
            self.step(state, action, reward)
        return {"state": state, "recommended": self.recommend(state)}
