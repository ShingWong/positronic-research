# PEEP ISE Submission Package

Two Internet-Drafts, two submission emails to
`rfc-ise@rfc-editor.org` (ISE: Eliot Lear). Each email must include the
exact elements below per the ISE checklist.

---

## Email 1 — Data Contract

**To:** rfc-ise@rfc-editor.org
**Subject:** Independent Submission: draft-peep-data-contract-00

Dear Eliot Lear,

I am submitting the following Internet-Draft for consideration as an
Independent Submission RFC:

**Internet-Draft file name:**
`draft-peep-data-contract-00`

**Desired category:** Informational

**Summary of related discussion:**
No IETF working group or IESG discussion has occurred. The document is an
independent specification produced outside the IETF process. The companion
transport draft (`draft-peep-http-transport-00`) is submitted separately;
the two are designed as a pair (data contract + transport binding).

**IANA allocation assertion:**
This document requests no IANA allocations and does not require IETF Review
or Standards Action. It has no IANA Considerations actions of its own; the
companion transport draft requests a service name, port, and URI scheme
registration (Expert Review policy only, not IETF Review / Standards Action).

**Purpose, intended audience, merits, and significance:**

*Purpose.* PEEP (Positronic Engram Exchange Protocol) defines the structure
of polytemporal data a memory engine delivers to a reasoning agent: the
per-hit record, the entity digest (a "peep"), and the tau-ordered dossier.
It is the standard interface of an agent memory system, decoupling any
consumer from the engine that produced the data.

*Intended audience.* Agent developers, LLM memory-system implementers, and
anyone building persistent memory for AI agents — the opencode, Claude Code,
and custom-agent communities.

*Merits.* Agent memory is a fast-moving field with no shared data contract;
every system invents its own payload. PEEP defines a minimal, self-describing
contract where each record carries its polytemporal vector (tau, wall,
provenance, salience). Compliance is machine-checkable: an executable
conformance suite (5 tests) proves a producer's payloads conform, so the
spec is enforceable, not aspirational.

*Significance.* This addresses interoperability directly: any agent that
speaks PEEP can consume polytemporal memory from any producer. It provides
the missing interface layer for the emerging class of memory-capable agents,
with an open reference implementation (positronic-engram /
positronic-agent-interface, GPL-3.0).

**IPR acknowledgment:**
I acknowledge that the IPR rules of RFC 4846 and RFC 5744 apply, and unless
stated otherwise, permission is granted to produce derivative works, in
whole or in part, as stated in those RFCs.

**Suggested independent reviewers:**
1. A memory/RAG systems researcher (contact available on request).
2. An LLM agent-framework maintainer (contact available on request).

The document and its artifacts are available at:
- https://github.com/ShingWong/positronic-research (papers/positronic-prism/rfc/PEEP-0001.md)
- https://github.com/ShingWong/positronic-engram (reference implementation)
- https://github.com/ShingWong/positronic-agent-interface (producer, PEEP conformance suite)

Regards,
Shing Wong
swong@stuartconsultinggroup.com

---

## Email 2 — HTTP Transport

**To:** rfc-ise@rfc-editor.org
**Subject:** Independent Submission: draft-peep-http-transport-00

Dear Eliot Lear,

I am submitting the following Internet-Draft for consideration as an
Independent Submission RFC:

**Internet-Draft file name:**
`draft-peep-http-transport-00`

**Desired category:** Informational

**Summary of related discussion:**
No IETF working group or IESG discussion has occurred. The document is an
independent specification produced outside the IETF process. It is the
transport binding for the companion data-contract draft
(`draft-peep-data-contract-00`), submitted separately.

**IANA allocation assertion:**
This document requests the registration of the `peep` service name and TCP
port 2114 (RFC 6335) and the `peep` URI scheme (RFC 7595). Both are Expert
Review policy per RFC 8126 — **not** IETF Review or Standards Action. No
IANA registry action in this document requires IETF Review or Standards
Action. All three registrations were verified unassigned at the time of
writing.

**Purpose, intended audience, merits, and significance:**

*Purpose.* This document specifies the HTTP transport for PEEP-0001 payloads:
the endpoints, request/response shapes, authentication model, and federation
semantics that let a polytemporal memory service expose its brains to clients
and fan recall out across peer hosts. It is the "brain as a service" and
"brain federation" interface.

*Intended audience.* Operators and developers who want to expose or federate
a memory service over HTTP — agent platforms, memory-as-a-service providers,
and multi-host memory deployments.

*Merits.* The specification is thin and stateless: every verb delegates to a
producer's memory ops; federation is a one-hop fan-out with reciprocal-rank
fusion, an unreachable peer never fails recall, and a recursion guard bounds
the fan-out. A reference implementation (`positronic-serve`, GPL-3.0) ships
with an executable conformance gate (12 checks, including a live two-server
federation test), so compliance is machine-checkable.

*Significance.* It defines a standard, interoperable way to expose polytemporal
memory over the network — the transport layer for the agent-memory contract.
It directly improves interoperability between memory producers, agents, and
federated memory hosts.

**IPR acknowledgment:**
I acknowledge that the IPR rules of RFC 4846 and RFC 5744 apply, and unless
stated otherwise, permission is granted to produce derivative works, in
whole or in part, as stated in those RFCs.

**Suggested independent reviewers:**
1. A distributed-systems / federation researcher (contact available on
   request).
2. A network protocol / HTTP API designer (contact available on request).

The document and its artifacts are available at:
- https://github.com/ShingWong/positronic-research (papers/positronic-prism/rfc/PEEP-0002.md)
- https://github.com/ShingWong/positronic-serve (reference implementation + conformance gate)

Regards,
Shing Wong
swong@stuartconsultinggroup.com

---

## Pre-submission checklist

- [ ] Post `draft-peep-data-contract-00.xml` to the Datatracker
      (authors.ietf.org: create account → upload I-D)
- [ ] Post `draft-peep-http-transport-00.xml` to the Datatracker
- [ ] Send Email 1 (data contract) to rfc-ise@rfc-editor.org
- [ ] Send Email 2 (transport) to rfc-ise@rfc-editor.org
- [ ] Wait for ISE initial review (Step 4); be ready to iterate
- [ ] Note: IETF Conflict Review may follow; the ISE handles the coordination

## Notes for the ISE lens (from the ISE's three questions)

1. **Improves interoperability?** Yes — PEEP is a shared data contract +
   transport for agent memory; any producer/consumer pair that speaks it
   interoperates without coupling.
2. **Continuous improvement of the Internet?** Yes — agent memory is an
   emerging Internet-scale application class; a standard interface improves
   the ecosystem.
3. **Levity?** The port 2114 "NDR-2114, '2' for bi" (Bicentennial Man)
   mnemonic is the light touch — a memorable nod that a reviewer may smile at.