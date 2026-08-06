from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


def canonical_digest(data: dict[str, Any]) -> str:
    encoded = json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_tool_contracts(tool_dir: Path = Path("mcp_tools")) -> list[dict[str, Any]]:
    contracts: list[dict[str, Any]] = []
    for path in sorted(tool_dir.glob("*.tool.yaml")):
        data = yaml.safe_load(path.read_text()) or {}
        data["_path"] = str(path)
        contracts.append(data)
    return contracts


def build_tool_lock(tool_dir: Path = Path("mcp_tools")) -> dict[str, Any]:
    tools = []
    for contract in load_tool_contracts(tool_dir):
        body = {k: v for k, v in contract.items() if k != "_path"}
        tools.append({
            "path": contract["_path"],
            "name": contract.get("name"),
            "version": contract.get("version"),
            "protocol_shape": contract.get("protocol_shape"),
            "digest_sha256": canonical_digest(body),
        })
    return {"schema_version": "0.1.0", "tool_count": len(tools), "tools": tools}


def verify_tool_lock(lock_path: Path = Path("mcp_tools.lock.json"), tool_dir: Path = Path("mcp_tools")) -> tuple[bool, dict[str, Any]]:
    expected = json.loads(lock_path.read_text())
    actual = build_tool_lock(tool_dir)
    return expected == actual, actual
