#!/usr/bin/env python3
"""Lightweight animation prototype — explanatory only."""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

OUT = Path(__file__).resolve().parents[1] / "illustrations" / "nested_lobe_bridge_preview.mp4"


def frame_data(t: float):
    """t in [0, 1] storyboard progress."""
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.set_aspect("equal")
    ax.axis("off")
    th = np.linspace(0, 2 * math.pi, 128)
    if t < 0.25:
        r = 1.0 + 0.15 * np.sin(5 * th + 8 * t * math.pi)
        ax.plot(r * np.cos(th), r * np.sin(th), "k-", lw=1)
        ax.set_title("Wild packet winding")
    elif t < 0.5:
        stretch = 1.0 + 3.0 * max(0, (t - 0.25) / 0.25)
        ax.add_patch(plt.matplotlib.patches.Ellipse((0, 0), 2 * stretch, 0.4, fill=False, color="b"))
        ax.text(0, -1.2, "Eccentric REJECTED", ha="center", color="red", fontsize=12)
    elif t < 0.75:
        ax.plot(np.cos(th), np.sin(th), "b-", lw=2)
        ax.plot(0.45 * np.cos(th), 0.45 * np.sin(th), "c-", lw=2)
        ax.set_title("Annular normalize → reference")
    else:
        s = 0.6 + 0.2 * math.sin(6 * math.pi * (t - 0.75))
        pts = np.array([[0, s], [s, 0], [0, -s], [-s, 0], [0, s]])
        ax.plot(pts[:, 0], pts[:, 1], "g-", lw=2)
        ax.set_title("Rhombus → square (D=0)")
    return fig, ax


def main():
    fig, ax = plt.subplots(figsize=(6, 6))

    def update(i):
        ax.clear()
        ax.set_xlim(-1.6, 1.6)
        ax.set_ylim(-1.6, 1.6)
        ax.set_aspect("equal")
        ax.axis("off")
        t = i / 44
        th = np.linspace(0, 2 * math.pi, 128)
        if t < 0.25:
            r = 1.0 + 0.15 * np.sin(5 * th + 8 * t * math.pi)
            ax.plot(r * np.cos(th), r * np.sin(th), "k-", lw=1)
            ax.set_title("Wild packet winding")
        elif t < 0.5:
            stretch = 1.0 + 3.0 * max(0, (t - 0.25) / 0.25)
            ax.add_patch(plt.matplotlib.patches.Ellipse((0, 0), 2 * stretch, 0.4, fill=False, color="b"))
            ax.text(0, -1.2, "Eccentric REJECTED", ha="center", color="red", fontsize=12)
        elif t < 0.75:
            ax.plot(np.cos(th), np.sin(th), "b-", lw=2)
            ax.plot(0.45 * np.cos(th), 0.45 * np.sin(th), "c-", lw=2)
            ax.set_title("Annular normalize → reference")
        else:
            s = 0.6 + 0.2 * math.sin(6 * math.pi * (t - 0.75))
            pts = np.array([[0, s], [s, 0], [0, -s], [-s, 0], [0, s]])
            ax.plot(pts[:, 0], pts[:, 1], "g-", lw=2)
            ax.set_title("Rhombus → square (D=0)")

    ani = animation.FuncAnimation(fig, update, frames=45, interval=100)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    try:
        ani.save(str(OUT), writer="ffmpeg", fps=10, dpi=80)
    except Exception:
        gif = OUT.with_suffix(".gif")
        ani.save(str(gif), writer="pillow", fps=10, dpi=80)
    plt.close(fig)


if __name__ == "__main__":
    main()
