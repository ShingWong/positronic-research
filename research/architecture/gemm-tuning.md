# GEMM Tuning Opportunity (gfx906 decode path)

> Preserved finding — do the sweep after context compaction.

## State as of 2026-08-22

- **No runtime GEMM tuner exists** in llama.cpp (BeeLlama v0.4.3 or upstream
  32703b4): no `GGML_CUDA/HIP_TUNE`, no cache, no auto wave-sweep. Grepped
  entire ggml-cuda/ggml-hip — zero hits.
- Kernel geometry is **compile-time hardcoded** per architecture table.
- Decode (batch=1) uses MMVQ (`ggml_cuda_should_use_mmvq`), gated per-arch and
  per-quant-type via `get_mmvq_mmid_max_batch_cdna(type)`.

## The gfx906 values (generic, untuned)

`mmvq.cu` → `get_device_table_id`:
- gfx906 (GCN/CDNA1) → `MMVQ_PARAMETERS_GCN`
- `calc_nwarps`: **2 warps** for ncols_dst 1–4, **1 warp** for 5–8
- `calc_rows_per_block`: **1 row** (generic)

Contrast: CDNA2 (MI200) table uses `rows_per_block=2`, explicitly commented
"2 gives best perf based on tuning". gfx906 gets the generic fallback, NOT
tuned values.

## Why it matters

Decode on gfx906 is **ALU-bound** (no tensor cores) — proven earlier
(`docs/gfx906-throughput-analysis.md`, in dls repo: Q8/F16 ≈ 2x effective
bandwidth of Q4, ALU ceiling not memory). ALU-bound kernels are exactly where
occupancy (nwarps, rows_per_block) determines throughput. The GCN values are
fallbacks — plausible headroom exists.

## RESULT — sweep run 2026-08-24

| nwarps | rows | t/s | note |
|---:|---:|---:|---|
| 2 | 1 | 17.98 ± 0.38 | production default (baseline) |
| **1** | **1** | **19.60 ± 0.47** | **winner, +9.0%** |
| 4 | 1 | 16.06 ± 0.37 | |
| 1 | 2 | 19.38 ± 0.89 | tie w/ rows=1 |
| 1 | 4 | 18.38 ± 0.52 | |

nwarps=8 skipped: trend 1 > 2 > 4 monotonic (ALU-bound occupancy). Confirmed in
production: server live at 20.91 t/s (500 tok, thinking off, MTP n-max=4).

### small_k follow-up
IQ4_XS: blocks_per_iter = 8*nwarps. nwarps=2 leaves a full warp idle on K=2048
layers (8 blocks vs 16). small_k (rows=nwarps) was the codebase's partial fix,
but IQ4_XS is excluded from it (register pressure). Decisive test:
nwarps=2+small_k = 19.06 t/s (beats 17.98 baseline) but still < nwarps=1 (19.60).
nwarps=1 is the clean fix. No further rows/small_k headroom for IQ4_XS.

Change: one line in `mmvq.cu` GCN `calc_nwarps`, ncols_dst=1: `return 2` → `return 1`.
Full method + rationale in dls `docs/gemm-tuning.md`.

## Follow-up — HIP graphs + VGPR occupancy (2026-08-24)

- **HIP graphs regress decode**: GGML_HIP_GRAPHS was already ON and active, but
  graph replay overhead > launch savings on ROCm 5.7. `GGML_CUDA_DISABLE_GRAPHS=1`
  → 23.65 vs 20.76 t/s (tg128 r7). Disabled in /etc/llama.config.
- **wavefront 64 already**: gfx906 native; `__GFX9__` → 64 in code. Flag redundant.
- **VGPR occupancy at ceiling**: IQ4_XS decode = 30 VGPR / 24 SGPR / 0 LDS
  → 8 waves/SIMD (80% of 10 max). Enough to saturate VALU; no headroom.

Net raw decode: 17.98 → 23.65 t/s (**+31.5%**). Production live 22.88 t/s.
Detail: dls `docs/hip-graphs-vgpr-occupancy.md`.

## Related, already banked

- Decode ALU-bound proof: dls `docs/gfx906-throughput-analysis.md`
- FastMTP depth sweep: dls `docs/fastmtp-port.md` (n-max 4 optimal)
- Three-tier cognition + Ornith benchmark: llmem `research/architecture/`

## Compile-flag probes (2026-08-24) — neutral, reverted
`-funsafe-math-optimizations -munsafe-fp-atomics` on ggml-hip: tg128 23.56 vs
23.65 baseline (neutral — decode is V_DOT/DP4A integer-bound). Bonus bug:
CMAKE_HIP_FLAGS never reaches the compile under CXX_IS_HIPCC, so the
maintainer-intended fast-math was silently a no-op. Not worth shipping.

## Batch size sweep (2026-08-24) — np=4 shipped, FastMTP retired
Batching scales aggregate decode: np2 1.38x, np4 1.67x, np8 2.03x. Lone
requests on multi-slot servers run full speed (continuous batching). MTP is
-36% when batched (draft overhead; batching already amortizes weight-reads)
and was neutral solo after graphs-off — retired from production. Live:
22.9 t/s lone / 36.3 t/s at 4 concurrent.

## -ub sweep (2026-08-24) — shipped -ub 2048
Prefill micro-batch 512->2048: pp1536 187.8->199.5 t/s (+6.2%); flat for short
prompts; -b irrelevant; decode unaffected. Vision prompts (~1024 img tokens +
text) are the deep brain's prefill path.

## HIP_FORCE_DEV_KERNARG / HSA_ENABLE_SDMA (2026-08-24) — neutral, not shipped
Round-one load deltas (-28%) failed to reproduce; warm reloads ~13-16s for all
configs, cold loads NVMe-bound. KERNARG decode also neutral. Left unset.

## MTP restored (2026-08-24) — acceptance-rate is the missing variable
Coding prompt A/B: lone 32.5 vs 22.8 t/s (+42%); x4 parity. MTP pays when
draft acceptance is high (code), wastes compute on prose. Reconciles: prose
solo neutral / prose np4 -36% / code np4 +2%. Production = MTP n-max=4 +
np=4 + graphs-off + -ub 2048.
