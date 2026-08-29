# Pilot: business-domain chronological cognition run

> Status: LIVE — incremental walk started 2026-08-25 at stream position 0
> (August 2007). This document accumulates findings as the cursor advances.
>
> **Anonymization policy:** persons appear as P-codes (`p_0001`…), domains as
> letters, subjects paraphrased. Raw identifiers live ONLY in untracked
> runtime state on the source server. All examples herein are paraphrased or
> structural.

## Corpus

| property | value |
|---|---|
| source | self-hosted Dovecot (mdbox) via `mailgrep` DoveadmSource |
| account | domain-J principal account + 15 domain siblings |
| unique dated messages | **38,245** across 16 folders |
| span | **2007-08 → 2026-08** (19 years) |
| per-year shape | 5 (2007) → ~2.6k/yr steady state, peak 4.9k (2023) |
| sync cost | 16.9 s full-header sweep (mailgrep lib, all folders merged by Date) |

Folder-as-feature note: Junk/Spam/Spam-trained arrive through the same
stream — arrival folder is a user-labeled value signal the gate may learn
from, not an excluded class.

## Toolchain (the three organs)

1. **pull.py** — chronological event server (cursor-based, deduped,
   pseudonymous person ids auto-assigned on first address sighting).
   Built on the `mailgrep` library after its live-hardening pass.
2. **brain.py** — GPU llama-server assessor: strict-JSON novelty/arousal/
   category/suggest per message (thinking off, temp 0.1, ≤160 tokens).
3. **ingest.py** — feeds MemoryEngine.new_event, prints per-message
   introspection (predictions, gate feature vector, trigger trace) and batch
   telemetry; tracks brain↔gate agreement.

## Finding P1 — Cold-start law (H14×H17 interaction, first evidence)

With an empty rule store, EVERY message gates as novel (novelty=0.9 ⇒
score≈0.58 > 0.55 threshold). The brain independently rated message 4
(routine progress note to a known contact) as reinforce-worthy —
disagreement logged, gate overrode.

This is not a bug: it is infant-memory dynamics. "Routine" is undefined until
patterns exist to be violated. Theory predicts an **encode-rate decay curve**
as rules crystallize: 100% at birth → equilibrium ≈5–10% once cadence/thread
schemas form (the synthetic-mix equilibrium already measured).

**Measurable signature added to E3:** encode-rate vs stream position, fit
against rule-formation events. A flat curve would falsify H17's below-gate
learning claim.

## Finding P2 — Brain↔gate agreement as calibration channel

Agreement tracking (brain suggestion vs gate verdict) ran cleanly: 3/4 on
untuned weights. Disagreements are diagnostic artifacts, each one a tuning
signal distinguishing *brain misjudgment* from *gate miscalibration*.
This becomes a standing metric reported per batch.

## Finding P3 — Telemetry warm-up visibility

First-batch stage costs exposed cold-cache effects precisely as designed:
persons-stage 24 ms (registration burst), commit 3.6 ms (cold fd) — both
amortizing toward steady-state <1 ms. Steady-state throughput measured
separately at **~6k events/s** synthetic / 0.17 ms per event.

## Engineering findings (reproducibility appendix)

1. OpenSSH re-splits argv on the remote shell: multi-word doveadm args
   (fetch-field lists, folders like "Deleted Messages") must travel
   pre-quoted, or fields shatter into search keys (reported uppercased).
2. Dovecot `imap.bodystructure` emits ROOT MULTIPARTS WITHOUT enclosing
   parens — parsers demanding one top-level expression must synthesize the
   wrapper ((part1)(part2) "alternative" …).
3. `binary.<section>` envelope: field-header line plus ONE blank separator
   precede content; strip exactly, verify magic bytes (%PDF, FFD8/FFD9).
4. Migrated stores reset save-times: chronology ONLY from Date headers;
   undated messages are unplaceable and excluded (18 calendar auto-replies).
5. bodystructure sizes are ENCODED (base64) lengths; decoded ≈ ×0.75.

## Standing next steps

- Walk 2007→2010 watching P1's encode-rate curve fall as first schemas form
- Person-gain trajectory logging (H18): principal-contact gain curves
- First natural anchor candidates: ownership-transfer correspondence burst
  (live event), earliest international-order episode (expansion anchor)

## Walk 1 — positions 4→404 (2007-10 → 2011-10, 400 messages)

### Finding W1 — Cold-start persistence requires an INDUCER (H14×H17 refined)

Encode rate held at **100% across all 400 messages**. Root cause found by
observation: rules never formed (0→0) because H17's *induction* side did not
exist architecturally — `grade_rule` could strengthen seeded rules, but
nothing proposed new ones from repetition. Worse, the first inducer
implementation sat inside the reinforce-only branch, starving precisely
because everything gated: a chicken-and-egg deadlock (no rules ⇒ all novel ⇒
all encoded ⇒ reinforce path never runs ⇒ still no rules).

**Refinement to H17:** below-gate rule learning has TWO halves —
strengthening (grading existing rules on confirmation) AND induction
(proposing rules from counted repetition). The inducer must run on EVERY
event regardless of gate outcome; routine confirmations are exactly its food.

**Methodological validation:** bulk ingestion would have silently produced a
flat, everything-is-an-episode store. The slow walk with per-message trace
review surfaced the deadlock within one batch. The operator's directive —
process slowly, inspect store and triggers after each message — is what
caught it. Added as standing method note.

Also fixed en route: stream-tau cache served stale snapshots (τ frozen at
0.9 across 400 surprise-weighted events) — found only because τ was being
observed per batch.

Post-fix state: inducer runs on every event; co-occurrence counting
(subject_norm ↔ sender) feeds auto-rule proposals at threshold ≥3 repeats;
walk continues into denser years where the falling encode-rate curve
(Finding P1) becomes testable.

## Attachment census — full-archive sweep

| metric | value |
|---|---|
| messages with IMAGE parts | **16,450 (43% of corpus)** |
| messages with PDF parts | 11,217 |
| image subtypes | PNG 15k · JPEG 11k · TIFF 5.2k · GIF 296 · HEIC/BMP/WebP/PSD/EPS ~36 |
| era spread | continuous 2008→2026 |
| folders | Sent 14.4k · INBOX 4.4k |

Implication: vision analysis is not an edge case — nearly half the archive's
messages carry images, making the perception-tier dedup gate (below)
load-bearing rather than optional.

## Vision recognition gate (H14 applied at perception layer)

Two-tier hashing so the retina tier recognizes instead of re-analyzes:
sha256 (exact duplicates) + 64-bit dHash (resized/re-encoded variants,
Hamming ≤ 6). Registry accumulates corpus-wide.

Classification refinement from operator insight: **a single signature class**
covers personal signatures AND corporate logos — repetition defines the
class, not size or origin. Lifecycle:

| sighting | class | action |
|---|---|---|
| 1st, small | signature (provisional) | skip VLM |
| 1st, large | content candidate | ONE VLM triage |
| 2nd+ (exact or variant) | signature (promoted) | skip forever |

25 unit tests green including byte-integrity checks on extracted binaries
(%PDF…%%EOF framing, JPEG FFD8/FFD9 markers).

## Object layer live — first entity stored

Standardized VLM→database contract (kind/dimension/level/confidence
vocabularies, brace-matching JSON extraction, validation+normalization).
First analysis run on a real 2007-era attachment (vendor logo banner):

```
object e37f2e7e · kind=logo · born τ=720.9 · status=forming
  physical    width_px=400, height_px=80, colors=[black,orange,blue,white]
  qualitative clutter=clean, formality=formal
  abstract    purpose=brand identification, audience=industrial clients
```

Multi-axial classification validated live: VLM assigned
materiality=abstract (the design is a symbol), origin=artifact (human-made),
animacy=null — nuance impossible under a single-tree taxonomy.

Object graph extended with recursive children (ECE Monogram, Company Name
Text — contained-by logo) and DEDUCED relations beyond the visible frame
(logo -[brand-of]-> company node created on demand). Typed edges carry
provenance (vlm-visual vs deduced) and confidence.

## Standing next steps

- Continue walk through dense years (2013+, ~4.9k msgs/yr); test P1 decay
  curve now that the inducer exists
- Person-gain trajectories (H18) as senders repeat across batches
- Wire attachment features (attach_count, has_image, novel_image) into gate
- Vision triage tier: gated novel images → local VLM → perceptual episodes

## Walk 2 — clean restart, positions 1→300 (2007-08 → 2009-07): THE CYCLE FIRES

After wiping the brain and re-running with the completed inducer, all three
predicted milestones fired IN SEQUENCE on real correspondence:

```
*** FIRST REPEAT SIGHTING  — object ×2: 'more stuff'
*** FIRST RULE PROPOSED    — subject_norm='liqui-fire rx' → sender=p_0001
                             (support=3, i.e., distilled on the THIRD sighting —
                              exactly the two-glasses mechanism of C7's family)
*** FIRST below-gate reinforcement (H14) — 'Re: Liqui-Fire RX'
```

The very next matching message was processed as *recognition, not perception*:
no episode written, rule support incremented, schema reinforced.

### Finding W2 — The encode-rate curve bends locally around induced rules

Bucketed encode rates dipped below 100% for the first time (92–96% in four of
twelve buckets; 16 reinforcements total). The dip is LOCALIZED around the one
induced rule's subject — confirming the causal chain
**repetition → induction → prediction → below-gate reinforcement** rather
than a global decay. In the sparse 2008–09 era only one pattern reached
support ≥3; the dense years (2013+, ~4.9k msgs/yr with recurring clients)
are where the curve should sag visibly. Standing measurement.

### Engineering appendix — what observation caught that bulk would have hidden

Three defects, each invisible to bulk import, each surfaced by per-batch
introspection:

1. **Frozen subjective time**: stream cache served stale τ snapshots — τ sat
   frozen at 0.9 across hundreds of surprise-weighted events. Found because
   τ is printed per batch.
2. **Inducer branch-starvation**: the induction code initially lived inside
   the reinforce-only branch — unreachable while everything gates
   (chicken-and-egg). Found because rules stayed 0 despite ×7 threads.
3. **NULL person-id leak**: the bulk-walk path bypassed person resolution,
   flowing None into auto-registration (SQLite permits NULL primary keys).
   Found by feature-dump diff against the interactive path.

Plus an operations lesson: `walk | head` kills the walker mid-stream via
SIGPIPE and strands the cursor — batch output goes to log files now.

Method standing note reinforced: slow chronological processing with per-step
trace review is not patience theater — it is the debugger this architecture
actually has.

## E7 EXECUTED — retention profiles on identical experience (78 weeks)

Four brains fed the SAME chronological stream (55 messages, 2007-08 →
2009-01), weekly consolidation passes, differing ONLY in retention profile:

| profile | episodes alive @ wk78 | expired | day_merged |
|---|---:|---:|---:|
| archival | 55 | 0 | 0 |
| long_term | 55 | 0 | 0 |
| balanced | 35 | 0 | 20 |
| short_term | 7 | 35 | 13 |

CONTROL PASSED: object formation IDENTICAL across brains (37 objects,
same names/statuses) — profiles affect only forgetting, not perception.
First divergence: week 36 (npc brain froze at 7 during the Liqui-Fire burst).
Second divergence: weeks 53–54 (balanced begins reabsorbing during the
Genesis-stuff burst). Long_term indistinguishable from archival at this Δτ —
expected until Δτ/S approaches 1.

This validates H15's ladder dynamics empirically AND demonstrates the
application-knob thesis: identical experience yields four different memory
states by policy choice alone. Full data: brain_henry/state/e7_results.json;
harness: brain_henry/experiment_profiles.py.
