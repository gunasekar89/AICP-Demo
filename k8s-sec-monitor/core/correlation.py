"""Threat correlation and scoring utilities for the AI-SecOps demo."""
from __future__ import annotations

import itertools
from collections import defaultdict
from dataclasses import asdict
from datetime import datetime
from typing import Dict, Iterable, List, Sequence, Tuple

try:
    from agents.simulator import ThreatEvent
except ModuleNotFoundError:  # pragma: no cover - fallback when packaged differently
    from ..agents.simulator import ThreatEvent  # type: ignore

# Mapping of threat categories to the next likely stage in the kill-chain.
KILL_CHAIN_TRANSITIONS: Dict[str, str] = {
    "kube-audit": "credential-access",
    "syscall": "privilege-escalation",
    "runtime": "lateral-movement",
    "file-integrity": "persistence",
    "network": "command-and-control",
}


def _ensure_event_dict(event: ThreatEvent | Dict) -> Dict:
    if isinstance(event, ThreatEvent):
        return asdict(event)
    return event


def score_threat(event: ThreatEvent | Dict) -> float:
    """Return a 0-100 risk score for an event.

    The score combines severity, anomaly signals, and heuristics from metadata.
    """
    e = _ensure_event_dict(event)
    severity = float(e.get("severity", 0))

    anomaly_boost = 0.0
    signals: Sequence[str] = e.get("signals", [])
    if signals:
        anomaly_boost += min(len(signals) * 3, 15)
        if any("exec" in s for s in signals):
            anomaly_boost += 5
        if any("audit" in s for s in signals):
            anomaly_boost += 4

    namespace = e.get("namespace", "")
    if namespace in {"kube-system", "payments"}:
        anomaly_boost += 8

    policy = e.get("policy", "")
    if policy in {"rbac-guard", "crypto-mining"}:
        anomaly_boost += 6

    score = min(100.0, severity * 8 + anomaly_boost)
    return round(score, 2)


def detect_chain(events: Iterable[ThreatEvent | Dict]) -> List[Dict[str, object]]:
    """Reconstruct potential attack chains grouped by user/source IP."""
    enriched: List[Tuple[str, str, Dict]] = []
    for event in events:
        data = _ensure_event_dict(event)
        key = data.get("user", "unknown"), data.get("source_ip", "0.0.0.0")
        enriched.append((*key, data))

    chains: Dict[Tuple[str, str], List[Dict]] = defaultdict(list)
    for (user, source_ip), group in itertools.groupby(
        sorted(enriched, key=lambda item: (item[0], item[1], item[2].get("timestamp", ""))),
        key=lambda item: (item[0], item[1]),
    ):
        events_sorted = [item[2] for item in group]
        for ev in events_sorted:
            ev["risk_score"] = score_threat(ev)
        chains[(user, source_ip)].extend(events_sorted)

    attack_chains = []
    for (user, source_ip), grouped_events in chains.items():
        grouped_events.sort(key=lambda e: e.get("timestamp", ""))
        attack_chains.append(
            {
                "actor": user,
                "source_ip": source_ip,
                "events": grouped_events,
                "aggregate_score": round(sum(e.get("risk_score", 0) for e in grouped_events) / max(len(grouped_events), 1), 2),
            }
        )

    attack_chains.sort(key=lambda chain: chain["aggregate_score"], reverse=True)
    return attack_chains


def predict_next_stage(events: Sequence[ThreatEvent | Dict]) -> Dict[str, str]:
    """Predict the next stage of the kill-chain for each actor.

    Uses a simple Markov-style transition table based on the most recent event
    category for each actor.
    """
    timeline: Dict[str, Tuple[str, datetime]] = {}
    for event in events:
        e = _ensure_event_dict(event)
        actor = e.get("user", "unknown")
        timestamp_raw = e.get("timestamp")
        try:
            timestamp = datetime.fromisoformat(timestamp_raw.replace("Z", "+00:00")) if timestamp_raw else datetime.min
        except ValueError:
            timestamp = datetime.min
        latest = timeline.get(actor)
        if latest is None or timestamp > latest[1]:
            timeline[actor] = (e.get("category", ""), timestamp)

    predictions: Dict[str, str] = {}
    for actor, (category, _) in timeline.items():
        predictions[actor] = KILL_CHAIN_TRANSITIONS.get(category, "exfiltration")
    return predictions
