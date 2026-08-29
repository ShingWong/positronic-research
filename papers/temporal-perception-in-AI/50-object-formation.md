# Object Formation — from event streams to a world of things

> Research track proposal (2026-08-25). The event database records *what
> happened*. This track builds the companion database of *what exists* —
> objects condensed out of repeated multisensory experience, the way infants
> extract cups, faces, and gravity from raw happening.

## Thesis

Human autobiographical memory is doubly organized: **anchors** partition time
(see `45-pilot` anchor findings); **objects** populate space and agency. An
object is not stored IN any single event — it condenses across many, as
cross-modal features (sight, sound, texture, effect) repeatedly co-occur until
the bundle stabilizes. The unit of storage is a multimodal tensor: modality ×
feature × evidence-over-time, including AFFORDANCES — the effects the object
invites or resists (Gibson).

## Why our engine is already half-way there

The `person` table is a working object store for one class of thing: runtime
registration on first encounter, enrichment per event, learned relationship
weights, bidirectional episode bindings. Object formation generalizes that
pattern from people to everything the stream proves persistent.

Existing machinery that plugs in unchanged:
- `image_registry` — perceptual clusters are proto-objects (phash identity +
  seen-count). Promotion path: cluster crossing sighting threshold ⇒ object.
- `causal_rule` — H17 rules are proto-AFFORDANCES when their antecedents name
  an object ("near-edge + hand ⇒ shattered"). Scope them: object_affordance.
- `anchor_edge` — anchors organize WHEN; objects organize WHAT. Constellation
  walks will traverse both.

## Hypotheses

**H19 — Object condensation.** Objects form from recurrent cross-modal
co-occurrence; recognition strength ∝ sightings × modality breadth; partial
cues (one slice of the tensor) complete to the whole object.
*P:* planted recurring attachments/entities reach recognition threshold;
partial-cue probes (image alone, name alone) retrieve the full object.

**H20 — Affordance encoding.** Objects absorb causal rules scoped to them;
action-decisions consult object-scoped affordances before global rules.
*P:* affordance-scoped retrieval beats global-rule retrieval on action
probes; affordance updates change subsequent decisions (John places glasses
carefully after the break).

## Schema v2 additions (drafted in engine discussion, pending implementation)

```
object(id, kind, canonical_name, visual_phash, text_embed,
       first_seen_tau, last_seen_tau, salience, status)
object_sighting(episode_id, object_id, channel, confidence)
object_affordance(object_id, rule_id, evidence_count)
```

Promotion pipeline: image_registry cluster → candidate object → consolidator
verifies recurrence across ≥N episodes and ≥1 other channel → status=forming
→ stable. Dormancy replaces deletion (Piaget: permanent existence).

## Relationship to the literature we will borrow

- Treisman & Kahneman — object files / momentary bindings
- Spelke — core object principles (cohesion, continuity, contact) as
  formation filters
- Piaget — object permanence ⇒ dormancy model
- Gibson — affordances ⇒ object_affordance table
- Biederman — geon-style shape primitives for the visual slice (later)

## Pilot application (henry@ corpus)

16,450 image-bearing messages + 11,217 PDF-bearing ones are the raw feed.
First target: collapse the Trifold PDF + JPEG preview + "international order"
thread into ONE object with sightings, participants, and outcome — then ask
it the canonical anchored question without mentioning a date.

## Related work — verified sweep (2026-08-25)

**Object-centric learning (ML):**
- Locatello et al., *Slot Attention*, NeurIPS 2020 (arXiv:2006.15055). Slots
  explicitly framed as computational OBJECT FILES (citing Kahneman/Treisman).
  Competitive binding over attention rounds = feature binding solved for
  frames. BORROW: binding-as-competition. ADD BEYOND: slots are momentary;
  nothing persists a slot as a growing entity across months of events.
- GOLD (arXiv:2410.18809) — global object identity across scenes via
  disentangled scene-dependent vs scene-invariant attributes. Same problem we
  face: recognizing the Trifold across 19 years of renderings.
- uOCF (arXiv:2402.07376) — unsupervised 3D object discovery in real scenes.

**Infant object-concept formation (computational):**
- Luger, Bower & Wishart (1983) — object concept as rewrite-rule grammars
  parsing perceptual phenomena. Our H14 gate is a descendant of this idea.
- Mareschal & Johnson-line unified models of unity/permanence/trajectories.
- Bramley lab (2023) — **object perception as PROGRAM INDUCTION**: concepts
  capture rigidity and persistence. Directly validates H17-style rule
  distillation as the object-learning mechanism.

**Affordances & visual knowledge:**
- AffordanceLLM (arXiv:2401.06341, IEEE 2024) — VLM world-knowledge grounds
  affordances from single images. Borrowable for our vision-triage tier.
- VKnowU benchmark (arXiv:2511.20272) — tests exactly our glass example:
  inferring fragility of transparent crystals from appearance.

**Nearest neighbors in agent memory (2025–26 wave):**
- *TeleMem* — evolving OBJECT-CENTRIC GRAPHS tracking changing states of
  environments. Closest existing system to our object layer. `[verify cite]`
- *SSGM* (arXiv:2603.11768) — memory governance: semantic-drift bounding via
  immutable anchor ledger + periodic reconciliation. Addresses our H6
  reconsolidation risk (drift without audit).
- Du, *Memory for Autonomous LLM Agents* survey (arXiv:2603.07670, Mar 2026)
  — lists as OPEN FRONTIERS: continual consolidation, causally grounded
  retrieval, learned forgetting, multimodal embodied memory. Our exact
  agenda, independently confirmed open.
- Tresp et al., *The Tensor Brain*, Neural Computation 35(2) 2023 — unified
  theory of perception/memory/semantic decoding built on tensor
  representations. The user's "tensor-like structure" intuition has a named
  theory to engage.

## Confirmed open lane

No existing system combines: persistent cross-year object condensation +
affordance induction scoped to objects + experience-time (τ) decay + anchor-
event organization. The pieces exist separately (slots, induction, graphs,
governance); the synthesis for long-lived agent memory does not.

## Characteristic description layer (grounding hierarchy) — new open problem

Objects need DESCRIPTIONS at three grounding levels:

| level | examples | acquisition |
|---|---|---|
| physical | dimensions, size, material, page-count | sensed/measured/VLM-estimated |
| qualitative | glossy, stiff, bright, loud | ordinal quality ladders, context-relative |
| abstract | purpose, value, currency, ownership | language+culture+consequence; mutates independently |

Key structural claims:
1. Qualitative properties are ORDINAL SPACES with object-relative calibration
   — comparisons ("glossier than") are primary, absolute tags secondary.
   Legacy qualitative-reasoning (QR) formalisms apply, never built into
   agent memory stores.
2. Abstract characteristics are relationship-to-context values with their own
   temporal dynamics ("current marketing" → "outdated" → "artifact") while
   bytes stay frozen — hence valid_tau + re-evaluation at consolidation.
3. Every characteristic carries provenance (sensed / vlm-estimated /
   llm-inferred / told) and confidence.

Schema: `object_characteristic(object_id, level, dimension,
val_scalar|val_range|val_ordinal|val_symbol|val_embed, comparator,
confidence, provenance, valid_tau)` — see engine discussion.

Related verified work: VKnowU (arXiv:2511.20272) benchmarks physical-
property inference (crystal→fragile); AffordanceLLM grounds interaction;
QR literature supplies comparison algebras. Open: no persistent,
provenance-tracked, comparison-capable characteristic store attached to
long-lived agent objects. Second PhD-scale lane confirmed.

## Adopted classification scheme (post-research, 2026-08-25)

Multi-axial (Wikidata-style) instead of a single tree — orthogonal axes as
nullable columns on `object`:

| axis | values | lineage |
|---|---|---|
| materiality | physical / abstract | SUMO primary split |
| animacy | living / non-living / null | cognitive animate-inanimate divide |
| origin | natural / artifact / null | developmental induction differences |
| basic_level_name | free text ("brochure","company") | Rosch basic level |

Rationale: enumerated subclass trees bloat and fossilize (Cyc lesson);
basic-level labels are DATA (FTS-searchable), not ontology nodes; axes are
independently queryable and each earns its keep (decay keys on materiality,
affordance priors on animacy+origin). Live VLM result validated the nuance:
logo classified abstract/artifact simultaneously — impossible in a single
tree. Verified sources: Mascardi et al. upper-ontology comparison (2007);
Wikidata polyhierarchy paper (arXiv:2512.12260); Rosch basic-object research
(1976); Bloom artifact-intentionality (1996).

## Implementation status (2026-08-25) — object layer LIVE

- Tables live: `object`, `object_sighting`, `object_relation` (typed, 12
  predicates), `object_characteristic` (3 grounding levels ×
  scalar/range/ordinal/symbol value forms + confidence + provenance +
  valid_tau)
- Standardized VLM contract v1: strict-JSON analysis constrained to store
  vocabulary; recursive `children` (visible sub-objects) and deduced
  `relations` (edges to inferred targets, nodes created on demand);
  multi-axial classification fields (materiality/animacy/origin/basic-level)
- First entity stored from real corpus: vendor logo banner → kind=logo,
  name read from pixels ("Environmental Compliance Equipment"), 7
  characteristics across all three levels, child parts (monogram,
  company-name text), deduced edges (brand-of company, references industry)
- Thread-object formation wired into the chronological walker: 300 messages
  → 213 objects, 15 stable (≥3 sightings), sighting histogram confirms
  sparse-tail structure (175 singletons vs 24 multi-sighted)

Pilot-corpus attachment census motivating the vision tier: 16,450
image-bearing messages (43%), 11,217 PDF-bearing; signature/logo class
collapses via sha256+dHash recognition gate so VLM triage is spent only on
genuinely novel content.
