from __future__ import annotations

from pathlib import Path
from typing import Any
import yaml

REQUIRED_SKILL_FIELDS = {"name", "version", "purpose", "inputs", "outputs", "failure_handling"}


def load_skill_contracts(skill_dir: Path = Path("skills")) -> list[dict[str, Any]]:
    contracts = []
    for path in sorted(skill_dir.glob("*.skill.yaml")):
        data = yaml.safe_load(path.read_text()) or {}
        data["_path"] = str(path)
        contracts.append(data)
    return contracts


def validate_skill_contracts(skill_dir: Path = Path("skills")) -> list[str]:
    errors: list[str] = []
    contracts = load_skill_contracts(skill_dir)
    if not contracts:
        return ["no skill contracts found"]
    for contract in contracts:
        missing = sorted(REQUIRED_SKILL_FIELDS - set(contract))
        if missing:
            errors.append(f"{contract.get('_path')}: missing {missing}")
        if not contract.get("failure_handling"):
            errors.append(f"{contract.get('_path')}: failure_handling must not be empty")
    return errors
