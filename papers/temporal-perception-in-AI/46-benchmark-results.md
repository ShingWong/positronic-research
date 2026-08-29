# Benchmark Results — E7 Retention + LongMemEval / RULER Pilots (Draft, not for arXiv)

> **Status:** local draft — refine before any upload. `consumers/benchmarks` pilots are
> harness-validation unless marked **credible** (real `xiaowu0162/longmemeval` `500` cached `278M` + `BGE :8090` `local` + `Muse Spark 1.2` answer + `70b` judge).

## 1. E7 — Identical Experience, Divergent Forgetting (Credible, main paper Fig)

Four brains, same 55 messages over 78 weeks (`2007-08→2009-01`), weekly `prune(tau_now)` ladder
`0.35→day_token 0.05→expired` `engine.py:443` per `retention_profile` `archival|long_term|balanced|short_term`
(`S_base 1e6/120/30/6` + `S_arousal 0-40` `engine.py:48`).

| profile | episodes alive @ wk78 | expired | day_merged | strength at arousal 0 |
|---|---:|---:|---:|---:|
| archival | 55 | 0 | 0 | 1e6 |
| long_term | 55 | 0 | 0 | 120 |
| balanced | 35 | 0 | 20 | 30 |
| short_term | 7 | 35 | 13 | 6 |

*First divergence* wk36 (`short_term` froze at 7 during `Liqui-Fire` burst), *second* wk53-54
(`balanced` reabsorbing `Genesis-stuff`). `long_term==archival` at `Δτ≈49.9` expected until `Δτ/S→1`.
`CONTROL` object formation identical (37 objects) — profiles affect only forgetting.
Gated by `tests/test_synthetic_e7.py:test_synthetic_e7_replicates_55_55_35_7` `55/55/35/7`.
Full replication `consumers/benchmarks/suites/synthetic_e7/driver.py` (`per-message` `arousal 0`, same weekly cadence as
`positronic-private/brain_henry/experiment_profiles.py`). Real `--real` replay of `index.jsonl` window planned as sensitivity `±2`.

Paper claim: **application-knob thesis** — same hardware, different policy.

## 2. Harness Validation — Synthetic Pilots (Not for paper, Appendix harness proof)

Isolated `tmp DB` per-question `harness/adapter.py` (`BenchmarkAdapter` → `SQLiteStore`+`MemoryEngine` per-domain `retention_profile`
+ batch `BGE` `512tok` `2000char` truncate + per-message chunking `550 msgs/54 sessions`).

| suite | n | embed | episodes | recall | fallback_rate | mean_rrf | p95 | tokens with/without | ratio |
|---|---:|---|---|---:|---:|---:|---:|---:|---:|
| `longmemeval` synthetic | 50 | lexical `FTS 0.5ms` | 50 | 1.0 | 0.0 | 0.016 | 0.7ms | 242 / 4496 | 0.05 |
| `ruler` synthetic `32k` `72k chars` | 5 | lexical | 550 `per-msg` | 1.0 | 0.0 | 0.016 | 1.6ms | 242 / 4496 | 0.05 |
| `ruler` profiles | 5 | `balanced==archival==long_term` | — | 1.0 invariant | 0.0 | — | — | — | expected null at `Δτ<5` |

*Why not paper:* synthetic `pilot{i:03d}` / `needle{i:04d}` unique tokens → `FTS` tautology. Tests `tests/test_longmemeval_pilot.py`,
`tests/test_ruler.py`, `tests/test_adapter.py` gate `domain retention` wiring + `fallback False` + `k truncation` + `profile invariance`
(`14 passed 1 skipped`), not external validity.

## 3. Real LongMemEval Spot Checks — `xiaowu0162/longmemeval` `longmemeval_s` 500 (Preliminary, refine before claim)

Cached blob `08d8dad...` `500` `6 types` `single-session-user 70` `multi-session 133` `temporal-reasoning 133` `knowledge-update 78`
`avg 115k tok` `~500 msgs` haystack per question. Per-message events preserve gold tail
(`session body[:8000]` head `0.31` vs tail `0.49` vs per-msg `0.59` `sim` to `What degree...` `BGE :8090 1024d`).

| q idx | type | Q | lexical `550 msgs` | local `BGE :8090` `511/550 embeds` batch 32 |
|---|---|---|---|---|
| 0 | single-session-user | What degree did I graduate with? (`Business Administration`) | `hits 8 fallback True has_gold False` `1.25s` | `hits 8 fallback False has_gold True` `27.8s` `rrf 0.0197` |
| 1 | single-session-user | How long is daily commute? (`45 min`) | `fallback True has_gold False` | `fallback False has_gold True` `rrf 0.0197` |
| 6 | single-session-user | Where do I take yoga? (`Serenity Yoga`) | `has_gold True` (lexical hit on `yoga`) | `has_gold True` |

*Diagnosis:* session-level `FTS` `What degree... →0` `degree→2` `Business→1`; `BGE` `batch 512tok` limit `938tok` `500 err` killed `7/54` embeds until
`truncate 2000char` + batch chunking fixed `44→511/550` embeddings, gold `rank 22 @0.31 → rank 1 @0.59`.

*Next gate before arXiv:* `lexical vs local` per-message `n=10` `--no-judge` `recall_proxy + fallback_rate + p95`
(then `n=50` `Muse Spark 1.2` `1024tok` answer + `70b` `llm_judge` `YES/NO` `hybrid` vs `without=full 30k chars` `acc_with vs acc_without delta + per_type`).
`404` for `llama-3.1-405b-instruct` on OpenRouter → default judge `meta-llama/llama-3.3-70b-instruct` (`hybrid` exact fallback).
Requires `OPENROUTER_API_KEY` `set` `73ch` `cost ~$0.002/10q` `70b`.

## 4. RULER 32k Efficiency (Preliminary, Appendix + pitch, not retention)

`consumers/benchmarks/suites/ruler` `NIAH` `4k/8k/16k/32k` `per-message` `32k→72k chars` `batch BGE` `tokens_with ~242` vs `without ~4496`
`1/20` headline, `1/16th` at `32k top-8`. Primary retention stays `E7` + `LongMemEval 500`; `RULER` labeled **efficiency Appendix**.

## 5. What is still validation-only

Need `n=50` real `balanced vs long_term` `lexical vs local` `recall + fallback 0.0 + mean_rrf` + `Muse Spark` `70b` `accuracy` vs `RAG top-8` baseline
to quote `Wu Table 3 GPT-4o 0.45` comparison. Current `1.0`s prove brain wiring, not toughest-memory claim.

Refs: `consumers/benchmarks/README.md`, `harness/judge.py` (`70b` `YES/NO`), `suites/longmemeval/real_driver.py` (`--judge-model` `--answer-model` `--judge-mode hybrid|exact|llm`).
