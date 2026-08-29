# Episode Schema & Curator Contracts — v0 draft

> The design core: what a memory *is*, who curates it, and how it moves
> between tiers. Everything else (salience gate, consolidator, retrieval)
> hangs off these contracts.

## Episode record v0

```json
{
  "id": "uuid",
  "created": "2026-08-22T14:03:00Z",
  "last_access": "2026-08-22T15:10:00Z",
  "access_count": 3,
  "salience": 0.82,
  "source": {"agent": "bot01", "session": ":10", "kind": "game-screen"},
  "cue_tags": ["shop_screen", "wave3", "armor_purchase"],
  "modalities": {
    "visual": {
      "snapshot_refs": ["s3://frames/bot01/20260822_140300.jpg"],
      "scene_embedding": [0.12, -0.44, "..."],
      "extracted_state": {"screen": "alliance_help", "help_points": 300}
    },
    "text": {"summary": "Bought armor before wave 3; lost at wave 5"},
    "audio": null
  },
  "relations": [
    {"type": "contradicts", "ref": "<other-episode-id>"},
    {"type": "reinforces", "ref": "<other-episode-id>"}
  ],
  "tier": "episodic",
  "decay": {"half_life_days": 14, "protected_until": null}
}
```

## Semantic fact record (consolidator output)

```json
{
  "id": "uuid",
  "statement": "Armor-first build loses at wave 5 in solo defense",
  "derived_from": ["<episode-id-1>", "<episode-id-2>"],
  "confidence": 0.85,
  "domain": "game-strategy",
  "first_seen": "...", "last_confirmed": "...",
  "tier": "semantic"
}
```

## Curator contracts

| Curator | Domain | Owns | May NOT touch |
|---|---|---|---|
| project-state | task/goal/status facts | current objectives, blockers | user preferences |
| user-model | stable preferences/patterns | likes, habits, corrections | transient state |
| tech-facts | environment/config/tooling | versions, endpoints, procedures | episodic events |

Contract rules:
1. Each memory has exactly ONE owning curator (no dual-writes).
2. Cross-domain references go in `relations`, never copies.
3. Curators emit `memory.created` / `memory.updated` / `memory.superseded`
   events; the consolidator subscribes.

## Promotion path (episodic → semantic)

Trigger candidates (research, not settled):
- **Repetition**: same statement derived from N distinct episodes
- **Contradiction resolution**: two contradicting episodes → consolidate
  with confidence weighting
- **Age + access**: old + frequently accessed → promote and protect
- **Explicit**: agent/user marks a fact as permanent

## Decay policy v0

- Episodic default half-life: 14 days, refreshed on access (+50% per access,
  capped)
- Semantic: no decay; superseded-by-newer-fact instead (chain preserved for
  audit)
- Protected memories: pinned by explicit user/agent marking
