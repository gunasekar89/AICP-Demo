"""Concrete CrewAI security agents orchestrating the demo platform."""

from __future__ import annotations

import math
import random
from typing import Any, Dict, List

from .base import AgentMessage, AgentRegistry, SecurityAgent


def _threat_reasoning(context: Dict[str, Any]) -> Dict[str, Any]:
    """Heuristic reasoning used by the Threat Hunter."""

    indicators = context.get("indicators", [])
    score = 0.3 + 0.1 * len(indicators)
    score += 0.2 if context.get("anomaly_score", 0) > 0.8 else 0
    decision = "escalate" if score > 0.7 else "hunt"
    context.update({"decision_score": min(score, 1.0), "action": decision})
    context["notes"] = "Deep packet inspection triggered" if decision == "escalate" else "Hunting in background"
    return context


def _forensic_reasoning(context: Dict[str, Any]) -> Dict[str, Any]:
    """Collect data points for forensic analysis."""

    artefacts = [f"artifact_{i}" for i in range(1, 4)]
    context.update(
        {
            "action": "collect",
            "decision_score": 0.85,
            "collected": artefacts,
            "notes": "Memory dump and container snapshot gathered",
        }
    )
    return context


def _policy_reasoning(context: Dict[str, Any]) -> Dict[str, Any]:
    """Perform zero-trust policy verification."""

    non_compliant = [policy for policy, passed in context.get("policy_results", {}).items() if not passed]
    action = "remediate" if non_compliant else "approve"
    context.update({"decision_score": 0.9 if non_compliant else 0.6, "action": action, "non_compliant": non_compliant})
    return context


def _intel_reasoning(context: Dict[str, Any]) -> Dict[str, Any]:
    """Blend threat intel with federated analytics."""

    feeds: List[Dict[str, Any]] = context.get("feeds", [])
    high_risk = [feed for feed in feeds if feed.get("risk", 0) > 0.75]
    context.update(
        {
            "decision_score": 0.5 + 0.1 * len(high_risk),
            "action": "curate",
            "high_risk": high_risk,
            "notes": "TTP correlation complete",
        }
    )
    return context


def _commander_reasoning(context: Dict[str, Any]) -> Dict[str, Any]:
    """Strategic coordination and reinforcement feedback."""

    priority = context.get("priority", "medium")
    base_score = {"low": 0.4, "medium": 0.7, "high": 0.95}.get(priority, 0.6)
    context.update(
        {
            "decision_score": base_score,
            "action": "coordinate" if base_score < 0.9 else "contain",
            "notes": "Playbook triggered" if base_score >= 0.9 else "Monitoring via unified command",
        }
    )
    return context


class ThreatHunterAgent(SecurityAgent):
    """Locate and triage malicious activity across telemetry sources."""

    def __init__(self) -> None:
        super().__init__(
            name="ThreatHunterAgent",
            description="Performs behavioral analytics and hunts anomalous activity",
            reasoning_hook=_threat_reasoning,
        )


class ForensicCollectorAgent(SecurityAgent):
    """Capture evidence artefacts and share with investigation teams."""

    def __init__(self) -> None:
        super().__init__(
            name="ForensicCollectorAgent",
            description="Acquires forensics artefacts from compromised assets",
            reasoning_hook=_forensic_reasoning,
        )


class PolicyValidatorAgent(SecurityAgent):
    """Validate zero-trust posture and compliance drift."""

    def __init__(self) -> None:
        super().__init__(
            name="PolicyValidatorAgent",
            description="Checks policy compliance against zero-trust baselines",
            reasoning_hook=_policy_reasoning,
        )


class ThreatIntelAgent(SecurityAgent):
    """Fuse curated intelligence with internal telemetry."""

    def __init__(self) -> None:
        super().__init__(
            name="ThreatIntelAgent",
            description="Curates intelligence feeds and prioritises relevant TTPs",
            reasoning_hook=_intel_reasoning,
        )


class IncidentCommanderAgent(SecurityAgent):
    """Coordinate response efforts and close the loop with reinforcement."""

    def __init__(self, registry: AgentRegistry) -> None:
        super().__init__(
            name="IncidentCommanderAgent",
            description="Coordinates multi-agent SecOps playbooks",
            reasoning_hook=_commander_reasoning,
        )
        self.registry = registry

    def coordinate(self, incident: Dict[str, Any]) -> Dict[str, Any]:
        """Request situational awareness from all agents and produce an action plan."""

        fanout = self.registry.broadcast(sender=self.name, payload=incident)
        risk = max((payload.get("decision_score", 0.0) for payload in fanout.values()), default=0.0)
        incident_summary = {
            "risk": round(risk, 3),
            "recommendation": "contain" if risk > 0.8 else "investigate",
            "responses": fanout,
        }
        reinforcement = 0.9 if incident_summary["recommendation"] == "contain" else 0.6
        self.feedback.record(reinforcement)
        return incident_summary


def build_agent_registry() -> AgentRegistry:
    """Create and register all agents for use across the platform."""

    registry = AgentRegistry()
    threat_hunter = ThreatHunterAgent()
    forensic = ForensicCollectorAgent()
    policy = PolicyValidatorAgent()
    intel = ThreatIntelAgent()
    commander = IncidentCommanderAgent(registry=registry)

    for agent in (threat_hunter, forensic, policy, intel, commander):
        registry.register(agent)
    return registry
