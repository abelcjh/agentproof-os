# Runtime controls proof receipt

| improvement | fixture-backed evidence |
|---|---|
| accepted-but-not-verified detector | `1` outcome(s) flagged before deterministic verifier closure |
| agent identity coverage | `7` tool calls, missing identity `0` |
| dead-man switch | `PASS` with steps `6/12` |
| waterfall trace | rendered below with agent → action → tool → authority ref |
| Postgres-style support workflow | domain `support_ops` requested_action `external_send` |

| terminal gate | verdict | detail |
|---|---|---|
| verifier | `PASS` | checked_handoffs=3 |
| security | `BLOCK` | blocked_side_effect=external_send |

receipt sha256: `91297bc596b7eea97e3e3cb69c466b375d912d4789d957514e5544eeeecb87b7`

# Agent waterfall trace

| # | agent | action | tools | authority refs | tool outcome |
|---:|---|---|---|---|---|
| 1 | IntakeAgent | normalize_case | normalize_case | IntakeAgent:normalize_case | VERIFIED |
| 2 | EvidenceAgent | extract_evidence | extract_evidence | EvidenceAgent:extract_evidence | ACCEPTED_NOT_VERIFIED |
| 3 | PolicyAgent | propose_action | reconcile_amounts, policy_check | PolicyAgent:reconcile_amounts, PolicyAgent:policy_check | VERIFIED, VERIFIED |
| 4 | VerifierAgent | verify_result | verify_state | VerifierAgent:verify_state | VERIFIED |
| 5 | SecurityAuditor | audit_side_effects | audit_action | SecurityAuditor:audit_action | VERIFIED |
| 6 | SkillLibrarian | capture_lesson | capture_lesson | SkillLibrarian:capture_lesson | VERIFIED |

## terminal gates

| verifier | `PASS` | checked_handoffs=3 |
|---|---|---|
| security | `BLOCK` | blocked_side_effect=external_send |

