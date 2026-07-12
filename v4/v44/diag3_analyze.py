#!/usr/bin/env /usr/bin/python3
"""DIAG 3 analysis — attenuation factor R = increment@M_lo / increment@M_hi.

Increment is the CRN-PAIRED difference d_i = y_i(kappa) - y_i(0) at matched
(M, block). Bootstrap resamples the paired-difference VECTORS (not raw y), so the
common-random-numbers correlation is preserved; resampling raw y independently
would discard it and OVERSTATE SE(R).

The two M arms are independent (distinct seeds / diverged RNG streams), so they are
resampled independently and R* = A*/B*.
"""
import json, sys, argparse
import numpy as np

STATS = ["quad_loop_rate", "omega_roi"]


def load(path):
    rows = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            rows[(r["M"], r["kappa"], r["block"])] = r
    return rows


def paired_diffs(rows, M, k, stat):
    """d_i = y_i(k) - y_i(0) over blocks present in BOTH kappa cells at this M."""
    blocks = sorted(b for (m, kk, b) in rows if m == M and kk == k
                    if (m, 0.0, b) in rows)
    d = np.array([rows[(M, k, b)][stat] - rows[(M, 0.0, b)][stat] for b in blocks])
    return d, blocks


def boot_ratio(dA, dB, n_boot, rng):
    """R = mean(dA)/mean(dB); independent resamples of the paired-diff vectors."""
    nA, nB = len(dA), len(dB)
    iA = rng.integers(0, nA, size=(n_boot, nA))
    iB = rng.integers(0, nB, size=(n_boot, nB))
    A = dA[iA].mean(axis=1)
    B = dB[iB].mean(axis=1)
    return A / B, A, B


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ndjson", required=True)
    ap.add_argument("--out")
    ap.add_argument("--m-lo", type=int, default=400)
    ap.add_argument("--m-hi", type=int, default=2000)
    ap.add_argument("--kappas", default="4.0,8.0")
    ap.add_argument("--n-boot", type=int, default=8000)
    ap.add_argument("--rng", type=int, default=999)
    args = ap.parse_args()

    rows = load(args.ndjson)
    rng = np.random.default_rng(args.rng)
    out = {"ndjson": args.ndjson, "n_boot": args.n_boot, "rng_seed": args.rng,
           "m_lo": args.m_lo, "m_hi": args.m_hi,
           "namespace": "diag10::", "pilot": True, "registers": None,
           "results": {}}

    for k in [float(x) for x in args.kappas.split(",")]:
        for stat in STATS:
            dA, bA = paired_diffs(rows, args.m_lo, k, stat)
            dB, bB = paired_diffs(rows, args.m_hi, k, stat)
            if len(dA) == 0 or len(dB) == 0:
                continue
            R, A, B = boot_ratio(dA, dB, args.n_boot, rng)
            mA, mB = dA.mean(), dB.mean()
            seA = dA.std(ddof=1) / np.sqrt(len(dA))
            seB = dB.std(ddof=1) / np.sqrt(len(dB))
            Rhat = mA / mB
            seR = R.std(ddof=1)
            lo, hi = np.percentile(R, [2.5, 97.5])
            # sigma-distance of R from 1.0 (no attenuation)
            sig = abs(1.0 - Rhat) / seR if seR > 0 else float("nan")
            # unpaired SE, for the record: how much CRN bought us
            yA_k = np.array([rows[(args.m_lo, k, b)][stat] for b in bA])
            yA_0 = np.array([rows[(args.m_lo, 0.0, b)][stat] for b in bA])
            se_unp = np.sqrt(yA_k.var(ddof=1) / len(yA_k) + yA_0.var(ddof=1) / len(yA_0))
            key = f"k{k:g}::{stat}"
            out["results"][key] = {
                "kappa": k, "stat": stat, "n_blocks": [len(dA), len(dB)],
                "incr_lo": float(mA), "se_lo": float(seA),
                "incr_hi": float(mB), "se_hi": float(seB),
                "R": float(Rhat), "se_R": float(seR),
                "ci95": [float(lo), float(hi)],
                "sigma_from_1": float(sig),
                "attenuation_pct": float(100 * (1 - Rhat)),
                "se_lo_unpaired": float(se_unp),
                "crn_variance_gain": float(se_unp / seA) if seA > 0 else None,
            }
            print(f"{key:28s} incr@{args.m_lo} {mA:+.4e} (se {seA:.2e}) | "
                  f"incr@{args.m_hi} {mB:+.4e} (se {seB:.2e}) | "
                  f"R {Rhat:.3f} [{lo:.3f},{hi:.3f}] ({sig:.1f}s) | "
                  f"CRN gain x{se_unp/seA:.2f}")

    if args.out:
        with open(args.out, "w") as f:
            json.dump(out, f, indent=1)
        print(f"# -> {args.out}")


if __name__ == "__main__":
    main()
