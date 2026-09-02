# Positronic PRISM — Polytemporal Retrieval with Isolated Scoring of Models

> **Status:** scaffold — results fill in as the `final-context1` n=50 run and the
> model panel (cookoff) land. See `consumers/benchmarks` for the harness.
> Cookoff results (frontier ceiling, flash-failures panel, opus-5 falsification)
> are committed in `cookoff-results.md` + `results/`.

**Positronic PRISM is not a benchmark of memory systems. It is a benchmark of
models — measured against a memory system that does not fail.**

The finding that motivated it: on LongMemEval, positronic's retrieval *finds the
gold* every time, yet the reported score is dragged down by the *answer model* —
a model that returns empty strings, hallucinates, or short-circuits on exact
extraction. The memory is not the bottleneck. The model is.

PRISM isolates that fact and makes it measurable. One score is decomposed into
its component wavelengths — retrieval quality, extraction quality, answer-model
choice — on a fixed polytemporal substrate. The question PRISM answers is not
"which memory system wins?" but:

> **Given retrieval that does not fail, which model extracts the gold, and how
> does each model fail when it doesn't?**

That is the goal every measurement below serves.

## What PRISM measures (the inverted design)

| Component | Isolated how | What it shows |
|---|---|---|
| Retrieval | fixed `context_window=1` brains, gold-presence check | positronic recall: passes (all golds retrievable) |
| Extraction | same brains × N answer models | model fitness: who gets the gold out |
| Answer model | exact-substring + LLM judge, with/without | the real variable: models, not memory |
| Failure mode | per-model error taxonomy | *how* each model fails — the interesting read |

## The failure taxonomy (the core contribution)

1. **Retrieval-miss** — gold absent from top-8. In PRISM, this is *not* a model
   failure; it is the memory system's, and it is measured separately (and is
   fixable — see `context_window`).
2. **Extraction-miss** — gold present in context, model fails to copy it.
   *This is what PRISM measures.*
3. **Empty-answer defect** — model returns nothing. A structural failure that
   poisons any benchmark that doesn't check for it.

## The worked example

Q17, "What did I buy for my sister's birthday gift?" — gold `a yellow dress`,
present verbatim in the top-8 context. A model that fails this is not limited
by retrieval; it is limited by extraction. PRISM records exactly that.

## Goal of this document set

- **Motivation** — positronic's recall is not failing; the models are.
- **Method** — measure models' best fit for positronic; all measurements serve
  that goal.
- **Depth** — dive into how each model fails, model by model.
- **Audience** — the most advanced professionals in the field; a read worth
  their attention.

See `00-objective.md` for the full thesis, `05-four-dimensional-access.md`
for the core image (4D access to a 3D haystack), `10-methodology.md` for the
protocol, `25-failure-autopsies.md` for the per-failure traces that prove
each miss is a model limit not a memory failure, `cookoff-results.md` for the
measured answer-model panel, and `60-partnerships.md`
for the model-testing / funding offer.