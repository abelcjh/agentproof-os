# OpenTelemetry / AgentLoop-shaped trace schema

AgentProof OS emits local JSON evidence first and keeps fields compatible with AgentLoop/OpenTelemetry-style spans.

## span categories

- `ENTRY`
- `AGENT`
- `STEP`
- `TOOL`
- `MCP`
- `SKILL`
- `VERIFIER`
- `SECURITY`

## minimum fields

```json
{
  "trace_id": "case-goai-001",
  "span_id": "span-003",
  "parent_span_id": "span-001",
  "span_kind": "MCP",
  "agent.name": "EvidenceAgent",
  "gen_ai.skill.name": "evidence-reconciliation",
  "gen_ai.skill.version": "0.1.0",
  "tool.name": "case-store.read_case",
  "status": "OK",
  "latency_ms": 0,
  "evidence_uri": "artifacts/runs/latest.json"
}
```

## verification rule

A trace is not proof by itself. A judge-visible claim is valid only when backed by a deterministic command, receipt hash, source URL, screenshot, or artifact path.
