from __future__ import annotations

from .models import RunState
from .tools import extract_evidence, reconcile_amounts, policy_check
from .verifier import verify_state
from .security import audit_action
from .runtime_controls import tool_call


class IntakeAgent:
    name = "IntakeAgent"

    def run(self, state: RunState) -> None:
        raw = state.raw_case
        normalized = {
            "case_id": raw.get("case_id", state.case_id),
            "domain": raw.get("domain", "enterprise_risk"),
            "requested_action": raw.get("requested_action", "review"),
            "stakeholder": raw.get("stakeholder", "unknown"),
            "currency": raw.get("currency", "USD"),
        }
        missing = [k for k, v in normalized.items() if v in (None, "unknown")]
        state.normalized_case = normalized | {
            "missing_fields": missing,
            "tool_calls": [tool_call(self.name, "normalize_case")],
        }
        state.record_step(self.name, "normalize_case", state.normalized_case)
        state.handoff(self.name, "EvidenceAgent", "normalized case ready for extraction", state.normalized_case)


class EvidenceAgent:
    name = "EvidenceAgent"

    def run(self, state: RunState) -> None:
        evidence = extract_evidence(state.raw_case)
        state.evidence = evidence
        output = {
            "evidence_count": len(evidence),
            "evidence": evidence,
            "tool_calls": [
                tool_call(
                    self.name,
                    "extract_evidence",
                    status="ACCEPTED_NOT_VERIFIED",
                    reason="tool output accepted before deterministic verifier gate",
                )
            ],
        }
        state.record_step(self.name, "extract_evidence", output)
        state.handoff(self.name, "PolicyAgent", "evidence extracted for deterministic policy check", output)


class PolicyAgent:
    name = "PolicyAgent"

    def run(self, state: RunState) -> None:
        reconciliation = reconcile_amounts(state.evidence)
        policy = policy_check(state.raw_case, reconciliation)
        state.proposal = {
            "reconciliation": reconciliation,
            "policy": policy,
            "tool_calls": [tool_call(self.name, "reconcile_amounts"), tool_call(self.name, "policy_check")],
        }
        state.record_step(self.name, "propose_action", state.proposal)
        state.handoff(self.name, "VerifierAgent", "proposal ready for verification", state.proposal)


class VerifierAgent:
    name = "VerifierAgent"

    def run(self, state: RunState) -> None:
        state.verification = verify_state(state)
        state.verification["tool_calls"] = [tool_call(self.name, "verify_state")]
        state.record_step(self.name, "verify_result", state.verification)
        state.handoff(self.name, "SecurityAuditor", "verified proposal ready for side-effect audit", state.verification)


class SecurityAuditor:
    name = "SecurityAuditor"

    def run(self, state: RunState) -> None:
        state.security = audit_action(state.raw_case, state.proposal)
        state.security["tool_calls"] = [tool_call(self.name, "audit_action")]
        state.record_step(self.name, "audit_side_effects", state.security)
        state.handoff(self.name, "SkillLibrarian", "audit complete; capture reusable lesson", state.security)


class SkillLibrarian:
    name = "SkillLibrarian"

    def run(self, state: RunState) -> None:
        state.reusable_lesson = {
            "skill_candidate": "approval-gated-financial-action",
            "trigger": state.proposal.get("policy", {}).get("requested_action"),
            "reuse_rule": "When financial/legal side effects are proposed without approval, block execution and emit a reviewer receipt.",
            "rollback": "No external side effect executed in fixture mode.",
            "tool_calls": [tool_call(self.name, "capture_lesson")],
        }
        state.record_step(self.name, "capture_lesson", state.reusable_lesson)
