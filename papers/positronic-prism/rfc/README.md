# PEEP RFC Series

Versioned, normative specifications for the Positronic Engram Exchange
Protocol. Each RFC is machine-checkable against an executable conformance
suite.

| RFC | title | status | conformance |
|---|---|---|---|
| [PEEP-0001](PEEP-0001.md) | Level 1 Data Contract (per-hit, digest, dossier) | Proposed | `test_peep_conformance.py` (5 tests) in `positronic-peep` |
| [PEEP-0002](PEEP-0002.md) | HTTP Transport (endpoints, auth, federation) | Proposed | `validate-protocol.sh` (12 checks) in `positronic-serve` |

## How to read an RFC

- Key words (MUST / SHOULD / MAY) are per RFC 2119.
- A **producer** (memory engine) conforms to PEEP-0001; a **server** conforms
  to PEEP-0002.
- Compliance is defined by the executable tests, not the prose alone.

## Naming

- Port **2114** — NDR-2114, the Andrew port ("2" for bi).
- PEEP dual meaning: the *protocol* (the standard) and a *peep* (the glimpse
  a digest gives into an engram).