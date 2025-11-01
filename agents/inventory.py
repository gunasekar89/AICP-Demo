"""Inventory intelligence agent for proactive restocking decisions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class StockAlert:
    """Represents an item that risks going out of stock."""

    sku: str
    current_level: int
    forecast_demand: int
    days_until_stockout: float


@dataclass
class SupplierOrder:
    """Represents a recommendation for replenishment."""

    sku: str
    order_quantity: int
    supplier: str
    rationale: str


class SmartInventoryAI:
    """Lightweight forecasting agent with supplier recommendations."""

    def __init__(self) -> None:
        self.lead_times: Dict[str, int] = {"farm_co": 2, "dairy_collective": 3, "artisan_bakery": 1}
        self.daily_velocity: Dict[str, float] = {
            "organic apples": 18.0,
            "oat milk": 12.5,
            "free-range eggs": 22.0,
            "sourdough bread": 15.0,
            "avocado": 30.0,
        }
        self.current_stock: Dict[str, int] = {
            "organic apples": 120,
            "oat milk": 48,
            "free-range eggs": 60,
            "sourdough bread": 40,
            "avocado": 55,
        }

    def forecast_low_stock(self, horizon_days: int = 7) -> List[StockAlert]:
        """Return items projected to run low within the provided horizon."""

        alerts: List[StockAlert] = []
        for sku, velocity in self.daily_velocity.items():
            projected_demand = int(round(velocity * horizon_days))
            current_level = self.current_stock.get(sku, 0)
            days_until_stockout = current_level / velocity if velocity else float("inf")
            if projected_demand >= current_level:
                alerts.append(
                    StockAlert(
                        sku=sku,
                        current_level=current_level,
                        forecast_demand=projected_demand,
                        days_until_stockout=round(days_until_stockout, 1),
                    )
                )
        alerts.sort(key=lambda alert: alert.days_until_stockout)
        return alerts

    def recommend_supplier_orders(self, alerts: List[StockAlert]) -> List[SupplierOrder]:
        """Suggest supplier orders to resolve the low-stock alerts."""

        orders: List[SupplierOrder] = []
        for alert in alerts:
            supplier = self._map_supplier(alert.sku)
            lead_time = self.lead_times.get(supplier, 2)
            buffer = max(int(alert.forecast_demand * 0.2), 10)
            quantity = alert.forecast_demand + buffer
            rationale = (
                f"Lead time {lead_time} days. Adds {buffer} units safety stock to cover "
                f"demand spike and micro-fulfillment routing."
            )
            orders.append(
                SupplierOrder(
                    sku=alert.sku,
                    order_quantity=quantity,
                    supplier=supplier,
                    rationale=rationale,
                )
            )
        return orders

    @staticmethod
    def _map_supplier(sku: str) -> str:
        if sku in {"organic apples", "avocado"}:
            return "farm_co"
        if sku in {"oat milk", "free-range eggs"}:
            return "dairy_collective"
        return "artisan_bakery"
