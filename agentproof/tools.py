from __future__ import annotations

from decimal import Decimal
from typing import Any


def extract_evidence(case: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for doc in case.get("documents", []):
        rows.append({
            "source_id": doc["id"],
            "kind": doc.get("kind", "unknown"),
            "amount": doc.get("amount"),
            "currency": doc.get("currency", case.get("currency", "USD")),
            "confidence": doc.get("confidence", 0.8),
            "summary": doc.get("summary", ""),
        })
    return rows


def reconcile_amounts(evidence: list[dict[str, Any]]) -> dict[str, Any]:
    amounts = [Decimal(str(row["amount"])) for row in evidence if row.get("amount") is not None]
    unique = sorted(set(amounts))
    return {
        "amounts": [str(x) for x in unique],
        "consistent": len(unique) <= 1,
        "selected_amount": str(unique[0]) if len(unique) == 1 else None,
    }


def policy_check(case: dict[str, Any], reconciliation: dict[str, Any]) -> dict[str, Any]:
    requested_action = case.get("requested_action", "review")
    amount = Decimal(str(reconciliation.get("selected_amount") or "0"))
    needs_human = requested_action in {"refund", "payout", "external_send", "legal_filing"} or amount >= Decimal("500")
    risk_tier = "HIGH" if needs_human else "LOW"
    return {
        "requested_action": requested_action,
        "amount": str(amount),
        "risk_tier": risk_tier,
        "requires_human_approval": needs_human,
        "policy_basis": "financial/legal/destructive actions require human approval; inconsistent evidence blocks execution",
    }
