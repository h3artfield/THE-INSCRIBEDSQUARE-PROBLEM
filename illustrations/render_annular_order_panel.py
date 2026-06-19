#!/usr/bin/env python3
"""Ordered vs interleaving attachment chain panel (Directive 026)."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[1] / "illustrations" / "annular_order_panel.svg"


def main():
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    ax0, ax1 = axes
    for ax in axes:
        ax.set_aspect("equal")
        ax.axis("off")

    ax0.set_title("Valid ordered forest")
    ax0.plot([0, 2, 3], [0, 0, 1], "b-o", lw=2)
    ax0.text(1.5, -0.3, "signature → 0", ha="center", color="green")

    ax1.set_title("Invalid interleaving forest")
    ax1.plot([0, 2, 1, 3], [0, 0, 0, 0], "r-o", lw=2)
    ax1.plot([1, 1], [0, 1], "r--", lw=2)
    ax1.text(1.5, -0.3, "macroscopic σ", ha="center", color="red")

    fig.suptitle("ORDER, NOT SIZE ALONE, CONTROLS THE ATTACHMENT AREA", fontsize=11)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=120, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
