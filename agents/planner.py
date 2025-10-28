"""Planner agent responsible for coordinating the other capabilities."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class Milestone:
    """Represents a concrete step in the simulated project plan."""

    title: str
    description: str
    owner: str


@dataclass
class PlannerAgent:
    """Simple planner that produces a set of milestones from inputs."""

    name: str = "Planner"
    milestones: List[Milestone] = field(default_factory=list)

    def build_plan(
        self,
        vision_summary: str,
        preferences: Dict[str, Any],
        brand_voice: str,
    ) -> List[Milestone]:
        """Generate a linear plan tailored to the client information."""
        audience = preferences.get("audience", "customers")
        tone = preferences.get("tone", "friendly")
        deliverable = preferences.get("deliverable", "launch plan")

        self.milestones = [
            Milestone(
                title="Discovery",
                description=(
                    f"Validate the vision with {audience} interviews and collect key "
                    f"insights for a {tone} {deliverable}."
                ),
                owner="Vision",
            ),
            Milestone(
                title="Creative Direction",
                description=(
                    "Craft narrative concepts that honour the brand voice while "
                    f"emphasising: {vision_summary}"
                ),
                owner="Brand",
            ),
            Milestone(
                title="Production",
                description=(
                    "Produce campaign assets and messaging, weaving in the "
                    f"{brand_voice} perspective so every touchpoint feels cohesive."
                ),
                owner="Fulfillment",
            ),
        ]
        return self.milestones

    def to_bullets(self) -> List[str]:
        """Return the plan as formatted bullet points."""
        return [
            f"• {milestone.title} — {milestone.description} (Lead: {milestone.owner})"
            for milestone in self.milestones
        ]
