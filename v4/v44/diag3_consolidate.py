#!/usr/bin/env /usr/bin/python3
"""Consolidate DIAG 3 into one analysis JSON (the deliverable)."""
import json, hashlib, os, subprocess
import numpy as np
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diag3_analyze import load, paired_diffs, boot_ratio

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "/private/tmp/claude-501/-Users-tony-studio/4c29e945-7fc9-485d-b74d-58d800127f95/scratchpad/entwt-v44/v4/v44"
STATS = ["quad_loop_rate", "omega_roi"]
Z = 3.858
NB, RSEED = 8000, 999


def comp(rows, Mlo, Mhi, k, rng):
    o = {}
    for stat in STATS:
        dA, _ = paired_diffs(rows, Mlo, k, stat)
        dB, _ = paired_diffs(rows, Mhi, k, stat)
        if not len(dA) or not len(dB):
            continue
        R, A, B = boot_ratio(dA, dB, NB, rng)
        Rh = dA.mean() / dB.mean()
        lo, hi = [float(x) for x in np.percentile(R, [2.5, 97.5])]
        o[stat] = {
            "n_blocks": [len(dA), len(dB)],
            "incr_lo": float(dA.mean()), "se_lo": float(dA.std(ddof=1)/np.sqrt(len(dA))),
            "incr_hi": float(dB.mean()), "se_hi": float(dB.std(ddof=1)/np.sqrt(len(dB))),
            "R": float(Rh), "se_R": float(R.std(ddof=1)), "R_ci95": [lo, hi],
            "sigma_from_1": float(abs(1-Rh)/R.std(ddof=1)),
            "attenuation_pct": float(100*(1-Rh)),
            "inflation_1_over_R": float(1/Rh),
            "inflation_ci95": [float(1/hi), float(1/lo)],
            "R_ci_excludes_1": bool(lo > 1.0 or hi < 1.0),
        }
    return o


rng = np.random.default_rng(RSEED)
main = load(os.path.join(HERE, "diag3_all.ndjson"))       # equal-tau + convergence
a1 = load(os.path.join(HERE, "diag3_aniso_arm1.ndjson"))
a2 = load(os.path.join(HERE, "diag3_aniso_arm2.ndjson"))

# block sd of the NULL arm at M=400 -> the floor the scout actually uses
sd400 = {s: float(np.std([r[s] for (m, k, b), r in main.items()
                          if m == 400 and k == 0.0], ddof=1)) for s in STATS}
floor96 = {s: Z*sd400[s]*np.sqrt(2/96) for s in STATS}

rep = {
    "diagnostic": "DIAG 3 — signal-fidelity M-sweep",
    "status": "PILOT — registers nothing, authorizes nothing",
    "seed_namespace": "diag10::",
    "quarantine": "QUARANTINED from v44pilot:: and v43::; NEVER pooled (law #6)",
    "interpreter": "/usr/bin/python3 (Python 3.9.6, numpy 2.0.2)",
    "harness": {
        "file": "v44_scout.py (PRISTINE, unedited; imported from a snapshot copy)",
        "source_sha256": hashlib.sha256(
            open(os.path.join(HERE, "v44_scout_pristine.py"), "rb").read()).hexdigest(),
        "source_sha_short": "0b65a9ee92b9fe2c",
        "config_hash": "a344d6c47c8a22c1",
        "cfg_edited": False,
        "M_passed_via": "M_grid_ov override (CFG untouched -> config_hash unchanged)",
    },
    "chamber": {"mode": "frozen", "scale": 10.0, "Tc": 1.0,
                "signal": "registered c4v vortex arms kappa in {4,8} (calibrated true signal)"},
    "estimand": ("R = increment@M_lo / increment@M_hi, increment = mean(y|kappa) - mean(y|k0) "
                 "at matched (M, block). R<1 => the coarse grid ATTENUATES the realized "
                 "response to a KNOWN vortex."),
    "bootstrap": {"n_resamples": NB, "rng_seed": RSEED,
                  "unit": "paired-difference vectors d_i (preserves the CRN correlation; "
                          "resampling raw y independently would OVERSTATE se(R))"},
    "detection_floor": {
        "formula": "3.858 * sd * sqrt(2/B)  [harness line 670; alpha_worst=.005, power=.90]",
        "B_conf": 96,
        "sd_null_M400": sd400,
        "floor_B96": {s: float(floor96[s]) for s in STATS},
        "note": ("DIAG 1 (receipt 06) showed sd is ~M-independent, so the FLOOR is "
                 "~M-independent. All M-dependence of detectability therefore flows "
                 "through the signal attenuation R: D_min(M) = floor / R(M)."),
    },
    "results": {},
}

rep["results"]["equal_tau_1_1"] = {
    "note": "primary measurement, n=900 blocks per (M,kappa) cell",
    "k4_M400_vs_M2000": comp(main, 400, 2000, 4.0, rng),
    "k8_M400_vs_M2000": comp(main, 400, 2000, 8.0, rng),
}
rep["results"]["convergence_check"] = {
    "note": ("M=2000 is not a priori ground truth. If the response were still rising with M, "
             "R=resp400/resp2000 would OVERSTATE fidelity (the dangerous direction). "
             "These arms test that. n=300/cell."),
    "k8_M2000_vs_M5000": comp(main, 2000, 5000, 8.0, rng),
    "k8_M2000_vs_M8000": comp(main, 2000, 8000, 8.0, rng),
    "k8_M400_vs_M8000": comp(main, 400, 8000, 8.0, rng),
}
rep["results"]["aniso_transfer"] = {
    "note": ("Does the attenuation measured at equal-tau transfer to the MISMATCH geometry "
             "the scout actually runs? Registered aniso_pairs. k8, n=400/cell."),
    "arm1_tx0.25_ty1.0__k8_M400_vs_M2000": comp(a1, 400, 2000, 8.0, rng),
    "arm2_tx1.0_ty0.25__k8_M400_vs_M2000": comp(a2, 400, 2000, 8.0, rng),
}

# worst case across every cell measured
cells = []
for grp in rep["results"].values():
    for kk, v in grp.items():
        if kk == "note":
            continue
        for stat, d in v.items():
            cells.append((f"{kk}::{stat}", d["R"], d["R_ci95"][0], d["inflation_ci95"][1]))
worst = max(cells, key=lambda c: c[3])
rep["verdict"] = {
    "n_cells_measured": len(cells),
    "R_range": [float(min(c[1] for c in cells)), float(max(c[1] for c in cells))],
    "worst_cell": worst[0],
    "worst_case_inflation_of_min_detectable_true_current": float(worst[3]),
    "feared_value_from_receipt06": 1/0.67,
    # No pass/fail boolean is emitted: a bare threshold constant here would be
    # exactly the kind of ungrounded naked number this program forbids. The
    # verdict is the argument in DIAG3_REPORT.md sec.5-sec.7, not a magic constant.
    "scope": ("Bounds the EXTERNAL-FORCE channel (injected vortex). The scout's engine "
              "signal is GRID-GENERATED (a difference of two noisy S_c grids); that "
              "channel is reduced by the aniso-transfer arms but NOT directly bounded. "
              "See DIAG3_REPORT.md sec.7."),
}
json.dump(rep, open(os.path.join(OUT, "diag3_analysis.json"), "w"), indent=1)
print(json.dumps(rep["verdict"], indent=1))
print("\n-> diag3_analysis.json")
