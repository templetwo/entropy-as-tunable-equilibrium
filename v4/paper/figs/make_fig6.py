#!/usr/bin/env python3
"""fig6: (A) rotating sampling bias -> no mouth circulation (C4c records);
(B) the structural reason, drawn from the construction: the actual v4.1
estimator's scalar field S_c(r; tau=1.0) on an illustration grid (M=250,
seed = first 8 bytes of SHA-256("fig6::field")) with its gradient arrows.
Curl-free by construction; the panel is the argument."""
import importlib.util, hashlib, json
import os
from pathlib import Path
HERE = Path(__file__).resolve().parent           # v4/paper/figs/
ROOT = Path(os.environ.get("ETE_ROOT", HERE.parents[2]))  # repo root
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle

BLUE, BLUE_D = "#1b4fa8", "#0f3d8c"
GRAY, INK, PAPER, FRAME = "#7a828c", "#2a2f36", "#f7f9fc", "#9aa3ad"
ORANGE = "#ff7a1a"
plt.rcParams.update({"font.size": 8.2, "axes.edgecolor": FRAME,
                     "axes.linewidth": 0.9, "xtick.color": "#4a525c",
                     "ytick.color": "#4a525c", "axes.labelcolor": "#333a42",
                     "text.color": "#333a42"})

spec = importlib.util.spec_from_file_location(
    "h41", str(ROOT / "v4/v41_harness.py"))
h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)

recs = {}
with open(ROOT / "v4/v41_run.ndjson") as f:
    for line in f:
        r = json.loads(line)
        recs[r["unit"]] = r["data"]

fig, (a, bx) = plt.subplots(1, 2, figsize=(7.2, 3.0),
                            gridspec_kw={"width_ratios": [0.85, 1.35]})
for ax in (a, bx):
    ax.set_facecolor(PAPER)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

# ---- A: mouth loop rate under rotating sampling bias ----
groups = [("bias 0", [recs[f"C1_online_tau1.0_sb{i}"] for i in range(16)], GRAY),
          ("0.5", [recs[f"C4c_online_cb0.5_tau1.0_sb{i}"] for i in range(8)], BLUE),
          ("1.0", [recs[f"C4c_online_cb1.0_tau1.0_sb{i}"] for i in range(8)], BLUE_D)]
for k, (lab, us, col) in enumerate(groups):
    v = np.array([u["mouth"]["mouth_loop_rate"] for u in us]) * 1e4
    a.scatter(np.full(len(v), k) + np.linspace(-0.12, 0.12, len(v)), v,
              s=13, c=col, alpha=0.85, zorder=3)
    a.hlines(v.mean(), k - 0.24, k + 0.24, color=col, lw=2, zorder=4)
a.axhline(0, color=FRAME, lw=0.9)
a.set_xticks(range(3))
a.set_xticklabels(["bias $0$", "bias $0.5$", "bias $1.0$"])
a.set_ylabel(r"mouth loop rate $\times 10^{4}$")
a.set_title("A  rotating sampling bias: no circulation", loc="left",
            fontsize=8.6, color=INK)

# ---- B: the estimator's own scalar field + gradient arrows ----
b = h.CFG["box"]; e = h.CFG["entropy"]
geom = h.Geom(b["Lx"], b["Ly"], b["wall_t"], b["ch_w_default"])
e["M_grid"] = 250  # illustration grid, labeled
seed = int.from_bytes(hashlib.sha256(b"fig6::field").digest()[:8], "big")
rng = np.random.default_rng(seed)
S, xs, ys = h.frozen_grid(geom, 1.0, rng)
mask = np.zeros_like(S, bool)
for i, x in enumerate(xs):
    for j, y in enumerate(ys):
        mask[i, j] = geom.blocked(np.array([[x, y]]))[0]
Sm = np.ma.masked_array(S, mask)
cmap = LinearSegmentedColormap.from_list("house", ["#ffffff", "#dbe6f7",
                                                   "#7fa4dc", BLUE_D])
pm = bx.pcolormesh(xs, ys, Sm.T, cmap=cmap, shading="gouraud",
                   rasterized=True)
# wall slabs
bx.add_patch(Rectangle((geom.wx0, 0), geom.wx1 - geom.wx0, geom.cy0,
                       fc=INK, ec="none", zorder=5))
bx.add_patch(Rectangle((geom.wx0, geom.cy1), geom.wx1 - geom.wx0,
                       b["Ly"] - geom.cy1, fc=INK, ec="none", zorder=5))
# gradient arrows (F = Tc * grad S), downsampled
Fx, Fy = np.gradient(S, xs, ys)
step = 3
XX, YY = np.meshgrid(xs[1:-1:step], ys[1:-1:step], indexing="ij")
U = Fx[1:-1:step, 1:-1:step]; V = Fy[1:-1:step, 1:-1:step]
M2 = mask[1:-1:step, 1:-1:step]
U = np.ma.masked_array(U, M2); V = np.ma.masked_array(V, M2)
bx.quiver(XX, YY, U, V, color=INK, alpha=0.75, width=0.0035,
          scale=14, zorder=6)
bx.set_xlim(0, b["Lx"]); bx.set_ylim(0, b["Ly"]); bx.set_aspect("equal")
bx.set_xticks([]); bx.set_yticks([])
cb = fig.colorbar(pm, ax=bx, fraction=0.035, pad=0.015)
cb.set_label(r"$S_c(\mathbf{r};\,\tau{=}1.0)$", fontsize=7.5)
cb.ax.tick_params(labelsize=6.5)
cb.outline.set_edgecolor(FRAME)
bx.text(0.02, 0.04, r"$\mathbf{F} = T_c\,\widehat{\nabla} S$"
        + "\n" + r"$\nabla\times\langle\mathbf{F}\rangle = 0$ by construction",
        transform=bx.transAxes, fontsize=7.6, color=INK, zorder=7)
bx.text(0.98, 0.04, "illustration grid, $M{=}250$", transform=bx.transAxes,
        fontsize=6.4, ha="right", color="#4a525c", zorder=7)
bx.set_title("B  scalar field, gradient force", loc="left", fontsize=8.6,
             color=INK)
fig.tight_layout(pad=0.4, w_pad=1.2)
fig.savefig(str(HERE) + "/fig6_c4pipeline.pdf")
fig.savefig(str(HERE) + "/fig6_preview.png", dpi=170)
print("fig6 written, seed", seed)
