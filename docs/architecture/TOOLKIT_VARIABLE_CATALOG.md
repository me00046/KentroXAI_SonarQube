# Toolkit Variable Catalog

This document lists toolkit variables and explains what each variable is and why it is important.
Scope includes configuration keys, schema contract fields, CLI inputs, environment overrides, and orchestration payload keys.

## Environment Override Variables

| Variable | What It Is | Why It Is Important |
|---|---|---|
| `TAT_OUTPUT_DIR` | Environment override for `output_dir` in config loading. | Allows redirecting artifact output location without editing YAML. |
| `TAT_RUN_ID` | Environment override for `monitoring.run_id`. | Forces deterministic run folder naming for reproducibility and CI workflows. |
| `TAT_ADAPTER_PROVIDER` | Environment override for `adapters.provider`. | Enables provider switching (for example `stub` to `azure_openai`) without config file edits. |

## CLI Input Variables

| Variable | Command(s) | What It Is | Why It Is Important |
|---|---|---|---|
| `config` | Most CLI commands (`eval run`, `xai reasoning-report`, `redteam run`, `report`, `docs build`, `monitor summarize`, `incident generate`, `run prompt`) | Path to toolkit YAML config. | Governs all runtime settings and risk controls for the run. |
| `prompt` | `tat run prompt` | End-user prompt text under test. | Defines the primary evaluation input for orchestration runs. |
| `model_output` | `tat run prompt` | Optional provided output text; otherwise a stub output is used. | Allows offline testing of governance pipeline without live model invocation. |
| `context_file` | `tat run prompt` | Optional JSON context source file for retrieved contexts. | Enables traceability and grounding checks against retrieval context. |

## Orchestration Payload Variables

| Variable | What It Is | Why It Is Important |
|---|---|---|
| `project_name` | Project identifier included in `prompt_run.json`. | Links run evidence to the intended system/workstream. |
| `run_id` | Unique run identifier included in `prompt_run.json` and all artifacts. | Enables end-to-end traceability and artifact correlation. |
| `prompt` | Prompt text stored in `prompt_run.json`. | Preserves exact input for audit and reproducibility. |
| `model_output` | Output text stored in `prompt_run.json`. | Preserves evaluated output for scoring and governance review. |
| `retrieved_contexts` | Retrieval metadata stored in `prompt_run.json`. | Supports grounding, explainability, and citation lineage checks. |
| `adapter` | Serialized adapter config stored in `prompt_run.json`. | Records integration/runtime profile used for the run. |

## Schema Contract Variables

### `ToolkitConfig`
Top-level toolkit configuration contract.

| Variable | Type | Default | What It Is | Why It Is Important |
|---|---|---|---|---|
| `project_name` | `str` | `trusted-ai-project` | Field in `ToolkitConfig` used by toolkit workflows. | Anchors traceability and governance scope across all artifacts. |
| `risk_tier` | `Literal` | `medium` | Field in `ToolkitConfig` used by toolkit workflows. | Anchors traceability and governance scope across all artifacts. |
| `output_dir` | `str` | `artifacts` | Field in `ToolkitConfig` used by toolkit workflows. | Determines evidence-pack completeness and auditability. |
| `data` | `trusted_ai_toolkit.schemas.DataConfig | None` | None | Field in `ToolkitConfig` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `model` | `trusted_ai_toolkit.schemas.ModelConfig | None` | None | Field in `ToolkitConfig` used by toolkit workflows. | Controls external model adapter behavior and integration boundaries. |
| `eval` | `EvalConfig` | `dynamic/default_factory` | Field in `ToolkitConfig` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `xai` | `XAIConfig` | `dynamic/default_factory` | Field in `ToolkitConfig` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `redteam` | `RedTeamConfig` | `dynamic/default_factory` | Field in `ToolkitConfig` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `monitoring` | `MonitoringConfig` | `dynamic/default_factory` | Field in `ToolkitConfig` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `governance` | `GovernanceConfig` | `dynamic/default_factory` | Field in `ToolkitConfig` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `adapters` | `AdapterConfig` | `dynamic/default_factory` | Field in `ToolkitConfig` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `artifact_policy` | `ArtifactPolicyConfig` | `dynamic/default_factory` | Field in `ToolkitConfig` used by toolkit workflows. | Determines evidence-pack completeness and auditability. |

### `DataConfig`
Configuration describing the dataset and intended use context.

| Variable | Type | Default | What It Is | Why It Is Important |
|---|---|---|---|---|
| `dataset_name` | `str` | `sample_dataset` | Field in `DataConfig` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `source` | `str` | `local` | Field in `DataConfig` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `sensitive_features` | `list` | `dynamic/default_factory` | Field in `DataConfig` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `intended_use` | `str` | `Demonstration and governance workflow validation` | Field in `DataConfig` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `limitations` | `str` | `Synthetic placeholders only; not production data` | Field in `DataConfig` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |

### `ModelConfig`
Configuration describing the model/system under evaluation.

| Variable | Type | Default | What It Is | Why It Is Important |
|---|---|---|---|---|
| `model_name` | `str` | `sample_model` | Field in `ModelConfig` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `version` | `str` | `0.1.0` | Field in `ModelConfig` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `owner` | `str` | `ml-team` | Field in `ModelConfig` used by toolkit workflows. | Assigns accountability for governance actions and follow-ups. |
| `task` | `str` | `classification` | Field in `ModelConfig` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `intended_use` | `str` | `Internal validation and risk documentation` | Field in `ModelConfig` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `limitations` | `str` | `Stub model behavior` | Field in `ModelConfig` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `known_failures` | `list` | `dynamic/default_factory` | Field in `ModelConfig` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |

### `EvalConfig`
Evaluation configuration for suite and metric execution.

| Variable | Type | Default | What It Is | Why It Is Important |
|---|---|---|---|---|
| `suites` | `list` | `dynamic/default_factory` | Field in `EvalConfig` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `metrics` | `list` | `dynamic/default_factory` | Field in `EvalConfig` used by toolkit workflows. | Drives quantitative quality and safety decisions. |
| `thresholds` | `dict` | `dynamic/default_factory` | Field in `EvalConfig` used by toolkit workflows. | Defines pass/fail gate criteria and release risk posture. |

### `XAIConfig`
Explainability artifact generation settings.

| Variable | Type | Default | What It Is | Why It Is Important |
|---|---|---|---|---|
| `reasoning_report_template` | `str` | `reasoning_report.md.j2` | Field in `XAIConfig` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `include_sections` | `list` | `dynamic/default_factory` | Field in `XAIConfig` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |

### `RedTeamConfig`
Red-team runner configuration.

| Variable | Type | Default | What It Is | Why It Is Important |
|---|---|---|---|---|
| `suites` | `list` | `dynamic/default_factory` | Field in `RedTeamConfig` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `cases` | `list` | `dynamic/default_factory` | Field in `RedTeamConfig` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `severity_threshold` | `Literal` | `high` | Field in `RedTeamConfig` used by toolkit workflows. | Defines pass/fail gate criteria and release risk posture. |

### `MonitoringConfig`
Monitoring and telemetry settings.

| Variable | Type | Default | What It Is | Why It Is Important |
|---|---|---|---|---|
| `enabled` | `bool` | `True` | Field in `MonitoringConfig` used by toolkit workflows. | Switches major pipeline behavior on/off for operations. |
| `telemetry_path` | `str` | `telemetry.jsonl` | Field in `MonitoringConfig` used by toolkit workflows. | Enables monitoring, anomaly detection, and post-run accountability. |
| `run_id` | `str | None` | None | Field in `MonitoringConfig` used by toolkit workflows. | Anchors traceability and governance scope across all artifacts. |

### `GovernanceConfig`
Governance controls and stage-gate rules by risk tier.

| Variable | Type | Default | What It Is | Why It Is Important |
|---|---|---|---|---|
| `risk_gate_rules` | `dict` | `dynamic/default_factory` | Field in `GovernanceConfig` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `required_stage_gates` | `list` | `dynamic/default_factory` | Field in `GovernanceConfig` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |

### `AdapterConfig`
Adapter settings for offline stubs and future provider integrations.

| Variable | Type | Default | What It Is | Why It Is Important |
|---|---|---|---|---|
| `provider` | `Literal` | `stub` | Field in `AdapterConfig` used by toolkit workflows. | Controls external model adapter behavior and integration boundaries. |
| `endpoint` | `str | None` | None | Field in `AdapterConfig` used by toolkit workflows. | Controls external model adapter behavior and integration boundaries. |
| `deployment` | `str | None` | None | Field in `AdapterConfig` used by toolkit workflows. | Controls external model adapter behavior and integration boundaries. |
| `api_version` | `str | None` | None | Field in `AdapterConfig` used by toolkit workflows. | Controls external model adapter behavior and integration boundaries. |
| `model` | `str | None` | None | Field in `AdapterConfig` used by toolkit workflows. | Controls external model adapter behavior and integration boundaries. |
| `timeout_seconds` | `int` | `30` | Field in `AdapterConfig` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |

### `ArtifactPolicyConfig`
Required outputs for evidence pack completeness checks.

| Variable | Type | Default | What It Is | Why It Is Important |
|---|---|---|---|---|
| `required_outputs_by_risk_tier` | `dict` | `dynamic/default_factory` | Field in `ArtifactPolicyConfig` used by toolkit workflows. | Determines evidence-pack completeness and auditability. |

### `MetricResult`
Individual metric output with threshold evaluation status.

| Variable | Type | Default | What It Is | Why It Is Important |
|---|---|---|---|---|
| `metric_id` | `str` | required | Field in `MetricResult` used by toolkit workflows. | Drives quantitative quality and safety decisions. |
| `value` | `float` | required | Field in `MetricResult` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `threshold` | `float | None` | None | Field in `MetricResult` used by toolkit workflows. | Defines pass/fail gate criteria and release risk posture. |
| `passed` | `bool | None` | None | Field in `MetricResult` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `details` | `dict` | `dynamic/default_factory` | Field in `MetricResult` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |

### `EvalResult`
Aggregate evaluation result payload.

| Variable | Type | Default | What It Is | Why It Is Important |
|---|---|---|---|---|
| `suite_name` | `str` | required | Field in `EvalResult` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `run_id` | `str` | required | Field in `EvalResult` used by toolkit workflows. | Anchors traceability and governance scope across all artifacts. |
| `started_at` | `datetime` | required | Field in `EvalResult` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `completed_at` | `datetime` | required | Field in `EvalResult` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `metric_results` | `list` | required | Field in `EvalResult` used by toolkit workflows. | Drives quantitative quality and safety decisions. |
| `overall_passed` | `bool` | required | Field in `EvalResult` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `notes` | `list` | `dynamic/default_factory` | Field in `EvalResult` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |

### `RedTeamFinding`
Security finding from an executed red-team case.

| Variable | Type | Default | What It Is | Why It Is Important |
|---|---|---|---|---|
| `case_id` | `str` | required | Field in `RedTeamFinding` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `severity` | `Literal` | required | Field in `RedTeamFinding` used by toolkit workflows. | Sets security escalation level and incident sensitivity. |
| `passed` | `bool` | required | Field in `RedTeamFinding` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `evidence` | `str` | required | Field in `RedTeamFinding` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `recommendation` | `str` | required | Field in `RedTeamFinding` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `tags` | `list` | `dynamic/default_factory` | Field in `RedTeamFinding` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |

### `Scorecard`
Governance scorecard summary contract.

| Variable | Type | Default | What It Is | Why It Is Important |
|---|---|---|---|---|
| `project_name` | `str` | required | Field in `Scorecard` used by toolkit workflows. | Anchors traceability and governance scope across all artifacts. |
| `run_id` | `str` | required | Field in `Scorecard` used by toolkit workflows. | Anchors traceability and governance scope across all artifacts. |
| `risk_tier` | `Literal` | required | Field in `Scorecard` used by toolkit workflows. | Anchors traceability and governance scope across all artifacts. |
| `overall_status` | `Literal` | required | Field in `Scorecard` used by toolkit workflows. | Represents governance decision state used for release control. |
| `go_no_go` | `Literal` | required | Field in `Scorecard` used by toolkit workflows. | Represents governance decision state used for release control. |
| `stage_gate_status` | `dict` | `dynamic/default_factory` | Field in `Scorecard` used by toolkit workflows. | Represents governance decision state used for release control. |
| `evidence_completeness` | `float` | `0.0` | Field in `Scorecard` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `metric_results` | `list` | `dynamic/default_factory` | Field in `Scorecard` used by toolkit workflows. | Drives quantitative quality and safety decisions. |
| `redteam_summary` | `dict` | `dynamic/default_factory` | Field in `Scorecard` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `required_actions` | `list` | `dynamic/default_factory` | Field in `Scorecard` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `artifact_links` | `dict` | `dynamic/default_factory` | Field in `Scorecard` used by toolkit workflows. | Determines evidence-pack completeness and auditability. |

### `TelemetryEvent`
Event emitted by monitoring logger as JSONL.

| Variable | Type | Default | What It Is | Why It Is Important |
|---|---|---|---|---|
| `timestamp` | `datetime` | required | Field in `TelemetryEvent` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `run_id` | `str` | required | Field in `TelemetryEvent` used by toolkit workflows. | Anchors traceability and governance scope across all artifacts. |
| `event_type` | `Literal` | required | Field in `TelemetryEvent` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `component` | `str` | required | Field in `TelemetryEvent` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `metadata` | `dict` | `dynamic/default_factory` | Field in `TelemetryEvent` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |

### `SystemSpec`
System metadata used for evaluation and governance.

| Variable | Type | Default | What It Is | Why It Is Important |
|---|---|---|---|---|
| `system_name` | `str` | required | Field in `SystemSpec` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `owner` | `str` | required | Field in `SystemSpec` used by toolkit workflows. | Assigns accountability for governance actions and follow-ups. |
| `risk_tier` | `Literal` | required | Field in `SystemSpec` used by toolkit workflows. | Anchors traceability and governance scope across all artifacts. |
| `intended_use` | `str` | required | Field in `SystemSpec` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `constraints` | `list` | `dynamic/default_factory` | Field in `SystemSpec` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |

### `TestCase`
Evaluation or red-team test case contract.

| Variable | Type | Default | What It Is | Why It Is Important |
|---|---|---|---|---|
| `case_id` | `str` | required | Field in `TestCase` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `prompt` | `str` | required | Field in `TestCase` used by toolkit workflows. | Captures model interaction context for reproducibility and review. |
| `expected_behavior` | `str` | required | Field in `TestCase` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `category` | `str` | required | Field in `TestCase` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `risk_tier` | `Literal` | `medium` | Field in `TestCase` used by toolkit workflows. | Anchors traceability and governance scope across all artifacts. |
| `tags` | `list` | `dynamic/default_factory` | Field in `TestCase` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |

### `LineageNode`
One lineage/source node used by generated outputs.

| Variable | Type | Default | What It Is | Why It Is Important |
|---|---|---|---|---|
| `node_id` | `str` | required | Field in `LineageNode` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `source_type` | `Literal` | required | Field in `LineageNode` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `title` | `str` | required | Field in `LineageNode` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `uri` | `str | None` | None | Field in `LineageNode` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `used_for` | `str` | `context` | Field in `LineageNode` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |

### `LineageReport`
Lineage report payload for explainability artifacts.

| Variable | Type | Default | What It Is | Why It Is Important |
|---|---|---|---|---|
| `run_id` | `str` | required | Field in `LineageReport` used by toolkit workflows. | Anchors traceability and governance scope across all artifacts. |
| `prompt` | `str` | required | Field in `LineageReport` used by toolkit workflows. | Captures model interaction context for reproducibility and review. |
| `model_output` | `str` | required | Field in `LineageReport` used by toolkit workflows. | Determines evidence-pack completeness and auditability. |
| `nodes` | `list` | `dynamic/default_factory` | Field in `LineageReport` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `citation_coverage` | `float` | `0.0` | Field in `LineageReport` used by toolkit workflows. | Supports trust, explainability, and responsible AI evidence claims. |
| `transparency_risk` | `Literal` | `medium` | Field in `LineageReport` used by toolkit workflows. | Supports trust, explainability, and responsible AI evidence claims. |

### `AuthoritativeSource`
Approved source entry for authoritative data index.

| Variable | Type | Default | What It Is | Why It Is Important |
|---|---|---|---|---|
| `source_id` | `str` | required | Field in `AuthoritativeSource` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `name` | `str` | required | Field in `AuthoritativeSource` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `owner` | `str` | `unknown` | Field in `AuthoritativeSource` used by toolkit workflows. | Assigns accountability for governance actions and follow-ups. |
| `classification` | `Literal` | `internal` | Field in `AuthoritativeSource` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `uri` | `str | None` | None | Field in `AuthoritativeSource` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `approved` | `bool` | `True` | Field in `AuthoritativeSource` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |

### `ArtifactManifestItem`
One manifest record for an artifact in a run directory.

| Variable | Type | Default | What It Is | Why It Is Important |
|---|---|---|---|---|
| `path` | `str` | required | Field in `ArtifactManifestItem` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `sha256` | `str` | required | Field in `ArtifactManifestItem` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `size_bytes` | `int` | required | Field in `ArtifactManifestItem` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `modified_at` | `datetime` | required | Field in `ArtifactManifestItem` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |

### `ArtifactManifest`
Manifest of generated run artifacts.

| Variable | Type | Default | What It Is | Why It Is Important |
|---|---|---|---|---|
| `run_id` | `str` | required | Field in `ArtifactManifest` used by toolkit workflows. | Anchors traceability and governance scope across all artifacts. |
| `generated_at` | `datetime` | required | Field in `ArtifactManifest` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `items` | `list` | `dynamic/default_factory` | Field in `ArtifactManifest` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `required_outputs` | `list` | `dynamic/default_factory` | Field in `ArtifactManifest` used by toolkit workflows. | Determines evidence-pack completeness and auditability. |
| `completeness` | `float` | `0.0` | Field in `ArtifactManifest` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |

### `IncidentRecord`
Incident record contract for threshold breaches.

| Variable | Type | Default | What It Is | Why It Is Important |
|---|---|---|---|---|
| `incident_id` | `str` | required | Field in `IncidentRecord` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `run_id` | `str` | required | Field in `IncidentRecord` used by toolkit workflows. | Anchors traceability and governance scope across all artifacts. |
| `severity` | `Literal` | required | Field in `IncidentRecord` used by toolkit workflows. | Sets security escalation level and incident sensitivity. |
| `trigger` | `str` | required | Field in `IncidentRecord` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `summary` | `str` | required | Field in `IncidentRecord` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `containment_action` | `str` | required | Field in `IncidentRecord` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `owner` | `str` | `incident-commander` | Field in `IncidentRecord` used by toolkit workflows. | Assigns accountability for governance actions and follow-ups. |
| `due_date` | `str` | `TBD` | Field in `IncidentRecord` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `status` | `Literal` | `open` | Field in `IncidentRecord` used by toolkit workflows. | Represents governance decision state used for release control. |
| `related_artifacts` | `list` | `dynamic/default_factory` | Field in `IncidentRecord` used by toolkit workflows. | Determines evidence-pack completeness and auditability. |

### `MonitoringSummary`
Aggregated telemetry metrics for one run.

| Variable | Type | Default | What It Is | Why It Is Important |
|---|---|---|---|---|
| `run_id` | `str` | required | Field in `MonitoringSummary` used by toolkit workflows. | Anchors traceability and governance scope across all artifacts. |
| `total_events` | `int` | required | Field in `MonitoringSummary` used by toolkit workflows. | Enables monitoring, anomaly detection, and post-run accountability. |
| `events_by_type` | `dict` | `dynamic/default_factory` | Field in `MonitoringSummary` used by toolkit workflows. | Enables monitoring, anomaly detection, and post-run accountability. |
| `events_by_component` | `dict` | `dynamic/default_factory` | Field in `MonitoringSummary` used by toolkit workflows. | Enables monitoring, anomaly detection, and post-run accountability. |
| `metric_failure_rate` | `float` | `0.0` | Field in `MonitoringSummary` used by toolkit workflows. | Drives quantitative quality and safety decisions. |
| `anomaly_flags` | `list` | `dynamic/default_factory` | Field in `MonitoringSummary` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |

### `StageGateDecision`
Stage-gate evaluation contract used in scorecards.

| Variable | Type | Default | What It Is | Why It Is Important |
|---|---|---|---|---|
| `gate` | `str` | required | Field in `StageGateDecision` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |
| `status` | `Literal` | required | Field in `StageGateDecision` used by toolkit workflows. | Represents governance decision state used for release control. |
| `rationale` | `str` | required | Field in `StageGateDecision` used by toolkit workflows. | Provides required context used by pipeline components and governance checks. |

