# AAAI-26 arXiv — Option B Gated Submission + Landing Page

> **Goal:** AAAI/IJCAI `cs.AI` primary `cs.CL`+`cs.NE` arXiv-ready paper gated on real `n=50` LongMemEval evidence, built with `aaai2026.sty` `letterpaper` `submission`, parallel landing page. Ship v1 fast after gate, v2 with `n=500`.
> **Status:** Spec — Option B approved 2026-08-29. Inherits `papers/temporal-perception-in-AI/00-outline.md` 10-section map, `30-related-work.md` 33 sources, `46-benchmark-results.md` maturity gates.
> **Style:** `aaai2026.sty 12K` `aaai2026.bst 30K` from `https://raw.githubusercontent.com/NousResearch/hermes-agent/HEAD/skills/research/research-paper-writing/templates/aaai2026/` (mirrors `https://aaai.org/authorkit26/`). `hyperref` forbidden.

## Decisions Locked

- **Approach:** Option B — gate writing on real `n=50` LongMemEval `balanced vs long_term` × `lexical vs local` + `70b` judge `acc_with vs acc_without Δ` per-type, with E7 `55/55/35/7` as co-primary figure. Option A (synthetic-only) explicitly deferred to appendix; Option C (new τ-vs-wall-clock E1) is future work §8.9.
- **Venue budget:** AAAI-26 `7 pages technical + refs + reproducibility checklist` submission (`\usepackage[submission]{aaai2026}` anonymized), `12 pages + refs + appendix` on arXiv (same `main.tex` with `\nocopyright` for camera-ready toggle). `cs.AI` primary, `cs.CL`+`cs.NE` cross-lists.
- **Gating invariant:** No arXiv upload until `tests/test_synthetic_e7.py` gate `55/55/35/7` still passes AND real `n=50` harness run produces `results/longmemeval/run-*/metrics.json` with `fallback_rate`, `recall_proxy`, `p95`, `acc_with/acc_without` populated.
- **Landing page:** Built in parallel at `positronic-research/docs/site/` (or `positronic-engram/docs/site`) — shares figures/metrics with paper appendix; no PII; deploy via GitHub Pages.

## 1. Repo & Target Layout (§1)

### 1.1 Source of truth
- Markdown corpus stays canonical: `papers/temporal-perception-in-AI/*.md` (`README.md` abstract v0, `10-case-corpus.md` C1-C8, `20-hypotheses.md` H1-H18, `25-polytemporal-schema.md` schema v1, `26-beyond-sql.md` engine, `30-related-work.md` BORROW/ADD, `40-experiments.md` E1-E6, `45-pilot-mail-cognition.md` P1-W2+attachment census, `46-benchmark-results.md` result ledger, `50-object-formation.md` objects, `55-federation.md` federation). No PII (`P-codes`, paraphrased subjects, `positronic-private/` gitignored).

### 1.2 New LaTeX tree
```
papers/temporal-perception-in-AI/
  arxiv/
    aaai26/
      main.tex                 ← 7p tech + refs + checklist (+ appendix on arXiv)
      refs.bib                 ← 33 entries from 30-related-work.md, [verify] resolved
      aaai2026.sty             ← 12K Author Kit (DO NOT EDIT, copied verbatim)
      aaai2026.bst             ← 30K (DO NOT EDIT)
      figs/
        e7_survival.pdf        ← archival/long_term/balanced/short_term 0→78 wks (from e7_results.json)
        ruler_efficiency.pdf   ← tokens_with vs without 4k/8k/16k/32k (from consumers/benchmarks/results/ruler/)
        longmemeval_table.tex  ← generated n=50 table (see §3)
      appendix/
        harness.tex            ← synthetic pilots labeled "Harness Validation"
        object_layer.tex       ← 50-object-formation.md snapshot (optional, gated)
      Makefile | latexmkrc     ← `latexmk -pdf -bibtex main.tex` + `make arxiv.zip`
      .gitignore               ← *.aux *.bbl *.blg *.log *.out *.fls *.fdb_latexmk main.pdf
```

### 1.3 Build
- Local: `latexmk -pdf -bibtex main.tex` (TeX Live, `times`+`helvet`+`courier`+`natbib`+`caption`+`graphicx` per `aaai2026.sty` preamble, `frenchspacing`, `pdfpagewidth 8.5in`). `hyperref`+`bbm`+`CJK` forbidden.
- Overleaf parity: `arxiv.zip` (`main.tex`+`refs.bib`+`aaai2026.*`+`figs/*.pdf`) drag-drop compiles identical.
- arXiv upload: `main.tex`+`refs.bib`+`aaai2026.*`+`figs/` as `tar.gz`; arXiv `cs.AI` primary.

### 1.4 Versioning
- `main` branch holds markdown; `arxiv/aaai26/main.pdf` gitignored (built artifact). Tag `arxiv-v1-b-gated` after `n=50` gate passes. `beta → main` paper merge not required — paper lives on `main`, harness stays `consumers/benchmarks`.

## 2. Document Mapping — Outline to AAAI Sections (§2)

Maps `00-outline.md:37` 10-section map to 7-page budget (plus appendix on arXiv):

| AAAI Section | Source | Budget | Notes |
|---|---|---|---|
| **Abstract** | `README.md` draft v0 | 150-200w | Lead with E7 `55/55/35/7` + real `n=50 Δ`; label pilots as pilots |
| **1 Introduction** | `00-outline.md:3` Tom vignette `10-case-corpus.md:9` C1 | 0.7p | Cargo-cult memory thesis "borrow wheels, not clocks" |
| **2 Related Work** | `30-related-work.md` 33 sources BORROW/ADD | 1.0p | §2.1 benchmarks ToT/TRAM/TimeBench, §2.2 temporal blindness Cheng `2510.23853`, §2.3 memory MemGPT/Mem0/MemoryBank/HippoRAG/Engram, §2.4 cog sci SET/CLS, §2.5 gap "re-derive not decorate" |
| **3 Disanalogy Catalog** | `20-hypotheses.md` H1-H18 → D1-D10 `00-outline.md:14` | 1.2p | One para per D: texture-vs-timestamp, salience-gated, anchors, etc. Each ends with `→ H*` |
| **4 Polytemporal Representation** | `25-polytemporal-schema.md` + `20-hypotheses.md` H-τ | 0.9p | `time_vector` typed table, `τ = ∫ novelty` `00-outline.md:22`, regime coords, fuzzy interval `width=confidence` H9 |
| **5 Encoding & Recall** | `50-object-formation.md` + `26-beyond-sql.md` `Activate·Reconstruct·Decay·Fuse` | 0.8p | Three registers, gate-at-encoding H14, escalation H16, reconstruction H5/H6 |
| **6 Experiments** | `40-experiments.md` E1-E7 + `46-benchmark-results.md` | 1.8p | **Main:** E7 78-wk + real `n=50` (see §3). Appendix: synthetic pilots |
| **7 Federation & Continuity** | `55-federation.md` + `20-hypotheses.md` H11-H13 | 0.6p | `private/accessed-live/imported`, continuous body, wake-up ritual |
| **8 Discussion / Limits** | `00-outline.md:34` | 0.4p | No qualia claim, τ operationalization, human-likeness cost |
| **9 Conclusion** | `00-outline.md:37` | 0.2p | Re-derive time |
| **Refs** | `refs.bib` | uncapped | `aaai2026.bst` `natbib` `\cite`/`\citeauthor` |
| **Reproducibility Checklist** | AAAI-26 template | 1p | Harness `ENGRAM_TAG=v0.2.0`, `consumers/benchmarks`, no PII |
| **Appendix (arXiv only)** | `46-benchmark-results.md` pilots | uncapped | RULER `1/16th at 32k`, synthetic `recall@1 1.0` labeled validation |

Page math: ~6.6p tech + refs → fits 7p submission. Appendix pushes arXiv to ~10-12p.

## 3. Evidence Gates — What Makes B Credible (§3)

### 3.1 Gate G0 — E7 credible figure (already passes, must not regress)
- **Input:** Same 55 messages `2007-08→2009-01` weekly `prune(tau_now)` ladder `0.35→day_token 0.05→expired` `engine.py:443` per `retention_profile` `archival|long_term|balanced|short_term` `S_base 1e6/120/30/6` `engine.py:48`.
- **Output:** `archival 55 long_term 55 balanced 35 short_term 7` `±2` (`0603bf8` + `tests/test_synthetic_e7.py:test_synthetic_e7_replicates_55_55_35_7`).
- **Figure:** `figs/e7_survival.pdf` — 4 curves wks 0→78, first divergence wk36 Liqui-Fire burst, second wk53-54 Genesis-stuff. `CONTROL` identical 37 objects.
- **Paper claim:** Application-knob thesis `46-benchmark-results.md:26`.

### 3.2 Gate G1 — Real LongMemEval n=50 (the B gate)
- **Dataset:** `THUDM/LongMemEval` `longmemeval_s` 500 sessions `avg 115k tok ~500 msgs 6 types` `46-benchmark-results.md:44` (`single-session-user 70 multi-session 133 temporal-reasoning 133 knowledge-update 78`). Cached blob `08d8dad... 278M`.
- **Adapter:** `consumers/benchmarks/harness/adapter.py` `BenchmarkAdapter` → `SQLiteStore`+`MemoryEngine` per-domain `retention_profile` `archival|long_term|balanced|short_term` + per-message chunking `550 msgs/54 sessions` + batch `BGE 512tok 2000char` truncate `suites/longmemeval/real_driver.py`.
- **Matrix:** 2 profiles × 2 embeds = 4 runs: `balanced×lexical`, `long_term×lexical`, `balanced×local :8090 BGE`, `long_term×local`. Each: isolated tmp DB `BenchmarkAdapter(profile, embed, tmp_root)`, `prune(tau_now)` ladder as above.
- **Metrics per run (`results/longmemeval/run-*/metrics.json`):** `recall_proxy` (gold tail `sim` per-message `0.59` vs session head `0.31` `46-benchmark-results.md:47`), `fallback_rate`, `mean_rrf`, `p95_ms`, `p50_ms`, `tokens_with/without`, `ratio`, `has_gold_rate`. Lexical baseline: `FTS +0.5ms` `fallback True has_gold False` for sparse queries until per-message fixed (`1.25s` vs `BGE 27.8s` spot `46-benchmark-results.md:50` with `batch 32`).
- **Judge layer:** `Muse Spark 1.2` answer `1024tok` + `meta-llama/llama-3.3-70b-instruct` `hybrid` judge `YES/NO` (`harness/judge.py` `70b` > `405b 404` `46-benchmark-results.md:60`) → `acc_with` (top-8 RRF `~2k tok`) vs `acc_without` (full `30k chars truncated` or `7.5k` haystack) `Δ = acc_with - acc_without` per-type (`single-session-user`, `temporal-reasoning`, etc.) + overall.
- **Pass threshold for v1 upload:** `recall_proxy` populated for all 4 cells, `fallback_rate` reported, `p95` measured, `acc_with` vs `acc_without` table present for at least `lexical` baseline (local may be gated on `:8090` availability). No claim of beating `GPT-4o 0.45` `Wu Table 3` until `n=500` — pilot honesty `46-benchmark-results.md:69`.

### 3.3 Gate G2 — RULER efficiency (appendix + landing page)
- `suites/ruler` `NIAH` `4k/8k/16k/32k` per-message `32k→72k chars` `consumers/benchmarks/suites/ruler` → `tokens_with ~242 vs without ~4496 1/20` `1/16th at 32k top-8` `46-benchmark-results.md:66`. Labeled "Efficiency Appendix" not retention claim.

### 3.4 What is NOT claimed in B v1
- `n=50` does not quote `Wu Table 3 GPT-4o 0.45` as SOTA — `46-benchmark-results.md:69` "need `n=50 balanced vs long_term lexical vs local` + `70b` accuracy vs RAG top-8 baseline to quote" — follow `n=500` as arXiv v2.
- Synthetic `n=50 recall@1 1.0 p95 0.69ms` `46-benchmark-results.md:34` stays Appendix "Harness Validation" (tautology `pilot{i:03d}`).

## 4. Anonymization & arXiv Hygiene (§4)

- **Double-blind:** `aaai2026.sty` `[submission]` → `Anonymous submission` header, `\affiliations{}` suppressed `12K:9`, no `people.json`/`brain_henry/state`/`index.jsonl`/`datasets/` in zip (`.gitignore` + pre-commit `research/AGENTS.md`). Persons as `p_0001` `45-pilot-mail-cognition.md:6` paraphrased subjects only. Self-cites as "Anon 2026".
- **PII firewall:** Mail corpus aggregates only (`38,245 msgs 2007→2026` `per-year 5→4.9k` `43% image-bearing 16,450` `45-pilot-mail-cognition.md:11` + `attachment census`); no raw bodies. `positronic-private/` never linked.
- **AAAI compliance:** `times`+`helvet`+`courier`+`url`+`graphicx`+`natbib`+`caption` `frenchspacing` `pdfpagewidth 8.5in` per `12K`; no `hyperref`/`bbm`/`CJK`/`ushend` (package error already in sty). `\pdfinfo{/TemplateVersion (2026.1)}` retained.
- **arXiv category:** `cs.AI` primary per Q1 `cs.CL`+`cs.NE` secondary; `cs.CL` cross gets Cheng `2510.23853` citation graph.

## 5. References & Verification Debt (§5)

- `refs.bib` built from `30-related-work.md:117` 33 entries: Cheng `2510.23853` AAAI-26, `2506.05790` token-time, Fatemi `2406.09170` ToT + TRAM/TimeBench/TempReason/TIME, Packer `2310.08560` MemGPT, Zhong `2305.10250` MemoryBank `R=e^{-t/S}` baseline E1, Park `2304.03442` Generative Agents, Gutiérrez `2405.14831` HippoRAG, FOREVER `2601.03938` model-time, Engram `tonitangpotato/engram-ai`, plus cog sci James/Ebbinghaus/Bartlett/Atkinson-Tulving/Collins-Loftus/Gibbon/CLS/Conway/Zacks/Schacter/Bergson `[verify]` flags resolved by `2026-08-24` search results in md.
- `aaai2026.bst` sets `\bibliographystyle` automatically on `natbib` load — do NOT add `\bibliographystyle` in `main.tex`. Use `\cite`/`\shortcite`/`\citeauthor`/`\citeyear`.
- Each arXiv ID checked live before upload; `[verify]` stubs (`TeleMem`, `SSGM 2603.11768`, `Du 2603.07670`, `VKnowU 2511.20272`, `Wittmann`, `Droit-Volet` `30-related-work.md`) either verified or cited as "cited as" with note.

## 6. Landing Page — Parallel Track (§6)

### 6.1 Location & stack
- `positronic-research/docs/site/` (or `positronic-engram/docs/site` if engine-owned) — static HTML (`landing.html` or `index.md` via GitHub Pages). Shares `figs/*.pdf` → `figs/*.png` renders + `results/*/metrics.json` for live numbers. No build deps beyond paper figures.

### 6.2 Content (mirrors paper but sales-pitched)
- Hero: `temporal-perception` one-liner + E7 survival plot interactive (archival/long_term/balanced/short_term toggle).
- Sections: Disanalogies (8 cards C1–C8), Polytemporal vector (typed table `25-polytemporal-schema.md`), Benchmarks (E7 + `n=50` table with `acc Δ` + RULER `1/16th`), Install `curl | bash` from `positronic-opencode-plugin/install.sh` `beta/c985bcb`.
- Footer: `cs.AI` arXiv link (post-upload), GitHub `positronic-engram` + `positronic-opencode-plugin`.

### 6.3 Isolation
- Paper + site share `figs/` source; site does not import private state. Deploy via `gh-pages` branch or `docs/site` Pages source; no PII; same anonymization as paper.

## 7. Out of Scope (§7)

- Auto-building `llama.cpp`/`BGE-M3` on reader machines — docs only.
- Postgres/pgvector HNSW — `FlatVectorIndex 184ms at 880 episodes` proves need at `10k+` but not for `n=50` gate.
- New τ-vs-wall-clock E1 head-to-head — future work, not B blocker.

## 8. Interfaces (§8)

- Consumes: `positronic-engram/engine/src/memeng` (`SQLiteStore`, `MemoryEngine`, `Event`, `engine.py:48` `retention_profiles`, `engine.py:443` `prune`), `consumers/benchmarks/harness/{adapter,metrics,report,config,judge}` + `suites/{longmemeval/{dataset,driver,real_driver},ruler,synthetic_e7}`, `THUDM/LongMemEval` cached `datasets/`, `bge-embed.service :8090` (BGE-M3 dim 1024 pooling cls 262MB), `OPENROUTER_API_KEY` for `70b` judge + `Muse Spark` answer.
- Produces: `papers/temporal-perception-in-AI/arxiv/aaai26/main.pdf` (arXiv `cs.AI`), `results/longmemeval/run-*/metrics.json`+`report.md`, `arxiv.zip`, `docs/site/index.html`.

## 9. Risks (§9)

- `:8090` BGE availability — gate `local` runs with skip + lexical fallback note `46-benchmark-results.md:55` `511/550 embeds` batch 32 fix; paper table notes lexical vs local separately.
- `405b 404` on OpenRouter — default `70b` `hybrid YES/NO` `46-benchmark-results.md:60` cost `~$0.002/10q`.
- `500` msgs `115k tok` per Q → per-message chunking required or haystack truncated `7.5k` as `acc_without` baseline `46-benchmark-results.md:43`.
- `hyperref` accidentally imported via package — `aaai2026.sty` hard errors; guard in Makefile `grep -r hyperref`.

## Self-Review

- Placeholder scan: No TBD — `ENGRAM_TAG=v0.2.0`, `08d8dad... 278M`, `48` retention, `443` prune, `55/55/35/7`, `16,450 43%`, `38,245` all pinned; refs explicit.
- Internal consistency: 7p + refs + checklist math matches AAAI-26 `January 20-27 2026 Singapore` limits; appendix on arXiv uncapped; `cs.AI` primary vs `cs.CL` benchmark section not contradictory — cross-list covers both.
- Scope check: B gates on `n=50` real + E7; `n=500` Wu `Table 3` deferred to v2 — single-impl plan feasible.
- Ambiguity check: `hyperref` ban explicit, `anonymous submission` header explicit, `P-codes` anonymization explicit, `synthetic pilots = validation not claim` explicit.

