# LLM Agent Memory Landscape — Survey Seed

> Research seed. Each entry: mechanism → what it solves → structural flaw
> through the multi-specialist lens. **[verify]** marks claims needing a fresh
> look at current docs/repos before we rely on them.

## The pattern to test against

Nearly every project answers "how should an agent remember?" with *one brain*:
a single frontier model deciding what to keep, plus (usually) one vector index
deciding what's relevant. Our hypothesis says the win is in **federation**:
small specialized curators + consolidation cycles. So for each project ask:
(1) who decides salience? (2) who distills? (3) is there a sleep cycle?
(4) does memory reconstruct or replay?

## Projects

### MemGPT / Letta
- Mechanism: OS analogy — main context = RAM, archival/recall storage = disk;
  the LLM itself issues paging instructions via function calls.
- Solves: context-window overflow; self-directed retrieval.
- Flaw: the conductor manages the archive with its full attention cost;
  no offline consolidation; episodic hoarding tendency; salience = whatever
  the model notices mid-task.

### Mem0
- Mechanism: extraction of candidate memories from conversations, embedding
  dedup/merge, tooling around add/search/update/delete.
- Solves: turn-key pipeline; decent extraction prompts.
- Flaw: single-model extraction & consolidation; similarity-based merge
  conflates distinct facts; no domain specialization; decay policy thin.

### Zep / Graphiti
- Mechanism: temporal knowledge graph — entities, relations, validity
  intervals; hybrid search (semantic + BM25 + graph walk).
- Solves: temporal validity ("X was true from A to B"), entity resolution,
  structured queries.
- Flaw: graph curation heuristics, not judgment; still one model deciding
  edges; domain taxonomy absent.

### HippoRAG
- Mechanism: neurobiologically-inspired RAG mirroring hippocampal indexing
  theory (PPR over a Personalized PageRank graph of NER'd concepts).
- Solves: multi-hop retrieval; explicitly borrows the right neuroscience.
- Flaw: it is *retrieval only* — no encoding gates, no consolidation, no
  forgetting. Borrows the index, skips the lifecycle.

### Cognee / A-MEM / others **[survey deeper]**
- A-MEM: agentic Zettelkasten — notes that link and evolve. Closest in spirit
  to reconstruction; check maturity.
- Cognee: pipelines data into KG + vectors. Same single-model curation issue.

### Vector-DB-as-memory (Chroma/Qdrant/pgvector patterns)
- The default everyone falls into. Nearest-neighbor lookup ≠ relevance;
  remembers everything indiscriminately; no lifecycle.

## Gap analysis → our differentiation

| Lifecycle stage | Landscape coverage | llmem answer |
|---|---|---|
| Salience gating | ❌ mostly absent | dedicated tiny gate model |
| Domain partition | ❌ single namespace | specialized curators |
| Distillation (episodic→semantic) | partial (Mem0 merge) | consolidator model, off-cycle |
| Forgetting/decay | ❌ rare, crude | first-class policy per curator |
| Reconstructive retrieval | ❌ transcript replay | fragment + cue format |
| Cost model | frontier-model tax | billion-scale curators on idle GPU |

## Survey method notes
- For each project: read docs + key paper; note license, runtime footprint,
  whether curation can be swapped for our small models (integration path!).
- Several could serve as *storage layers* under our federation — we may not
  need to rebuild persistence at all. **[investigate]**

## Multimodal memory (visual/audio) — landscape seed

- **Vision-language RAG / Video memory**: embedding-based retrieval over
  frames/clips (CLIP-class indexes). Replay-style: returns pixels, not state.
  Missing the two-tier split (familiarity vs structured detail).
- **Screen-recording agent memories** (e.g., computer-use agents): recent
  push toward screenshot histories for UI agents. Hoarding tendency; salience
  gates rare; VLM distillation per frame is costly without event detection.
- **Audio**: mostly transcription→text pipelines (sensible default). Native
  audio-event memory is research-grade.
- **Our edge**: gt-spector already has frame capture + VLM state extraction
  in production; the salience gate can be game-state diffing rather than an
  LLM call. This may be the cheapest real-world sensory-memory lab available.
