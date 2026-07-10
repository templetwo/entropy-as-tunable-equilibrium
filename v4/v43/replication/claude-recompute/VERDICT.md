# Independent Recompute — Matched-τ Occupancy Shift & Detailed Balance
## claude-fable seat, 2026-07-09 · replication/claude-recompute

**Question under test.** The last surviving positive of the v4 campaign: the
matched-τ occupancy micro-shift (C1m frozen vs online, τ=0.25, M=256, 32
blocks/arm). Does it carry probability current (motor) or is it an
equilibrium difference (no motor)?

**Protocol.** Blind-first: preregistration, harness, and raw NDJSON read;
`v43_analysis.json`, `v4_analysis.json`, FORENSIC and VERDICT docs left
unopened until my numbers existed. Statistics pre-declared in
`recompute_stats.py` header before any confirmatory unit ran.

**Method.** All 72 relevant units (32 frozen, 32 online, 6 C4v k8, 2 C4v k0)
re-simulated from archived seeds with a passive transition-count observer
hooked into `CurrentAcc.add` (zero RNG calls added). Bit-exact agreement with
the archived NDJSON therefore proves cross-version determinism (numpy
2.0.2→2.4.4, python 3.9.6→3.12.3) **and** observer non-interference
simultaneously. Result: **72/72 bit-exact** (sole tolerance: 1-ulp libm
`atan2` drift in the unrounded `quad_loop_rate`; every occupancy integer,
FPT time, and ROI current field identical).

## Results

| Test | Statistic | Result |
|---|---|---|
| CTRL (pipeline validity) | k8 ROI plaquette circulation | +3.7e-4, sign 6/6, sign-flip p at floor; k0 quiet |
| OCC-1 (shift, center of mass) | 32v32 permutation | null, p=0.62 — the shift moves no mass centroid |
| OCC-2 (shift, per-bin max-\|t\|, 18 valid bins) | 10k permutations | **p=0.020** — shift real |
| CIRC-1/2 (circulation, global & ROI) | sign-flip + bootstrap CI, both arms | all null; online ROI −2.7e-5, CI [−2.3e-4, +1.7e-4] |
| CIRC-3 (online−frozen contrast) | 32v32 permutation | null, p=0.42 (global), p=0.82 (ROI) |
| EDGE-1 (per-edge net-flow contrast, 3180 edges) | max-\|z\| permutation | p=0.041 — investigated, see below |

**Shift localization (new).** The occupancy difference is a COM-invariant
*shape* change: online gains mass in the left-chamber interior
(x∈[0.5,1.0], t up to +3.3) and loses it on the wall-approach band
(x∈[1.5,1.83]) and the far-left edge. Total displaced mass ≈1%, matching the
original TV≈0.010. Interpretation (labeled as such): finite-M estimator
noise perturbs U_eff most where entropy gradients are steepest (mouth
approach) — a re-sculpted potential, which is the equilibrium story.

**EDGE-1 resolution.** The p=0.041 tripped my pre-declared escalation rule
and was run down post hoc: (i) neighborhood plaquette sums of the
online−frozen difference field around the max edge alternate sign
incoherently — no loop structure; (ii) top edges are dominated by sparse
multi-cell diagonal jumps (heavy-tailed rare events); (iii) once the
occupancy shift is real, the EDGE global null is strictly false anyway —
two nearby equilibria under one reset protocol must differ somewhere at
edge level. Classification: occupancy-shift signature, not a motor.
The online arm's one-sample circulation CI excludes a k8-control-sized
current outright.

## Verdict

**Match.** Shift real (p=0.020 here vs p=0.024 original, ~1% mass both),
current zero (circulation null both arms and contrast, at a validated
detection floor of ~2e-4 ROI circulation/step). The July 8 conclusion —
equilibrium difference, no probability current — is independently
corroborated by a different observable (directed transition counts) and a
different statistical pipeline. **No motor, real horizon** stands.

## Caveats & scope

- Scope matches the registered SCOPE line: reset-defined transport protocol,
  not a stationary closed-system NESS claim.
- Motors below the ~2e-4/step ROI circulation floor are not excluded
  (bounded null, same shape as registered G3).
- OCC-2 as first implemented had a NaN bug (zero-variance wall bins);
  fixed by valid-bin masking before unblinding. The uncorrected output is
  preserved in the run log for the record.

## Files

- `recompute_driver.py` — re-simulation + passive observer + bit-exact check
- `recompute_stats.py` — pre-declared statistics (plan in header)
- `recompute_followup.py` — OCC-2 fix + EDGE diagnostics (post hoc, labeled)
- `recompute_results.pkl` — per-unit transition counts, occupancy, flags

## Action item for deposit

The July 8 detailed-balance analysis artifact is not yet committed to this
repository (last commit predates it). It should land alongside this folder
before the DOI is minted, so the closing result and its independent
replication enter the archive together.
