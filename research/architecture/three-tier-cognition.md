# Three-Tier Cognition — Reflexes, Fast Brain, Deep Brain

> System 1 / System 1.5 / System 2 (Kahneman) mapped onto the bot farm.
> The farm already has reflexes (scripts + link graph); this adds the
> trained-intuition layer between reflexes and deliberate reasoning.

## The tiers

| Tier | Engine | Trigger | Latency | Cost |
|---|---|---|---|---|
| **Reflexes** | OpenCV templates + game_world.yaml link graph | known screens | <50 ms | free |
| **Fast brain** | **MiniCPM-V 4.6** (multimodal, tool-use-tuned) | unknown screens, semi-novel variants | ~seconds | small |
| **Deep brain** | HauhauCS IQ4_XS (+ embedded reasoning) | truly novel situations, strategy, learning | tens of seconds | large |

## Why MiniCPM-V 4.6 for the fast brain

1. **Native vision**: takes raw frames directly — novel screens need no
   pre-built template or OCR heuristics. Cold-start solved by construction.
2. **Tool-use training**: emits reliable structured action calls (the
   click/decision contract), not prose that needs parsing.
3. **Prompt coherence**: holds the JSON contract across long sessions.
4. **Low hallucination**: RLAIF-V tuned — matters when decisions drive clicks.
5. **llama.cpp-native** (GGUF), LoRA-fine-tunable via SWIFT/LLaMA-Factory.

## The promotion flywheel (compounding)

```
novel screen → deep brain analyzes + decides     (slow, expensive)
             → decision LOGGED (state JSON in, action out)
             → screen record built → scripts take over forever
             → log ALSO curates into fast-brain training set
periodically → LoRA-distill deep-brain decisions into MiniCPM-V
             → fast brain covers more novelty without escalation
metric      → % of situations resolved WITHOUT deep-brain escalation
              climbs over time = expertise graph rising
```

Two memory systems grow simultaneously: game_world.yaml (procedural/scripts)
and the fast brain (learned intuition). Deep brain shifts toward genuinely
new territory — which is exactly what expertise progression looks like.

## Deployment notes

- MiniCPM-V 4.6: ~8B params; Q4 GGUF ≈ 5 GB + mmproj. Current MI50 is full
  (games + main agent) — interim options: CPU-resident inference (viable at
  novel-event volume), on-demand load/unload, or dedicated slot post-2nd-card.
- Vision encode adds ~1–3 s/image on CPU; acceptable at event-driven rates.
- Escalation contract: fast brain outputs confidence; below threshold →
  deep brain handles + trains.

## Open questions
- Quant choice for latency vs accuracy on game UIs (Q4 vs Q5)
- Cross-session consistency: same screen → same decision? (temperature 0)
- Fine-tune cadence and curation of training logs (ties to llmem consolidator)

## Benchmark results (2026-08-22, live game frame, help-loop screen)

| Candidate | Config | Latency | Result |
|---|---|---|---|
| Deep brain (IQ4_XS+vision, MI50) | MTP n4, medium effort | 21.5s | correct, spec overhead wasteful |
| Deep brain, spec overridden per-request | n0 | 16.7s | correct |
| MiniCPM-V 4.6 Q6_K (CPU, local VM) | base | 14–17s | good detail, correct |
| **Ornith-1.0-35B @ ai2 (thinking off)** | **MTP n2 stays on** | **6.4s over LAN** | **live OCR accurate (help-points counter read from frame)** |
| Ornith baseline thinking-on | defaults | 50.8s | ❌ max_tokens consumed by reasoning, empty answer |
| Ornith reasoning_effort=low | kwarg | 40.3s | ❌ template ignores effort kwarg |

### Findings
1. `enable_thinking:false` is the vision-workload switch: 8x faster than
   thinking-on, accurate structured extraction with live OCR.
2. Speculative decoding (MTP/FastMTP) is NET-NEGATIVE for short vision
   outputs — disable per-request via request overrides when serving VLM.
3. `reasoning_effort` kwarg unsupported by Ornith template; use
   enable_thinking instead.

## Capacity doubling (2026-08-22)

Second identical Ornith server on **ai1** (faster rig) — load-balance
fast-brain requests across both endpoints → ~2x decision throughput,
redundancy, and headroom for all 17 sessions' novelty queue.
