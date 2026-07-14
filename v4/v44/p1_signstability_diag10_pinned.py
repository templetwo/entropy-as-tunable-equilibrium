#!/usr/bin/env /usr/bin/python3
"""
P1 SIGN-STABILITY DIAGNOSTIC — PINNED RE-RUN (blocker 5, Lane A mesh-20260713).

The 2026-07-12 P1 run imported the LIVE v44_scout.py mid-edit, with no sha
assert, and wrote a JSON aggregate (law #7 deviation). Its numbers were
therefore PROVISIONAL — not pinned to a known source. This runner is the
pinned supersession:

  * sha-asserts v44_scout.py (full sha256 + module SOURCE_SHA + config_hash)
    at import, in the parent AND every pool worker — one byte of drift and it
    refuses to run;
  * emits a raw NDJSON primary record (law #7): header with pins, one row per
    (pair, M_grid, estimator) carrying ALL per-seed curls, and per-cell P1-B
    agreement rows;
  * still writes the same-shape JSON aggregate so the existing
    p1_signstability_analyze.py continues to read it (the JSON is now the
    SECONDARY record; the NDJSON is primary);
  * uses the IDENTICAL quarantined diag10:: seed derivation — if the mid-edit
    import did not touch the physics, per-seed curls reproduce bit-exact; if
    they differ, the divergence is itself the finding.

NOT a registration. NOT the P1 precondition run (law #1: Anthony's gate).
Seed namespace diag10:: — quarantined, disjoint from precond_P1:: (law #6).
Interpreter: /usr/bin/python3 (3.9.6, numpy 2.0.2) — canonical.
"""
import hashlib
import json
import os
import sys
from multiprocessing import Pool

import numpy as np

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)
from v44_scout import CFG, Geom, frozen_grid  # noqa: E402
import v44_scout as VS                        # noqa: E402

# ---- the pin (blocker 5's missing piece) -----------------------------------
PIN_SHA256 = "1fe9fa1c9d203c508fbc4016a8e39e1a7dc055824a91e2935b1db9bfbfc0e35d"
PIN_CONFIG = "a344d6c47c8a22c1"
PIN_GIT    = "7a02eb5"

def _assert_pins():
    sha = hashlib.sha256(open(os.path.join(_DIR, "v44_scout.py"), "rb").read()).hexdigest()
    assert sha == PIN_SHA256, "v44_scout.py sha256 %s != pinned %s" % (sha, PIN_SHA256)
    assert VS.SOURCE_SHA == sha[:16], "module SOURCE_SHA mismatch"
    assert VS.config_hash() == PIN_CONFIG, "config_hash drift"

_assert_pins()   # import time: parent and every spawned worker

# ---- identical instrument + seeds as the unpinned run ----------------------
from p1_signstability_diag10 import (  # noqa: E402
    CELLS, PAIRS, EST, diag_seed, one_realization, run_pair)

P1B_THRESHOLD = 12   # v3.5 sec 1.1: STABLE iff >= 12/16 per-seed M=400 signs
P1B_OF        = 16   # agree with the sign registered by (a) at M=4000


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    nproc = int(os.environ.get("NPROC", "12"))
    N = int(os.environ.get("NSEEDS", "64"))
    ndjson_path = os.path.join(_DIR, "p1_signstability_%s_pinned.ndjson" % mode)
    json_path = os.path.join(_DIR, "diag10_signstability_%s_pinned.json" % mode)

    out = {"namespace": "diag10::", "mode": mode, "pinned": True,
           "note": "QUARANTINED DIAGNOSTIC -- not a registration, not the P1 run",
           "pin": {"v44_scout_sha256": PIN_SHA256, "source_sha": VS.SOURCE_SHA,
                   "config_hash": PIN_CONFIG, "git": PIN_GIT},
           "pairs": {}, "cells": [dict(c) for c in CELLS]}

    if mode == "validate":
        plan = [((0.1, 2.0), 400, 16), ((0.1, 1.0), 400, 16),
                ((0.1, 2.0), 4000, 8), ((0.1, 1.0), 4000, 8)]
    else:
        plan = [(p, 400, N) for p in PAIRS] + [(p, 4000, N) for p in PAIRS]

    fh = open(ndjson_path, "w")
    fh.write(json.dumps({
        "type": "header", "run": "p1_signstability_diag10_pinned", "mode": mode,
        "lane": "mesh-20260713 Lane A (fable 1/3) — blocker-5 pinned re-run",
        "pin": out["pin"], "interpreter": sys.version.split()[0],
        "numpy": np.__version__, "n_seeds": N, "nproc": nproc,
        "seed_namespace": "diag10:: (quarantined, law #6; identical derivation "
                          "to the 2026-07-12 unpinned run for bit-exact diff)",
        "p1b_rule": ">= %d/%d per-seed M=400 sign agreement with DEF-A M=4000 sign"
                    % (P1B_THRESHOLD, P1B_OF)}) + "\n")
    fh.flush()

    with Pool(nproc) as pool:
        for pair, m, n in plan:
            key = "tx%s_ty%s_M%d" % (pair[0], pair[1], m)
            sys.stderr.write("[diag10-pinned] %s  n=%d ...\n" % (key, n))
            sys.stderr.flush()
            out["pairs"][key] = run_pair(pair, m, n, pool)
            for est in EST:
                r = out["pairs"][key][est]
                fh.write(json.dumps({
                    "type": "pair", "pair_key": key, "tx": pair[0], "ty": pair[1],
                    "M_grid": m, "n_seeds": n, "estimator": est,
                    "per_seed_curls": r["per_seed_curls"],
                    "curl_of_mean_field_DEF_A": r["curl_of_mean_field_DEF_A"],
                    "mean_of_per_seed_curls": r["mean_of_per_seed_curls"],
                    "identity_residual": r["identity_residual"],
                    "std": r["std"], "snr": r["snr"],
                    "n_pos": r["n_pos"], "n_neg": r["n_neg"]}) + "\n")
            fh.flush()

    # ---- P1-B agreement per pair/estimator: sign from DEF-A @ M=4000 vs
    #      per-seed M=400 curls. The packet's headline check, now pinned. ----
    for pair in PAIRS:
        k400 = "tx%s_ty%s_M400" % (pair[0], pair[1])
        k4000 = "tx%s_ty%s_M4000" % (pair[0], pair[1])
        if k400 not in out["pairs"] or k4000 not in out["pairs"]:
            continue
        for est in EST:
            sigma = np.sign(out["pairs"][k4000][est]["curl_of_mean_field_DEF_A"])
            curls400 = np.array(out["pairs"][k400][est]["per_seed_curls"])
            agree = float(np.mean(np.sign(curls400) == sigma)) if sigma != 0 else float("nan")
            # windowed 16-seed subsets: how often would a 16-seed P1-B fire?
            n16 = len(curls400) // 16
            fires = [int((np.sign(curls400[i*16:(i+1)*16]) == sigma).sum() >= P1B_THRESHOLD)
                     for i in range(n16)] if sigma != 0 else []
            fh.write(json.dumps({
                "type": "p1b", "pair_key": k400, "estimator": est,
                "sigma_from_DEF_A_M4000": int(sigma),
                "per_seed_M400_agreement": round(agree, 4),
                "windows_16seed": len(fires),
                "windows_fired_STABLE": int(sum(fires)),
                "p_stable_windowed": round(sum(fires) / len(fires), 4) if fires else None
            }) + "\n")
    fh.flush()
    fh.close()

    with open(json_path, "w") as jh:
        json.dump(out, jh, indent=2)
    print(ndjson_path)
    print(json_path)


if __name__ == "__main__":
    main()
