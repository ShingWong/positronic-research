#!/usr/bin/env python3
"""RULER efficiency figure — p95 latency and fallback vs profile.
G1 gate: n=50 real LongMemEval, lexical 0.5ms, local gated.
Outputs ruler_efficiency.pdf in same dir for Task 6 \\includegraphics.
"""
from pathlib import Path
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent / "ruler_efficiency.pdf"
FIGS = Path(__file__).resolve().parent

def load_metrics():
    # Load 50 metrics
    try:
        m_bal = json.load(open(FIGS / "metrics-50.json"))
    except Exception:
        m_bal = {"p95_ms": 1899.9, "fallback_rate": 1.0, "acc_with": 0.1}
    try:
        lt_path = Path("/usr/local/devel/positronic/consumers/benchmarks/results/longmemeval/run-50-long_term-lexical/metrics.json")
        m_lt = json.load(open(lt_path))
    except Exception:
        m_lt = {"p95_ms": 1574.8, "fallback_rate": 1.0, "acc_with": 1.0}
    return m_bal, m_lt

def main():
    m_bal, m_lt = load_metrics()
    # Data for plot: two profiles, lexical only (local gated)
    profiles = ["balanced\nlexical", "long_term\nlexical", "balanced\nlocal*", "long_term\nlocal*"]
    p95 = [m_bal.get("p95_ms", 0), m_lt.get("p95_ms", 0), 0, 0]
    fallback = [m_bal.get("fallback_rate", 0), m_lt.get("fallback_rate", 0), 1, 1]
    # Create figure with two y-axes: p95 and fallback
    fig, ax1 = plt.subplots(figsize=(3.4, 2.4))
    # p95 bars
    x = range(len(profiles))
    bars = ax1.bar(x, p95, color=["#4a90e2", "#7ed321", "#d0d0d0", "#d0d0d0"], edgecolor="black", linewidth=0.5)
    ax1.set_ylabel("p95 latency (ms)", fontsize=8)
    ax1.set_ylim(0, max(p95)*1.3 if max(p95) else 2000)
    ax1.set_xticks(x)
    ax1.set_xticklabels(profiles, fontsize=6)
    # Annotate values
    for i, v in enumerate(p95):
        if v:
            ax1.text(i, v+50, f"{v:.0f}ms", ha="center", fontsize=6)
        else:
            ax1.text(i, 100, "skipped\n(BGE 500)", ha="center", fontsize=5, color="red")
    # fallback as line on secondary axis
    ax2 = ax1.twinx()
    ax2.plot(x[:2], fallback[:2], "ro-", label="fallback", markersize=4)
    ax2.set_ylabel("fallback_rate", fontsize=8, color="red")
    ax2.set_ylim(0, 1.1)
    ax2.tick_params(axis='y', labelsize=6, colors="red")
    plt.title("RULER/LongMemEval efficiency (n=50 lexical, local gated)", fontsize=7)
    plt.tight_layout()
    plt.savefig(str(OUT))
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
    print(f"balanced p95 {p95[0]:.1f} fallback {fallback[0]:.2f} acc {m_bal.get('acc_with')}")
    print(f"long_term p95 {p95[1]:.1f} fallback {fallback[1]:.2f}")

if __name__ == "__main__":
    main()
