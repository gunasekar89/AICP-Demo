"""Mock connectors for extended detection and response integrations."""

from __future__ import annotations

from typing import Dict, List


CONNECTOR_SOURCES = {
    "aws_security_hub": "AWS Security Hub",
    "azure_sentinel": "Azure Sentinel",
    "crowdstrike": "CrowdStrike Falcon",
    "okta": "Okta Identity Cloud",
}


def fetch_events(source: str) -> List[Dict[str, str]]:
    """Return mock events for the requested XDR source."""

    label = CONNECTOR_SOURCES.get(source, source)
    return [
        {
            "source": label,
            "status": "synced",
            "message": f"Latest telemetry ingested from {label}",
        }
    ]


def unified_schema(event: Dict[str, str]) -> Dict[str, str]:
    """Project connector events into the unified schema."""

    return {
        "provider": event.get("source", "unknown"),
        "status": event.get("status", "unknown"),
        "detail": event.get("message", ""),
    }
