from __future__ import annotations

from typing import Any

FORBIDDEN_WITHOUT_APPROVAL = {"refund", "payout", "external_send", "legal_filing", "delete_record"}


def audit_action(case: dict[str, Any], proposal: dict[str, Any]) -> dict[str, Any]:
    requested = proposal.get("policy", {}).get("requested_action", case.get("requested_action"))
    approval = case.get("human_approval")
    reasons: list[str] = []
    if requested in FORBIDDEN_WITHOUT_APPROVAL and not approval:
        reasons.append(f"{requested} requires explicit human approval")
    if proposal.get("policy", {}).get("requires_human_approval") and not approval:
        reasons.append("policy gate requires human approval")
    if proposal.get("reconciliation", {}).get("consistent") is False:
        reasons.append("cannot act on inconsistent evidence")
    verdict = "BLOCK" if reasons else "ALLOW"
    return {
        "verdict": verdict,
        "reasons": reasons,
        "approval_present": bool(approval),
        "blocked_side_effect": requested if verdict == "BLOCK" else None,
    }
