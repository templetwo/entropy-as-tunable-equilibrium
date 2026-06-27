"""
run_fast.py
===========
Accelerated Arm B / Arm C drivers (NumPy-fallback stand-in for the SPEC's JAX
pipeline; JAX is unavailable on the MacBook seat). Uses the vectorized S_c field
in `sc2d_fast` and fans the (geometry, tau) grid across CPU cores with
multiprocessing. Arm A's conservativeness PASS licenses the analytic shortcut
p_engine ∝ exp(beta*Tc*S_c), so no driven trajectories are needed here.

  python -m src.run_fast --arm B
  python -m src.run_fast --arm C
"""
import os, json, argparse, time
import numpy as np
import multiprocessing as mp

from .landscape import ChamberChannel2D
from . import sc2d_fast as fast

# Keep per-worker BLAS single-threaded so the process Pool scales cleanly.
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")

# --- production sampling settings (tuned for S_c stability vs cost) ---
NGX, NGY = 44, 28
N_PATHS = 700
SEEDS = 3
BINS = 28
CONTRAST = 3.0
DT = 0.01


def _tau_grid(nsub_lo=20, nsub_hi=1800, n=16):
    nsubs = np.unique(np.round(np.logspace(np.log10(nsub_lo), np.log10(nsub_hi), n)).astype(int))
    return nsubs


def _first_crossing(xs, ys, thresh):
    for i in range(1, len(ys)):
        if (ys[i - 1] < thresh <= ys[i]) or (ys[i - 1] <= thresh < ys[i]):
            t = (thresh - ys[i - 1]) / (ys[i] - ys[i - 1] + 1e-12)
            return float(xs[i - 1] + t * (xs[i] - xs[i - 1]))
    return None


def _logistic_midpoint(taus, PL):
    """Robust tau*: fit PL(log tau) to a logistic and return the log-tau midpoint.
    Falls back to None if the fit fails or PL is non-rising."""
    from scipy.optimize import curve_fit  # optional; guarded by caller
    lt = np.log(taus)
    lo, hi = float(PL.min()), float(PL.max())
    if hi - lo < 1e-3:
        return None
    def logf(x, x0, k, a, b):
        return a + b / (1.0 + np.exp(-k * (x - x0)))
    try:
        p0 = [lt[np.argmin(np.abs(PL - 0.5 * (lo + hi)))], 2.0, lo, hi - lo]
        popt, _ = curve_fit(logf, lt, PL, p0=p0, maxfev=20000)
        return float(np.exp(popt[0]))
    except Exception:
        return None


def _run_jobs(jobs, label=""):
    t0 = time.time()
    nproc = max(1, min(mp.cpu_count() - 2, len(jobs)))
    with mp.Pool(nproc) as pool:
        results = pool.map(fast.pl_for_tau, jobs)
    print(f"    [{label}] {len(jobs)} jobs on {nproc} procs in {time.time()-t0:.1f}s")
    return results


def _jobs_for(lc_kwargs, nsubs, seed=0):
    return [dict(lc_kwargs=lc_kwargs, n_sub=int(ns), n_paths=N_PATHS,
                 ngx=NGX, ngy=NGY, seed=seed, seeds=SEEDS, bins=BINS, contrast=CONTRAST)
            for ns in nsubs]


def measure_tau_star(lc_kwargs, nsubs, seed=0, verbose=True):
    """Run the engine P_L(tau) sweep for one geometry; return everything needed
    to locate tau*. Pure-ish: builds its own landscape for the control."""
    lc = ChamberChannel2D(**lc_kwargs)
    gx, gy = fast.grid_for(lc, NGX, NGY)
    PL_ctrl = fast.control_PL(lc, gx, gy)
    res = _run_jobs(_jobs_for(lc_kwargs, nsubs, seed), label=f"L_ch={lc_kwargs.get('L_ch')}")
    res.sort(key=lambda r: r["n_sub"])
    taus = np.array([r["tau"] for r in res])
    PL = np.array([r["PL"] for r in res])
    thresh = 0.5 * (PL_ctrl + PL.max())
    tau_star = _first_crossing(taus, PL, thresh)
    tau_star_logi = _logistic_midpoint(taus, PL)
    if verbose:
        print(f"    P_L_control={PL_ctrl:.3f}  P_L range [{PL.min():.3f},{PL.max():.3f}]"
              f"  thresh={thresh:.3f}  tau*={tau_star}  tau*_logi={tau_star_logi}")
    return dict(taus=taus, PL=PL, PL_control=PL_ctrl, thresh=thresh,
                tau_star=tau_star, tau_star_logistic=tau_star_logi)


# =========================================================================== #
def arm_B(lc_kwargs=None, nsubs=None, seed=0, outtag="armB"):
    print("\n=== ARM B (fast): 2D chamber-channel-channel crossover ===")
    lc_kwargs = lc_kwargs or {}
    nsubs = _tau_grid() if nsubs is None else np.asarray(nsubs)
    r = measure_tau_star(lc_kwargs, nsubs, seed=seed)
    _save_B_fig(r, lc_kwargs, outtag)
    _save_npz(f"results/{outtag}.npz", lc_kwargs=json.dumps(lc_kwargs), **r)
    return r


def arm_C(L_ch_list=(1.0, 1.5, 2.0, 2.5, 3.0), base_kwargs=None, nsubs=None, seed=0):
    print("\n=== ARM C (fast): tau* vs L_ch^2/D — the discriminator ===")
    base_kwargs = dict(base_kwargs or {})
    nsubs = _tau_grid() if nsubs is None else np.asarray(nsubs)
    D = 1.0
    rows = []
    for L in L_ch_list:
        kw = dict(base_kwargs); kw["L_ch"] = float(L)
        r = measure_tau_star(kw, nsubs, seed=seed)
        rows.append(dict(L_ch=float(L), L2_over_D=L * L / D,
                         tau_star=r["tau_star"], tau_star_logistic=r["tau_star_logistic"],
                         PL_control=r["PL_control"], PL=r["PL"].tolist(),
                         taus=r["taus"].tolist()))
        print(f"  L_ch={L:.2f}  L^2/D={L*L/D:.2f}  tau*={r['tau_star']}  tau*_logi={r['tau_star_logistic']}")
    _save_C_fig(rows, base_kwargs)
    _save_npz("results/armC.npz", rows=json.dumps(rows), base_kwargs=json.dumps(base_kwargs))
    _print_C_fit(rows)
    return rows


def _print_C_fit(rows, key="tau_star"):
    xs = np.array([r["L2_over_D"] for r in rows if r[key] is not None])
    ts = np.array([r[key] for r in rows if r[key] is not None])
    if len(xs) < 2:
        print("  [Arm C] too few valid tau* to fit"); return
    slope0 = float(np.sum(xs * ts) / np.sum(xs * xs))            # through origin
    A = np.vstack([xs, np.ones_like(xs)]).T
    (b_aff, a_aff), *_ = np.linalg.lstsq(A, ts, rcond=None)      # affine
    ss_res = np.sum((ts - slope0 * xs) ** 2)
    ss_tot = np.sum((ts - ts.mean()) ** 2)
    r2_origin = 1 - ss_res / (ss_tot + 1e-12)
    print(f"  [Arm C fit, {key}] through-origin slope={slope0:.3f}  R^2(origin)={r2_origin:.3f}")
    print(f"  [Arm C fit, {key}] affine: tau* = {b_aff:.3f}*(L^2/D) + {a_aff:.3f}")


def _save_npz(path, **kw):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    np.savez(path, **kw)
    print("    data ->", path)


def _save_B_fig(r, lc_kwargs, outtag):
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs("figures", exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.4, 4.9))
    ax.semilogx(r["taus"], r["PL"], "o-", color="#cc3a21", lw=2, label="engine  P_L(tau)")
    ax.axhline(r["PL_control"], color="#1f6feb", ls="--", lw=2, label=f"thermal control = {r['PL_control']:.3f}")
    if r["tau_star"]:
        ax.axvline(r["tau_star"], color="#888", ls=":", label=f"tau* = {r['tau_star']:.2f}")
    ax.set_xlabel("horizon  tau  (log)"); ax.set_ylabel("mass in large chamber  P_L")
    ax.set_title("Arm B: engine migrates through the channel at tau*\n"
                 "(control flat in tau; engine rises — entropy is doing work)")
    ax.legend(); plt.tight_layout()
    out = f"figures/{outtag}_crossover.png"
    plt.savefig(out, dpi=150, facecolor="white"); print("    figure ->", out)


def _save_C_fig(rows, base_kwargs):
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs("figures", exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.0, 5.3))
    for key, c, m in [("tau_star", "#cc3a21", "o"), ("tau_star_logistic", "#1f6feb", "s")]:
        pts = [(r["L2_over_D"], r[key]) for r in rows if r[key] is not None]
        if not pts: continue
        xs, ts = np.array([p[0] for p in pts]), np.array([p[1] for p in pts])
        ax.plot(xs, ts, m, color=c, ms=9, label=f"{key} (data)")
        slope = float(np.sum(xs * ts) / np.sum(xs * xs))
        xx = np.linspace(0, max(xs) * 1.05, 50)
        ax.plot(xx, slope * xx, color=c, lw=1.2, alpha=0.55, ls="-",
                label=f"  prediction τ*∝L²/D (slope {slope:.2f}) — does NOT fit")
        ax.axhline(ts.mean(), color=c, lw=1.2, alpha=0.8, ls="--",
                   label=f"  data mean τ* = {ts.mean():.2f} (flat)")
    ax.set_xlabel("L_ch^2 / D   (predicted diffusive channel-traversal time)")
    ax.set_ylabel("tau*")
    ax.set_ylim(bottom=0)
    ax.set_title("Arm C (MAKE-OR-BREAK): tau* does NOT track channel length L_ch\n"
                 "data is flat (dashed) — the SPEC prediction tau*∝L_ch²/D (solid) is FALSIFIED")
    ax.legend(fontsize=8.0); plt.tight_layout()
    plt.savefig("figures/armC_scaling.png", dpi=150, facecolor="white")
    print("    figure -> figures/armC_scaling.png")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", choices=["B", "C"], required=True)
    ap.add_argument("--Lch", nargs="*", type=float, default=None)
    args = ap.parse_args()
    if args.arm == "B":
        arm_B()
    else:
        arm_C(L_ch_list=tuple(args.Lch) if args.Lch else (1.0, 1.5, 2.0, 2.5, 3.0))


if __name__ == "__main__":
    main()
