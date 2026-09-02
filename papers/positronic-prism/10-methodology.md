# 10 — Methodology: measuring model fitness on a non-failing memory substrate

> **Status:** protocol final; numbers fill in from `final-context1` + cookoff.

## Principle

The memory system is held **constant and non-failing**; the models are the
**variable**. All isolation is designed so a score difference can only be
attributed to the answer model (or to a separately-classified retrieval miss).

## Fixed substrate (the controlled constant)

- **Brain**: per-question `tmp-{idx}` memory.db, one question per brain.
- **Retrieval**: `activate(text, k=8, context_window=1)` — top-8 snippets, each
  expanded to ±1 τ-adjacent stream neighbor. This is the version that recovers
  all 18 previously-missing golds; retrieval is *verified* non-failing by the
  gold-presence check below.
- **Ingest**: per-message chunking (~500 msgs/question), BGE-M3 local embeddings.
- **Profile**: `archival`, embed `local` — the paper's configuration.

## Gold-presence check (isolates retrieval from extraction)

For every question, before any model is called:

```
gold_in_context = gold[:12] in join(snippet for hit in top8)  # lowercase
```

This binary check classifies every question:
- gold **present** → a model miss is an *extraction* failure (model's fault).
- gold **absent** → a *retrieval* miss (memory system's fault, measured
  separately, and — after the `context_window` fix — observed to be 0).

This is the load-bearing check: it is what lets PRISM say "the memory system
did not fail; the model did."

## Model panel (the variable)

Six answer models, identical prompts, temperature 0, max_tokens 64:

| model | class |
|---|---|
| deepseek/deepseek-v4-flash-0731 | cheap open-weight (the main-run model) |
| deepseek/deepseek-v4-pro-0813 | open-weight pro |
| z-ai/glm-5.3-flash | open-weight flash |
| qwen/qwen3.8-flash | open-weight flash |
| moonshotai/kimi-k3 | open-weight |
| google/gemini-3.7-flash | frontier flash |

Each model sees the **same** retrieved context (same brains, same `context_window=1`),
so any accuracy difference is extraction ability, not retrieval.

## Judge protocol

- **Exact-substring** (primary): `gold[:12] in answer` or first-word match —
  deterministic, no model-judge confound.
- **LLM judge** (secondary, `llama-3.3-70b`, hybrid): for answers where
  exact-substring is too strict (paraphrase).
- Reported numbers state which judge was used; the paper's headline uses the
  same judge for with/without.

## Failure taxonomy (per-model classification)

For every wrong answer, classify into:

| class | definition | attributed to |
|---|---|---|
| retrieval-miss | gold absent from top-8 | memory system (separate) |
| extraction-miss | gold present, model wrong | answer model |
| empty-answer | `ans == ''` | answer model (structural) |
| error | model call failed (API) | infrastructure |

The **extraction-miss + empty-answer** rows are the model-fitness data. The
retrieval-miss row is reported separately and kept at 0 by the fixed substrate.

## Worked example: Q17

- Question: "What did I buy for my sister's birthday gift?"
- Gold: `a yellow dress`
- Retrieval: gold present in hit0 ("For my sister's birthday, I got her a
  yellow dress and a pair of earrings to match.") — **not a retrieval miss.**
- deepseek-v4-flash: missed → **extraction-miss**.
- PRISM records this as a model failure, with the evidence (gold in context).

## Reproducibility

- Harness: `consumers/benchmarks/suites/longmemeval/real_driver.py`
  (`--context 1 --answer-model <id>`)
- Cookoff: `consumers/benchmarks/model_panel.py`
- Dataset: cached `xiaowu0162/longmemeval longmemeval_s` (278 MB blob).
- Every per-question brain is retained under `results/.../tmp-{idx}/`.