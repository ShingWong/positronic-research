# 25 — Failure Autopsies (per-failure full traces)

> **Status:** template. One record per failed question, filled as the run +
> cookoff produce failures. Every failure is fully investigated so the reader
> sees, with their own eyes, that the gold was in the retrieved context and the
> model still failed — the limit is the LLM, not the memory system.

## Trace format

Every failure gets a complete, self-contained record:

```
## <Q-idx> — <short question>

**Question:** <verbatim question>
**Gold:** <verbatim gold>

**Retrieved context (context_window=1, top-8, gold marked):**
<verbatim snippets; the snippet containing the gold is marked [GOLD HERE]>

**Model answer:** <verbatim model output; '' if empty>

**Classification:** extraction-miss | empty-answer | error | retrieval-miss

**Autopsy:** why this is a model limit, not a memory failure:
- gold present in retrieved context? YES/NO (retrieval verified separately)
- gold unambiguous in context? (e.g. "a yellow dress" appears once, verbatim)
- model behavior: failed to copy / returned empty / hallucinated
- what a better model did on the same input (from cookoff, if available)
```

## Failure records

<!-- Template row — duplicate per failure:

### Q17 — What did I buy for my sister's birthday gift?
- **Gold:** a yellow dress
- **In context:** YES — hit0: "For my sister's birthday, I got her a yellow
  dress and a pair of earrings to match."
- **Model (deepseek-v4-flash):** <answer>
- **Classification:** extraction-miss
- **Autopsy:** gold present, verbatim, unambiguous. Model failed to copy.
  Retrieval is not at fault.
-->

_(To be filled from `final-context1` failures + cookoff misses.)_

## Cross-model autopsy (the interesting part)

For each failure, once the cookoff runs, add what *each* panel model did on the
*same* retrieved context:

| Q | gold | flash | pro | glm | qwen | kimi | gemini | class |
|---|---|---|---|---|---|---|---|---|
| 17 | a yellow dress | miss | | | | | | extraction |
| 19 | 7 | miss | | | | | | extraction |

This is the reader-payoff: a single question, identical context, six models —
the reader sees the *model* decide the outcome. The memory system is held
constant, so the variance is visibly, provably the LLM's.

## Rule

No failure is reported without its trace. A reported accuracy without an
autopsy for each miss is not PRISM-grade.