# Paper Split: arXiv (long form) vs AAAI26 (empirical core)

> Date: 2026-09-02
> Status: approved design — implementing
> Decision: fork the current `arxiv/aaai26/main.tex` into two diverging papers.

## Context and motivation

The single paper currently serves both arXiv and AAAI26. A reviewer's critique
exposed the tension: the paper carries the full C1-C8/D1-D10/H1-H18 apparatus
(which AAAI reviewers called "phantom references") *and* the experiments, all
crammed into 7 pages. The user's decision: **arXiv gets the intellectual
contribution (more words, full theory, exhaustive tables), AAAI26 gets the
scientific core (thesis + empirical proof, stripped for a 7-page reviewer).**
They diverge on purpose.

## Target structure

```
papers/temporal-perception-in-AI/
  arxiv/           ← NEW: the intellectual contribution (long form)
    main.tex       ← fork of current; theory + full experiments + appendices
    figs/  appendix/  refs.bib  aaai2026.sty  aaai2026.bst  Makefile
  aaai26/          ← NEW: the empirical core (7 pages, double-blind)
    main.tex       ← stripped: thesis + experiments + 4 invariants
    figs/  appendix/  refs.bib  aaai2026.sty  aaai2026.bst  Makefile
```

Both are forked from the current `arxiv/aaai26/`. Shared assets (`refs.bib`,
`.sty/.bst`, `figs/`, `appendix/`) are **copied** into each so the two diverge
independently. The old `arxiv/aaai26/` dir is removed after both forks build.

## arXiv version (long form, ~10-14 pages, non-blind)

Keeps everything the current paper has, **plus** what reviewers said was
missing because the long form has room:

- Full apparatus: Introduction (Tom vignette), Related Work, **complete D1-D10
  disanalogy catalog**, Polytemporal Representation, Encoding/Recall, all
  experiments (E7, LongMemEval, RULER, token-reduction, **E1 decay ablation**),
  Federation/Continuity, Discussion, Conclusion, appendices (harness, RULER).
- **NEW: exhaustive C→D→H table** (1-2 pages): Case Vector C1-C8 →
  Disanalogy D1-D10 → Formal Hypothesis H1-H18 → Operational Test. Resolves
  "phantom references" by enumeration.
- **NEW: PRISM defined** (one clean paragraph + the measurement axes).
- **NEW: E1 decay-ablation 2×2 matrix** (the decisive reviewer experiment).
- Author: **Shing Wong** (arXiv is non-blind).

## AAAI26 version (7 pages, double-blind, "thesis not theory")

- **S1 Introduction & Motivation (~1 page)**: tightened 2-sentence "cold
  morning at LSU" texture-vs-timestamp intuition; the cargo-cult critique
  stated directly.
- **S2 The Polytemporal Architecture (~1.5 pages)**: Table 1 (schema
  primitives: `tau`, `fuzz`, GiST indexes), how τ is computed via
  compression-progress `dτ/dt`.
- **S3 Disanalogies & Predictions (~1 page)**: NOT 18 rows — **4 architectural
  invariants** (Salience Gating over Temporal Age; Multi-Coordinate
  Polytemporal Vectors; Schema Fusion over Hoarding; Continuous Substrate
  Coupling), each a dense table row.
- **S4 Empirical Feasibility (~2.5-3 pages)**: E7, LongMemEval (0.90/0.12,
  Δ0.78), RULER (1/74), **E1 decay ablation (2×2 matrix)**; PRISM defined in
  one sentence. Frame as system feasibility + retrieval efficiency proofs,
  conceding the fleet decision-quality ablation is the targeted next phase.
- **S5 Related Work & Discussion (~1 page)**: tight; limitations clean.
- **Double-blind compliance**: NO `Shing Wong`, NO affiliation, NO AAAI
  copyright strip; third-person tool refs; `[Anonymous Tool]` for custom
  internals.
- **Hardware leakage cleaned**: NO `:8090`, `:8080`, `renderD128`, `gfx906`
  in main body; reproducibility stated as "dual Intel Xeon CPUs with AMD Vega
  accelerators using llama.cpp and BGE-M3 embeddings".

## Reviewer-driven improvements (where they land)

| Reviewer point | arXiv | AAAI26 |
|---|---|---|
| Confounded baseline | E1 ablation full | E1 2×2 matrix |
| Phantom refs (H/C/D) | exhaustive C→D→H table | 4 invariants table |
| Underpowered n=50 | n=500 roadmap in Discussion | already discloses POC framing |
| Raw log dumps | stays in appendix | `:8090` etc removed; "standard compute params" |
| Double-blind | N/A (non-blind) | author stripped, anonymous tools |

## Shared vs diverged

- **Shared (copied)**: `refs.bib`, `aaai2026.sty/bst`, `figs/` generators.
- **Diverged**: `main.tex` bodies, `appendix/harness.tex` (AAAI version
  anonymized/generalized; arXiv keeps full repro dump), the E1 table.
- `metrics-50.json`, `e7_survival.pdf`, `ruler_efficiency.pdf` are in `figs/`
  and copied (both papers reference them).

## Testing / verification

- Each `Makefile` builds its own `main.pdf` with `latexmk -pdf -bibtex`.
- arXiv must compile ~10-14 pages, 0 errors.
- AAAI26 must compile exactly ≤7 pages, 0 errors, no `Shing Wong`, no `:8090`.
- Grep-gate each: stale 0.58/0.44/55-55-35-7 absent; new 0.90/0.78 (LongMemEval)
  and the E1 2×2 (tau 35/55 vs wall 0/55 on burst-quiet) present.
- Regenerate `arxiv.zip` for arXiv (16+ entries, clean).
- Update `docs/site/paper.pdf` to the arXiv main.pdf.

## Out of scope (recorded, not this task)

- Full n=500 LongMemEval run (roadmap item, referenced in Discussion).
- Salience-gated burst variant of E1 (follow-up experiment).
- PEEP standalone repo (separate queue item).

## Non-goals

- Do NOT keep a single shared file. The two papers are separate artifacts.
- Do NOT cut the E1 result from either — it is the decisive evidence.