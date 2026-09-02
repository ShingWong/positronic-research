# Paper Split — arXiv vs AAAI26 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fork the single `arxiv/aaai26/main.tex` into two diverging papers — arXiv (long form, full theory, non-blind) and AAAI26 (7-page empirical core, double-blind) — with the E1 decay-ablation result in both.

**Architecture:** Two sibling paper directories under `papers/temporal-perception-in-AI/`. Each is self-contained (own `main.tex`, `refs.bib`, `.sty/.bst`, `figs/`, `appendix/`, `Makefile`). Shared assets are copied, not symlinked, so the papers diverge independently. The old `arxiv/aaai26/` path is removed after both build.

**Tech Stack:** LaTeX (latexmk/pdflatex, bibtex), `aaai2026.sty`, matplotlib figure generators (`figs/*.py`), the E1 results in `../positronic-prism/experiments/decay_ablation/`.

**Spec:** `docs/superpowers/specs/2026-09-02-paper-split-arxiv-aaai26-design.md`

## Global Constraints

- arXiv keeps author `\author{Shing Wong}` (non-blind). AAAI26 is double-blind: NO author, NO affiliation, NO AAAI copyright strip.
- AAAI26 main body: NO `:8090`, `:8080`, `renderD128`, `gfx906`, `/usr/local/devel/models` (they live in the appendix or are generalized to "dual Intel Xeon CPUs with AMD Vega accelerators using llama.cpp and BGE-M3 embeddings").
- Both papers must contain the E1 decay-ablation 2×2 matrix (tau 35/55 vs wall 0/55 on burst-quiet; uniform parity 35/55).
- Both papers must contain LongMemEval 0.90/0.12 (Δ0.78), E7 55/55/35/11, RULER 1/10–1/74.
- Stale numbers forbidden: `0.58`, `0.44`, `55/55/35/7` (and `short_term 7`).
- AAAI26 must compile to ≤7 pages, 0 errors. arXiv may be ~10–14 pages, 0 errors.
- `aaai2026.sty` is NOT modified.

---

### Task 1: Fork the directory structure + shared assets

**Files:**
- Create: `papers/temporal-perception-in-AI/arxiv/` (dir)
- Create: `papers/temporal-perception-in-AI/aaai26/` (dir)
- Copy: current `arxiv/aaai26/main.tex`, `refs.bib`, `aaai2026.sty`, `aaai2026.bst`, `latexmkrc`, `Makefile`, `figs/*`, `appendix/*`, `.gitignore` → into **both** new dirs.
- Modify: each copy's `Makefile` if the `$(PDF)` target or relative paths need adjusting (they should not — same relative layout).

**Interfaces:**
- Produces: two independent paper dirs, each with `main.tex` = identical copy of the current paper (baseline for divergence).

- [ ] **Step 1: Create the two sibling directories and copy the current paper tree into both**

```bash
cd /usr/local/devel/positronic/positronic-research/papers/temporal-perception-in-AI
SRC=arxiv/aaai26
for DST in arxiv aaai26; do
  mkdir -p "$DST"
  cp -r "$SRC/main.tex" "$SRC/refs.bib" "$SRC/aaai2026.sty" "$SRC/aaai2026.bst" \
     "$SRC/latexmkrc" "$SRC/Makefile" "$SRC/.gitignore" "$DST/"
  mkdir -p "$DST/figs" "$DST/appendix"
  cp "$SRC/figs/"* "$DST/figs/"
  cp "$SRC/appendix/"* "$DST/appendix/"
done
```

- [ ] **Step 2: Verify both new dirs are complete copies**

Run: `diff -q arxiv/main.tex arxiv/aaai26/main.tex && diff -q arxiv/aaai26/main.tex aaai26/main.tex && ls arxiv/figs aaai26/figs`
Expected: identical main.tex; both `figs/` contain `e7_survival.pdf`, `e7_survival.py`, `longmemeval_table.tex`, `metrics-50.json`, `ruler_efficiency.pdf`, `ruler_efficiency.py`.

- [ ] **Step 3: Commit**

```bash
git add arxiv aaai26
git commit -m "refactor(papers): fork arxiv/aaai26 into arxiv/ + aaai26/ sibling trees

Identical copies to start; each diverges toward its venue. Old
arxiv/aaai26/ removed once both build."
```

---

### Task 2: arXiv — baseline builds standalone

**Files:**
- Modify: `papers/temporal-perception-in-AI/arxiv/Makefile` (no change expected — verify)

**Interfaces:**
- Consumes: Task 1's copied tree.
- Produces: a compiling `arxiv/main.pdf` as the fork baseline.

- [ ] **Step 1: Build the arXiv fork from the copied tree**

Run: `cd arxiv && make 2>&1 | tail -5`
Expected: `Output written on main.pdf` — the arXiv fork is a working baseline.

- [ ] **Step 2: Commit (if any Makefile fix needed; otherwise skip)**

```bash
cd arxiv && git add Makefile 2>/dev/null && git commit -m "chore(arxiv): baseline build" 2>/dev/null || echo "no change"
```

---

### Task 3: arXiv — add the exhaustive C→D→H→Test table

**Files:**
- Modify: `papers/temporal-perception-in-AI/arxiv/main.tex` (insert new subsection after the Disanalogy Catalog, ~line 75)
- Source: `../10-case-corpus.md`, `../20-hypotheses.md`, `../40-experiments.md` for the enumeration.

**Interfaces:**
- Consumes: the existing D1–D10 paragraphs and C1–C8 cases already in the paper.
- Produces: `\label{tab:cdh}` — the exhaustive mapping table, referenced by later tasks' text.

- [ ] **Step 1: Insert the C→D→H→Test table after the last D10 paragraph**

Add after line 75 (`\paragraph{D10 ...}`), before `\section{Polytemporal Representation}`:

```latex
\subsection{The Case–Disanalogy–Hypothesis Map}
Table~\ref{tab:cdh} enumerates the full mapping from case vectors to
disanalogies to falsifiable hypotheses to operational tests. The cases are
specification test-vectors (C1--C8); the hypotheses are the falsifiable claims
(H1--H18, H-$\tau$); each row's test is the experiment that would falsify it.

\begin{table*}[t]\centering\small
\caption{Case $\to$ Disanalogy $\to$ Hypothesis $\to$ Operational test.}
\label{tab:cdh}
\begin{tabular}{@{}p{0.8cm}p{2.4cm}p{5.2cm}p{5.2cm}@{}}
\toprule
C & Disanalogy (D) & Hypothesis (H) & Operational test \\
\midrule
C1 & D1 texture-vs-timestamp; D2 salience-gated durability & H1, H2 &
    texture-indexed retrieval beats date-range on human probes;
    flashbulb tier survives decay \\
C1--C2 & D2; D5 reconstruction-vs-lookup & H2, H5, H6 &
    arousal sets durability tier at write-time; intrusions cluster as
    schema-consistent \\
C3 & D4 schema-fusion-vs-hoarding & H4, H14 & storage grows $\sim\log$;
    routine recall correctly fails per-instance \\
C5 & D3 anchored-constellations; D9 landmark-relative dating & H3, H9 &
    ``when'' answered by anchor traversal; interval width tracks error \\
C6, C8 & D6 subjective-time-density & H-$\tau$ (E1) &
    \textbf{E1 ablation:} $\tau$-keyed vs wall-keyed decay on
    burst-quiet stream --- $\tau$ preserves, wall purges \\
C8 & D7 continuity-vs-discontinuity; D10 precision-as-confidence &
    H11--H13, H9 & gap-provenance; reported width $=$ confidence \\
C2, C7 & D9, D10 & H9 & calibrated-confidence interval widths \\
C1, C3, C5 & D2, D4, D3 & H2, H4, H3 & salience tier, fusion, anchors \\
-- & D8 drives & H8/H-$\tau$ & curiosity/boredom gates encoding cadence \\
\bottomrule
\end{tabular}
\end{table*}
```

- [ ] **Step 2: Compile to verify the table parses**

Run: `cd arxiv && latexmk -pdf -bibtex main.tex 2>&1 | grep -E "Output written|Error"`
Expected: `Output written on main.pdf`, no `Error` lines.

- [ ] **Step 3: Commit**

```bash
git add main.tex
git commit -m "feat(arxiv): exhaustive C->D->H->test mapping table (resolves phantom refs)
"
```

---

### Task 4: arXiv — add the E1 decay-ablation section

**Files:**
- Modify: `papers/temporal-perception-in-AI/arxiv/main.tex` (in Experiments, after the LongMemEval/Token-reduction paragraphs, ~line 117)
- Source: `../positronic-prism/experiments/decay_ablation/report.md` (the 2×2 matrix).

**Interfaces:**
- Consumes: Task 3's compiled baseline.
- Produces: `\label{tab:e1}` — the E1 2×2 matrix table in the arXiv Experiments section.

- [ ] **Step 1: Insert the E1 ablation subsection after the Token-reduction paragraph**

Add after line 117 (the token-reduction paragraph), before the RULER figure:

```latex
\paragraph{Decay ablation (E1): $\tau$-keyed vs wall-clock-keyed decay.}
The strongest confound test is not retrieval quality but the decay clock
itself. We replay identical $55$-event streams through two engines that differ
\textbf{only} in the clock driving the prune ladder (Eq.~decay):
polytemporal $\tau$ (novelty-integrated) vs.\ wall-clock $t$
(MemoryBank-style $R=e^{-t/S}$). On a uniform stream (control) the two clocks
are calibrated to retain identically ($S_{\text{wall}}=340$~d at $n{=}55$);
on a burst-quiet stream (all $55$ events in the first $2$ weeks, then $76$
quiet weeks) they diverge completely (Table~\ref{tab:e1}).

\begin{table}[t]\centering\caption{E1 decay ablation (E7's $n{=}55$, $78$~wks,
balanced profile): identical streams, only the decay clock differs.}
\label{tab:e1}
\begin{tabular}{@{}llcc@{}}
\toprule
Stream & Metric & $\tau$-decay & Wall-decay \\
\midrule
uniform (control) & retention & 35/55 & 35/55 \\
uniform (control) & retrieval & 1.00 & 1.00 \\
burst-quiet (stress) & retention & \textbf{35/55} & \textbf{0/55} \\
burst-quiet (stress) & retrieval & \textbf{1.00} & \textbf{0.00} \\
\bottomrule
\end{tabular}
\end{table}

After an eventful burst followed by equal wall duration of quiet, wall-clock
decay purges the entire burst ($0/55$) while $\tau$-decay preserves it
($35/55$, retrievable $1.0$): on equal wall time, \emph{wall forgets, $\tau$
remembers}. This isolates the decay clock as the causal variable --- not the
embedding, not the retrieval, not the answer model.
```

- [ ] **Step 2: Compile**

Run: `cd arxiv && latexmk -pdf -bibtex main.tex 2>&1 | grep -E "Output written|Error"`
Expected: `Output written`, no `Error`.

- [ ] **Step 3: Commit**

```bash
git add main.tex
git commit -m "feat(arxiv): E1 decay-ablation 2x2 matrix (tau preserves, wall purges on burst-quiet)"
```

---

### Task 5: arXiv — add the n=500 roadmap sentence to Discussion

**Files:**
- Modify: `papers/temporal-perception-in-AI/arxiv/main.tex` (Discussion / Validity threats, ~line 130)

**Interfaces:**
- Consumes: Task 4 baseline.
- Produces: the arXiv's "next phase" framing for the n=500 run.

- [ ] **Step 1: Append the roadmap sentence to the validity-threats paragraph**

Add at the end of the existing `Validity threats.` paragraph:

```latex
 The $n{=}50$ single-session slice is the proof-of-concept bound; the full
$500$-question, six-type LongMemEval suite is the targeted next phase,
alongside a salience-gated burst variant of the E1 ablation and a
continuously-observing fleet deployment for the D7 substrate claim.
```

- [ ] **Step 2: Compile**

Run: `cd arxiv && latexmk -pdf -bibtex main.tex 2>&1 | grep -E "Output written|Error"`

- [ ] **Step 3: Commit**

```bash
git add main.tex
git commit -m "docs(arxiv): n=500 + fleet roadmap in discussion"
```

---

### Task 6: AAAI26 — strip to the empirical core (thesis not theory)

**Files:**
- Modify: `papers/temporal-perception-in-AI/aaai26/main.tex` — **rewrite the body** per the 5-section spec.
- Modify: `papers/temporal-perception-in-AI/aaai26/appendix/harness.tex` — anonymize/generalize.

**Interfaces:**
- Consumes: Task 1's copy + the E1 numbers from `../positronic-prism/experiments/decay_ablation/report.md`.
- Produces: `aaai26/main.tex` structured as S1–S5 with the 4-invariant table (`\label{tab:invariants}`), E1 table (`\label{tab:e1}`), LongMemEval table (`\ref{tab:lme50}`), E7 (`\ref{tab:e7}`).

- [ ] **Step 1: Replace the body sections with the 5-section structure**

Rewrite the file so the structure is exactly:

```
\author{}                          % EMPTY — double-blind (was \author{Shing Wong})
\affiliations{}
...abstract: keep, but tighten to the empirical claim...

\section{Introduction and Motivation}      % ~1 page: 2-sentence LSU intuition + cargo-cult critique
\section{The Polytemporal Architecture}    % ~1.5 pages: Table 1 (schema primitives), dτ/dt via compression-progress
\section{Disanalogies and Predictions}     % ~1 page: Table (4 architectural invariants), NOT 18 hypotheses
\section{Empirical Feasibility}            % ~2.5-3 pages: E7, LongMemEval, RULER, E1; PRISM in one sentence
\section{Related Work and Discussion}      % ~1 page: tight, limitations
\section*{Checklist}                       % keep the AAAI self-check
```

- [ ] **Step 2: Remove the D1–D10 prose paragraphs; replace with the 4-invariant table**

The 4 invariants (each one dense table row) replace the 10 disanalogy paragraphs:

```latex
\begin{table}[t]\centering
\caption{Four architectural invariants (the falsifiable core of D1--D10).}
\label{tab:invariants}
\begin{tabular}{@{}ll@{}}
\toprule
Invariant & Claim \\
\midrule
1. Salience gating over temporal age & durability tier set at encoding by
surprise $\times$ goal-weight; not by elapsed time (D2) \\
2. Multi-coordinate polytemporal vectors & events indexed by
\{wall, mono, $\tau$, fuzz, regime\}; each mechanism uses its own projection (D6) \\
3. Schema fusion over hoarding & repeated episodes compress to a schema-trace;
prediction-errors retain episode status (D4) \\
4. Continuous substrate coupling & a discontinuous inference core is coupled to
a continuous sensor stream; change is marked witnessed-vs-reconstructed (D7) \\
\bottomrule
\end{tabular}
\end{table}
```

- [ ] **Step 3: Insert the E1 2×2 matrix table into Empirical Feasibility** (same table as Task 4 Step 1, `\label{tab:e1}`).

- [ ] **Step 4: Anonymize the appendix harness**

Rewrite `appendix/harness.tex` hardware paragraph to generalize:

```latex
\paragraph{Hardware and runtime (reproducibility).}
Evaluated on dual Intel Xeon CPUs with AMD Vega accelerators using llama.cpp
and BGE-M3 embeddings, serving local embedding and a quantized local LLM.
Answering used an open-weight commodity model via a third-party router; the
hybrid judge used a 70B open-weight model. ENGRAM\_TAG=\texttt{v0.2.0} pinned.
```

- [ ] **Step 5: Grep-gate the AAAI26 fork for leaks**

Run:
```bash
cd aaai26
! grep -n "Shing Wong\|:8090\|:8080\|renderD\|gfx906\|usr/local/devel" main.tex appendix/*.tex
```
Expected: no matches (exit 1 from `!` is correct — it means zero hits).

- [ ] **Step 6: Compile**

Run: `cd aaai26 && latexmk -pdf -bibtex main.tex 2>&1 | grep -E "Output written|Error|pages"`
Expected: `Output written on main.pdf`, **7 pages or fewer**, no `Error`.

- [ ] **Step 7: Commit**

```bash
git add main.tex appendix/harness.tex
git commit -m "feat(aaai26): strip to empirical core — S1-S5, 4 invariants, E1 matrix, double-blind clean"
```

---

### Task 7: Both papers — final verification gate

**Files:**
- Modify: none (read-only verification).

**Interfaces:**
- Consumes: Task 4 (arxiv) + Task 6 (aaai26) finished states.

- [ ] **Step 1: Verify no stale numbers in either paper's source**

Run:
```bash
cd /usr/local/devel/positronic/positronic-research/papers/temporal-perception-in-AI
for D in arxiv aaai26; do
  echo "== $D =="
  grep -n "0.58\|0.44\|55/55/35/7\|short_term 7" "$D/main.tex" && echo "STALE FOUND" || echo "clean"
done
```
Expected: both print `clean`.

- [ ] **Step 2: Verify the required new numbers are present in both**

Run:
```bash
for D in arxiv aaai26; do
  echo "== $D =="
  grep -c "0.90" "$D/main.tex"
  grep -c "0.78" "$D/main.tex"
  grep -c "35/55" "$D/main.tex"
  grep -c "0/55" "$D/main.tex"
  grep -c "55/55/35/11" "$D/main.tex"
done
```
Expected: all `grep -c` ≥ 1 in both.

- [ ] **Step 3: Verify page counts from the compiled PDFs**

Run: `for D in arxiv aaai26; do echo "$D: $(pdfinfo $D/main.pdf | grep Pages)"; done`
Expected: `arxiv: Pages: 10-14` (roughly), `aaai26: Pages: <= 7`.

- [ ] **Step 4: Commit any residual fixes**

```bash
git add -A arxiv aaai26
git commit -m "fix(papers): final verification gate — stale numbers gone, required metrics present"
```

---

### Task 8: Remove old path + refresh site paper + arxiv.zip

**Files:**
- Delete: `papers/temporal-perception-in-AI/arxiv/aaai26/` (the old combined dir).
- Modify: `papers/temporal-perception-in-AI/arxiv/arxiv.zip` (regenerate from `arxiv/main.tex`).
- Modify: `docs/site/paper.pdf` (copy of `arxiv/main.pdf`).

**Interfaces:**
- Consumes: Task 7 verified arXiv paper.

- [ ] **Step 1: Remove the old combined directory**

Run: `git rm -r papers/temporal-perception-in-AI/arxiv/aaai26`

- [ ] **Step 2: Regenerate the arXiv submission bundle**

Run:
```bash
cd /usr/local/devel/positronic/positronic-research/papers/temporal-perception-in-AI/arxiv
python3 - <<'EOF'
import zipfile, os
entries=['main.tex','refs.bib','aaai2026.sty','aaai2026.bst']
for base in ('figs','appendix'):
    entries += [os.path.join(base,f) for f in os.listdir(base)]
with zipfile.ZipFile('arxiv.zip','w',zipfile.ZIP_DEFLATED) as z:
    for e in entries: z.write(e,e)
print('entries:', len(entries))
EOF
```

- [ ] **Step 3: Refresh the site paper copy**

Run: `cp papers/temporal-perception-in-AI/arxiv/main.pdf docs/site/paper.pdf`

- [ ] **Step 4: Verify the bundle is clean**

Run:
```bash
python3 -c "
import zipfile
z=zipfile.ZipFile('arxiv.zip')
bad=[n for n in z.namelist() if n.endswith('.tex') and ('0.58' in z.read(n).decode() or '0.44' in z.read(n).decode())]
print('stale refs in bundle:', bad if bad else 'NONE')
"
```
Expected: `NONE`.

- [ ] **Step 5: Commit**

```bash
cd /usr/local/devel/positronic/positronic-research
git add -A papers/temporal-perception-in-AI docs/site/paper.pdf
git commit -m "chore(papers): remove old arxiv/aaai26 combined dir; refresh arxiv.zip + site paper
"
```

---

### Task 9: Push + record to brain

**Files:**
- Modify: none.

**Interfaces:**
- Consumes: all completed tasks.

- [ ] **Step 1: Push the research repo**

Run: `git push origin master`

- [ ] **Step 2: Record the milestone to the brain**

Run:
```bash
cd /usr/local/devel/positronic
PYTHONPATH=positronic-engram/engine/src python3 -m positronic_ai consolidate \
  "Paper split complete: arxiv/ (long form, non-blind, author Shing Wong) + aaai26/ (7-page empirical core, double-blind). Both contain LongMemEval 0.90/0.12, E7 55/55/35/11, RULER 1/10-1/74, E1 decay ablation 2x2 (tau 35/55 vs wall 0/55). arXiv adds C->D->H->test table + n=500 roadmap. AAAI26: S1-S5, 4 invariants, no author, no :8090. Old arxiv/aaai26 removed." --json
```