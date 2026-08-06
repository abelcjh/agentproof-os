from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def canonical_hash(data: dict[str, Any]) -> str:
    encoded = json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def build_receipt(run: dict[str, Any]) -> dict[str, Any]:
    receipt_body = {
        "case_id": run["case_id"],
        "objective": run["objective"],
        "agent_count": len({step["agent"] for step in run["steps"]}),
        "handoff_count": len(run["handoffs"]),
        "verification": run["verification"],
        "security": run["security"],
        "proposal": run["proposal"],
        "evidence_sources": [row.get("source_id") for row in run.get("evidence", [])],
        "no_external_side_effect_executed": run.get("security", {}).get("verdict") == "BLOCK",
    }
    return receipt_body | {"receipt_sha256": canonical_hash(receipt_body)}


def receipt_from_run(run_path: Path, out: Path) -> dict[str, Any]:
    run = json.loads(run_path.read_text())
    receipt = build_receipt(run)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipt, indent=2, sort_keys=True))
    return receipt


def verify_receipt(path: Path) -> tuple[bool, str]:
    receipt = json.loads(path.read_text())
    expected = receipt.get("receipt_sha256")
    body = {k: v for k, v in receipt.items() if k != "receipt_sha256"}
    actual = canonical_hash(body)
    return expected == actual, actual


def build_receipt_summary(receipt: dict[str, Any]) -> str:
    """Render a judge-readable proof summary from a verified receipt."""
    security = receipt.get("security", {})
    verification = receipt.get("verification", {})
    proposal = receipt.get("proposal", {})
    policy = proposal.get("policy", {})
    evidence_sources = receipt.get("evidence_sources", [])
    rows = [
        ("case", receipt.get("case_id", "unknown"), "receipt case id"),
        ("agents", str(receipt.get("agent_count", 0)), "distinct roles in the run"),
        ("typed handoffs", str(receipt.get("handoff_count", 0)), "handoff records preserved"),
        ("evidence sources", ", ".join(evidence_sources), "source ids retained"),
        ("verification", verification.get("verdict", "UNKNOWN"), f"failures={len(verification.get('failures', []))}"),
        ("security gate", security.get("verdict", "UNKNOWN"), f"blocked={security.get('blocked_side_effect', 'none')}"),
        ("approval boundary", str(policy.get("requires_human_approval", "unknown")), "policy requires explicit approval"),
        ("external side effect", "not executed" if receipt.get("no_external_side_effect_executed") else "executed/unknown", "fixture-safe demo boundary"),
        ("receipt sha256", receipt.get("receipt_sha256", "missing"), "tamper-evident hash"),
    ]
    table = ["| Signal | Value | Judge-visible proof |", "|---|---|---|"]
    table.extend(f"| {name} | {value} | {proof} |" for name, value, proof in rows)
    return "\n".join([
        "# Receipt proof summary",
        "",
        "Generated from `artifacts/receipts/latest.json` so judges can inspect the core proof signals without reading raw JSON.",
        "",
        *table,
        "",
    ])


def summary_from_receipt(receipt_path: Path, out: Path) -> str:
    ok, actual = verify_receipt(receipt_path)
    if not ok:
        raise ValueError(f"receipt hash mismatch, actual={actual}")
    receipt = json.loads(receipt_path.read_text())
    summary = build_receipt_summary(receipt)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(summary)
    return summary
