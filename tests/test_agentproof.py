from pathlib import Path

from agentproof.teams import run_fixture
from agentproof.receipt import receipt_from_run, verify_receipt, summary_from_receipt
from agentproof.skills import validate_skill_contracts
from agentproof.contracts import build_tool_lock, verify_tool_lock


def test_fixture_blocks_refund_without_approval(tmp_path):
    run_path = tmp_path / "run.json"
    data = run_fixture(Path("fixtures/cases/vendor_refund_claim.json"), run_path)
    assert len({step["agent"] for step in data["steps"]}) >= 3
    assert data["verification"]["verdict"] == "PASS"
    assert data["security"]["verdict"] == "BLOCK"
    assert data["security"]["blocked_side_effect"] == "refund"


def test_receipt_hash_roundtrip(tmp_path):
    run_path = tmp_path / "run.json"
    receipt_path = tmp_path / "receipt.json"
    run_fixture(Path("fixtures/cases/vendor_refund_claim.json"), run_path)
    receipt = receipt_from_run(run_path, receipt_path)
    ok, actual = verify_receipt(receipt_path)
    assert ok
    assert actual == receipt["receipt_sha256"]


def test_receipt_summary_renders_judge_proof_table(tmp_path):
    run_path = tmp_path / "run.json"
    receipt_path = tmp_path / "receipt.json"
    summary_path = tmp_path / "receipt.md"
    run_fixture(Path("fixtures/cases/vendor_refund_claim.json"), run_path)
    receipt_from_run(run_path, receipt_path)
    summary = summary_from_receipt(receipt_path, summary_path)
    assert "| agents | 6 | distinct roles in the run |" in summary
    assert "| security gate | BLOCK | blocked=refund |" in summary
    assert "receipt sha256" in summary


def test_skill_contracts_valid():
    assert validate_skill_contracts() == []


def test_tool_lock_matches_contracts():
    ok, actual = verify_tool_lock(Path("mcp_tools.lock.json"))
    assert ok
    assert actual["tool_count"] == len(build_tool_lock()["tools"])
