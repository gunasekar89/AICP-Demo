"""Base classes and utilities for CrewAI-powered security agents."""

from __future__ import annotations

import json
import random
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

try:  # pragma: no cover - optional CrewAI import
    from crewai import Agent as CrewAgent  # type: ignore
except Exception:  # pragma: no cover - gracefully degrade when CrewAI is unavailable
    class CrewAgent:  # type: ignore
        """Fallback CrewAgent used when the real dependency is not installed."""

        def __init__(self, name: str, goal: str, backstory: str) -> None:
            self.name = name
            self.goal = goal
            self.backstory = backstory

        def __repr__(self) -> str:  # pragma: no cover - representational
            return f"CrewAgent(name={self.name})"


@dataclass
class AgentMessage:
    """Represents an inter-agent JSON serialisable message."""

    sender: str
    recipient: str
    payload: Dict[str, Any]
    timestamp: float = field(default_factory=lambda: time.time())

    def to_json(self) -> str:
        """Return the message as a JSON string."""

        return json.dumps(
            {
                "sender": self.sender,
                "recipient": self.recipient,
                "payload": self.payload,
                "timestamp": self.timestamp,
            }
        )


class AgentFeedback:
    """Simple reinforcement signal container."""

    def __init__(self) -> None:
        self._scores: List[float] = []
        self._lock = threading.Lock()

    def record(self, score: float) -> None:
        """Persist a numeric score for later analysis."""

        with self._lock:
            self._scores.append(score)

    @property
    def trend(self) -> float:
        """Return the rolling mean score used by agents to self-correct."""

        with self._lock:
            if not self._scores:
                return 0.0
            return sum(self._scores[-10:]) / min(len(self._scores), 10)


class SecurityAgent:
    """Abstract helper that wraps CrewAI agents with platform utilities."""

    def __init__(
        self,
        name: str,
        description: str,
        reasoning_hook: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
    ) -> None:
        self.name = name
        self.description = description
        self.reasoning_hook = reasoning_hook
        self._crew_agent = CrewAgent(name=name, goal=description, backstory=description)
        self.feedback = AgentFeedback()

    def _run_reasoning_loop(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a bounded reasoning loop using optional deterministic heuristics."""

        base_context = dict(context)
        base_context["agent"] = self.name
        if self.reasoning_hook:
            return self.reasoning_hook(base_context)

        # Fallback reasoning: simple weighted decision making
        decision_score = random.random() * (1 + self.feedback.trend)
        base_context["decision_score"] = decision_score
        base_context["action"] = (
            "escalate" if decision_score > 0.7 else "investigate" if decision_score > 0.4 else "observe"
        )
        return base_context

    def handle(self, message: AgentMessage) -> AgentMessage:
        """Process an incoming message and produce a reply."""

        result = self._run_reasoning_loop(message.payload)
        self.feedback.record(result.get("decision_score", 0.5))
        return AgentMessage(sender=self.name, recipient=message.sender, payload=result)

    def plan(self, facts: Dict[str, Any]) -> Dict[str, Any]:
        """Entry point used by orchestrators to solicit a plan from the agent."""

        message = AgentMessage(sender="orchestrator", recipient=self.name, payload=facts)
        response = self.handle(message)
        return response.payload


class AgentRegistry:
    """Central registry and message bus for agent-to-agent communication."""

    def __init__(self) -> None:
        self._agents: Dict[str, SecurityAgent] = {}
        self._lock = threading.Lock()

    def register(self, agent: SecurityAgent) -> None:
        """Register a new agent instance on the message bus."""

        with self._lock:
            self._agents[agent.name] = agent

    def get(self, name: str) -> SecurityAgent:
        """Return a registered agent by name."""

        with self._lock:
            if name not in self._agents:
                raise KeyError(f"Agent {name} not registered")
            return self._agents[name]

    def send(self, message: AgentMessage) -> AgentMessage:
        """Route a message to the requested recipient and return the reply."""

        with self._lock:
            agent = self._agents.get(message.recipient)
        if not agent:
            raise KeyError(f"Agent {message.recipient} not registered")
        return agent.handle(message)

    def broadcast(self, sender: str, payload: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Send the payload to every registered agent and collect their responses."""

        results: Dict[str, Dict[str, Any]] = {}
        for name in list(self._agents.keys()):
            if name == sender:
                continue
            reply = self.send(AgentMessage(sender=sender, recipient=name, payload=payload))
            results[name] = reply.payload
        return results
