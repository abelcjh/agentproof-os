from __future__ import annotations

from typing import Any


def verify_state(state: Any) -> dict[str, Any]:
    failures: list[str] = []
    if not state.normalized_case.get("case_id"):
        failures.append("missing case_id")
    if len(state.handoffs) < 3:
        failures.append("expected at least three typed handoffs before verification")
    if not state.evidence:
        failures.append("no evidence extracted")
    if not state.proposal:
        failures.append("no policy proposal")
    if not state.proposal.get("reconciliation", {}).get("consistent"):
        failures.append("evidence amounts are inconsistent")
    verdict = "PASS" if not failures else "BLOCK"
    return {"verdict": verdict, "failures": failures, "checked_handoffs": len(state.handoffs)}
