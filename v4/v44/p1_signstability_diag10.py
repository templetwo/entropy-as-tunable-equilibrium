#!/usr/bin/env /usr/bin/python3
"""
P1 SIGN-STABILITY DIAGNOSTIC  --  namespace diag10::  (QUARANTINED, law #6)

NOT a registration. NOT the P1 precondition run. This is a characterization of
the BEHAVIOUR of the two candidate operational definitions of sign-stability,
run in a quarantined seed namespace that is disjoint from the registered
precond_P1:: sets (77001-77032 @ M=4000, 78001-78016 @ M=400). Nothing here
may be pooled into, or substituted for, the registered P1 run, which is
Anthony's gate alone.

Definitions implemented (decision-rule v3.5 sec 1.1, and the v3 OPEN ITEM):
  (a) AVERAGE-then-CURL : average N seeds' aniso mean fields, take the ROI
      mixed partial of the average -> ONE sign per cell. ("unanimity" is
      vacuous under this reading.)   == v3.5 P1-A (at M=4000, N_avg=32)
  (b) PER-SEED-CURL-then-UNANIMITY : per-seed ROI mixed partial, require sign
      unanimity (or a threshold fraction) across the seed set.
  (P1-B / cross-resolution pin) : sign registered by (a) at M=4000; STABLE iff
      >= 12/16 (75%) of per-seed M=400 curls agree with it. == v3.5 P1-B

Instrument fidelity: reproduces the scout's own per-block grid construction --
one RNG per block, tau_x grid drawn first, tau_y grid drawn SECOND from the
same stream (v44_scout.py simulate(), mode='frozen'). The aniso force field is
F = Tc * grad-pair of (S(tau_x), S(tau_y)); its curl is
    curl F = Tc * d2/dxdy [ S(tau_y) - S(tau_x) ].
We integrate that signed mixed partial over the ROI (receipt 07's statistic).

Tc > 0 scales the curl multiplicatively and CANNOT change its sign, so cells
A, AxT2, AxT4 share one sign, and only the four distinct (tau_x, tau_y) pairs
carry distinct grid work.
"""
import hashlib
import json
import math
import os
import sys
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v44_scout import CFG, Geom, frozen_grid  # noqa: E402

# ---------------------------------------------------------------- cells / ROI
CELLS = CFG["scout"]["cells"]                      # A B C D AxT2 AxT4
ROI = CFG["roi"]
BOX = CFG["box"]

# The four distinct (tau_x, tau_y) grid-pairs. Tc is sign-irrelevant.
PAIRS = sorted({(c["tx"], c["ty"]) for c in CELLS})


def diag_seed(pair, m_grid, k):
    """Quarantined diag10:: seed. Disjoint from precond_P1:: by namespace."""
    tag = "diag10::p1sign::tx%.4f::ty%.4f::M%d::s%d" % (pair[0], pair[1], m_grid, k)
    h = hashlib.sha256(tag.encode()).digest()
    return int.from_bytes(h[:8], "big")


def roi_curl_from_grids(Sx, Sy, xs, ys, estimator="stencil"):
    """Signed ROI-integrated mixed partial d2(S_y - S_x)/dx dy  (Tc = 1).

    This is curl F / Tc for the anisotropic causal-entropic force whose
    x-component is the gradient of S(.;tau_x) and y-component the gradient of
    S(.;tau_y) -- v44_scout.force_frozen_aniso.

    estimator="stencil": the 4-point 2h central-difference mixed partial the
      scout itself uses (v44_scout.py selftest, mixed_partial_mag), summed
      (unweighted) over the ROI. This is the instrument's own operator.
    estimator="gradient": np.gradient applied twice, area-weighted. Smoother
      (extra +/-1 averaging), retained as a robustness cross-check.

    BOTH are LINEAR in the field D, so for either one:
        curl( mean_over_seeds(field) )  ==  mean_over_seeds( curl(field) )
    exactly. This is definition (a) == the arithmetic mean of definition (b)'s
    per-seed curls -- an algebraic identity, not an empirical finding.
    """
    D = Sy - Sx                                    # (nx, ny)
    cx, cy = ROI["center"]
    hx_roi, hy_roi = ROI["half"]
    dx = xs[1] - xs[0]
    dy = ys[1] - ys[0]
    if estimator == "stencil":
        # scout's operator: centered on interior points xs[1:-1], ys[1:-1]
        mp = (D[2:, 2:] - D[2:, :-2] - D[:-2, 2:] + D[:-2, :-2]) / (4 * dx * dy)
        xc, yc = xs[1:-1], ys[1:-1]
        mx = (xc >= cx - hx_roi) & (xc <= cx + hx_roi)
        my = (yc >= cy - hy_roi) & (yc <= cy + hy_roi)
        return float(np.nansum(mp[np.ix_(mx, my)]))
    dDdx = np.gradient(D, xs, axis=0)
    d2 = np.gradient(dDdx, ys, axis=1)             # d2 D / dx dy
    mx = (xs >= cx - hx_roi) & (xs <= cx + hx_roi)
    my = (ys >= cy - hy_roi) & (ys <= cy + hy_roi)
    return float(d2[np.ix_(mx, my)].sum() * dx * dy)


def one_realization(args):
    """One seed, one (tau_x, tau_y) pair, one M_grid.

    Returns (curl, mean_field_x, mean_field_y) -- the per-seed curl AND the
    raw S grids, so definition (a) can average the FIELDS (not the curls).
    """
    pair, m_grid, k = args
    tx, ty = pair
    geom = Geom(BOX["Lx"], BOX["Ly"], BOX["wall_t"], BOX["ch_w_default"])
    rng = np.random.default_rng(diag_seed(pair, m_grid, k))
    # Instrument fidelity: tau_x grid FIRST, tau_y grid SECOND, one stream.
    Sx, xs, ys = frozen_grid(geom, tx, rng, M=m_grid)
    Sy, _, _ = frozen_grid(geom, ty, rng, M=m_grid)
    return (Sx, Sy, xs, ys)


EST = ("stencil", "gradient")


def run_pair(pair, m_grid, n_seeds, pool):
    jobs = [(pair, m_grid, k) for k in range(1, n_seeds + 1)]
    res = pool.map(one_realization, jobs)
    xs, ys = res[0][2], res[0][3]
    # definition (a): average the FIELDS, then curl the average
    Sx_bar = np.mean([r[0] for r in res], axis=0)
    Sy_bar = np.mean([r[1] for r in res], axis=0)
    out = {"n_seeds": n_seeds, "M_grid": m_grid}
    for est in EST:
        curls = np.array([roi_curl_from_grids(r[0], r[1], xs, ys, est) for r in res])
        com = roi_curl_from_grids(Sx_bar, Sy_bar, xs, ys, est)
        out[est] = {
            "per_seed_curls": curls.tolist(),
            "curl_of_mean_field_DEF_A": com,           # definition (a)
            "mean_of_per_seed_curls": float(curls.mean()),
            "identity_residual": float(abs(com - curls.mean())),
            "std": float(curls.std(ddof=1)),
            "snr": float(abs(curls.mean()) / curls.std(ddof=1)),
            "n_pos": int((curls > 0).sum()), "n_neg": int((curls < 0).sum())}
    return out


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    nproc = int(os.environ.get("NPROC", "12"))
    out = {"namespace": "diag10::", "mode": mode,
           "note": "QUARANTINED DIAGNOSTIC -- not a registration, not the P1 run",
           "pairs": {}, "cells": [dict(c) for c in CELLS]}

    if mode == "validate":
        # Receipt-07 reproduction: cells A(0.1,2.0) and C(0.1,1.0),
        # 16 seeds @ M=400 and 8 seeds @ M=4000. Statistical agreement with
        # the frozen receipt validates the method (seeds differ: diag10::).
        plan = [((0.1, 2.0), 400, 16), ((0.1, 1.0), 400, 16),
                ((0.1, 2.0), 4000, 8), ((0.1, 1.0), 4000, 8)]
    else:
        N = int(os.environ.get("NSEEDS", "64"))
        plan = [(p, 400, N) for p in PAIRS] + [(p, 4000, N) for p in PAIRS]

    with Pool(nproc) as pool:
        for pair, m, n in plan:
            key = "tx%s_ty%s_M%d" % (pair[0], pair[1], m)
            sys.stderr.write("[diag10] %s  n=%d ...\n" % (key, n))
            sys.stderr.flush()
            out["pairs"][key] = run_pair(pair, m, n, pool)
            for est in EST:
                r = out["pairs"][key][est]
                sys.stderr.write("    %-8s mean %+9.4f  std %8.4f  SNR %.3f  "
                                 "sign +%d/-%d  DEF_A %+9.4f  |a-mean|=%.2e\n"
                                 % (est, r["mean_of_per_seed_curls"], r["std"],
                                    r["snr"], r["n_pos"], r["n_neg"],
                                    r["curl_of_mean_field_DEF_A"],
                                    r["identity_residual"]))
            sys.stderr.flush()

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "diag10_signstability_%s.json" % mode)
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)
    print(path)


if __name__ == "__main__":
    main()
