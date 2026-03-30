"""Versioned deterministic control library for scorecard decisions."""

from __future__ import annotations

import re

from tat.controls.models import Control
from tat.schemas import SystemSpec
from tat.schemas.system_spec import SEMVER_PATTERN


def _metadata_has(system: SystemSpec, key: str) -> bool:
    value = system.metadata.get(key)
    return isinstance(value, str) and bool(value.strip())


def get_controls_v0() -> list[Control]:
    """Return the v0 deterministic control set."""

    return [
        Control(
            control_id="SEC-01",
            pillar="security",
            severity="high",
            description="Production deployments must declare a known model provider.",
            evaluator=lambda system: (
                (system.environment != "production" or system.model_provider.strip().lower() != "unknown"),
                "Production systems must not use an unknown model provider."
                if system.environment == "production"
                else "Non-production deployment; provider allowlist check not required.",
            ),
        ),
        Control(
            control_id="SEC-02",
            pillar="security",
            severity="high",
            description="Critical-risk systems cannot use the internal compliance profile.",
            evaluator=lambda system: (
                (system.risk_level != "critical" or system.compliance_profile != "internal"),
                "Critical-risk systems require a regulated or restricted compliance profile."
                if system.risk_level == "critical"
                else "Compliance profile is acceptable for the declared risk level.",
            ),
        ),
        Control(
            control_id="SEC-03",
            pillar="security",
            severity="medium",
            description="Regulated systems should classify data in metadata.",
            evaluator=lambda system: (
                (
                    system.compliance_profile not in {"regulated", "restricted"}
                    or _metadata_has(system, "data_classification")
                ),
                "Regulated or restricted systems must declare metadata.data_classification."
                if system.compliance_profile in {"regulated", "restricted"}
                else "Data classification metadata not required for the current compliance profile.",
            ),
        ),
        Control(
            control_id="REL-01",
            pillar="reliability",
            severity="low",
            description="The declared spec version must remain valid semantic versioning.",
            evaluator=lambda system: (
                bool(re.fullmatch(SEMVER_PATTERN, system.version)),
                "System specification version is valid semantic versioning.",
            ),
        ),
        Control(
            control_id="REL-02",
            pillar="reliability",
            severity="medium",
            description="Production systems must pin a model version.",
            evaluator=lambda system: (
                (system.environment != "production" or bool(system.model_version.strip())),
                "Production systems must define a non-empty model_version."
                if system.environment == "production"
                else "Non-production deployment; strict model version pinning not required.",
            ),
        ),
        Control(
            control_id="REL-03",
            pillar="reliability",
            severity="low",
            description="Deployments should declare a non-local runtime region.",
            evaluator=lambda system: (
                system.deployment_region.strip().lower() not in {"", "local", "localhost"},
                "Deployment region must be a non-local identifier.",
            ),
        ),
        Control(
            control_id="TRN-01",
            pillar="transparency",
            severity="medium",
            description="Systems should declare intended use metadata.",
            evaluator=lambda system: (
                _metadata_has(system, "intended_use"),
                "metadata.intended_use is required for traceable system intent.",
            ),
        ),
        Control(
            control_id="TRN-02",
            pillar="transparency",
            severity="low",
            description="Non-low-risk systems should declare known limitations.",
            evaluator=lambda system: (
                (system.risk_level == "low" or _metadata_has(system, "limitations")),
                "metadata.limitations is required when risk_level is medium or higher."
                if system.risk_level != "low"
                else "Limitations metadata is optional for low-risk systems.",
            ),
        ),
        Control(
            control_id="TRN-03",
            pillar="transparency",
            severity="low",
            description="Production changes should reference a change ticket.",
            evaluator=lambda system: (
                (system.environment != "production" or _metadata_has(system, "change_ticket")),
                "Production systems must include metadata.change_ticket for traceability."
                if system.environment == "production"
                else "Change ticket metadata not required outside production.",
            ),
        ),
        Control(
            control_id="GOV-01",
            pillar="governance",
            severity="high",
            description="Production systems require at least standard telemetry.",
            evaluator=lambda system: (
                (system.environment != "production" or system.telemetry_level in {"standard", "enhanced"}),
                "Production systems require telemetry_level standard or enhanced."
                if system.environment == "production"
                else "Minimal telemetry is acceptable outside production.",
            ),
        ),
        Control(
            control_id="GOV-02",
            pillar="governance",
            severity="medium",
            description="High-risk systems require enhanced telemetry.",
            evaluator=lambda system: (
                (system.risk_level not in {"high", "critical"} or system.telemetry_level == "enhanced"),
                "High and critical systems require telemetry_level enhanced."
                if system.risk_level in {"high", "critical"}
                else "Enhanced telemetry not required for the declared risk level.",
            ),
        ),
        Control(
            control_id="GOV-03",
            pillar="governance",
            severity="high",
            description="Restricted systems must not remain in development.",
            evaluator=lambda system: (
                (system.compliance_profile != "restricted" or system.environment != "development"),
                "Restricted systems cannot be designated as development environments."
                if system.compliance_profile == "restricted"
                else "Environment is acceptable for the current compliance profile.",
            ),
        ),
    ]
