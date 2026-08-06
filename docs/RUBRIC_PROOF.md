# Rubric proof ledger

| Claim | Evidence artifact | Verification command | Status |
|---|---|---|---|
| repo has at least 3 agent roles | `agentproof/agents.py`, `docs/ARCHITECTURE.md` | `make verify` | verified: 6 agents |
| fixture run emits typed handoffs | `artifacts/runs/latest.json` | `python -m agentproof.cli run ...` | verified: 5 handoffs |
| unsafe side effect is blocked without human approval | `fixtures/cases/vendor_refund_claim.json`, receipt audit reasons | `python -m agentproof.cli receipt ...` | verified: refund BLOCK |
| Skills have schemas and failure handling | `skills/*.skill.yaml`, `skills/*/SKILL.md` | `python -m agentproof.cli check-skills` | verified |
| MCP/tool behavior digest detects drift | `mcp_tools.lock.json`, `agentproof/contracts.py` | `python -m agentproof.cli check-tool-lock` | verified: 1 tool contract |
| AgentTeams design baseline exists | `agentteams/*.yaml`, `docs/AGENTTEAMS_FIT.md` | YAML lint + review | packaged; not yet live-CRD validated |
| multi-agent collaboration is judge-readable without raw JSON | `artifacts/runs/latest.md` | `python -m agentproof.cli trace-summary ...` | verified by `make verify` |
| receipt is tamper-evident | `artifacts/receipts/latest.json` | `python -m agentproof.cli verify-receipt ...` | verified: `efc2ee49361f7c288fafd4cc5cf95ec929328c48a66ccbd858c612c40526da80` |
| receipt has a judge-readable proof table | `artifacts/receipts/latest.md` | `python -m agentproof.cli receipt-summary ...` | verified by `make verify` |

## write-ahead rule

Every measured claim must point to a file, command output, source URL, screenshot, or demo recording. Delete unsupported claims before submission.
