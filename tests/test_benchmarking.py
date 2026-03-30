from __future__ import annotations

from trusted_ai_toolkit.benchmarking import build_cohort_key
from trusted_ai_toolkit.schemas import ToolkitConfig


def test_build_cohort_key_uses_adapter_model_identity() -> None:
    cfg = ToolkitConfig(
        project_name="demo",
        risk_tier="medium",
        model={"task": "question_answering"},
        system={
            "created_at": "2026-03-01T12:00:00Z",
            "system_id": "agent-risk-gateway",
            "system_name": "Agent Risk Gateway",
            "version": "1.0.0",
            "model_provider": "OpenAI",
            "model_name": "stale-system-model",
            "model_version": "2026-02-15",
            "environment": "production",
            "risk_level": "medium",
            "compliance_profile": "regulated",
            "telemetry_level": "enhanced",
            "deployment_region": "us-east-1",
            "owner": "ai-governance",
        },
        adapters={
            "provider": "openai_compatible",
            "endpoint": "https://api.openai.com/v1",
            "model": "gpt-4.1-mini",
        },
    )

    assert build_cohort_key(cfg) == "medium|question_answering|gpt-4.1-mini"
