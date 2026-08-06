from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .agents import IntakeAgent, EvidenceAgent, PolicyAgent, VerifierAgent, SecurityAuditor, SkillLibrarian
from .models import RunState


class TeamRunner:
    def __init__(self) -> None:
        self.agents = [IntakeAgent(), EvidenceAgent(), PolicyAgent(), VerifierAgent(), SecurityAuditor(), SkillLibrarian()]

    def run_case(self, case: dict[str, Any]) -> RunState:
        state = RunState(case_id=case.get("case_id", "unknown"), objective=case.get("objective", "enterprise task"), raw_case=case)
        for agent in self.agents:
            agent.run(state)
        return state


def run_fixture(fixture: Path, out: Path) -> dict[str, Any]:
    case = json.loads(fixture.read_text())
    state = TeamRunner().run_case(case)
    data = state.to_dict()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2, sort_keys=True))
    return data
