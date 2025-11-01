"""Self-healing workflows for automated containment."""

from __future__ import annotations

from typing import Dict


def evaluate_exploit_detection(risk_score: float) -> Dict[str, str]:
    """Return containment actions when risk threshold exceeded."""

    if risk_score > 0.85:
        return {"status": "triggered", "action": "isolate node", "reason": "Exploit pattern detected"}
    return {"status": "clear", "action": "monitor"}


def predictive_patching(vuln_score: float) -> Dict[str, str]:
    """Automatically patch when vulnerability score is high."""

    if vuln_score > 0.8:
        return {"status": "patched", "window": "immediate", "reason": "High risk vulnerability"}
    return {"status": "scheduled", "window": "next maintenance", "reason": "Within tolerance"}
