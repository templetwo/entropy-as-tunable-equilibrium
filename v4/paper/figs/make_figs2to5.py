#!/usr/bin/env python3
"""Figs 2-5 drafted directly from the raw records, fig1 design language.
Annotated statistics are the verified machine outputs:
  v41_blocklevel_analysis.json (Table 1 of record), v41_analysis.json,
  v4_analysis.json (v4.0). No statistic in any label is computed here."""
import json
import os
from pathlib import Path
HERE = Path(__file__).resolve().parent           # v4/paper/figs/
ROOT = Path(os.environ.get("ETE_ROOT", HERE.parents[2]))  # repo root
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, BLUE_D = "#1b4fa8", "#0f3d8c"
TEAL = "#0e9488"
GRAY, INK, PAPER, FRAME = "#7a828c", "#2a2f36", "#f7f9fc", "#9aa3ad"
ORANGE = "#ff7a1a"
plt.rcParams.update({"font.size": 8.2, "axes.edgecolor": FRAME,
                     "axes.linewidth": 0.9, "xtick.color": "#4a525c",
                     "ytick.color": "#4a525c", "axes.labelcolor": "#333a42",
                     "text.color": "#333a42"})
RUN = str(ROOT / "v4/v41_run.ndjson")
recs = {}
with open(RUN) as f:
    for line in f:
        r = json.loads(line)
        recs[r["unit"]] = r["data"]

def fam(prefix, n=16):
    return [recs[f"{prefix}_sb{i}"] for i in range(n)]

def style_ax(ax):
    ax.set_facecolor(PAPER)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

# ================= fig2: fork (a) survival + occupancy insets ============
fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.35), sharey=True)
ANN = {  # v41_blocklevel_analysis.json, exact
    "0.25": dict(p=r"$p_{\mathrm{blk}} = 5.0\times10^{-4}$", g=r"$g = 1.72$",
                 occ=r"occ.\ $p_{\mathrm{blk}} = 5\times10^{-5}$, TV $0.022$"),
    "0.5":  dict(p=r"$p_{\mathrm{blk}} = 5.0\times10^{-5}$", g=r"$g = 1.87$",
                 occ=r"occ.\ $p_{\mathrm{blk}} = 5\times10^{-5}$, TV $0.017$"),
}
for ax, tau in zip(axes, ("0.25", "0.5")):
    style_ax(ax)
    for arm, col, cold in (("frozen", GRAY, "#565e68"), ("online", BLUE, BLUE_D)):
        units = fam(f"C1_{arm}_tau{tau}")
        pooled = np.sort(np.concatenate([u["fpt"]["times"] for u in units]))
        for u in units:
            t = np.sort(u["fpt"]["times"])
            ax.step(t, 1 - np.arange(1, len(t) + 1) / len(t), color=col,
                    lw=0.55, alpha=0.16, where="post")
        ax.step(pooled, 1 - np.arange(1, len(pooled) + 1) / len(pooled),
                color=cold, lw=1.9, where="post",
                label=arm + (" (slower)" if arm == "online" else ""))
    ax.set_xscale("log"); ax.set_xlim(0.15, 60); ax.set_ylim(0, 1.02)
    ax.set_xlabel("first-passage time")
    ax.set_title(rf"$\tau = {tau}$", fontsize=9.5, color=INK)
    ax.text(0.03, 0.16, ANN[tau]["p"] + "\n" + ANN[tau]["g"],
            transform=ax.transAxes, fontsize=8.2, color=BLUE_D, va="bottom")
    # occupancy inset
    ins = ax.inset_axes([0.56, 0.56, 0.42, 0.40])
    ins.set_facecolor("white")
    xs = (np.arange(24) + 0.5) * 4.0 / 24
    for arm, col, lw in (("frozen", "#565e68", 1.5), ("online", BLUE, 1.1)):
        occ = np.array([np.array(u["occupancy_x"], float)
                        / np.sum(u["occupancy_x"])
                        for u in fam(f"C1_{arm}_tau{tau}")]).mean(0)
        ins.plot(xs, occ, color=col, lw=lw)
    ins.set_xticks([]); ins.set_yticks([])
    ins.set_title("occupancy", fontsize=6.4, color="#4a525c", pad=1.5)
    ins.text(0.5, -0.16, ANN[tau]["occ"], transform=ins.transAxes,
             fontsize=5.9, ha="center", va="top", color="#4a525c")
axes[0].set_ylabel(r"survival  $P(T > t)$")
axes[0].legend(frameon=False, fontsize=7.6, loc="lower left",
               bbox_to_anchor=(0.0, 0.32))
fig.tight_layout(pad=0.4)
fig.savefig(str(HERE) + "/fig2_forka.pdf"); fig.savefig(str(HERE) + "/fig2_preview.png", dpi=170)
plt.close(fig)

# ================= fig3: p versus tau, three series =======================
fig, ax = plt.subplots(figsize=(4.5, 3.35)); style_ax(ax)
taus40 = [0.25, 0.5, 1.0, 2.0, 4.0]
p40 = [0.041, 0.0675, 0.8876, 0.6837, 0.5792]          # v4_analysis.json
taus41 = [0.25, 0.5, 1.0, 2.0]
p41_pool = [0.0005, 0.0005, 0.0605, 0.3458]             # v41_analysis.json
p41_blk = [0.0005, 5e-5, 0.06905, 0.44383]              # blocklevel (record)
ax.axhline(0.01, color=ORANGE, lw=1.0, ls=(0, (5, 3)), alpha=0.85)
ax.text(2.9, 0.0122, r"registered $\alpha = 0.01$", fontsize=7.2,
        color=ORANGE)
ax.axhline(5e-5, color="#5a6470", lw=0.9, ls=(0, (1.5, 2)), alpha=0.9)
ax.text(2.9, 6.1e-5, "permutation floor", fontsize=7.2, color="#5a6470")
ax.plot(taus40, p40, "s--", color=GRAY, mfc="white", ms=5.5, lw=1.0,
        label="v4.0 pooled (motivating)")
ax.plot(taus41, p41_pool, "o-", color=BLUE, mfc="white", ms=6, lw=1.1,
        label="v4.1 pooled (registered rule)")
ax.plot(taus41, p41_blk, "o-", color=BLUE_D, ms=6.5, lw=1.9,
        label="v4.1 block-level (of record)")
ax.set_yscale("log"); ax.set_xscale("log")
ax.set_xticks(taus40); ax.set_xticklabels([str(t) for t in taus40])
ax.set_ylim(2.5e-5, 1.6)
ax.set_xlabel(r"horizon $\tau$"); ax.set_ylabel("KS permutation $p$")
ax.legend(frameon=False, fontsize=7.3, loc="lower right")
fig.tight_layout(pad=0.4)
fig.savefig(str(HERE) + "/fig3_pvtau.pdf"); fig.savefig(str(HERE) + "/fig3_preview.png", dpi=170)
plt.close(fig)

# ================= fig4: gyrator | v4.0 flips | v4.1 mouth rates ==========
fig, (a, b, c) = plt.subplots(1, 3, figsize=(7.2, 2.75),
                              gridspec_kw={"width_ratios": [0.9, 1.0, 1.5]})
for ax in (a, b, c): style_ax(ax)
# A: gyrator per-block |ang_mom_rate|
hot = [abs(recs[f"C0_hot_sb{i}"]["ang_mom_rate"]) for i in range(4)]
ctl = [abs(recs[f"C0_ctrl_sb{i}"]["ang_mom_rate"]) for i in range(4)]
for x0, vals, col in ((0, ctl, GRAY), (1, hot, ORANGE)):
    a.scatter(np.full(4, x0) + np.linspace(-0.07, 0.07, 4), vals, s=22,
              c=col, zorder=3)
    a.hlines(np.mean(vals), x0 - 0.2, x0 + 0.2, color=col, lw=2)
a.set_yscale("log"); a.set_xticks([0, 1])
a.set_xticklabels(["equal $T$", "hot"]); a.set_xlim(-0.5, 1.5)
a.set_ylabel(r"$|\langle L\rangle|$ (block)")
a.text(0.5, 0.5, r"$12.8\times$", transform=a.transAxes, ha="center",
       fontsize=10, color=INK)
a.set_title("A  gyrator calibration", loc="left", fontsize=8.6, color=INK)
# B: v4.0 max-plaquette z, sign flips (v4_analysis.json C2 z_vs_frozen)
z40 = [-8.81, 6.86, 0.06, 0.18, 0.62]
b.axhspan(-3, 3, color=GRAY, alpha=0.14, lw=0)
b.axhline(0, color=FRAME, lw=0.8)
b.stem(range(5), z40, linefmt="-", basefmt=" ",
       markerfmt="o")
for art in b.lines: art.set_color(BLUE)
b.collections[0].set_color(BLUE) if b.collections else None
b.set_xticks(range(5)); b.set_xticklabels(["0.25", "0.5", "1", "2", "4"])
b.set_xlabel(r"$\tau$"); b.set_ylabel(r"registered $z$")
b.text(2.2, -6.5, r"$|z| \geq 3$ cleared," "\n" "signs flip", fontsize=7.4,
       color=BLUE_D)
b.set_title("B  v4.0 max-plaquette", loc="left", fontsize=8.6, color=INK)
# C: v4.1 block mouth loop rates, frozen vs online per tau
REG = {  # v41_analysis.json C2: registered z and sign consistency
    "0.25": ("+1.97", 9), "0.5": (r"$-$0.17", 8),
    "1.0": (r"$-$3.26", 9), "2.0": ("+0.60", 8)}
for k, tau in enumerate(["0.25", "0.5", "1.0", "2.0"]):
    fr = np.array([u["mouth"]["mouth_loop_rate"] for u in fam(f"C1_frozen_tau{tau}")])
    on = np.array([u["mouth"]["mouth_loop_rate"] for u in fam(f"C1_online_tau{tau}")])
    jf = np.linspace(-0.10, 0.10, 16)
    c.scatter(np.full(16, k - 0.16) + jf, fr * 1e4, s=9, c=GRAY, alpha=0.8)
    c.scatter(np.full(16, k + 0.16) + jf, on * 1e4, s=9, c=BLUE, alpha=0.8)
    z, sgn = REG[tau]
    c.annotate(rf"$z$ = {z}" + f"\nsign {sgn}/16",
               (k, 1.0), xytext=(k, 1.03), textcoords=("data", "axes fraction"),
               ha="center", fontsize=6.6, color="#4a525c",
               annotation_clip=False)
c.axhline(0, color=FRAME, lw=0.8)
c.set_xticks(range(4)); c.set_xticklabels(["0.25", "0.5", "1.0", "2.0"])
c.set_xlabel(r"$\tau$")
c.set_ylabel(r"mouth loop rate $\times 10^{4}$")
c.scatter([], [], s=9, c=GRAY, label="frozen"); c.scatter([], [], s=9, c=BLUE, label="online")
c.legend(frameon=False, fontsize=7, loc="lower left")
c.set_title("C  v4.1 block-level mouth loop rates", loc="left", fontsize=8.6,
            color=INK, pad=26)
fig.tight_layout(pad=0.4, w_pad=1.0)
fig.savefig(str(HERE) + "/fig4_forkb.pdf"); fig.savefig(str(HERE) + "/fig4_preview.png", dpi=170)
plt.close(fig)

# ================= fig5: Kramers, nominal vs effective ====================
Ls = [0.15, 0.3, 0.6, 1.2]
mfpt = {L: [np.mean(recs[f"C3t_frozen_L{L}_tau1.0_sb{i}"]["fpt"]["times"])
            for i in range(4)] for L in Ls}
fig, (l, r) = plt.subplots(1, 2, figsize=(4.6, 2.5), sharey=True)
for ax in (l, r): style_ax(ax)
def panel(ax, xs, slope, label, band=None, ci=None):
    means = np.array([np.mean(mfpt[L]) for L in Ls])
    X = np.array(xs)
    for x, L in zip(xs, Ls):
        ax.scatter([x] * 4, mfpt[L], s=12, c=BLUE, alpha=0.55, zorder=3)
    ax.scatter(X, means, s=26, c=BLUE_D, zorder=4)
    # line with the RECORD slope, anchored at the log-centroid of block means
    cx, cy = np.exp(np.mean(np.log(X))), np.exp(np.mean(np.log(means)))
    xx = np.array([min(X) * 0.85, max(X) * 1.18])
    ax.plot(xx, cy * (xx / cx) ** slope, color=INK, lw=1.3)
    if ci:
        ax.fill_between(xx, cy * (xx / cx) ** ci[0], cy * (xx / cx) ** ci[1],
                        color=BLUE, alpha=0.13, lw=0)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xticks(X); ax.set_xticklabels([str(x) for x in xs], fontsize=7)
    ax.minorticks_off()
    ax.set_xlabel(label, fontsize=8)
panel(l, Ls, 1.150, r"nominal $L$")
l.set_title(r"slope $1.15$ — registered fail", fontsize=8, color=INK,
            loc="left")
panel(r, [L + 0.2 for L in Ls], 1.729, r"effective $L + 0.2$",
      ci=(1.671, 1.798))
r.set_title(r"slope $1.729\;[1.671, 1.798]$", fontsize=8, color=INK,
            loc="left")
r.text(0.96, 0.06, r"$\in [1.7, 2.3]$" "\nexploratory", transform=r.transAxes,
       ha="right", fontsize=7, color=BLUE_D)
l.set_ylabel("transit MFPT")
fig.tight_layout(pad=0.4)
fig.savefig(str(HERE) + "/fig5_kramers.pdf"); fig.savefig(str(HERE) + "/fig5_preview.png", dpi=170)
plt.close(fig)
print("figs 2-5 written")
