# Cognitive Foundations: How Human Memory Actually Works

> Research seed. Claims marked **[verify]** need literature confirmation.

## 1. The taxonomy is functional, not structural

Human memory is not one store. The classic decomposition (Atkinson–Shiffrin
1968, elaborated by Tulving 1972/1985):

| System | Content | Timescale | Substrate |
|---|---|---|---|
| Sensory buffer | raw percepts | <1 s | modality cortices |
| Working memory | active manipulation | seconds | prefrontal + parietal |
| Episodic | *events, "what-where-when"* | lifetime, but fragile early | hippocampus |
| Semantic | *facts distilled from events* | lifetime, stable | neocortex (distributed) |
| Procedural | *skills, how-to* | lifetime, very stable | striatum, cerebellum |

**Agent mapping insight:** most LLM memory projects implement episodic storage
(transcripts/logs) and call it done. They skip semantic distillation entirely
and procedural memory not at all. Humans offload nearly everything to semantic
+ procedural and keep episodic as a sparse index.

## 2. Encoding: attention is the gate

The hippocampus does not record passively. Salience gates what encodes:
- Novelty, emotional valence, goal-relevance boost encoding (amygdala/dopamine modulation)
- Most experience is discarded within seconds — this is a *feature*
- Divided attention at encoding = poor recall later (Craik & Watkins levels-of-processing)

**Open question for llmem:** what is our salience signal? Explicit scoring by
a small model? Contradiction with existing memory? User affect markers?
Probably all three with different weights. **[investigate]**

## 3. Systems consolidation: sleep is the write path

Episodic memories are initially hippocampus-dependent. Over time (days–years)
they reorganize into distributed neocortical representations — systems
consolidation. Sleep (especially slow-wave) drives hippocampal *replay* to
neocortex (Wilson & McNaughton).

Key properties worth stealing:
- **Replay is selective**: consolidation prefers reward/novelty/relevant traces
- **Distillation happens during replay**: gist extracted, detail dropped
- Two theories compete: standard consolidation (hippocampus eventually
  unnecessary) vs multiple-trace theory (episodic detail persists; semantics
  accrete separately). Both can be true per-memory-type. **[verify]**

**Agent mapping:** the CONSOLIDATOR's "sleep" cycle = offline replay job:
re-read recent episodic entries, extract/update semantic facts, merge
contradictions, decay unreinforced traces. Cadence matters (nightly?) as does
selectivity (don't consolidate garbage).

## 4. Retrieval is reconstruction, not playback

Bartlett (1932) → modern view: recall rebuilds a plausible scene from sparse
cues + semantic knowledge. Consequences:
- Memories are *lossy schemas plus pointers*, not transcripts
- Retrieval is generative — and fallible (misattribution, confabulation)
- Each retrieval *reconsolidates* the trace, subtly rewriting it

**Agent implication:** store structured fragments (entities, relations,
timestamps, confidence) + enough context cues to reconstruct, rather than raw
transcripts. Accept probabilistic reconstruction. Design the format so
re-consolidation (updating on retrieval) is natural.

## 5. Forgetting is adaptive, not failure

- Decay curves exist but are secondary to interference
- Retrieval-induced forgetting: retrieving A suppresses competing B
- Directed forgetting: humans can discard on cue when told context changed
- Without forgetting, generalization collapses (catastrophic interference in
  neural nets without decay/regularization)

**Agent implication:** forgetting policy is first-class design, not an afterthought.
Candidate signals: recency, access count since write, contradiction count,
source reliability.

## Reading list to work through
- Tulving, *Elements of Episodic Memory* (1983)
- Squire & Alvarez, systems consolidation review
- Baddeley, *Working Memory* models
- McClelland et al. 1995, "Why there are complementary learning systems"
- Kandel, *In Search of Memory* (mechanistic grounding)

## Open questions carried forward → architecture/
- Domain taxonomy for curators (fixed vs learned; see §1 functional split as starting point)
- Salience function design (§2)
- Consolidation cadence + selectivity (§3)
- Storage format for reconstructive retrieval (§4)
- Decay/forgetting policy (§5)
