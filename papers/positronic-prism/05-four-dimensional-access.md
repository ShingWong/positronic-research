# 05 — Four-Dimensional Access: the polytemporal plane over the corpus volume

> **Status:** the core image of the PRISM thesis. Formalizes "4D access to a
> 3D haystack."

## The claim, in one sentence

A conventional memory system **searches a 3D corpus** (text, interleaved, no
time axis). Positronic **traverses time** — the fourth dimension — so the
needle is presented in context without searching the haystack at all.

## The 3D haystack (what everyone else does)

A raw corpus is three dimensions: the document stream, unordered by meaning.
There is no time axis on the *access path* — a model reading 30k characters
must simultaneously:

1. **find** the needle (locate the region holding the answer), and
2. **extract** it (copy the exact value from that region).

This is the LongMemEval "without-memory" condition. It is a *needle-in-haystack*
task. The baseline scores it at 0.10–0.14.

## The 4D plane (what positronic does)

The polytemporal substrate adds **τ — subjective time** — as a fourth
coordinate on every episode. Retrieval does not scan the volume; it **slices
the corpus along τ**, presenting the entity's temporal family:

- the entity's **τ-span** tells you *where in time* the answer lives,
- the **event-defined interval** ("between Jack quit and Jane took over")
  resolves the search to a bounded temporal region,
- the **digest** (the peep) tells you how much depth exists before you look.

From the τ-plane, the haystack is **perpendicular to the access path** — you
never look through it. The needle is presented *in context*; only **extraction**
remains.

## Why the benchmark proves it

| condition | task | measured |
|---|---|---|
| without memory (3D) | find + extract | 0.10–0.14 |
| with positronic (4D) | extract only | **0.891** (flash), floor 0.84 |
| frontier on 4D | extract only | ~1.0 ceiling (opus/gpt-5.6/glm 4/4) |

The delta is not "faster search." It is **no search**. The 4D plane removes the
haystack; the model's remaining job — extraction — is the variable PRISM
measures.

## The opus-5 falsification, restated in 4D

Opus-5 "by itself" reads the 3D haystack. On the one question where the gold
was inside the truncated window ("7" shirts), opus **missed it** — it said
"you haven't mentioned" — because in 3D it had to find *and* extract. Given
the same gold presented in 4D context (positronic), every frontier model in the
panel extracted it trivially. The 4D plane did not make opus smarter; it made
the task *single-step*.

## The image, precisely

- **3D** = search. The needle hides in the volume; cost grows with the volume.
- **4D** = traverse. The τ-plane is perpendicular to the volume; the needle is
  *visible from the plane* without entering the volume.
- **PRISM** = the name made literal: the 4D plane *prisms* the 3D volume into
  its time-sliced components, so each is examined on its own axis.

## Use

This framing is the paper's core image and the pitch's opening line. It is a
*scientific* claim — the measured delta (3D 0.14 → 4D 0.891) is the evidence —
not just an analogy.

## Indexes label the haystack; we X-ray through it

A conventional index (FTS, keyword, inverted) is a **label on the haystack**:
it tells you *which* straw holds the needle, but the haystack is still there —
still in the context window, still obscuring. It compresses the *search time*,
not the *search task*: the model must still find the needle and extract from
within distraction. That is why the lexical ablation fails: a keyword index on
the same corpus retrieves nothing usable on all 50 questions (fallback 1.00,
acc 0.10) — faster navigation, same needle-in-haystack problem.

Polytemporal access is **4D X-ray vision**: it does not locate the needle *in*
the haystack — it collapses the haystack along the τ-axis so the needle is
presented directly, in context, with the haystack perpendicular to the access
path. The search task itself is eliminated; only extraction remains.

- **Index** = metadata *about* the haystack.
- **Engram** = a view of the corpus the haystack cannot occlude.
- **Indexing** is a search technology; **polytemporal access** is an access
  technology.

## Division of labor: the cabinet and the working memory

Exact bytes are the file cabinet's job; meaning is the engram's. The brain
forgets bytes aggressively *because it never claimed them* — git, the database,
and the filesystem preserve byte-perfect truth, and every consolidation
*references* that truth (a pointer to commit `9ecab9a`) rather than duplicating
it. Working memory keeps the distilled engram; the cabinet keeps the copy. Each
layer does what it is best at — fidelity lives in the cabinet, meaning lives in
the mind, and the two never need to be the same store.