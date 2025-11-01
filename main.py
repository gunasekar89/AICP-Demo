"""Entry point for the Walmart-branded agentic commerce demo."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from agents import (
    AgenticRetailAssistant,
    MultiAgentCommercePlanner,
    SmartInventoryAI,
    SupportCopilot,
)


@dataclass
class DemoResult:
    """Container aggregating all artefacts from the demo run."""

    combo_offers: List[Dict[str, Any]]
    stock_alerts: List[Dict[str, Any]]
    supplier_orders: List[Dict[str, Any]]
    ticket_summary: Dict[str, Any]
    strategy_packet: Dict[str, Any]


class AgenticCommerceDemo:
    """Coordinate the new Walmart agent cohort into a cohesive narrative."""

    def __init__(self) -> None:
        self.retail_agent = AgenticRetailAssistant()
        self.inventory_agent = SmartInventoryAI()
        self.support_copilot = SupportCopilot()
        self.commerce_planner = MultiAgentCommercePlanner()

    def run(self) -> DemoResult:
        self._rule("Agentic Retail Assistant — Combo Intelligence")
        combos = self.retail_agent.find_best_combos("Premium Walmart+ households")
        combo_payload = [
            {
                "name": combo.name,
                "total_price": combo.total_price,
                "savings": combo.savings,
                "insights": combo.insights,
            }
            for combo in combos
        ]
        for payload in combo_payload:
            print(f"{payload['name']}: ${payload['total_price']} (savings ${payload['savings']})")
            print(f"  ↳ {payload['insights']}")

        self._rule("Smart Inventory AI — Forecast & Procurement")
        alerts = self.inventory_agent.forecast_low_stock()
        alert_payload = [
            {
                "sku": alert.sku,
                "current_level": alert.current_level,
                "forecast_demand": alert.forecast_demand,
                "days_until_stockout": alert.days_until_stockout,
            }
            for alert in alerts
        ]
        for payload in alert_payload:
            print(
                f"{payload['sku']} — level {payload['current_level']} vs demand {payload['forecast_demand']} "
                f"(stockout in {payload['days_until_stockout']} days)"
            )

        orders = self.inventory_agent.recommend_supplier_orders(alerts)
        order_payload = [
            {
                "sku": order.sku,
                "order_quantity": order.order_quantity,
                "supplier": order.supplier,
                "rationale": order.rationale,
            }
            for order in orders
        ]
        for payload in order_payload:
            print(
                f"Reorder {payload['sku']} x{payload['order_quantity']} via {payload['supplier']}"
            )
            print(f"  ↳ {payload['rationale']}")

        self._rule("Support Copilot — Ticket Summaries")
        transcript = (
            "Customer is frustrated that the fresh grocery delivery window keeps slipping. "
            "Mentions inventory gaps on avocados and expects proactive updates."
        )
        ticket = self.support_copilot.summarise("TCK-48291", transcript)
        ticket_payload = {
            "ticket_id": ticket.ticket_id,
            "synopsis": ticket.synopsis,
            "sentiment": ticket.sentiment,
            "next_action": ticket.next_action,
        }
        print(f"Ticket {ticket_payload['ticket_id']} → {ticket_payload['synopsis']}")
        print(f"  Sentiment: {ticket_payload['sentiment']} | Next: {ticket_payload['next_action']}")

        self._rule("Multi-Agent Commerce Planner — Strategy Synthesis")
        retail_story = [
            f"{item['name']} saves ${item['savings']} for {item['insights']}"
            for item in combo_payload
        ]
        inventory_story = [
            f"{payload['sku']} stockout in {payload['days_until_stockout']}d"
            for payload in alert_payload
        ]
        strategy = self.commerce_planner.compose_strategy(
            retail_story=retail_story,
            inventory_alerts=inventory_story,
            support_focus=ticket_payload["next_action"],
        )
        strategy_payload = {
            "executive_summary": strategy.executive_summary,
            "execution_roadmap": strategy.execution_roadmap,
            "quantum_outlook": strategy.quantum_outlook,
            "memory_updates": strategy.memory_updates,
            "delivery_overview": strategy.delivery_overview,
        }
        print(strategy_payload["executive_summary"])
        print("Roadmap:")
        for bullet in strategy_payload["execution_roadmap"]:
            print(f"  {bullet}")
        print(f"Quantum Outlook: {strategy_payload['quantum_outlook']}")
        for channel, update in strategy_payload["memory_updates"].items():
            print(f"Memory[{channel}]: {update}")
        print("\nFulfillment Delivery Overview")
        print("------------------------------")
        print(strategy_payload["delivery_overview"])

        return DemoResult(
            combo_offers=combo_payload,
            stock_alerts=alert_payload,
            supplier_orders=order_payload,
            ticket_summary=ticket_payload,
            strategy_packet=strategy_payload,
        )

    @staticmethod
    def _rule(title: str) -> None:
        """Simple divider similar to the Rich console rule."""

        print("\n" + title)
        print("-" * len(title))


def main() -> None:
    """Execute the demo when called from the command line."""

    demo = AgenticCommerceDemo()
    demo.run()


if __name__ == "__main__":
    main()
