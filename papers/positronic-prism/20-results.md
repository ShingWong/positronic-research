# 20 — Results (placeholders — fill from `final-context1` + cookoff)

> **Status:** tables are templates. Populate when the main n=50 run and the
> model cookoff complete. All measurements serve the goal: **model fitness for
> positronic, on a non-failing memory substrate.**

## 1. Gold-presence (retrieval isolation)

| metric | value | meaning |
|---|---|---|
| gold present in top-8 (context_window=1) | _PENDING_ | should be 50/50 — retrieval non-failing |
| retrieval-miss count | _PENDING_ | expected 0 |

## 2. Main run — deepseek-v4-flash, n=50

| metric | value |
|---|---|
| acc_with | _PENDING_ |
| acc_without (30k truncated haystack) | _PENDING_ |
| delta | _PENDING_ |
| fallback_rate | _PENDING_ |
| floor (secured if all remaining fail) | _PENDING_ |

## 3. Model cookoff — per-model accuracy on identical retrieval

| model | acc | extraction-miss | empty-answer | error |
|---|---:|---:|---:|---:|
| deepseek-v4-flash | | | | |
| deepseek-v4-pro | | | | |
| glm-5.3-flash | | | | |
| qwen3.8-flash | | | | |
| kimi-k3 | | | | |
| gemini-3.7-flash | | | | |

## 4. Failure taxonomy (all models pooled)

| class | count | % |
|---|---:|---:|
| retrieval-miss | | |
| extraction-miss | | |
| empty-answer | | |
| error | | |

## 5. Worked example detail

| Q | question | gold | in-context | model | verdict |
|---|---|---|---|---|---|
| 17 | sister's birthday gift | a yellow dress | yes | deepseek-v4-flash | extraction-miss |
| ... | | | | | |

## 6. Run history (methodology evidence)

n=50 executed 10+ times across profiles, embed tiers, judge modes — see
`50-appendix.md`. The `fix-recheck` archival/local run reproduced the paper's
0.58/0.10; the `final-context1` run (deepseek + context_window=1) is the
headline.