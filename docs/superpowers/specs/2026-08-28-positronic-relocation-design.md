# Positronic relocation & naming — Design

Date: 2026-08-28
Status: approved (Sections 1–4)
Scope: move all llmem/cognitive/memory research, code, and private brain data out of `~/llmem` + stray `~/dls` into `/usr/local/devel/positronic`; keep game-bot projects in `~/dls`.

## Context

`~/llmem` grew as a single repo mixing public research, a generic memory engine, and Henry's private deployment (PII, `brain_henry/state`, `people.json`). `~/dls` mixes game-bot work (gt-spector, dxvk, wine) with scattered cognitive notes. The system is aspirationally a "positron brain" (Bicentennial Man) but today is only perception + storage (polytemporal schema, salience gate, episodic encoding, consolidation, fuzzy recall). Future stages add utilization — reflexive and deliberative action.

Goal: a clean, PII-safe home that names the whole brain and its first organ separately, supports polyrepo evolution, and leaves `~/dls` as a pure game-bot workspace.

## Decisions carried in

- Whole system metaphor: **positron brain** (Bicentennial Man). Filesystem umbrella: `/usr/local/devel/positronic` (user pick, adjective form).
- Memory+perception subsystem naming: **hybrid** — Asimov umbrella, cognitive-science terms inside (engram, consolidation, etc.).
- Repo topology: **polyrepo umbrella** — top dir is a plain folder, not a git repo; separate git repos inside. Cleanest PII boundary.
- Move scope: **all** research/papers/cognitive/brain data/test imports move; `gt-spector`, `wine`, `dxvk`, game-related stays in `~/dls`.
- Transition: **no symlinks**, clean cut, fix callers in the same migration commits.
- Private protection: `kairos_brain.py` + `brain_henry/` (including `state/`) are private, gated by `.gitignore` (must never appear in a public remote). User confirmed "as long as it is gitignore".
- Future: reflexive/deliberate action will need names that fit the same hybrid scheme.

## Architecture — umbrella layout

```
/usr/local/devel/positronic/                  ← plain folder, NOT a git repo
  positronic-research/                        ← public git repo
    papers/                 ← from ~/llmem/papers
    research/               ← from ~/llmem/research
    notes/                  ← from ~/llmem/notes
    docs/superpowers/       ← specs/plans for research

  positronic-engram/                          ← public git repo — first organ (engram)
    engine/                 ← from ~/llmem/engine (dirname kept, package stays memeng)
    tests/                  ← from ~/llmem/tests (engine tests)
    tests/test_bridge.py    ← from ~/llmem/tests/test_bridge.py
    docs/, README.md        ← public engram docs
    AGENTS.md               ← public contributor guidance (no PII)

  positronic-private/                         ← PRIVATE git repo (private remote or local-only rsync)
    kairos_brain.py         ← from ~/llmem/kairos_brain.py — DB path retargeted
    brain_henry/            ← from ~/llmem/brain_henry (FULL, including state/)
    orchestration/          ← from ~/llmem/orchestration
    experiments/            ← from ~/llmem/experiments (PII-bearing fixtures stay here)
    AGENTS.md               ← Henry-session rules + PII warning
    .gitignore              ← strict: state/memory.db, people.json, index.jsonl, datasets/ ignored

  consumers/                                  ← plain folder for projects that USE the brain
                            ← each consumer is its own public/private git repo, depends on engram as lib
```

`~/dls` after: pure game bots (`src/gt-spector`, `dxvk/`, `wine-*/`, `wineprefix_bots/`, `game-base/`, `hardware/`, `scripts/`). Stray paper/research files, if found in `~/dls`, move to `positronic-research`.

Future organs alongside `positronic-engram` without renames:
- `positronic-reflex/` — fast, reflexive action loop (cerebellar analogue)
- `positronic-prefrontal/` — slow, deliberative planning

## Naming & path contracts

- **Umbrella dirname**: `positronic` at `/usr/local/devel/positronic` (owned by `swong`, already exists as parent).
- **Subsystem name**: `engram` for today's memory+perception system (memory trace). It is an organ inside the future brain, not the brain itself — matches "positron brain is not yet".
- **Internal package**: keep `engine/src/memeng` and `import memeng` unchanged; repo identity is `positronic-engram`, not a Python rename. Future internal rename `memeng → engram` is a separate step.
- **DB path**: `kairos_brain.py:DB` changes from `~/llmem/brain_henry/state/memory.db` to `/usr/local/devel/positronic/positronic-private/brain_henry/state/memory.db` (keeps `brain_henry/` self-contained; `kairos_brain.py` computes `HERE / "brain_henry" / "state" / "memory.db"`).
- **Agent access snippet** (`AGENTS.md`):
  ```python
  import sys
  sys.path.insert(0, "/usr/local/devel/positronic/positronic-private")
  sys.path.insert(0, "/usr/local/devel/positronic/positronic-engram/engine/src")
  from kairos_brain import brain, remember, recall, ask, stats  # private deployment
  from memeng.engine import MemoryEngine  # generic public lib
  ```
- **Paper ↔ code link**: `papers/temporal-perception-in-AI/25-polytemporal-schema.md` etc. live in `positronic-research`; `positronic-engram/README.md` points to research. No duplication.

## Migration mechanics

1. **Snapshot** `~/llmem` to `/tmp/llmem-backup-YYYYMMDD` before any move.
2. **Move** with `git mv` where history matters; otherwise `cp` + `git add`. Three new repos initialized at the new paths:
   - `positronic-research` — `git init`, add research files, first commit.
   - `positronic-engram` — `git init`, add engine code + tests + public docs, first commit.
   - `positronic-private` — `git init`, add kairos/brain_henry/orchestration/state scaffolding, `.gitignore` first, then content; remote is private or no remote (rsync + encrypted backup).
3. **Patch callers** in the same commits: `kairos_brain.py:DB`, `AGENTS.md` snippets, `orchestration/` scripts referencing `~/llmem`, any `sys.path` inserts in consumer projects. `brain_henry/state/config.json` path updated.
4. **PII gate (future fail-safe)**: pre-commit + pre-push hooks in both public repos (`positronic-research`, `positronic-engram`) that scan staged files for private patterns (`brain_henry/state/`, `memory.db`, `people.json`, `henry@`, private `kairos_brain.py` import) and fail. This is a follow-up deliverable in the implementation plan, not a blocker for the move itself.
5. **Delete** `~/llmem` after verification (no symlinks per user decision).
6. **Rollback**: restore from snapshot, revert path patches, `git worktree`/`git status` clean.

## Verification

- **Inventory**: `find ~/llmem -type f | wc -l` before equals sum of `git ls-files` in three new repos after (minus `.gitignore`'d PII files). `git status` clean on public repos; `git ls-files` in public repos shows no `state/`, `people.json`, `memory.db`.
- **Import & DB smoke test** (fresh Python with new `sys.path`):
  ```python
  from kairos_brain import wake, remember, recall, ask, stats
  wake(); stats()  # same episode counts and τ as before
  recall("liqui-fire"); ask("web2")
  ```
- **Email import test**: re-run `brain_henry/ingest.py` or `pull.py` against a test mailbox fixture in `positronic-private/datasets` — episodes land in `positronic-private/state/memory.db` with expected `tau` advance.
- **OpenCode integration test**: fresh opencode session follows `AGENTS.md` in `positronic-private` (Henry) and `positronic-engram` (public) — `remember`/`recall` round-trip succeeds, new `sys.path` inserts work.
- **Engine suite**: `pytest` in `positronic-engram` (46 engine + 2 bridge tests green).
- **Game bots untouched**: `~/dls` `pytest`/`ruff` still green, no files missing.

## Non-goals

- No Python package rename (`memeng` stays).
- No schema migration for `memory.db` (DB moves, not rebuilt).
- No consumer project migrations beyond fixing their `sys.path` if they imported `~/llmem`.

## Open questions for implementation plan

- Exact GitHub remote names for the two public repos (default `positronic-research`, `positronic-engram`).
- Whether `positronic-private` gets a private GitHub remote or stays local-only with encrypted backup.
- Hook implementation detail: simple shell `grep` vs Python scanner for PII patterns.
