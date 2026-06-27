"""
run.py
======
Orchestrates the experiment arms. See SPEC.md for the full specification.

  python -m src.run --arm A        # conservativeness check  (fully implemented, 1D)
  python -m src.run --arm B        # 2D crossover            (reference impl, validate + JAX on Studio)
  python -m src.run --arm C        # geometry-scaling test   (reference impl)

EXECUTOR NOTES:
  * Reproduce Phase 0 first:  python -m src.phase0_validated_1d
  * Arm A is runnable as-is and is the gate for the analytic shortcut.
  * Arms B/C ship as correct-but-slow NumPy references. Validate them by reproducing
    the Phase 0 logic in 2D (engine must avoid the deep chamber, control must not),
    THEN reimplement the S_c field with JAX (vmap/jit/scan) for the full sweeps.
  * Boot the Sovereign Stack, record insights as you go, handoff on completion.
"""
import argparse
import os
import numpy as np

from .landscape import Dumbbell1D, ChamberChannel2D
from . import causal_entropy as ce


# =========================================================================== #
# ARM A — conservativeness check (1D, fully implemented)
# =========================================================================== #
def arm_A(n_paths=2000, n_grid=80, tau_nsub=200, n_particles=4000, n_steps=20000, seed=0):
    print("\n=== ARM A: conservativeness check (1D dumbbell) ===")
    lc = Dumbbell1D()
    D, dt = 1.0, 0.01
    grid = np.linspace(lc.xl + 0.3, lc.xr - 0.3, n_grid)
    rng_range = (lc.xl, lc.xr)

    drift = lambda x: -lc.dU(x) / 1.0
    reflect = lc.reflect

    # 1) S_c field at a fixed tau
    sc = ce.sc_field_1d(grid, tau_nsub, n_paths, drift, reflect, D, dt, seed,
                        estimator=ce.sc_endpoint, seeds=2, rng_range=rng_range)
    beta_Tc = 3.0 / (sc.max() - sc.min())

    # 2) analytic steady state
    p_analytic = ce.analytic_steady_state(sc, grid, beta_Tc)

    # 3) force field F_ce = T_c grad S_c  (T_c folded via beta_Tc, kT=1 -> beta=1)
    F = ce.force_field_from_sc(sc, grid, T_c=beta_Tc)  # beta=1 so beta*Tc = Tc here
    force_interp = lambda x: np.interp(x, grid, F)

    # 4) drive particles under F_ce, histogram
    edges = np.linspace(lc.xl, lc.xr, 60)
    centers, p_driven = ce.driven_steady_state_1d(
        force_interp, reflect, D, dt, n_particles, n_steps,
        x_init=0.0, grid_edges=edges, seed=seed + 7)

    # 5) compare on a common grid
    p_an_on_centers = np.interp(centers, grid, p_analytic)
    p_an_on_centers /= np.trapezoid(p_an_on_centers, centers)
    p_driven /= np.trapezoid(p_driven, centers)
    kl = ce.kl_divergence(p_driven, p_an_on_centers, centers)
    overlap = float(np.trapezoid(np.minimum(p_driven, p_an_on_centers), centers))

    print(f"beta*T_c = {beta_Tc:.3f}")
    print(f"KL(driven || analytic) = {kl:.4f}   (small => conservative shortcut valid)")
    print(f"overlap coefficient    = {overlap:.4f}   (-> 1.0 => match)")
    verdict = "PASS: use analytic shortcut in Arms B/C" if (kl < 0.05 and overlap > 0.9) \
        else "INCONCLUSIVE/FAIL: inspect curl; fall back to driven trajectories (SPEC §5)"
    print("VERDICT:", verdict)

    _save_arm_A_fig(grid, sc, p_analytic, centers, p_driven)
    return dict(kl=kl, overlap=overlap, verdict=verdict)


def _save_arm_A_fig(grid, sc, p_analytic, centers, p_driven):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs("figures", exist_ok=True)
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
    ax[0].plot(grid, sc, color="#cc3a21"); ax[0].set_title("S_c(x) field"); ax[0].set_xlabel("x")
    ax[1].plot(grid, p_analytic, color="#1f6feb", lw=2, label="analytic  exp(beta Tc S_c)")
    ax[1].plot(centers, p_driven, color="#ff2d2d", lw=1.5, ls="--", label="driven (F_ce)")
    ax[1].set_title("Arm A: conservativeness check"); ax[1].set_xlabel("x"); ax[1].legend()
    plt.tight_layout(); plt.savefig("figures/armA_conservativeness.png", dpi=150, facecolor="white")
    print("figure -> figures/armA_conservativeness.png")


# =========================================================================== #
# ARM B — 2D chamber-channel-chamber crossover (reference impl)
# =========================================================================== #
def _sc_field_2d(lc2d, gx, gy, n_sub, n_paths, seed, seeds=2):
    """Reference (slow) 2D S_c field via endpoint entropy. JAX-accelerate on Studio."""
    drift = lambda p: -lc2d.grad_U(p[..., 0], p[..., 1])
    reflect = lc2d.reflect
    rng_range = [[lc2d.xl, lc2d.xr], [lc2d.yl, lc2d.yr]]
    D, dt = 1.0, 0.01
    field = np.zeros((len(gy), len(gx)))
    for s in range(seeds):
        rng = np.random.default_rng(seed + 131 * s)
        for iy, y0 in enumerate(gy):
            for ix, x0 in enumerate(gx):
                field[iy, ix] += ce.sc_endpoint(
                    np.array([x0, y0]), n_sub, n_paths, drift, reflect, D, dt, rng,
                    dim=2, bins=36, rng_range=rng_range)
    return field / seeds


def arm_B(tau_list=None, n_paths=600, ngx=48, ngy=32, seed=0):
    print("\n=== ARM B: 2D chamber-channel-chamber crossover (reference impl) ===")
    print("    NOTE: validate against Phase 0 logic, then JAX-accelerate. See SPEC §6.")
    lc = ChamberChannel2D()
    if tau_list is None:
        nsubs = np.unique(np.round(np.logspace(np.log10(10), np.log10(1200), 16)).astype(int))
        tau_list = nsubs * 0.01
    gx = np.linspace(lc.xl + 0.3, lc.xr - 0.3, ngx)
    gy = np.linspace(lc.yl + 0.3, lc.yr - 0.3, ngy)
    X, Y = np.meshgrid(gx, gy)
    cellA = (gx[1] - gx[0]) * (gy[1] - gy[0])

    # control: thermal, tau-invariant
    Ueq = lc.U(X, Y)
    peq = np.exp(-Ueq / 1.0); peq /= peq.sum() * cellA
    maskL = X > 0.0
    PL_control = float((peq[maskL].sum() * cellA))
    print(f"control P_L (mass in large chamber) = {PL_control:.3f}  (fixed, no tau)")

    # engine: P_L(tau)
    PL = []
    for tau, nsub in zip(tau_list, (tau_list / 0.01).astype(int)):
        sc = _sc_field_2d(lc, gx, gy, nsub, n_paths, seed)
        beta_Tc = 3.0 / (sc.max() - sc.min())
        peng = np.exp(beta_Tc * (sc - sc.max())); peng /= peng.sum() * cellA
        PL.append(float(peng[maskL].sum() * cellA))
        print(f"  tau={tau:6.2f}   P_L(engine)={PL[-1]:.3f}")
    PL = np.array(PL)

    # locate tau* : where P_L crosses halfway between control and its max
    thresh = 0.5 * (PL_control + PL.max())
    tau_star = _first_crossing(tau_list, PL, thresh)
    print(f"tau* (P_L crosses {thresh:.3f}) = {tau_star}")
    _save_arm_B_fig(tau_list, PL, PL_control, tau_star)
    return dict(tau=tau_list, PL=PL, PL_control=PL_control, tau_star=tau_star)


def _first_crossing(xs, ys, thresh):
    for i in range(1, len(ys)):
        if (ys[i - 1] < thresh <= ys[i]) or (ys[i - 1] <= thresh < ys[i]):
            # linear interp
            t = (thresh - ys[i - 1]) / (ys[i] - ys[i - 1] + 1e-12)
            return float(xs[i - 1] + t * (xs[i] - xs[i - 1]))
    return None


def _save_arm_B_fig(tau, PL, PL_control, tau_star):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs("figures", exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 4.8))
    ax.semilogx(tau, PL, "o-", color="#cc3a21", label="engine  P_L(tau)")
    ax.axhline(PL_control, color="#1f6feb", ls="--", label="thermal control (fixed)")
    if tau_star:
        ax.axvline(tau_star, color="#888", ls=":", label=f"tau* = {tau_star:.2f}")
    ax.set_xlabel("horizon tau (log)"); ax.set_ylabel("mass in large chamber  P_L")
    ax.set_title("Arm B: engine migrates through the channel at tau*"); ax.legend()
    plt.tight_layout(); plt.savefig("figures/armB_crossover.png", dpi=150, facecolor="white")
    print("figure -> figures/armB_crossover.png")


# =========================================================================== #
# ARM C — tau* tracks geometry (the discriminator)
# =========================================================================== #
def arm_C(L_ch_list=(1.0, 1.5, 2.0, 2.5, 3.0), seed=0):
    print("\n=== ARM C: tau* vs L_ch^2/D  (the make-or-break test) ===")
    print("    PREDICTION: tau* proportional to L_ch^2 / D. A disguised reward cannot.")
    D = 1.0
    tau_stars, xvals = [], []
    for L in L_ch_list:
        # rebuild Arm B with this channel length
        import copy
        res = _arm_B_with_Lch(L, seed=seed)
        tau_stars.append(res["tau_star"])
        xvals.append(L ** 2 / D)
        print(f"  L_ch={L:.2f}  L^2/D={L**2/D:.2f}  ->  tau*={res['tau_star']}")
    _save_arm_C_fig(np.array(xvals), tau_stars, L_ch_list)
    return dict(L_ch=list(L_ch_list), L2_over_D=xvals, tau_star=tau_stars)


def _arm_B_with_Lch(L_ch, seed=0):
    # thin wrapper: Arm B with an overridden channel length
    from .landscape import ChamberChannel2D
    lc = ChamberChannel2D(L_ch=L_ch)
    globals()  # (kept simple; the executor may refactor arm_B to accept a landscape)
    # reuse arm_B body by monkeypatching default landscape would be ugly; instead inline:
    return _arm_B_core(lc, seed=seed)


def _arm_B_core(lc, n_paths=600, ngx=48, ngy=32, seed=0):
    nsubs = np.unique(np.round(np.logspace(np.log10(10), np.log10(1500), 16)).astype(int))
    tau_list = nsubs * 0.01
    gx = np.linspace(lc.xl + 0.3, lc.xr - 0.3, ngx)
    gy = np.linspace(lc.yl + 0.3, lc.yr - 0.3, ngy)
    X, Y = np.meshgrid(gx, gy)
    cellA = (gx[1] - gx[0]) * (gy[1] - gy[0])
    Ueq = lc.U(X, Y); peq = np.exp(-Ueq); peq /= peq.sum() * cellA
    maskL = X > 0.0
    PL_control = float(peq[maskL].sum() * cellA)
    PL = []
    for nsub in (tau_list / 0.01).astype(int):
        sc = _sc_field_2d(lc, gx, gy, nsub, n_paths, seed)
        beta_Tc = 3.0 / (sc.max() - sc.min())
        peng = np.exp(beta_Tc * (sc - sc.max())); peng /= peng.sum() * cellA
        PL.append(float(peng[maskL].sum() * cellA))
    PL = np.array(PL)
    thresh = 0.5 * (PL_control + PL.max())
    return dict(tau=tau_list, PL=PL, PL_control=PL_control, tau_star=_first_crossing(tau_list, PL, thresh))


def _save_arm_C_fig(xvals, tau_stars, L_ch_list):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs("figures", exist_ok=True)
    valid = [(x, t) for x, t in zip(xvals, tau_stars) if t is not None]
    fig, ax = plt.subplots(figsize=(6.5, 5))
    if valid:
        xs, ts = zip(*valid)
        ax.plot(xs, ts, "o", color="#cc3a21", ms=9)
        # least-squares through origin
        xs, ts = np.array(xs), np.array(ts)
        slope = float(np.sum(xs * ts) / np.sum(xs * xs))
        xx = np.linspace(0, max(xs) * 1.05, 50)
        ax.plot(xx, slope * xx, color="#1f6feb", label=f"tau* = {slope:.2f} * L_ch^2/D")
    ax.set_xlabel("L_ch^2 / D  (diffusive traversal time)")
    ax.set_ylabel("tau*")
    ax.set_title("Arm C: tau* tracks channel geometry\n(linear-through-origin => engine, not disguised reward)")
    ax.legend()
    plt.tight_layout(); plt.savefig("figures/armC_scaling.png", dpi=150, facecolor="white")
    print("figure -> figures/armC_scaling.png")


# =========================================================================== #
def main():
    ap = argparse.ArgumentParser(description="Entropy-as-Engine experiment arms")
    ap.add_argument("--arm", choices=["A", "B", "C"], required=True)
    ap.add_argument("--Lch", nargs="*", type=float, default=None,
                    help="Arm C: channel lengths to sweep")
    args = ap.parse_args()
    if args.arm == "A":
        arm_A()
    elif args.arm == "B":
        arm_B()
    elif args.arm == "C":
        arm_C(L_ch_list=tuple(args.Lch) if args.Lch else (1.0, 1.5, 2.0, 2.5, 3.0))


if __name__ == "__main__":
    main()
