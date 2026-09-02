# 30 — Findings: the memory system is not the variable

> **Status:** draft findings, pending final numbers. The narrative is fixed by
> the isolated measurements, not the absolute scores.

## Finding 1 — Recall does not fail; extraction does

The gold-presence check separates the two. On every analyzed failure, the gold
was either present in top-8 (extraction failed) or — before the `context_window`
fix — absent because a *premise* message outranked its *answer* message (a
retrieval artifact, now fixed). Once retrieval is fixed, the remaining failures
are model failures: extraction-miss or empty-answer.

The uncomfortable implication for the field: **published memory-benchmark
scores conflate the memory system with the answer model.** A weak answer model
deflates every memory system's number equally; a strong one inflates it. The
memory system's true contribution is invisible until the model is isolated.

## Finding 2 — Model fitness varies wildly, and visibly

Same brains, same context, same prompt: model accuracy differs because of
extraction ability — exact-value copying under distracting but sufficient
context. This is the "answer-model sensitivity" that PRISM makes explicit. The
cookoff table (20-§3) quantifies it; the taxonomy (20-§4) names *how* each
model fails.

## Finding 3 — The empty-answer defect poisons naive benchmarks

muse-spark returned `''` on 5/50 questions — not a wrong answer, a *non-answer*.
A benchmark that doesn't check for empty responses misreads this as a memory
failure. PRISM classifies it separately and attributes it to the model. This is
a structural, model-side defect that no retrieval improvement can fix.

## Finding 4 — Cheap models can be the right fit

The main-run model is deepseek-v4-flash — near-frontier reasoning at commodity
cost. If the cookoff shows flash ≈ frontier on this substrate, the practical
claim is strong: **positronic's value is in retrieval; the cheapest competent
model extracts it.** Deployment cost does not need to scale with capability.

## What a frontier lab would read here

- **Train toward exact-value extraction under distracting context.** The
  extraction-miss class is precisely that: the gold is in context, the model
  does not copy it.
- **Treat empty-answer as a first-class failure mode.** It is not an edge case;
  it is 10% of one production model's output.
- **Benchmark models, not just memory systems.** The conflation in Finding 1
  is a measurement error the field is currently repeating.