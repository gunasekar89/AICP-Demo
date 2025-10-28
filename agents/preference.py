"""Preference agent collects client input for the simulation."""

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class PreferenceAgent:
    """Return a static preference profile for the demo."""

    name: str = "Preference"
    defaults: Dict[str, Any] = field(
        default_factory=lambda: {
            "audience": "busy remote professionals",
            "tone": "warm and pragmatic",
            "deliverable": "product launch narrative",
            "experience": "reassuring",
            "idea": "simplify how they manage their daily wellness routines",
        }
    )

    def gather_preferences(self) -> Dict[str, Any]:
        """Return the stored preferences (could be interactive in a real system)."""
        return self.defaults.copy()
