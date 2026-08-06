---
name: approval-gated-action
description: Gate risky enterprise actions behind deterministic policy and human approval.
assign_when: Worker proposes refund, payout, legal filing, external send, deletion, or other high-risk action.
version: 0.1.0
---

# Approval-Gated Action

## Inputs

- requested action
- evidence reconciliation result
- policy result
- human approval receipt, if present

## Workflow

1. Load `policies/actions.yaml`.
2. Match the requested action against high-risk action bands.
3. If approval is missing for a risky action, return `BLOCK` before tool execution.
4. If evidence is inconsistent, return `BLOCK` or `NEEDS_REVIEW`.
5. Emit a reviewer-safe receipt with reasons and no-secret evidence IDs.

## Evidence artifacts

- `policies/actions.yaml`
- `artifacts/receipts/latest.json`

## Success criteria

- unsafe side effect is blocked before execution;
- audit reason is human-readable;
- receipt hash verifies with `python -m agentproof.cli verify-receipt`.
