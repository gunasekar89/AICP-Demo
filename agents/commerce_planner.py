"""Multi-agent commerce planner that stitches insights into an execution roadmap."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from .brand import BrandAgent
from .fulfillment import FulfillmentAgent
from .planner import PlannerAgent
from .preference import PreferenceAgent
from .vision import VisionAgent


@dataclass
class StrategyPacket:
    """Aggregated planning output for downstream teams."""

    executive_summary: str
    execution_roadmap: List[str]
    quantum_outlook: str
    memory_updates: Dict[str, str]
    delivery_overview: str


class MultiAgentCommercePlanner:
    """Coordinator that reasons across retail, inventory, and support signals."""

    def __init__(self) -> None:
        self.planner_agent = PlannerAgent()
        self.brand_agent = BrandAgent()
        self.preference_agent = PreferenceAgent()
        self.vision_agent = VisionAgent()
        self.fulfillment_agent = FulfillmentAgent()

    def compose_strategy(
        self,
        retail_story: List[str],
        inventory_alerts: List[str],
        support_focus: str,
    ) -> StrategyPacket:
        """Create a narrative tying together all agent outputs."""

        preferences = self.preference_agent.gather_preferences()
        preferences.update(
            {
                "audience": preferences.get("audience", "customers"),
                "tone": preferences.get("tone", "assurance-first"),
                "deliverable": "agentic commerce orchestration brief",
            }
        )

        idea_context = (
            "coordinate combo savings, predictive replenishment, and proactive support"
        )
        if retail_story:
            idea_context = (
                "activate "
                + retail_story[0].split(" saves ")[0]
                + " style bundles while "
                + "bridging inventory intelligence and support readiness"
            )
        vision_summary = self.vision_agent.craft_vision(idea_context, preferences)

        brand_voice = self.brand_agent.apply_voice(
            "Every touchpoint should reassure Walmart shoppers that our AI network is "
            "quietly orchestrating deals, availability, and care."
        )

        self.planner_agent.build_plan(vision_summary, preferences, brand_voice)
        roadmap = self.planner_agent.to_bullets()
        delivery_overview = self.fulfillment_agent.compile_package(
            plan_bullets=roadmap,
            vision_summary=vision_summary,
            brand_voice=brand_voice,
        )

        executive_summary = (
            "1. Retail: "
            + " | ".join(retail_story)
            + "\n2. Inventory: "
            + " | ".join(inventory_alerts)
            + f"\n3. Support: {support_focus}"
        )
        quantum_outlook = (
            "Quantum annealing sandbox models supplier and last-mile trade-offs in near real time, "
            "unlocking 18% faster decision cycles and adaptive shopper journeys."
        )
        memory_updates = {
            "shared": "Sync combo uplift metrics to federated reinforcement learner.",
            "support": "Flag recurring pricing signal drift for proactive knowledge updates.",
        }
        return StrategyPacket(
            executive_summary=executive_summary,
            execution_roadmap=roadmap,
            quantum_outlook=quantum_outlook,
            memory_updates=memory_updates,
            delivery_overview=delivery_overview,
        )
