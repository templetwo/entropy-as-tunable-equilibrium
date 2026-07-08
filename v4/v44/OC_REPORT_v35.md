# v4.4 Scout — OC Confirmation Report (v3.5)

*HQ (Mac Studio, canonical interpreter), 2026-07-08. Produced by `oc_sim_v35.py` on `/usr/bin/python3` (Python 3.9.6, numpy 2.0.2), seed 20260708, N=4×10⁶. Fills v3.5's one TBD number (gate 9/9Ω compound power). Reference-uncertain estimand baked in and verified (α selftest). NOT registered.*

## Results
| quantity | value | criterion | verdict |
|---|---|---|---|
| rerun H0 one-sided α (reference-uncertain selftest) | **0.04999** | ≈ 0.05 (NOT ~0.019) | ✓ invariant locked |
| rerun per-contrast power, n_rerun=56 | **0.91335** | ≥ 0.90 | ✓ |
| **gate 9/9Ω compound power — full protective union (law #3)** | **0.97994** | ≥ 0.90 | ✓ **PASS** |
| — disposition-only reading (anomaly-flag × rerun; the *wrong* event) | 0.760 | — | recorded, not the gate |
| gate 1 false-GREEN on null (per cell) | 0.000236 | small | ✓ (six-cell ≈ 0.0014) |
| gate 4 GREEN power @ +3×floor | 0.99991 | ≥ 0.90 | ✓ |
| wrong-sign −1×floor terminal band dist | ANOM 0.832 / INCONCLUSIVE 0.148 / RED 0.020 | — | belt+ladder |

## The compound-power resolution (v3.5's last TBD)
"Compound six-cell power" for gate 9/9Ω = **P(the rule does NOT clear a gating cell to actual-RED | that cell carries a −1×floor wrong-sign current)**, via the full protective union {belt |μ̂|-magnitude bound, ANOMALOUS→powered n=56 rerun, STABLE-fail}, through the complete terminal ladder (16b/B96 → 32b/B96 → 32b/B128 → INCONCLUSIVE).

**Value: 0.980 ≥ 0.90 → PASS.** It is a **lower bound** — the sim credits banding only, not the STABLE (P1-B) gate, which adds further protection. The disposition-only product (anomaly-flag × rerun = 0.76) is the v4.3 per-contrast trap and is **not** the gate — the powered rerun is a backup to the belt, not the sole guarantee.

Note vs the earlier single-16b-look estimate (0.9965): the full ladder is lower (0.980) because it gives a wrong-sign current more looks to eventually band RED (2.0% terminal RED vs 0.35% at one look). The full-path number supersedes the one-look shortcut. Consistent with gate 5 (invalid-pivot ≤ 0.02).

## Cross-check pending (independent replication)
Grok Build has been issued the same contracted OC run on numpy 2.4.4 (raw output → HQ diffs). A clean match against these canonical-interpreter numbers is a cross-version replication (cf. v4.3 48/48 bit-exact). The full exhaustive scenario set (omega-only S8, occupancy-only S10, demotion S9, coupling ρ∈{−1,0,0.5,1,2} per-arm) remains for the exhaustive registration artifact; the load-bearing gates are confirmed here.

## Provenance
`oc_sim_v35.py` (source), `oc_results_v35.json` (results). Deterministic, seeded, canonical interpreter. Estimand invariant (draw the 64-block reference each rep) verified by the α=0.05 selftest.
