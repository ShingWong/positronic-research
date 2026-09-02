# Level-1 Fine-Tune — one rented A100, one hour, ~$2-4

Prove the PRISM Level-1 data: fine-tune Qwen3.8-27B to extract golds from
polytemporal context, then verify it on the SAME saved brains that the
headline run used.

## The one-box pipeline

| step | compute | time | cost |
|---|---|---|---|
| train (LoRA on bf16, 80GB A100) | GPU | ~10-20 min | ~$1-2 |
| merge adapter → bf16 | GPU RAM | ~5 min | (in hour) |
| requantize → GGUF Q4_K_M | CPU RAM (in-box) | ~10 min | (in hour) |
| **total** | | **~30-60 min** | **~$2-4** |

Train on full bf16 (no quantization during training — `quantization: none`),
requantize afterward. The 80GB A100 fits the 56GB bf16 base resident, so no
layer streaming needed and no merge-RAM wall.

## Why a rented box (not local)

- MI50 (gfx906): ROCm — Soup/Qwench layer streaming is CUDA-verified only.
- RTX 2080S (8GB/32GB Windows): 8GB too small for bf16 27B + can't merge
  (~60GB RAM needed, box has 32GB).
- Rented A100 80GB: everything in one box, one hour, ~$2-4. Your dual-Xeon
  can run the eval/requantize locally afterward if you prefer.

## Files

- `rent-finetune.sh` — train → merge → requantize → GGUF (run on the A100)
- `eval-finetune.py` — PRISM eval: fine-tune vs the 5 extraction-misses on
  the saved `final-context1` brains (serve the GGUF on :8080 first)

## Dataset

`../dataset/level1/train.jsonl` — 41 real records (context → gold), all
<1630 tokens (config `max_length: 2048` keeps every record). The 5
extraction-misses (Q16/18/28/30/42) are the discriminating set the eval
targets.

## The claim being tested

Retrieval is already perfect (50/50, recall 1.0). The fine-tune's job is
extraction: recover the golds the base model missed. **Recovery ≥ 4/5 on the
saved brains = PRISM-certified** (headline lifts from 0.90 toward 0.98).

## Growth path

41 records proves the pipeline. Expand with generated extractions from the
full harness (n=500 run) for the production fine-tune. The PEEP Level-1
schema makes the dataset a community-adoptable standard.