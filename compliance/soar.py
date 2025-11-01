"""Automated SOAR playbook triggers for remediation workflows."""

from __future__ import annotations

from typing import Dict, List


PLAYBOOKS = {
    "containment": ["isolate host", "block indicators", "notify SOC"],
    "eradication": ["patch systems", "rotate credentials"],
    "recovery": ["restore services", "monitor anomalies"],
}


def trigger_playbook(name: str, context: Dict[str, str]) -> Dict[str, object]:
    """Return the ordered remediation steps for the requested playbook."""

    steps = PLAYBOOKS.get(name, [])
    return {"playbook": name, "steps": steps, "context": context}
