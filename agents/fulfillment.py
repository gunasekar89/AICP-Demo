"""Fulfillment agent assembles the final delivery package."""

from dataclasses import dataclass
from typing import Iterable


@dataclass
class FulfillmentAgent:
    """Generate a succinct project hand-off summary."""

    name: str = "Fulfillment"

    def compile_package(
        self,
        plan_bullets: Iterable[str],
        vision_summary: str,
        brand_voice: str,
    ) -> str:
        """Return the final delivery overview."""
        plan_section = "\n".join(plan_bullets)
        return (
            "FINAL DELIVERY SUMMARY\n"
            "======================\n"
            f"Vision:\n{vision_summary}\n\n"
            f"Brand Voice:\n{brand_voice}\n\n"
            "Execution Plan:\n"
            f"{plan_section}"
        )
