"""
figures_armB.py
===============
SPEC §9 deliverable (b): 2D heatmaps of the causal path entropy field S_c(x,y;tau)
and the resulting engine steady state p_engine ∝ exp(beta*Tc*S_c) at representative
horizons (below / near / above tau*), for the tuned chamber-channel landscape.

  python -m src.figures_armB
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .landscape import ChamberChannel2D
from . import sc2d_fast as fast

DT = 0.01
TAUS = [0.5, 2.4, 7.3, 18.0]     # below, near, above tau* (Arm B tau* ~ 1.3-2.4)
NGX, NGY, N_PATHS, SEEDS, BINS = 60, 40, 600, 2, 30


def main():
    lc = ChamberChannel2D()
    gx, gy = fast.grid_for(lc, NGX, NGY)
    X, Y = np.meshgrid(gx, gy)
    cellA = (gx[1] - gx[0]) * (gy[1] - gy[0])
    extent = [gx[0], gx[-1], gy[0], gy[-1]]

    Sc_list, peng_list, PL_list = [], [], []
    for tau in TAUS:
        n_sub = int(round(tau / DT))
        sc = fast.sc_field_2d_fast(lc, gx, gy, n_sub, N_PATHS, seed=0, seeds=SEEDS, bins=BINS)
        PL, peng = fast.pl_from_field(sc, X, cellA)
        Sc_list.append(sc); peng_list.append(peng); PL_list.append(PL)
        print(f"  tau={tau:5.2f}  P_L(engine)={PL:.3f}")

    fig, axes = plt.subplots(2, len(TAUS), figsize=(4.0 * len(TAUS), 7.4))
    for j, tau in enumerate(TAUS):
        ax = axes[0, j]
        im = ax.imshow(Sc_list[j], origin="lower", extent=extent, aspect="auto", cmap="viridis")
        ax.set_title(f"S_c(x,y)   tau={tau:.2f}")
        ax.axvline(0, color="w", ls=":", lw=0.8)
        fig.colorbar(im, ax=ax, shrink=0.8)
        ax2 = axes[1, j]
        im2 = ax2.imshow(peng_list[j], origin="lower", extent=extent, aspect="auto", cmap="magma")
        ax2.set_title(f"p_engine   P_L={PL_list[j]:.2f}")
        ax2.axvline(0, color="w", ls=":", lw=0.8)
        fig.colorbar(im2, ax=ax2, shrink=0.8)
        for a in (ax, ax2):
            a.set_xlabel("x  (small @ -3.5 | channel @ 0 | large @ +3.5)")
            a.set_ylabel("y")
    fig.suptitle("Arm B: causal entropy field S_c (top) and engine steady state p_engine (bottom)\n"
                 "as the horizon grows, S_c peak and engine mass migrate through the channel into the large chamber",
                 fontsize=11)
    plt.tight_layout(rect=(0, 0, 1, 0.96))
    os.makedirs("figures", exist_ok=True)
    out = "figures/armB_heatmaps.png"
    plt.savefig(out, dpi=140, facecolor="white")
    print("figure ->", out)


if __name__ == "__main__":
    main()
