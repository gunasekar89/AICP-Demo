"""Lightweight ML analytics for the AI-SecOps demo."""
from __future__ import annotations

from dataclasses import asdict
from typing import Dict, Iterable, List

import numpy as np
from sklearn.ensemble import IsolationForest

try:
    from agents.simulator import ThreatEvent
except ModuleNotFoundError:  # pragma: no cover - fallback when packaged differently
    from ..agents.simulator import ThreatEvent  # type: ignore


class RiskAnalyzer:
    """Compute anomaly scores and risk summaries using simple ML heuristics."""

    def __init__(self) -> None:
        self._model = IsolationForest(
            n_estimators=100,
            contamination=0.15,
            random_state=42,
        )
        self._fitted = False

    @staticmethod
    def _event_to_features(event: ThreatEvent | Dict) -> List[float]:
        data = asdict(event) if isinstance(event, ThreatEvent) else event
        severity = float(data.get("severity", 0))
        signal_count = float(len(data.get("signals", [])))
        syscall_count = float(data.get("details", {}).get("syscall_count", 0))
        privileged_namespace = 1.0 if data.get("namespace") == "kube-system" else 0.0
        category_hash = float(hash(data.get("category", "")) % 100) / 100.0
        return [severity, signal_count, syscall_count, privileged_namespace, category_hash]

    def fit(self, events: Iterable[ThreatEvent | Dict]) -> None:
        matrix = np.array([self._event_to_features(event) for event in events])
        if len(matrix) == 0:
            raise ValueError("Cannot fit analyzer with no events")
        self._model.fit(matrix)
        self._fitted = True

    def score_events(self, events: Iterable[ThreatEvent | Dict]) -> List[float]:
        data_matrix = np.array([self._event_to_features(event) for event in events])
        if not len(data_matrix):
            return []
        if not self._fitted:
            self._model.fit(data_matrix)
            self._fitted = True
        # IsolationForest returns anomaly scores, higher is more normal. Invert.
        raw_scores = self._model.decision_function(data_matrix)
        normalized = (raw_scores.max() - raw_scores) / (raw_scores.max() - raw_scores.min() + 1e-6)
        return normalized.tolist()

    def cluster_risk_summary(self, events: Iterable[ThreatEvent | Dict]) -> Dict[str, Dict[str, float]]:
        by_cluster: Dict[str, List[float]] = {}
        for event, score in zip(events, self.score_events(events)):
            data = asdict(event) if isinstance(event, ThreatEvent) else event
            cluster = data.get("cluster", "unknown")
            by_cluster.setdefault(cluster, []).append(score)

        summary = {}
        for cluster, scores in by_cluster.items():
            arr = np.array(scores)
            summary[cluster] = {
                "avg_risk": float(np.mean(arr) if len(arr) else 0.0),
                "p95_risk": float(np.percentile(arr, 95) if len(arr) else 0.0),
                "event_count": float(len(arr)),
            }
        return summary


def compute_anomaly_scores(events: List[ThreatEvent | Dict]) -> List[float]:
    analyzer = RiskAnalyzer()
    analyzer.fit(events)
    return analyzer.score_events(events)
