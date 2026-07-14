# Lane A Report — Certify the Code That Runs

*mesh-20260713, fable (1/3). Worktree `~/Desktop/lab/mesh-v44-laneA`, branch
`v44-audit-ocsim` @ `7a02eb5`. Main tree untouched. NOT a registration
artifact; nothing here registers, authorizes, or tunes anything (laws #1, #3).
Canonical interpreter `/usr/bin/python3` (3.9.6, numpy 2.0.2). All receipts
self-hashed cmd (the worktree lives under `~/Desktop`; the iCloud receipt
wedge applies).*

## Verdict line

**Gate 9/9Ω compound power for v3.5-AS-EXECUTABLE = 0.98114 ≥ 0.90 → PASS.**
Blocker 1 was real — the certified sims and the executable rule genuinely band
different estimators, and the divergence reproduces exactly — but the
executable gate lands on the same side of the law-#3 floor as the ratified
number (0.97994), marginally stronger. **The certification-instrument mismatch
does not, by itself, invalidate the ratified compound-power verdict.** It does
mean the 0.980 was luck, not certification, until tonight: the number that now
describes the code that runs was produced by the code that runs.

## 1. The estimator seam, named exactly (task 1)

| | certified sims (`oc_sim_v35.py`, `oc_sim_v35_full.py`) | executable (`scout_report → ladder_terminal → stamp`, `v44_scout.py:839–841`) |
|---|---|---|
| statistic fed to the band | `mean(blocks) − mean(64-block reference)`, reference redrawn per replication (the rerun-power arbitration's estimand invariant) | `band_cell(v.mean(), v.std(ddof=1), …)` — the **raw cell mean**; no reference is drawn or subtracted anywhere in the scout data path |
| variance of that statistic under null | `sd²(1/n + 1/64)` — matches the SE the rule uses | `sd²/n` — **tighter** than the SE the rule uses (`rule_se` folds in a 1/64 that never exists) |
| consequence | — | the executable rule REDs **more** on a true null at every config |

Also mapped (known/secondary): the ratified-numbers sim additionally used a
fixed (sd=1) floor — the documented erratum — and a single-statistic ladder
vs the executable primary-OR-omega shared ladder. The sec-8 powered rerun
(`n_rerun=56`) has **no executable function** — it exists as config + prose
only; it did not enter the ratified 0.980 either (disposition-only reading
was recorded, not the gate), so the compound event here is identical.

Blocker-1's measured pair reproduces through the **imported** `band_cell`
(400k draws/config, identical band logic, only the estimator varied):

| config | exec (raw mean) | ref-subtracted | note |
|---|---|---|---|
| 16b/B96 1s | 0.20677 | 0.18653 | |
| 32b/B96 1s | 0.70969 | 0.61245 | |
| **32b/B96 2s** | **0.47984** | **0.40205** | ≈ blocker's 0.4768/0.4002 |
| **32b/B128 1s** | **0.48024** | **0.40073** | ≈ blocker's 0.4768/0.4002 |
| 32b/B128 2s | 0.18029 | 0.14769 | |

## 2. The instrument (task 2)

`oc_sim_v36_exec.py` — **nothing reimplemented.** Every replication routes
through the imported `v44_scout.band_cell` / `ladder_terminal` /
`scout_outcome`. Certify-what-runs is structural: sha-pin asserted at import
in the parent and every spawned worker —

```
v44_scout.py  sha256 = 1fe9fa1c9d203c508fbc4016a8e39e1a7dc055824a91e2935b1db9bfbfc0e35d
config_hash  = a344d6c47c8a22c1     git = 7a02eb5     rule_version = v3.5
```

(matches blocker-2's post-edit hash exactly). One byte of drift and the sim
refuses to run. Law-#4 spot-asserts on floor/SE constants at import.

## 3. The compound-power Monte Carlo, executable path (task 3)

Seed 20260713 (quarantined namespace, disjoint from 20260707/08/10, law #6).
Raw NDJSON primary record with per-chunk derived seeds (law #7):
`oc_results_v36_exec.ndjson`, sha256
`839f93e34a4d55d55f63293e4181aa68070f82d6fa9f15990250ae7430a8e9d1`.
Chunk totals reconcile to every declared N. Wall 123s on 12 workers.

| quantity | EXECUTABLE (this run) | ratified / §13 | reading |
|---|---|---|---|
| **gate 9/9Ω compound (1 − P(wrong-sign −1×floor cleared to RED))**, N=4M | **0.98114** | 0.97994 | **PASS ≥ 0.90.** Composition shifts: ANOM 0.876 vs 0.832, CEILING 0.106 vs 0.148, RED 0.0189 vs 0.020 — more of the protection is carried by ANOMALOUS, less by the ceiling; the union is equivalent. |
| gate 1 false-GREEN on null (per cell), N=4M | 0.000416 | 0.000236 | 1.8× the ratified rate, still ≪ any threshold that matters. Direct consequence of the tighter executable statistic. |
| terminal P(RED \| null) per cell, N=4M | 0.647867 | (refsub ≈ 0.55–0.61 by config) | The pivot's fuel. The executable rule is *more* willing to call a null cell RED. |
| gate 4 GREEN power @ +3×floor, N=4M | 0.99997 | 0.99991 | equivalent |
| pivot licensed \| 6-cell true null, STABLE at chance, N=500k each | **0 of 500,000** (one-sided); **0 of 500,000** (two-sided) | §13 predeclared 0.017 / 0.0014 | See §4 — the suspenders, not the band. |
| pivot licensed \| 6-cell true null, **STABLE forced true**, N=500k | **0.016304** | §13 predeclared 0.017 | Lands on the predeclared value. The §13 expectation implicitly assumed STABLE fires. |

## 4. Finding for the table (reported, not fixed)

**The executable rule licenses its pivot at the §13-predeclared rate (~1.6%
per fully-null six-cell pass) ONLY when STABLE is granted.** With STABLE at
its null-chance rate (P(≥12/16 | p=½) ≈ 0.038 per cell), the executable
`scout_outcome` licensed **zero** pivots in a million six-cell null passes —
the all-RED × all-STABLE conjunction is ≈10⁻¹⁰. This is the code-side twin of
the P1 packet's physics-side finding (P1-B cannot fire because σ_cell is
unidentifiable at the registered instrument): **wherever STABLE's true firing
rate lands, the pivot rate is bounded by (that rate)⁶ × 0.074.** The two
findings compose into one sentence: *as ratified and as executable, outcome 2
(PIVOT_ALL_RED) is unreachable unless P1 is amended.* Which amendment (P1
packet options 1–4) is a Lane B / Anthony decision, not Lane A's.

Secondary observations, same status:
- The sec-8 powered rerun is prose+config only; if a future rule revision
  leans on it as executable protection, it must first exist as code.
- The wrong-sign protection's composition shift (more ANOM, less CEILING)
  slightly changes what an operator *sees* on a wrong-sign current, not what
  the gate does.

## 5. P1 pinned re-run (task 5, blocker 5) — **provisional status LIFTABLE**

`p1_signstability_diag10_pinned.py` (new file; the unpinned original is
untouched) re-ran the full diag10 plan — identical quarantined `diag10::`
seed derivation, same instrument path (`frozen_grid`/`Geom` imported from the
pinned harness), sha-assert in parent and every worker, raw NDJSON primary
record (`p1_signstability_full_pinned.ndjson`).

**All 1,536 per-seed curls are bit-exact against the 2026-07-12 unpinned run**
(8 pair×M combinations × 3 estimators × 64 seeds, compared value-for-value).
The mid-edit harness import did not touch the physics path. The P1 packet's
numbers are hereby reproduced under pin `1fe9fa1c…` @ `7a02eb5` — blocker 5's
"not pinned to a known source" no longer applies to them.

The pinned P1-B check (sign from DEF-A @ M=4000 vs per-seed M=400 agreement):
agreement 0.41–0.63 across all four τ-pairs and all three estimators (12/16
threshold needs 0.75); **2 of 48 sixteen-seed windows fired STABLE** (~0.04);
and `stencil_clean` flips σ_cell's sign vs `stencil` on two of four pairs —
the registered directional prediction is estimator-dependent, i.e.
unidentifiable, exactly as the packet said. Composed with §4:
P(pivot | true null) ≲ 0.04⁶ × 0.074 ≈ 10⁻¹⁰ as ratified.

## 6. Artifacts (all on branch `v44-audit-ocsim`, worktree only)

| file | sha256 |
|---|---|
| `oc_sim_v36_exec.py` (hardened: canonical chunk order + sorted keys, wall time stdout-only) | `3ede691124835db906df761ede3f2c0e98ca75592cb5220bdd28188b155e0bce` |
| `oc_results_v36_exec.ndjson` (primary, **byte-reproducible**: two independent full runs both hash `f80838ef…`) | `f80838efe04933577e333e4a37e40b7ce1a7a668a14b7677fe9142fe87021a5f` |
| `p1_signstability_diag10_pinned.py` | `bb9865e4c5b4718b9023a4cbcf4c996c14fefccf96fb5baa005e98dbd2491fc8` |
| `p1_signstability_full_pinned.ndjson` (primary) | `79f0ed2670daecbbabf3b892e95bc07d93578bc2d43fa9bef900b55080b9686a` |
| `diag10_signstability_full_pinned.json` (secondary, analyzer-compat) | `7ffe3e38d05cf931871ac31296cbac40899aea6dd8eea6e856b7a8bbfee4a024` |

Nothing merges without anchor verification + Anthony (collision law).

*Rev 2 (anchor's hardening note applied): chunk records now written in
canonical (scenario, chunk) order with sorted keys; wall time removed from the
record. Verified by running the full MC twice — identical NDJSON sha256 both
times, gate 9 compound unchanged at 0.98114. The earlier unordered record
(`839f93e3…`) is superseded by `f80838ef…`; same seeds, same counts, same
numbers, canonical bytes.*
