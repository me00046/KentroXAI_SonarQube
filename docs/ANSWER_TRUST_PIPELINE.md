# Answer Trust Pipeline

This document explains the main runtime path for the answer-level trust card.

## Flow

1. `tat run simulate` builds a prompt and optionally injects retrieved context.
2. `model_client.invoke_model(...)` calls the configured provider.
3. The run writes `prompt_run.json` and `model_response.json`.
4. `run_eval(...)` computes metric results from:
   - prompt
   - model output
   - retrieved contexts
   - optional fairness and labeled-eval payloads
   - optional embeddings
5. `generate_scorecard(...)` converts metric outputs into:
   - answer-level verdict
   - answer trust score
   - governance status
   - historical trust z-score
6. The run writes the rendered trust card and supporting artifacts.

## Key Concepts

### Answer Verdict

The answer verdict is user-facing and answers:

- `trusted`
- `use_caution`
- `not_trusted`

It is based primarily on answer-level truth signals such as:

- `claim_support_rate`
- `unsupported_claim_rate`
- `contradiction_rate`
- `evidence_sufficiency_score`

### Governance Status

The governance status is release-facing and answers:

- did the overall governed system pass all required gates?

It can fail even when the answer verdict is `trusted`.

### Trust Score

`trust_score` is a historical z-style comparison against prior runs in the same
cohort. Cohorts are split by:

- deployment risk tier
- task
- effective generation model

This keeps OpenAI runs separate from prior Ollama baselines.

## Important Files

- `src/trusted_ai_toolkit/cli.py`
- `src/trusted_ai_toolkit/model_client.py`
- `src/trusted_ai_toolkit/eval/runner.py`
- `src/trusted_ai_toolkit/eval/metrics/__init__.py`
- `src/trusted_ai_toolkit/reporting.py`
- `src/trusted_ai_toolkit/benchmarking.py`

## Artifact Outputs

Important run artifacts:

- `prompt_run.json`
- `model_response.json`
- `embedding_trace.json`
- `eval_results.json`
- `scorecard.json`
- `scorecard.html`
- `benchmark_summary.json`

## Engineering Notes

- Comments are intentionally focused on non-obvious logic.
- The codebase avoids line-by-line commentary because that tends to drift and
  make the scoring logic harder to audit.
