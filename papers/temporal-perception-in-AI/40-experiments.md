# Experiment Designs

> All experiments run on the continuously-observing game-agent fleet
> (17 sessions). Judge model: MI50 deep brain (thinking-on, blind to
> condition). Prerequisite: Phase-0 episode-capture pipeline (gt-spector).

## E1 — Headline: τ-keyed vs wall-clock-keyed memory (H-τ)

Replay an identical episode corpus through two stores differing ONLY in the
time axis driving decay/reinforcement/consolidation cadence:
  A) wall-clock t (MemoryBank-style R = e^(−t/S))
  B) τ = ∫ novelty-density dt (agent-native)
Probe both with decision scenarios requiring relevant history, sampled from
quiet stretches AND event-dense stretches of equal wall duration.
Metric: decision quality vs ground truth + probe answers graded blind.
**Claim at stake:** re-derived time outperforms borrowed time.

## E2 — Texture-primary vs date-range retrieval (H1, H3)

Human-style probes: "what usually happens when…", "around the first raid
loss…", "that cold-morning-like stretch…". Compare texture/anchor-keyed store
vs timestamp-indexed store on probe-answer quality + cluster-recall coverage.

## E3 — Storage dynamics under salience tiers & schema fusion (H2, H4)

Measure: storage growth curve (expect ~log under fusion), survival rates by
salience tier across consolidation rounds (flashbulb tier exempt), and
"what usually happens" quality gains vs per-instance recall of routine events.

## E4 — Constellation recall dynamics (H10)

Free-recall probes; analyze output sequence structure: does it follow anchor-
constellation adjacency (ours) vs embedding-similarity rank (control)?
Metric: adjacency-adherence of recall order; human-judged coherence.

## E5 — Provenance & the wake-up ritual (H11–H13)

Forced-gap A/B: cold restart vs digest+wake-up-ritual restart, gaps injected
across quiet/eventful periods. Metrics: stale-belief error rate (beliefs
contradicted by events during gap), provenance-weighted decision quality,
re-orientation latency to first correct decision.

## E6 — Interval calibration (H9)

Reported fuzzy-interval widths vs actual temporal error on reconstructable
ground-truth events. Expect width ∝ error (scalar variability analog);
calibration curve is itself a result.

## Infrastructure prerequisites

1. Episode capture hook in gt-spector monitor loop (JSONL per bot/day):
   dual stamps (wall + mono), regime tags, screen-state context, action,
   outcome, salience features (novelty vs nav-table, prediction-error proxy).
2. Anchor detection: salience threshold + explicit event markers (season
   resets, event launches, firsts, losses).
3. τ meter: online novelty-density estimate (rolling prediction-error over
   detect_screen classifications).
4. Probe suite authoring: ~200 human-style temporal-memory probes with
   ground-truth labels from session logs.

## E7 + External Benchmarks — harness at `consumers/benchmarks`

Pilot validation harness `consumers/benchmarks` (umbrella plain folder, isolated tmp DBs,
PII-firewalled, `ENGRAM_TAG=v0.2.0`). Shared `harness/adapter.py`
(`BenchmarkAdapter` → `SQLiteStore`+`MemoryEngine` per-domain `retention_profile`,
`engine.py:48` balanced|archival|long_term|short_term, `prune(tau_now)` ladder
`0.35→day_token` `0.05→expired`). Suites:

- `suites/longmemeval` — Wu et al. 2024 `2410.10813`, HF `THUDM/LongMemEval`
  (500 sessions, avg 115k tok, 5 question types). Pilot `n=5|50` synthetic
  (unique tokens, `recall@1=1.0` expected, lexical `p95 <2ms`); full `500`
  via `datasets` fetch deferred until pilot+ E7 gate.
- `suites/synthetic_e7` — E7 replication (`45-pilot-mail-cognition.md:231`):
  same 55 synthetic events over 78 weeks, weekly `prune` cadence, final survival
  archival `55` / long_term `55` / balanced `35` / short_term `7`
  (`0603bf8` + harness gate `tests/test_synthetic_e7.py`). `--real` replays
  `positronic-private/brain_henry/state/index.jsonl` if present (otherwise synthetic).
- `suites/locomo` — Maharana et al. ACL'24 (10×600-turn dialogues) deferred.

Outputs `results/{suite}/run-*/metrics.json` + `report.md` (paper + pitch).
Plan: `docs/superpowers/plans/2026-08-29-positronic-benchmarks.md`.
