# 20 — Results (placeholders — fill from `final-context1` + cookoff)

> **Status:** tables are templates. Populate when the main n=50 run and the
> model cookoff complete. All measurements serve the goal: **model fitness for
> positronic, on a non-failing memory substrate.**

## 1. Gold-presence (retrieval isolation)

| metric | value | meaning |
|---|---|---|
| gold present in top-8 (context_window=1) | _PENDING_ | should be 50/50 — retrieval non-failing |
| retrieval-miss count | _PENDING_ | expected 0 |

## 2. Main run — deepseek-v4-flash, n=50

| metric | value |
|---|---|
| acc_with | _PENDING_ |
| acc_without (30k truncated haystack) | _PENDING_ |
| delta | _PENDING_ |
| fallback_rate | _PENDING_ |
| floor (secured if all remaining fail) | _PENDING_ |

## 3. Model cookoff — per-model accuracy on identical retrieval

| model | acc | extraction-miss | empty-answer | error |
|---|---:|---:|---:|---:|
| deepseek-v4-flash | | | | |
| deepseek-v4-pro | | | | |
| glm-5.3-flash | | | | |
| qwen3.8-flash | | | | |
| kimi-k3 | | | | |
| gemini-3.7-flash | | | | |

## 4. Failure taxonomy (all models pooled)

| class | count | % |
|---|---:|---:|
| retrieval-miss | | |
| extraction-miss | | |
| empty-answer | | |
| error | | |

## 5. Worked example detail

| Q | question | gold | in-context | model | verdict |
|---|---|---|---|---|---|
| 17 | sister's birthday gift | a yellow dress | yes | deepseek-v4-flash | extraction-miss |
| ... | | | | | |

## 6. Run history (methodology evidence)

n=50 executed 10+ times across profiles, embed tiers, judge modes — see
`50-appendix.md`. The `fix-recheck` archival/local run reproduced the paper's
0.58/0.10; the `final-context1` run (deepseek + context_window=1) is the
headline: **0.90/0.12, Δ0.78**.

## 7. E1 decay ablation — τ-decay vs wall-clock decay (the decisive test)

The reviewer's core objection was that Δ0.78 (LongMemEval) compares semantic
retrieval against a blind window, not τ-decay against wall-clock decay. This
2×2 experiment answers that directly: identical streams through two engines
differing **only in the clock** driving the prune ladder.

Full protocol + code in `experiments/decay_ablation/` (driver.py,
test_decay_ablation.py, report.md). Engine `decay_axis` flag in
`positronic-engram` (`prune`, committed `5fe495a`).

| Stream | Metric | τ-decay | Wall-decay | Insight |
|---|---|---|---|---|
| Uniform (control) | Retention | 35/55 | 35/55 | Calibrated scale parity |
| Uniform (control) | Retrieval | 1.00 | 1.00 | Baseline parity |
| Burst-quiet (stress) | Retention | **35/55** | **0/55** | Wall over-prunes dormant contexts |
| Burst-quiet (stress) | Retrieval | **1.00** | **0.00** | τ keeps memory answerable; wall loses it |

On equal-wall-duration eventful-then-quiet stretches, wall-clock decay purges
the entire burst (0/55) while τ-decay preserves it (35/55, retrievable 1.00).
This is D6/E1 made measurable: **the thesis directly tested, not inferred.**