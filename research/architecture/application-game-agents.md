# Application Target: Game-Agent Benchmarks & Persistent Play

> The llmem system's first killer app: game-playing agents that *learn across
> sessions*. Aligns with the emerging benchmark family testing LLM/VLM agents
> on actual games (BALROG — NetHack/Crafter/BabyAI; GameBench — real game UIs;
> VisualAgentBench; post-"Claude Plays Pokémon" wave).

## Why our rig maps to these benchmarks

| Benchmark demand | Rig capability |
|---|---|
| Screen observation | Xvfb frames → OpenCV/Coral tier → VLM extraction (production, 17 streams) |
| Action execution | gt-spector locator/click stack (proven) |
| Goal coherence | FastMTP-class main agent |
| Long-horizon memory | **llmem federation — the missing piece everywhere else** |

## The thesis: cross-session memory is the unsolved axis

Current submissions reset every episode. Same blunders, run after run.
With llmem, an agent accumulates:

- **Familiarity tier**: recognize screens/states seen in prior sessions
  ("this is the shop inventory layout")
- **Detail tier**: structured outcomes ("armor-first build lost at wave 3,
  session 2026-08-20")
- **Semantic tier**: consolidated strategy ("prioritize economy before wave 5")
- **Episodic index**: sparse pointers to notable past events

That converts a benchmark from *testing* an agent into *training-by-living*:
every episode improves every future episode.

## Why 17 instances matter

Population-level experience collection: same game, independent accounts and
choices → consolidation sees diverse trajectories of the same environment →
stronger semantic distillation than any single-run agent can produce.
This is experiment infrastructure, not just gameplay.

## Evaluation plan (doubles as harness design)

1. Pick one benchmark environment runnable under Wine/headless (candidate:
   BALROG's NetHack — native Linux, deterministic seeds; or GameBench-style
   Android/UI games via our existing stack).
2. Baseline: current bot behavior, memoryless.
3. Treatment A: + familiarity tier only.
4. Treatment B: + full federation (curators + consolidator).
5. Metric: per-episode score delta across sessions; time-to-first-success;
   strategy stability under perturbation.

This doubles as the llmem evaluation harness (README open question #6):
games provide ground-truth scoring that subjective "memory quality" lacks.
