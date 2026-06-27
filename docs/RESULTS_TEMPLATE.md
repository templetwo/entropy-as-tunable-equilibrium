# RESULTS

Copy to `RESULTS.md` at repo root and fill in as arms complete.

## Environment
- hardware:
- jax backend / device:
- seeds:
- wall-clock per arm:

## Phase 0 reproduction
- argmax migration:           (expect -3.7 -> ~0)
- mass-in-B:                  (expect 0.48 -> ~0.67)
- KL(engine||eq) range:       (expect ~0.75 - 1.16)
- reproduces Phase 0?  [ ] yes  [ ] no

## Arm A — conservativeness
- KL(driven||analytic):
- overlap:
- verdict:  [ ] PASS (analytic shortcut OK)   [ ] FAIL (driven fallback)

## Arm B — 2D crossover
- P_L control (fixed):
- P_L(tau) range:
- tau*:
- engine != control?  [ ] yes  [ ] no

## Arm C — discriminator  (MAKE-OR-BREAK)
- tau* per L_ch:
- fit  tau* = slope * L_ch^2/D :  slope =
- linear through origin?  [ ] yes  [ ] no
- VERDICT:  [ ] engine-entropy survives   [ ] FAILS (report honestly)

## Honest caveats
-
