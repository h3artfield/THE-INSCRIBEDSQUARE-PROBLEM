#!/usr/bin/env python3
"""Attachment signature surgery animation (Directive 025)."""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

OUT = Path(__file__).resolve().parents[1] / "illustrations" / "attachment_signature_preview.mp4"


def main():
    fig, ax = plt.subplots(figsize=(7, 7))

    def update(i):
        ax.clear()
        ax.set_xlim(-1.4, 1.4)
        ax.set_ylim(-1.4, 1.4)
        ax.set_aspect("equal")
        ax.axis("off")
        t = i / 44
        n = max(8, int(8 + 40 * t))
        th = np.linspace(0, 2 * math.pi, n + 1)
        pts = np.column_stack([np.cos(th), np.sin(th)])
        ax.plot(pts[:, 0], pts[:, 1], "k--", lw=0.8, alpha=0.4, label="retained")
        for k in range(n):
            ax.plot([pts[k, 0], pts[k + 1, 0]], [pts[k, 1], pts[k + 1, 1]], "r-", lw=1.2)
        ax.plot(pts[:, 0], pts[:, 1], "b-o", ms=3, lw=1.5)
        if t > 0.55:
            ax.text(0, -1.25, "SQUARE_MASS INSUFFICIENT", ha="center", color="red", fontsize=10)
        if t > 0.75:
            ax.text(0, 1.2, "ATTACHMENT SIGNATURE, NOT PACKET SIZE ALONE", ha="center", fontsize=9)
        ax.set_title("Tiny packets → attachment chain winding")

    ani = animation.FuncAnimation(fig, update, frames=45, interval=100)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    try:
        ani.save(str(OUT), writer="ffmpeg", fps=10, dpi=80)
    except Exception:
        ani.save(str(OUT.with_suffix(".gif")), writer="pillow", fps=10, dpi=80)
    plt.close(fig)


if __name__ == "__main__":
    main()
