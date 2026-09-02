#!/usr/bin/env python3
"""E7 survival figure — true survival curves from the actual engine run.

Runs the E7 synthetic stream (55 msgs, 78 wks, weekly prune ladder per
retention profile) four times — archival / long_term / balanced / short_term —
and records per-week surviving level="event" episodes, so the figure shows the
real survival curves, not a canonical approximation.

G0 gate: archival 55, long_term 55, balanced 35, short_term 11 (current engine
v0.2.0, profile-driven ladder). Outputs e7_survival.pdf in same dir (figs/).
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, "/usr/local/devel/positronic/consumers/benchmarks")

OUT = Path(__file__).resolve().parent / "e7_survival.pdf"

def run_survival():
    from suites.synthetic_e7.driver import PROFILES, WEEKS, T0, _synthetic_events
    from harness.adapter import BenchmarkAdapter
    from harness.config import RunConfig

    events = _synthetic_events(n=55)
    weekly = [[] for _ in range(WEEKS)]
    for ev in events:
        w = int((ev["wall"] - T0).total_seconds() // (7 * 86400))
        w = max(0, min(WEEKS - 1, w))
        weekly[w].append(ev)

    curves: dict[str, list[int]] = {}
    finals: dict[str, int] = {}
    for prof in PROFILES:
        cfg = RunConfig(brain=f"e7_{prof}", profile=prof, embed="lexical",
                        tmp_root=OUT.parent / f"tmp-e7-{prof}", k=8)
        cfg.domain = f"e7_{prof}"
        adapter = BenchmarkAdapter(cfg)
        trace = [0] * WEEKS
        for w in range(WEEKS):
            for ev in weekly[w]:
                adapter.ingest([ev])
            tau_now = adapter.store.stream_time(adapter._stream)[0]
            adapter.prune(tau_now=tau_now)
            trace[w] = len(adapter.store.iter_episodes(level="event"))
        tau_now = adapter.store.stream_time(adapter._stream)[0]
        adapter.prune(tau_now=tau_now)
        curves[prof] = trace
        finals[prof] = len(adapter.store.iter_episodes(level="event"))
    return curves, finals

def main():
    curves, finals = run_survival()
    weeks = list(range(78))
    plt.figure(figsize=(3.3, 2.2))
    order = ["archival", "long_term", "balanced", "short_term"]
    for prof in order:
        plt.plot(weeks, curves[prof], label=prof)
    plt.xlabel("Weeks")
    plt.ylabel("Episodes alive")
    plt.ylim(0, 60)
    plt.xlim(0, 78)
    plt.legend(fontsize=6, loc="lower left", framealpha=0.9)
    plt.tight_layout()
    plt.savefig(str(OUT))
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
    print("finals:", " ".join(f"{p}={finals[p]}" for p in order))

if __name__ == "__main__":
    main()