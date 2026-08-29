# Beyond SQL: toward a fuzzy-memory engine (paper #2 seed)

> Position: PostgreSQL implements the MemoryEngine interface for v0 research.
> The long-term contribution is a storage engine whose primitives match
> cognitive retrieval semantics. That engine is its own research program.

## Why SQL is scaffolding

SQL answers: *which rows satisfy predicate P, exactly.*
Fuzzy memory asks: *what would a mind reconstruct from this cue, with what
confidence — and how does asking change what it knows?*

Four operations have no SQL analogue:

1. **Read-mutates** (H6 reconsolidation): SELECT with side effects.
2. **Expiring-by-default storage** (decay as physics): permanence requires
   justification (flashbulb tier), not the reverse.
3. **Confidence-compounding results** (H5×H9): joins carry epistemics;
   provenance chains propagate uncertainty through reconstruction.
4. **Experience-time ordering** (τ): no physical clock is privileged.

## Lineage to borrow (do not reinvent)

| source | contributes |
|---|---|
| Kanerva, *Sparse Distributed Memory* (1988) | pattern completion from noisy partial cues; majority-sum readout; counter-based decay — the founding fuzzy store |
| ACT-R declarative memory (Anderson et al.) | retrieval probability & latency as closed-form activation functions (recency+frequency+context+noise) |
| Ramsauer et al., *Hopfield Networks is All You Need* (2020) | attention IS associative retrieval — the inference core already contains a fuzzy-read mechanism |
| Probabilistic DBs (Trio, MayBMS) | tuple-confidence algebra |
| kNN-LM / RETRO | retrieval interpolated into generation |

Novel synthesis: an engine whose API primitives are
**Activate · Reconstruct · Decay · Fuse** — none of which exist in any
production datastore.

## Structural hedge (do this NOW)

All hypothesis experiments target the `MemoryEngine` interface:

```
Activate(cue, budget)      -> activation distribution over episodes
Reconstruct(query, budget) -> synthesized answer + confidence + provenance chain
Decay(tau_now)             -> background physics pass (the engine's "sleep")
Fuse(cluster_id)           -> schema-trace materialization
```

v0 backend: PostgreSQL (`25-polytemporal-schema.md`).
Future backend: purpose-built engine (Rust candidate).
Theory never rewrites; storage swaps.

## Open design questions for the engine paper

1. Activation space geometry: embedding ⊗ regime ⊗ anchor-graph — one metric
   or per-projection metrics with late fusion?
2. Write-amplification of reconsolidation: every read rewrites — crash-safe
   edit-history semantics (append-only trace? CRDT-flavored?).
3. Decay as garbage collection vs decay as signal: what must survive for
   reconstruction even after traces fade (schema-traces, anchors persist).
4. Confidence algebra: how do interval-width, activation, and provenance
   compose into one calibrated number?
