# OC Simulation Report — v4.4 Scout Decision Rule v3.2 (frozen)

**Artifact:** `oc_simulation_v32.py` | **Results:** `oc_results_v32.json` | **Log:** `oc_run_v32.log`
**Interpreter:** `/usr/bin/python3`, numpy 2.0.2 | **RNG seed:** 20260707 (pin proposed in DECISION_RULE v3.2 §9.1)
**Trials:** 200,000 (S1, S2 — tail scenarios), 50,000 (S1b, S3, S4, S5)
**P1 modeled:** **TRUE** (STABLE is modeled from coupled per-seed draws, never hardcoded — the v3.2 requirement v3.1 failed)

## 1. Frozen rule implemented (exact)

All magnitudes in units of the cell's own block SD. floor(sd) = 3.858·sd·√(2/B) (0.5569 @ B=96, 0.4823 @ B=128); SE(sd,n) = sd·√(1/n+1/64) (0.2795 @ 16, 0.2165 @ 32); Student-t 1.753/2.131 (16b one/two-sided), 1.696/2.040 (32b); χ² upper-SD factors 1.437 (16b), 1.268 (32b). One-sided (registered σ, x = σ·μ̂): GREEN x − t·SE > floor; ANOMALOUS x < −t·SE (checked before RED); RED = ¬ANOM ∧ |μ̂|+t·SE(sd̂) < floor(sd̂) ∧ |μ̂|+t·SE(sd_up) < floor(sd_up) (the v3.2 magnitude belt); else AMBER. Two-sided (σ=None): same with two-sided t, |μ̂| GREEN, no ANOMALOUS. Ladder: 16b@B96 → (AMBER) 32b@B96 keeping the first 16 → (AMBER) same 32-block sample re-banded @B128 (§9.1 draw model) → (AMBER) INCONCLUSIVE_AT_CEILING. Pivot iff every cell RED and every direction-registered RED cell STABLE; GREEN→register, ANOMALOUS→investigate, INCONCLUSIVE→no pivot. v3.1 comparator: RED uses aligned x in place of |μ̂| (no magnitude bound).

## 2. P1 model (stated explicitly — do not skip)

- **P1-A registration:** σ_cell = sign of the cell's TRUE mean-field current. A truly-null cell has no sign → registers INDETERMINATE (σ=None), bands two-sided, STABLE vacuous for it. S2 overrides cell A's registration to +1 (wrong-sign registration). Sensitivity S1b models the alternative (nulls force-registered +1).
- **P1-B STABLE:** N=16 predeclared M=400 per-seed curls; each agrees with the TRUE current sign with p_true = 0.5 + 0.5·ρ·tanh(|μ_true|/noise_scale), noise_scale = floor(96)/0.4 = 1.3922 (receipt-07: single-M400-curl SNR ~0.3–0.5 for a floor-magnitude current; midpoint 0.4 ⇒ tanh(0.4)=0.380 at |μ|=floor). Agreement with the REGISTERED σ: p_true if signs match, 1−p_true if opposed, 0.5 if null. STABLE iff ≥12/16 agree with the registered σ. ρ ∈ {0.0, 0.3, 0.6, 0.9}; ρ=0 → STABLE ≈ chance (exact 0.03841), ρ→1 → follows truth (wrong-sign registration fails STABLE).

## 3. Partition completeness + boundary selftests

- **Completeness = 1.0** over 300,075 grid points (μ̂ ∈ [−5,5]×4001, sd̂ ∈ {0.25,0.5,1,2,4}, stages 1–3, σ ∈ {+1,−1,None}, both rules). No limbo, no double-band after precedence. **Gate 6a PASS.**
- **v3.2 raw predicates are fully disjoint (0 overlaps):** κ < t·SE at every stage, so ANOMALOUS and magnitude-RED can never co-fire. **v3.1 raw aligned-RED overlaps ANOMALOUS at 52,432 grid points** (x < −t·SE implies x < κ) — the precedence guard is what kept v3.1 coherent; that overlap region is exactly the wrong-sign mass v3.1 laundered into RED.
- Selftests all pass: wrong-sign-at-floor is NOT RED under v3.2 (it *is* raw-RED under v3.1); two-sided RED unreachable at 16b (κ_2s = −0.039), reachable at 32b (+0.115); mid-band cell stays AMBER through the ladder → INCONCLUSIVE_AT_CEILING.

## 4. S1 — global null (200,000 trials; nulls INDETERMINATE, two-sided)

| Quantity | Value |
|---|---|
| P(any-cell false GREEN) | **0.00214** (MC SE 2.3e-4) — gate ≤0.01 **PASS** |
| per-cell false GREEN | 0.000356 |
| **Pivot rate (correct pivot under null)** | **0.01208** |
| **Any-cell INCONCLUSIVE_AT_CEILING** | **0.98787** |
| Any ANOMALOUS | 0 (two-sided cells have no anomaly branch) |
| Per-cell terminal bands | RED 0.480, INCONCLUSIVE 0.519, GREEN 0.0004 |

**S1b sensitivity (nulls force-registered σ=+1, one-sided, 50,000 trials):** all-RED rate 0.1467 — reproducing the v3.2 doc's §13 expected operating point (~0.148, which was measured with STABLE forced True). With STABLE actually modeled at chance (0.0384/cell), **pivot-under-null = 0.0 at every ρ** (needs 6 simultaneous chance-STABLEs ≈ 3e-9). Per-cell terminal false-anomaly 0.0477, six-cell 0.2543 — matching the doc's advisory ~0.048/~0.254 (breaches the 0.20 soft cap, non-blocking, conservative direction, per §9.3). Pivot-under-null being near-unreachable when P1-B is genuinely modeled is an advisory observation ("low is legitimate" per §9.3), not a gate.

## 5. S2 — KEY: wrong-sign at floor (cell A μ_true = −0.5569, registered σ_A = +1; B..F null; 200,000 trials)

Cell A banding (shared block sample across rules): under **v3.2** — ANOMALOUS 0.872, RED 0.0329, INCONCLUSIVE 0.0952, GREEN 0; under **v3.1** — ANOMALOUS 0.612, RED **0.388**, INCONCLUSIVE ~0. (Doc §13 measured 0.033 / 0.386 / screen 0.61 — independent reproduction.) Nulls all-RED 0.0258.

**Invalid-pivot decomposition (THE load-bearing table).** belt = v3.2 RED |μ̂| bound; suspenders = modeled P1-B STABLE:

| ρ | (a) full v3.2 (belt+suspenders) | (b) belt only (STABLE≡True) | (c) suspenders only (v3.1 aligned-RED) | P(STABLE) wrong-sign cell, exact |
|---|---|---|---|---|
| 0.0 | 5.0e-05 (SE 1.6e-05) | 7.85e-04 | 4.15e-04 | 0.03841 |
| 0.3 | 1.0e-05 | 7.85e-04 | 1.15e-04 | 0.01292 |
| 0.6 | **0** (<1.5e-05, 95% UB) | 7.85e-04 | 4.5e-05 | 0.00346 |
| 0.9 | 0 (<1.5e-05) | 7.85e-04 | 0 (<1.5e-05) | 0.00069 |

Cell-A-only leakage (P(A RED ∧ STABLE), removing the null-cell suppression): v3.2 full 1.2e-3 → 1.1e-4 → 2e-5 across ρ 0→0.6→0.9; v3.1+STABLE 1.45e-2 → 1.4e-3 → 2.4e-4.

**Reading:** the **belt alone already meets the gate** (7.85e-04 ≤ 0.02, ρ-independent) — it is the layer that carries the guarantee at ρ=0, where suspenders are pure chance. The **suspenders alone also meet the gate** at every ρ (worst 4.15e-04 at ρ=0), but only because chance-STABLE (0.038) multiplies v3.1's large 0.388 RED leakage — at ρ=0 that protection is luck, not physics; it becomes real (≤4.5e-05) by ρ=0.6. **Together they are multiplicative:** full v3.2 is ~16× below belt-only at ρ=0 and hits measurable-zero by ρ=0.6. Gate 5 (≤0.02) **PASS** with two orders of magnitude of margin under the deployed rule at every coupling.

## 6. S3 — one cell aligned at floor (μ_A = +0.5569, σ_A = +1 correct; 50,000 trials)

Cell A: **extends past stage 1 in 91.5%** of trials, terminal INCONCLUSIVE_AT_CEILING **0.846**, GREEN 0.120, RED 0.034, ANOMALOUS 1e-4. Terminal stage distribution: 8.5% / 3.9% / 87.6% (stages 1/2/3). As designed: an at-floor aligned current mostly AMBERs and extends — the scout neither mints it GREEN nor buries it RED. Pivot rate ≤ 2.8e-4 at every ρ (blocked by A's non-RED plus modeled STABLE).

## 7. S4 — GREEN power (aligned; 50,000 trials each)

| Amplitude | P(GREEN, compound through ladder) | by stage (1/2/3) | law #2: planted signal breaks pivot |
|---|---|---|---|
| 2× floor (1.114) | 0.9161 (SE 1.2e-3) | 0.613 / 0.245 / 0.059 | 0.99998 |
| **3× floor (1.671)** | **0.99996** — gate ≥0.90 **PASS** | 0.979 / 0.021 / 0.0002 | 1.00000 |

Compound (whole-loop) power, not analytic per-contrast — per law #3.

## 8. S5 — Tc-heteroscedastic null (sd_true = 1 + 0.62·(k/4)², k=0..5 → ×1.62 at Tc4; 50,000 trials)

Any-cell false GREEN **0.00268** (≈ S1 level; gate ≤0.01 **PASS**), per-cell 0.00045, pivot 0.0128, inconclusive 0.987. Per-cell sd̂ banding neutralizes the Tc SD growth — **no false GREEN under heteroscedastic null.**

## 9. Hard gates

| Gate | Value | Threshold | Verdict |
|---|---|---|---|
| P(false GREEN \| null) — worst of S1/S1b/S5 | 0.00268 | ≤ 0.01 | **PASS** |
| P(invalid pivot \| wrong-sign at floor) — v3.2 full, worst over ρ | 5.0e-05 | ≤ 0.02 | **PASS** |
| GREEN power @ 3× floor (compound) | 0.99996 | ≥ 0.90 | **PASS** |
| Partition completeness | 1.0 | = 1.0 | **PASS** |

## 10. Observations (non-blocking)

1. **The coupled-upper RED clause never binds under the frozen constants.** Both clauses scale linearly in sd (SE and floor are both ∝ sd), so |μ̂| < sd_up·(floor_c − t·SE_c) is implied by the point-sd clause whenever floor_c − t·SE_c > 0, which holds at every operative stage (0.067 / 0.190 / 0.115). It is implemented exactly as frozen and verified inert on the partition grid; it functions as a no-op safeguard unless the constants change.
2. **Stage 3 (same-sample re-band at B=128, §9.1) can only add GREENs, never REDs or ANOMALOUS:** the lower floor loosens GREEN but tightens RED (κ shrinks 0.190→0.115 one-sided, 0.115→0.040 two-sided) on identical data, and the anomaly threshold is unchanged. Hence the high INCONCLUSIVE rates under null (per-cell 0.52 two-sided) — conservative, pivot-blocking.
3. **Six-cell terminal false-anomaly 0.254 (S1b, one-sided nulls)** breaches the 0.20 advisory soft cap exactly as the v3.2 doc predicts (§3 note, fork 9 — Anthony's ratification call). Conservative direction; never verdict-flipping.
4. **External consistency:** this independent implementation reproduces the DECISION_RULE v3.2 §13 session measurements to MC error (wrong-sign RED-banding 0.0329 vs 0.033; v3.1 0.388 vs 0.386; anomaly screen 0.61 at floor; S1b all-RED 0.147 vs ~0.148; false-anomaly 0.254 vs ~0.254).

## Verdict: **clean** — all four hard gates pass; P1 modeled; partition complete.
