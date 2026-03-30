# Scorecard Data Backing and Interpretation (Current Architecture)

## Purpose
Explain what the scorecard is actually backed by, what is still proxy-backed, and how to interpret the headline Trust Score relative to release decisions.

## Bottom Line
- Release outcomes (`go/no-go`) are driven by stage gates in `reporting.py`.
- The visible Trust Score is a presentation score built from a control-backed baseline plus penalties.
- Some metric inputs are still placeholders (known prototype limitation).

## 1) Data Sources Used by the Scorecard

Primary source file:
- `src/trusted_ai_toolkit/reporting.py`

Scorecard combines:
1. Evaluation metrics (`eval_results.json`)
2. Red-team findings (`redteam_findings.json`)
3. Controls evaluated from `config.system`
4. Evidence completeness from required artifact presence
5. Telemetry/monitoring and incident context

## 2) Authoritative Decision Path (Release Logic)

Stage gates:
- `evaluation`: fail if any metric failed
- `redteam`: needs review for blocker findings; can escalate to fail by risk rule
- `documentation`: pass when completeness >= 90, else needs_review
- `monitoring`: pass (current behavior)
- `human_signoff`: needs_review when required by risk tier

Decision:
- any `fail` -> `overall_status=fail`, `go_no_go=no-go`
- else any `needs_review` -> `overall_status=needs_review`, `go_no_go=no-go`
- else -> `overall_status=pass`, `go_no_go=go`

This path is the compliance/release authority.

## 3) Trust Baseline (Control-Backed)

Source:
- `src/tat/controls/scoring.py`

Flow:
1. Run deterministic controls over `config.system`
2. Compute pillar scores (`security`, `reliability`, `transparency`, `governance`)
3. Compute weighted trust baseline

Weights:
- security: `0.30`
- reliability: `0.30`
- transparency: `0.25`
- governance: `0.15`

Security pillar nuance:
- blended with red-team pass rate (`50% controls + 50% red-team`) when red-team summary is available.

## 4) Displayed Trust Score (Card Number)

Source:
- `src/trusted_ai_toolkit/reporting.py` (`_card_score_summary`)

Displayed score formula:
- `base = control_score_pct` if available, else `70`
- penalties:
  - `failed_metrics * 6.0`
  - `medium_findings * 2.0`
  - `high_findings * 8.0`
  - `critical_findings * 12.0`
  - `max(0, 90 - evidence_completeness) * 0.15`
- `display_score = clamp(round(base - penalty), 0, 100)`

Interpretation:
- This score is meant for readability and trend signaling.
- It is intentionally coupled to governance signals, but it is not the release gate itself.

## 5) What Is Strongly Backed vs Proxy-Backed

Strongly backed:
- Stage-gate logic
- Control evaluation and weighting
- Red-team severity and pass-rate summary
- Evidence completeness and artifact manifesting

Proxy-backed / prototype-level:
- Stub evaluation metrics (`accuracy_stub`, `reliability`, `groundedness_stub`)
- Safety proxies derived from suite composition (`refusal_correctness`, `unanswerable_handling`)
- Fairness metrics currently run on synthetic cohort arrays

## 6) Recommended Reading Order for Any Scorecard

1. `overall_status`
2. `go_no_go`
3. failed/needs_review stage gates
4. required actions
5. pillar and control context
6. displayed Trust Score

This order prevents over-weighting the headline score.

## 7) Safe Demo Statement

Use this statement:

`The scorecard uses real gate and control logic over real run artifacts; some metric inputs are still proxy-backed, so it should be treated as governance workflow evidence rather than final production assurance.`

## Source of Truth Files

- `src/trusted_ai_toolkit/reporting.py`
- `src/tat/controls/scoring.py`
- `src/tat/controls/library.py`
- `src/trusted_ai_toolkit/eval/runner.py`
- `src/trusted_ai_toolkit/eval/metrics/__init__.py`
- `src/trusted_ai_toolkit/templates/scorecard.html.j2`
