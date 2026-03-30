"""Benchmark registry and historical standardization utilities."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from trusted_ai_toolkit.schemas import MetricResult, ToolkitConfig


def resolved_generation_model_name(config: ToolkitConfig) -> str:
    """Return the effective generation model identity used for cohorting.

    Cohorts should follow the model that actually produced the answer, not
    whichever system metadata field happened to be set. This prevents OpenAI
    runs from being benchmarked against stale or unrelated local-model history.
    """

    if config.adapters.model:
        return config.adapters.model
    if config.system and config.system.model_name:
        return config.system.model_name
    return "unknown_model"


def _registry_path(path: str | Path) -> Path:
    return Path(path)


def load_registry(path: str | Path) -> dict[str, Any]:
    registry_path = _registry_path(path)
    if not registry_path.exists():
        return {"runs": []}
    payload = json.loads(registry_path.read_text(encoding="utf-8"))
    if isinstance(payload, dict) and isinstance(payload.get("runs"), list):
        return payload
    return {"runs": []}


def write_registry(path: str | Path, payload: dict[str, Any]) -> Path:
    registry_path = _registry_path(path)
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    registry_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return registry_path


def update_registry(path: str | Path, project_name: str, run_id: str, metric_results: list[MetricResult]) -> Path:
    registry = load_registry(path)
    runs = [item for item in registry.get("runs", []) if isinstance(item, dict) and item.get("run_id") != run_id]
    runs.append(
        {
            "project_name": project_name,
            "run_id": run_id,
            "metrics": {
                metric.metric_id: {
                    "value": metric.value,
                    "threshold": metric.threshold,
                    "passed": metric.passed,
                }
                for metric in metric_results
            },
        }
    )
    registry["runs"] = runs
    return write_registry(path, registry)


def build_cohort_key(config: ToolkitConfig) -> str:
    """Build a benchmark cohort key from deployment tier, task, and model identity."""

    deployment_risk_tier = config.risk_tier
    task = config.model.task if config.model else "unknown_task"
    effective_model = resolved_generation_model_name(config)
    # Tier, task, and model are the minimum split needed to keep trust-score
    # baselines meaningfully comparable without exploding the cohort count.
    return f"{deployment_risk_tier}|{task}|{effective_model}"


def update_registry_for_config(
    path: str | Path,
    config: ToolkitConfig,
    run_id: str,
    metric_results: list[MetricResult],
) -> Path:
    registry = load_registry(path)
    runs = [item for item in registry.get("runs", []) if isinstance(item, dict) and item.get("run_id") != run_id]
    runs.append(
        {
            "project_name": config.project_name,
            "cohort_key": build_cohort_key(config),
            "risk_tier": config.risk_tier,
            "task": config.model.task if config.model else None,
            "model_name": resolved_generation_model_name(config),
            "run_id": run_id,
            "metrics": {
                metric.metric_id: {
                    "value": metric.value,
                    "threshold": metric.threshold,
                    "passed": metric.passed,
                }
                for metric in metric_results
            },
        }
    )
    registry["runs"] = runs
    return write_registry(path, registry)


def benchmark_distributions(
    registry_path: str | Path,
    config: ToolkitConfig,
    current_run_id: str,
) -> dict[str, dict[str, float]]:
    """Summarize historical metric distributions from prior registry entries."""

    registry = load_registry(registry_path)
    values_by_metric: dict[str, list[float]] = {}
    cohort_key = build_cohort_key(config)
    for item in registry.get("runs", []):
        if not isinstance(item, dict):
            continue
        if (
            item.get("run_id") == current_run_id
            or item.get("project_name") != config.project_name
            or item.get("cohort_key") != cohort_key
        ):
            continue
        metrics = item.get("metrics", {})
        if not isinstance(metrics, dict):
            continue
        for metric_id, details in metrics.items():
            if not isinstance(metric_id, str) or not isinstance(details, dict):
                continue
            value = details.get("value")
            if isinstance(value, (int, float)):
                values_by_metric.setdefault(metric_id, []).append(float(value))

    distributions: dict[str, dict[str, float]] = {}
    for metric_id, values in values_by_metric.items():
        if len(values) < 2:
            continue
        mean = sum(values) / len(values)
        variance = sum((value - mean) ** 2 for value in values) / (len(values) - 1)
        std_dev = math.sqrt(variance)
        distributions[metric_id] = {
            "n": float(len(values)),
            "mean": round(mean, 6),
            "std_dev": round(std_dev, 6),
        }
    return distributions


def metric_z_from_history(metric: MetricResult, distributions: dict[str, dict[str, float]]) -> float | None:
    """Compute z-score from historical distributions when enough data exists."""

    stats = distributions.get(metric.metric_id)
    if not stats:
        return None
    std_dev = float(stats.get("std_dev", 0.0))
    if std_dev <= 0:
        return None
    mean = float(stats.get("mean", 0.0))
    return round((float(metric.value) - mean) / std_dev, 4)
