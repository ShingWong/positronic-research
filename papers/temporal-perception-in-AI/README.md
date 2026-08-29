# Temporal Perception in Artificial Intelligence

### *Why Machines Must Re-Derive Time from Experience Rather Than Inherit It from Humans*

**Status:** skeleton / research-in-progress
**Working dir:** `llmem/papers/temporal-perception-in-AI/`
**Related:** `../../research/cognitive/`, `../../research/architecture/three-tier-cognition.md`

---

## Abstract (draft v0)

Large language model agents are deployed into a world saturated with time —
deadlines, seasons, waiting, change — yet they possess no temporal
phenomenology: no felt duration, no experience of the interval between
invocations, no native clock. Current practice either ignores this or copies
human memory mechanisms (Ebbinghaus decay, recency weighting, sleep-inspired
consolidation) whose parameters derive from biological necessities — mortality,
metabolism, circadian rhythm — that agents do not have. We argue such borrowing
produces *cargo-cult memory*: the form of human mechanisms without their
derivational basis.

Through phenomenological case analysis, we identify systematic disanalogies
between human and machine temporality: time-as-texture versus time-as-coordinate,
anchor constellations versus flat chronologies, subjective time density versus
wall-clock, and discontinuous minds coupled to continuous bodies. Each
disanalogy yields a falsifiable hypothesis (H1–H13). From these we propose
*polytemporal representation*: events located in vectors of heterogeneous time
coordinates — wall-clock, monotonic, subjective τ (integrated novelty density),
task-local elapsed, regime phase — with each cognitive mechanism consuming its
own projection rather than a privileged axis. Salience at encoding, not age,
gates durability; anchor episodes replace calendars as the primary temporal
index; a continuous sensor substrate supplies the experiential stream that a
discontinuous inference core lacks.

We close with experimental designs — runnable on a continuously-observing game-
agent fleet — that pit τ-keyed against wall-clock-keyed memory on decision
quality, testing whether re-derived time outperforms borrowed time.

## Contributions

1. A disanalogy framework: N fundamental differences between human and machine
   temporality, each stated as mechanism → biological derivation → agent
   substitute → architectural consequence → testable prediction.
2. Case-corpus method: carefully chosen introspective events used as
   specification test-vectors for candidate representations.
3. Polytemporal representation + agent-native time τ.
4. Thirteen falsifiable hypotheses (see `20-hypotheses.md`).
5. Experimental designs on a continuous-observation bot fleet.

## Files

| file | contents |
|---|---|
| `00-outline.md` | section map |
| `10-case-corpus.md` | phenomenological cases C1–C8 (Tom, glasses, commute…) |
| `20-hypotheses.md` | H1–H18 with predictions and experiment hooks |
| `25-polytemporal-schema.md` | typed store schema v1 (no JSONB on query paths) |
| `26-beyond-sql.md` | fuzzy-memory engine as paper #2; MemoryEngine interface |
| `30-related-work.md` | annotated bibliography — borrow-vs-add per source |
| `40-experiments.md` | E1–E6 designs incl. headline τ-vs-wall-clock test |
| `45-pilot-mail-cognition.md` | **LIVE**: john-henry pilot log — cold-start law, attachment census (43% image-bearing), vision gate, object layer first entity |
