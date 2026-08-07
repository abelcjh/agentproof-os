from pathlib import Path

from agentproof.teams import run_fixture
from agentproof.receipt import receipt_from_run, verify_receipt, summary_from_receipt
from agentproof.trace_summary import trace_summary_from_run
from agentproof.control_summary import control_summary_from_paths
from agentproof.health_summary import health_summary_from_paths
from agentproof.proof_index import proof_index_from_paths
from agentproof.readiness_summary import readiness_summary_from_paths
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


def test_trace_summary_renders_agentteams_handoffs(tmp_path):
    run_path = tmp_path / "run.json"
    summary_path = tmp_path / "run.md"
    run_fixture(Path("fixtures/cases/vendor_refund_claim.json"), run_path)
    summary = trace_summary_from_run(run_path, summary_path)
    assert "# Agent team trace summary" in summary
    assert "AgentTeams-style room transcript" in summary
    assert "IntakeAgent → EvidenceAgent" in summary
    assert "SecurityAuditor::audit_side_effects" in summary
    assert "BLOCK `refund`" in summary


def test_control_summary_renders_gateway_style_proof(tmp_path):
    run_path = tmp_path / "run.json"
    receipt_path = tmp_path / "receipt.json"
    summary_path = tmp_path / "control.md"
    run_fixture(Path("fixtures/cases/vendor_refund_claim.json"), run_path)
    receipt = receipt_from_run(run_path, receipt_path)
    summary = control_summary_from_paths(run_path, receipt_path, summary_path)
    assert "# Control surface summary" in summary
    assert "| policy decision | BLOCK |" in summary
    assert "MCP gateway pattern" in summary
    assert receipt["receipt_sha256"] in summary


def test_health_summary_renders_demo_fallback_contract(tmp_path):
    run_path = tmp_path / "run.json"
    receipt_path = tmp_path / "receipt.json"
    summary_path = tmp_path / "health.md"
    run_fixture(Path("fixtures/cases/vendor_refund_claim.json"), run_path)
    receipt = receipt_from_run(run_path, receipt_path)
    summary = health_summary_from_paths(run_path, receipt_path, summary_path)
    assert "# Demo health and fallback contract" in summary
    assert "| one-command verify | make verify |" in summary
    assert "| AI/API dependency | not required |" in summary
    assert "| external side effects | blocked |" in summary
    assert receipt["receipt_sha256"] in summary


def test_proof_index_renders_judge_packet(tmp_path):
    run_path = tmp_path / "run.json"
    receipt_path = tmp_path / "receipt.json"
    summary_path = tmp_path / "proof.md"
    run_fixture(Path("fixtures/cases/vendor_refund_claim.json"), run_path)
    receipt = receipt_from_run(run_path, receipt_path)
    summary = proof_index_from_paths(run_path, receipt_path, summary_path)
    assert "# Judge proof packet index" in summary
    assert "| agent roles | 6 | >=3 distinct agents required by GOAI Agent Infra |" in summary
    assert "| side-effect policy | BLOCK | blocked=refund |" in summary
    assert "artifacts/control/latest.md" in summary
    assert receipt["receipt_sha256"] in summary


def test_readiness_summary_maps_goai_rubric(tmp_path):
    run_path = tmp_path / "run.json"
    receipt_path = tmp_path / "receipt.json"
    summary_path = tmp_path / "readiness.md"
    run_fixture(Path("fixtures/cases/vendor_refund_claim.json"), run_path)
    receipt = receipt_from_run(run_path, receipt_path)
    summary = readiness_summary_from_paths(run_path, receipt_path, summary_path)
    assert "# GOAI Agent Infra readiness receipt" in summary
    assert "**Fixture-backed weighted readiness:** 100/100" in summary
    assert "| multi-agent collaboration / autonomous loop | 25% | READY |" in summary
    assert "| engineering verification / security auditability | 20% | READY |" in summary
    assert receipt["receipt_sha256"] in summary


def test_skill_contracts_valid():
    assert validate_skill_contracts() == []


def test_tool_lock_matches_contracts():
    ok, actual = verify_tool_lock(Path("mcp_tools.lock.json"))
    assert ok
    assert actual["tool_count"] == len(build_tool_lock()["tools"])
