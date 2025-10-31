"""Support copilot that summarises and routes internal tickets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class TicketSummary:
    """Condensed overview of a service ticket."""

    ticket_id: str
    synopsis: str
    sentiment: str
    next_action: str


class SupportCopilot:
    """Simulates summarisation and triage of support tickets."""

    def __init__(self) -> None:
        self.topic_keywords: Dict[str, str] = {
            "checkout": "Payments Squad",
            "delivery": "Fulfillment Ops",
            "inventory": "Supply Chain",
            "pricing": "Merchandising Analytics",
        }

    def summarise(self, ticket_id: str, transcript: str) -> TicketSummary:
        """Return an enriched summary with routing hints."""

        sentiment = self._detect_sentiment(transcript)
        owner = self._route_ticket(transcript)
        synopsis = transcript.split(".")[0].strip()
        next_action = (
            f"Escalate to {owner} with sentiment marker '{sentiment}'. "
            "Auto-generate status update for requester."
        )
        return TicketSummary(
            ticket_id=ticket_id,
            synopsis=synopsis,
            sentiment=sentiment,
            next_action=next_action,
        )

    def _detect_sentiment(self, transcript: str) -> str:
        transcript_lower = transcript.lower()
        if any(word in transcript_lower for word in ["angry", "frustrated", "urgent"]):
            return "high negative"
        if any(word in transcript_lower for word in ["thanks", "appreciate", "resolved"]):
            return "positive"
        return "neutral"

    def _route_ticket(self, transcript: str) -> str:
        transcript_lower = transcript.lower()
        for keyword, squad in self.topic_keywords.items():
            if keyword in transcript_lower:
                return squad
        return "Central Support Pod"
