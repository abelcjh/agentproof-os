from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _agent_role(step: dict[str, Any]) -> str:
    return f"{step.get('agent', 'UnknownAgent')}::{step.get('action', 'unknown_action')}"


def build_trace_summary(run: dict[str, Any]) -> str:
    """Render a judge-readable AgentTeams-style collaboration transcript."""
    steps = run.get("steps", [])
    handoffs = run.get("handoffs", [])
    agents = [_agent_role(step) for step in steps]
    gate = run.get("security", {})
    verification = run.get("verification", {})
    proposal = run.get("proposal", {})
    policy = proposal.get("policy", {})

    overview_rows = [
        ("case", run.get("case_id", "unknown"), "single fixture used for reproducible review"),
        ("agent roles", str(len({step.get("agent") for step in steps})), "distinct workers visible to the judge"),
        ("handoffs", str(len(handoffs)), "typed context transfers preserved in order"),
        ("verification", verification.get("verdict", "UNKNOWN"), f"failures={len(verification.get('failures', []))}"),
        ("policy gate", gate.get("verdict", "UNKNOWN"), f"requested={policy.get('requested_action', 'unknown')} risk={policy.get('risk_tier', 'unknown')}"),
        ("human approval", str(policy.get("requires_human_approval", "unknown")), "risky side effects cannot self-approve"),
    ]
    overview = ["| Signal | Value | Why judges should care |", "|---|---|---|"]
    overview.extend(f"| {name} | {value} | {why} |" for name, value, why in overview_rows)

    handoff_table = ["| # | Sender → Receiver | Summary | Payload keys |", "|---:|---|---|---|"]
    for idx, handoff in enumerate(handoffs, start=1):
        payload = handoff.get("payload", {})
        keys = ", ".join(sorted(payload.keys())) if isinstance(payload, dict) else "non-object"
        handoff_table.append(
            f"| {idx} | {handoff.get('sender', 'unknown')} → {handoff.get('receiver', 'unknown')} | "
            f"{handoff.get('summary', '')} | {keys} |"
        )

    action_table = ["| # | Agent action | Judge-visible result |", "|---:|---|---|"]
    for idx, step in enumerate(steps, start=1):
        output = step.get("output", {})
        if step.get("agent") == "SecurityAuditor":
            result = f"{output.get('verdict', 'UNKNOWN')} `{output.get('blocked_side_effect', 'none')}`"
        elif step.get("agent") == "VerifierAgent":
            result = f"{output.get('verdict', 'UNKNOWN')} failures={len(output.get('failures', []))}"
        elif step.get("agent") == "EvidenceAgent":
            result = f"evidence_count={output.get('evidence_count', 0)}"
        elif step.get("agent") == "SkillLibrarian":
            result = f"skill_candidate={output.get('skill_candidate', 'none')}"
        else:
            result = ", ".join(sorted(output.keys())) if isinstance(output, dict) else "output captured"
        action_table.append(f"| {idx} | {_agent_role(step)} | {result} |")

    return "\n".join(
        [
            "# Agent team trace summary",
            "",
            "Generated from `artifacts/runs/latest.json` to make the multi-agent collaboration legible without opening raw JSON.",
            "It is a local, deterministic replay artifact and a stable fallback for later AgentTeams/Matrix room integration.",
            "",
            "## overview",
            "",
            *overview,
            "",
            "## AgentTeams-style room transcript",
            "",
            "AgentProof maps each typed handoff to a future Matrix/AgentTeams room message: sender, receiver, summary, and payload contract are all explicit.",
            "",
            *handoff_table,
            "",
            "## worker action ledger",
            "",
            *action_table,
            "",
            "## role inventory",
            "",
            "- " + "\n- ".join(agents) if agents else "- no steps recorded",
            "",
        ]
    )


def trace_summary_from_run(run_path: Path, out: Path) -> str:
    run = json.loads(run_path.read_text())
    summary = build_trace_summary(run)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(summary)
    return summary
