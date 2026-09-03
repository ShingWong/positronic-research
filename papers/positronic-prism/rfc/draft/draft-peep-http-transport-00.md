---
title: "Positronic Engram Exchange Protocol: HTTP Transport"
abbrev: PEEP-HTTP
docname: draft-peep-http-transport-00
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
  RFC3986:
  RFC5234:
  RFC6335:
  RFC7595:

informative:
  PEEP-0001:
    title: "Positronic Engram Exchange Protocol: Level 1 Data Contract"
    author:
      - ins: S. Wong
        name: Shing Wong
    date: 2026-09-02
    seriesinfo:
      PEEP: 0001

--- abstract

This document specifies the HTTP transport for PEEP-0001 payloads: how a
polytemporal memory service exposes its brains to clients, and how federated
recall fans out across peer hosts. It defines the endpoints, request/response
shapes, authentication model, and federation semantics. A server that conforms
to this specification is PEEP-HTTP-compliant; compliance is verified by the
executable conformance gate.

This document requests the registration of the "peep" service name and TCP
port 2114 in the IANA Service Name and Transport Protocol Port Number
Registry, and the "peep" URI scheme in the IANA URI Schemes registry.

--- middle

# Introduction

PEEP-0001 {{PEEP-0001}} defines *what* a polytemporal payload is. This
document defines *how to move it*: a stateless HTTP service that exposes a
brain's memory operations, and a one-hop federation model that lets recall
span many hosts. The reference implementation is `positronic-serve` (port
2114).

The transport is **thin and stateless**: every memory verb delegates to a
producer's memory ops, the server holds no conversation, and federation is a
bounded fan-out with reciprocal-rank fusion (RRF). There is no stateful
session and no connection-oriented semantics beyond HTTP itself.

# Terminology

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in {{RFC2119}}. All PEEP payload shapes are defined
in {{PEEP-0001}}.

# Base Protocol

## Transport

- HTTP/1.1 or HTTP/2.0. Request and response bodies MUST be UTF-8 JSON
  (`application/json`).
- The default well-known port is **2114**. Servers MAY bind other ports;
  clients MUST discover the port from the base URL.
- All `/v1/memory/*` endpoints are `POST` and carry a JSON body. Liveness and
  read-only discovery endpoints (`/healthz`, `/v1/federation/peers`) are
  `GET`.

## Endpoints

| method | path | public | description |
|---|---|---|---|
| `GET` | `/healthz` | yes | liveness: `{ok: bool, brain: str, peers: int}` |
| `POST` | `/v1/memory/recall` | no | PEEP-0001 recall hits (+ optional object digest) |
| `POST` | `/v1/memory/ask` | no | PEEP-0001 dossier for a named object |
| `POST` | `/v1/memory/consolidate` | no | write a consolidation summary event |
| `POST` | `/v1/memory/prune` | no | run tau-decay pruning on the live brain |
| `POST` | `/v1/memory/ingest` | no | ingest a new memory episode |
| `POST` | `/v1/memory/federated_recall` | no | local + peer recall, RRF-fused |
| `GET` | `/v1/federation/peers` | yes | configured peer list |

## Request/response shapes

`POST /v1/memory/recall`:

Request:

~~~ json
{"text": "what did we decide about the paper", "k": 8,
 "consolidation": null, "context_window": 0}
~~~

Response — a PEEP-0001 recall payload:

~~~ json
{"results": [ {"episode_id": "...", "tau": 1935.4, "wall": "...",
               "kind": "message", "salience": 0.5, "fallback": false} ],
 "object": {"canonical_name": "...", "versions": {...}}}
~~~

- `text` REQUIRED; `k` OPTIONAL (default 8); `consolidation` OPTIONAL
  (`null` | `"only"` | `"first"`); `context_window` OPTIONAL (integer >= 0).
- The `object` block is OPTIONAL and present only when the cue fuzzy-matches.

`POST /v1/memory/ask`:

Request: `{"object": "auth-system"}`

Response:

~~~ json
{"sightings": [ {"episode_id": "...", "tau": 16.2, "wall": "...",
                 "kind": "message"} ]}
~~~

`POST /v1/memory/consolidate`:

Request: `{"text": "summary...", "brain": "kairos", "arousal": 0.4}`

Response: `{"ok": true, "tau": 1935.4, "encoded": true, "episode_id": "..."}`

`POST /v1/memory/prune`:

Request: `{}`

Response: a prune report — `{"scanned": n, "day_merged": n, "week_merged": n,
"expired": n, "residues": n}`.

`POST /v1/memory/ingest`:

Request: `{"text": "a new memory", "brain": "kairos", "arousal": 0.5}`

Response: `{"tau": n, "encoded": bool, "episode_id": "..."}`

`POST /v1/memory/federated_recall`:

Request: `{"text": "...", "k": 8}`

Response — PEEP-0001 hits, each tagged with `source_host`, plus `sources`:

~~~ json
{"results": [ {"episode_id": "...", "tau": n, "source_host": "local"} ],
 "sources": ["local", "http://10.0.0.5:2114"]}
~~~

## HTTP error semantics

A server MUST use the following status codes:

| code | meaning |
|---|---|
| `200 OK` | successful retrieval, mutation, or prune sweep |
| `400 Bad Request` | request payload violates the data contract (missing `text` on recall, invalid `tau` float, malformed JSON) |
| `401 Unauthorized` | missing, expired, or invalid bearer token |
| `404 Not Found` | unknown brain name, or ask with an unknown entity cue |
| `502 Bad Gateway` / `504 Gateway Timeout` | peer unreachable during strict non-federated proxying (federated fan-out drops dead peers instead) |

The `400` response body SHOULD name the offending field:
`{"error": "invalid request", "field": "tau"}`.

# Authentication

## Model

The transport defines an authentication **seam**, not a single scheme. A
server MAY use any scheme that satisfies a minimal `KeyManager` contract:
validate a token against a scope. Two schemes are specified normatively.

## Local (development)

**`local`**: no token required. A server using this scheme MUST NOT bind
non-loopback interfaces; it is for development only.

## Single shared key

**`single`**: one bearer token. A client MUST send
`Authorization: Bearer <key>` on every `/v1/memory/*` request.

- A missing or wrong token MUST produce `401 Unauthorized`.
- A correct token MUST produce the normal response.

## Extension

Other schemes (Google, Azure, AWS, OAuth, and so on) MAY be implemented
behind the `KeyManager` contract. The server MUST only call
`validate(token, scope)`; it MUST NOT couple to a scheme's internals.

# Federation

## Peer registration

A server's configured peers are a list of base URLs, registered out-of-band
(config), not self-advertised.

## Fan-out semantics

`federated_recall` MUST:

1. run local recall on the configured brain;
2. fan out to each peer's `/v1/memory/recall` (single hop);
3. RRF-fuse the hit lists, dedup by `episode_id`;
4. tag each hit with its `source_host`;
5. return `{results, sources}`.

## Peer authentication scope

Under the `single` scheme, all participating peers share the **same
symmetric cluster token**; the fan-out forwards the server's own token to
every registered peer. This assumes a mesh of mutually trusted nodes.

Implementations MAY instead maintain **per-peer outbound tokens** (a distinct
credential per registered peer URL) when a peer is not fully trusted. A
server MUST NOT forward its master cluster token to a peer it does not trust.
The per-peer map is out-of-band configuration, like the peer list itself.

## Resilience

A peer that is unreachable, times out, or returns an error MUST be skipped —
recall MUST NOT fail because one peer is down. The response degrades to the
healthy subset.

## Recursion guard

Peers MUST be queried at their plain `/v1/memory/recall` (single hop). A
server MUST NOT recurse into a peer's `/v1/memory/federated_recall`.

## Timeout

The default per-peer timeout SHOULD be 3 seconds. A server MAY make this
configurable.

# Conformance

A server is PEEP-HTTP-compliant iff it satisfies the base protocol,
authentication, and federation requirements above. The executable conformance
gate (`validate-protocol.sh`) seeds a temporary brain, boots the server, and
checks endpoints, payload shape, the auth matrix, and live two-server
federation. The gate exits 0 iff every check passes.

# Security Considerations

- The transport carries PEEP-0001 payloads, which may contain arbitrary user
  text. Servers MUST treat memory content as untrusted and MUST NOT evaluate
  it.
- A `single`-key server MUST require TLS when not bound to loopback.
- Federation forwards the server's own token to peers. A server SHOULD only
  register peers it trusts with that token.
- `/v1/memory/ingest` and `/v1/memory/consolidate` write to the brain; they
  MUST be auth-guarded like reads.

# IANA Considerations

This document requests **three** registrations. All three were verified
unassigned against the IANA registries at the time of writing (2026-09-02).

## Service Name and Transport Protocol Port Number Registry

IANA is requested to register the following service name and port per
{{RFC6335}}:

| Service Name | Transport Protocol | Port | Description | Reference |
|---|---|---|---|---|
| `peep` | TCP | 2114 | Positronic Engram Exchange Protocol (HTTP transport) | this document |

- **Service name:** `peep` — length 4, valid per the RFC 6335 service-name
  syntax.
- **Port:** 2114 — in the Registered range (1024-49151); verified unassigned.
- **Description:** Port 2114 is requested for the Positronic Engram Exchange
  Protocol (PEEP), providing low-latency, deterministic transport for
  polytemporal memory stores, episodic consolidation, and federated
  reciprocal-rank recall.
- **Note (NDR-2114):** the port number doubles as a mnemonic — "2" for bi
  (Bicentennial Man, model NDR-114). The assignee is the PEEP protocol
  project (Shing Wong).

## URI Scheme

IANA is requested to register the **`peep`** URI scheme as a **Provisional**
registration in the "Uniform Resource Identifier (URI) Schemes" registry per
{{RFC7595}}:

| Scheme | Description | Reference |
|---|---|---|
| `peep` | Positronic Engram Exchange Protocol - locate a PEEP-HTTP memory service or a PEEP data object | this document |

**Registration tree:** Provisional. The scheme is specified by an open
specification with a public reference implementation; it may be elevated to
Permanent once it demonstrates widespread deployment, as {{RFC7595}} allows.

**ABNF syntax** — the `peep` URI conforms to {{RFC3986}} and is defined by
the following {{RFC5234}} ABNF:

~~~ abnf
peep-URI      = "peep:" hier-part [ "?" query ] [ "#" fragment ]
hier-part     = "//" authority path-abempty
authority     = host [ ":" port ]
host          = IP-literal / IPv4address / reg-name
port          = *DIGIT
path-abempty  = *( "/" segment )
~~~

Examples:

~~~
peep://10.0.0.5:2114/v1/memory/recall
peep://node1.local/v1/memory/ask
peep://10.0.0.5:2114/v1/memory/ask?object=auth-system
~~~

The host component addresses a PEEP-HTTP server; the path names the
operation (`/v1/memory/<operation>`). There is no opaque `peep:` object form
— all `peep` URIs are hierarchical and resolve to a service endpoint. This
avoids the ambiguous split between a service form and an opaque object form.

- **Character encoding:** ASCII, per {{RFC3986}}.
- **Intended usage:** locates a PEEP-compliant memory service, for use by
  agents and client libraries.
- **Applications using the scheme:** PEEP-compliant agents, the
  `positronic-serve` reference implementation, and federated memory peers.

## Expert Review

Per {{RFC6335}} and {{RFC7595}}, registration requests are subject to Expert
Review. The designated expert verifies: (a) no collision with existing
registrations, (b) the service name meets the syntax rules, and (c) the
scheme is used in a manner consistent with its specification.

## Security

The port and scheme registrations carry no security considerations beyond
those above: a `peep://` service MUST use TLS when not bound to loopback, and
the scheme MUST NOT be used to signal trust in the payload content.

# Acknowledgements

The PEEP protocol series is developed in the positron project.