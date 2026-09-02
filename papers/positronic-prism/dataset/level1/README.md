# PRISM Level 1 — Polytemporal Extraction Training Set (Free)

> **Status:** scaffold — 41 seed records generated from the `final-context1`
> run's real saved brains. Free tier of the PRISM data standard.

## What this is

A supervised extraction dataset: for each question, the **retrieved polytemporal
context** (`context_window=1`, top-8 joined) paired with the **gold answer**.
The training signal is `context → gold`: teach a model to extract the exact
value from a rich, distracting context where the answer is present.

Every record has `gold_in_context: true` — the retrieval substrate is
non-failing, so any miss is an extraction failure, not a memory failure. That
is what makes this dataset *polytemporal*: the context is real retrieved
memory, not a synthetic paragraph.

## Files

- `train.jsonl` — 41 records (name 17, exact-value 15, counting 9)
- `schema.md` — field definitions + extraction taxonomy
- `generate.py` — regenerate from the benchmark's saved brains

## Training use

Feed `train.jsonl` to a LoRA/QLoRA fine-tune: instruction = "answer the
question from the context", target = gold. A few hundred to a few thousand such
pairs is a realistic extraction-fix run (see the fine-tune cost note in the
repo README).

## Roadmap

- **Level 1 (this)** — free, the standard's adoption seed.
- **Higher levels** — private request: full n=500 autopsies, fresh-model failure
  data, cross-model fingerprint tables, priority access to new runs.

## License / status

Seed data generated from the public LongMemEval cached dataset + positronic
retrieval. Distribution terms TBD — the free level is intended to drive
adoption of the PRISM standard.