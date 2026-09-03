#!/usr/bin/env python3
"""Design summary figure — the polytemporal representation in one glance.

Left-to-right flow: every event carries a typed time_vector
(wall, mono, tau, fuzz); encoding is gated by salience at write-time;
decay/consolidation/recall operate on dT (tau), not wall-clock;
anchor constellations replace flat chronologies as the primary index.

Pure matplotlib (Agg), no TikZ. Outputs design_summary.pdf in figs/.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(__file__).resolve().parent / "design_summary.pdf"

fig, ax = plt.subplots(figsize=(7.2, 2.6), dpi=200)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")


def box(x, y, w, h, title, body, fc, ec="0.25"):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.5",
                       fc=fc, ec=ec, lw=1.2)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h - 9, title, ha="center", va="center",
            fontsize=9.5, fontweight="bold", color="0.1")
    ax.text(x + w / 2, y + h - 22, body, ha="center", va="center",
            fontsize=7.6, color="0.15")


def arrow(x1, y1, x2, y2):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                        mutation_scale=16, lw=1.6, color="0.3")
    ax.add_patch(a)


# 1. event carries time_vector
box(2, 55, 22, 40, "EVENT",
    "time_vector\n(wall, mono,\nτ, fuzz)", "#dbeafe")
# 2. salience gate at write-time
box(31, 55, 20, 40, "GATE (write-time)",
    "salience s =\nsurprise × goal\nset durability tier", "#dcfce7")
arrow(24.5, 75, 30, 75)
# 3. decay/consolidation/recall on Δτ
box(58, 55, 20, 40, "DECAY / RECALL",
    "Δτ drives decay,\nconsolidation,\nrecall (E1)", "#fef9c3")
arrow(51.5, 75, 57, 75)
# 4. anchor constellations
box(85, 55, 13, 40, "ANCHORS",
    "constellations\nreplace flat\nchronologies", "#fce7f3")
arrow(78.5, 75, 84, 75)

# bottom caption strip
ax.text(2, 12, "Events carry (wall, mono, τ, fuzz). Encoding is gated by salience at write-time.",
        fontsize=8, color="0.2")
ax.text(2, 2, "Decay, consolidation, and recall operate on Δτ, not wall-clock. Anchor constellations replace calendars.",
        fontsize=8, color="0.2")

fig.savefig(OUT, bbox_inches="tight")
print(f"wrote {OUT}")