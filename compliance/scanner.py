"""Continuous compliance scanning routines."""

from __future__ import annotations

from typing import Dict, List

from .policy_engine import PolicyResult, evaluate_policies


def run_continuous_scan(environment: str, assets: List[str]) -> Dict[str, object]:
    """Run a simulated continuous compliance scan and summarise drift."""

    results = evaluate_policies(environment, assets)
    failing = [result for result in results if not result.passed]
    return {
        "environment": environment,
        "total": len(results),
        "failing": len(failing),
        "details": results,
    }
