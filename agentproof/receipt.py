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
