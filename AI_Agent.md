# AI Agent Entry Point

You are helping improve AgentProof OS for the GOAI Agent Infra track.

## goal

Make enterprise multi-agent workflows production-verifiable: typed handoffs, reusable Skills, MCP-style tools, deterministic validation, security audit, evidence capture, and open-source docs.

## highest-priority files

- `README.md` — judge-facing summary
- `docs/GOAI_BRIEF.md` — official requirements mapped to build artifacts
- `docs/RUBRIC_PROOF.md` — proof ledger
- `agentproof/teams.py` — agent loop and trace records
- `agentproof/verifier.py` — deterministic gates
- `agentproof/security.py` — approval and side-effect guard
- `skills/*.skill.yaml` — reusable Skill contracts
- `fixtures/cases/*.json` — safe demo inputs

## verify before claiming success

```bash
make verify
```

Do not invent benchmark numbers. Add placeholders to `docs/RUBRIC_PROOF.md` only if backed by a command, artifact, source URL, or screenshot path.
