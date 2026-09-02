# PRISM Level 1 Dataset — Schema

> **Status:** scaffold — records generated from the `final-context1` run's saved
> brains (real retrieval context, real golds). Free tier, JSONL.

## Format

JSONL — one extraction pair per line, UTF-8, no newlines in fields.

## Fields

| field | type | required | meaning |
|---|---|---|---|
| `id` | string | yes | `prism-l1-<NNNN>` |
| `source` | string | yes | dataset/question reference, e.g. `longmemeval/q16` |
| `question_type` | string | yes | LongMemEval type: `single-session-user`, `multi-session`, `temporal-reasoning`, `knowledge-update` |
| `question` | string | yes | the verbatim question |
| `context` | string | yes | the retrieved windowed snippet (`context_window=1`, top-8 joined) |
| `gold` | string | yes | the exact expected answer |
| `gold_in_context` | bool | yes | retrieval verification — always true in Level 1 (retrieval non-failing) |
| `extraction_class` | string | yes | `exact-value` \| `counting` \| `name` \| `durative` \| `boolean` |
| `difficulty` | string | yes | `easy` (verbatim in context) \| `hard` (needs reasoning/counting across context) |
| `known_model_miss` | bool | no | true if a tested model missed this on identical context (fingerprint data) |
| `note` | string | no | free text |

## Extraction taxonomy (the training signal)

- **exact-value** — copy a literal fact verbatim ("500 Mbps", "16GB", "a yellow dress")
- **counting** — derive a count from context ("7 shirts", "how many playlists")
- **name** — extract a proper noun ("Serenity Yoga", "Sarah", "Target")
- **durative** — a duration/span ("over a year", "4 hours")
- **boolean** — yes/no from context

## Design goals

1. **Fine-tune-ready** — the `context → gold` pair is the supervised example; a
   few hundred to a few thousand such pairs is the input to a LoRA/QLoRA run.
2. **Retrieval-isolated** — `gold_in_context: true` guarantees the failure, when
   it occurs, is the model's, not the memory's. The dataset measures extraction.
3. **Fingerprint-able** — `known_model_miss` lets a lab see which cases trip
   specific model families.

## Generation

Records are produced from `consumers/benchmarks/results/longmemeval/final-context1/tmp-{idx}/*.db`
via `activate(text, k=8, context_window=1)`, pairing the real retrieved context
with the dataset gold. See `README.md` in this directory for the generator.