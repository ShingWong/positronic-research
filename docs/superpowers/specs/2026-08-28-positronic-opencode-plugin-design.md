# Positronic OpenCode Plugin — Design

> **Goal:** Public `opencode` plugin that lets any user `pull from GitHub` and run the positron brain (federated `MemoryEngine` brains), gated as private-beta via `beta` branch until milestone, with sufficient `llama.cpp/BGE-M3` docs and no can-of-worms auto-install.

**Decisions locked 2026-08-28:** Approach A (thin plugin + wizard) approved, §§1-4 approved, 3-tier llama docs required.

## 1. Repo & Distribution (§1)

* **New repo:** `positronic-opencode-plugin` (alt `positronic-plugin`) at `github.com/<your-org>/positronic-opencode-plugin` (e.g., `positronic` org). Public visibility from day 0.
* **Branches:** `main` = stable docs-only (install works lexically, no beta features). `beta` = active development + wizard. **Beta gating is install-time, not GitHub branch ACL** (public repo branches are world-readable): `beta` docs carry `> Beta — invite only` notice and installer checks `GITHUB_TOKEN` allowlist via `gh api repos/<org>/positronic-opencode-plugin/collaborators` or `npm` dist-tag `beta` (`npm install @positronic/plugin@beta` requires token). Testers get Collaborator invite; public users see `main` only until `beta→main` merge + tag `v0.1.0`.
* **Engine dependency:** `positronic-engram` stays public (separate repo). Plugin pins an `engram` tag (`ENGRAM_TAG=v0.2.0`) at install, clones via `git clone --depth 1 --branch $TAG https://github.com/<your-org>/positronic-engram`, then `pip install -e engine` (or `uv pip`). No vendoring.
* **Why public+beta:** preserves stars/history, avoids private→public history rewrite, matches relocation spec's polyrepo model (`positronic-research/docs/superpowers/plans/2026-08-28-positronic-relocation.md:15`).

## 2. Plugin Runtime (§2)

* **Stack:** `@opencode-ai/plugin` `define` (promise or effect). Single file `src/index.ts` + `src/wizard.ts` + `src/doctor.ts`.
* **Hooks:**
  * `session.created` → `wake()` if `.positronic/brains/*/memory.db` exists else launch `positronic init` wizard.
  * `message.updated` (assistant) → `remember(subject, arousal=heuristic, text=summary)` best-effort; also expose `recall(text,k)` / `ask(object)` as tools.
  * `session.compacting` → `consolidate(summary, arousal=0.4)` (pre-compaction ritual `brain_henry/state/session_backup_2026-08-25.md:144`).
  * `tool` hooks: `positronic.recall`, `positronic.ask`, `positronic.stats`, `positronic.doctor`.
* **Federation:** User chooses N brains in wizard. Each brain = `SQLiteStore` file `.positronic/brains/{name}/memory.db` + `config.json` `{retention_profile, threshold, burst_threshold, tau_per_surprise}`. Profiles `engine/src/memeng/engine.py:48` `balanced|archival|long_term|short_term` — retention has major impact, so wizard explains with E7 numbers (`55/55/35/7` survival). `activate()` RRF-fuses across brains when `k` request spans federation; `ask()` scopes to named brain or all.
* **Embed backends (user choice at init, change via `positronic config`):**
  * `lexical` — FTS5 only (`0.5ms` verified `2026-08-28`, always works).
  * `local` — `http://127.0.0.1:8090/v1/embeddings` `BGE-M3` (`18-35ms` dim 1024 verified via `bge-embed.service`).
  * `remote` — `baseURL + apiKey` (e.g., `https://api.openai.com/v1`, hosted `BGE-M3`/`nomic`), calls same `/v1/embeddings`.
* **Config:** `.positronic/config.json` (gitignored DB, tracked config). Example: `{"brains":{"kairos":{"profile":"balanced","embed":"lexical"},"mail":{"profile":"long_term","embed":"local"}}, "embed":{"local_url":"http://127.0.0.1:8090"}}`.

## 3. Llama Docs (§3)

* **File:** `docs/llama.md` (and `README.md` quick-start). Three tiers, no auto-build:
  * **Tier 1 — Lexical only (0 deps):** `opencode plugin add ... && positronic init --embed lexical` → works, `recall()` uses FTS5+recency.
  * **Tier 2 — Remote API (30ms, no local build):** `export OPENAI_API_KEY=...; positronic init --embed remote --base-url https://...` + example for OpenAI/BGE/hosted.
  * **Tier 3 — Local BGE-M3 (recommended):**
    1. `llama.cpp` install: `apt install llama.cpp` vs `cmake` build with `HIP/CUDA` notes, link to `llama.config:4` `LLAMA_BIN` pattern.
    2. Model: `curl -L https://huggingface.co/.../bge-m3-Q8_0.gguf -o /usr/local/devel/models/embedding/bge-m3-Q8_0.gguf` (606MB) + `sha256sum` check.
    3. Service: `sudo cp docs/bge-embed.service /etc/systemd/system/ && sudo systemctl enable --now bge-embed.service` (unit proved `2026-08-28`: `ExecStart=-m ... --embedding --pooling cls --host 127.0.0.1 --port 8090 -c 8192`, `Restart=always`, `262MB` RAM).
    4. Verify: `curl http://127.0.0.1:8090/health`, `curl :8090/v1/embeddings`, `python3 -c "from kairos_brain import recall; print(recall('web2'))"` (fallback=False).
    5. Troubleshoot: `journalctl -u bge-embed`, `HIP` vs CPU, `pooling cls` vs `mean` warning, port conflict `:8090`.
* **Doctor:** `positronic doctor` (or `opencode positronic doctor`) checks `engram` import, DB, FTS, `:8090/health`, `llama-server --version`, prints tier status.

## 4. Federation & Safety (§4)

* **PII firewall:** `.gitignore` `*.db`, `memory.db`, `brain_henry/state` (mirrors `positronic-private/.gitignore:1` and `positronic-engram/.githooks/pre-commit` hook). Pre-commit + pre-push hooks in plugin repo block `brain_henry/state|memory.db|people.json|kairos_brain.py` (patterns hardened `de4c891`).
* **Testing:** `pytest` for wizard (temp `tmp_path` DB, mock `beta` branch), `test_bridge.py` style `engine/tests/test_bridge.py:1` for `ask()/recall()` round-trip; integration: `fresh clone → lexical recall → (if :8090) semantic recall` in CI.
* **Versioning:** Plugin pins `engram` tag, exposes `positronic --version`.
* **Milestone TBD:** flip `beta→main` when functional gate (E7 repro + `recall@k`/`p95<300ms`) and docs/tests gate pass.

## Interfaces

* Consumes: `positronic-engram/engine/src` (`MemoryEngine`, `SQLiteStore`, `extract_entities`), `llama.cpp` `llama-server`, `BGE-M3` `bge-m3-Q8_0.gguf`, `opencode` plugin API.
* Produces: per-project `.positronic/brains/*/memory.db`, federated `activate()`.

## Out of Scope

* Auto-building `llama.cpp` (explicitly deferred — can-of-worms).
* Postgres/pgvector HNSW (future, after `FlatVectorIndex` `184ms` at 880 episodes `2026-08-28` proves need at `10k+`).
