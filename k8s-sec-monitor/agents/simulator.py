"""Synthetic security agent simulator for Kubernetes clusters."""
from __future__ import annotations

import json
import random
import time
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Dict, Generator, Iterable, List, Optional

CLUSTERS = [
    "prod-east-1",
    "prod-west-2",
    "staging-eu-1",
    "dev-apac-2",
]

NODES = [
    "node-1",
    "node-2",
    "node-3",
    "node-4",
    "node-5",
    "node-6",
    "node-7",
    "node-8",
]

NAMESPACES = [
    "kube-system",
    "default",
    "payments",
    "ml-infra",
    "security",
]

EVENT_TEMPLATES = [
    {
        "event": "crypto-mining process detected",
        "severity": (7, 10),
        "category": "runtime",
        "policy": "crypto-mining",
        "signals": ["ebpf.proc.exec", "cpu.burst"],
    },
    {
        "event": "suspicious syscall anomaly",
        "severity": (6, 9),
        "category": "syscall",
        "policy": "syscall-baseline",
        "signals": ["ebpf.sys.open", "ebpf.sys.execve"],
    },
    {
        "event": "file integrity violation",
        "severity": (5, 8),
        "category": "file-integrity",
        "policy": "fimap",
        "signals": ["fs.watch.modify", "hash.mismatch"],
    },
    {
        "event": "kube-audit: privilege escalation attempt",
        "severity": (8, 10),
        "category": "kube-audit",
        "policy": "rbac-guard",
        "signals": ["audit.bindClusterRole", "audit.createServiceAccount"],
    },
    {
        "event": "network beaconing pattern",
        "severity": (4, 7),
        "category": "network",
        "policy": "egress-anomaly",
        "signals": ["net.conn.freq", "dns.suspicious"],
    },
]

USERS = ["system:serviceaccount:security:agent", "alice", "bob", "sre-bot", "ml-app"]
IP_POOL = [
    "10.1.{}.{}".format(i, j) for i in range(1, 5) for j in range(10, 20)
]


@dataclass
class ThreatEvent:
    """Represents a synthetic threat detection event."""

    id: str
    timestamp: str
    cluster: str
    node: str
    namespace: str
    pod: str
    container: str
    event: str
    severity: int
    category: str
    policy: str
    signals: List[str]
    user: str
    source_ip: str
    dest_ip: str
    details: Dict[str, str]

    def to_json(self) -> str:
        return json.dumps(asdict(self))


def _random_pod(namespace: str) -> str:
    base = random.choice([
        "api-gateway",
        "payments",
        "recommender",
        "threat-detector",
        "feature-store",
    ])
    return f"{base}-{random.randint(1, 9999):04d}-{namespace.replace('-', '')[:4]}"


def _random_container() -> str:
    return random.choice([
        "sidecar-security",
        "python-app",
        "nodejs",
        "golang",
        "inference",
    ])


def generate_event(seed: Optional[int] = None) -> ThreatEvent:
    """Generate a single synthetic threat event."""
    if seed is not None:
        random.seed(seed)

    template = random.choice(EVENT_TEMPLATES)
    cluster = random.choice(CLUSTERS)
    node = random.choice(NODES)
    namespace = random.choice(NAMESPACES)
    severity = random.randint(*template["severity"])

    pod = _random_pod(namespace)
    container = _random_container()

    event = ThreatEvent(
        id=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc).isoformat(),
        cluster=cluster,
        node=node,
        namespace=namespace,
        pod=pod,
        container=container,
        event=template["event"],
        severity=severity,
        category=template["category"],
        policy=template["policy"],
        signals=template["signals"],
        user=random.choice(USERS),
        source_ip=random.choice(IP_POOL),
        dest_ip=random.choice(IP_POOL),
        details={
            "process": random.choice([
                "/usr/bin/python",
                "/usr/bin/kubectl",
                "/usr/local/bin/miner",
                "/bin/bash",
            ]),
            "hash": uuid.uuid4().hex,
            "syscall_count": str(random.randint(50, 5000)),
        },
    )
    return event


def stream_events(interval: float = 1.0, limit: Optional[int] = None) -> Generator[ThreatEvent, None, None]:
    """Yield a continuous stream of events.

    Args:
        interval: Seconds between events.
        limit: Optional limit on number of events yielded.
    """
    count = 0
    while True:
        yield generate_event()
        count += 1
        if limit is not None and count >= limit:
            break
        time.sleep(max(0.0, interval))


def batch_events(batch_size: int = 50) -> List[ThreatEvent]:
    """Return a batch of events useful for initialization."""
    return [generate_event() for _ in range(batch_size)]


def load_events_from_file(path: str) -> List[ThreatEvent]:
    """Load pre-generated events from JSON file."""
    with open(path, "r", encoding="utf-8") as handle:
        raw_events = json.load(handle)
    return [ThreatEvent(**event) for event in raw_events]


def save_events(events: Iterable[ThreatEvent], path: str) -> None:
    """Persist generated events for offline demos."""
    with open(path, "w", encoding="utf-8") as handle:
        json.dump([asdict(e) for e in events], handle, indent=2)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate synthetic Kubernetes threat events")
    parser.add_argument("--count", type=int, default=10, help="Number of events to generate")
    parser.add_argument("--output", type=str, help="Optional output JSON file path")
    args = parser.parse_args()

    events = batch_events(args.count)
    if args.output:
        save_events(events, args.output)
    else:
        for event in events:
            print(event.to_json())
