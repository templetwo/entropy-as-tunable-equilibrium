# Receipt 06 — scale-10 diagnostics (HQ, 2026-07-07)

Three measured diagnostics run by HQ to convert ChatGPT's a-priori "M_grid ≥ 2000"
recommendation (and Fable's mean-suppression / T_c-self-defeat hypotheses) into
measured facts, at the **scout's real scale (10)** rather than a proxy. These are
**diagnostics, not scout results** — they run the equal-τ (1,1) chamber, not the
`v44pilot::` cells, and are NOT pooled into anything. Interpretation is in
`v44_scout_DECISION_RULE_v2_DRAFT.md` §4/§4.1.

## Method
- Interpreter `/usr/bin/python3` (Python 3.9.6, numpy 2.0.2). Harness `v44_scout.py`
  source_sha `0b65a9ee92b9fe2c` (frozen, unedited — imported as a module).
- Chamber: `run_chamber("frozen", 1.0, seed, scale=10.0, tau_y=1.0, M_grid_ov=M, Tc_ov=Tc, vortex_kappa=k)`.
- Seed namespace `diag10::` (throwaway, quarantined from `v44pilot::` and `v43::`).
- n = 20 blocks/arm. Bootstrap 90% CIs on SD ratios (4000 resamples, fixed rng=999).
- Six arms: A(k0,Tc1,M400) B(k0,Tc1,M2000) C(k0,Tc2,M400) D(k0,Tc4,M400) E(k4,Tc1,M400) F(k4,Tc1,M2000).

## DIAG 1 — SD-vs-M (is the detection floor estimator-limited at scale 10?)
Ratio SD@400 / SD@2000; ~1 => trajectory-limited (M won't lower floor), ~√5=2.24 => pure-grid.
- quad:  SD@400 5.03e-5, SD@2000 4.23e-5, ratio **1.19 [0.80, 1.74]**
- omega: SD@400 4.45e-5, SD@2000 5.13e-5, ratio **0.87 [0.61, 1.25]**
=> Floor is ~trajectory-limited even at scale 10. Raising M does not meaningfully lower it.
   (Refutes ChatGPT's stated "beat-the-floor" motivation, at the real scale.)

## DIAG 2 — SD-vs-Tc at M=400 (do the T_c cells self-defeat?)
Ratio of block SD to the Tc=1 arm; ~1 thermal-limited, growing => T_c-scaled grid-noise inflates the floor.
- quad:  Tc1 5.03e-5 | Tc2 6.27e-5 (r1.25 [0.91,1.82]) | Tc4 8.16e-5 (**r1.62 [1.15,2.39]**)
- omega: Tc1 4.45e-5 | Tc2 6.66e-5 (r1.50 [1.09,2.06]) | Tc4 8.90e-5 (**r2.00 [1.37,2.84]**)
=> Block SD grows with T_c (sub-linear). T_c cells partially self-defeating at M=400:
   the floor inflates ~1.6-2x by Tc=4, discounting the naive linear signal gain.

## DIAG 3 — κ-injection (does M=400 grid roughness suppress the realized mean?)
Increment = mean(k4) − mean(k0), equal-τ, at each M. Ratio incr@M400 / incr@M2000; <1 => M=400 suppresses transduction.
- quad:  incr@M400 +9.52e-5 (SE 1.6e-5), incr@M2000 +1.057e-4 (SE 1.6e-5), ratio **0.90** (~0.5σ; weak)
- omega: incr@M400 +9.80e-5 (SE 1.4e-5), incr@M2000 +1.462e-4 (SE 1.7e-5), ratio **0.67** (~2.2σ)
=> M=400 grid roughness suppresses the realized response to a KNOWN vortex, ~10% (quad) to ~33% (omega).
   This is the v4.2 "estimator roughness" mechanism; it is the failure mode that would fire the null
   branch falsely. It is the load-bearing reason to raise M (signal fidelity), NOT the floor (DIAG 1).

## Caveat
n=20/arm is scouting-grade: the SD ratios carry wide CIs, and the DIAG-3 omega
suppression (~2.2σ) is suggestive, not definitive. These size the effects and set
direction; they are not registration-grade measurements.
