"""Retail assistant agent that curates grocery bundle offers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class ComboOffer:
    """Represents a curated grocery bundle and the associated savings."""

    name: str
    items: Dict[str, int]
    total_price: float
    savings: float
    insights: str


class AgenticRetailAssistant:
    """Simulated assistant that reasons over catalog data to surface combos."""

    def __init__(self) -> None:
        self.weekly_catalog: Dict[str, float] = {
            "organic apples": 3.99,
            "oat milk": 5.49,
            "free-range eggs": 4.79,
            "sourdough bread": 4.25,
            "avocado": 1.69,
            "almond butter": 7.99,
            "quinoa": 6.50,
            "heirloom tomatoes": 4.10,
            "spinach": 2.85,
            "greek yogurt": 6.25,
        }
        self.partner_discounts: Dict[str, float] = {
            "farm_co": 0.10,
            "dairy_collective": 0.08,
            "artisan_bakery": 0.12,
        }
        self.curated_offers: List[ComboOffer] = []

    def find_best_combos(self, audience: str, max_results: int = 3) -> List[ComboOffer]:
        """Return the top grocery bundles for the requested audience."""

        bundles: List[Tuple[str, Dict[str, int]]] = [
            (
                "Brunch Delight",
                {
                    "sourdough bread": 1,
                    "avocado": 4,
                    "free-range eggs": 1,
                    "heirloom tomatoes": 3,
                },
            ),
            (
                "Wellness Glow",
                {
                    "organic apples": 6,
                    "spinach": 2,
                    "quinoa": 1,
                    "greek yogurt": 1,
                },
            ),
            (
                "Plant-Powered Pantry",
                {
                    "oat milk": 2,
                    "almond butter": 1,
                    "quinoa": 2,
                    "organic apples": 4,
                },
            ),
        ]

        premium_multiplier = 1.05 if "premium" in audience.lower() else 1.0
        offers: List[ComboOffer] = []
        for name, items in bundles:
            list_price = sum(self.weekly_catalog[item] * qty for item, qty in items.items())
            partner_discount = self._estimate_discount(name)
            adjusted_price = list_price * (1 - partner_discount)
            if premium_multiplier > 1:
                adjusted_price *= premium_multiplier
            savings = list_price - adjusted_price
            insights = (
                f"Tailored for {audience}. Partner discount: {partner_discount:.0%}. "
                f"Upsell cushion applied: {premium_multiplier:.2f}."
            )
            offers.append(
                ComboOffer(
                    name=name,
                    items=items,
                    total_price=round(adjusted_price, 2),
                    savings=round(savings, 2),
                    insights=insights,
                )
            )

        offers.sort(key=lambda combo: combo.savings, reverse=True)
        self.curated_offers = offers[:max_results]
        return self.curated_offers

    def _estimate_discount(self, bundle_name: str) -> float:
        """Approximate the partner discount based on the bundle composition."""

        if "Brunch" in bundle_name:
            return self.partner_discounts["artisan_bakery"]
        if "Wellness" in bundle_name:
            return self.partner_discounts["farm_co"]
        return self.partner_discounts["dairy_collective"]
