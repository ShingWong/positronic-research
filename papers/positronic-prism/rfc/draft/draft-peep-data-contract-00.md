---
title: "Positronic Engram Exchange Protocol: Level 1 Data Contract"
abbrev: PEEP
docname: draft-peep-data-contract-00
category: info
ipr: trust200902
area: General
submissionType: independent

stand_alone: true
pi:
  sortrefs: yes
  symrefs: yes
  toc: yes

author:
  -
    ins: S. Wong
    name: Shing Wong
    org: Positron
    email: swong@stuartconsultinggroup.com

normative:
  RFC2119:

informative:
  PEEP-0002:
    title: "Positronic Engram Exchange Protocol: HTTP Transport"
    author:
      - ins: S. Wong
        name: Shing Wong
    date: 2026-09-02
    seriesinfo:
      PEEP: 0002

--- abstract

PEEP (Positronic Engram Exchange Protocol) defines the structure of the
polytemporal data a memory engine delivers to a reasoning agent. This
document specifies Level 1: the per-hit record, the entity digest, and the
tau-ordered dossier. A system that produces payloads conforming to the
requirements in Section 3 is PEEP-compliant; compliance is machine-checkable
from the payload alone (see Section 5).

--- middle

# Introduction

A memory system that stores every byte is a database, not a memory. PEEP is
the interface of a polytemporal memory system: the structure it hands to an
agent so the agent can decide retrieval depth without coupling to the engine
that produced the data. Adopt PEEP, and any agent can consume polytemporal
memory from any producer.

The contract is built on four design principles:

1. **Polytemporal by construction** - every record carries its time vector,
   so time is never a decoration; it is the structure.
2. **Agent-decision-friendly** - the contract presents the entity's temporal
   family and lets the agent decide depth. It does not pre-judge.
3. **Self-describing** - each record is complete enough to interpret without
   the engine: tau, wall, provenance, salience travel with the data.
4. **Retrieval-isolated** - gold-presence is verifiable from the payload
   alone.

# Terminology

| term | meaning |
|---|---|
| **producer** | a memory engine that emits PEEP payloads |
| **consumer** | an agent or service that receives PEEP payloads |
| **episode** | one encoded memory event (a message, snapshot, or consolidation) |
| **object** | a family of tau-stamped sightings of one canonical entity |
| **tau** | subjective time: integrated novelty/prediction-error density, agent-native (not wall-clock) |
| **wall** | wall-clock timestamp of the episode |
| **dossier** | the full tau-ordered list of an object's sightings |
| **digest** | the compact "peep" summary of an object's depth |

# Normative Requirements

## Per-hit record (a recall hit)

A recall operation returns zero or more hits. Each hit MUST be a JSON object
containing the following fields:

| field | type | requirement | meaning |
|---|---|---|---|
| `episode_id` | string | MUST | stable unique identifier of the episode |
| `tau` | number | MUST | subjective time coordinate; MUST NOT be null |
| `wall` | string | MUST | ISO-8601 wall-clock timestamp; MUST be a string |
| `stream` | string | SHOULD | the source stream identifier |
| `kind` | string | MUST | one of `message`, `consolidation` (extensible) |
| `salience` | number | MUST | encoding salience in [0,1] |
| `snippet` | string | SHOULD | the retrieved text |
| `fuzz_lo` | string or null | MAY | fuzzy lower interval bound |
| `fuzz_hi` | string or null | MAY | fuzzy upper interval bound |
| `provenance` | string | SHOULD | one of `witnessed`, `reconstructed` |
| `person_boost` | number | MAY | person-weighting applied at retrieval |
| `fallback` | boolean | MUST | true if the hit came from the fallback channel |

Normative example:

~~~ json
{
  "episode_id": "9f1c8b2a-0000-4000-8000-000000000000",
  "tau": 1935.4,
  "wall": "2026-09-01T04:11:32+00:00",
  "stream": "chat:1",
  "kind": "message",
  "salience": 0.5,
  "snippet": "...retrieved text...",
  "fuzz_lo": null,
  "fuzz_hi": null,
  "provenance": "witnessed",
  "person_boost": 1.0,
  "fallback": false
}
~~~

## Entity digest (the "peep")

When a cue fuzzy-matches an object, the recall response MAY include an
`object` block. When present, it MUST be a compact summary - a peep - not a
full dump. It MUST contain a `versions` object with these fields:

| field | type | requirement | meaning |
|---|---|---|---|
| `canonical_name` | string | MUST | normalized entity name |
| `kind` | string | SHOULD | `entity` (extensible) |
| `status` | string | SHOULD | one of `active`, `forming`, `dormant`, `forgotten` |
| `versions.sighting_count` | integer | MUST | number of sightings |
| `versions.tau_span` | array[number] | MUST | [min_tau, max_tau] of the family |
| `versions.latest_consolidation` | string | MUST | distilled summary of the latest consolidation |
| `versions.oldest_tau` | number | MUST | oldest sighting's tau |

Normative example:

~~~ json
{
  "canonical_name": "positronic-opencode-plugin",
  "kind": "entity",
  "status": "active",
  "versions": {
    "sighting_count": 106,
    "tau_span": [16.2, 2368.3],
    "latest_consolidation": "...distilled summary...",
    "oldest_tau": 16.2
  }
}
~~~

The digest MUST be a glimpse, not the data: a consumer reads it to learn that
polytemporal depth exists, then decides whether to dig (dossier). It MUST NOT
treat `latest_consolidation` as the whole truth.

## Dossier (dig-deeper)

A dossier is the full tau-ordered list of every sighting of an object. Each
sighting MUST include an `episode_id`, `tau`, `wall`, and `kind`; MAY include
`subject_norm`, `body_text`, `channel`, and `confidence`. The list MUST be
ordered by tau (ascending or descending; a consumer MUST NOT assume a
direction without inspecting two adjacent tau values).

Normative example:

~~~ json
[
  {"episode_id": "...", "tau": 16.2, "wall": "2026-08-25T09:00:00+00:00",
   "kind": "message", "subject_norm": "...", "body_text": "...",
   "channel": "text", "confidence": 0.9},
  {"episode_id": "...", "tau": 2368.3, "wall": "2026-09-01T04:11:32+00:00",
   "kind": "consolidation", "confidence": 0.9}
]
~~~

## Level semantics

| Level | content | access |
|---|---|---|
| PEEP Level 1 | recall hit + entity digest + dossier structure (this RFC) | free, standard |
| PEEP Level 2+ | full n=500 autopsies, fresh-model fingerprints, private runs | private, per agreement |

# Security Considerations

- Payloads are data, not code. Consumers MUST NOT evaluate any field as an
  expression or query language.
- `snippet`, `body_text`, and `latest_consolidation` may contain arbitrary
  user text. Consumers MUST treat them as untrusted data (rendering,
  logging, or echoing verbatim can leak PII).
- Producers MAY redact or omit `body_text` for privacy tiers; the contract
  is satisfied by the mandatory fields only.

# Conformance

A system is PEEP-compliant if every payload it produces satisfies the
per-hit record, entity digest (when an object block is present), and dossier
(when requested) requirements above. Compliance is machine-checkable from the
payload alone.

The executable conformance suite lives in the `positronic-peep` project
(`test_peep_conformance.py`, 5 tests). A producer is compliant iff every test
passes against its payload. The tests assert, normatively:

1. every recall hit carries `episode_id`, non-null `tau`, string `wall`;
2. every hit carries `salience`, `kind` in {message, consolidation}, boolean
   `fallback`;
3. the digest exposes `versions` with `sighting_count`, 2-element `tau_span`,
   `latest_consolidation`, `oldest_tau`;
4. the dossier is tau-ordered and every sighting has `episode_id` + `kind`;
5. the digest is a peep - compact, not a full dump.

# IANA Considerations

This document has no IANA actions. The companion transport specification
(PEEP-0002) requests the `peep` service name, TCP port 2114, and the `peep`
URI scheme.

# Acknowledgements

The PEEP protocol series is developed in the positron project.