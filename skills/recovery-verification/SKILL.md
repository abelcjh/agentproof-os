---
name: recovery-verification
description: Verify a proposed enterprise-agent outcome against deterministic checks and receipt integrity.
assign_when: Worker must decide whether a multi-agent run can be presented as complete.
version: 0.1.0
---

# Recovery Verification

## Workflow

1. Check required normalized fields.
2. Check minimum typed handoffs were produced.
3. Check evidence rows exist and preserve sources.
4. Check policy proposal exists.
5. Check receipt hash round-trips.
6. Fail closed if evidence is inconsistent or the receipt was modified.

## Commands

```bash
make verify
python -m agentproof.cli verify-receipt --receipt artifacts/receipts/latest.json
```
