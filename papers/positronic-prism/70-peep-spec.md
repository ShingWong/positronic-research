# PEEP — Positronic Engram Exchange Protocol

> **Status:** Level 1 specification. The data contract between a polytemporal
> memory substrate and a reasoning agent — published for adoption.

**PEEP** (Positronic Engram Exchange Protocol) defines the structure of the
polytemporal data a memory engine delivers to an agent. It is the standard
*interface* of the memory system: adopt PEEP, and any agent can consume
polytemporal memory without coupling to the engine that produced it.

## Design principles

1. **Polytemporal by construction** — every record carries its time vector, so
   time is never a decoration; it is the structure.
2. **Agent-decision-friendly** — the contract *presents* the entity's temporal
   family and lets the agent (the frontal lobe) decide depth. It does not
   pre-judge.
3. **Self-describing** — each record is complete enough to interpret without
   the engine: tau, wall, provenance, salience travel with the data.
4. **Retrieval-isolated** — gold-presence is verifiable from the payload alone.

## Level 1 — the recall/dossier contract

### Per-hit record (a single episode in a recall)

```json
{
  "episode_id": "uuid",
  "tau": 1935.4,
  "wall": "2026-09-01T04:11:32+00:00",
  "stream": "chat:1",
  "kind": "message | consolidation",
  "salience": 0.5,
  "snippet": "...retrieved text...",
  "fuzz_lo": null,
  "fuzz_hi": null,
  "provenance": "witnessed | reconstructed",
  "person_boost": 1.0,
  "fallback": false
}
```

### Entity digest (the polytemporal object block)

```json
{
  "canonical_name": "positronic-opencode-plugin",
  "kind": "entity",
  "status": "active | forming | dormant | forgotten",
  "versions": {
    "sighting_count": 106,
    "tau_span": [16.2, 2368.3],
    "latest_consolidation": "...distilled summary...",
    "oldest_tau": 16.2
  }
}
```

### Dossier (ask — the dig-deeper payload)

A τ-ordered list of every sighting of an entity:

```json
[
  {"episode_id": "...", "tau": 16.2, "wall": "...", "kind": "message",
   "subject_norm": "...", "body_text": "...", "channel": "text",
   "confidence": 0.9}
]
```

## Level semantics

| Level | content | access |
|---|---|---|
| **PEEP Level 1** | recall hit + entity digest + dossier structure (this spec) | free, standard |
| **PEEP Level 2+** | full n=500 autopsies, fresh-model fingerprints, private runs | private request |

## Conformance

A system is **PEEP-compliant** if it delivers: (1) a per-hit record with the
time vector fields above, (2) an entity digest with `versions`, and (3) a
τ-ordered dossier on dig-deeper. Compliance is machine-checkable from the
payload alone.

## Adoption

- Consumers: any agent (opencode, Claude Code, or custom) that receives PEEP
  and decides retrieval depth from the digest.
- Producers: any memory engine that emits the contract.
- The free Level 1 spec is the adoption seed; the standard is engine-agnostic
  by design.

See `dataset/level1/` for the associated training-data tier.