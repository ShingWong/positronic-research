# Hypotheses H1–H13

Each hypothesis: statement → prediction → experiment hook. All experiments
target our continuously-observing game-agent fleet (17 sessions, months of
episodes).

## Encoding & durability

**H1 — Texture-primary indexing.** Durable retrieval keys are {regime-texture,
place-context, entities, valence-magnitude}; wall-clock decays like any weak
attribute and is reconstructable, never primary.
*P:* retrieval by texture beats retrieval by date-range on human-style probes.
*Exp:* E2.

**H2 — Salience-at-encoding.** Durability tier is decided at write-time by
surprise × goal-weight; flashbulb-class memories are exempt from decay.
*P:* one high-salience episode survives consolidation rounds that erase a
thousand low-salience ones, regardless of access frequency.
*Exp:* E3.

**H4 — Schema fusion.** Repeated near-identical episodes compress into a
schema-trace; only prediction-errors retain full episode status.
*P:* storage grows ~log with experience; recall quality for "what usually
happens" improves while per-instance recall of routine events correctly fails.
*Exp:* E3.

## Temporal indexing

**H3 — Landmark-relative dating (anchored constellations).** High-salience
anchor episodes are organizational hubs; peripheral episodes store relational
edges {anchor, before/during/after, offset, phase}; the calendar is
reconstructed by graph traversal.
*P:* anchored stores answer "when, roughly?" comparably to timestamped stores,
while answering cluster-recall probes ("what happened around X?") far better.
*Exp:* E2/E4.

**H9 — Fuzzy-interval coordinates.** Positions stored as labeled intervals
whose width = encoding confidence; recall returns answers at stored resolution,
never manufactured precision.
*P:* calibrated-confidence scoring: reported interval widths predict actual
temporal error.

## Recall

**H5 — Reconstruction-not-retrieval.** Recall is generative inference from
cues + schemas, graded by confidence — not record lookup.
*P:* reconstruction errors cluster systematically (schema-consistent
intrusions), matching Bartlett's findings; confidence tracks accuracy.

**H6 — Reconsolidation.** Every recall re-writes the trace toward the current
schema; memory is an edit-history.
*P:* repeatedly-recalled episodes drift schema-ward vs never-recalled controls;
audit log detects it.

**H8 — Dual recall channels.** Involuntary pattern-completion on partial cues
is a distinct path from strategic top-down search; both must exist.
*P:* cue-similarity-triggered recall fires without task relevance and precedes
strategic query construction in latency.

## Structure of autobiographical time

**H7 — Period containers.** Experience partitions into named nested periods
("last clash season") that bound decay and scope queries.
*P:* period-scoped recall beats global recall on within-period probes.

**H10 — Spreading activation.** Retrieval from any constellation member
activates neighbors; "tell me about that time" works by cluster-walk.
*P:* free-recall output sequences follow constellation adjacency, not
similarity rank.

## Subjective time & continuity

**D6/H-τ — Subjective time density.** dτ/dt = f(novelty-rate,
prediction-error, engagement). Decay, reinforcement, and consolidation cadence
operate on τ.
*P:* τ-keyed memory beats wall-clock-keyed memory on decision-quality probes
across quiet-vs-eventful stretches of equal wall duration. *Exp:* **E1 (the
headline experiment).**

**H11 — Continuity-dependent linearity.** Felt linearity requires
uninterrupted sensorimotor flow; discontinuous minds must couple to continuous
substrates or model their gaps explicitly.
*P:* agents fed a body-stream (bot fleet) show monotone world-model updates;
gap-only agents show step-changes and stale-belief failures.

**H12 — Change provenance.** Witnessed-change and inferred-change are
epistemically distinct memory classes.
*P:* downstream decisions weight provenance-marked beliefs differently;
stale-belief errors concentrate in reconstructed class.

**H13 — Wake-up ritual.** Re-orientation after absence (read digest, diff
expectation vs observation, restale staleness) is a distinct operation that
improves post-gap decision quality.
*P:* ritual-on vs ritual-off A/B across forced gaps.

## Write path

**H14 — Gate-at-encoding (encode-on-surprise).** Sensing is continuous;
encoding is exceptional. Events whose prediction-error falls below threshold
never become episodes — they only reinforce schema-traces (rhythm models,
latency priors). τ advances on surprise; uneventful stretches contribute
≈ zero subjective time. (Completes H4: fusion handles routine events at
consolidation; H14 ensures they mostly never arrive individually.)
*P:* episode-store growth is sublinear in sensed events; per-instance recall
of routine spans correctly fails while schema-level probes succeed;
τ-density plots show flat regions matching independently-reported
uneventful spans. *Exp:* E3 extension + gate-threshold sweep.

**H15 — Resolution ladder & reabsorption.** Memory decays by losing
resolution, not existence: event → day-token → week-token → schema-reference,
with atypical events surviving longest at each rung before re-fusing into the
schema they deviated from (flashbulbs excepted). Gate-fired episodes snapshot
ambient context at trigger time (co-participants, ongoing activity), since
context unrecoverable later binds only through the anchor ("John Doe and Paul
Lee were there").
*P:* aged recalls show systematic resolution loss (details → gist tokens)
rather than random forgetting; day/week-token probes succeed long after
episode-detail probes fail; co-participant recall succeeds via anchor cues
but fails via direct person-query. *Exp:* E3 extension — retention curves
per resolution level + context-binding asymmetry test.

**H16 — Escalation bursts & deferred significance.** High arousal (startle,
threat, sustained aftermath-engagement) triggers an *escalation burst*: the
capture gate holds open, recording wide-scene detail for a days-scale window
at temporarily boosted strength. Burst magnitude ∝ arousal at encoding —
NOT long-term value. Durable tier assignment (flashbulb) is deferred and
evidence-based: downstream references, schema impact, narrative reuse.
Arousal without follow-on significance yields slow fade of great detail
(John's glass); significance without arousal still promotes eventually
(Tom's glance).
*P:* three dissociable detail-retention curves (routine-absent /
escalated-spike-then-slow-fade / flashbulb-flat); tier promotion correlates
with downstream reference counts, not encoding-time arousal; burst windows
show elevated context-capture breadth vs trigger-moment-only controls.
*Exp:* E3 extension — arousal-classed retention curves; promotion-prediction
from reference features; burst-width sweep.

**H17 — Forward-running schemas & causal distillation.** Schema-traces are
generative: they predict outcomes (and sub-features — the sound of shattering)
in real time; matched predictions reinforce causal rules WITHOUT episodic
encoding (learning below the H14 gate); mismatched features fire the gate at
feature granularity. Across repeats, the consolidator diffs antecedents of
similar episodes and distills causal rules (antecedent-pattern → outcome,
confidence ∝ confirmations) that outlive their evidencing episodes and drive
behavioral change (episodic → semantic → procedural, one lifecycle).
*P:* second-instance responses show prediction-then-confirmation signatures;
rule confidence rises monotonically with confirmations while evidencing
episodes fade down the H15 ladder; rule-violating outcomes produce outsized
gate firing + rule revision. *Exp:* E-series extension — synthetic streams
with planted conditional regularities; measure rule induction latency,
confirmation-strengthening below-gate, violation-driven revision.

**H18 — Relationship-conditioned signal gain.** Salience gates are
person-modulated: each person carries a learned gain multiplying weak-signal
admission, built from co-anchor density, interaction persistence,
miss-cost history (ignored signals followed by costly outcomes), and
state-informativeness. Attachment figures earn near-maximal gain — their
lowest-level signals route through personal rules ("her stare → check
something") learned from prior misses, and trigger self-state probes
(interoception: checking one's own hand for the ring). Operational attachment
= the statistics that make someone's weakest signals maximally informative;
no felt-love primitive required.
*P:* identical weak signals produce gated encoding for high-gain persons only;
person-gain predicts miss-costs retrospectively; rule-mediated boosts precede
self-state queries. *Exp:* corpus pilot — person-gain learned from mail
history vs held-out miss-events; gaze-type probe asymmetry.
