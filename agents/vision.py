"""Vision agent crafts the overarching narrative."""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class VisionAgent:
    """Translate preferences into a concrete product or campaign vision."""

    name: str = "Vision"

    def craft_vision(self, idea: str, preferences: Dict[str, Any]) -> str:
        """Return a vision statement emphasising the target outcome."""
        audience = preferences.get("audience", "customers")
        tone = preferences.get("tone", "encouraging")
        experience = preferences.get("experience", "delightful")
        return (
            f"A {tone} experience that helps {audience} {idea.lower()} while feeling "
            f"effortlessly {experience}."
        )
