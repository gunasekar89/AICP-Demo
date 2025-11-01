"""Simplified Flink-style streaming joins and enrichment logic."""

from __future__ import annotations

import itertools
from typing import Dict, Iterable, List, Tuple

from .kafka_pipeline import TopicMessage


def correlate_events(messages: Iterable[TopicMessage]) -> List[Dict[str, object]]:
    """Correlate Kafka messages into enriched incident candidates."""

    grouped: Dict[str, Dict[str, object]] = {}
    for message in messages:
        incident_id = message.value.get("id") or message.value.get("asset") or message.value.get("ttp")
        incident_id = str(incident_id)
        bucket = grouped.setdefault(
            incident_id,
            {
                "id": incident_id,
                "severity": "medium",
                "signals": [],
                "intel": [],
                "policy": [],
            },
        )
        if message.topic == "threat-events":
            bucket["severity"] = message.value.get("severity", bucket["severity"])
            bucket["anomaly_score"] = message.value.get("anomaly_score", 0.5)
            bucket["signals"].append(message.value)
        elif message.topic == "intel-feed":
            bucket["intel"].append(message.value)
        elif message.topic == "policy-audit":
            bucket["policy"].append(message.value)
    return list(grouped.values())


def risk_score(event: Dict[str, object]) -> float:
    """Compute a deterministic risk score used for prioritisation."""

    base = {"low": 0.3, "medium": 0.6, "high": 0.9}.get(event.get("severity", "medium"), 0.5)
    anomaly = float(event.get("anomaly_score", 0.4))
    intel_boost = sum(feed.get("risk", 0.0) for feed in event.get("intel", [])) / 10
    policy_penalty = 0.1 * sum(1 for result in event.get("policy", []) if not result.get("passed", True))
    return round(min(base + anomaly + intel_boost + policy_penalty, 1.0), 3)


def process_stream(messages: Iterable[TopicMessage]) -> List[Dict[str, object]]:
    """Perform streaming joins and augment events with risk scoring."""

    correlated = correlate_events(messages)
    for event in correlated:
        event["risk_score"] = risk_score(event)
    return correlated


def derive_threat_summary(enriched_events: Iterable[Dict[str, object]]) -> Dict[str, float]:
    """Produce aggregated KPI metrics for the dashboard."""

    events = list(enriched_events)
    if not events:
        return {"high": 0, "medium": 0, "low": 0, "average_risk": 0.0}
    severity_counts = {key: 0 for key in ("high", "medium", "low")}
    risk_total = 0.0
    for event in events:
        severity = str(event.get("severity", "medium"))
        if severity not in severity_counts:
            severity_counts[severity] = 0
        severity_counts[severity] += 1
        risk_total += float(event.get("risk_score", 0.0))
    severity_counts["average_risk"] = round(risk_total / len(events), 3)
    return severity_counts
