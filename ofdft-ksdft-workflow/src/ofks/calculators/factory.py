from __future__ import annotations

from pathlib import Path
from typing import Any

from ofks.calculators.base import CalculatorRunner
from ofks.calculators.dftpy_runner import DftpyCalculatorRunner
from ofks.calculators.fake_runner import FakeCalculatorRunner
from ofks.config import load_yaml


def build_calculator(config_path: str | Path) -> CalculatorRunner:
    config = load_yaml(config_path)
    backend = str(config.get("backend", "")).lower()
    if backend == "fake":
        return FakeCalculatorRunner(config)
    if backend == "dftpy":
        return DftpyCalculatorRunner(config)
    raise ValueError(f"Unsupported calculator backend for local workflow: {backend!r}")


def calculator_name(config: dict[str, Any]) -> str:
    return str(config.get("name") or config.get("backend") or "calculator")
