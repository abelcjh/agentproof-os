---
name: evidence-reconciliation
description: Extract and reconcile source-linked enterprise case evidence.
assign_when: Worker needs document, ticket, or case evidence normalized before policy review.
version: 0.1.0
---

# Evidence Reconciliation

## Inputs

- case JSON with `documents[]`
- each document should include `id`, `kind`, optional `amount`, `currency`, `confidence`, and `summary`

## Workflow

1. Preserve every source `id` as `source_id`.
2. Extract evidence rows with amount/currency/confidence.
3. Reconcile amounts deterministically.
4. If amounts conflict, return `BLOCK` for side effects and request reviewer clarification.
5. Emit evidence rows into the run trace.

## Evidence artifacts

- `artifacts/runs/latest.json`
- `artifacts/receipts/latest.json`

## Success criteria

- all extracted rows retain source IDs;
- exactly one selected amount before financial execution;
- no external side effect is executed by this Skill.
