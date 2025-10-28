"""Brand guardian agent that adapts messaging to a consistent voice."""

from dataclasses import dataclass


@dataclass
class BrandAgent:
    """Apply a fictional brand voice to generated copy."""

    name: str = "Brand"
    voice_attributes: tuple[str, ...] = (
        "optimistic",
        "human",
        "expert",
    )

    def describe_voice(self) -> str:
        """Describe the high-level brand voice attributes."""
        return ", ".join(self.voice_attributes)

    def apply_voice(self, text: str) -> str:
        """Wrap the provided text in the brand language guidelines."""
        return (
            "As an "
            + self.describe_voice()
            + " guide, we say: "
            + text.capitalize()
        )
