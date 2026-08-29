# Sensory Memory: Visual & Audio Foundations

> Research seed. The senses feed memory; each modality has its own buffer,
> encoding economics, and loss profile. For agents, this is the frontier:
> most current memory work is text-only while real agent experience is
> screens, sound, and interaction.

## 1. The sensory buffers (pre-attention)

| Buffer | Modality | Duration | Capacity |
|---|---|---|---|
| Iconic | visual | ~0.5 s | large but pre-categorical (Sperling 1960) |
| Echoic | auditory | ~2–4 s | moderate; survives attention better |

Sperling's partial-report experiment proved a rich brief buffer exists that
is discarded *unless attended*. Attention selects; only selected content
becomes working memory.

**Agent mapping:** raw frames/audio are the iconic buffer. Retention policy:
seconds-to-minutes at full fidelity, then either attended (→ distilled into
structured memory) or dropped. Never hoard raw captures by default.

## 2. Visual episodic memory is enormous

- Standing (1973): recognition for ~10,000 distinct pictures at ~83%+
- Picture superiority effect: images remembered far better than words
- But recognition ≠ recall: humans know they've seen something without being
  able to reconstruct it — vast *familiarity* store, sparse *detail* store

**Agent mapping:** two-tier visual memory.
1. **Familiarity tier:** cheap embeddings of scene snapshots → "have I seen
   this state before?" (game bots: level/screen recognition)
2. **Detail tier:** on salient events, extract structured description via VLM
   (entities, UI state, scores) — not the pixels.

## 3. Auditory/verbal memory: the phonological loop

Baddeley's working-memory subsystem: speech/sound held in a rehearsal loop
(~2 s capacity). Language is how most human semantic memory gets encoded —
heard → rehearsed → recoded into meaning.

**Agent mapping:** audio arrives as streams; transcription (Whisper-class)
converts to the text pipeline early. Native-audio memory only matters if the
agent must remember *sound qualities* (voice ID, alarms, prosody).
**[investigate]** whether our use cases need non-transcribed audio retention.

## 4. Cross-modal binding: one episode, many senses

An episode binds what was seen, heard, and done into a single retrieved event
(episodic "binding problem"; hippocampus as the binder).

**Agent implication:** an episode record should reference its modalities:
```
episode {
  time, cue-tags,
  visual: [snapshot-embeddings, VLM-extracted-state],
  audio:  [transcript-segments],
  actions:[what the agent did],
  salience: score, source-reliability: weight
}
```
Retrieval reconstructs across references rather than replaying any single stream.

## 5. Direct relevance to our rig

- 17 game instances × continuous frames = infinite iconic buffer supply
- gt-spector `vlm.py` already extracts structured state from frames
  (analyze_frame → JSON) — that IS the detail-tier distiller, half-built
- The MI50 serves vision natively today (mmproj active)
- Salience gate can key on frame-diff + game-state change instead of LLM cost

## Open questions
- Frame sampling cadence vs event detection (diff-based? **[investigate]**)
- Embedding model choice for scene familiarity tier
- Storage budget: embeddings per snapshot vs structured extractions only
- Audio: do we have any live sources, or defer echoic track? **[decide]**
