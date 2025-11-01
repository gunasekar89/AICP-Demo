"""Mock Kafka pipeline utilities powering the streaming SecOps demo."""

from __future__ import annotations

import json
import queue
import random
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class TopicMessage:
    """Represents an event transported on the simulated Kafka bus."""

    topic: str
    value: Dict[str, Any]
    timestamp: float = field(default_factory=lambda: time.time())

    def to_json(self) -> str:
        """Return the message payload as JSON for downstream processors."""

        return json.dumps({"topic": self.topic, "value": self.value, "timestamp": self.timestamp})


class MockKafkaTopic:
    """In-memory Kafka topic simulation with bounded retention."""

    def __init__(self, name: str, maxsize: int = 1000) -> None:
        self.name = name
        self._queue: "queue.Queue[TopicMessage]" = queue.Queue(maxsize=maxsize)

    def publish(self, value: Dict[str, Any]) -> None:
        """Publish a JSON-serialisable message to the topic."""

        message = TopicMessage(topic=self.name, value=value)
        try:
            self._queue.put_nowait(message)
        except queue.Full:  # pragma: no cover - defensive path
            _ = self._queue.get_nowait()
            self._queue.put_nowait(message)

    def consume(self) -> Iterable[TopicMessage]:
        """Yield messages until the queue is empty."""

        while not self._queue.empty():
            yield self._queue.get()


class KafkaPipeline:
    """Convenience wrapper hosting multiple topics for the demo."""

    def __init__(self) -> None:
        self.topics = {
            "threat-events": MockKafkaTopic("threat-events"),
            "policy-audit": MockKafkaTopic("policy-audit"),
            "intel-feed": MockKafkaTopic("intel-feed"),
        }
        self._lock = threading.Lock()

    def publish(self, topic: str, value: Dict[str, Any]) -> None:
        """Publish an event to the requested topic."""

        with self._lock:
            if topic not in self.topics:
                self.topics[topic] = MockKafkaTopic(topic)
            self.topics[topic].publish(value)

    def drain(self) -> List[TopicMessage]:
        """Drain all topic queues and return their messages."""

        events: List[TopicMessage] = []
        with self._lock:
            for topic in self.topics.values():
                events.extend(list(topic.consume()))
        return events


def simulate_threat_event(seed: Optional[int] = None) -> Dict[str, Any]:
    """Generate a synthetic threat event used by the streaming demo."""

    random.seed(seed or time.time())
    severities = ["low", "medium", "high"]
    severity = random.choice(severities)
    return {
        "id": f"evt-{int(time.time()*1000)}",
        "severity": severity,
        "anomaly_score": round(random.random(), 3),
        "source": random.choice(["endpoint", "k8s", "cloud", "identity"]),
        "description": random.choice(
            [
                "Multiple failed logins",
                "Container escape attempt",
                "Suspicious network beacon",
                "Privilege escalation",
            ]
        ),
    }


def bootstrap_pipeline(pipeline: KafkaPipeline, sample_size: int = 10) -> None:
    """Populate the pipeline with deterministic data for the dashboard."""

    for _ in range(sample_size):
        pipeline.publish("threat-events", simulate_threat_event())
        pipeline.publish(
            "policy-audit",
            {
                "policy": random.choice(["NIST-800-53", "ZeroTrust-Core", "PCI-DSS"]),
                "passed": random.choice([True, False]),
                "asset": random.choice(["prod-cluster", "gov-edge", "dev-lab"]),
            },
        )
        pipeline.publish(
            "intel-feed",
            {
                "source": random.choice(["CrowdStrike", "Mandiant", "Internal"],),
                "risk": round(random.random(), 2),
                "ttp": random.choice(["T1059", "T1204", "T1486"]),
            },
        )
