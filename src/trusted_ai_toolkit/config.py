"""Configuration loading and environment override utilities."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from trusted_ai_toolkit.schemas import ToolkitConfig


class ConfigError(ValueError):
    """Raised when config file parsing or validation fails."""


def _load_dotenv(path: str | Path = ".env") -> None:
    """Load simple KEY=VALUE pairs from a local .env file if present.

    Existing environment variables win over file values.
    """

    env_path = Path(path)
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        if key and key not in os.environ:
            os.environ[key] = value


def _apply_env_overrides(raw: dict[str, Any]) -> dict[str, Any]:
    """Apply environment variable overrides to config dictionary."""

    output_dir_override = os.getenv("TAT_OUTPUT_DIR")
    run_id_override = os.getenv("TAT_RUN_ID")
    adapter_provider_override = os.getenv("TAT_ADAPTER_PROVIDER")
    adapter_endpoint_override = os.getenv("TAT_ADAPTER_ENDPOINT")
    adapter_model_override = os.getenv("TAT_ADAPTER_MODEL")
    adapter_api_key_env_override = os.getenv("TAT_ADAPTER_API_KEY_ENV")
    adapter_request_format_override = os.getenv("TAT_ADAPTER_REQUEST_FORMAT")

    if output_dir_override:
        raw["output_dir"] = output_dir_override

    monitoring = raw.setdefault("monitoring", {})
    if run_id_override:
        monitoring["run_id"] = run_id_override
    if adapter_provider_override:
        adapters = raw.setdefault("adapters", {})
        adapters["provider"] = adapter_provider_override
    if adapter_endpoint_override:
        adapters = raw.setdefault("adapters", {})
        adapters["endpoint"] = adapter_endpoint_override
    if adapter_model_override:
        adapters = raw.setdefault("adapters", {})
        adapters["model"] = adapter_model_override
    if adapter_api_key_env_override:
        adapters = raw.setdefault("adapters", {})
        adapters["api_key_env"] = adapter_api_key_env_override
    if adapter_request_format_override:
        adapters = raw.setdefault("adapters", {})
        adapters["request_format"] = adapter_request_format_override

    return raw


def load_config(path: str | Path) -> ToolkitConfig:
    """Load YAML config from path and validate as ToolkitConfig.

    Args:
        path: Path to YAML configuration file.

    Returns:
        Validated ToolkitConfig.

    Raises:
        ConfigError: If file is missing, malformed, or invalid.
    """

    config_path = Path(path)
    if not config_path.exists():
        raise ConfigError(f"Config file not found: {config_path}")

    # Load local developer secrets before reading env-based config overrides.
    _load_dotenv(Path.cwd() / ".env")

    try:
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ConfigError(f"Invalid YAML in {config_path}: {exc}") from exc

    if raw is None:
        raw = {}
    if not isinstance(raw, dict):
        raise ConfigError("Config root must be a mapping/object")

    raw = _apply_env_overrides(raw)

    try:
        return ToolkitConfig.model_validate(raw)
    except ValidationError as exc:
        raise ConfigError(f"Invalid configuration: {exc}") from exc
