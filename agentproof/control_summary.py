from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _policy_rows(run: dict[str, Any]) -> list[tuple[str, str, str]]:
    proposal = run.get("proposal", {})
    policy = proposal.get("policy", {})
    security = run.get("security", {})
    verification = run.get("verification", {})
    normalized = run.get("normalized_case", {})
    evidence_sources = ", ".join(row.get("source_id", "unknown") for row in run.get("evidence", []))
    side_effect = policy.get("requested_action", "unknown")
    decision = security.get("verdict", "UNKNOWN")
    approval_required = str(policy.get("requires_human_approval", "unknown"))
    approval_present = str(security.get("approval_present", "unknown"))
    return [
        ("task identity", run.get("case_id", "unknown"), "stable case/session id emitted in every receipt"),
        ("human / tenant boundary", normalized.get("stakeholder", "unknown"), "actor is tracked separately from workers; no worker receives real credentials in fixture mode"),
        ("requested tool/action", str(side_effect), "side-effect candidate extracted before any execution"),
        ("evidence inputs", evidence_sources or "none", "source ids remain attached to the decision"),
        ("deterministic verifier", verification.get("verdict", "UNKNOWN"), f"failures={len(verification.get('failures', []))}"),
        ("policy decision", decision, "; ".join(security.get("reasons", [])) or "no reasons recorded"),
        ("approval gate", f"required={approval_required}; present={approval_present}", "high-risk actions cannot self-approve"),
        ("external side effect", "not executed" if decision == "BLOCK" else "allowed/needs-review", "fixture-safe replay keeps mutation outside the agent process"),
    ]


def build_control_summary(run: dict[str, Any], receipt: dict[str, Any]) -> str:
    """Render gateway-style controls for the live request path from a run + receipt."""
    rows = _policy_rows(run)
    control_table = ["| Control surface | Current fixture value | Judge-visible proof |", "|---|---|---|"]
    control_table.extend(f"| {name} | {value} | {proof} |" for name, value, proof in rows)

    gateway_rows = [
        ("AgentTeams / HiClaw", "maps handoffs to visible Manager → Worker room messages", "`artifacts/runs/latest.md`"),
        ("MCP gateway pattern", "intercept tool/action before execution; deny risky mutation without approval", "this control summary + `agentproof/security.py`"),
        ("observability pattern", "emit task id, actor, tool/action, decision, reason, and receipt hash", "`artifacts/receipts/latest.json`"),
        ("tamper-evident exit artifact", "bind final decision to sha256 receipt", receipt.get("receipt_sha256", "missing")),
    ]
    gateway_table = ["| Inspiration pattern | Rule-clean AgentProof adaptation | Artifact |", "|---|---|---|"]
    gateway_table.extend(f"| {name} | {value} | {artifact} |" for name, value, artifact in gateway_rows)

    return "\n".join([
        "# Control surface summary",
        "",
        "Generated from `artifacts/runs/latest.json` and `artifacts/receipts/latest.json`.",
        "It turns the gateway / observability inspiration into concrete, local proof without claiming a live external MCP gateway deployment.",
        "",
        "## live-request-path controls in the fixture",
        "",
        *control_table,
        "",
        "## rule-clean inspiration mapping",
        "",
        *gateway_table,
        "",
    ])


def control_summary_from_paths(run_path: Path, receipt_path: Path, out: Path) -> str:
    run = json.loads(run_path.read_text())
    receipt = json.loads(receipt_path.read_text())
    summary = build_control_summary(run, receipt)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(summary)
    return summary
