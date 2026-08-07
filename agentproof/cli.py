from __future__ import annotations

import argparse
from pathlib import Path

from .teams import run_fixture
from .receipt import receipt_from_run, verify_receipt, summary_from_receipt
from .trace_summary import trace_summary_from_run
from .control_summary import control_summary_from_paths
from .health_summary import health_summary_from_paths
from .proof_index import proof_index_from_paths
from .readiness_summary import readiness_summary_from_paths
from .gateway_trace import gateway_trace_from_paths
from .carrier_summary import carrier_summary_from_paths
from .identity_summary import identity_summary_from_paths
from .ops_metrics_summary import ops_metrics_summary_from_paths
from .governance_gates_summary import governance_gates_summary_from_paths
from .skills import validate_skill_contracts
from .contracts import build_tool_lock, verify_tool_lock


def main() -> None:
    parser = argparse.ArgumentParser(prog="agentproof")
    sub = parser.add_subparsers(dest="cmd", required=True)

    run_p = sub.add_parser("run")
    run_p.add_argument("--fixture", required=True)
    run_p.add_argument("--out", required=True)

    receipt_p = sub.add_parser("receipt")
    receipt_p.add_argument("--run", required=True)
    receipt_p.add_argument("--out", required=True)

    verify_p = sub.add_parser("verify-receipt")
    verify_p.add_argument("--receipt", required=True)

    summary_p = sub.add_parser("receipt-summary")
    summary_p.add_argument("--receipt", required=True)
    summary_p.add_argument("--out", required=True)

    trace_p = sub.add_parser("trace-summary")
    trace_p.add_argument("--run", required=True)
    trace_p.add_argument("--out", required=True)

    control_p = sub.add_parser("control-summary")
    control_p.add_argument("--run", required=True)
    control_p.add_argument("--receipt", required=True)
    control_p.add_argument("--out", required=True)

    health_p = sub.add_parser("health-summary")
    health_p.add_argument("--run", required=True)
    health_p.add_argument("--receipt", required=True)
    health_p.add_argument("--out", required=True)

    proof_p = sub.add_parser("proof-index")
    proof_p.add_argument("--run", required=True)
    proof_p.add_argument("--receipt", required=True)
    proof_p.add_argument("--out", required=True)

    readiness_p = sub.add_parser("readiness-summary")
    readiness_p.add_argument("--run", required=True)
    readiness_p.add_argument("--receipt", required=True)
    readiness_p.add_argument("--out", required=True)

    gateway_p = sub.add_parser("gateway-trace")
    gateway_p.add_argument("--run", required=True)
    gateway_p.add_argument("--receipt", required=True)
    gateway_p.add_argument("--out", required=True)

    carrier_p = sub.add_parser("carrier-summary")
    carrier_p.add_argument("--run", required=True)
    carrier_p.add_argument("--receipt", required=True)
    carrier_p.add_argument("--out", required=True)

    identity_p = sub.add_parser("identity-summary")
    identity_p.add_argument("--run", required=True)
    identity_p.add_argument("--receipt", required=True)
    identity_p.add_argument("--out", required=True)

    ops_p = sub.add_parser("ops-metrics-summary")
    ops_p.add_argument("--run", required=True)
    ops_p.add_argument("--receipt", required=True)
    ops_p.add_argument("--out", required=True)

    gates_p = sub.add_parser("governance-gates-summary")
    gates_p.add_argument("--run", required=True)
    gates_p.add_argument("--receipt", required=True)
    gates_p.add_argument("--out", required=True)

    lock_p = sub.add_parser("write-tool-lock")
    lock_p.add_argument("--out", default="mcp_tools.lock.json")

    verify_lock_p = sub.add_parser("check-tool-lock")
    verify_lock_p.add_argument("--lock", default="mcp_tools.lock.json")

    sub.add_parser("check-skills")
    args = parser.parse_args()

    if args.cmd == "run":
        data = run_fixture(Path(args.fixture), Path(args.out))
        print(f"run written: {args.out} agents={len({s['agent'] for s in data['steps']})} handoffs={len(data['handoffs'])}")
    elif args.cmd == "receipt":
        receipt = receipt_from_run(Path(args.run), Path(args.out))
        print(f"receipt written: {args.out} sha256={receipt['receipt_sha256']}")
    elif args.cmd == "verify-receipt":
        ok, actual = verify_receipt(Path(args.receipt))
        if not ok:
            raise SystemExit(f"receipt hash mismatch, actual={actual}")
        print(f"receipt verified: {args.receipt} sha256={actual}")
    elif args.cmd == "receipt-summary":
        summary_from_receipt(Path(args.receipt), Path(args.out))
        print(f"receipt summary written: {args.out}")
    elif args.cmd == "trace-summary":
        trace_summary_from_run(Path(args.run), Path(args.out))
        print(f"trace summary written: {args.out}")
    elif args.cmd == "control-summary":
        control_summary_from_paths(Path(args.run), Path(args.receipt), Path(args.out))
        print(f"control summary written: {args.out}")
    elif args.cmd == "health-summary":
        health_summary_from_paths(Path(args.run), Path(args.receipt), Path(args.out))
        print(f"health summary written: {args.out}")
    elif args.cmd == "proof-index":
        proof_index_from_paths(Path(args.run), Path(args.receipt), Path(args.out))
        print(f"proof index written: {args.out}")
    elif args.cmd == "readiness-summary":
        readiness_summary_from_paths(Path(args.run), Path(args.receipt), Path(args.out))
        print(f"readiness summary written: {args.out}")
    elif args.cmd == "gateway-trace":
        gateway_trace_from_paths(Path(args.run), Path(args.receipt), Path(args.out))
        print(f"gateway trace written: {args.out}")
    elif args.cmd == "carrier-summary":
        carrier_summary_from_paths(Path(args.run), Path(args.receipt), Path(args.out))
        print(f"carrier summary written: {args.out}")
    elif args.cmd == "identity-summary":
        identity_summary_from_paths(Path(args.run), Path(args.receipt), Path(args.out))
        print(f"identity summary written: {args.out}")
    elif args.cmd == "ops-metrics-summary":
        ops_metrics_summary_from_paths(Path(args.run), Path(args.receipt), Path(args.out))
        print(f"ops metrics summary written: {args.out}")
    elif args.cmd == "governance-gates-summary":
        governance_gates_summary_from_paths(Path(args.run), Path(args.receipt), Path(args.out))
        print(f"governance gates summary written: {args.out}")
    elif args.cmd == "check-skills":
        errors = validate_skill_contracts()
        if errors:
            raise SystemExit("skill contract errors:\n" + "\n".join(errors))
        print("skill contracts verified")
    elif args.cmd == "write-tool-lock":
        import json
        lock = build_tool_lock()
        Path(args.out).write_text(json.dumps(lock, indent=2, sort_keys=True))
        print(f"tool lock written: {args.out} tools={lock['tool_count']}")
    elif args.cmd == "check-tool-lock":
        ok, actual = verify_tool_lock(Path(args.lock))
        if not ok:
            raise SystemExit("tool lock drift detected; run `python -m agentproof.cli write-tool-lock`")
        print(f"tool lock verified: {args.lock} tools={actual['tool_count']}")


if __name__ == "__main__":
    main()
