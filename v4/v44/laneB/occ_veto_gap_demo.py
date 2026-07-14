#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lane B, task 2 — concrete demonstration of the occupancy GREEN-veto hole
(blocker 4): a pivot PRECONDITION (sec 5 (iii')) can be evaluated — and a
full PIVOT_ALL_RED licensed — on an estimand the code itself labels
"NOT RATIFIED, NOT REGISTERED".

The demonstration is three runs of the REAL scout_report() (imported,
sha-asserted) over the same synthetic scout NDJSON:

  RUN A  no --occ-reduction        -> decision WITHHELD (OCC_REDUCTION_GAP).
                                      This is the code behaving correctly.
  RUN B  --occ-reduction lr_asymmetry
                                   -> decision EMITTED, outcome PIVOT_ALL_RED,
                                      pivot_licensed=True. The ONLY change
                                      from run A is one analysis-time CLI
                                      flag selecting a reduction whose own
                                      docstring says NOT RATIFIED, NOT
                                      REGISTERED. Nothing downstream checks
                                      registration; the choice is stamped in
                                      the report but never blocks.
  RUN C  same flag, occupancy histograms carrying a LARGE symmetric shift
         (25x mass moved from center to both edges, invisible to a
         left/right asymmetry scalar)
                                   -> pivot STILL licensed. An alternative
                                      (equally unregistered) reduction on the
                                      SAME blocks bands GREEN — i.e. would
                                      veto. The veto's answer is a function
                                      of an estimand chosen at the CLI, which
                                      is exactly why sec 5 (iii') is an open
                                      hole until the reduction is REGISTERED.

Constructed cell data (deterministic, no RNG): primary and omega blocks are
[+1, -1] * 8 per cell (mean exactly 0, sd ~ 1.03), so both band RED at the
16b/B96 rung (|mu| = 0 < kappa = 0.067*sd; not ANOMALOUS; ladder terminates
at 16b since neither statistic is AMBER). Occupancy is stamped at that same
terminal rung, where two-sided RED is unreachable (kappa_2s < 0) and the
constructed lr_asymmetry scalars are far from GREEN -> occupancy AMBER,
recorded + caveated, NON-blocking. All preconditions in the p1 file are
satisfied (STABLE everywhere, full rosters registered).

Primary record: NDJSON on stdout (law #7).
"""
import hashlib
import importlib.util
import io
import json
import os
import sys
from contextlib import redirect_stdout

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SCOUT = os.path.normpath(os.path.join(HERE, "..", "v44_scout.py"))
EXPECTED_SHA256 = "1fe9fa1c9d203c508fbc4016a8e39e1a7dc055824a91e2935b1db9bfbfc0e35d"
got = hashlib.sha256(open(SCOUT, "rb").read()).hexdigest()
assert got == EXPECTED_SHA256, "v44_scout.py sha mismatch: not the pinned rule"

spec = importlib.util.spec_from_file_location("v44_scout", SCOUT)
scout = importlib.util.module_from_spec(spec)
sys.argv = [SCOUT]
spec.loader.exec_module(scout)

def emit(o):
    print(json.dumps(o), flush=True)

emit({"type": "provenance", "probe": "occ_veto_gap", "lane": "B",
      "scout_sha256": got, "source_sha": scout.SOURCE_SHA,
      "rule_version": scout.RULE["rule_version"], "numpy": np.__version__})

CELLS = ["A", "B", "C", "D", "AxT2", "AxT4"]

def hist_mild(i):
    """24-bin occupancy histogram with a hair of L/R asymmetry, alternating
    sign per block (lr_asymmetry scalar = ~ +-0.001; mean ~ 0, sd > 0)."""
    v = [10.0] * 24
    v[18] += 0.5 if i % 2 == 0 else -0.5     # +-0.5 of 240 total -> ~0.002
    v[6] -= 0.5 if i % 2 == 0 else -0.5
    return v

def hist_edge_shift(i):
    """SAME lr_asymmetry (~+-0.001 alternating) but with a huge SYMMETRIC
    center->edges mass shift a left/right scalar cannot see."""
    v = [2.0] * 24
    for k in (0, 1, 2, 3, 20, 21, 22, 23):
        v[k] = 50.0                            # edges loaded 25x vs center
    v[0] += 0.01 * (i % 3)                     # deterministic jitter so the
    v[23] += 0.01 * ((i + 1) % 3)              # edge-mass scalar has sd > 0
    v[18] += 0.5 if i % 2 == 0 else -0.5
    v[6] -= 0.5 if i % 2 == 0 else -0.5
    return v

def make_rows(hist_fn):
    rows = []
    for cell in CELLS:
        for b in range(16):
            pm = 1.0 if b % 2 == 0 else -1.0   # mean 0, sd ~1.03 -> RED 1-sided
            rows.append({"cell": cell, "block": b,
                         "quad_loop_rate": pm,
                         "omega_roi": pm,
                         "occupancy_x": hist_fn(b)})
    return rows

P1 = {c: {"sigma_cell": 1, "sigma_omega_cell": 1, "stable": True} for c in CELLS}
P1["__gating_roster__"] = CELLS
P1["__full_roster__"] = CELLS
p1_path = os.path.join(HERE, "occ_demo_p1.json")
json.dump(P1, open(p1_path, "w"))

def run(rows, opts):
    buf = io.StringIO()
    with redirect_stdout(buf):
        rep = scout.scout_report(rows, opts)
    return rep

# ---- RUN A: no reduction selected -> the code refuses (correct behavior) ----
rep_a = run(make_rows(hist_mild), {"p1": p1_path})
emit({"type": "RUN_A_no_reduction",
      "decision_emitted": rep_a["decision"]["emitted"],
      "withheld_because": rep_a["decision"]["withheld_because"]})
assert rep_a["decision"]["emitted"] is False
assert any("NOT registered" in w for w in rep_a["decision"]["withheld_because"])

# ---- RUN B: one CLI flag selects the unregistered reduction -----------------
rep_b = run(make_rows(hist_mild), {"p1": p1_path, "occ_reduction": "lr_asymmetry"})
emit({"type": "RUN_B_unregistered_reduction",
      "decision_emitted": rep_b["decision"]["emitted"],
      "outcome": rep_b["decision"].get("outcome"),
      "pivot_licensed": rep_b["decision"].get("pivot_licensed"),
      "occ_reduction_stamped": rep_b["decision"].get("occ_reduction"),
      "occupancy_bands": {c: rep_b["cells"][c]["occupancy"] for c in CELLS},
      "reduction_self_label": scout._occ_lr_asymmetry.__doc__.splitlines()[0]})

# ---- RUN C: estimand-dependence — a symmetric shift the scalar cannot see ---
rows_c = make_rows(hist_edge_shift)
rep_c = run(rows_c, {"p1": p1_path, "occ_reduction": "lr_asymmetry"})

def edge_mass(hist):
    v = np.asarray(hist, float)
    return float((v[:4].sum() + v[-4:].sum()) / v.sum())

# Band the SAME blocks under an alternative (equally unregistered) reduction,
# through the real band_cell at the same terminal rung (16b/B96, two-sided).
em = [edge_mass(r["occupancy_x"]) for r in rows_c if r["cell"] == "A"]
em_band = scout.band_cell(float(np.mean(em)), float(np.std(em, ddof=1)),
                          16, 96, None)[0]
emit({"type": "RUN_C_estimand_dependence",
      "pivot_licensed_under_lr_asymmetry": rep_c["decision"].get("pivot_licensed"),
      "occupancy_bands_under_lr_asymmetry": {c: rep_c["cells"][c]["occupancy"] for c in CELLS},
      "same_blocks_under_edge_mass_reduction": em_band,
      "edge_mass_mean": round(float(np.mean(em)), 4),
      "note": "identical occupancy data: lr_asymmetry -> no veto, pivot "
              "licensed; edge_mass -> GREEN -> would veto. The veto's answer "
              "is the analyst's estimand choice."})

emit({"type": "SUMMARY",
      "hole_demonstrated": (rep_a["decision"]["emitted"] is False
                            and rep_b["decision"].get("pivot_licensed") is True
                            and rep_c["decision"].get("pivot_licensed") is True
                            and em_band == "GREEN"),
      "statement": "sec 5 (iii') evaluated, and PIVOT_ALL_RED licensed, on a "
                   "reduction the code labels NOT RATIFIED NOT REGISTERED; "
                   "registration of the reduction is load-bearing."})
