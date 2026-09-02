# RunPod Quickstart — one-hour A100 fine-tune, one-man band

Deploy → train → download → delete. Total ~$2, no IAM, no roles, no policies.
~10 minutes of your time; the rest is scripted.

## 1. Pre-flight (local, before you spend anything)

```bash
# 41 records, all <1630 tokens — config max_length:2048 keeps every one
python3 -c "import json; r=[json.loads(l) for l in open('dataset/level1/train.jsonl')]; print(len(r), 'records')"

# syntax-check the scripts
bash -n experiments/finetune/rent-finetune.sh && echo "bash OK"
python3 -m py_compile experiments/finetune/eval-finetune.py && echo "py OK"
```

## 2. Create the RunPod account

- Sign up at runpod.io (email + credit card; **no IAM, no API keys to manage**).
- Set a **spending cap** (e.g. $10) so a forgotten pod can never run away.

## 3. Deploy the pod (5 min, web UI)

1. **Pods → Deploy**.
2. Search GPU: **NVIDIA A100 80GB**.
3. Tier: **Community Cloud** (cheapest, ~$1.20-1.39/hr; job is short + resumable so no-SLA is fine).
4. Template: **RunPod PyTorch** (2.1.0+ / CUDA 12.4) — CUDA + transformers pre-installed.
5. Volume: **none** (we ship data in, ship GGUF out — nothing persists).
6. **Deploy**, wait ~30-60s for pod to start.
7. Copy the **SSH command** (runs on the pod's shell).

## 4. Ship the data + script, run the pipeline (one command)

On your local box, `scp` the inputs to the pod, then run the fine-tune.
The script does install → train (bf16 LoRA) → merge → requantize → GGUF.

```bash
# local
POD_HOST=<the pod's SSH host from step 3>
scp -P <pod_port> dataset/level1/train.jsonl \
    experiments/finetune/rent-finetune.sh root@$POD_HOST:/workspace/
ssh -p <pod_port> root@$POD_HOST 'cd /workspace && DATASET=./train.jsonl OUT_DIR=./output bash rent-finetune.sh'
```

> The script's default paths assume it runs with `train.jsonl` beside it;
> if you put it elsewhere, set `DATASET`/`OUT_DIR` env vars (already handled
> above). Expect **~30-60 min** total: train ~10-20, merge ~5, quant ~10.

## 5. Pull the GGUF home, delete the pod

```bash
# local
scp -P <pod_port> root@$POD_HOST:/workspace/output/prism-l1/qwen3.8-27b-prism-l1.Q4_K_M.gguf ./

# web UI: Pods -> (your pod) -> Delete  ← do this immediately, billing stops
```

## 6. Verify (optional, your dual-Xeon tears through this locally)

Serve the GGUF on your local llama.cpp, point `eval-finetune.py` at it, run
against the saved `final-context1` brains:

```bash
# local, MI50 or dual-Xeon box
llama-server -m qwen3.8-27b-prism-l1.Q4_K_M.gguf -c 32768 -p 8080 &
PRISM_SERVE=http://127.0.0.1:8080/v1/chat/completions \
  python3 experiments/finetune/eval-finetune.py
# recovery >= 4/5 on Q16/18/28/30/42 = PRISM-certified (0.90 -> ~0.98)
```

## Cost math (honest)

| line | $ |
|---|---|
| A100 80GB Community, ~45 min @ ~$1.30/hr | ~$1.00 |
| storage/egress (GGUF ~17GB out) | ~$0.10 |
| idle minutes (forgot to delete) | avoid via spending cap |
| **total** | **~$1.10** |

## If RunPod Community is full / you want an SLA

Secure Cloud A100 is ~$1.49-1.79/hr — same script, just more per hour. Still
under $2 for the hour. The only difference is the tier dropdown in step 3.