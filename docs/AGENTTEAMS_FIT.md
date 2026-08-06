# AgentTeams / HiClaw fit

GOAI Agent Infra requires AgentTeams as the collaboration design baseline. AgentProof OS starts with a lightweight local runner, then maps cleanly to AgentTeams resources.

## concept mapping

| AgentTeams / HiClaw concept | AgentProof OS equivalent | Migration note |
|---|---|---|
| `Manager` | `TeamRunner` / ComplianceOps manager | owns decomposition, state, and worker dispatch |
| `Team` | AgentProof compliance team | references independently managed workers via `spec.workerMembers` in v1.2-style manifests |
| `Worker` | Intake/Evidence/Policy/Verifier/Security/Skill workers | each worker can load one or more `SKILL.md` packages |
| `Human` | reviewer / approver | receives approval requests and blocked-action receipts |
| Matrix transparent collaboration | typed `Handoff` list + run trace | later mirrored into Matrix rooms for human-in-the-loop review |
| Higress MCP gateway | `mcp_tools/*.tool.yaml` | later served through Higress HTTP-to-MCP / MCP proxy with credential isolation |
| Nacos Skill/MCP Registry | `skills/` + `mcp_tools.lock.json` | later publish versioned Skills/tools with lifecycle labels |
| AgentLoop observability | `artifacts/runs/*.json`, `observability/traces/*.jsonl` | later export OpenTelemetry/AgentLoop spans |

## current declarative package

See `agentteams/`:

- `manager.yaml`
- `workers.yaml`
- `team.yaml`
- `human.yaml`

These manifests are **design-baseline manifests**, not yet claimed as validated against a live installed AgentTeams CRD. Exact fields must be checked against the installed v1.2 CRDs before final runnable claims.

## demo migration path

1. keep local `make verify` as stable fallback;
2. install AgentTeams / Higress in local or cloud environment;
3. create Worker CRs for Evidence, Policy, Verifier, Security;
4. configure Team with `spec.workerMembers`;
5. expose case-store as MCP via Higress;
6. mirror run trace into AgentLoop / OTel-shaped spans;
7. use Human reviewer room for approval/rollback demo.
