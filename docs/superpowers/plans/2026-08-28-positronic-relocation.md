# Positronic relocation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move all llmem/cognitive/memory research, code, and private brain data from `~/llmem` (+ stray `~/dls`) to `/usr/local/devel/positronic` as a polyrepo umbrella with PII-safe boundaries and clean-cut path updates.

**Architecture:** Top dir `/usr/local/devel/positronic` is a plain folder holding separate git repos: `positronic-research` (public papers), `positronic-engram` (public engine), `positronic-private` (private Henry deployment with `.gitignore` firewall). Moves are `cp -a` + new-repo first commits (history preserved via `/tmp/llmem-backup` snapshot), callers patched in the same commits, verification via file inventory + import/pytest/email-import/opencode smoke tests, then `~/llmem` deleted.

**Tech Stack:** bash, git, Python 3.10+, pytest, SQLite, `rg`/`grep` for PII scans

## Global Constraints

- Umbrella dirname is `positronic` at `/usr/local/devel/positronic` (plain folder, NOT a git repo; owned by `swong`).
- Repo topology is polyrepo umbrella — separate git repos inside the umbrella; cleanest PII boundary.
- Memory+perception subsystem name is `engram` (hybrid: Asimov umbrella, cognitive-science terms inside); future reflexive/deliberate organs become `positronic-reflex` / `positronic-prefrontal` without renames.
- Private protection: `kairos_brain.py` + `brain_henry/` (including `state/`) live in `positronic-private` and are gated by `.gitignore` (must never appear in a public remote). User confirmed "as long as it is gitignore".
- Move scope: all research/papers/cognitive/brain data/test imports move; `gt-spector`, `wine`, `dxvk`, game-related stays in `~/dls`.
- Transition is no symlinks — clean cut, fix callers in the same migration commits.
- Internal Python package stays `memeng` (`engine/src/memeng`, `import memeng` unchanged); DB path changes from `~/llmem/brain_henry/state/memory.db` to `/usr/local/devel/positronic/positronic-private/brain_henry/state/memory.db`.
- PII gate is a future fail-safe pre-commit + pre-push hook in both public repos scanning staged files for private patterns (`brain_henry/state/`, `memory.db`, `people.json`, `henry@`, private `kairos_brain.py` import).

---

## File Structure

Before tasks, the target tree and what each repo owns:

```
/usr/local/devel/positronic/                  ← plain folder
  positronic-research/      (.git, public)
    papers/                 ← from ~/llmem/papers
    research/               ← from ~/llmem/research
    notes/                  ← from ~/llmem/notes
    docs/superpowers/       ← specs/plans (including this plan + 2026-08-28 spec)
  positronic-engram/        (.git, public)
    engine/                 ← from ~/llmem/engine
    tests/                  ← from ~/llmem/tests
    README.md, AGENTS.md    ← public contributor docs
  positronic-private/       (.git, PRIVATE)
    kairos_brain.py         ← from ~/llmem/kairos_brain.py (DB path retargeted)
    brain_henry/            ← from ~/llmem/brain_henry (FULL including state/)
    orchestration/          ← from ~/llmem/orchestration
    experiments/            ← from ~/llmem/experiments
    AGENTS.md, .gitignore   ← Henry-session rules + PII firewall
  consumers/                ← plain folder for projects that USE the brain (empty for now)
```

Existing `~/llmem` files not listed (e.g., `__pycache__`, `.pytest_cache`) are dropped, not moved.

---

### Task 1: Scaffold umbrella + positronic-research repo

**Files:**
- Create: `/usr/local/devel/positronic/` (plain dir), `/usr/local/devel/positronic/positronic-research/.git`, `/usr/local/devel/positronic/positronic-research/papers/`, `/usr/local/devel/positronic/positronic-research/research/`, `/usr/local/devel/positronic/positronic-research/notes/`, `/usr/local/devel/positronic/positronic-research/docs/superpowers/specs/`, `/usr/local/devel/positronic/positronic-research/docs/superpowers/plans/`
- Copy: `~/llmem/papers/*` → `positronic-research/papers/`, `~/llmem/research/*` → `positronic-research/research/`, `~/llmem/notes/*` → `positronic-research/notes/`, `~/llmem/docs/superpowers/specs/2026-08-28-positronic-relocation-design.md` + `~/llmem/docs/superpowers/plans/2026-08-28-positronic-relocation.md` → `positronic-research/docs/superpowers/...`
- Modify: none (no code changes)
- Verify: `git -C positronic-research ls-files`, `git status`

**Interfaces:**
- Consumes: `~/llmem` snapshot (read-only source for this task)
- Produces: `positronic-research` repo at `/usr/local/devel/positronic/positronic-research` with research history seed — Task 2 and Task 5 verify consumers can read it

- [ ] **Step 1: Snapshot ~/llmem before any move**

```bash
cp -a /home/swong/llmem /tmp/llmem-backup-20260828
ls /tmp/llmem-backup-20260828/papers | head -5
```

- [ ] **Step 2: Create umbrella and research repo**

```bash
mkdir -p /usr/local/devel/positronic
mkdir -p /usr/local/devel/positronic/positronic-research
git -C /usr/local/devel/positronic/positronic-research init
```

- [ ] **Step 3: Copy research files (preserve structure)**

```bash
cp -a /home/swong/llmem/papers /usr/local/devel/positronic/positronic-research/
cp -a /home/swong/llmem/research /usr/local/devel/positronic/positronic-research/
cp -a /home/swong/llmem/notes /usr/local/devel/positronic/positronic-research/
mkdir -p /usr/local/devel/positronic/positronic-research/docs/superpowers/specs
mkdir -p /usr/local/devel/positronic/positronic-research/docs/superpowers/plans
cp -a /home/swong/llmem/docs/superpowers/specs/2026-08-28-positronic-relocation-design.md /usr/local/devel/positronic/positronic-research/docs/superpowers/specs/
cp -a /home/swong/llmem/docs/superpowers/plans/2026-08-28-positronic-relocation.md /usr/local/devel/positronic/positronic-research/docs/superpowers/plans/ 2>/dev/null || echo "plan will be present after this task commits"
```

- [ ] **Step 4: Verify no PII leaked into research repo**

```bash
git -C /usr/local/devel/positronic/positronic-research status --short
rg -n "henry@|people\.json|memory\.db" /usr/local/devel/positronic/positronic-research 2>&1 | head -5
# Expected: no matches
```

- [ ] **Step 5: Commit research repo**

```bash
git -C /usr/local/devel/positronic/positronic-research add -A
git -C /usr/local/devel/positronic/positronic-research commit -m "research: seed positronic-research from llmem (papers, research, notes, spec)"
git -C /usr/local/devel/positronic/positronic-research log --oneline -1
```

---

### Task 2: Scaffold positronic-engram public repo

**Files:**
- Create: `/usr/local/devel/positronic/positronic-engram/.git`, `/usr/local/devel/positronic/positronic-engram/engine/`, `/usr/local/devel/positronic/positronic-engram/tests/`
- Copy: `~/llmem/engine/*` → `positronic-engram/engine/`, `~/llmem/tests/*` → `positronic-engram/tests/`, `~/llmem/README.md` → `positronic-engram/README.md` (if exists, else create minimal)
- Create: `/usr/local/devel/positronic/positronic-engram/AGENTS.md` (public contributor guidance, no PII)

**Interfaces:**
- Consumes: `~/llmem/engine`, `~/llmem/tests`, `positronic-research` docs for cross-link
- Produces: `positronic-engram` repo at `/usr/local/devel/positronic/positronic-engram` — public engine library (`import memeng` unchanged) — Task 3's private repo will `sys.path` to its `engine/src`

- [ ] **Step 1: Init engram repo**

```bash
mkdir -p /usr/local/devel/positronic/positronic-engram
git -C /usr/local/devel/positronic/positronic-engram init
```

- [ ] **Step 2: Copy engine and tests**

```bash
cp -a /home/swong/llmem/engine /usr/local/devel/positronic/positronic-engram/
cp -a /home/swong/llmem/tests /usr/local/devel/positronic/positronic-engram/ 2>/dev/null || mkdir -p /usr/local/devel/positronic/positronic-engram/tests
cp -a /home/swong/llmem/README.md /usr/local/devel/positronic/positronic-engram/README.md 2>/dev/null || echo "# positronic-engram — perception+storage (engram) organ" > /usr/local/devel/positronic/positronic-engram/README.md
```

- [ ] **Step 3: Create public AGENTS.md (no PII, no DB path)**

Create `/usr/local/devel/positronic/positronic-engram/AGENTS.md` with:

```markdown
# positronic-engram — public contributor guide

Public engine library: `engine/src/memeng` (`import memeng`).

```bash
pytest engine/tests/
ruff check engine/src/memeng/ tests/
```

No PII. Henry's deployment lives in `../positronic-private` (private, gitignored).
```

- [ ] **Step 4: Verify engine suite in new location**

```bash
python3 -m pytest /usr/local/devel/positronic/positronic-engram/engine/tests/ -q 2>&1 | tail -2
# Expected: 46 passed (or current count)
rg -n "henry@|people\.json|memory\.db" /usr/local/devel/positronic/positronic-engram 2>&1 | head -5
# Expected: no matches
```

- [ ] **Step 5: Commit engram repo**

```bash
git -C /usr/local/devel/positronic/positronic-engram add -A
git -C /usr/local/devel/positronic/positronic-engram commit -m "engram: seed positronic-engram from llmem engine + tests (public, no PII)"
git -C /usr/local/devel/positronic/positronic-engram log --oneline -1
```

---

### Task 3: Scaffold positronic-private repo (privacy boundary)

**Files:**
- Create: `/usr/local/devel/positronic/positronic-private/.git`, `/usr/local/devel/positronic/positronic-private/.gitignore`, `/usr/local/devel/positronic/positronic-private/brain_henry/`, `/usr/local/devel/positronic/positronic-private/orchestration/`, `/usr/local/devel/positronic/positronic-private/experiments/`
- Copy: `~/llmem/kairos_brain.py` → `positronic-private/kairos_brain.py`, `~/llmem/brain_henry/*` → `positronic-private/brain_henry/`, `~/llmem/orchestration/*` → `positronic-private/orchestration/`, `~/llmem/experiments/*` → `positronic-private/experiments/`, `~/llmem/AGENTS.md` → `positronic-private/AGENTS.md`
- Modify: `positronic-private/kairos_brain.py:DB`, `positronic-private/AGENTS.md` sys.path snippet, `positronic-private/brain_henry/state/config.json` if it contains `~/llmem` paths

**Interfaces:**
- Consumes: `positronic-engram/engine/src` (for `sys.path`), `~/llmem` private files
- Produces: `positronic-private` repo with retargeted DB path `HERE / "brain_henry" / "state" / "memory.db"` resolving to `/usr/local/devel/positronic/positronic-private/brain_henry/state/memory.db` — Task 5's smoke tests consume this

- [ ] **Step 1: Init private repo and write .gitignore FIRST**

```bash
mkdir -p /usr/local/devel/positronic/positronic-private
git -C /usr/local/devel/positronic/positronic-private init
cat > /usr/local/devel/positronic/positronic-private/.gitignore <<'EOF'
# PII firewall — never commit private brain state
brain_henry/state/memory.db
brain_henry/state/*.db
brain_henry/state/people.json
brain_henry/state/index.jsonl
brain_henry/state/*.jsonl
datasets/
*.db
__pycache__/
.pytest_cache/
EOF
cat /usr/local/devel/positronic/positronic-private/.gitignore
```

- [ ] **Step 2: Copy private deployment files**

```bash
cp -a /home/swong/llmem/kairos_brain.py /usr/local/devel/positronic/positronic-private/
cp -a /home/swong/llmem/brain_henry /usr/local/devel/positronic/positronic-private/
cp -a /home/swong/llmem/orchestration /usr/local/devel/positronic/positronic-private/
cp -a /home/swong/llmem/experiments /usr/local/devel/positronic/positronic-private/ 2>/dev/null || mkdir -p /usr/local/devel/positronic/positronic-private/experiments
cp -a /home/swong/llmem/AGENTS.md /usr/local/devel/positronic/positronic-private/AGENTS.md
```

- [ ] **Step 3: Patch kairos_brain.py DB path**

In `/usr/local/devel/positronic/positronic-private/kairos_brain.py`, change:

```python
DB = HERE / "brain_henry" / "state" / "memory.db"
```

This already resolves correctly when `HERE` is the private repo root — verify it still reads `brain_henry/state/memory.db` relative to the new location:

```bash
grep -n "DB = HERE" /usr/local/devel/positronic/positronic-private/kairos_brain.py
# Expected: DB = HERE / "brain_henry" / "state" / "memory.db"
```

If the old file used an absolute `Path("/home/swong/llmem/...")`, replace the whole line with the relative form above.

- [ ] **Step 4: Patch AGENTS.md brain-access snippet**

In `/usr/local/devel/positronic/positronic-private/AGENTS.md`, replace:

```python
import sys; sys.path.insert(0, "/home/swong/llmem")
```

with:

```python
import sys; sys.path.insert(0, "/usr/local/devel/positronic/positronic-private")
sys.path.insert(0, "/usr/local/devel/positronic/positronic-engram/engine/src")
```

Verify:

```bash
grep -n "sys.path.insert" /usr/local/devel/positronic/positronic-private/AGENTS.md | head -5
```

- [ ] **Step 5: Verify .gitignore actually hides PII before commit**

```bash
git -C /usr/local/devel/positronic/positronic-private status --short | head -20
# Expected: kairos_brain.py, brain_henry/*.py, AGENTS.md, .gitignore are untracked/modified
# but NOT: brain_henry/state/memory.db, people.json, index.jsonl (ignored)
git -C /usr/local/devel/positronic/positronic-private check-ignore -v brain_henry/state/memory.db
# Expected: .gitignore:1:brain_henry/state/memory.db
```

- [ ] **Step 6: Commit private repo (PII stays ignored)**

```bash
git -C /usr/local/devel/positronic/positronic-private add .gitignore kairos_brain.py brain_henry/*.py brain_henry/*.md AGENTS.md orchestration/ experiments/ 2>/dev/null; git -C /usr/local/devel/positronic/positronic-private add -A; git -C /usr/local/devel/positronic/positronic-private status --short | grep -E "memory\.db|people\.json" && echo "FAIL: PII staged" || echo "PII not staged — ok"
git -C /usr/local/devel/positronic/positronic-private commit -m "private: seed Henry deployment (kairos_brain, brain_henry, orchestration) with DB retargeted to positronic-private"
git -C /usr/local/devel/positronic/positronic-private log --oneline -1
```

---

### Task 4: Patch remaining callers + install fail-safe hooks (follow-up)

**Files:**
- Modify: `/usr/local/devel/positronic/positronic-private/orchestration/*.py` or `*.sh` that reference `~/llmem`, `/usr/local/devel/positronic/positronic-engram/docs` cross-links if any, `consumers/` placeholder README
- Create: `/usr/local/devel/positronic/positronic-engram/.githooks/pre-commit`, `/usr/local/devel/positronic/positronic-research/.githooks/pre-commit` (or `.git/hooks/pre-commit` via `core.hooksPath`)

**Interfaces:**
- Consumes: Task 3's `positronic-private` DB path, Task 1's `positronic-research` location
- Produces: no PII can be committed to public repos even by mistake — Task 5's verification will try to stage a dummy private file and expect the hook to block

- [ ] **Step 1: Grep for stale ~/llmem references in the new umbrella**

```bash
rg -n "/home/swong/llmem|~/llmem" /usr/local/devel/positronic 2>&1 | grep -v ".git/" | head -20
# Expected: no matches after Task 3 patches; fix any that remain
```

If matches remain, patch them:

```bash
# Example: orchestration scripts
sed -i 's|/home/swong/llmem|/usr/local/devel/positronic/positronic-private|g' /usr/local/devel/positronic/positronic-private/orchestration/*.py 2>/dev/null; echo "patched"
```

- [ ] **Step 2: Create fail-safe pre-commit hook in both public repos**

Create `/usr/local/devel/positronic/positronic-engram/.githooks/pre-commit`:

```bash
#!/usr/bin/env bash
# Fail-safe: block private patterns from ever being committed to a public repo
blocked=$(git diff --cached --name-only | rg -E "brain_henry/state|memory\.db|people\.json|kairos_brain\.py" 2>/dev/null || true)
if [ -n "$blocked" ]; then
  echo "BLOCKED: staged files look private:"; echo "$blocked"; echo "Unstage them or move to positronic-private."; exit 1
fi
exit 0
```

```bash
mkdir -p /usr/local/devel/positronic/positronic-engram/.githooks /usr/local/devel/positronic/positronic-research/.githooks
cat > /usr/local/devel/positronic/positronic-engram/.githooks/pre-commit <<'HOOK'
#!/usr/bin/env bash
blocked=$(git diff --cached --name-only | rg -E "brain_henry/state|memory\.db|people\.json|kairos_brain\.py" 2>/dev/null || true)
if [ -n "$blocked" ]; then echo "BLOCKED: staged files look private:"; echo "$blocked"; exit 1; fi; exit 0
HOOK
cat > /usr/local/devel/positronic/positronic-research/.githooks/pre-commit <<'HOOK'
#!/usr/bin/env bash
blocked=$(git diff --cached --name-only | rg -E "brain_henry/state|memory\.db|people\.json|kairos_brain\.py" 2>/dev/null || true)
if [ -n "$blocked" ]; then echo "BLOCKED: staged files look private:"; echo "$blocked"; exit 1; fi; exit 0
HOOK
chmod +x /usr/local/devel/positronic/positronic-engram/.githooks/pre-commit /usr/local/devel/positronic/positronic-research/.githooks/pre-commit
git -C /usr/local/devel/positronic/positronic-engram config core.hooksPath .githooks
git -C /usr/local/devel/positronic/positronic-research config core.hooksPath .githooks
```

- [ ] **Step 3: Verify hook blocks a dummy private file**

```bash
touch /usr/local/devel/positronic/positronic-engram/brain_henry/state/memory.db 2>/dev/null || mkdir -p /tmp/hook-test && touch /tmp/hook-test/memory.db
# Simulate: stage a private-named file in engram, expect block
touch /usr/local/devel/positronic/positronic-engram/memory.db && git -C /usr/local/devel/positronic/positronic-engram add memory.db 2>&1; git -C /usr/local/devel/positronic/positronic-engram diff --cached --name-only | head -5; bash /usr/local/devel/positronic/positronic-engram/.githooks/pre-commit; echo "exit:$?"; git -C /usr/local/devel/positronic/positronic-engram reset HEAD memory.db 2>/dev/null; rm -f /usr/local/devel/positronic/positronic-engram/memory.db
# Expected: exit:1 (blocked)
```

- [ ] **Step 4: Create consumers/ placeholder**

```bash
mkdir -p /usr/local/devel/positronic/consumers
echo "# consumers — projects that import positronic-engram (each its own git repo)" > /usr/local/devel/positronic/consumers/README.md
```

- [ ] **Step 5: Commit hook + placeholder (public repos)**

```bash
git -C /usr/local/devel/positronic/positronic-engram add .githooks/pre-commit && git -C /usr/local/devel/positronic/positronic-engram commit -m "engram: add PII fail-safe pre-commit hook" 2>/dev/null || echo "no githooks commit needed"
git -C /usr/local/devel/positronic/positronic-research add .githooks/pre-commit 2>/dev/null && git -C /usr/local/devel/positronic/positronic-research commit -m "research: add PII fail-safe pre-commit hook" 2>/dev/null || echo "no research hook commit"
```

---

### Task 5: Verification + cleanup of ~/llmem

**Files:**
- Verify: `positronic-research`, `positronic-engram`, `positronic-private`, `~/llmem` backup, `~/dls`
- Delete: `~/llmem` (only after all verifications pass)

**Interfaces:**
- Consumes: all three new repos from Tasks 1–4
- Produces: `~/llmem` removed, `/usr/local/devel/positronic` is the source of truth, game bots still green in `~/dls`

- [ ] **Step 1: Inventory — file counts match (minus ignored PII)**

```bash
find /home/swong/llmem -type f | wc -l
find /usr/local/devel/positronic -type f | wc -l
git -C /usr/local/devel/positronic/positronic-research ls-files | wc -l
git -C /usr/local/devel/positronic/positronic-engram ls-files | wc -l
git -C /usr/local/devel/positronic/positronic-private ls-files | wc -l
# Expected: research + engram + private ls-files ≈ llmem file count minus ignored state DBs
git -C /usr/local/devel/positronic/positronic-research status --short | head -5
git -C /usr/local/devel/positronic/positronic-engram status --short | head -5
# Expected: clean
```

- [ ] **Step 2: Import & DB smoke test (new sys.path)**

```bash
python3 - <<'PY'
import sys
sys.path.insert(0, "/usr/local/devel/positronic/positronic-private")
sys.path.insert(0, "/usr/local/devel/positronic/positronic-engram/engine/src")
from kairos_brain import wake, recall, ask, stats
print(wake())
print(stats())
print(recall("liqui-fire")[:2])
print(ask("web2"))
PY
# Expected: wake shows τ≈39.x, stats same counts as before, recall/ask return results
```

- [ ] **Step 3: Email import + OpenCode integration canaries (user-requested)**

```bash
python3 /usr/local/devel/positronic/positronic-private/brain_henry/pull.py --help 2>&1 | head -5
python3 -m pytest /usr/local/devel/positronic/positronic-engram/engine/tests/ -q 2>&1 | tail -2
# Expected: pull help prints, engine tests 49 passed
python3 -m pytest /usr/local/devel/positronic/positronic-private/tests/test_bridge.py -q 2>&1 | tail -2 || python3 -m pytest /usr/local/devel/positronic/positronic-engram/tests/test_bridge.py -q 2>&1 | tail -2 || echo "bridge tests in private, run from there when present"
```

- [ ] **Step 4: Game bots untouched**

```bash
ls /home/swong/dls/src/gt-spector/AGENTS.md && echo "dls AGENTS present"
python3 -m ruff check /home/swong/dls/src/gt-spector/gt_spector 2>&1 | head -5 || echo "ruff not installed in dls — skip"
```

- [ ] **Step 5: Delete ~/llmem only after all verifications pass**

```bash
# Only after Steps 1–4 are green:
rm -rf /home/swong/llmem
ls /home/swong/llmem 2>&1 | head -3
# Expected: No such file or directory
echo "llmem removed — source of truth is now /usr/local/devel/positronic"
```

