#!/usr/bin/env bash
# =====================================================================
# PRISM Level-1 Qwen3.8-27B fine-tune — one rented A100 box, one hour.
#
# Pipeline (single box, ~$2-4 total):
#   1. Train  : LoRA on FULL bf16 weights (80GB A100, no quant during train)
#   2. Merge  : adapter -> full-precision weights (in-box, GPU RAM)
#   3. Quant  : bf16 -> GGUF Q4_K_M (CPU-bound, llama-quantize, in-box RAM)
#   4. Output : qwen3.8-27b-prism-l1.Q4_K_M.gguf (~17GB) ready for llama.cpp
#
# Run from the rented box after installing dependencies. The 41-record
# Level-1 set trains in minutes; the hour budget covers train+merge+quant.
#
# Usage: bash rent-finetune.sh
# =====================================================================
set -euo pipefail

# ---- config -----------------------------------------------------------
MODEL="Qwen/Qwen3.8-27B"
DATASET="./dataset/level1/train.jsonl"        # 41 records, all <1630 tok
OUT_DIR="./output/prism-l1"
MAX_LEN=2048                                   # all records fit (max 1627)
LORA_R=64
LORA_ALPHA=16
EPOCHS=5
BATCH=2
LR=2e-4
GGUF_Q="Q4_K_M"                                # sweet spot for 24GB-class deploy

# ---- 0. environment ---------------------------------------------------
echo "== installing deps =="
pip install -q "soup-cli[train]" 2>/dev/null || pip install -q "qwench"
# llama.cpp for the requantize step
if ! command -v llama-quantize >/dev/null 2>&1; then
  echo "llama-quantize not found; building llama.cpp (few min)"
  git clone --depth 1 https://github.com/ggml-org/llama.cpp /tmp/llama.cpp
  cmake -S /tmp/llama.cpp -B /tmp/llama.cpp/build -DGGML_CUDA=OFF >/dev/null
  cmake --build /tmp/llama.cpp/build --config Release -j$(nproc) \
    --target llama-quantize >/dev/null
  export PATH="/tmp/llama.cpp/build/bin:$PATH"
fi

# ---- 1. train (LoRA on bf16, no quantization) --------------------------
echo "== training (LoRA bf16) =="
cat > soup.yaml <<YAML
base: ${MODEL}
task: sft
backend: transformers
data:
  train: ${DATASET}
  format: jsonl
  max_length: ${MAX_LEN}
  val_split: 0.1
training:
  epochs: ${EPOCHS}
  lr: ${LR}
  batch_size: ${BATCH}
  gradient_accumulation_steps: 2
  quantization: none            # bf16 base resident on 80GB; no quant during train
  gradient_checkpointing: true
  lora:
    r: ${LORA_R}
    alpha: ${LORA_ALPHA}
    dropout: 0.05
output: ${OUT_DIR}
YAML
soup train --config soup.yaml

# ---- 2. merge adapter -> full-precision weights -------------------------
echo "== merging adapter into bf16 =="
soup merge --config soup.yaml --output ${OUT_DIR}/merged

# ---- 3. requantize bf16 -> GGUF (CPU-bound, in-box RAM) -----------------
echo "== requantizing to GGUF ${GGUF_Q} =="
# llama.cpp needs an f16/b16 gguf from the HF safetensors; convert + quant
python3 - <<'EOF'
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
model = AutoModelForCausalLM.from_pretrained(
    "./output/prism-l1/merged", torch_dtype=torch.bfloat16, device_map="cpu")
model.save_pretrained("./output/prism-l1/gguf-staging")
tok = AutoTokenizer.from_pretrained("./output/prism-l1/merged")
tok.save_pretrained("./output/prism-l1/gguf-staging")
EOF
python3 /tmp/llama.cpp/convert_hf_to_gguf.py ./output/prism-l1/gguf-staging \
  --outfile ./output/prism-l1/qwen3.8-27b-prism-l1.f16.gguf --outtype f16
llama-quantize ./output/prism-l1/qwen3.8-27b-prism-l1.f16.gguf \
  ./output/prism-l1/qwen3.8-27b-prism-l1.${GGUF_Q}.gguf ${GGUF_Q}

# ---- 4. report ----------------------------------------------------------
echo ""
echo "== DONE =="
ls -lh ./output/prism-l1/*.gguf
echo ""
echo "Deploy target: MI50 box (or RTX 2080S) via llama.cpp / Ollama:"
echo "  llama-server -m qwen3.8-27b-prism-l1.${GGUF_Q}.gguf -c 32768"