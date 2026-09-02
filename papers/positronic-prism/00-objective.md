# 00 — Objective: measure models, not the memory system

## The claim that motivated PRISM

On LongMemEval (n=50, archival/local), positronic's retrieval placed the gold
answer in the top-8 context on every question it was given to answer. The
reported accuracy was not a measure of the memory system — it was a measure of
the answer model's willingness and ability to extract an exact value from
unambiguous context.

Evidence from the development session:

- **muse-spark** returned empty strings on 5/50 questions (`ans_with == ''`),
  including cases where the gold sat verbatim in the context ("500 Mbps",
  "IKEA").
- Re-called with the gold explicitly in context, muse-spark *errored*; the same
  prompt answered correctly under deepseek-v4-flash and glm-5.3-flash.
- With a non-failing answer model, previously-failed questions answered
  correctly, at 16/17 (94%) through the first third of the run.

**Conclusion: positronic's recall is not failing. The models are.**

## Why a formal benchmark

If a memory benchmark's score is dominated by answer-model behavior, then:

1. Every published number is ambiguous — it does not say what failed.
2. Frontier labs cannot see *what to train for* — is it retrieval? extraction?
   refusal behavior?
3. Practitioners cannot choose a model with evidence.

PRISM exists to remove that ambiguity. It is the formal system that answers:
*which model is the best fit for positronic, and how does each one fail?*

## The inverted design

Conventional benchmark: *"which memory system retrieves best?"*
PRISM: *"given a memory system whose retrieval does not fail, which model
extracts best — and how does each model fail?"*

Every measurement in this study serves that goal. Nothing measures the memory
system's quality; the memory system is the *controlled constant*. The models
are the *variable*.

## Design principle: the cabinet and the working memory

Exact copies live in file cabinets and databases; working memory keeps meaning.
Positronic is not a database replacement — git and the filesystem preserve
byte-perfect truth, and the engram *references* that truth instead of
duplicating it. The brain forgets bytes aggressively because it never claimed
them; it preserves the distilled decision structure, and the cabinet preserves
the copy. Fidelity is the cabinet's job; meaning is the engram's. The 4D-access
claim depends on this division of labor: the engram can collapse the haystack
because the byte-truth it points at is never lost.

## Success criteria

- A per-model accuracy matrix on identical retrieval (the cookoff).
- A per-model failure taxonomy: extraction-miss vs empty-answer vs
  retrieval-miss (the latter attributed to the memory system, separately).
- A recommendation: which model class fits positronic, and what a frontier lab
  would train toward (exact-value extraction under distracting context).

## Status

- [x] Failure class identified (muse-spark empty answers, verified)
- [x] Retrieval isolated as non-failing (gold-presence, all recoverable)
- [x] Inverted design locked
- [ ] Main run (deepseek-flash, context_window=1, n=50) — in progress
- [ ] Model cookoff (flash/pro/glm/qwen/kimi/gemini) — ready, waits on run