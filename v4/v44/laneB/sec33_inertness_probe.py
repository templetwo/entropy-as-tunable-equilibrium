#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lane B, task 1 — independent verification of the sec-3.3 coupled-upper
inertness claim, against THE CODE THAT RUNS (band_cell in v44_scout.py,
imported, sha-asserted), not a reimplementation.

CLAIM UNDER AUDIT (overnight finding, 2026-07-12): sec 3.3's ratified
"coupled-upper" RED-robustness clause is provably inert — 3.6M probes never
changed an answer.

METHOD (three legs, each required):

  ANALYTIC — the emptiness theorem (stated in LANEB_FINDINGS.md, verified
  numerically here): rule_floor(sd,B) = F·sd and rule_se(sd,n) = S·sd are both
  homogeneous of degree 1 in sd. Writing kappa := F − t·S (the unit-sd RED
  margin) and c := chi2_upper_factor(df) > 1, each upper conjunct
  `y + t·SE(c·sd) < floor(c·sd)` is `y < c·sd·kappa`, while its point-sd twin
  is `y < sd·kappa`.
    - If kappa > 0: point implies upper strictly (c > 1). Upper never binds.
    - If kappa <= 0: the v3.2 magnitude point conjunct |mu| < sd·kappa <= 0 is
      unsatisfiable, so RED is unreachable and the conjunction is already
      false without the upper clauses.
  Hence the coupled-upper conjuncts can never change a verdict. (Corollary:
  the v3.1 aligned point conjunct is also implied by the magnitude point
  conjunct, since x = sigma·mu <= |mu|; the operative content of sec 3.3 is
  the single inequality |mu| + t·SE(sd) < floor(sd).)

  EMPIRICAL-IDENTITY — sweep band_cell (the real one) against band_cell with
  the coupled-upper clause turned off THROUGH ITS OWN CODE PATH (monkeypatch
  _chi2_upper_factor -> 1.0, making sd_up == sd_cell so the upper conjuncts
  degenerate to the point conjuncts). Any verdict difference anywhere =
  the clause binds = the claim is FALSE.

  POWER CONTROL (law #2 applied to this probe itself) — the same sweep is run
  against a deliberately BINDING variant (floor-only upper: floor at sd_up,
  SE at point sd — the variant v3.1's own MC measured at 18.86% vs point-sd
  3.95%). If the sweep cannot find differences THERE, the sweep is blind and
  its null on the real clause counts for nothing. Expected: many differences.

Anti-blind-fixture notes: the sweep uses NO fixed seed for the grid legs
(they are deterministic grids, including boundary-hugging points at
float-epsilon distances from every cutpoint, at five sd scales spanning 1e-6
to 1e6); the randomized block-level leg seeds are printed. Nothing stubs any
timing, I/O, or arithmetic inside band_cell/ladder_terminal.

Primary record: NDJSON lines on stdout (law #7), one per (leg, config) with
counts; final SUMMARY line carries the verdict.
"""
import hashlib
import importlib.util
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SCOUT = os.path.normpath(os.path.join(HERE, "..", "v44_scout.py"))

# ---- certify-what-runs: sha-assert the imported source ----------------------
EXPECTED_SHA256 = "1fe9fa1c9d203c508fbc4016a8e39e1a7dc055824a91e2935b1db9bfbfc0e35d"
got = hashlib.sha256(open(SCOUT, "rb").read()).hexdigest()
assert got == EXPECTED_SHA256, (
    "v44_scout.py sha256 mismatch: probing code that is not the pinned rule\n"
    "  expected %s\n  got      %s" % (EXPECTED_SHA256, got))

spec = importlib.util.spec_from_file_location("v44_scout", SCOUT)
scout = importlib.util.module_from_spec(spec)
sys.argv = [SCOUT]  # keep its main() argument sniffing inert on import
spec.loader.exec_module(scout)
assert scout.SOURCE_SHA == EXPECTED_SHA256[:16]

RULE = scout.RULE

def emit(obj):
    print(json.dumps(obj), flush=True)

emit({"type": "provenance", "probe": "sec33_inertness", "lane": "B",
      "scout_sha256": got, "source_sha": scout.SOURCE_SHA,
      "rule_version": RULE["rule_version"], "numpy": np.__version__,
      "python": sys.version.split()[0]})

# ---- the three band_cell variants -------------------------------------------
band_real = scout.band_cell

def with_chi2_factor_one(fn, *args):
    """Run fn with the coupled-upper clause degenerated through band_cell's
    OWN code path: sd_up == sd_cell, so the upper conjuncts equal the point
    conjuncts. This IS 'clause off' without touching band_cell's source."""
    orig = scout._chi2_upper_factor
    scout._chi2_upper_factor = lambda df: 1.0
    try:
        return fn(*args)
    finally:
        scout._chi2_upper_factor = orig

# Positive control: a variant in which the upper clause PROVABLY binds —
# SE at sd_up but floor at POINT sd, so the upper-conjunct threshold is
# sd·(F − c·t·S) < sd·kappa: strictly tighter, must flip REDs to AMBER.
# (First attempt used floor-only-at-sd_up, threshold sd·(c·F − t·S) > kappa —
# ALSO inert, by the same homogeneity lemma; that run is kept in the raw
# record as sec33_probe_raw_run1.ndjson: a control must be tighter than the
# point conjunct to bind, and only the SE-side inflation achieves that.)
# Built from band_cell's real source with ONE surgical substitution.
import inspect
src = inspect.getsource(scout.band_cell)
needle = "f_u = rule_floor(sd_up, B_conf)"
assert src.count(needle) == 1, "band_cell source drifted; refusing to build control"
ctrl_src = src.replace(needle, "f_u = rule_floor(sd_cell, B_conf)")
ctrl_src = ctrl_src.replace("def band_cell(", "def band_cell_flooronly(", 1)
ns = dict(vars(scout))
exec(ctrl_src, ns)
band_flooronly = ns["band_cell_flooronly"]

# ---- sweep infrastructure ----------------------------------------------------
CONFIGS = [(8, 96), (16, 96), (32, 96), (32, 128), (8, 64)]
SIGMAS = [+1, -1, None]

def kappa_unit(n, B, sigma):
    df = n - 1
    t = (RULE["t_two_sided"] if sigma is None else RULE["t_one_sided"])[df]
    F = RULE["Z"] * math.sqrt(2.0 / B)
    S = math.sqrt(1.0 / n + 1.0 / RULE["ref_blocks"])
    return F - t * S, t, F, S

def boundary_points(n, B, sigma, sd):
    """Cutpoint-hugging mu values: every threshold the rule owns, at +-eps."""
    k, t, F, S = kappa_unit(n, B, sigma)
    c = RULE["chi2_upper"][n - 1]
    pts = []
    for base in (k * sd, c * k * sd, -k * sd, -c * k * sd,
                 (F + t * S) * sd, -(F + t * S) * sd,
                 t * S * sd, -t * S * sd, 0.0):
        for i in range(1, 41):
            pts.append(math.nextafter(base, base + 1.0 * i))
            pts.append(math.nextafter(base, base - 1.0 * i))
        pts.extend([base, base + 1e-12 * sd, base - 1e-12 * sd,
                    base + 1e-9 * sd, base - 1e-9 * sd])
    return pts

def run_sweep(tag, mus, sd, n, B, sigma):
    """Return (n_probes, diffs_clause_off, diffs_flooronly)."""
    d_off = 0
    d_ctl = 0
    for mu in mus:
        b_real = band_real(mu, sd, n, B, sigma)[0]
        b_off = with_chi2_factor_one(band_real, mu, sd, n, B, sigma)[0]
        b_ctl = band_flooronly(mu, sd, n, B, sigma)[0]
        if b_real != b_off:
            d_off += 1
            emit({"type": "DIFF_CLAUSE_BINDS", "tag": tag, "mu": mu, "sd": sd,
                  "n": n, "B": B, "sigma": sigma, "real": b_real, "off": b_off})
        if b_real != b_ctl:
            d_ctl += 1
    return len(mus), d_off, d_ctl

total = 0
diffs_off = 0
diffs_ctl = 0

# LEG 1 — dense grids at five sd scales (deterministic; no seed to hide behind)
for sd in (1e-6, 0.037, 1.0, 137.0, 1e6):
    n_grid = 120001 if sd == 1.0 else 30001
    for (n, B) in CONFIGS:
        for sigma in SIGMAS:
            mus = np.linspace(-2.5 * sd, 2.5 * sd, n_grid)
            npr, do, dc = run_sweep("grid", mus, sd, n, B, sigma)
            total += npr; diffs_off += do; diffs_ctl += dc
            emit({"type": "leg", "leg": "grid", "sd": sd, "n": n, "B": B,
                  "sigma": sigma, "probes": npr, "diff_clause_off": do,
                  "diff_flooronly_control": dc})

# LEG 2 — cutpoint-hugging float-boundary probes
for sd in (1e-6, 1.0, 137.0):
    for (n, B) in CONFIGS:
        for sigma in SIGMAS:
            mus = boundary_points(n, B, sigma, sd)
            npr, do, dc = run_sweep("boundary", mus, sd, n, B, sigma)
            total += npr; diffs_off += do; diffs_ctl += dc
emit({"type": "leg", "leg": "boundary", "note": "cutpoint-hugging, all configs",
      "cum_probes": total, "cum_diff_clause_off": diffs_off,
      "cum_diff_flooronly_control": diffs_ctl})

# LEG 3 — randomized block-level identity through ladder_terminal (the real
# pipeline: stamp() computes mu/sd from block series; both statistics laddered)
SEEDS = [11, 20260713, 424242, 777, 31337]
lad_total = 0
lad_diffs = 0
for seed in SEEDS:
    rng = np.random.default_rng(seed)
    for i in range(20000):
        kind = i % 4
        if kind == 0:
            q = rng.normal(rng.uniform(-0.4, 0.4), rng.uniform(0.2, 3.0), 32)
        elif kind == 1:
            q = rng.standard_t(3, 32) * rng.uniform(0.05, 2.0)
        elif kind == 2:
            q = rng.normal(0.0, 1.0, 32) * 1e-3       # deep-RED shaped
        else:
            q = rng.normal(rng.uniform(0.5, 3.0), 1.0, 32)  # GREEN shaped
        w = rng.normal(rng.uniform(-0.3, 0.3), rng.uniform(0.2, 2.0), 32)
        sp = rng.choice([1, -1, 0]); sw = rng.choice([1, -1, 0])
        sp = None if sp == 0 else int(sp)
        sw = None if sw == 0 else int(sw)
        r1 = scout.ladder_terminal(list(q), list(w), None, sp, sw)
        r2 = with_chi2_factor_one(scout.ladder_terminal, list(q), list(w), None, sp, sw)
        lad_total += 1
        if (r1["primary"], r1["omega"], r1["rung"]) != (r2["primary"], r2["omega"], r2["rung"]):
            lad_diffs += 1
            emit({"type": "DIFF_LADDER", "seed": seed, "i": i,
                  "real": r1, "off": r2})
emit({"type": "leg", "leg": "ladder_random", "seeds": SEEDS,
      "cells": lad_total, "diff_clause_off": lad_diffs})

total += lad_total
diffs_off += lad_diffs

emit({"type": "SUMMARY",
      "probes_total": total,
      "clause_off_verdict_differences": diffs_off,
      "flooronly_control_differences": diffs_ctl,
      "probe_has_power": diffs_ctl > 0,
      "inertness_confirmed": (diffs_off == 0 and diffs_ctl > 0),
      "kappa_unit_by_config": {
          "%db_B%d_%s" % (n, B, {1: "1s+", -1: "1s-", None: "2s"}[s]):
              round(kappa_unit(n, B, s)[0], 6)
          for (n, B) in CONFIGS for s in SIGMAS}})
