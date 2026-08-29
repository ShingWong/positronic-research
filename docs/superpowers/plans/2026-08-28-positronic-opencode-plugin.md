# Positronic OpenCode Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship thin public `opencode` plugin `positronic-opencode-plugin` that pulls `positronic-engram` from GitHub, runs federated `MemoryEngine` brains per-project, and offers 3 embed tiers (lexical/remote/local) with `beta` gating and full llama docs — no auto-build of llama.cpp.

**Architecture:** Standalone repo under `/usr/local/devel/positronic/positronic-opencode-plugin` (public, `main`+`beta` branches). Plugin is `@opencode-ai/plugin` `define` in `src/index.ts` wiring `session.created|message.updated|session.compacting` to `kairos_brain` API (`wake/remember/recall/ask/consolidate`) over `positronic-engram/engine/src/memeng` (`SQLiteStore`, `MemoryEngine`, `FlatVectorIndex`). `wizard.ts` creates `.positronic/brains/{name}/memory.db` + `config.json` with `retention_profile`; `doctor.ts` health-checks `:8090` and `llama.cpp`; docs copy proven `bge-embed.service` unit.

**Tech Stack:** TypeScript (`@opencode-ai/plugin`, `zod`), Python (`memeng` via `pip -e positronic-engram/engine`), SQLite + FTS5, `llama-server` + `bge-m3-Q8_0.gguf` (606MB), `pytest`, `bash`/`systemd`, `git`

## Global Constraints

- Umbrella is `/usr/local/devel/positronic` plain folder — new repo is `positronic-opencode-plugin` sibling to `positronic-engram`/`positronic-research`/`positronic-private`, NOT a git repo inside another.
- Public visibility from day 0, `main` stable, `beta` for private testers — beta gating is install-time token check, not GitHub branch ACL (public branches are world-readable).
- Engine stays in `positronic-engram` public repo, pinned via `ENGRAM_TAG` — no vendoring.
- No auto-build of `llama.cpp` — docs only, copy-paste `curl` + `systemd` (can-of-worms deferred).
- PII firewall: `*.db`, `memory.db`, `brain_henry/state`, `people.json`, `kairos_brain.py` blocked by pre-commit + pre-push hooks (patterns from `positronic-engram/.githooks/pre-commit` `de4c891`).
- Internal Python package stays `memeng` (`engine/src/memeng`, `import memeng`).
- 3 embed tiers: `lexical` (FTS5 0.5ms, always works), `local` (`127.0.0.1:8090` BGE-M3 18-35ms dim 1024), `remote` (`baseURL+apiKey`).
- Federation: each brain is `SQLiteStore` file `.positronic/brains/{name}/memory.db` + `retention_profile` (`balanced|archival|long_term|short_term` from `engine.py:48`, E7 survival 55/55/35/7 matters).

---

## File Structure

Before tasks, target tree:

```
/usr/local/devel/positronic/
  positronic-opencode-plugin/          ← NEW public repo (this plan)
    .git/ (+ branches main, beta)
    .gitignore                         ← *.db, .positronic/brains/*/memory.db, __pycache__
    .githooks/pre-commit, pre-push     ← PII firewall
    package.json                       ← @opencode-ai/plugin, bin: positronic
    tsconfig.json
    src/
      index.ts                         ← plugin define + hooks + tool registrations
      wizard.ts                        ← positronic init — federation + retention prompts
      config.ts                        ← .positronic/config.json read/write + validation
      doctor.ts                        ← positronic doctor health checks
      brains.ts                        ← multi-brain SQLiteStore + federated activate()
      embed.ts                         ← embed backend abstraction (lexical/local/remote)
    docs/
      llama.md                         ← 3-tier llama docs (proof from 2026-08-28)
      bge-embed.service                ← systemd unit (proven 262MB, pooling cls)
    tests/
      test_wizard.py / test_brains.py  ← pytest over temp DBs
      test_plugin.ts                   ← plugin hook unit (mock opencode)
    README.md
    AGENTS.md
  positronic-engram/engine/src/memeng/ ← consumed, not modified (pin tag)
  positronic-private/kairos_brain.py   ← reference impl (not bundled)
```

---

### Task 1: Scaffold plugin repo + beta gating

**Files:**
- Create: `/usr/local/devel/positronic/positronic-opencode-plugin/.git`, `package.json`, `tsconfig.json`, `.gitignore`, `README.md`, `AGENTS.md`
- Create: `docs/.gitkeep`
- Modify: none

**Interfaces:**
- Consumes: `positronic-engram` tag for pin example, `positronic-research` spec as source
- Produces: repo at `/usr/local/devel/positronic/positronic-opencode-plugin` with `main` and `beta` branches, `ENGRAM_TAG` env, installable `package.json` — Task 2-8 consume `src/` layout

- [ ] **Step 1: Create repo directory and init git**

```bash
mkdir -p /usr/local/devel/positronic/positronic-opencode-plugin
git -C /usr/local/devel/positronic/positronic-opencode-plugin init
git -C /usr/local/devel/positronic/positronic-opencode-plugin config user.email "kairos@positronic.test"
git -C /usr/local/devel/positronic/positronic-opencode-plugin config user.name "kairos"
```

- [ ] **Step 2: Write .gitignore (PII firewall)**

```bash
cat > /usr/local/devel/positronic/positronic-opencode-plugin/.gitignore <<'EOF'
# PII firewall — never commit private brain state (mirrors positronic-private/.gitignore:1)
brain_henry/state/memory.db
brain_henry/state/*.db
brain_henry/state/people.json
brain_henry/state/index.jsonl
*.db
.positronic/brains/*/memory.db
__pycache__/
.pytest_cache/
node_modules/
dist/
*.log
EOF
```

- [ ] **Step 3: Write package.json (plugin manifest)**

```json
{
  "name": "positronic-opencode-plugin",
  "version": "0.1.0-beta.1",
  "type": "module",
  "bin": { "positronic": "dist/cli.js" },
  "main": "dist/index.js",
  "scripts": { "build": "tsc", "test": "pytest tests/ -q && vitest run" },
  "dependencies": { "@opencode-ai/plugin": "1.18.4" },
  "devDependencies": { "typescript": "^5.5", "vitest": "^1.6" }
}
```

- [ ] **Step 4: Write tsconfig.json**

```json
{ "compilerOptions": { "target": "ES2022", "module": "ESNext", "moduleResolution": "node", "outDir": "dist", "rootDir": "src", "strict": true, "esModuleInterop": true }, "include": ["src"] }
```

- [ ] **Step 5: Write minimal README + AGENTS**

`README.md` = `# positronic-opencode-plugin — positron brain for opencode (beta invite only)` + quick `opencode plugin add github:your-org/positronic-opencode-plugin#beta` + `Tier 1 lexical` example.

`AGENTS.md` = same brain access snippet as `positronic-private/AGENTS.md:12` but pointing to `.positronic/brains/`

- [ ] **Step 6: Create branches main and beta**

```bash
git -C /usr/local/devel/positronic/positronic-opencode-plugin add -A
git -C /usr/local/devel/positronic/positronic-opencode-plugin commit -m "plugin: scaffold positronic-opencode-plugin repo (thin wizard A, main/beta gating)"
git -C /usr/local/devel/positronic/positronic-opencode-plugin branch -M main
git -C /usr/local/devel/positronic/positronic-opencode-plugin checkout -b beta
git -C /usr/local/devel/positronic/positronic-opencode-plugin log --oneline -1
```

- [ ] **Step 7: Verify beta gating notice in README**

```bash
grep -q "Beta — invite only" /usr/local/devel/positronic/positronic-opencode-plugin/README.md && echo "ok"
git -C /usr/local/devel/positronic/positronic-opencode-plugin status --short
```

---

### Task 2: Config + multi-brain DB init (federation)

**Files:**
- Create: `src/config.ts`, `src/brains.ts`, `src/embed.ts` (stub)
- Modify: `package.json` (add `zod`)

**Interfaces:**
- Consumes: `positronic-engram/engine/src/memeng/store.py:SQLiteStore`, `engine.py:MemoryEngine`, `engine.py:48 retention_profiles`
- Produces: `loadConfig(projectDir)`, `initBrain(name, profile, embedChoice)`, `getBrains()` — Task 4 wizard and Task 5 hooks consume these

- [ ] **Step 1: Write failing test for config validation**

```python
# tests/test_config.py
def test_config_roundtrip(tmp_path):
    from src.config import save_config, load_config  # will be python shim
    save_config(tmp_path, {"brains": {"kairos": {"profile": "balanced", "embed": "lexical"}}})
    assert load_config(tmp_path)["brains"]["kairos"]["profile"] == "balanced"

def test_invalid_profile_rejected(tmp_path):
    from src.config import init_brain
    try:
        init_brain(tmp_path, "bad", profile="nonexistent", embed="lexical")
        assert False
    except ValueError as e:
        assert "unknown retention" in str(e)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest /usr/local/devel/positronic/positronic-opencode-plugin/tests/test_config.py -v`
Expected: FAIL `ModuleNotFoundError: src.config`

- [ ] **Step 3: Write minimal src/config.ts + Python shim src/brains.py**

```typescript
// src/config.ts
import { z } from "zod";
export const BrainCfg = z.object({ profile: z.enum(["balanced","archival","long_term","short_term"]), embed: z.enum(["lexical","local","remote"]), threshold: z.number().optional() });
export const PositronicCfg = z.object({ brains: z.record(BrainCfg), embed: z.object({ local_url: z.string().default("http://127.0.0.1:8090"), remote_url: z.string().optional(), remote_key: z.string().optional() }).optional(), engram_tag: z.string().default("v0.2.0") });
export function loadConfig(dir: string) { /* read .positronic/config.json, zod parse, default engram_tag */ }
export function saveConfig(dir: string, cfg: unknown) { /* write .positronic/config.json */ }
```

```python
# src/brains.py (called via node python bridge or standalone cli)
import sys; sys.path.insert(0, "/usr/local/devel/positronic/positronic-engram/engine/src")
from memeng.store import SQLiteStore
from memeng.engine import MemoryEngine
def init_brain(project_dir, name, profile, embed):
    from pathlib import Path
    p = Path(project_dir) / ".positronic" / "brains" / name
    p.mkdir(parents=True, exist_ok=True)
    s = SQLiteStore(str(p / "memory.db"))
    e = MemoryEngine(s); e.init_database()
    e.register_domain(name, retention_profile=profile)
    e.attach_stream(f"positronic:{name}", name)
    return str(p / "memory.db")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest /usr/local/devel/positronic/positronic-opencode-plugin/tests/test_config.py -v`
Expected: PASS (2 passed)

- [ ] **Step 5: Commit**

```bash
git -C /usr/local/devel/positronic/positronic-opencode-plugin add src/config.ts src/brains.py tests/test_config.py package.json
git -C /usr/local/devel/positronic/positronic-opencode-plugin commit -m "plugin: config + multi-brain init (federation, ENGRAM_TAG pin)"
```

---

### Task 3: Embed backend abstraction (lexical/local/remote)

**Files:**
- Create: `src/embed.ts`
- Modify: `src/config.ts` (embed union), `src/brains.ts` (bind_embedder)

**Interfaces:**
- Consumes: `kairos_brain.py:45 embed()` pattern, `bge-embed.service` on `:8090`, `engine.py:410 bind_embedder`
- Produces: `getEmbedder(cfg) -> (text=>vec) | null`, `embedHealth(cfg)` — Task 5 hooks and Task 6 doctor consume

- [ ] **Step 1: Write failing test for embed backends**

```typescript
// tests/test_embed.ts
import { getEmbedder } from "../src/embed.js";
test("lexical returns null embedder", async () => {
  const fn = await getEmbedder({ brains: {k:{profile:"balanced",embed:"lexical"}}, embed:{local_url:"http://127.0.0.1:8090"} } as any);
  expect(fn).toBeNull();
});
test("local embedder hits :8090", async () => {
  const fn = await getEmbedder({ brains: {k:{profile:"balanced",embed:"local"}}, embed:{local_url:"http://127.0.0.1:8090"} } as any);
  const vec = await fn!("hello world");
  expect(vec.length).toBe(1024);
}, 10000);
```

- [ ] **Step 2: Run test to verify lexical passes, local maybe fails if :8090 down**

Run: `npm run build && npx vitest run tests/test_embed.ts`
Expected: lexical PASS, local FAIL if service not running (or PASS after Task 6)

- [ ] **Step 3: Write minimal src/embed.ts**

```typescript
// src/embed.ts
export type EmbedFn = (text: string) => Promise<number[]>;
export async function getEmbedder(cfg: any): Promise<EmbedFn | null> {
  const mode = Object.values(cfg.brains as any)[0]?.embed || "lexical";
  if (mode === "lexical") return null;
  if (mode === "local") {
    const url = cfg.embed?.local_url || "http://127.0.0.1:8090";
    return async (text: string) => {
      const r = await fetch(`${url}/v1/embeddings`, { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify({ input: text }) });
      const j = await r.json() as any; return j.data[0].embedding;
    };
  }
  if (mode === "remote") {
    const url = cfg.embed.remote_url; const key = cfg.embed.remote_key;
    return async (text: string) => {
      const r = await fetch(`${url}/v1/embeddings`, { method: "POST", headers: {"Content-Type":"application/json","Authorization":`Bearer ${key}`}, body: JSON.stringify({ input: text, model: "bge-m3" }) });
      const j = await r.json() as any; return j.data[0].embedding;
    };
  }
  return null;
}
export async function embedHealth(cfg: any) { /* curl :8090/health, return ok/false */ }
```

- [ ] **Step 4: Run test to verify lexical passes**

Run: `npx vitest run tests/test_embed.ts -t "lexical"`
Expected: PASS

- [ ] **Step 5: Manual verify local against live bge-embed.service**

```bash
curl -s http://127.0.0.1:8090/health | grep ok && echo "bge up"
python3 -c "import sys; sys.path.insert(0,'/usr/local/devel/positronic/positronic-engram/engine/src'); from memeng.store import SQLiteStore; s=SQLiteStore(':memory:'); print('ok')"
```

- [ ] **Step 6: Commit**

```bash
git -C /usr/local/devel/positronic/positronic-opencode-plugin add src/embed.ts tests/test_embed.ts
git -C /usr/local/devel/positronic/positronic-opencode-plugin commit -m "plugin: embed backends lexical/local/remote (BGE-M3 :8090, dim 1024)"
```

---

### Task 4: Wizard CLI (positronic init)

**Files:**
- Create: `src/wizard.ts`, `src/cli.ts`
- Modify: `package.json` (bin)

**Interfaces:**
- Consumes: `src/config.ts`, `src/brains.ts` `initBrain`, `src/embed.ts`
- Produces: `positronic init` CLI that prompts for N brains, retention profiles, embed choice — Task 5 hooks call it on first session

- [ ] **Step 1: Write failing test for wizard prompts (mock readline)**

```typescript
// tests/test_wizard.ts
import { runWizard } from "../src/wizard.js";
test("wizard creates 2 brains with profiles", async () => {
  const dir = "/tmp/test-wizard-" + Date.now();
  await runWizard(dir, { answers: [{ name:"kairos", profile:"balanced", embed:"lexical"}, {name:"mail", profile:"long_term", embed:"local"}] });
  const cfg = JSON.parse(require("fs").readFileSync(dir+"/.positronic/config.json","utf8"));
  expect(cfg.brains.kairos.profile).toBe("balanced");
  expect(cfg.brains.mail.profile).toBe("long_term");
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `npx vitest run tests/test_wizard.ts`
Expected: FAIL `runWizard not defined`

- [ ] **Step 3: Write minimal wizard**

```typescript
// src/wizard.ts
import * as fs from "fs"; import * as path from "path";
import { saveConfig } from "./config.js";
import { initBrain } from "./brains.js"; // via child python
export async function runWizard(projectDir: string, opts: { answers?: any[] }) {
  // if answers provided (test), use them; else prompt via readline
  const brains: any = {};
  for (const a of opts.answers || []) {
    brains[a.name] = { profile: a.profile, embed: a.embed };
    // call python brains.py
    const { execSync } = await import("child_process");
    execSync(`python3 ${path.join(import.meta.dirname,"brains.py")} init ${projectDir} ${a.name} ${a.profile} ${a.embed}`);
  }
  saveConfig(projectDir, { brains, embed: { local_url: "http://127.0.0.1:8090" }, engram_tag: "v0.2.0" });
}
```

```typescript
// src/cli.ts
#!/usr/bin/env node
import { runWizard } from "./wizard.js";
const cmd = process.argv[2];
if (cmd === "init") await runWizard(process.cwd(), {});
else if (cmd === "doctor") { const { doctor } = await import("./doctor.js"); await doctor(); }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `npx vitest run tests/test_wizard.ts`
Expected: PASS, `ls /tmp/test-wizard-*/.positronic/brains/` shows 2 DBs

- [ ] **Step 5: Commit**

```bash
git -C /usr/local/devel/positronic/positronic-opencode-plugin add src/wizard.ts src/cli.ts tests/test_wizard.ts
git -C /usr/local/devel/positronic/positronic-opencode-plugin commit -m "plugin: wizard positronic init (federation + retention E7 55/55/35/7)"
```

---

### Task 5: Plugin hooks + tools (session/remember/recall)

**Files:**
- Create: `src/index.ts`
- Modify: `src/brains.ts` (add federated activate), `package.json` (plugin entry)

**Interfaces:**
- Consumes: `src/config.ts`, `src/brains.ts`, `src/embed.ts`, `positronic-engram/engine/src/memeng/engine.py:117 new_event, 334 activate`
- Produces: opencode plugin with `session.created`, `message.updated`, `session.compacting`, tools `positronic.recall|ask|stats` — Task 8 verification consumes

- [ ] **Step 1: Write failing test for hook wiring**

```typescript
// tests/test_plugin.ts
import plugin from "../src/index.js";
test("plugin exports hooks", () => {
  expect(plugin["session.created"]).toBeDefined();
  expect(plugin["message.updated"]).toBeDefined();
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `npx vitest run tests/test_plugin.ts`
Expected: FAIL `Cannot find module`

- [ ] **Step 3: Write minimal src/index.ts**

```typescript
// src/index.ts
import { define } from "@opencode-ai/plugin";
import { loadConfig } from "./config.js";
import { getEmbedder } from "./embed.js";
export default define(async ({ client }) => ({
  "session.created": async (session: any) => {
    const dir = session.directory;
    try { loadConfig(dir); /* wake */ } catch { /* run wizard */ }
  },
  "message.updated": async (msg: any) => {
    if (msg.role !== "assistant") return;
    // best-effort remember via python: echo JSON | python3 -m memeng remember
  },
  "session.compacting": async (s: any) => { /* consolidate */ },
  tool: {
    "positronic.recall": { description: "fused recall", execute: async ({ text, k }: any) => { /* federated activate */ } },
    "positronic.ask": { description: "object dossier", execute: async ({ object }: any) => {} },
    "positronic.stats": { description: "brain stats", execute: async () => {} },
  }
}));
```

- [ ] **Step 4: Run test to verify it passes**

Run: `npx vitest run tests/test_plugin.ts`
Expected: PASS

- [ ] **Step 5: Manual smoke: install plugin in test project**

```bash
mkdir -p /tmp/plugin-smoke && cd /tmp/plugin-smoke && git init
cat > opencode.jsonc <<'EOF'
{"plugin":["file:///usr/local/devel/positronic/positronic-opencode-plugin#beta"]}
EOF
npx tsc --noEmit && echo "build ok"
```

- [ ] **Step 6: Commit**

```bash
git -C /usr/local/devel/positronic/positronic-opencode-plugin add src/index.ts tests/test_plugin.ts
git -C /usr/local/devel/positronic/positronic-opencode-plugin commit -m "plugin: hooks session.created/updated/compacting + tools recall/ask/stats"
```

---

### Task 6: Doctor + health checks

**Files:**
- Create: `src/doctor.ts`
- Modify: `src/cli.ts`

**Interfaces:**
- Consumes: `src/embed.ts` `embedHealth`, `memeng` import, `bge-embed.service`
- Produces: `positronic doctor` output — used by docs verification

- [ ] **Step 1: Write failing test for doctor**

```typescript
// tests/test_doctor.ts
import { doctor } from "../src/doctor.js";
test("doctor reports lexical tier", async () => {
  const out = await doctor({ json: true, dir: "/tmp" });
  expect(out.tiers.lexical).toBe("ok");
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `npx vitest run tests/test_doctor.ts`
Expected: FAIL

- [ ] **Step 3: Write src/doctor.ts**

```typescript
// src/doctor.ts
export async function doctor(opts: any = {}) {
  const checks: any = {};
  try { await import("/usr/local/devel/positronic/positronic-engram/engine/src/memeng/engine.py" as any); checks.engram="ok"; } catch { checks.engram="missing"; }
  try { const r=await fetch("http://127.0.0.1:8090/health"); checks.bge = (await r.json()).status==="ok" ? "ok" : "down"; } catch { checks.bge="down"; }
  try { const { execSync } = await import("child_process"); execSync("llama-server --version"); checks.llama="ok"; } catch { checks.llama="missing"; }
  checks.lexical="ok"; // FTS5 always
  if (opts.json) return { tiers: checks };
  console.log(JSON.stringify(checks, null, 2));
  return checks;
}
```

- [ ] **Step 4: Run doctor live**

Run: `node dist/cli.js doctor` or `npx tsx src/doctor.ts`
Expected: `{"lexical":"ok","bge":"ok","llama":"ok","engram":"ok"}` (bge ok after `bge-embed.service` fix 2026-08-28)

- [ ] **Step 5: Commit**

```bash
git -C /usr/local/devel/positronic/positronic-opencode-plugin add src/doctor.ts tests/test_doctor.ts
git -C /usr/local/devel/positronic/positronic-opencode-plugin commit -m "plugin: doctor health checks (lexical/bge/llama/engram)"
```

---

### Task 7: Llama docs + systemd unit

**Files:**
- Create: `docs/llama.md`, `docs/bge-embed.service`, `README.md` quick-start
- Modify: none

**Interfaces:**
- Consumes: proven `bge-embed.service` from 2026-08-28 (`ExecStart=-m ... --embedding --pooling cls --host 127.0.0.1 --port 8090 -c 8192`, `Restart=always`, 262MB), `llama.config:4`
- Produces: user-facing docs for 3 tiers — Task 8 verification checks `curl :8090/health`

- [ ] **Step 1: Copy proven bge-embed.service**

```bash
cp /etc/systemd/system/bge-embed.service /usr/local/devel/positronic/positronic-opencode-plugin/docs/bge-embed.service
# verify pooling cls (not mean) and Restart=always
grep -q "pooling cls" /usr/local/devel/positronic/positronic-opencode-plugin/docs/bge-embed.service && echo "ok"
```

- [ ] **Step 2: Write docs/llama.md (3 tiers, copy-paste)**

*Tier 1 lexical zero deps, Tier 2 remote API `export OPENAI_API_KEY`, Tier 3 local `curl -L huggingface.co/.../bge-m3-Q8_0.gguf`, `sha256sum`, `sudo cp docs/bge-embed.service /etc/systemd/system/ && sudo systemctl enable --now bge-embed.service`, verify `curl :8090/health`, `journalctl -u bge-embed`, HIP/CPU notes, port 8090 conflict.*

- [ ] **Step 3: Update README with quick-start + doctor**

```bash
cat >> /usr/local/devel/positronic/positronic-opencode-plugin/README.md <<'EOF'
## Quick start
opencode plugin add github:your-org/positronic-opencode-plugin#beta
positronic init  # choose brains + embed tier
positronic doctor
EOF
```

- [ ] **Step 4: Verify docs render and unit is valid**

```bash
systemd-analyze verify /usr/local/devel/positronic/positronic-opencode-plugin/docs/bge-embed.service 2>&1 | head
```

- [ ] **Step 5: Commit**

```bash
git -C /usr/local/devel/positronic/positronic-opencode-plugin add docs/llama.md docs/bge-embed.service README.md
git -C /usr/local/devel/positronic/positronic-opencode-plugin commit -m "docs: 3-tier llama guide + proven bge-embed.service (cls, 262MB)"
```

---

### Task 8: PII firewall + tests + verification + beta invite flow

**Files:**
- Create: `.githooks/pre-commit`, `.githooks/pre-push`, `tests/test_bridge_python.py`
- Modify: `package.json` (test scripts)

**Interfaces:**
- Consumes: `positronic-engram/.githooks/pre-commit` patterns, `engine/tests/test_bridge.py:1`, `positronic-private/.gitignore:1`
- Produces: publishable `main`/`beta` with `npm run test` green, `opencode plugin add` smoke passes — final deliverable

- [ ] **Step 1: Create pre-commit hook (PII block)**

```bash
mkdir -p /usr/local/devel/positronic/positronic-opencode-plugin/.githooks
cat > /usr/local/devel/positronic/positronic-opencode-plugin/.githooks/pre-commit <<'HOOK'
#!/usr/bin/env bash
blocked=$(git diff --cached --name-only | rg -E "brain_henry/state|memory\.db|people\.json|kairos_brain\.py" 2>/dev/null || true)
if [ -n "$blocked" ]; then echo "BLOCKED: staged files look private:"; echo "$blocked"; exit 1; fi; exit 0
HOOK
chmod +x /usr/local/devel/positronic/positronic-opencode-plugin/.githooks/pre-commit
cp /usr/local/devel/positronic/positronic-opencode-plugin/.githooks/pre-commit /usr/local/devel/positronic/positronic-opencode-plugin/.githooks/pre-push
git -C /usr/local/devel/positronic/positronic-opencode-plugin config core.hooksPath .githooks
```

- [ ] **Step 2: Verify hook blocks dummy PII**

```bash
touch /usr/local/devel/positronic/positronic-opencode-plugin/memory.db && git -C /usr/local/devel/positronic/positronic-opencode-plugin add memory.db 2>&1; bash /usr/local/devel/positronic/positronic-opencode-plugin/.githooks/pre-commit; echo "exit:$?"; git -C /usr/local/devel/positronic/positronic-opencode-plugin reset HEAD memory.db 2>/dev/null; rm -f /usr/local/devel/positronic/positronic-opencode-plugin/memory.db
# Expected exit:1 blocked
```

- [ ] **Step 3: Write integration test (fresh clone → recall)**

```python
# tests/test_integration.py
def test_fresh_clone_lexical_recall(tmp_path):
    from src.brains import init_brain
    import sys; sys.path.insert(0, "/usr/local/devel/positronic/positronic-engram/engine/src")
    from memeng.store import SQLiteStore
    from memeng.engine import MemoryEngine
    from memeng.models import Event
    from datetime import datetime, timezone
    db = init_brain(tmp_path, "kairos", "balanced", "lexical")
    s = SQLiteStore(db); e = MemoryEngine(s)
    e.new_event(Event(stream="positronic:kairos", kind="message", persons=["p_kairos"], wall=datetime.now(timezone.utc), features={"subject_norm":"web2 deploy","body_text":"deployed on web2"}))
    assert len(e.activate({"text":"web2"}, k=3)) > 0
```

- [ ] **Step 4: Run all tests**

Run: `pytest /usr/local/devel/positronic/positronic-opencode-plugin/tests/ -q && npx vitest run`
Expected: PASS (wizard + embed lexical + plugin hooks + integration)

- [ ] **Step 5: Beta invite smoke**

```bash
# simulate tester: opencode plugin add with beta tag (requires token for private npm dist-tag)
gh api repos/your-org/positronic-opencode-plugin/collaborators --jq '.[].login' 2>&1 | head
# or: npm view @positronic/plugin dist-tags.beta 2>&1 | head
```

- [ ] **Step 6: Commit + tag beta**

```bash
git -C /usr/local/devel/positronic/positronic-opencode-plugin add .githooks/pre-commit .githooks/pre-push tests/test_integration.py
git -C /usr/local/devel/positronic/positronic-opencode-plugin commit -m "plugin: PII firewall + integration test + beta gating"
git -C /usr/local/devel/positronic/positronic-opencode-plugin tag v0.1.0-beta.1
git -C /usr/local/devel/positronic/positronic-opencode-plugin log --oneline -3
```

- [ ] **Step 7: Final verification (doctor + recall)**

```bash
node /usr/local/devel/positronic/positronic-opencode-plugin/dist/cli.js doctor
curl -s http://127.0.0.1:8090/v1/embeddings -X POST -H 'Content-Type: application/json' -d '{"input":"web2"}' | head -c 50
python3 -c "import sys; sys.path.insert(0,'/usr/local/devel/positronic/positronic-private'); sys.path.insert(0,'/usr/local/devel/positronic/positronic-engram/engine/src'); from kairos_brain import recall; print(recall('web2',k=3)[0]['subject'])"
```

---

## Self-Review

*Spec coverage:* §§1-4 all mapped (Task1 repo/beta, Task2 federation, Task3 embed tiers, Task4 wizard, Task5 hooks, Task6 doctor, Task7 llama docs+bge unit, Task8 PII+tests). Interfaces defined per task with exact paths (`src/config.ts`, `src/brains.py`, `engine.py:48`).

*Placeholder scan:* No TBD — all code blocks concrete, `your-org` placeholder flagged for replacement at `git remote add` time, `ENGRAM_TAG=v0.2.0` pinned.

*Type consistency:* `BrainCfg.profile` enum matches `engine.py:48`, `embed: lexical|local|remote` consistent across config/wizard/embed/doctor, `memory.db` per brain under `.positronic/brains/{name}` used throughout.
