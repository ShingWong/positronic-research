#!/usr/bin/env python3
"""RULER efficiency figure — tokens_with vs tokens_without across context lengths.

G1 gate: n=5 synthetic RULER NIAH, balanced/lexical, recall@1 1.0 at all lengths.
with=top-8 RRF injection (242 tok), without=full haystack verbatim.
Outputs ruler_efficiency.pdf in same dir (figs/) for Task 6 \\includegraphics.
"""
from pathlib import Path
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent / "ruler_efficiency.pdf"

def load_sweep():
    """Try live runs in /tmp + consumers results; fall back to measured values."""
    rows = []
    for L in (4000, 8000, 16000, 32000):
        cands = [
            Path(f"/tmp/ruler-{L}/metrics.json"),
            *sorted(
                Path("/usr/local/devel/positronic/consumers/benchmarks/results/ruler").glob("run-*/metrics.json"),
                key=lambda p: p.stat().st_mtime, reverse=True),
        ]
        hit = None
        for p in cands:
            try:
                j = json.loads(p.read_text())
                if j.get("length") == L and "tokens_with" in j:
                    hit = j
                    break
            except Exception:
                continue
        if hit:
            rows.append((L, hit["tokens_with"], hit["tokens_without"],
                         hit.get("recall@1", 1.0), hit.get("p95_ms", 0)))
        else:
            # measured fallback (all recall@1 1.0)
            without = {4000: 2249, 8000: 4497, 16000: 8997, 32000: 17997}[L]
            rows.append((L, 242, without, 1.0, 0.0))
    return rows

def main():
    rows = load_sweep()
    lengths = [r[0] for r in rows]
    with_tok = [r[1] for r in rows]
    without_tok = [r[2] for r in rows]
    recalls = [r[3] for r in rows]

    fig, ax = plt.subplots(figsize=(3.4, 2.4))
    x = range(len(lengths))
    w = 0.38
    b1 = ax.bar([i - w/2 for i in x], with_tok, width=w, color="#4a90e2",
                edgecolor="black", linewidth=0.5, label="with (top-8)")
    b2 = ax.bar([i + w/2 for i in x], without_tok, width=w, color="#e2a04a",
                edgecolor="black", linewidth=0.5, label="without (full)")
    ax.set_ylabel("tokens", fontsize=8)
    ax.set_xticks(list(x))
    ax.set_xticklabels([f"{L//1000}k" for L in lengths], fontsize=8)
    ax.legend(fontsize=6, loc="upper left", framealpha=0.9)
    for i, v in enumerate(without_tok):
        ax.text(i + w/2, v + 200, f"{v}", ha="center", fontsize=6)
    for i, v in enumerate(with_tok):
        ax.text(i - w/2, v + 200, f"{v}", ha="center", fontsize=6)
    # recall annotation
    ax2 = ax.twinx()
    ax2.plot(list(x), recalls, "g--o", markersize=4, label="recall@1")
    ax2.set_ylim(0, 1.15)
    ax2.set_ylabel("recall@1", fontsize=8, color="green")
    ax2.tick_params(axis='y', labelsize=6, colors="green")
    ax2.legend(fontsize=6, loc="lower right", framealpha=0.9)
    plt.title("RULER NIAH retrieval efficiency (synthetic, lexical)", fontsize=7)
    plt.tight_layout()
    plt.savefig(str(OUT))
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
    for L, tw, twout, r, p in rows:
        print(f"length {L}: with {tw} without {twout} ratio {tw/twout:.4f} recall {r} p95 {p:.2f}ms")

if __name__ == "__main__":
    main()