# 60 — Partnerships: run PRISM on your model

> **Status:** proposal template. This is the funding model that makes PRISM a
> sustainable research operation, not a one-time paper.

## The offer

We run Positronic PRISM on your model. You get the data your own evals don't
give you. The community gets the study.

**What we deliver, per model:**

- **Full failure autopsies** — every miss traced: gold in context? what did the
  model return (including empty answers)? classification (extraction-miss /
  empty-answer / error).
- **Extraction taxonomy** — *how* your model fails, by question type (exact
  value, counting, names, durative), so you know what to train toward.
- **Retrieval isolation guarantee** — failures are attributed to the model, not
  the memory system; you see your model's true extraction ceiling on a
  non-failing substrate.
- **Recommendation** — where your model sits in the panel, and what the frontier
  gap is.

**What you pay for:** the compute and the analysis. The method is public; the
per-model result is yours to use (and, by agreement, ours to publish in the
aggregate study).

## Why a model maker would fund this

1. **Pre-release signal** — know your beta model's extraction weaknesses
   before release, on a controlled, reproducible substrate.
2. **Comparative evidence** — for open-weight labs: proof that your cheap model
   matches or beats frontier on good retrieval (the DeepSeek-flash result is
   the template).
3. **Training signal** — the empty-answer and extraction-miss classes are
   concrete, actionable training targets.
4. **Cheap** — a PRISM run is near-free in API cost; the value is the analysis.

## Who to approach

- **Open-weight labs** (DeepSeek, Qwen/Alibaba, GLM/Zhipu, Moonshot, Mistral) —
  strongest fit: they want evidence their models are production-viable.
- **Frontier labs** — pre-release betas, where the training signal has most
  value.
- **Institutional consumers** — a variant: run PRISM on *their* anonymized
  corpus to pick their deployment model stack (consulting contract, not grant).

## Donation / research tier (n=500 and scale)

- **n=500 stress run** — the rigorous study that finds what fails next; ~$5-10
  API + ~2 days compute. Funded by grant or donation.
- **3TB scale engineering** — SQLite/FTS limits, memory exhaustion, timeouts
  (see the scale-failure roadmap). Funded as a research program.

## Contact / call to action

_Placeholder — contact for a PRISM run on your model, or to fund the n=500 /
scale program._

## Honest notes

- The method is public and reproducible, so the *value* is the analysis and the
  isolation, not the harness.
- Results are published in aggregate; per-model data is shared per agreement.
- This is a partnership offer with a defined deliverable — not a donation ask.
  A separate donation tier exists for the scale program.