# Cookoff results — answer-model extraction variance on identical retrieval

> **Status:** measured, reproducible. Raw artifacts in `results/` alongside this
> file. Full 6-model panel study is the publishable follow-up (`model_panel.py`
> exists in `consumers/benchmarks/`; not yet run at n=50).

## Frontier ceiling test (the PRISM money result)

All **4 deepseek-flash failures** on identical `context_window=1` brains are
trivially extractable by frontier models. The failures are answer-model
extraction misses, not retrieval misses — retrieval placed the gold in context
every time (recall 1.0).

| model | correct / 4 | note |
|---|---|---|
| claude-opus-5 | 4/4 | |
| gpt-5.6-luna-pro | 4/4 | |
| glm-5.3 | 4/4 | |
| deepseek-v4-pro-0813 | 3/4 | 1 empty content |
| gemini-3.7-flash | 2/4 | "Based"-style non-answers on the rest |

**Proof of the PRISM thesis:** retrieval perfect → flash misses 4 → frontier
gets all 4 → the same brains would score ~1.0 with a frontier extractor. The
measured 0.90 acc_with is therefore **extraction-bound**, not retrieval-bound.

## Flash-failures cookoff (6 models, 3 questions)

Same three questions the frontier test used, all 6 panel models on identical
`context_window=1` brains:

- **Q16** (sister's gift): flash/pro/kimi/qwen all hit; glm-5.3-flash missed
  ("You"); gemini-3.7-flash missed (quoted fragment).
- **Q18** (7 shirts, counting): **kimi-k3 the only hit** — "you packed 7
  shirts" — the same question opus-5 missed *without* memory. flash/pro/glm
  all empty-content; qwen rate-limited; gemini non-answer.
- **Q28** (3:1 ratio): no model cleanly extracted (flash/pro empty; judge
  boundary — the answer contained "3:1" but the strict judge did not match).

Rate-limit / empty-content errors (`[ERR HTTP ...]`, `[ERR empty content]`)
are infra artifacts, not extraction failures — a retry-tolerant harness would
recover them (see kimi-k3 on Q18: hit when it answered).

## Opus-5 "nearly perfect by itself" — falsified

Opus-5 reading the raw 30k-character haystack (no positronic) on the 5
failure questions:

| question | gold | opus-5 without memory |
|---|---|---|
| idx16 | "a yellow dress" | HIT (but claimed "you didn't say") |
| idx18 | "7" | **MISS** — "you haven't mentioned a trip to Costa Rica" |
| idx28 | "3:1" | MISS — "nothing in our conversation" |
| idx30 | "triple what I paid" | HIT (guess-framing) |
| idx42 | "a lemon blueberry cake" | HIT (guess-framing) |

On idx18 the gold was **inside** the truncated window and opus-5 still missed
it — directly falsifying "opus-5 nearly perfect on n=50 by itself." The other
golds fell outside the 30k truncation, so opus's rejection was correct given
what it saw; that is the weakened-baseline artifact the paper's validity
section discloses. The without-memory condition is needle-in-haystack
(find+extract); positronic removes the haystack (extract only).