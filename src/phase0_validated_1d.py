"""
phase0_validated_1d.py
======================
The validated Phase 0 kernel. Reproduce this FIRST on the Studio before trusting
the 2D pipeline. It implements the causal-entropic-force mechanism on a 1D dumbbell
and regenerates the engine-vs-control 3D overlay figure.

Validated result (sandbox, recentered [-5, 5] axis):
  - engine != readout:        KL(p_engine || p_eq) ~ 0.75 - 1.16 across the sweep
  - horizon knob (Tc-free):   argmax(S_c) migrates  -3.7 -> 0  as tau grows
  - mass in option-rich well: 0.48 -> 0.67 monotonically (control fixed ~0.53)
  - recentering robustness:   result is invariant to where the origin is placed

NOTE: Phase 0 USES the conservative shortcut p_engine ∝ exp(beta*Tc*S_c).
      It does NOT verify it. Arm A verifies it. See SPEC.md §5.

Run:  python -m src.phase0_validated_1d
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.lines import Line2D

# ---- recentered dumbbell: ridge at 0, A(-2.5 deep+narrow), B(+2.5 wide+shallow) ----
A_CENTER, A_DEPTH, A_WIDTH = -2.5, 4.0, 0.5      # option-poor: deep narrow trap
B_CENTER, B_DEPTH, B_WIDTH = +2.5, 3.0, 1.5      # option-rich: wide shallow basin
XL, XR = -5.0, 5.0
KT, GAMMA, DT = 1.0, 1.0, 0.01
DDIFF = KT / GAMMA


def U(x):
    a = -A_DEPTH * np.exp(-((x - A_CENTER) ** 2) / (2 * A_WIDTH ** 2))
    b = -B_DEPTH * np.exp(-((x - B_CENTER) ** 2) / (2 * B_WIDTH ** 2))
    return a + b


def dU(x):
    a = -A_DEPTH * np.exp(-((x - A_CENTER) ** 2) / (2 * A_WIDTH ** 2)) * (-(x - A_CENTER) / A_WIDTH ** 2)
    b = -B_DEPTH * np.exp(-((x - B_CENTER) ** 2) / (2 * B_WIDTH ** 2)) * (-(x - B_CENTER) / B_WIDTH ** 2)
    return a + b


def _reflect(x):
    x = np.where(x < XL, 2 * XL - x, x)
    x = np.where(x > XR, 2 * XR - x, x)
    return np.clip(x, XL, XR)


def sc_endpoint(x0, n_sub, n_paths, seed, nbins=44):
    """Causal path entropy proxy: Shannon entropy of reachable endpoints after horizon
    tau = n_sub*dt, sampled under the NATURAL (uncontrolled) Langevin dynamics in U."""
    rng = np.random.default_rng(seed)
    x = np.full(n_paths, float(x0))
    sd = np.sqrt(2 * DDIFF * DT)
    for _ in range(n_sub):
        x = x - dU(x) / GAMMA * DT + sd * rng.standard_normal(n_paths)
        x = _reflect(x)
    hist, _ = np.histogram(x, bins=nbins, range=(XL, XR))
    p = hist / hist.sum()
    p = p[p > 0]
    return -np.sum(p * np.log(p))


def run(n_paths=1200, n_grid=46, n_tau=14, seeds=2):
    grid = np.linspace(XL + 0.3, XR - 0.3, n_grid)
    nsubs = np.unique(np.round(np.logspace(np.log10(8), np.log10(700), n_tau)).astype(int))
    taus = nsubs * DT

    Sc = np.zeros((len(nsubs), len(grid)))
    for i, ns in enumerate(nsubs):
        Sc[i] = np.mean(
            [[sc_endpoint(x0, ns, n_paths, seed=s * 131 + j) for j, x0 in enumerate(grid)]
             for s in range(seeds)],
            axis=0,
        )

    mid = len(nsubs) // 2
    beta_tc = 3.0 / (Sc[mid].max() - Sc[mid].min())
    P = np.exp(beta_tc * (Sc - Sc.max(axis=1, keepdims=True)))
    P = P / np.trapezoid(P, grid, axis=1)[:, None]

    peq = np.exp(-U(grid) / KT)
    peq /= np.trapezoid(peq, grid)
    Pc = np.tile(peq, (len(taus), 1))  # control extruded flat along tau

    # diagnostics
    def mass_B(p):
        m = grid > 0.0
        return float(np.trapezoid(p[m], grid[m]) / np.trapezoid(p, grid))

    def kl(p, q):
        p = p / np.trapezoid(p, grid); q = q / np.trapezoid(q, grid)
        m = p > 0
        return float(np.trapezoid(np.where(m, p * np.log(p / np.maximum(q, 1e-300)), 0.0), grid))

    argmax_engine = [round(float(grid[np.argmax(P[i])]), 2) for i in range(len(taus))]
    massB_engine = [round(mass_B(P[i]), 3) for i in range(len(taus))]
    kl_engine = [round(kl(P[i], peq), 3) for i in range(len(taus))]

    print("tau            :", [round(float(t), 2) for t in taus])
    print("argmax x       :", argmax_engine, "   (expect monotone climb -3.7 -> ~0)")
    print("mass in B (x>0):", massB_engine, "   (expect monotone 0.48 -> ~0.67)")
    print("KL(eng||eq)    :", kl_engine, "   (expect ~0.75 - 1.16, never ~0)")
    print("control argmax :", round(float(grid[np.argmax(peq)]), 2), "| control mass B:", round(mass_B(peq), 3))

    _figure(grid, taus, P, Pc, peq)
    return dict(grid=grid, taus=taus, P=P, peq=peq, Sc=Sc, beta_tc=beta_tc)


def _figure(grid, taus, P, Pc, peq):
    os.makedirs("figures", exist_ok=True)
    X, Tg = np.meshgrid(grid, taus)
    fig = plt.figure(figsize=(12.5, 8.8))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, Tg, Pc, color="#1f6feb", alpha=0.34, linewidth=0.15,
                    edgecolor="#0b3a78", rstride=1, cstride=2, antialiased=True)
    surf = ax.plot_surface(X, Tg, P, cmap=cm.magma, rstride=1, cstride=1, linewidth=0.2,
                           edgecolor="black", alpha=0.97, antialiased=True, vmin=0)
    ax.plot(grid[np.argmax(P, axis=1)], taus, P.max(axis=1), color="#ff2d2d", lw=2.4, zorder=10)
    ax.plot(grid[np.argmax(Pc, axis=1)], taus, Pc.max(axis=1), color="#00e5ff", lw=2.4, zorder=10)
    ax.set_xlabel("\nposition x   (A @ -2.5  |  ridge 0  |  B @ +2.5)")
    ax.set_ylabel("\nhorizon  tau")
    ax.set_zlabel("steady-state density")
    ax.set_title("Engine vs thermal control, overlaid in 3D:\n"
                 "control (blue) flat in tau — engine (magma) tilts and migrates toward well B")
    ax.view_init(elev=24, azim=-60)
    ax.set_box_aspect((1.4, 1.0, 0.72))
    legend = [
        Line2D([0], [0], color="#1f6feb", lw=8, alpha=0.5, label="thermal control (tau-invariant)"),
        Line2D([0], [0], color="#cc3a21", lw=8, label="engine (entropy-driven)"),
        Line2D([0], [0], color="#00e5ff", lw=2.4, label="control crest — pinned in well A"),
        Line2D([0], [0], color="#ff2d2d", lw=2.4, label="engine crest — slides A->ridge->B"),
    ]
    ax.legend(handles=legend, loc="upper left", fontsize=8.6, framealpha=0.9)
    fig.colorbar(surf, ax=ax, shrink=0.48, pad=0.07).set_label("engine density")
    plt.tight_layout()
    out = "figures/phase0_tau_overlay_3d.png"
    plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    print("figure ->", out)


if __name__ == "__main__":
    run()
