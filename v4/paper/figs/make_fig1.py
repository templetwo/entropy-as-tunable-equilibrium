#!/usr/bin/env python3
"""fig1_geometry: the two-chamber system with the horizon knob made visible.
Rollouts are genuine v43 harness trajectories (Geom + step_reflect + CFG),
seed derived in house style: first 8 bytes of SHA-256("fig1::geometry").
Vector PDF for the paper + PNG preview."""
import importlib.util, hashlib, os
import os
from pathlib import Path
HERE = Path(__file__).resolve().parent           # v4/paper/figs/
ROOT = Path(os.environ.get("ETE_ROOT", HERE.parents[2]))  # repo root
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Rectangle, Circle

HARNESS = str(ROOT / "v4/v43/v43_harness.py")
spec = importlib.util.spec_from_file_location("h", HARNESS)
h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)

b = h.CFG["box"]; e = h.CFG["entropy"]
geom = h.Geom(b["Lx"], b["Ly"], b["wall_t"], b["ch_w_default"])
LX, LY = b["Lx"], b["Ly"]
seed = int.from_bytes(hashlib.sha256(b"fig1::geometry").digest()[:8], "big")
rng = np.random.default_rng(seed)
start = np.array([LX * 0.25, LY * 0.5])
dtp = e["dt_path"]; sig = np.sqrt(2.0 * h.CFG["bath"]["D"] * dtp)

def rollouts(tau, M):
    n = max(6, int(round(tau / dtp)))
    pos = np.tile(start, (M, 1))
    path = np.empty((n + 1, M, 2)); path[0] = pos
    for k in range(n):
        noise = rng.standard_normal((M, 2)) * sig
        pos = h.step_reflect(geom, pos.copy(), 0.0, noise)
        path[k + 1] = pos
    return path

LONG = rollouts(2.0, 170)
SHORT = rollouts(0.25, 170)

# palette
BLUE, BLUE_D = "#1b4fa8", "#0f3d8c"
TEAL, TEAL_D = "#0e9488", "#086b62"
INK, PAPER, FRAME = "#2a2f36", "#f7f9fc", "#9aa3ad"

fig, ax = plt.subplots(figsize=(7.4, 4.05))
ax.set_xlim(-0.14, LX + 0.14); ax.set_ylim(-0.24, LY + 0.14)
ax.set_aspect("equal"); ax.axis("off")

# domain + entropy-bin lattice (h_ent = 0.2)
ax.add_patch(Rectangle((0, 0), LX, LY, fc=PAPER, ec="none", zorder=0))
for x in np.arange(0.2, LX, 0.2):
    ax.plot([x, x], [0, LY], color=BLUE, alpha=0.05, lw=0.4, zorder=1)
for y in np.arange(0.2, LY, 0.2):
    ax.plot([0, LX], [y, y], color=BLUE, alpha=0.05, lw=0.4, zorder=1)
ax.add_patch(Rectangle((0, 0), LX, LY, fc="none", ec=FRAME, lw=1.1, zorder=8))

# wall slabs with channel
ax.add_patch(Rectangle((geom.wx0, 0), geom.wx1 - geom.wx0, geom.cy0,
                       fc=INK, ec="#161a1f", lw=0.6, zorder=6))
ax.add_patch(Rectangle((geom.wx0, geom.cy1), geom.wx1 - geom.wx0, LY - geom.cy1,
                       fc=INK, ec="#161a1f", lw=0.6, zorder=6))
ax.text(0.5 * (geom.wx0 + geom.wx1), 1.62, "wall", rotation=90, ha="center",
        va="center", color="white", fontsize=7.2, zorder=7)

def fan(path, color, dark, lw, la, ea, es, z):
    segs = np.transpose(path, (1, 0, 2))
    ax.add_collection(LineCollection(segs, colors=color, lw=lw, alpha=la,
                                     capstyle="round", zorder=z))
    ax.scatter(path[-1, :, 0], path[-1, :, 1], s=es, c=dark, alpha=ea,
               lw=0.2, edgecolors="white", zorder=z + 1)

fan(LONG, BLUE, BLUE_D, 0.7, 0.10, 0.55, 5.5, 2)
fan(SHORT, TEAL, TEAL_D, 0.95, 0.20, 0.85, 7.0, 4)

# mouth gates (v4.1 MouthFlux band) and first-passage target
gy0, gy1 = geom.cy0 - 0.25, geom.cy1 + 0.25
for xg in (geom.wx0 - 0.15, geom.wx1 + 0.15):
    ax.plot([xg, xg], [gy0, gy1], color="#5a6470", lw=1.15, ls=(0, (1.4, 1.7)),
            zorder=7)
xt = geom.wx1 + 0.2
ax.plot([xt, xt], [0, LY], color="#37424e", lw=1.35, ls=(0, (5, 2.6)), zorder=7)

# start marker with halo
ax.add_patch(Circle(start, 0.085, fc="none", ec="#ff7a1a", lw=1.1, alpha=0.5,
                    zorder=9))
ax.add_patch(Circle(start, 0.135, fc="none", ec="#ff7a1a", lw=0.8, alpha=0.22,
                    zorder=9))
ax.add_patch(Circle(start, 0.045, fc="#ff7a1a", ec="white", lw=1.0, zorder=10))

# annotations — thin, sparse, leader lines
A = dict(fontsize=8.2, color="#333a42", zorder=11)
L = dict(color="#8a929c", lw=0.7, zorder=11)
ax.text(0.30, 1.80, r"$\tau = 0.25$", color=TEAL_D, fontsize=9.2,
        fontweight="bold", zorder=11)
ax.plot([0.62, 0.82], [1.76, 1.46], **L)
ax.text(3.12, 1.80, r"$\tau = 2.0$", color=BLUE_D, fontsize=9.2,
        fontweight="bold", zorder=11)
ax.plot([3.10, 2.86], [1.76, 1.44], **L)
ax.text(0.52, 0.62, "start", ha="right", **A)
ax.plot([0.55, 0.90], [0.66, 0.93], **L)
ax.text(2.0, -0.175, "mouth gates", ha="center", **A)
ax.plot([1.83, geom.wx0 - 0.15], [-0.10, 0.28], **L)
ax.plot([2.17, geom.wx1 + 0.15], [-0.10, 0.28], **L)
ax.text(xt + 0.07, 1.86, "first-passage target", rotation=90, va="top",
        fontsize=7.6, color="#37424e", zorder=11)
ax.text(3.62, 0.10, "endpoints " + r"$\to S_c$", ha="center", fontsize=7.6,
        color=BLUE_D, zorder=11)
ax.plot([3.50, 3.26], [0.20, 0.52], **L)

fig.tight_layout(pad=0.25)
out = str(HERE)
fig.savefig(os.path.join(out, "fig1_geometry.pdf"))
fig.savefig(os.path.join(out, "fig1_preview.png"), dpi=200)
print("seed:", seed)
print("long-fan endpoints past wall:",
      int((LONG[-1, :, 0] > geom.wx1).sum()), "/ 170")
print("short-fan max |r - start|: %.3f" %
      np.abs(SHORT[-1] - start).max())
