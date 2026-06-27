"""
diagnostics.py
==============
Post-hoc diagnostic for the Arm C result. Arm C found tau* does NOT track the
channel length L_ch (flat-to-decreasing vs L_ch^2/D). The hypothesis: under the
analytic steady-state shortcut, the engine's P_L crossover is gated by the
large-chamber *self-exploration* time r_L^2/D (L_ch-independent), not by channel
traversal. This script tests whether tau* is a genuine *diffusive* timescale by
varying the diffusion constant D at fixed equilibrium (kT=1, so changing D=kT/gamma
via the friction gamma leaves p_eq ∝ exp(-U) — and the control P_L — untouched).

  Prediction if tau* is a diffusive timescale (r_eff^2/D):  tau* ∝ 1/D.
  A disguised constant reward toward the large chamber need not give tau* ∝ 1/D.

  python -m src.diagnostics --scan D
"""
import os, json, argparse
import numpy as np
import multiprocessing as mp

from .landscape import ChamberChannel2D
from . import sc2d_fast as fast
from . import run_fast as rf


def measure_with_D(lc_kwargs, nsubs, D, seed=0):
    lc = ChamberChannel2D(**lc_kwargs)
    gx, gy = fast.grid_for(lc, rf.NGX, rf.NGY)
    PL_ctrl = fast.control_PL(lc, gx, gy)   # depends on kT only -> D-invariant
    jobs = [dict(lc_kwargs=lc_kwargs, n_sub=int(ns), n_paths=rf.N_PATHS,
                 ngx=rf.NGX, ngy=rf.NGY, seed=seed, seeds=rf.SEEDS, bins=rf.BINS,
                 contrast=rf.CONTRAST, D=D) for ns in nsubs]
    nproc = max(1, min(mp.cpu_count() - 2, len(jobs)))
    with mp.Pool(nproc) as pool:
        res = pool.map(fast.pl_for_tau, jobs)
    res.sort(key=lambda r: r["n_sub"])
    taus = np.array([r["tau"] for r in res]); PL = np.array([r["PL"] for r in res])
    thresh = 0.5 * (PL_ctrl + PL.max())
    return dict(D=float(D), taus=taus, PL=PL, PL_control=PL_ctrl,
                tau_star=rf._first_crossing(taus, PL, thresh),
                tau_star_logistic=rf._logistic_midpoint(taus, PL))


def scan_D(D_list=(0.5, 0.7, 1.0, 1.4, 2.0), nsubs=None, seed=0):
    print("\n=== DIAGNOSTIC: tau* vs D  (fixed tuned landscape, L_ch=1.5) ===")
    print("    Prediction if tau* is diffusive (r_eff^2/D): tau* ∝ 1/D.")
    nsubs = rf._tau_grid(20, 1800, 14) if nsubs is None else np.asarray(nsubs)
    rows = []
    for D in D_list:
        r = measure_with_D({}, nsubs, D, seed)
        rows.append(dict(D=float(D), invD=1.0 / D, tau_star=r["tau_star"],
                         tau_star_logistic=r["tau_star_logistic"],
                         PL_control=r["PL_control"], PL=r["PL"].tolist(),
                         taus=r["taus"].tolist()))
        ts, tl = r["tau_star"], r["tau_star_logistic"]
        print(f"  D={D:4.2f}  1/D={1/D:4.2f}  tau*={ts}  tau*_logi={tl}"
              f"  tau*·D={ (ts*D) if ts else None }  tau*_logi·D={ (tl*D) if tl else None }"
              f"  P_L_ctrl={r['PL_control']:.3f}")
    _fit_and_fig(rows)
    os.makedirs("results", exist_ok=True)
    np.savez("results/diag_Dscan.npz", rows=json.dumps(rows))
    print("    data -> results/diag_Dscan.npz")
    return rows


def _fit_and_fig(rows):
    for key in ("tau_star", "tau_star_logistic"):
        xs = np.array([r["invD"] for r in rows if r[key] is not None])
        ts = np.array([r[key] for r in rows if r[key] is not None])
        if len(xs) < 2:
            continue
        slope = float(np.sum(xs * ts) / np.sum(xs * xs))     # tau* = slope * (1/D)
        ss_res = np.sum((ts - slope * xs) ** 2); ss_tot = np.sum((ts - ts.mean()) ** 2)
        r2 = 1 - ss_res / (ss_tot + 1e-12)
        prod = [r[key] * r["D"] for r in rows if r[key] is not None]
        print(f"  [fit {key}] tau* = {slope:.3f}/D   R^2(through-origin in 1/D)={r2:.3f}"
              f"   tau*·D mean={np.mean(prod):.3f} std={np.std(prod):.3f} (const => ∝1/D)")
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6.6, 5.0))
    for key, c, m in [("tau_star", "#cc3a21", "o"), ("tau_star_logistic", "#1f6feb", "s")]:
        pts = [(r["invD"], r[key]) for r in rows if r[key] is not None]
        if not pts: continue
        xs, ts = np.array([p[0] for p in pts]), np.array([p[1] for p in pts])
        ax.plot(xs, ts, m, color=c, ms=9, label=key)
        slope = float(np.sum(xs * ts) / np.sum(xs * xs))
        xx = np.linspace(0, max(xs) * 1.05, 50)
        ax.plot(xx, slope * xx, color=c, lw=1.4, alpha=0.7, label=f"  fit: tau* = {slope:.2f}/D")
    ax.set_xlabel("1 / D"); ax.set_ylabel("tau*")
    ax.set_title("Diagnostic: tau* ∝ 1/D (diffusive timescale)\n"
                 "tau* is L_ch-independent (Arm C) but scales as 1/D — a diffusive geometric time")
    ax.legend(fontsize=8.5); plt.tight_layout()
    os.makedirs("figures", exist_ok=True)
    plt.savefig("figures/diag_Dscan.png", dpi=150, facecolor="white")
    print("    figure -> figures/diag_Dscan.png")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", choices=["D"], default="D")
    args = ap.parse_args()
    if args.scan == "D":
        scan_D()


if __name__ == "__main__":
    main()
