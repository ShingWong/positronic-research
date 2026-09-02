# 50 — Appendix: harness wiring, run history, worked example

> **Status:** reference material. Fill run-history counts from the results dir.

## Harness wiring

- **Main driver**: `consumers/benchmarks/suites/longmemeval/real_driver.py`
  - `--n 50 --profile archival --embed local --judge --context 1 --answer-model <id>`
  - Writes per-question brains to `results/<run>/tmp-{idx}/` + `metrics.json`,
    `details.json`, `report.md`, `run.log`.
- **Cookoff**: `consumers/benchmarks/model_panel.py`
  - Reuses saved brains with `context_window=1`; calls the model panel with the
    same retrieved context; exact-substring judged; writes a JSON summary.
- **Retrieval isolation**: gold-presence check in `model_panel.py` / analyzed
  in `real_driver` details (`recall_hit`).

## Run history (n=50, 10+ executions)

| run | profile | embed | judge | acc_with | acc_without | note |
|---|---|---:|---|---:|---:|---|
| run-50-balanced-lexical | balanced | lexical | none | 1.0 | 0.0 | pilot |
| run-50-long_term-lexical | long_term | lexical | none | 1.0 | 0.0 | pilot |
| run-50-balanced-local | balanced | local | none | 0.0 | 0.0 | pilot (embed ingest issue) |
| run-50-balanced-lexical-judged | balanced | lexical | 70b | 0.1 | 0.1 | judge artifact |
| fix-recheck | archival | local | 70b | 0.58 | 0.10 | reproduced paper |
| final-context1 | archival | local | 70b | _PENDING_ | _PENDING_ | deepseek + context_window=1 |

(Full listing in `consumers/benchmarks/results/longmemeval/`.)

## The failure taxonomy, discovered live

1. muse-spark empty answers (5/50) — model defect, verified by re-call.
2. Premise-outranks-answer retrieval artifact — fixed by `context_window`.
3. Extraction-miss on gold-in-context (Q17) — the model-fitness signal.

## Q17 full trace (the worked example)

- **Question**: "What did I buy for my sister's birthday gift?"
- **Gold**: `a yellow dress`
- **Retrieval (context_window=1)**: hit0 snippet — "For my sister's birthday,
  I got her a yellow dress and a pair of earrings to match." → gold present.
- **Answer (deepseek-v4-flash)**: missed → extraction-miss, attributed to model.
- **Why it matters**: this is a case where retrieval is *provably* correct and
  the model still fails — the exact class PRISM isolates.

## Latency evidence

- Live kairos brain (~10k episodes): `activate` mean 8.9 ms, min 3.4 ms,
  max 28.7 ms (5 query shapes incl. event-defined-interval).
- henry brain (spinning disks, retired server): similar interval query
  < 500 ms (reported from development session).

## Reproducibility

- Dataset blob: cached `xiaowu0162/longmemeval longmemeval_s`.
- Engine: `ENGRAM_TAG`-pinned; `context_window` + `consolidation` live in
  `positronic-engram/engine/src/memeng`.
- No PII: all run data under `consumers/benchmarks/results/` (gitignored).