#!/usr/bin/env /usr/bin/python3
"""DIAG 3 — map the attenuation factor R onto the DECISION.

R alone is not the deliverable. The deliverable is: after a x R haircut, does a
true (fine-grid) engine current still clear the scout's detection floor?

Arithmetic (all of it pinned to the harness's OWN floor formula, line 670):

    floor(B, sd) = (z_{1-alpha} + z_{power}) * sd * sqrt(2/B) = 3.858 * sd * sqrt(2/B)
                   [alpha_worst=0.005, power_target=0.90]

DIAG 1 (receipt 06) measured sd to be ~M-independent at scale 10 (SD ratio
M400/M2000: quad 1.19 [0.80,1.74], omega 0.87 [0.61,1.25] -- both consistent with 1).
So floor is ~M-independent, and ALL the M-dependence of detectability flows through
the SIGNAL attenuation R. Therefore:

    a true fine-grid current of size D is realized at M as R(M) * D
    it is detected when R(M) * D >= floor
    => minimum detectable TRUE current at M:   D_min(M) = floor / R(M)

M=400 therefore inflates the minimum detectable true current by the factor 1/R
relative to a perfect grid. That inflation -- not R -- is the safety number.
"""
import json, argparse
import numpy as np

Z = 3.858  # z_{0.995} + z_{0.90}, per decision-rule v3.5 sec.2 / harness line 670


def floor_of(sd, B):
    return Z * sd * np.sqrt(2.0 / B)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--analysis", required=True)
    ap.add_argument("--raw", required=True)
    ap.add_argument("--b-conf", type=int, default=96)
    ap.add_argument("--out")
    args = ap.parse_args()

    an = json.load(open(args.analysis))

    # block sd at M=400 (the registered M) from the k=0 cells -- the null arm,
    # which is what the scout's floor is actually computed from.
    rows = [json.loads(l) for l in open(args.raw) if l.strip()]
    sd400 = {}
    for stat in ("quad_loop_rate", "omega_roi"):
        v = [r[stat] for r in rows if r["M"] == 400 and r["kappa"] == 0.0]
        sd400[stat] = float(np.std(v, ddof=1))

    out = {"b_conf": args.b_conf, "sd_null_M400": sd400,
           "floor_formula": "3.858 * sd * sqrt(2/B)", "cells": {}}
    print(f"B_conf = {args.b_conf}\n")
    print(f"{'cell':26s} {'R':>16s} {'floor':>10s} {'Dmin@400':>10s} {'Dmin@fine':>10s} "
          f"{'inflation 1/R':>16s}")
    for key, r in an["results"].items():
        stat = r["stat"]
        sd = sd400[stat]
        fl = floor_of(sd, args.b_conf)
        R, seR = r["R"], r["se_R"]
        lo, hi = r["ci95"]
        # 1/R with CI: invert and swap the bounds
        infl, infl_lo, infl_hi = 1 / R, 1 / hi, 1 / lo
        out["cells"][key] = {
            "R": R, "R_ci95": [lo, hi], "sd_null_M400": sd, "floor": fl,
            "Dmin_M400": fl / R, "Dmin_fine_grid": fl,
            "inflation_1_over_R": infl, "inflation_ci95": [infl_lo, infl_hi],
            "attenuation_pct": 100 * (1 - R),
        }
        print(f"{key:26s} {R:6.3f}[{lo:.3f},{hi:.3f}] {fl:10.3e} {fl/R:10.3e} "
              f"{fl:10.3e} {infl:6.3f}[{infl_lo:.3f},{infl_hi:.3f}]")

    if args.out:
        json.dump(out, open(args.out, "w"), indent=1)
        print(f"\n# -> {args.out}")


if __name__ == "__main__":
    main()
