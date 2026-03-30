"""Deterministic control definitions and evaluation results."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Literal

from tat.schemas import SystemSpec

Pillar = Literal["security", "reliability", "transparency", "governance"]
Severity = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class Control:
    """A single deterministic control check."""

    control_id: str
    pillar: Pillar
    severity: Severity
    description: str
    evaluator: Callable[[SystemSpec], tuple[bool, str]]


@dataclass(frozen=True)
class ControlResult:
    """Result of evaluating one control."""

    control_id: str
    pillar: Pillar
    severity: Severity
    passed: bool
    message: str

    def as_dict(self) -> dict[str, str | bool]:
        return {
            "control_id": self.control_id,
            "pillar": self.pillar,
            "severity": self.severity,
            "passed": self.passed,
            "message": self.message,
        }
