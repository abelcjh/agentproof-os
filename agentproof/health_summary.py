from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _status(value: bool) -> str:
    return "PASS" if value else "NEEDS_REVIEW"


def build_health_summary(run: dict[str, Any], receipt: dict[str, Any]) -> str:
    """Render a judge-visible demo health and fallback contract.

    The goal is not to claim live infrastructure exists. It gives judges a fast,
    honest contract for how the demo can be rerun, which parts are fixture-safe,
    and which production integrations remain future work.
    """
    security = run.get("security", {})
    verification = run.get("verification", {})
    evidence_count = len(run.get("evidence", []))
    handoff_count = len(run.get("handoffs", []))
    agent_count = len({step.get("agent") for step in run.get("steps", [])})
    hash_present = bool(receipt.get("receipt_sha256"))
    side_effect_blocked = security.get("verdict") == "BLOCK"

    rows = [
        ("public repo", "https://github.com/abelcjh/agentproof-os", "open-source inspection path"),
        ("one-command verify", "make verify", "runs tests, fixture demo, receipt hash check, and generated summaries"),
        ("fixture/demo mode", _status(run.get("case_id") == "CASE-GOAI-001"), run.get("case_id", "unknown")),
        ("agent team minimum", _status(agent_count >= 3), f"agents={agent_count}"),
        ("typed handoffs", _status(handoff_count >= 3), f"handoffs={handoff_count}"),
        ("deterministic verifier", verification.get("verdict", "UNKNOWN"), f"failures={len(verification.get('failures', []))}"),
        ("AI/API dependency", "not required", "fixture path is deterministic and runs without live model keys"),
        ("external side effects", "blocked" if side_effect_blocked else "needs review", "; ".join(security.get("reasons", [])) or "no security reasons recorded"),
        ("evidence inputs", _status(evidence_count > 0), f"evidence_rows={evidence_count}"),
        ("tamper-evident receipt", _status(hash_present), receipt.get("receipt_sha256", "missing")),
        ("fallback path", "local replay", "use committed synthetic fixture if live AgentTeams/MCP deployment is unavailable"),
    ]
    table = ["| Demo health signal | Current status | Proof / fallback |", "|---|---|---|"]
    table.extend(f"| {name} | {value} | {proof} |" for name, value, proof in rows)

    return "\n".join([
        "# Demo health and fallback contract",
        "",
        "Generated from `artifacts/runs/latest.json` and `artifacts/receipts/latest.json`.",
        "It gives judges the reliability contract before the demo starts: what runs offline, what is blocked, and how to rerun the proof without secrets.",
        "",
        *table,
        "",
        "## honest scope boundary",
        "",
        "- Current committed proof is a deterministic local fixture, not a live AgentTeams room or production MCP gateway deployment.",
        "- The fixture intentionally blocks the risky refund side effect because explicit human approval is absent.",
        "- Future live integrations should preserve this contract: deterministic replay first, gateway/policy check before mutation, and a hashable receipt after execution.",
        "",
    ])


def health_summary_from_paths(run_path: Path, receipt_path: Path, out: Path) -> str:
    run = json.loads(run_path.read_text())
    receipt = json.loads(receipt_path.read_text())
    summary = build_health_summary(run, receipt)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(summary)
    return summary
