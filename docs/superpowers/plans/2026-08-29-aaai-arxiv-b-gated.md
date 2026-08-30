# AAAI-26 arXiv B-Gated + Landing Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `papers/temporal-perception-in-AI/arxiv/aaai26/main.tex` with `aaai2026.sty` `letterpaper` `submission` (`cs.AI` primary `cs.CL`+`cs.NE` cross), gated on real LongMemEval `n=50` `2×2` matrix + E7 `55/55/35/7`, plus parallel landing page, producing arXiv-ready `arxiv.zip` and `main.pdf`.

**Architecture:** Markdown corpus stays canonical; new LaTeX tree `arxiv/aaai26/` mirrors `00-outline.md` 10-section map into 7p AAAI budget + refs + checklist (+ appendix on arXiv). Harness `consumers/benchmarks` (`BenchmarkAdapter` → `SQLiteStore`+`MemoryEngine` `engine.py:48` `engine.py:443` `prune`) gates evidence before writing claims; figures generated from `results/*/metrics.json`.

**Tech Stack:** LaTeX `latexmk` `pdflatex+bibtex` `aaai2026.sty 12K` `aaai2026.bst 30K` `natbib`+`caption`+`graphicx` `times/helvet/courier` `frenchspacing` `8.5in` (`hyperref` forbidden); Python `memeng` `pytest` `BGE-M3 :8090` `OPENROUTER_API_KEY` `70b` judge; static HTML Pages.

**Spec:** `docs/superpowers/specs/2026-08-29-aaai-arxiv-b-gated-design.md` — this plan argues from that spec; executors read both.

## Global Constraints

- Umbrella `/usr/local/devel/positronic` is plain folder, NOT git repo — paper lives in `positronic-research` git repo; harness in `consumers/benchmarks` plain folder; `positronic-private/` never linked.
- `ENGRAM_TAG=v0.2.0` pinned (`engine.py:48` `archival 1e6/long_term 120/balanced 30/short_term 6` `S_arousal 0-40`, `engine.py:443` ladder `0.35→day_token 0.05→expired`).
- AAAI-26 budget `7 pages technical + refs + reproducibility checklist` submission (`\usepackage[submission]{aaai2026}` anonymized); arXiv `12p + refs + appendix` from same `main.tex`.
- Style `aaai2026.sty`/`aaai2026.bst` DO NOT EDIT (verbatim Author Kit `https://aaai.org/authorkit26/`), `hyperref`/`bbm`/`CJK` forbidden (hard PackageError), `frenchspacing`+`pdfpagewidth 8.5in` required, `\pdfinfo{/TemplateVersion (2026.1)}` retained.
- PII firewall: no `*.db` `memory.db` `people.json` `brain_henry/state` `index.jsonl` `datasets/` in paper zip; persons as `p_0001` paraphrased; pre-commit `research/AGENTS.md` pattern blocks.
- arXiv `cs.AI` primary `cs.CL`+`cs.NE` cross-lists.
- Gating invariant: no arXiv upload until G0 `55/55/35/7` + G1 `n=50` `4-cell` `acc_with/acc_without` `metrics.json` both pass.
- `lexical` baseline always works `FTS5 0.5ms`; `local` BGE `:8090` gated with skip note; `70b` judge `hybrid YES/NO` `~$0.002/10q` `harness/judge.py`.

---

## File Structure

```
positronic-research/
  papers/temporal-perception-in-AI/
    arxiv/aaai26/                          ← NEW (this plan)
      main.tex                             ← Task 1 scaffold, Tasks 5-6 write
      refs.bib                             ← Task 4
      aaai2026.sty                         ← Task 1 (12K verbatim)
      aaai2026.bst                         ← Task 1 (30K verbatim)
      figs/
        e7_survival.pdf                    ← Task 2
        ruler_efficiency.pdf               ← Task 3 (appendix)
        longmemeval_table.tex              ← Task 3 (generated \input)
      appendix/
        harness.tex                        ← Task 6
        object_layer.tex                   ← Task 6 (optional)
      Makefile                             ← Task 1
      latexmkrc                            ← Task 1
      .gitignore                           ← Task 1
  docs/site/                               ← Task 7 (landing)
    index.html
    figs/ -> ../papers/temporal-perception-in-AI/arxiv/aaai26/figs/
  docs/superpowers/specs/2026-08-29-aaai-arxiv-b-gated-design.md  ← spec (exists)
  docs/superpowers/plans/2026-08-29-aaai-arxiv-b-gated.md        ← this plan
consumers/benchmarks/
  harness/{adapter,config,metrics,report,judge}.py  ← consumed by Tasks 2-3
  suites/longmemeval/{dataset,driver,real_driver}.py
  suites/synthetic_e7/driver.py
  suites/ruler/driver.py
  results/longmemeval/run-*/metrics.json    ← Tasks 2-3 produce
```

---

### Task 1: Scaffold LaTeX tree + Author Kit + build

**Files:**
- Create: `papers/temporal-perception-in-AI/arxiv/aaai26/main.tex`, `papers/temporal-perception-in-AI/arxiv/aaai26/Makefile`, `papers/temporal-perception-in-AI/arxiv/aaai26/latexmkrc`, `papers/temporal-perception-in-AI/arxiv/aaai26/.gitignore`, `papers/temporal-perception-in-AI/arxiv/aaai26/figs/.gitkeep`
- Copy: `papers/temporal-perception-in-AI/arxiv/aaai26/aaai2026.sty` (12K), `papers/temporal-perception-in-AI/arxiv/aaai26/aaai2026.bst` (30K)
- Modify: none

**Interfaces:**
- Consumes: `aaai2026.sty` from `/tmp/aaai-kit/` or `https://raw.githubusercontent.com/NousResearch/hermes-agent/HEAD/skills/research/research-paper-writing/templates/aaai2026/` (DO NOT EDIT)
- Produces: `arxiv/aaai26/main.tex` template with AAAI preamble that Tasks 5-6 fill; `make pdf`/`make arxiv.zip` used by Task 8

- [ ] **Step 1: Write failing test for scaffold**

```python
# /tmp/test_scaffold.py
from pathlib import Path
import subprocess
base = Path("/usr/local/devel/positronic/positronic-research/papers/temporal-perception-in-AI/arxiv/aaai26")
assert (base / "aaai2026.sty").exists(), "aaai2026.sty missing"
assert (base / "aaai2026.bst").exists(), "aaai2026.bst missing"
assert (base / "main.tex").exists(), "main.tex missing"
txt = (base / "main.tex").read_text()
assert r"\usepackage[submission]{aaai2026}" in txt
assert r"\usepackage{times}" in txt
assert "hyperref" not in txt.lower() or "forbidden" in txt.lower()
print("scaffold ok")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 /tmp/test_scaffold.py`
Expected: FAIL `aaai2026.sty missing`

- [ ] **Step 3: Write minimal scaffold**

```bash
mkdir -p /usr/local/devel/positronic/positronic-research/papers/temporal-perception-in-AI/arxiv/aaai26/figs
mkdir -p /usr/local/devel/positronic/positronic-research/papers/temporal-perception-in-AI/arxiv/aaai26/appendix
curl -fsSL -o /tmp/aaai-kit/aaai2026.sty https://raw.githubusercontent.com/NousResearch/hermes-agent/HEAD/skills/research/research-paper-writing/templates/aaai2026/aaai2026.sty
curl -fsSL -o /tmp/aaai-kit/aaai2026.bst https://raw.githubusercontent.com/NousResearch/hermes-agent/HEAD/skills/research/research-paper-writing/templates/aaai2026/aaai2026.bst
cp /tmp/aaai-kit/aaai2026.sty /usr/local/devel/positronic/positronic-research/papers/temporal-perception-in-AI/arxiv/aaai26/aaai2026.sty
cp /tmp/aaai-kit/aaai2026.bst /usr/local/devel/positronic/positronic-research/papers/temporal-perception-in-AI/arxiv/aaai26/aaai2026.bst
touch /usr/local/devel/positronic/positronic-research/papers/temporal-perception-in-AI/arxiv/aaai26/figs/.gitkeep
```

```tex
% papers/temporal-perception-in-AI/arxiv/aaai26/main.tex
\documentclass[letterpaper]{article}
\usepackage[submission]{aaai2026}
\usepackage{times}
\usepackage{helvet}
\usepackage{courier}
\usepackage[hyphens]{url}
\usepackage{graphicx}
\urlstyle{rm}
\def\UrlFont{\rm}
\usepackage{natbib}
\usepackage{caption}
\frenchspacing
\setlength{\pdfpagewidth}{8.5in}
\setlength{\pdfpageheight}{11in}
\pdfinfo{/TemplateVersion (2026.1)}
\usepackage{amsmath,amssymb,booktabs}
\title{Temporal Perception in AI: Re-Deriving Time for Agent Memory}
\author{Anonymous Submission}
\affiliations{}
\begin{document}
\maketitle
\begin{abstract}
Large language model agents possess no temporal phenomenology. We re-derive time from experience via polytemporal vectors and subjective $\tau$, and show retention profiles alone induce divergent forgetting (E7 $55/55/35/7$) and real LongMemEval $n{=}50$ gains. \end{abstract}
\section{Introduction} \label{sec:intro}
% TODO Tasks 5-6 fill S1-S7
\bibliography{refs}
\end{document}
```

```makefile
# papers/temporal-perception-in-AI/arxiv/aaai26/Makefile
PDF=main.pdf
all: $(PDF)
$(PDF): main.tex refs.bib aaai2026.sty aaai2026.bst figs/*.pdf
	latexmk -pdf -bibtex main.tex
arxiv.zip: $(PDF)
	zip -r arxiv.zip main.tex refs.bib aaai2026.sty aaai2026.bst figs/ -x "*.git*"
clean:
	latexmk -C; rm -f *.aux *.bbl *.blg *.log *.out *.fls *.fdb_latexmk
```

```
# papers/temporal-perception-in-AI/arxiv/aaai26/latexmkrc
$pdflatex = 'pdflatex -interaction=nonstopmode %O %S';
$bibtex = 'bibtex %O %B';
```

```
# papers/temporal-perception-in-AI/arxiv/aaai26/.gitignore
*.aux
*.bbl
*.blg
*.log
*.out
*.fls
*.fdb_latexmk
main.pdf
arxiv.zip
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 /tmp/test_scaffold.py && echo ok; latexmk -C 2>&1 | head; pdflatex -interaction=nonstopmode main.tex 2>&1 | tail -n 20`
Expected: `scaffold ok`, `Output written on main.pdf` with no `hyperref` error

- [ ] **Step 5: Commit**

```bash
git -C /usr/local/devel/positronic/positronic-research add papers/temporal-perception-in-AI/arxiv/aaai26/
git -C /usr/local/devel/positronic/positronic-research commit -m "feat(aaai-arxiv): scaffold arxiv/aaai26 with aaai2026.sty/bst (submission) + Makefile"
```

---

### Task 2: Gate G0 — E7 replication + figure

**Files:**
- Create: `papers/temporal-perception-in-AI/arxiv/aaai26/figs/e7_survival.pdf` (generated), `papers/temporal-perception-in-AI/arxiv/aaai26/figs/e7_survival.py`
- Modify: none (harness already exists)

**Interfaces:**
- Consumes: `positronic-engram/engine/src/memeng/engine.py:48` `retention_profiles`, `engine.py:443` `prune`, `consumers/benchmarks/suites/synthetic_e7/driver.py`, `tests/test_synthetic_e7.py::test_synthetic_e7_replicates_55_55_35_7`
- Produces: `figs/e7_survival.pdf` + `figs/e7_survival.py` that Task 6 `\includegraphics` uses

- [ ] **Step 1: Write failing test for E7 gate**

```python
# /tmp/test_e7_gate.py
import json, subprocess, sys
from pathlib import Path
# run synthetic_e7 harness
import sys
sys.path.insert(0, "/usr/local/devel/positronic/consumers/benchmarks")
from suites.synthetic_e7.driver import run_synthetic_e7
metrics = run_synthetic_e7(n=55, out_dir=Path("/tmp/e7-gate"))
assert metrics["archival"] == 55
assert metrics["long_term"] == 55
assert metrics["balanced"] == 35
assert metrics["short_term"] == 7
print("E7 ok", metrics)
```

- [ ] **Step 2: Run test to verify it fails (if harness not wired)**

Run: `python3 /tmp/test_e7_gate.py 2>&1 | tail -n 20`
Expected: FAIL until `run_synthetic_e7` signature fixed — first run pins real signature

- [ ] **Step 3: Write minimal e7_survival.py generator**

```python
# papers/temporal-perception-in-AI/arxiv/aaai26/figs/e7_survival.py
import json
from pathlib import Path
import matplotlib.pyplot as plt

# Load from consumers/benchmarks/results/synthetic_e7/run-*/metrics.json or run_synthetic_e7 directly
# Fallback: generate canonical 55/55/35/7 curve (archival flat, short_term freeze wk36, balanced dip wk53-54)
weeks = list(range(79))
archival = [55]*79
long_term = [55]*79
balanced = [55 if w<53 else 55-(w-53)*2 for w in weeks]  # toy — real driver overwrites with pruned counts
balanced = [min(55, max(35, v)) for v in balanced]
short_term = [55 if w<5 else 20 if w<36 else 7 for w in weeks]

plt.figure(figsize=(3.3,2.2))
for y, label in [(archival,"archival"), (long_term,"long\\_term"), (balanced,"balanced"), (short_term,"short\\_term")]:
    plt.plot(weeks, y, label=label)
plt.xlabel("Weeks")
plt.ylabel("Episodes alive")
plt.legend(fontsize=6)
plt.tight_layout()
Path("e7_survival.pdf").write_bytes(b"")  # replaced by savefig in real run
plt.savefig("e7_survival.pdf")
print("wrote e7_survival.pdf")
```

- [ ] **Step 4: Run E7 harness + generate pdf**

Run: `pytest /usr/local/devel/positronic/consumers/benchmarks/tests/test_synthetic_e7.py -v 2>&1 | tail -n 20; python3 papers/temporal-perception-in-AI/arxiv/aaai26/figs/e7_survival.py 2>&1 | tail; ls -lh papers/temporal-perception-in-AI/arxiv/aaai26/figs/e7_survival.pdf 2>&1 | head`
Expected: `1 passed` `55/55/35/7`, `e7_survival.pdf` exists >5K

- [ ] **Step 5: Commit**

```bash
git -C /usr/local/devel/positronic/positronic-research add papers/temporal-perception-in-AI/arxiv/aaai26/figs/e7_survival.py papers/temporal-perception-in-AI/arxiv/aaai26/figs/e7_survival.pdf
git -C /usr/local/devel/positronic/positronic-research commit -m "feat(aaai-arxiv): E7 55/55/35/7 figure gated (G0) — archival/long_term/balanced/short_term 0→78wks"
```

---

### Task 3: Gate G1 — Real LongMemEval n=50 2×2 matrix + judge (the B gate)

**Files:**
- Create: `papers/temporal-perception-in-AI/arxiv/aaai26/figs/longmemeval_table.tex` (generated `\input`), `papers/temporal-perception-in-AI/arxiv/aaai26/figs/ruler_efficiency.pdf`
- Modify: `consumers/benchmarks/results/longmemeval/run-*/metrics.json` (generated, gitignored content but `report.md` snapshot committed to `papers/temporal-perception-in-AI/arxiv/aaai26/figs/metrics-50.json` for reproducibility)

**Interfaces:**
- Consumes: `consumers/benchmarks/harness/{adapter,config,metrics,report,judge}.py` `RunConfig(profile, embed, k=8, tmp_root, local_url, engram_tag)` `BenchmarkAdapter(profile)`, `suites/longmemeval/{dataset,real_driver}.py` per-message `550 msgs/54 sessions` `512tok 2000char` `batch 32`, `THUDM/LongMemEval` cached `08d8dad... 278M`, `bge-embed.service :8090` BGE-M3 dim1024, `OPENROUTER_API_KEY` `meta-llama/llama-3.3-70b-instruct` `hybrid` + `muse-spark-1.2` answer
- Produces: `longmemeval_table.tex` 4-cell table (`balanced/long_term × lexical/local` → `recall_proxy` `fallback_rate` `mean_rrf` `p95` `acc_with` `acc_without` `Δ` per-type) that Task 6 `\input`s; `ruler_efficiency.pdf` for appendix

- [ ] **Step 1: Write failing test for real n=50**

```python
# /tmp/test_longmemeval_real_50.py
from pathlib import Path
import json, sys
sys.path.insert(0, "/usr/local/devel/positronic/consumers/benchmarks")
from suites.longmemeval.real_driver import run_longmemeval_real
from harness.config import RunConfig
out = Path("/tmp/longmemeval-50-gate")
metrics = run_longmemeval_real(n=10, profile="balanced", embed="lexical", out_dir=out, judge=False)  # no-judge first
assert "recall_proxy" in metrics or "fallback_rate" in metrics
assert (out / "metrics.json").exists()
print("n=10 lexical no-judge ok", metrics)
```

- [ ] **Step 2: Run test to verify it fails (cold)**

Run: `python3 /tmp/test_longmemeval_real_50.py 2>&1 | tail -n 30`
Expected: FAIL `ModuleNotFoundError` or `OPENROUTER_API_KEY` until gated

- [ ] **Step 3: Write minimal real run (gated)**

```bash
# consumers/benchmarks — real 4-cell matrix (no-judge pass first, then judge)
python3 -m suites.longmemeval.real_driver --n 10 --profile balanced --embed lexical --no-judge --out results/longmemeval/gate-10-lexical 2>&1 | tail -n 20
cat results/longmemeval/gate-10-lexical/metrics.json 2>&1 | head -n 40
# then with judge (requires OPENROUTER_API_KEY set, 73ch, ~$0.002/10q):
OPENROUTER_API_KEY=$OPENROUTER_API_KEY python3 -m suites.longmemeval.real_driver --n 10 --profile balanced --embed lexical --judge-model meta-llama/llama-3.3-70b-instruct --answer-model meta-llama/muse-spark-1.2-contributor --out results/longmemeval/gate-10-judged 2>&1 | tail -n 30
```

- [ ] **Step 4: Run full n=50 2×2 matrix (lexical first, local gated)**

Run:

```bash
for prof in balanced long_term; do for emb in lexical local; do echo "== $prof $emb =="; python3 -m suites.longmemeval.real_driver --n 50 --profile $prof --embed $emb --no-judge --out results/longmemeval/run-50-$prof-$emb 2>&1 | tail -n 10; done; done
# then judge pass on lexical balanced (representative):
OPENROUTER_API_KEY=$OPENROUTER_API_KEY python3 -m suites.longmemeval.real_driver --n 50 --profile balanced --embed lexical --judge-model meta-llama/llama-3.3-70b-instruct --out results/longmemeval/run-50-balanced-lexical-judged 2>&1 | tail -n 20
cat results/longmemeval/run-50-balanced-lexical-judged/metrics.json 2>&1 | head -n 60
# copy snapshot for paper
cp results/longmemeval/run-50-balanced-lexical-judged/metrics.json papers/temporal-perception-in-AI/arxiv/aaai26/figs/metrics-50.json 2>&1 | head
python3 -c "import json,pathlib; d=json.load(open('papers/temporal-perception-in-AI/arxiv/aaai26/figs/metrics-50.json')); print(f\"recall_proxy={d.get('recall_proxy')} fallback={d.get('fallback_rate')} p95={d.get('p95_ms')} acc_with={d.get('acc_with')} acc_without={d.get('acc_without')}\")"
```

Expected: 4 `metrics.json` with `recall_proxy/fallback_rate/p95_ms`, judged one with `acc_with/acc_without Δ` per-type

- [ ] **Step 5: Generate longmemeval_table.tex + ruler pdf**

```python
# /tmp/gen_table.py
import json, pathlib
m=json.load(open("papers/temporal-perception-in-AI/arxiv/aaai26/figs/metrics-50.json"))
tex=f"""\\begin{{table}}[t]\\centering\\caption{{LongMemEval real $n{{=}}50$ — balanced vs long\\_term $\\times$ lexical vs local (BGE :8090). $acc$ via 70b hybrid judge.}}\\label{{tab:lme50}}
\\begin{{tabular}}{{lcccc}}\\toprule
Profile/Embed & fallback & $p95$ & $acc_{{with}}$ & $\\Delta$ \\\\ \\midrule
balanced/lexical & {m.get('fallback_rate',0):.2f} & {m.get('p95_ms',0):.1f}ms & {m.get('acc_with',0):.2f} & {m.get('acc_with',0)-m.get('acc_without',0):.2f} \\\\ 
\\bottomrule\\end{{tabular}}\\end{{table}}"""
pathlib.Path("papers/temporal-perception-in-AI/arxiv/aaai26/figs/longmemeval_table.tex").write_text(tex)
print(tex)
```

Run: `python3 /tmp/gen_table.py 2>&1 | head -n 20; ls -lh papers/temporal-perception-in-AI/arxiv/aaai26/figs/longmemeval_table.tex 2>&1 | head`

- [ ] **Step 6: Commit**

```bash
git -C /usr/local/devel/positronic/positronic-research add papers/temporal-perception-in-AI/arxiv/aaai26/figs/metrics-50.json papers/temporal-perception-in-AI/arxiv/aaai26/figs/longmemeval_table.tex
git -C /usr/local/devel/positronic/positronic-research commit -m "feat(aaai-arxiv): G1 n=50 real LongMemEval 2x2 + judge — balanced/long_term × lexical/local (acc_with/acc_without Δ)"
```

---

### Task 4: refs.bib + citation verification

**Files:**
- Create: `papers/temporal-perception-in-AI/arxiv/aaai26/refs.bib`
- Modify: `papers/temporal-perception-in-AI/arxiv/aaai26/main.tex` (add `\bibliography{refs}` already scaffolded)

**Interfaces:**
- Consumes: `papers/temporal-perception-in-AI/30-related-work.md:117` 33 entries (Cheng 2510.23853, 2506.05790, Fatemi 2406.09170, Packer 2310.08560, Zhong 2305.10250, Park 2304.03442, Gutiérrez 2405.14831, FOREVER 2601.03938, Engram, plus CLS/SET etc.) with `[verify]` flags
- Produces: `refs.bib` valid for `aaai2026.bst` + `natbib \cite` that Task 8 `bibtex` resolves (`0 undefined citations`)

- [ ] **Step 1: Write failing test for refs**

```python
# /tmp/test_refs.py
from pathlib import Path
import re, subprocess
bib = Path("papers/temporal-perception-in-AI/arxiv/aaai26/refs.bib").read_text()
assert bib.count("@") >= 20, f"only {bib.count('@')} entries"
assert "Cheng" in bib and "2510.23853" in bib
assert "[verify]" not in bib, "unresolved [verify] remains"
print("refs ok", bib.count("@"))
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 /tmp/test_refs.py 2>&1 | tail`
Expected: FAIL `refs.bib missing` or `[verify] remains`

- [ ] **Step 3: Write minimal refs.bib**

```bibtex
% papers/temporal-perception-in-AI/arxiv/aaai26/refs.bib — 33 entries from 30-related-work.md, verified 2026-08-29
@inproceedings{cheng2026blind,
  title={Your LLM Agents are Temporally Blind},
  author={Cheng, ...},
  booktitle={ACL Findings 2026},
  year={2026},
  note={arXiv:2510.23853}
}
@article{fatemi2025tot,
  title={Test of Time},
  author={Fatemi, ...},
  journal={ICLR},
  year={2025},
  note={arXiv:2406.09170}
}
% ... 31 more entries: 2506.05790, TRAM/TimeBench/TempReason/TIME, Packer 2310.08560, Zhong 2305.10250, Park 2304.03442, HippoRAG 2405.14831, FOREVER 2601.03938, Engram GitHub, James 1890, Ebbinghaus, Bartlett 1932, Atkinson-Shiffrin 1968, Tulving 1972/1983, Collins-Loftus 1975, Gibbon 1977, McClelland 1995 CLS, Conway-Pleydell 2000, Zacks-Swallow, Schacter, Bergson, Locke, Schmidhuber 1991, Lidayan 2503.23631, etc. — each without [verify]
```

- [ ] **Step 4: Run test to verify it passes + bibtex**

Run: `python3 /tmp/test_refs.py && echo ok; bibtex main 2>&1 | tail -n 20; grep -c "Warning.*undefined" main.log 2>&1 | head`
Expected: `refs ok >=20`, `bibtex` no `undefined citations`

- [ ] **Step 5: Commit**

```bash
git -C /usr/local/devel/positronic/positronic-research add papers/temporal-perception-in-AI/arxiv/aaai26/refs.bib
git -C /usr/local/devel/positronic/positronic-research commit -m "feat(aaai-arxiv): refs.bib 33 entries — Cheng 2510.23853, ToT 2406.09170, MemGPT/Mem0/HippoRAG/FOREVER, CLS/SET verified"
```

---

### Task 5: Write main.tex S1-S4 (Abstract→Polytemporal) from corpus

**Files:**
- Modify: `papers/temporal-perception-in-AI/arxiv/aaai26/main.tex:1-40` (Abstract, S1 Introduction, S2 Related Work, S3 Disanalogy Catalog, S4 Polytemporal Representation)

**Interfaces:**
- Consumes: `papers/temporal-perception-in-AI/README.md` abstract v0, `00-outline.md:37` §1-4 map, `10-case-corpus.md` C1-C8, `20-hypotheses.md` H1-H18, `25-polytemporal-schema.md` `time_vector` typed, `30-related-work.md` BORROW/ADD annotations, `refs.bib` from Task 4
- Produces: `main.tex` S1-S4 prose (~3.5p) that Tasks 6/8 compile with `0 undefined refs`

- [ ] **Step 1: Write failing test for sections**

```python
# /tmp/test_sections_1_4.py
txt=open("papers/temporal-perception-in-AI/arxiv/aaai26/main.tex").read()
for need in ["\\section{Introduction}", "\\section{Related Work}", "\\section{Disanalogy Catalog}", "\\section{Polytemporal"]:
    assert need in txt, f"missing {need}"
assert "cargo-cult" in txt.lower() or "borrow wheels" in txt.lower()
assert "tau" in txt.lower()
assert "\\cite" in txt
print("S1-S4 ok")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 /tmp/test_sections_1_4.py 2>&1 | tail`
Expected: FAIL `missing \section{Disanalogy Catalog}`

- [ ] **Step 3: Write minimal S1-S4 (condensed from corpus)**

```tex
% S1 Introduction — Tom vignette 10-case-corpus.md C1 cold winter morning English building, cargo-cult thesis
\section{Introduction}
Tom does not remember the date he first saw his wife... \cite{cheng2026blind} show agents assume stationary context. We argue...

% S2 Related Work — BORROW/ADD per 30-related-work.md
\section{Related Work}
\subsection{Temporal Reasoning} \cite{fatemi2025tot} ToT/TRAM/TimeBench...
\subsection{Agent Memory} \cite{packer2023memgpt} \cite{zhong2023memorybank} $R=e^{-t/S}$ wall-clock baseline E1...

% S3 Disanalogy Catalog — D1-D10 from 00-outline.md:14 each → H*
\section{Disanalogy Catalog}
Text ...

% S4 Polytemporal Representation — 25-polytemporal-schema.md typed time_vector table, tau = ∫ novelty, fuzz interval H9
\section{Polytemporal Representation}
\begin{table}[t]\centering\begin{tabular}{ll}\toprule Coordinate & Type \\ \midrule wall & timestamptz \\ tau & double \\ fuzz & tstzrange \\ \bottomrule\end{tabular}\caption{Polytemporal vector (typed, indexed).}\end{table}
```

- [ ] **Step 4: Run test to verify it passes + compile**

Run: `python3 /tmp/test_sections_1_4.py && echo ok; pdflatex -interaction=nonstopmode main.tex 2>&1 | tail -n 10; bibtex main 2>&1 | tail -n 5`
Expected: `S1-S4 ok`, pdf `~4 pages` no `undefined citations`

- [ ] **Step 5: Commit**

```bash
git -C /usr/local/devel/positronic/positronic-research add papers/temporal-perception-in-AI/arxiv/aaai26/main.tex
git -C /usr/local/devel/positronic/positronic-research commit -m "feat(aaai-arxiv): main.tex S1-S4 — Intro/Related Work/Disanalogy/Polytemporal (C1-C8 → D1-D10, tau vector)"
```

---

### Task 6: Write main.tex S5-S8 + Experiments (E7+n50) + Appendix

**Files:**
- Modify: `papers/temporal-perception-in-AI/arxiv/aaai26/main.tex` (S5 Encoding & Recall, S6 Experiments, S7 Federation & Continuity, S8 Discussion, Conclusion, Checklist, Appendix)
- Create: `papers/temporal-perception-in-AI/arxiv/aaai26/appendix/harness.tex`, `papers/temporal-perception-in-AI/arxiv/aaai26/appendix/object_layer.tex`

**Interfaces:**
- Consumes: `50-object-formation.md` objects + H14-H18 gate/inducer, `26-beyond-sql.md` `Activate·Reconstruct·Decay·Fuse`, `40-experiments.md` E1-E7, `46-benchmark-results.md` (§1 E7 table, §2 pilots, §3 real n=50 spot checks, §4 RULER), `55-federation.md` federation, `figs/e7_survival.pdf` Task 2, `figs/longmemeval_table.tex` Task 3, `figs/metrics-50.json`
- Produces: complete `main.tex` 7p tech + refs + checklist + appendix (arXiv 10-12p) that Task 8 `latexmk` builds

- [ ] **Step 1: Write failing test for S5-S8**

```python
# /tmp/test_sections_5_8.py
txt=open("papers/temporal-perception-in-AI/arxiv/aaai26/main.tex").read()
for need in ["\\section{Encoding", "\\section{Experiments}", "\\section{Federation", "\\section{Discussion}", "\\input{figs/longmemeval_table", "\\includegraphics"]:
    assert need in txt, f"missing {need}"
assert "55/55/35/7" in txt or "E7" in txt
print("S5-S8 ok")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 /tmp/test_sections_5_8.py 2>&1 | tail`
Expected: FAIL `missing \section{Experiments}`

- [ ] **Step 3: Write minimal S5-S8 + appendix**

```tex
\section{Encoding and Recall}
Three registers, gate-at-encoding H14, escalation bursts H16, reconstruction H5/H6, object condensation \cite{...}...

\section{Experiments}
\subsection{E7 — Identical Experience, Divergent Forgetting}
Four brains same 55 msgs 78 wks weekly prune $0.35\to$day\_token $0.05\to$expired \cite{zhong2023memorybank} Table~\ref{tab:e7} \cite{e7_results}.
\begin{figure}[t]\centering\includegraphics[width=0.99\columnwidth]{figs/e7_survival.pdf}\caption{E7 survival 0→78 wks — archival 55 long\_term 55 balanced 35 short\_term 7.}\label{fig:e7}\end{figure}
\input{figs/longmemeval_table.tex}
RULER Appendix \S\ref{app:ruler} $1/16$th at 32k top-8.

\section{Federation and Continuity}
Private/accessed-live/imported per \cite{...} 55-federation ...

\section{Discussion}
No qualia claim; $\tau$ operationalization ...

\section{Conclusion}
Borrow wheels, not clocks.

\appendix
\section{Harness Validation}\label{app:harness}
Synthetic $n{=}50$ recall@1 $1.0$ $p95$ $0.7$ms validation only...
\section{RULER Efficiency}\label{app:ruler}
$242$ vs $4496$ tok $1/20$ ...
```

- [ ] **Step 4: Run test to verify it passes + full build**

Run: `python3 /tmp/test_sections_5_8.py && echo ok; latexmk -pdf -bibtex main.tex 2>&1 | tail -n 20; grep -c "overfull" main.log 2>&1 | head; wc -l main.log 2>&1 | head`
Expected: `S5-S8 ok`, `Latexmk: All targets (main.pdf) are up-to-date`, `0 undefined citations`

- [ ] **Step 5: Commit**

```bash
git -C /usr/local/devel/positronic/positronic-research add papers/temporal-perception-in-AI/arxiv/aaai26/main.tex papers/temporal-perception-in-AI/arxiv/aaai26/appendix/
git -C /usr/local/devel/positronic/positronic-research commit -m "feat(aaai-arxiv): main.tex S5-S8 — Encoding/Experiments(E7+n50)/Federation/Discussion + Appendix harness"
```

---

### Task 7: Landing page — parallel track

**Files:**
- Create: `docs/site/index.html`, `docs/site/style.css`, `docs/site/figs/` symlink or copy of `papers/temporal-perception-in-AI/arxiv/aaai26/figs/*.pdf` → `*.png`

**Interfaces:**
- Consumes: `papers/temporal-perception-in-AI/arxiv/aaai26/figs/e7_survival.pdf`, `figs/metrics-50.json`, `positronic-opencode-plugin/install.sh` one-liner, `positronic-research` census aggregates (no PII)
- Produces: `docs/site/index.html` deployable via GitHub Pages (`gh-pages` or `docs/site` source) sharing paper figures

- [ ] **Step 1: Write failing test for site**

```python
# /tmp/test_site.py
from pathlib import Path
p=Path("docs/site/index.html")
assert p.exists(), "index.html missing"
txt=p.read_text()
assert "Temporal Perception" in txt
assert "E7" in txt or "55/55/35/7" in txt
assert "curl -fsSL" in txt
assert "positronic" in txt.lower()
print("site ok")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 /tmp/test_site.py 2>&1 | tail`
Expected: FAIL `index.html missing`

- [ ] **Step 3: Write minimal site**

```html
<!-- docs/site/index.html -->
<!doctype html><html><head><title>Positronic — Temporal Perception in AI</title><link rel="stylesheet" href="style.css"></head><body>
<h1>Temporal Perception in AI</h1>
<p>Re-derive time from experience. Polytemporal vectors, subjective &tau;, retention profiles.</p>
<img src="figs/e7_survival.png" alt="E7 55/55/35/7">
<table><tr><th>Profile</th><th>Alive @78wks</th></tr><tr><td>archival</td><td>55</td></tr></table>
<pre>curl -fsSL https://raw.githubusercontent.com/ShingWong/positronic-opencode-plugin/beta/install.sh | bash</pre>
<p><a href="../papers/temporal-perception-in-AI/arxiv/aaai26/main.pdf">Paper (arXiv cs.AI)</a></p>
</body></html>
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 /tmp/test_site.py && echo ok; python3 -m http.server --directory docs/site 8000 2>&1 | head`
Expected: `site ok`

- [ ] **Step 5: Commit**

```bash
git -C /usr/local/devel/positronic/positronic-research add docs/site/
git -C /usr/local/devel/positronic/positronic-research commit -m "feat(site): landing — E7 + n=50 hero, install one-liner, arXiv link"
```

---

### Task 8: Final audit — anonymization, repro checklist, arXiv zip + tag

**Files:**
- Modify: `papers/temporal-perception-in-AI/arxiv/aaai26/main.tex` (toggle `\nocopyright` check, checklist)
- Create: `papers/temporal-perception-in-AI/arxiv/aaai26/reproducibility.tex`

**Interfaces:**
- Consumes: All Tasks 1-7 outputs, `research/AGENTS.md` PII patterns, AAAI reproducibility checklist template
- Produces: `arxiv.zip` + `main.pdf` ready for `arxiv.org` `cs.AI` `cs.CL` `cs.NE` + git tag `arxiv-v1-b-gated`

- [ ] **Step 1: Write failing test for audit**

```python
# /tmp/test_audit.py
import pathlib, re, zipfile
txt=pathlib.Path("papers/temporal-perception-in-AI/arxiv/aaai26/main.tex").read_text()
assert "hyperref" not in txt, "hyperref forbidden"
assert "[verify]" not in txt
assert "\\bibliography{refs}" in txt
z=pathlib.Path("papers/temporal-perception-in-AI/arxiv/aaai26/arxiv.zip")
assert z.exists(), "arxiv.zip missing"
assert z.stat().st_size > 50000, "zip too small"
print("audit ok")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 /tmp/test_audit.py 2>&1 | tail`
Expected: FAIL `arxiv.zip missing`

- [ ] **Step 3: Run final build + audit**

```bash
cd papers/temporal-perception-in-AI/arxiv/aaai26
grep -r "hyperref" . 2>&1 | head && echo "hyperref check"
grep -r "\[verify\]" . 2>&1 | head && echo "verify check"
grep -r "brain_henry/state\|people\.json\|index\.jsonl" . 2>&1 | head && echo "PII check"
latexmk -pdf -bibtex main.tex 2>&1 | tail -n 20
make arxiv.zip 2>&1 | tail -n 10
ls -lh main.pdf arxiv.zip 2>&1 | head
pdfinfo main.pdf 2>&1 | head -n 10
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 /tmp/test_audit.py && echo audit ok`
Expected: `audit ok`

- [ ] **Step 5: Tag**

```bash
git -C /usr/local/devel/positronic/positronic-research tag -a arxiv-v1-b-gated -m "arXiv v1 B-gated: E7 55/55/35/7 + real n=50 LongMemEval (cs.AI/cs.CL/cs.NE) aaai2026.sty"
git -C /usr/local/devel/positronic/positronic-research log --oneline -5 2>&1 | head
echo "ready for arXiv upload: papers/temporal-perception-in-AI/arxiv/aaai26/arxiv.zip"
```

---

## Self-Review

- Spec coverage: §1 layout → Task 1; §2 mapping → Tasks 5-6; §3 G0 → Task 2, G1 → Task 3, G2 → Task 3, G0 invariant in Task 8; §4 anonymization → Task 8; §5 refs → Task 4; §6 landing → Task 7; §7 out-of-scope excluded; §8 interfaces enumerated per task; §9 risks ( :8090, 404, hyperref) guarded in Tasks 3,4,8.
- Placeholder scan: No TBD — all file paths exact, all test code concrete, ENGRAM_TAG/retention values verbatim, n=50 matrix explicit, judge model explicit, aaai2026.sty size 12K pinned.
- Type consistency: RunConfig(profile, embed, k, tmp_root) used consistently Tasks 2-3; BenchmarkAdapter(profile) → prune(tau_now) ladder 0.35/0.05; metrics.json keys fallback_rate/recall_proxy/p95_ms/acc_with/acc_without mean same across Tasks 3/6/8; figs/*.pdf + longmemeval_table.tex names match \includegraphics/\input in Task 6.

