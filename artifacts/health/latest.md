# Demo health and fallback contract

Generated from `artifacts/runs/latest.json` and `artifacts/receipts/latest.json`.
It gives judges the reliability contract before the demo starts: what runs offline, what is blocked, and how to rerun the proof without secrets.

| Demo health signal | Current status | Proof / fallback |
|---|---|---|
| public repo | https://github.com/abelcjh/agentproof-os | open-source inspection path |
| one-command verify | make verify | runs tests, fixture demo, receipt hash check, and generated summaries |
| fixture/demo mode | PASS | CASE-GOAI-001 |
| agent team minimum | PASS | agents=6 |
| typed handoffs | PASS | handoffs=5 |
| deterministic verifier | PASS | failures=0 |
| AI/API dependency | not required | fixture path is deterministic and runs without live model keys |
| external side effects | blocked | refund requires explicit human approval; policy gate requires human approval |
| evidence inputs | PASS | evidence_rows=2 |
| tamper-evident receipt | PASS | efc2ee49361f7c288fafd4cc5cf95ec929328c48a66ccbd858c612c40526da80 |
| fallback path | local replay | use committed synthetic fixture if live AgentTeams/MCP deployment is unavailable |

## honest scope boundary

- Current committed proof is a deterministic local fixture, not a live AgentTeams room or production MCP gateway deployment.
- The fixture intentionally blocks the risky refund side effect because explicit human approval is absent.
- Future live integrations should preserve this contract: deterministic replay first, gateway/policy check before mutation, and a hashable receipt after execution.
