# Hardware Tiering — From Photons to Memory

> Architecture note. Maps compute hardware to the cognitive pipeline so each
> stage runs on the cheapest silicon capable of it — mirroring how the retina
> pre-processes vision before the brain spends anything.

## The insight

Human vision works because the retina is not a camera — it's a *processor*.
Edge detection, motion sensing, and contrast normalization happen before any
cortical neuron fires. Only ~1% of optic-nerve bandwidth carries attended
signal onward.

Our stack can do the same:

```
Tier 0 · RETINA        OpenCV on CPU + Coral TPU      (~5 W combined)
                       frame capture · decode · diff · classify · embed
                              │  only state-changes / salient events
                              ▼
Tier 1 · ATTENTION     Salience gate (small model, MI50 or CPU)
                       event scoring · episode boundary detection
                              │  salient episodes only
                              ▼
Tier 2 · CORTEX        VLM distillation on MI50 (mmproj, already live)
                       structured state extraction → detail-tier memory
                              ▼
Tier 3 · SLEEP         Consolidator (off-cycle batch)
                       episodic→semantic promotion · decay · merge
```

## Tier assignments

| Stage | Hardware | Why |
|---|---|---|
| Frame capture/decode | OpenCV, CPU | I/O bound; gt-spector `locator.py` pattern proven at scale (17 streams) |
| Frame differencing | OpenCV, CPU | cheap numpy ops; game-state change detection ≈ free salience pre-filter |
| Scene classification / detection | **Coral TPU** | INT8 MobileNet/EfficientNet-Lite class models at ~4 TOPS / 2 W; always-on duty without touching MI50 |
| Scene embeddings (familiarity tier) | **Coral TPU** | MobileNet embeddings per snapshot → "seen this state?" lookups |
| VLM structured extraction | MI50 (mmproj active today) | only N salient events/day; already benchmarked via `vlm.py` |
| Consolidation cycles | MI50, idle windows | 8B-class consolidator; night-cadence |

## Why the Coral matters

- **Power discipline**: continuous perception at ~2 W means the sensory
  cortex never sleeps and never costs anything — production-safe 24/7.
- **MI50 isolation**: the inference GPU stops being interrupted by
  preprocessing bursts; its thermal envelope stays dedicated to tg/pp.
- **Latency floor**: sub-ms classification enables real-time salience
  gating (event boundaries detected while frames are still hot).

## Constraints to investigate

- Edge TPU runs **fully int8 TFLite** only; conversion required for any
  candidate model; op coverage is limited (no dynamic shapes).
- One model compiled per Edge TPU context; batching is manual.
- USB vs M.2 vs PCIe variant: pick per host slot availability on met-kvm;
  USB has known latency jitter under load. **[decide]**
- Fallback path if Coral saturates: same TFLite models on CPU via XNNPACK
  (slower, still cheap).

## Cognitive parallel

Retina : cortex :: Coral+OpenCV : MI50. Pre-processing moved to dedicated
low-power substrate is not an optimization here — it is the architecture.
The expensive system should only ever see *attended, distilled events*.

## The multi-session scaling wall (observed in production)

VLM analysis of live frames saturates at ~1 concurrent session: each
analyze_frame call takes seconds on the shared MI50, so 17 streams cannot be
served. This is the practical blocker for sensory memory at fleet scale.

### Coral as the unblocking lever
Tier 0 classification/embedding across all 17 streams (~85 FPS aggregate)
fits trivially in 4 TOPS. VLM invocations become event-driven (state-change
gated) rather than continuous — converting an unservable queue into a
trickle. The VLM remains the detail-tier distiller; the Coral owns attention.

### Interim mitigation (pre-Coral, deployable now)
OpenCV frame-diff gate on CPU: `cv2.absdiff` mean above threshold → queue
VLM extraction. Static menu screens produce zero diffs. Expected VLM-call
reduction ~90%, unblocking multi-session operation today; the Coral slot
replaces the same gate with smarter semantics later.

## Reality check (2026-08-22): Tier 0 already exists in production

gt-spector's OpenCV stack (locator.py + game_world.py) performs game-screen
identification across all 17 streams at <50 ms each, entirely on CPU.
Consequences:

1. Tier 0 is not greenfield — the retina is deployed and proven.
2. Its output doubles as a FREE salience/event stream: every screen
   transition identified by locator.py is a labeled episode boundary —
   episodic memory can key off existing perception with zero new cost.
3. The Coral's role narrows to what OpenCV cannot do: neural embeddings for
   the familiarity tier (semantic scene similarity, UI-update resilience).
   That makes it a Phase-2 optimization for cross-session memory, not a
   prerequisite for multi-session visual memory (Phase-1 gate = frame-diff +
   locator events, deployable now).
