from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Literal

Verdict = Literal["ALLOW", "NEEDS_REVIEW", "BLOCK"]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Handoff:
    sender: str
    receiver: str
    summary: str
    payload: dict[str, Any]
    created_at: str = field(default_factory=utc_now)


@dataclass
class AgentStep:
    agent: str
    action: str
    output: dict[str, Any]
    created_at: str = field(default_factory=utc_now)


@dataclass
class RunState:
    case_id: str
    objective: str
    raw_case: dict[str, Any]
    normalized_case: dict[str, Any] = field(default_factory=dict)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    proposal: dict[str, Any] = field(default_factory=dict)
    verification: dict[str, Any] = field(default_factory=dict)
    security: dict[str, Any] = field(default_factory=dict)
    reusable_lesson: dict[str, Any] = field(default_factory=dict)
    handoffs: list[Handoff] = field(default_factory=list)
    steps: list[AgentStep] = field(default_factory=list)

    def record_step(self, agent: str, action: str, output: dict[str, Any]) -> None:
        self.steps.append(AgentStep(agent=agent, action=action, output=output))

    def handoff(self, sender: str, receiver: str, summary: str, payload: dict[str, Any]) -> None:
        self.handoffs.append(Handoff(sender=sender, receiver=receiver, summary=summary, payload=payload))

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
