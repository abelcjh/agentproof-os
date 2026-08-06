from __future__ import annotations

import argparse
from pathlib import Path

from .teams import run_fixture
from .receipt import receipt_from_run, verify_receipt
from .skills import validate_skill_contracts


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
    elif args.cmd == "check-skills":
        errors = validate_skill_contracts()
        if errors:
            raise SystemExit("skill contract errors:\n" + "\n".join(errors))
        print("skill contracts verified")


if __name__ == "__main__":
    main()
