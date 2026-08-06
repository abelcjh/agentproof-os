# AgentProof OS

**Track pick:** GOAI Global Open-source AI Challenge — **Agent Infra**.

AgentProof OS is an open-source control plane for enterprise multi-agent teams that turns every high-risk agent workflow into a **verifiable execution receipt**: task decomposition, role handoffs, skill/tool calls, deterministic verification, security audit, human approval boundary, and tamper-evident evidence hash.

The first demo scenario is an enterprise **compliance / financial-risk evidence loop**: a messy case intake is decomposed across specialist agents, processed through reusable Skills and MCP-style tools, verified against deterministic policy, audited for unsafe actions, and packaged into a reviewer-ready receipt.

## why this fits GOAI Agent Infra

| GOAI requirement | AgentProof OS artifact |
|---|---|
| at least 3 agents with different roles | IntakeAgent, EvidenceAgent, PolicyAgent, VerifierAgent, SecurityAuditor, SkillLibrarian |
| task decomposition + context passing | `agentproof/teams.py` emits typed `Handoff` records and trace JSON |
| reusable Skills | `skills/*.skill.yaml` with schemas, tools, failure handling, versioning |
| tool/MCP integration | `mcp_tools/*.tool.yaml`, `mcp_tools.lock.json` behavior digest, Python adapters; REST/MCP bridge planned |
| AgentTeams design baseline | `agentteams/*.yaml`, `docs/AGENTTEAMS_FIT.md` |
| result verification | `agentproof/verifier.py` deterministic gates and fixture tests |
| execution evidence capture | `artifacts/runs/*.json`, `artifacts/receipts/*.json`, receipt hash chain, OTel-shaped trace sample |
| security auditing | `agentproof/security.py` blocks forbidden side effects / missing approvals |
| open-source value | MIT repo, schemas, demo fixture, one-command verification |

## quick start

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
make verify
```

Run the fixture demo:

```bash
python -m agentproof.cli run --fixture fixtures/cases/vendor_refund_claim.json --out artifacts/runs/latest.json
python -m agentproof.cli receipt --run artifacts/runs/latest.json --out artifacts/receipts/latest.json
python -m agentproof.cli trace-summary --run artifacts/runs/latest.json --out artifacts/runs/latest.md
python -m agentproof.cli receipt-summary --receipt artifacts/receipts/latest.json --out artifacts/receipts/latest.md
python -m agentproof.cli control-summary --run artifacts/runs/latest.json --receipt artifacts/receipts/latest.json --out artifacts/control/latest.md
python -m agentproof.cli health-summary --run artifacts/runs/latest.json --receipt artifacts/receipts/latest.json --out artifacts/health/latest.md
python -m agentproof.cli check-tool-lock
```

## 10-second demo moment

A judge drops in a messy case JSON. The UI/CLI shows a live agent-team trace, a blocked unsafe refund action because approval is missing, a deterministic policy verdict, and a tamper-evident receipt hash.

Current judge-readable proof surfaces:

- `artifacts/runs/latest.md` — AgentTeams-style handoff transcript and worker action ledger.
- `artifacts/receipts/latest.md` — compact receipt proof table with agents, handoffs, evidence, gates, approval boundary, side-effect boundary, and hash.
- `artifacts/control/latest.md` — gateway-style control surface showing task identity, actor boundary, requested action, verifier result, policy decision, approval gate, side-effect state, and rule-clean MCP/observability inspiration mapping.
- `artifacts/health/latest.md` — demo health and fallback contract showing public repo, `make verify`, fixture mode, no-key AI fallback, blocked side effects, receipt hash, and honest non-live scope.

## rule-clean build note

- Repo created for GOAI after Abel's instruction to start public work.
- Generic planning/context and reusable Hermes skills existed before; project-specific code and docs here are new work.
- No private client data is included; all fixtures are synthetic.
