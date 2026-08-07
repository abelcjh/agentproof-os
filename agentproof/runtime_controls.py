from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


def tool_call(agent: str, name: str, *, status: str = "VERIFIED", reason: str = "verified by deterministic gate") -> dict[str, Any]:
    """Small, portable tool-call envelope with explicit agent identity."""
    return {
        "tool": name,
        "caller_agent": agent,
        "agent_role": agent.replace("Agent", "").replace("Auditor", "Auditor"),
        "authority_ref": f"{agent}:{name}",
        "outcome_status": status,
        "verification_reason": reason,
    }


def _iter_tool_calls(run: dict[str, Any]) -> list[dict[str, Any]]:
    calls: list[dict[str, Any]] = []
    for step in run.get("steps", []):
        for call in step.get("output", {}).get("tool_calls", []):
            merged = {"agent": step.get("agent"), "action": step.get("action")} | call
            calls.append(merged)
    return calls


def accepted_not_verified_outcomes(run: dict[str, Any]) -> list[dict[str, str]]:
    flagged: list[dict[str, str]] = []
    for call in _iter_tool_calls(run):
        if call.get("outcome_status") == "ACCEPTED_NOT_VERIFIED":
            flagged.append({
                "agent": str(call.get("caller_agent") or call.get("agent")),
                "tool": str(call.get("tool")),
                "outcome": "ACCEPTED_NOT_VERIFIED",
                "reason": str(call.get("verification_reason", "tool output accepted before deterministic verifier gate")),
            })
    return flagged


def agent_identity_coverage(run: dict[str, Any]) -> dict[str, Any]:
    calls = _iter_tool_calls(run)
    missing = [
        f"{call.get('agent')}:{call.get('tool')}"
        for call in calls
        if not (call.get("caller_agent") and call.get("agent_role") and call.get("authority_ref"))
    ]
    return {
        "tool_calls": len(calls),
        "missing_identity": missing,
        "authority_refs": [str(call.get("authority_ref")) for call in calls if call.get("authority_ref")],
    }


def deadman_switch_status(run: dict[str, Any], *, max_steps: int = 12, max_repeated_action: int = 2) -> dict[str, Any]:
    steps = run.get("steps", [])
    action_counts = Counter(f"{step.get('agent')}:{step.get('action')}" for step in steps)
    repeated = {k: v for k, v in action_counts.items() if v > max_repeated_action}
    failures: list[str] = []
    if len(steps) > max_steps:
        failures.append(f"step budget exceeded: {len(steps)} > {max_steps}")
    if repeated:
        failures.append(f"repeated action budget exceeded: {repeated}")
    return {
        "verdict": "BLOCK" if failures else "PASS",
        "steps": len(steps),
        "max_steps": max_steps,
        "max_repeated_action": max_repeated_action,
        "failures": failures,
    }


def waterfall_trace_markdown(run: dict[str, Any]) -> str:
    lines = [
        "# Agent waterfall trace",
        "",
        "| # | agent | action | tools | authority refs | tool outcome |",
        "|---:|---|---|---|---|---|",
    ]
    for idx, step in enumerate(run.get("steps", []), 1):
        calls = step.get("output", {}).get("tool_calls", [])
        tools = ", ".join(call.get("tool", "-") for call in calls) or "-"
        refs = ", ".join(call.get("authority_ref", "-") for call in calls) or "-"
        outcomes = ", ".join(call.get("outcome_status", "-") for call in calls) or "-"
        lines.append(f"| {idx} | {step.get('agent')} | {step.get('action')} | {tools} | {refs} | {outcomes} |")
    lines.extend([
        "",
        "## terminal gates",
        "",
        f"| verifier | `{run.get('verification', {}).get('verdict')}` | checked_handoffs={run.get('verification', {}).get('checked_handoffs')} |",
        "|---|---|---|",
        f"| security | `{run.get('security', {}).get('verdict')}` | blocked_side_effect={run.get('security', {}).get('blocked_side_effect')} |",
    ])
    return "\n".join(lines) + "\n"


def runtime_controls_summary_from_paths(run_path: Path, receipt_path: Path, out: Path) -> str:
    run = json.loads(run_path.read_text())
    receipt = json.loads(receipt_path.read_text())
    flagged = accepted_not_verified_outcomes(run)
    identity = agent_identity_coverage(run)
    guard = deadman_switch_status(run)
    waterfall = waterfall_trace_markdown(run)
    summary = f"""# Runtime controls proof receipt

| improvement | fixture-backed evidence |
|---|---|
| accepted-but-not-verified detector | `{len(flagged)}` outcome(s) flagged before deterministic verifier closure |
| agent identity coverage | `{identity['tool_calls']}` tool calls, missing identity `{len(identity['missing_identity'])}` |
| dead-man switch | `{guard['verdict']}` with steps `{guard['steps']}/{guard['max_steps']}` |
| waterfall trace | rendered below with agent → action → tool → authority ref |
| Postgres-style support workflow | domain `{run.get('normalized_case', {}).get('domain')}` requested_action `{run.get('normalized_case', {}).get('requested_action')}` |

| terminal gate | verdict | detail |
|---|---|---|
| verifier | `{run.get('verification', {}).get('verdict')}` | checked_handoffs={run.get('verification', {}).get('checked_handoffs')} |
| security | `{run.get('security', {}).get('verdict')}` | blocked_side_effect={run.get('security', {}).get('blocked_side_effect')} |

receipt sha256: `{receipt['receipt_sha256']}`

{waterfall}
"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(summary)
    return summary
