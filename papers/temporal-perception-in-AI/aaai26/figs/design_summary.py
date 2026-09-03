#!/usr/bin/env python3
"""Design summary figure — polytemporal representation + recall pipeline.

Lane 1 (encoding, top): every event carries a typed time_vector
(wall, mono, tau, fuzz); encoding is gated by salience at write-time;
decay/consolidation/recall operate on dT (tau), not wall-clock;
anchor constellations replace flat chronologies.
Lane 2 (recall, bottom): Activate -> Reconstruct -> Decay -> Fuse.

Pure matplotlib (Agg), no TikZ. Outputs design_summary.pdf in figs/.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(__file__).resolve().parent / "design_summary.pdf"

fig, ax = plt.subplots(figsize=(7.5, 3.4), dpi=200)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")


def box(x, y, w, h, title, body, fc, fs_title=9.5, fs_body=7.4):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.5",
                       fc=fc, ec="0.25", lw=1.2)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h - 8, title, ha="center", va="center",
            fontsize=fs_title, fontweight="bold", color="0.1")
    ax.text(x + w / 2, y + h - 20, body, ha="center", va="center",
            fontsize=fs_body, color="0.15")


def arrow(x1, y1, x2, y2):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                        mutation_scale=15, lw=1.5, color="0.3")
    ax.add_patch(a)


# ---- Lane 1: encoding (top) ----
box(2, 62, 21, 36, "EVENT",
    "time_vector\n(wall, mono,\nτ, fuzz)", "#dbeafe")
box(29, 62, 20, 36, "GATE (write-time)",
    "salience s =\nsurprise × goal\nset durability tier", "#dcfce7")
box(55, 62, 20, 36, "DECAY / CONSOLIDATE",
    "Δτ drives decay,\nconsolidation,\nrecall (E1)", "#fef9c3")
box(81, 62, 17, 36, "ANCHORS",
    "constellations\nreplace flat\nchronologies", "#fce7f3")
arrow(23.5, 80, 28.5, 80)
arrow(49.5, 80, 54.5, 80)
arrow(75.5, 80, 80.5, 80)

# ---- Lane 2: recall pipeline (bottom) ----
box(8, 12, 18, 30, "ACTIVATE",
    "spread over\nanchor\nconstellations", "#f5f3ff")
box(32, 12, 18, 30, "RECONSTRUCT",
    "schema-consistent\ncompletion,\ngraded confidence", "#f5f3ff")
box(56, 12, 18, 30, "DECAY",
    "rank by\nstrength ·\nexp(−Δτ/S)", "#f5f3ff")
box(80, 12, 18, 30, "FUSE",
    "merge schema\n+ episode\ndetails", "#f5f3ff")
arrow(26.5, 27, 31.5, 27)
arrow(50.5, 27, 55.5, 27)
arrow(74.5, 27, 79.5, 27)

# lane labels
ax.text(2, 101.5, "ENCODING", fontsize=8, fontweight="bold", color="0.35", va="bottom")
ax.text(8, 49, "RECALL:  Activate · Reconstruct · Decay · Fuse",
        fontsize=8, fontweight="bold", color="0.35", va="center")

fig.savefig(OUT, bbox_inches="tight")
print(f"wrote {OUT}")