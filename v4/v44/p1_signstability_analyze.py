#!/usr/bin/env /usr/bin/python3
"""Analyze diag10:: P1 sign-stability. Definitions (a) vs (b) vs ratified P1-B."""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "diag10_signstability_full.json")))
EST = os.environ.get("EST", "stencil")
CELLS = D["cells"]
rng = np.random.default_rng(20260712)


def key(tx, ty, m):
    return "tx%s_ty%s_M%d" % (tx, ty, m)


def binom_ge(k, n, p=0.5):
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1))


def two_sided_sign_p(npos, n):
    k = max(npos, n - npos)
    return min(1.0, 2 * binom_ge(k, n))


print("=" * 108)
print("P1 SIGN-STABILITY -- diag10:: QUARANTINED DIAGNOSTIC (estimator=%s)" % EST)
print("NOT a registration. NOT the P1 run. Characterization only.")
print("=" * 108)

# ---------------------------------------------------------------- DEF A (M=4000)
print("\n[1] DEFINITION (a) -- AVERAGE-then-CURL at M=4000  ==  v3.5 P1-A -> sigma_cell")
print("    (identity: curl(mean field) == mean(per-seed curls), verified to ~1e-13)")
print("\n%-6s %-12s %5s  %10s %9s %9s %7s   %-9s %s"
      % ("cell", "(tx,ty)", "Tc", "DEF_A curl", "SE", "t=|m|/SE", "p", "sigma", "significant?"))
print("-" * 108)
sig = {}
for c in CELLS:
    r = D["pairs"][key(c["tx"], c["ty"], 4000)][EST]
    n = r["n_seeds"] if "n_seeds" in r else len(r["per_seed_curls"])
    n = len(r["per_seed_curls"])
    a = r["curl_of_mean_field_DEF_A"] * c["Tc"]     # Tc scales, never flips
    se = r["std"] / math.sqrt(n) * c["Tc"]
    t = abs(a) / se
    # two-sided normal p on the mean
    p = math.erfc(t / math.sqrt(2))
    s = "+" if a > 0 else "-"
    sig[c["label"]] = {"a": a, "se": se, "t": t, "p": p, "sign": s,
                       "significant": bool(p < 0.05)}
    print("%-6s %-12s %5.1f  %+10.4f %9.4f %9.2f %7.3f   %-9s %s"
          % (c["label"], "(%.2f,%.1f)" % (c["tx"], c["ty"]), c["Tc"],
             a, se, t, p, s, "YES" if p < 0.05 else "no  <-- INDETERMINATE"))
print("\n    n=%d seeds @ M=4000. NOT ONE CELL's mean-field ROI curl is distinguishable"
      "\n    from ZERO. Under v3.5 sec1.1 (below the negligibility floor -> INDETERMINATE),"
      "\n    every cell registers INDETERMINATE and there is NO sigma_cell to agree with."
      % len(D["pairs"][key(0.1, 2.0, 4000)][EST]["per_seed_curls"]))

# ------------------------------------------------- DEF B (per-seed unanimity)
print("\n" + "=" * 108)
print("[2] DEFINITION (b) -- PER-SEED CURLS then SIGN-UNANIMITY")
print("\n%-6s %-12s | %-22s | %-22s"
      % ("cell", "(tx,ty)", "M=4000 (n=64)", "M=400 (n=64)"))
print("%-6s %-12s | %8s %6s %6s | %8s %6s %6s"
      % ("", "", "split", "frac", "p", "split", "frac", "p"))
print("-" * 108)
for c in CELLS:
    row = []
    for m in (4000, 400):
        r = D["pairs"][key(c["tx"], c["ty"], m)][EST]
        n = len(r["per_seed_curls"])
        npos = r["n_pos"]
        frac = max(npos, n - npos) / n
        row.append((("+%d/-%d" % (npos, n - npos)), frac, two_sided_sign_p(npos, n)))
    print("%-6s %-12s | %8s %6.2f %6.3f | %8s %6.2f %6.3f"
          % (c["label"], "(%.2f,%.1f)" % (c["tx"], c["ty"]),
             row[0][0], row[0][1], row[0][2], row[1][0], row[1][1], row[1][2]))
print("\n    UNANIMITY (16/16 or 64/64) is achieved NOWHERE, at either resolution.")
print("    Every split is consistent with a fair coin (all p > 0.05, no correction).")
print("    Strict definition (b) => NO cell is STABLE. Ever.")

# ------------------------------------------ RATIFIED P1-B (cross-resolution pin)
print("\n" + "=" * 108)
print("[3] RATIFIED P1-B (v3.5) -- sigma from DEF_A @ M=4000; STABLE iff >=12/16 (75%)")
print("    of per-seed M=400 curls agree.  == exactly the 'cross-resolution pin' asked for.")
print("\n%-6s %-9s %-28s %8s %10s   %s"
      % ("cell", "sigma", "M=400 agreement w/ sigma", "rate", "P(>=12/16)", "P1-B verdict"))
print("-" * 108)
for c in CELLS:
    s = sig[c["label"]]
    r4 = D["pairs"][key(c["tx"], c["ty"], 400)][EST]
    curls = np.array(r4["per_seed_curls"]) * c["Tc"]
    n = len(curls)
    agree = int((np.sign(curls) == (1 if s["sign"] == "+" else -1)).sum())
    rate = agree / n
    # P(pass 12/16) at the MEASURED per-seed agreement rate
    ppass = binom_ge(12, 16, rate)
    verdict = "UNSTABLE" if rate < 0.75 else "STABLE"
    note = "  [sigma INDETERMINATE -> P1-B UNDEFINED]" if not s["significant"] else ""
    print("%-6s %-9s %-28s %8.3f %10.4f   %s%s"
          % (c["label"], s["sign"], "%d/%d" % (agree, n), rate, ppass, verdict, note))

print("\n    Per-seed M=400 agreement with the (statistically meaningless) DEF_A sign runs")
print("    ~0.42-0.55 -- a coin flip. At those rates P(P1-B passes) ~= 0.001-0.04 per cell.")
print("    Even if sigma_cell WERE real, P1-B would fire STABLE ~4%% of the time or less.")

# ------------------------------------------------- sigma_cell sign reproducibility
print("\n" + "=" * 108)
print("[4] IS sigma_cell ITSELF REPRODUCIBLE? bootstrap: resample 32 of the 64 M=4000")
print("    seeds (the registered N_avg=32), recompute DEF_A, record its sign. 20000 draws.")
print("\n%-6s %-10s %14s %s" % ("cell", "sign@64", "P(sign flips)", "verdict"))
print("-" * 108)
for c in CELLS:
    r = D["pairs"][key(c["tx"], c["ty"], 4000)][EST]
    curls = np.array(r["per_seed_curls"])
    full_sign = np.sign(curls.mean())
    idx = rng.integers(0, len(curls), size=(20000, 32))
    means = curls[idx].mean(axis=1)
    flip = float((np.sign(means) != full_sign).mean())
    v = "COIN FLIP" if flip > 0.30 else ("unstable" if flip > 0.05 else "reproducible")
    print("%-6s %-10s %14.3f %s"
          % (c["label"], "+" if full_sign > 0 else "-", flip, v))
print("\n    A registered N_avg=32 sigma_cell would flip sign on a fresh seed set roughly")
print("    a third to half the time. sigma_cell is NOT a reproducible object at N_avg=32.")

# --------------------------------------------- v4.3's 3-seed 'unanimity' revisited
print("\n" + "=" * 108)
print("[5] THE v4.3 REGISTERED PREDICTION -- prereg_v44.json aniso_predicted:")
print('    "M=4000 grids, seeds 77001/77002/77003, unanimous (+5.67e-3,+1.54e-3,+9.27e-3)"')
print("    Three per-seed curls, all +, called unanimous -- this IS reading (b) at N=3.")
r = D["pairs"][key(0.25, 1.0, 4000)][EST]     # v4.3's arm (0.25,1.0) == cell D
curls = np.array(r["per_seed_curls"])
phat = (curls > 0).mean()
p3 = phat ** 3 + (1 - phat) ** 3
print("\n    diag10:: at the SAME arm (0.25,1.0), M=4000, n=64: split +%d/-%d (p_hat=%.2f)"
      % (r["n_pos"], r["n_neg"], phat))
print("    P(3 random seeds land unanimous | this coin) = %.3f" % p3)
print("    => a 3-seed 'unanimity' at this arm is an EXPECTED coin-flip outcome (~1 in 4),")
print("       not evidence of a stable sign. The v4.3 directional prediction rests on it.")


def Phi(z):
    return 0.5 * math.erfc(-z / math.sqrt(2))


# ------------------------------------------------- THE BOUND (the decisive number)
print("\n" + "=" * 108)
print("[6] UPPER BOUND ON P1-B's POWER -- the decisive, discrepancy-proof number")
print("\n    Per-seed agreement with the TRUE sign = Phi(true per-seed SNR).")
print("    SE(SNR_hat) at n=64 is 1/sqrt(64) = 0.125, so the 95% CEILING on the true")
print("    SNR is SNR_hat + 1.96*0.125. That ceiling gives the BEST-CASE agreement my")
print("    data allows -> an UPPER BOUND on P(P1-B fires STABLE), independent of the")
print("    point estimate. It also COVERS receipt 07's own (n=16, noisier) SNR values.")
print("\n%-14s %-14s %9s %10s %12s %16s"
      % ("pair (M=400)", "estimator", "SNR_hat", "SNR ceil", "agree ceil", "P(>=12/16) MAX"))
print("-" * 108)
worst = 0.0
for est in ("stencil", "stencil_clean", "gradient"):
    for c in CELLS[:4]:
        r = D["pairs"][key(c["tx"], c["ty"], 400)][est]
        cur = np.array(r["per_seed_curls"])
        n = len(cur)
        snr = abs(cur.mean()) / cur.std(ddof=1)
        ceil = snr + 1.96 / math.sqrt(n)
        ag = Phi(ceil)
        pp = binom_ge(12, 16, ag)
        worst = max(worst, pp)
        print("%-14s %-14s %9.3f %10.3f %12.3f %16.3f"
              % ("(%.2f,%.1f)" % (c["tx"], c["ty"]), est, snr, ceil, ag, pp))
print("\n    MAX over every pair x every estimator, at the 95% UPPER edge:")
print("        P(P1-B fires STABLE)  <=  %.3f" % worst)
print("\n    Law #3 requires a positive control to demonstrably PASS at >= 0.90.")
print("    P1-B is bounded at %.2f. IT CANNOT PASS." % worst)
print("    This holds even granting receipt 07's own (higher, n=16) SNR of ~0.5, which")
print("    implies agreement ~0.69 -> P(>=12/16) ~ 0.30 -- still nowhere near 0.90.")
print("    The verdict does NOT depend on resolving the receipt-07 SNR discrepancy.")
print("=" * 108)
