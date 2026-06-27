"""
sc2d_fast.py
============
Accelerated 2D causal-path-entropy field for Arms B/C.

The reference `run._sc_field_2d` triple-loops (seeds x gy x gx) and calls
`sc_endpoint` per grid point — correct but far too slow on CPU for the full
sweeps. This module evolves the walker ensembles for *all* grid points at once
as a single (G, n_paths, 2) array (G = ngx*ngy), so the inner time loop is a
handful of vectorized ops per step instead of thousands of Python calls. The
math is identical to the reference; only the executor changes.

This is the NumPy-fallback stand-in for the SPEC's JAX pipeline (JAX is not
installed on the MacBook seat; see RESULTS.md). float32 state keeps the big
ensembles cheap; endpoint entropy does not need float64.

`pl_for_tau` is a top-level, picklable worker so Arms B/C can fan the (geometry,
tau) grid across cores with multiprocessing.
"""
import numpy as np

D_DEFAULT = 1.0
DT_DEFAULT = 0.01


# --------------------------------------------------------------------------- #
# vectorized S_c field
# --------------------------------------------------------------------------- #
def sc_field_2d_fast(lc, gx, gy, n_sub, n_paths, seed, seeds=2, bins=30,
                     D=D_DEFAULT, dt=DT_DEFAULT, dtype=np.float32):
    """Causal path entropy S_c(x,y; tau=n_sub*dt) over the (gy, gx) grid.

    Evolves all G=ngx*ngy grid points' endpoint ensembles simultaneously under
    the NATURAL (uncontrolled) overdamped Langevin dynamics in U, then takes the
    Shannon entropy of each grid point's reachable endpoints. Averaged over
    `seeds` seeds for stability. Returns array shaped (len(gy), len(gx)).
    """
    X, Y = np.meshgrid(gx, gy)                      # (ny, nx)
    starts = np.stack([X.ravel(), Y.ravel()], -1).astype(dtype)   # (G, 2)
    G = starts.shape[0]
    rng_range = [[lc.xl, lc.xr], [lc.yl, lc.yr]]
    sd = np.float32(np.sqrt(2 * D * dt))
    # overdamped Langevin at fixed kT=1: gamma=1/D, so drift = -(1/gamma) grad_U
    # = -D grad_U, noise sqrt(2 D dt). (At D=1 this is identical to the reference;
    # the D factor only matters for the D-scaling diagnostic.)
    Ddt32 = np.float32(D * dt)
    field = np.zeros(G, dtype=np.float64)

    for s in range(seeds):
        rng = np.random.default_rng(seed + 131 * s)
        p = np.repeat(starts[:, None, :], n_paths, axis=1)         # (G, n_paths, 2)
        for _ in range(n_sub):
            g = lc.grad_U(p[..., 0], p[..., 1]).astype(dtype)      # g = grad_U
            p = p - Ddt32 * g + sd * rng.standard_normal(p.shape, dtype=dtype)
            p = lc.reflect(p).astype(dtype)
        # endpoint entropy per grid point
        for gi in range(G):
            field[gi] += _entropy2d(p[gi], bins, rng_range)
    return (field / seeds).reshape(len(gy), len(gx))


def _entropy2d(samples, bins, rng_range):
    h, _, _ = np.histogram2d(samples[:, 0], samples[:, 1], bins=bins, range=rng_range)
    pr = h / h.sum()
    pr = pr[pr > 0]
    return float(-np.sum(pr * np.log(pr)))


# --------------------------------------------------------------------------- #
# engine steady state -> P_L  (analytic shortcut; Arm A confirmed conservative)
# --------------------------------------------------------------------------- #
def pl_from_field(sc, X, cellA, contrast=3.0):
    """p_engine ∝ exp(beta*Tc*S_c) with beta*Tc fixed so the exponent spans
    `contrast` (matches the reference's 3.0/(max-min) normalization).
    Returns (P_L, p_engine)."""
    beta_Tc = contrast / (sc.max() - sc.min() + 1e-12)
    peng = np.exp(beta_Tc * (sc - sc.max()))
    peng /= peng.sum() * cellA
    PL = float(peng[X > 0.0].sum() * cellA)
    return PL, peng


def control_PL(lc, gx, gy):
    """Analytic thermal control P_L = mass fraction of exp(-U) in x>0."""
    X, Y = np.meshgrid(gx, gy)
    cellA = (gx[1] - gx[0]) * (gy[1] - gy[0])
    U = lc.U(X, Y)
    peq = np.exp(-(U - U.min()))
    peq /= peq.sum() * cellA
    return float(peq[X > 0.0].sum() * cellA)


def grid_for(lc, ngx, ngy):
    gx = np.linspace(lc.xl + 0.3, lc.xr - 0.3, ngx)
    gy = np.linspace(lc.yl + 0.3, lc.yr - 0.3, ngy)
    return gx, gy


# --------------------------------------------------------------------------- #
# picklable worker: one (geometry, tau) -> P_L(engine)
# --------------------------------------------------------------------------- #
def pl_for_tau(job):
    """job = dict(lc_kwargs, n_sub, n_paths, ngx, ngy, seed, seeds, bins, contrast).
    Builds the landscape, computes the S_c field at this tau, returns P_L(engine).
    Top-level so multiprocessing can pickle it."""
    from .landscape import ChamberChannel2D
    lc = ChamberChannel2D(**job["lc_kwargs"])
    gx, gy = grid_for(lc, job["ngx"], job["ngy"])
    X, _ = np.meshgrid(gx, gy)
    cellA = (gx[1] - gx[0]) * (gy[1] - gy[0])
    sc = sc_field_2d_fast(lc, gx, gy, job["n_sub"], job["n_paths"], job["seed"],
                          seeds=job.get("seeds", 2), bins=job.get("bins", 30),
                          D=job.get("D", D_DEFAULT))
    PL, _ = pl_from_field(sc, X, cellA, contrast=job.get("contrast", 3.0))
    return dict(L_ch=job["lc_kwargs"].get("L_ch"), tau=job["n_sub"] * DT_DEFAULT,
                n_sub=job["n_sub"], PL=PL, D=job.get("D", D_DEFAULT))
