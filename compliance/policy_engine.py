"""Policy-as-code evaluation using Rego/Checkov style simulation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class PolicyResult:
    """Represents a policy evaluation outcome."""

    policy: str
    passed: bool
    message: str


POLICIES = {
    "NIST-800-53": "ensure MFA enabled",
    "ISO-27001": "ensure encryption enforced",
    "PCI-DSS": "restrict cardholder data",
}


def evaluate_policies(environment: str, assets: List[str]) -> List[PolicyResult]:
    """Simulate running Rego/Checkov rules against infrastructure assets."""

    results: List[PolicyResult] = []
    for policy, requirement in POLICIES.items():
        passed = (hash(environment + policy) + len(assets)) % 2 == 0
        message = f"{policy} {'passed' if passed else 'failed'} for {environment}: {requirement}"
        results.append(PolicyResult(policy=policy, passed=passed, message=message))
    return results
