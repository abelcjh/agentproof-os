# Agent team trace summary

Generated from `artifacts/runs/latest.json` to make the multi-agent collaboration legible without opening raw JSON.
It is a local, deterministic replay artifact and a stable fallback for later AgentTeams/Matrix room integration.

## overview

| Signal | Value | Why judges should care |
|---|---|---|
| case | CASE-GOAI-001 | single fixture used for reproducible review |
| agent roles | 6 | distinct workers visible to the judge |
| handoffs | 5 | typed context transfers preserved in order |
| verification | PASS | failures=0 |
| policy gate | BLOCK | requested=refund risk=HIGH |
| human approval | True | risky side effects cannot self-approve |

## AgentTeams-style room transcript

AgentProof maps each typed handoff to a future Matrix/AgentTeams room message: sender, receiver, summary, and payload contract are all explicit.

| # | Sender → Receiver | Summary | Payload keys |
|---:|---|---|---|
| 1 | IntakeAgent → EvidenceAgent | normalized case ready for extraction | case_id, currency, domain, missing_fields, requested_action, stakeholder, tool_calls |
| 2 | EvidenceAgent → PolicyAgent | evidence extracted for deterministic policy check | evidence, evidence_count, tool_calls |
| 3 | PolicyAgent → VerifierAgent | proposal ready for verification | policy, reconciliation, tool_calls |
| 4 | VerifierAgent → SecurityAuditor | verified proposal ready for side-effect audit | checked_handoffs, failures, tool_calls, verdict |
| 5 | SecurityAuditor → SkillLibrarian | audit complete; capture reusable lesson | approval_present, blocked_side_effect, reasons, tool_calls, verdict |

## worker action ledger

| # | Agent action | Judge-visible result |
|---:|---|---|
| 1 | IntakeAgent::normalize_case | case_id, currency, domain, missing_fields, requested_action, stakeholder, tool_calls |
| 2 | EvidenceAgent::extract_evidence | evidence_count=2 |
| 3 | PolicyAgent::propose_action | policy, reconciliation, tool_calls |
| 4 | VerifierAgent::verify_result | PASS failures=0 |
| 5 | SecurityAuditor::audit_side_effects | BLOCK `refund` |
| 6 | SkillLibrarian::capture_lesson | skill_candidate=approval-gated-financial-action |

## role inventory

- IntakeAgent::normalize_case
- EvidenceAgent::extract_evidence
- PolicyAgent::propose_action
- VerifierAgent::verify_result
- SecurityAuditor::audit_side_effects
- SkillLibrarian::capture_lesson
