# positronic-research — AGENTS.md

Public research repo for the positron brain. Papers, cognitive foundations, architecture specs.

Umbrella: `/usr/local/devel/positronic` (plain folder)
- `positronic-research/` ← you are here (public)
- `positronic-engram/` ← public engine (`engine/src/memeng`, `import memeng`)
- `positronic-private/` ← PRIVATE (`kairos_brain`, `brain_henry/state` — PII, .gitignore firewall)
- `positronic-opencode-plugin/` ← public plugin (global `positronic.*` tools + `/positronic:*` slashes)

## Brain access (via plugin — no `sys.path` needed)

Plugin `positronic-opencode-plugin@git+https://github.com/ShingWong/positronic-opencode-plugin.git#beta` is active globally (`/positronic:*` slashes + `positronic.*` tools + `positronic <verb> --json` CLI). See `positronic-opencode-plugin/AGENTS.md` and `docs/commands.md` reference.

Store: `../positronic-private/brain_henry/state/memory.db` (private, never commit)

## House rules

- No PII in this repo (research is public). Keep `memory.db`, `people.json`, private email in `positronic-private` (private, `.gitignore`).
- Pre-commit hook blocks `brain_henry/state`, `memory.db`, `people.json`, `kairos_brain.py`, `index.jsonl`, `datasets/`, and private-email content.

## Build & test (engine, if you touch it)

```bash
python3 -m pytest /usr/local/devel/positronic/positronic-engram/engine/tests/ -q
```
