"""Entry point for the AICP multi-agent demo."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any

from agents import (
    BrandAgent,
    FulfillmentAgent,
    PlannerAgent,
    PreferenceAgent,
    VisionAgent,
)


@dataclass
class SimulationResult:
    """Container for the artefacts produced by the demo run."""

    preferences: Dict[str, Any]
    vision: str
    brand_voice: str
    plan_bullets: list[str]
    package: str


class MultiAgentSimulation:
    """Coordinate each agent to demonstrate a collaborative workflow."""

    def __init__(self) -> None:
        self.preference_agent = PreferenceAgent()
        self.vision_agent = VisionAgent()
        self.brand_agent = BrandAgent()
        self.planner_agent = PlannerAgent()
        self.fulfillment_agent = FulfillmentAgent()

    def run(self) -> SimulationResult:
        self._rule("Collecting Preferences")
        preferences = self.preference_agent.gather_preferences()
        for key, value in preferences.items():
            print(f"{key.title()}: {value}")

        self._rule("Defining Vision")
        idea = preferences.get("idea", "delight customers")
        vision = self.vision_agent.craft_vision(idea, preferences)
        print(vision)

        self._rule("Setting Brand Voice")
        brand_voice = self.brand_agent.describe_voice()
        print(f"Voice Attributes: {brand_voice}")
        voice_applied = self.brand_agent.apply_voice(
            "Deliver consistent guidance across every touchpoint."
        )
        print(voice_applied)

        self._rule("Planning Execution")
        plan = self.planner_agent.build_plan(vision, preferences, brand_voice)
        plan_bullets = self.planner_agent.to_bullets()
        for bullet in plan_bullets:
            print(bullet)

        self._rule("Packaging Output")
        package = self.fulfillment_agent.compile_package(
            plan_bullets=plan_bullets,
            vision_summary=vision,
            brand_voice=voice_applied,
        )
        print(package)

        return SimulationResult(
            preferences=preferences,
            vision=vision,
            brand_voice=voice_applied,
            plan_bullets=plan_bullets,
            package=package,
        )

    @staticmethod
    def _rule(title: str) -> None:
        """Simple divider similar to the Rich console rule."""
        print("\n" + title)
        print("-" * len(title))


def main() -> None:
    """Execute the demo when called from the command line."""
    simulation = MultiAgentSimulation()
    simulation.run()


if __name__ == "__main__":
    main()
