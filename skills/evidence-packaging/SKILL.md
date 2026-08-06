---
name: evidence-packaging
description: Package run traces, policy verdicts, security audit reasons, and receipt hashes into judge/reviewer evidence.
assign_when: Manager needs to prepare a proof bundle for judges, reviewers, or incident postmortems.
version: 0.1.0
---

# Evidence Packaging

## Workflow

1. Gather run trace, receipt, policy file, tool lock, and relevant docs.
2. Include command used to reproduce the artifact.
3. Include blocked/allowed action verdict and reason.
4. Include limitations and fixture/live-data label.
5. Never include secrets, raw credentials, or private client data.

## Evidence artifacts

- `docs/RUBRIC_PROOF.md`
- `artifacts/runs/latest.json`
- `artifacts/receipts/latest.json`
- `mcp_tools.lock.json`
