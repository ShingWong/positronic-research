# Brain Federation — access, import, and selective pruning

> The brain project's third act: memory is not one store but a FEDERATION
> of scoped stores with explicit sharing semantics. Three relationships any
> two brains can have: private, accessed-live, imported.

## The three relationships

| relationship | mechanism | provenance | revocable? |
|---|---|---|---|
| **private** | own episodes/objects/rules | native (`witnessed`) | n/a |
| **accessed-live** | query remote brain via `activate()` fan-out; nothing copied | results marked `source=<brain>` per call — never stored unless re-encoded deliberately | yes — unsubscribe |
| **imported** | objects/rules (semantic layer) copied in with origin tags; raw episodes only by explicit policy | `origin_brain` + `imported_at` stamped on every row | harder — imported knowledge entangles; prune by origin tag |

## Selective pruning (implemented v0)

`prune(domain='kairos')` scopes the entire ladder pass by domain. Verified:
mail domain untouched while kairos deep-primes, and vice versa. This is the
answer to "we don't want memory derived from his email" — origin-scoped
hygiene as a first-class operation.

## Domain = jurisdiction

Every episode/object carries `domain_id`. The domain IS the jurisdiction:
its retention profile governs decay; its boundary governs prune scope;
its name governs sharing policy. Kairos runs `kairos` (long_term) and
consumes `mail` (long_term) without merging them.

## Domain-specific brains (legal / accounting / coding)

A curated domain brain holds: objects + characteristics + causal rules +
affordances — the SEMANTIC layer, no raw episodes. Sharing policy:
- **access**: agent subscribes; queries fan out; answers cite source brain
- **import**: rules/objects copied with origin stamps → become prunable
  by origin ("drop legal-brain v1 when subscription lapses")

Privacy corollary (from mail pilot): import SEMANTIC layers freely between
one's own brains; import across ORGANIZATIONS only as curated rule/object
sets, never raw episodes.

## Open problems

1. Cross-brain τ: each brain has its own clock; activation-currency fusion
   (T2) needs a shared "now" per comparison.
2. Contradiction handling: imported rule conflicts with native experience
   (SSGM governance problem) — resolution order: native witnessed >
   imported stated?
3. Revocation propagation: forgetting an imported object must cascade to
   conclusions that cited it.
