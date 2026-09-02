# 40 — Implications

> **Status:** scaffold. Tighten after the numbers land.

## For frontier model labs

PRISM is a target-shaping study. It tells a lab *exactly what to train for*:

1. **Exact-value extraction under sufficient-but-distracting context.** The
   extraction-miss class is the training signal: the gold is present, the model
   fails to copy it. That is a capability gap, not a context-window gap.
2. **Empty-answer as a measurable defect.** Non-answers should be a failure
   mode in eval, not a silence to ignore.
3. **Model-vs-memory separation in evals.** Every long-context benchmark that
   feeds a model's answer through a model's judge has at least two model
   confounds. Isolating them (as PRISM does) is the methodology labs should
   adopt internally.

## For practitioners (and the email-archival sale)

PRISM is the evidence base for "we meticulously test and measure every
component":

- **Which model to deploy** — chosen by measurement, not by fashion.
- **What to budget** — cheap competent models may suffice; cost need not scale
  with capability.
- **What the memory system guarantees** — retrieval that places the gold in
  context, verified per-question, sub-second.
- **Audit mode synergy** — forensic/audit capability (provenance, fuzz,
  deterministic retrieval) pairs with a measured model-selection story.

## For the research community

- A reusable method: fixed non-failing substrate → model cookoff → failure
  taxonomy.
- A dataset artifact: per-question brains retained for anyone to re-run any
  model against.
- A correction: the conflation of memory score and model score (Finding 1).

## Next steps

1. Complete main run → fill 20-§1/§2.
2. Run cookoff (`model_panel.py`) → fill 20-§3/§4.
3. Analyze per-model failure modes → deepen 30-Finding 2.
4. Decide: standalone tech-report, or companion to the temporal-perception paper.