from __future__ import annotations

from pathlib import Path
import os

from trusted_ai_toolkit.config import load_config


def test_load_config_validates_new_sections(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
project_name: demo
risk_tier: medium
output_dir: artifacts
system:
  created_at: "2026-03-01T12:00:00Z"
  system_id: agent-risk-gateway
  system_name: Agent Risk Gateway
  version: 1.0.0
  model_provider: OpenAI
  model_name: gpt-4.1
  model_version: "2026-02-15"
  environment: production
  risk_level: high
  compliance_profile: regulated
  telemetry_level: enhanced
  deployment_region: us-east-1
  owner: ai-governance
eval:
  suites: [medium]
xai:
  reasoning_report_template: reasoning_report.md.j2
  include_sections: [Overview]
redteam:
  suites: [baseline]
  cases: [prompt_injection_basic]
  severity_threshold: high
monitoring:
  enabled: true
  telemetry_path: telemetry.jsonl
governance:
  required_stage_gates: [evaluation, redteam, documentation, monitoring]
adapters:
  provider: stub
artifact_policy:
  required_outputs_by_risk_tier:
    medium: [scorecard.md, scorecard.json]
""",
        encoding="utf-8",
    )

    cfg = load_config(config_path)
    assert cfg.project_name == "demo"
    assert cfg.system is not None
    assert cfg.system.system_id == "agent-risk-gateway"
    assert cfg.system.environment == "production"
    assert cfg.governance.required_stage_gates == ["evaluation", "redteam", "documentation", "monitoring"]
    assert cfg.adapters.provider == "stub"


def test_load_config_accepts_openai_compatible_adapter(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
project_name: demo
adapters:
  provider: openai_compatible
  endpoint: https://api.openai.com/v1
  model: gpt-4.1-mini
  embedding_model: text-embedding-3-small
  api_key_env: OPENAI_API_KEY
""",
        encoding="utf-8",
    )

    cfg = load_config(config_path)
    assert cfg.adapters.provider == "openai_compatible"
    assert cfg.adapters.endpoint == "https://api.openai.com/v1"
    assert cfg.adapters.model == "gpt-4.1-mini"
    assert cfg.adapters.embedding_model == "text-embedding-3-small"
    assert cfg.adapters.api_key_env == "OPENAI_API_KEY"


def test_load_config_accepts_ollama_adapter(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
project_name: demo
adapters:
  provider: ollama
  endpoint: http://localhost:11434
  model: qwen2.5-coder:3b
  request_format: ollama_generate
""",
        encoding="utf-8",
    )

    cfg = load_config(config_path)
    assert cfg.adapters.provider == "ollama"
    assert cfg.adapters.endpoint == "http://localhost:11434"
    assert cfg.adapters.model == "qwen2.5-coder:3b"
    assert cfg.adapters.request_format == "ollama_generate"


def test_load_config_reads_local_dotenv_when_present(tmp_path: Path, monkeypatch) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
project_name: demo
adapters:
  provider: openai_compatible
  endpoint: https://api.openai.com/v1
  model: gpt-4.1-mini
  api_key_env: OPENAI_API_KEY
""",
        encoding="utf-8",
    )
    (tmp_path / ".env").write_text("OPENAI_API_KEY=test_from_dotenv\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    cfg = load_config(config_path)

    assert cfg.adapters.api_key_env == "OPENAI_API_KEY"
    assert os.getenv("OPENAI_API_KEY") == "test_from_dotenv"
