# Architecture

```text
Case Intake
   │
   ▼
IntakeAgent ──typed handoff──▶ EvidenceAgent ──skill/tool results──▶ PolicyAgent
   │                              │                                  │
   └──────────── trace bus ◀──────┴────────────── trace bus ◀────────┘
                                  │
                                  ▼
VerifierAgent ──deterministic gates──▶ SecurityAuditor ──approval boundary──▶ Receipt
                                  │
                                  ▼
SkillLibrarian ──captures reusable lessons / rollback metadata
```

## agents

| Agent | Responsibility | Output |
|---|---|---|
| IntakeAgent | normalize task, classify domain, find missing fields | `normalized_case`, `missing_fields` |
| EvidenceAgent | call extraction/reconciliation Skills and MCP-style tools | evidence table + source confidence |
| PolicyAgent | apply deterministic policy/risk rules | action proposal + risk tier |
| VerifierAgent | verify required fields, policy consistency, receipt completeness | PASS/BLOCK/NEEDS_REVIEW |
| SecurityAuditor | block unsafe side effects without approval; scan tool plan | audit verdict + reasons |
| SkillLibrarian | package repeated success/failure patterns as reusable Skill metadata | reusable lesson draft |

## AgentTeams mapping

| AgentTeams concept | Local repo equivalent |
|---|---|
| Leader / orchestrator | `TeamRunner` |
| Worker agents | classes in `agentproof/agents.py` |
| task state | `RunState` dataclass |
| context passing | `Handoff` records |
| skill abstraction | YAML contracts in `skills/` |
| tool invocation | adapters in `agentproof/tools.py` + `mcp_tools/` contracts |
| trace / observability | JSON run trace in `artifacts/runs/` |

## safety boundary

No irreversible enterprise action is executed by the model. The model/agent proposes. Deterministic policy and security gates decide `ALLOW`, `NEEDS_REVIEW`, or `BLOCK`. Human approval is required for financial, legal, destructive, or external-send actions.
