# v4.4 Scout — Decision Rule v3.2 (re-pass-BLOCK-clearing revision of v3.1, for re-review + ratification)

*HQ (Mac Studio Claude Code seat, overwatch/provenance), 2026-07-07. **This is a DRAFT for re-review (ChatGPT methodology) + Antigravity re-audit + Anthony final-say. It is NOT registered, NOT chronicled, and edits NO harness bytes.** It revises `v44_scout_DECISION_RULE_v3.1.md` (a draft, not frozen) to clear the HQ diverse-lens re-pass BLOCK — three independent lenses converged on one defect in v3.1's RED rule. The frozen v4.3 artifacts, the `v44_scout.py` physics path, v3 (`v44_scout_DECISION_RULE_v3.md`, commit `138d109`), and v3.1 are **not modified** — this is a new file. Every ChatGPT Q1–Q7 disposition that v3.1 satisfied stays satisfied (§12); the re-pass repairs are keyed to a reconciliation table (§14). All numeric thresholds are grep-consistent (experimental law #4); every change from v3.1 is flagged inline. All §0 decisions remain revisable at re-review / audit / Anthony final-say.***

---

## ★ STANDING RULE (new in v3.2 — the recurring category error, stated once, load-bearing)

> **A null / RED claim must bound the effect MAGNITUDE, not merely the predicted-direction component.**
>
> "Absence of a predicted-direction signal" is **not** "evidence of absence of an effect." This is the same category error twice:
> - **On the compute-ceiling axis** (v3 → v3.1, ChatGPT Q4): an AMBER at the compute ceiling — a confidence interval that still overlaps the floor — was converted into `RED_AT_CEILING` and counted as a null. Repaired by `INCONCLUSIVE_AT_CEILING` blocking the pivot.
> - **On the wrong-sign axis** (v3.1 → v3.2, the re-pass BLOCK): a one-sided RED bounded only the sign-aligned component `x = σ·μ̂` and never bounded `|μ̂|`, so a **real opposite-direction current at floor magnitude** could satisfy "sub-floor in the predicted direction" and band RED, minting a null over a live effect. Repaired by the **RED magnitude bound** (§3) — RED requires `|μ̂| + t·SE < floor_c`, not merely `x + t·SE < floor_c`.
>
> Whenever a future rule declares a null, grep it against this sentence: does the RED/null condition bound `|μ̂|`, or only the aligned projection? If only the projection, it leaks on the wrong-sign axis.

---

## CHANGE SUMMARY — what v3.2 changes vs v3.1 (the re-pass BLOCK + six repairs)

| # | v3.1 state | v3.2 repair | § |
|---|---|---|---|
| **BLOCK (3 lenses)** | one-sided RED bounds only `x = σ·μ̂` (`x + t·SE < floor_c`); never bounds `\|μ̂\|`. A **real wrong-sign current at floor** bands RED ~39% (anomaly screen only ~61% power there) and the scout pivots to a NESS null over a live effect ~16% of runs — the Q4 absence→evidence-of-absence error relocated to the wrong-sign axis, blowing the rule's own safety gate. | **RED magnitude bound:** one-sided RED fires iff BOTH the v3.1 aligned coupled-upper conjunction (kept exactly) AND `\|μ̂\| + t·SE < floor_c(sd)` under the same point-and-coupled-upper conjunction. A wrong-sign super-floor current can no longer band RED (→ ANOMALOUS or AMBER, blocking the pivot). **Measured:** wrong-sign-at-floor invalid pivot **0.161 → 0.0066**; RED-banding of the wrong-sign cell **0.388 → 0.033**. HQ-verified leak 0.393 → 0.027 in the same direction. | §3, §3.3, §5, §7 |
| **Belt-and-suspenders** | STABLE hardcoded `True`; never measured; §5(ii) present but unexercised. | Wrong-sign protection is **belt (RED `\|μ̂\|` bound) + suspenders (STABLE / P1-B gate)**. v3.2 **declares** the OC sim (next phase) models P1-B STABLE from **coupled M=400 draws** (stated + sensitivity-tested coupling) and **measures** the JOINT protection. A cell counts toward the pivot only if STABLE (§5(ii)) **AND** its RED satisfies the magnitude bound (§3). | §1.1, §5, §9 |
| **Hard gate 5a mis-specified** | `P(wrong-sign ANOMALOUS) ≥ 0.90` was asked at −1×floor, where the anomaly **screen** achieves only ~0.61. | Guarantee **moved to the joint**: `P(invalid pivot \| ≥1 wrong-sign contrast at floor) ≤ 0.02` (and ≤0.005 at ≥2×floor) — symmetric with the predicted-direction S2 gate. The anomaly **screen** power is stated honestly as advisory (~0.61 at floor, ~0.90 at −1.45×floor); the magnitude bound + STABLE carry the guarantee, not the screen. | §9.3 |
| **Hard gate 5b impossible** | `P(pivot fired) == 0` under wrong-sign is mechanically unachievable (a finite tail always lands in RED). | Restated as `P(invalid pivot \| ≥1 real contrast at/above floor) ≤ 0.02` (≤0.005 at ≥2×floor). **This restatement is legitimate only because the magnitude bound actually fixes the leak** (0.161 → 0.0066), not as a way to dodge it. The acceptance scenario probes `\|current\|` **AT the floor**, never a weakened larger magnitude. | §9.3 |
| **Pivot-claim over-scope** | pivot claim read as "across the accessible design space" (a 3-parameter continuum). | Pivot bounds **raw mismatch currents sub-floor AT THE PROBED CONFIGURATIONS** — the six cells, which (receipt 07: A≡B and C≡D share the ROI mixed-partial to 4 s.f.) are **≈ 4 independent design points**. No coverage of interior/unprobed (τx, τy, Tc) is asserted. Matches v4.3's bounded-null-over-a-grid convention. | §2.1, §5, §10 |
| **Headline arithmetic** | "97.5% → 38%" mixed a per-cell rate with a joint rate. | Honest **joint-to-joint** shift: v3 six-cell joint pivot-under-null **0.808** (=0.965⁶) → v3.1 **0.349** → **v3.2 ≈ 0.148**. The per-cell 97.5% figure is dropped. | §11 fork 2, §13 |
| **False-anomaly arithmetic + minors** | spec used normal-approx 0.0251 per-cell / 0.141 six-cell; sim SE_FACTOR n=8 comment read 0.39528. | **Student-t₁₅:** the anomaly **screen at 16b** fires at **0.0344/cell** (not 0.0251). Under v3.2 the **terminal-through-ladder** rate rises to **≈0.048/cell**, six-cell **≈0.254** (strict 6-independent) — it **breaches the 0.20 soft cap**, stated honestly (non-blocking; §3 note). SE_FACTOR n=8 = **0.375** (not 0.39528) corrected for the next-phase OC sim. Two-sided INDETERMINATE RED is **unreachable at 16b/B96** (κ<0) — documented. | §3, §9.1, §14 |

**Kept from v3.1 unchanged (HQ-recommended-pending-Anthony):** Q1 option 2 (all-RED pivot = raw-current claim), the P1/P2 pins, B_max=128, 16-block first pass, τy-matched equal arm at matched Tc, the §3.3 coupled-upper Monte Carlo (Q3 PASS), the §4 `INCONCLUSIVE_AT_CEILING` ladder (Q4), the §8 anomaly state machine (Q2).

---

## 0. Identity + adopted decisions

### 0.1 Instrument identity (verify before any run — unchanged from v3.1)

| Anchor | Value |
|---|---|
| `version` | `v4h-1.4.0` |
| `config_hash` | `a344d6c47c8a22c1` (recomputed if any CFG block changes — §10) |
| `source_sha` | `0b65a9ee92b9fe2c` |
| `prereg_v44.json` sha256 | `b7c5aeb6bd21b70036f7fb6841f199fbf923aa984cba3d30a71943c75e9a2a2b` (re-issued if CFG changes — §10) |
| interpreter | `/usr/bin/python3` (Python 3.9.6, numpy 2.0.2 pinned) |

Detection floor, verified against `_detection_floor` (line 670) — a **two-arm** minimum-detectable-effect:

```
floor(B, sd) = (z_{0.995} + z_{0.90}) · sd · √(2/B) = 3.858 · sd · √(2/B)
```

| B | floor(B) = 3.858·sd·√(2/B) |
|---|---|
| 64  | 0.682·sd |
| 96  | **0.557·sd**  (adopted B_conf default) |
| 128 | 0.482·sd  (escalation ceiling B_max) |

### 0.2 Adopted decisions (all revisable at re-review / Anthony — unchanged from v3.1)

| # | Decision | Value | Rationale / coupling |
|---|---|---|---|
| D1 | Primary statistic | `quad_loop_rate` | Continuity with the v4.3 **G1 vortex-control calibration**. Rests on that continuity, **not** on the 2.2σ κ-suppression point estimate (§1.3). |
| D1′ | Secondary statistic | `omega_roi` (**descriptive only**) | Banded for information; **does not gate the pivot**. `occupancy_x` recorded, not banded. |
| D2 | First-pass blocks | **16** per cell | At 8 blocks RED is unreachable (κ<0, §3.3); 16 gives a usable first surface. (Q6-iv adopted.) |
| D3 | M_grid | **400** for geometric cells A/B/C/D, **GATED** on P1 sign-stability (§1.1). Tc cells AxT2/AxT4 **M frozen by P2 before the scout** (§1.2). | M does **not** lower the floor (DIAG 1); the M concern is grid-generated-signal fidelity, addressed by blocks/seed-averaging. |
| D4 | B_conf (floor projection) | **96** working default; escalation 96→128 ceiling for persistent AMBER (§4). | floor(96)=0.557·sd, floor(128)=0.482·sd. |
| D5 | Estimand | **Option (a)** — raw mismatch current as **screening/triage** statistic | μ̂ vs two-arm floor(B_conf); honest SE = sd·√(1/B_scout + 1/64). Restricts what (a) may claim (Q1): sizes a candidate signal and licenses a **raw-current** pivot only — **not** the mismatch-minus-equal contrast (§2.1, §5). |

### 0.3 Five couplings that must not drift apart (fifth added in v3.2)

1. **sign precondition ↔ per-cell predicted signs ↔ pivot license** — one chain (§1.1, §6.2, §5).
2. **estimand ↔ B_conf ↔ AMBER escalation ceiling** — share `floor_c` (§2, §4, §5).
3. **M_grid ↔ primary statistic** — one decision: quad@M400 (D1+D3; §1.3).
4. **claim class ↔ what was measured** (Q1/Q7) — a raw-current RED pivot is a raw-current claim; a contrast claim requires the equal arm; a Tc GREEN requires a measured two-sample contrast at confirmatory (§2.1, §5, §10).
5. **RED magnitude bound ↔ STABLE gate ↔ wrong-sign protection** (NEW, v3.2 re-pass) — the belt (`|μ̂|` bound, §3) and the suspenders (STABLE, §1.1/§5(ii)) are **one** wrong-sign guarantee, measured jointly by the OC sim (§9). Neither may be relaxed without re-measuring the joint invalid-pivot rate.

---

## 1. Precondition runs (gate the scout — complete and register BEFORE the scout)

These are **diagnostics, not scout results**. They run the mean-field / equal-τ rig in a declared, quarantined precondition namespace (`precond_P1::`, `precond_P2::`), **NEVER** pooled into `v44pilot::` or any confirmatory (experimental law #6). Their outputs are registered as part of the frozen prereg, because the scout's banding, pivot license, and claim class depend on them. **Both preconditions must terminate and register before the scout is licensed** (P2 finishes first, then the Tc-cell M and claim class are frozen — §1.2).

### 1.1 Precondition P1 — per-cell predicted signs + sign-stability (fully pinned — Q5-P1; v3.2 sharpens the pivot coupling)

The v3 spec carried an open ambiguity ("average-then-curl" vs "per-seed unanimity"). ChatGPT (Q5) required it killed before registration, because `stable_cell` gates the pivot (§5). v3.1 froze ChatGPT's pin; v3.2 keeps it verbatim and adds the belt-and-suspenders coupling (couple 5).

**P1-A — register the directional prediction σ_cell (the physical, mean-field object):**
- For each of the six cells, compute the **ROI-integrated curl of the seed-averaged mean aniso force field at M=4000** — **average-then-curl**: average the aniso force field over a predeclared high-M seed set into one mean field, then take the single ROI mixed-partial. One sign per cell.
- **σ_cell ∈ {+, −}** := sign of that high-M seed-averaged ROI curl. A cell with a high-M curl indistinguishable from 0 (below a predeclared negligibility floor) registers **σ_cell = INDETERMINATE** and bands **two-sided** (§3).
- **Predeclared high-M reference set (HQ proposal, revisable — fork §11):** average over **N_avg = 32** seeds `precond_P1::77001…77032` at **M=4000**. σ_cell = sign of the ROI curl of that averaged field.

**P1-B — the sign-stability robustness test (STABLE against a higher-resolution reference, not against itself):**
- Take a **separate, disjoint, predeclared seed set**, evaluate the ROI curl **per seed at M=400** (the scout's operating resolution).
- **STABLE iff ≥ 75% of those M=400 per-seed curls agree in sign with the registered high-M σ_cell.**
- **Predeclared robustness set + threshold (HQ proposal, revisable — fork §11):** **N = 16** seeds `precond_P1::78001…78016` at M=400; **STABLE iff ≥ 12/16** agree in sign with σ_cell.

**Consequence for the pivot (frozen):** a cell with **`stable_cell = UNSTABLE`** (< 12/16) **does not count toward the all-RED pivot** from an M=400 null (§5). It may only count after a **predeclared remedy** runs (r1 higher M per block, or r2 seed-averaged grids per block), following the amendment path (§8 step 4). No informal reclassification.

**Why STABLE is the *suspenders* of the wrong-sign protection (v3.2 — the belt-and-suspenders design):** the aniso current is *generated by* the grid curl (receipt 07). A **real opposite-direction current** — the exact object the RED magnitude bound (belt, §3) now blocks from banding RED — is also the object P1-B is built to catch: because P1-B's per-seed M=400 curls **share the underlying current** with the scout, a cell whose true current opposes its registered σ_cell will tend to fail the ≥12/16 agreement and register **UNSTABLE**, so §5(ii) excludes it from the pivot even in the residual fraction where the belt lets it band RED. **The two layers are one guarantee (couple 5):** belt = "a wrong-sign super-floor current cannot band RED"; suspenders = "even a residual wrong-sign RED sits on an UNSTABLE cell and is excluded." The OC sim (§9) **models P1-B STABLE from coupled M=400 draws that share the scout's underlying current** (with a stated, sensitivity-tested coupling) and **measures the joint** wrong-sign invalid-pivot rate — v3.1 hardcoded STABLE=True and could not see this second layer.

**Note (receipt 07, unchanged):** the quick per-seed SNR metric is *informative but not the instrument* — a single grid's ROI curl is noise-dominated at both M=400 and M=4000. Average-then-curl at high M establishes σ_cell; the per-seed check does not substitute for it.

### 1.2 Precondition P2 — crossed Tc×M diagnostic, operationalized as a GATE (Q5-P2 — unchanged from v3.1)

v3.2 keeps v3.1's P2 gate verbatim. Crossed `{Tc ∈ 1, 2, 4} × {M ∈ 400, 4000}` = **6 arms**, equal-τ, same rig as receipt 06 (DIAG 2). P2 **completes before the scout**; its output **freezes the Tc-cell M and claim class into the registered prereg**.

**Frozen estimator + sampling (HQ proposal, revisable — fork §11):**
- **n = 40 blocks/arm** (registration-grade).
- **SD estimator:** sample block-SD of the per-block primary statistic (`quad_loop_rate`), per arm.
- **Bootstrap:** percentile bootstrap, **10 000 resamples**, **rng pinned = 999**, **90% two-sided CI** on every ratio.

**M-sensitivity statistic.** `R(Tc) = SD(Tc, M=400) / SD(Tc, M=4000)`. R ≈ 1 ⇒ M-invariant → M=400 adequate. R > 1 ⇒ grid-noise contribution → M=400 inflates the floor.

**Frozen criteria (HQ proposal, revisable — fork §11):**
- **Material grid-noise contribution** ⇔ the **90% CI lower bound of R(Tc) > 1.10**.
- **M-invariant enough** ⇔ the **90% CI for R(Tc) lies entirely within [0.909, 1.10]** (TOST equivalence, ±10%).
- **Inconclusive** ⇔ neither.

**Action table (frozen — every branch predeclared):**

| P2 result for a Tc cell | Higher-M feasible? | Frozen action → registered into prereg |
|---|---|---|
| **M-invariant** (equivalence passes) | — | Tc cell runs at **M=400**; claim class = **full-sensitivity probe** (still subject to the Tc contrast refusal, §2.1). |
| **Material grid-noise** | yes | Tc cell runs at the **M that restores equivalence** (default M=4000); claim class = full-sensitivity probe. |
| **Material grid-noise** | no | Tc cell **demoted to DESCRIPTIVE**: banded for the record, **does not gate the pivot**; a Tc GREEN is candidate-only. |
| **Inconclusive** | — | **Bump n once** to **n = 80/arm** and re-test. Still inconclusive ⇒ **demote to DESCRIPTIVE**. |

**No pending state.** After P2 terminates, the Tc-cell M and claim class are **frozen constants** in the registered prereg.

### 1.3 Diagnostic language (frozen at n=20 reality — unchanged from v3.1)

- **Floor is trajectory-limited even at scale 10** (DIAG 1: SD@400/SD@2000 = 1.19 [0.80,1.74] quad, 0.87 [0.61,1.25] omega). Raising M does **not** lower the floor.
- **κ-injection suppression is NOT established:** quad ratio 0.90 (~0.5σ); omega ratio 0.67 (~2.2σ uncorrected p≈0.03, does **not** survive Holm across ~8 diagnostic contrasts). The quad-primary choice (D1) rests on v4.3 G1-calibration continuity.
- **Net relative sensitivity at M=400:** quad ≈ 0.90, omega ≈ 0.83 → quad wins at M=400 (couples D1↔D3).

---

## 2. Estimand + exact thresholds

### 2.1 Pinned estimand — option (a), a **screening/triage** statistic (Q1 licensing repair; v3.2 tightens the pivot scope)

μ̂ (per cell, per statistic) = the mean of the **raw mismatch current** over the scout blocks. It is a **screening proxy** that sizes a candidate signal. The honest SE folds in the v4.3 64-block equal-arm reference:

```
SE(B_scout) = sd_cell · √(1/B_scout + 1/64)
```

**Two distinct roles of "the equal arm" — do not conflate (auditor trip-wire, unchanged):**
1. **floor_c's SD source.** The scout runs **no equal arm**, so `floor_c` is projected from the cell's own measured block SD (`sd_cell`, n=B_scout) as a **homoscedastic proxy** for the confirmatory's equal-arm SD.
2. **The named equal-arm config (§6.1)** defines the **contrast estimand** and the confirmatory's second arm at Movement 3. Not used in the scout's floor arithmetic.

**Q1 — what estimand (a) may and may not claim (frozen):**
- A **GREEN** sizes a **candidate signal**; it triggers Movement-3 registration, and **Movement 3 is the independent two-sample contrast test**. A GREEN is candidate-selection, not a measured contrast (§10 claim limits).
- An **all-RED pivot** is restricted to a **RAW-CURRENT claim** (ChatGPT **option 2**, HQ-recommended-pending-Anthony): *"raw mismatch currents are sub-floor **at the probed configurations**."* **v3.2 scoping (re-pass fix 4):** the probed configurations are the **six cells**, which — because A≡B and C≡D share the ROI mixed-partial to 4 s.f. (receipt 07) — constitute **≈ four independent design points**, NOT a continuum. The pivot **does not** claim coverage of interior or unprobed (τx, τy, Tc) values. This matches v4.3's bounded-null-over-a-grid convention. It is explicitly **not** a contrast claim; the contrast test belongs to Movement 3.
- **Tc cells (Tc>1): estimand-(a) is REFUSED as contrast licensing (Q6-iii, frozen).** Any high-Tc GREEN requires a **measured two-sample contrast** (estimand (c)) at confirmatory.

> **Scope note (v3.2 — keep two "independences" apart).** "≈ four independent design points" above is a **claim-scope** statement about *physical* design-space coverage (the mixed-partial degeneracy A≡B, C≡D). It is **NOT** a statement about stochastic-noise independence. The OC-sim operating-characteristic rates (§9: pivot 0.148, false-anomaly 0.254) are computed with **independent per-cell block noise** — that independent-noise model is exactly what reproduces the receipt-06 anchors (§13). Do **not** apply the four-points degeneracy to soften any stochastic rate; whether the block noise is itself correlated across A≡B/C≡D is a separate OC-sim modelling decision (§9.1, flagged).

**Options for the contrast-licensing question (Anthony ratifies — fork §11).** HQ writes v3.2 around **option 2**. Options 1 (pre-scout equal-arm calibration gates at (1,1)@Tc1, (2,2)@Tc1, (2,2)@Tc2, (2,2)@Tc4 with a predeclared negligibility bound) and 3 (in-scout two-sample, ~2× compute) are documented as in v3.1 §2.1 and remain available. If Anthony picks 1 or 3, the raw-current restriction upgrades to a contrast claim and §6.1's equal arm becomes operative.

### 2.2 Frozen convention (law #4 grep-consistency — unchanged from v3.1)

One-sided **Student-t at (n−1) df, α=0.05** for GREEN/RED in the predicted direction; two-sided Student-t at (n−1) df, α=0.05 for INDETERMINATE-sign cells.

| df (n−1) | one-sided t (0.95) | two-sided t (0.975) |
|---|---|---|
| 7  (8 blocks)  | 1.895 | 2.365 |
| 15 (16 blocks) | **1.753** | **2.131** |
| 31 (32 blocks) | 1.696 | 2.040 |

### 2.3 Exact thresholds table (v3.2 adds the RED magnitude-bound column; all grep-consistent)

`floor_c` and `SE` are in units of the cell's own block SD, `sd_cell`. GREEN threshold on the aligned `x`: `floor_c + t·SE`. **v3.2 RED requires `|μ̂| < floor_c − t·SE = κ`** (point-governed where κ>0; §3.3 for the coupled-upper conjunction) — a **magnitude** bound, symmetric in μ̂.

| Config (blocks / B_conf) | floor_c | SE = sd·√(1/B+1/64) | **GREEN x >** (1-sided) | **GREEN \|μ̂\| >** (2-sided) | **RED \|μ̂\| < κ (v3.2 magnitude bound)** |
|---|---|---|---|---|---|
| **16 / 96  (OPERATIVE first pass)** | 0.557·sd | 0.2795·sd | **1.047·sd = 1.88× floor** | 1.153·sd = 2.07× floor | **0.067·sd** (one-sided κ) — two-sided κ = **−0.039 < 0 → RED unreachable** |
| 8 / 96   (legacy-block reference) | 0.557·sd | **0.3750·sd** | 1.267·sd = 2.28× floor | 1.444·sd | one-sided κ<0 → **unreachable** |
| 32 / 96  (AMBER block-extension) | 0.557·sd | 0.2165·sd | 0.924·sd = 1.66× floor | 0.998·sd | one-sided κ = **0.190·sd**; two-sided κ = **0.115·sd** (reachable) |
| 32 / 128 (AMBER B_conf escalation, ceiling) | 0.482·sd | 0.2165·sd | 0.849·sd = 1.76× floor | 0.924·sd | one-sided κ = **0.115·sd** |
| *8 / 64 (v2 legacy reference only)* | *0.682·sd* | *0.375·sd* | *1.393·sd = 2.04× floor* | *1.569·sd* | *unreachable (κ<0)* |

**Operative frozen GREEN for the primary (`quad_loop_rate`, 16 blocks, B_conf=96, one-sided): x = σ·μ̂ > 1.047·sd_cell (= 1.88× floor(96)).**
**Operative frozen RED (v3.2, 16 blocks, B_conf=96): `|μ̂| < 0.067·sd_cell`** (magnitude-bounded; point governs at κ>0).

> **Two-sided RED unreachability (v3.2 documentation — fix 6).** An INDETERMINATE-sign cell uses the two-sided t (2.131 at 16b), giving κ_2s(16/96) = 0.557 − 2.131·0.2795 = **−0.039 < 0**: an INDETERMINATE cell **can never band RED on the 16-block first pass** and must extend. Two-sided RED becomes reachable only at 32 blocks (κ_2s(32/96) = 0.557 − 2.040·0.2165 = **+0.115 > 0**, i.e. `|μ̂| < 0.115`). The v3.2 one-sided RED magnitude bound is the **same** `|μ̂|` test with the one-sided t (κ = +0.067 > 0, reachable at 16b) plus the ANOMALOUS carve-out — the one-sided and two-sided RED forms are now unified as magnitude bounds, differing only in t and the anomaly branch.

---

## 3. The four-band rule (exact inequalities — v3.2 adds the RED magnitude bound)

Banded on the **primary statistic** (`quad_loop_rate`) only; `omega_roi` gets the same arithmetic **descriptively** (does not gate the pivot). Let `t = t*(n−1 df)` per §2.2, `SE` per §2.1, `floor_c` per §2.3, σ_cell the registered predicted sign (P1). Terminal ceiling label **`INCONCLUSIVE_AT_CEILING`** (Q4).

**One-sided cells (σ_cell ∈ {+,−}).** Aligned statistic `x = σ_cell · μ̂` (`x > 0` = predicted direction).

- **GREEN** — register a confirmatory (candidate-selection, §10): `x − t·SE > floor_c`.
- **RED** — bounded sub-floor **in magnitude** (v3.2 repair; robust form §3.3): **BOTH** `x + t·SE < floor_c` (v3.1 aligned form, kept exactly) **AND** `|μ̂| + t·SE < floor_c` **AND** not ANOMALOUS.
- **ANOMALOUS** — a **significant** wrong-sign current; does **not** count toward the pivot; triggers the §8 state machine: `x < −t·SE` (significant against **0**, one-sided α=0.05).
- **AMBER** — none of the above; extend (§4).

> **The v3.2 RED repair, in one line.** Because `|μ̂| ≥ x` always, the magnitude conjunction `|μ̂| + t·SE < floor_c` **implies** the aligned conjunction `x + t·SE < floor_c`; the aligned form is kept explicitly (to preserve the Q3-PASS §3.3 verbatim and make the bounding transparent), but the **magnitude conjunction is what binds**. A wrong-sign current at floor magnitude has `|μ̂| ≈ floor_c`, so `|μ̂| + t·SE ≈ floor_c + t·SE > floor_c` — it **cannot** band RED (it goes ANOMALOUS if significant, else AMBER). This is the STANDING RULE enforced in the arithmetic.

**Partition (complete, no gap), one-sided:** with `κ = floor_c − t·SE > 0` at 16b/B96, RED = `|μ̂| < κ` (i.e. `μ̂ ∈ (−κ, κ)`); ANOMALOUS = `x < −t·SE` (i.e. `μ̂ < −t·SE` for σ=+1); GREEN = `x > floor_c + t·SE`; AMBER = the remainder. RED and ANOMALOUS are disjoint (RED requires `|μ̂| < κ < t·SE`, so `x > −κ > −t·SE`, never ANOMALOUS).

> **Finding-4 correction (Antigravity, retained).** ANOMALOUS keys on significance against **0** (`x < −t·SE`), not the floor magnitude. Together with the v3.2 magnitude bound, the wrong-sign axis is now covered by **two** disjoint mechanisms: significant wrong-sign → ANOMALOUS; small-but-real wrong-sign → excluded from RED by the `|μ̂|` bound (→ AMBER → ladder, where extra data at 32b tends to trip it ANOMALOUS or leave it INCONCLUSIVE).

> **Anomaly-rate arithmetic (v3.2 — Student-t₁₅, and the magnitude-bound consequence).** The honest SE = sd·√(1/16+1/64) = 0.2795·sd is conservative relative to μ̂'s true sampling SD = 0.25·sd, giving an effective ANOMALOUS z-threshold of 1.753·(0.2795/0.25) = 1.960; but the pivotal quantity is **t₁₅, not z** (sd̂ is estimated), so the **anomaly screen at 16b fires at P(t₁₅ < −1.96) ≈ 0.0344/cell** under a true null (the spec's normal-approx **0.0251 is superseded — fix 6**). **v3.2 raises the *terminal* rate:** the magnitude bound routes borderline wrong-sign null cells (`μ̂ ∈ (−t·SE, −κ)`, previously laundered into RED) through the AMBER ladder, where some trip ANOMALOUS at 32 blocks — so the **terminal per-cell false-anomaly rises to ≈ 0.048** (measured, §13). Six-cell, under the OC sim's **independent-noise** model: 1−(1−0.048)⁶ = **≈ 0.254**, which **exceeds the 0.20 soft cap**. This is reported honestly against the **standing 0.20 soft cap** (which it breaches) and is **non-blocking**: a false anomaly **blocks** the pivot (conservative) and routes to the §8 machine (higher-M rerun → GRID-ARTIFACT → re-band), it **never mints a wrong verdict**. Whether the *advisory* cap value should be widened (0.20 → 0.30) to reflect the magnitude bound's accepted reachability cost is a deferred **Anthony ratification call (§11 fork 9)** — **not** a threshold moved to fit the rule (the cap is advisory/non-blocking either way; the safety gates are §9.3's two invalid-pivot bounds, not this cap). **Do not** apply the §2.1 four-points degeneracy to reduce 0.254 to a smaller figure — that degeneracy is claim-scope, not noise-independence, and using it here would understate the cost (the exact v3.2 rate under a correlated-noise model is an OC-sim item, §9.1).

**Two-sided cells (σ_cell = INDETERMINATE from P1).** Use the two-sided `t`; ANOMALOUS does not apply (no predicted direction). RED is already a magnitude bound here (this is the form v3.2 generalizes to the one-sided case):
- **GREEN**: `|μ̂| − t·SE > floor_c`.
- **RED**: `|μ̂| + t·SE < floor_c` (robust form §3.3) — **unreachable at 16b/B96** (κ_2s<0; §2.3), reachable at 32b.
- **AMBER**: otherwise.

### 3.1 GREEN meaning
The scouting-grade sign-aligned lower confidence bound clears the confirmatory's minimum detectable effect. **A GREEN is candidate-selection** (§10): it names where to run the Movement-3 two-sample contrast; it is not itself a measured contrast.

### 3.2 ANOMALOUS meaning
A **significant** wrong-direction current is a grid-artifact / transduction-breakdown / sign-precondition signal, carved out of RED so it cannot launder into the null bucket. It triggers the frozen §8 state machine. Note (v3.2): the magnitude bound now also catches *sub-significance* wrong-sign currents at floor magnitude, which ANOMALOUS (a significance screen) misses — see §5 and the belt-and-suspenders design (§1.1).

### 3.3 RED robustness — v3.1 coupled-upper conjunction kept EXACTLY (Q3 PASS), v3.2 applies it to `|μ̂|` too

**The coupled-upper conjunction is unchanged from v3/v3.1 §3.3** (ChatGPT Q3 = PASS; Antigravity R2 reproduced the 4M-draw Monte Carlo). Reproduced in substance:

- v2's mental model was **coupled** (a single `sd` moving `floor_c` and `SE` together); upper-sd makes RED harder only while κ = floor_c − t·SE ≤ 0 (true at 8 blocks).
- At **16-block / B_conf=96**, **κ = +0.067·sd > 0**, so a **floor-only** upper-sd read makes RED **easier**, driving the false-null rate for an at-floor effect from 3.9% (point-sd) to 18.9% (floor-only upper-sd) — anti-conservative, unacceptable.

**Frozen RED rule (v3.2 — the aligned conjunction, kept exactly, AND the magnitude conjunction, added):**
```
RED  ⇔  ( x   + t·SE(sd̂)      < floor_c(sd̂)      )  AND  ( x   + t·SE(sd_upper) < floor_c(sd_upper) )   # aligned (v3.1, verbatim)
   AND  ( |μ̂| + t·SE(sd̂)      < floor_c(sd̂)      )  AND  ( |μ̂| + t·SE(sd_upper) < floor_c(sd_upper) )   # magnitude (v3.2, NEW)
   AND  ( NOT ANOMALOUS )
```
Each conjunction selects the harder ceiling. `sd_upper = sd̂ · √((n−1)/χ²_{0.05,n−1})`, factors **1.797 (n=8), 1.437 (n=16), 1.268 (n=32)**. The §3.3 Monte Carlo (4×10⁶ draws, Δ = floor(96), operative config, `/usr/bin/python3` numpy 2.0.2) that validated the **aligned** conjunction is unchanged (point-sd 3.95%, floor-only upper-sd 18.86%, coupled-upper 4.93%, conjunction 3.95%; Antigravity R2 reproduced 3.951% / 18.860% / 4.933% / 3.951%). The **magnitude** conjunction inherits the same coupled-upper conservatism; its whole-loop effect is measured by the OC sim (§9), not by this local MC.

**Operative RED (16b/B96): `|μ̂| < 0.067·sd_cell`** (magnitude bound; point governs at κ>0).

> **Q3 documentation caveats (retained from v3.1 — scope the warrant):**
> 1. **The Monte Carlo validates LOCAL false-null behavior only; it does NOT validate the six-cell loop.** The whole-loop validation is the OC simulation (§9) with predeclared acceptance criteria.
> 2. **The Monte Carlo assumes `sd_cell` is a reasonable proxy for the equal-arm SD.** Under option 2 this is a stated assumption bounding only the raw-current claim; under option 1/3 it is measured.

---

## 4. AMBER terminal rule + B_conf escalation → INCONCLUSIVE_AT_CEILING (Q4 — unchanged from v3.1)

A cell may not sit in AMBER forever. The terminal ladder, per AMBER cell, in order:

1. **One block-extension: 16 → 32 blocks.** SE shrinks 0.2795·sd → 0.2165·sd; re-band against floor(96). **The 32-block sample CONTAINS the 16-block first pass** (accumulation, not an independent redraw) — preserved in the OC simulation (§9).
2. **Still AMBER against floor(96) at 32 blocks → escalate B_conf 96 → 128.** floor_c drops 0.557·sd → 0.482·sd; a persistent AMBER may resolve **GREEN** against the larger confirmatory.
3. **Still AMBER against floor(128) at 32 blocks → `INCONCLUSIVE_AT_CEILING`.** B_max = 128 is the declared compute ceiling.

**Q4 repair (retained).** `INCONCLUSIVE_AT_CEILING` **BLOCKS the pivot** (it is not RED/GREEN/ANOMALOUS). An AMBER at the ceiling means the CI still overlaps the floor — the cell is **unresolved at the authorized compute**, not bounded below it. A scientifically legitimate outcome, not a null.

> **v3.2 interaction (stated).** The magnitude bound shifts mass from RED into AMBER at 16b (a wrong-sign or near-zero-magnitude cell that v3.1 called RED now extends), so **more cells reach the ladder and terminate INCONCLUSIVE** (per-cell INCONCLUSIVE 0.126 → 0.225, §13). This is the intended, honest direction: unresolved magnitude → INCONCLUSIVE, never a minted null.

---

## 5. The pivot rule — four honest terminal outcomes (Q4) + raw-current claim (Q1) + magnitude+STABLE gate (v3.2)

The scout ends in exactly one of **four** honest terminal outcomes:

1. **GREEN candidate** — ≥1 cell GREEN → **register the Movement-3 two-sample contrast** at the tie-break cell (do not pivot). Candidate-selection, §10.
2. **All-actual-RED pivot** — pivots to the closed no-reset NESS protocol **iff all pivot conditions below hold**. The claim is a **RAW-CURRENT claim** (Q1 option 2): *"raw mismatch currents are sub-floor at the probed configurations (the six cells ≈ four independent design points),"* **not** a contrast claim and **not** a continuum claim (§2.1).
3. **ANOMALOUS → investigate** — ≥1 cell ANOMALOUS → run the §8 state machine; **no pivot and no terminal-null decision while an anomaly is open**.
4. **INCONCLUSIVE at compute ceiling** — ≥1 cell `INCONCLUSIVE_AT_CEILING` (and no GREEN/ANOMALOUS forcing outcomes) → the scout **halts with a legitimate bound**. **This is not a null and not a failure.** It blocks the pivot.

**Pivot conditions for outcome 2 (ALL must hold):**
- **(0) No open anomaly (blocks the pivot):** **no** cell is ANOMALOUS. A cell leaves ANOMALOUS **only** through the §8 state machine.
- **(0′) No open inconclusive (blocks the pivot — Q4):** **no** cell is `INCONCLUSIVE_AT_CEILING`.
- **(i) Terminal-band condition:** at least one cell was banded, and **every** cell is **actual RED** (§3, §4) — and every counted RED satisfies the **v3.2 magnitude bound** (`|μ̂| < κ`; this is intrinsic to a RED band under §3, stated here for emphasis: **the belt**). Given (0) and (0′), "every cell" excludes ANOMALOUS and INCONCLUSIVE — no vacuous set, no ceiling-minted null.
- **(ii) Instrument precondition (the suspenders):** **`stable_cell` = STABLE** (P1, §1.1) for **every** cell whose RED is counted. An UNSTABLE RED at M=400 does not license the pivot until its predeclared remedy runs.

**Belt-and-suspenders (v3.2 — the re-pass fix, couple 5).** A cell may count toward the all-RED pivot **only if** it is **STABLE (§5(ii))** *AND* its RED satisfies the **magnitude bound (§3)**. Belt = the magnitude bound refuses a wrong-sign super-floor current a RED band; suspenders = STABLE excludes the residual wrong-sign RED that lands on an instrument-unstable cell. **Measured joint protection (§13):** wrong-sign-at-floor invalid pivot falls **0.161 (v3.1) → 0.0066 (belt alone) → ~0 (belt + suspenders)**, and now **matches** the predicted-direction rate (S2: 0.0067) — the directionality asymmetry that triggered the re-pass block is gone.

**In words:** a raw-current null (pivot) is earned only when **no cell showed a significant wrong-sign current** (ANOMALOUS guard), **no cell showed a sub-significance real wrong-sign current at floor magnitude** (the `|μ̂|` bound refuses it a RED), **no cell was left unresolved at the compute ceiling**, the six probed cells are confidently sub-floor **in raw mismatch-current magnitude**, and the instrument was demonstrably reading a **stable-sign** signal everywhere it called RED. The scout still "cannot fail": candidate, or bounded raw-current at the probed points with a stable instrument, or a named anomaly, or an honest compute-ceiling bound.

**Upgrading the pivot to a contrast claim** requires the baseline/equal-arm condition (option 1/3 or Movement 3). Under option 2 the scout does not upgrade; Movement 3 does.

**GREEN tie-break (outcome 1):** if several cells are GREEN, the registration cell is the one with the highest `x − t·SE` margin above `floor_c` on the primary. A Tc-cell GREEN is a **drive-amplitude** registration **requiring a measured two-sample contrast** (§2.1); a geometric-cell GREEN is a **Δτ** registration.

---

## 6. Per-cell configuration tables (unchanged from v3.1)

### 6.1 Equal-arm config per candidate cell (Q6-i adopted — τy-matched at matched Tc, conditional on Q1)

**Adopted: τy-matched equal arm** — the equal-τ config at the cell's **larger horizon** τy, at the **same Tc**. Rationale (receipt-07): the ROI mixed-partial of the small-τx grid is ≈ 0, so the curl and its block-SD noise are carried by the larger-horizon τy grid; the τy-matched arm is the closest noise-match. Matched-Tc is **non-optional** for the Tc cells (DIAG 2). Under option 2 this config defines only the Movement-3 second arm.

| Cell | (τx, τy) | Tc | Role | Equal-arm config (τy-matched, matched-Tc) |
|---|---|---|---|---|
| A    | (0.1, 2.0)  | 1 | widest horizon mismatch | (2.0, 2.0) @ Tc=1 |
| B    | (0.25, 2.0) | 1 | mismatch mid            | (2.0, 2.0) @ Tc=1 |
| C    | (0.1, 1.0)  | 1 | amplitude-only          | (1.0, 1.0) @ Tc=1 |
| D    | (0.25, 1.0) | 1 | replica bridge to v4.3  | (1.0, 1.0) @ Tc=1 |
| AxT2 | (0.1, 2.0)  | 2 | Tc sweep at widest pair | (2.0, 2.0) @ Tc=2 |
| AxT4 | (0.1, 2.0)  | 4 | Tc sweep at widest pair | (2.0, 2.0) @ Tc=4 |

**Design-space degeneracy (re-pass fix 4 — anchors the pivot scope).** A and B (both τy=2.0, Tc=1) and C and D (both τy=1.0, Tc=1) share the ROI mixed-partial to 4 s.f. (receipt 07): the small-τx grid contributes ≈0 curl, so within each pair the curl is set by the common τy grid. The six cells therefore probe **≈ four independent design points** {(τy=2,Tc=1), (τy=1,Tc=1), (τy=2,Tc=2), (τy=2,Tc=4)}. The all-RED pivot's raw-current claim is bounded to **these probed points**, matching v4.3's bounded-null-over-a-grid convention — not to the (τx,τy,Tc) interior.

**Reviewer alternatives (fork §11):** (τx,τx)-matched, or a dual-reference design.

### 6.2 Predicted-sign table (all TBD until P1 registers — unchanged from v3.1)

| Cell | (τx, τy, Tc) | Registered σ_cell | Banding |
|---|---|---|---|
| A    | (0.1, 2.0, 1) | **TBD by P1** (receipt-07 quick check leaned `+`, inconclusive) | one-sided if σ∈{+,−}, else two-sided |
| B    | (0.25, 2.0, 1) | **TBD by P1** | one-sided if σ∈{+,−}, else two-sided |
| C    | (0.1, 1.0, 1) | **TBD by P1** (leaned `+`, inconclusive) | one-sided if σ∈{+,−}, else two-sided |
| D    | (0.25, 1.0, 1) | **TBD by P1** (v4.3 arm1 τx<τy ⇒ `+`, re-derive per cell) | one-sided if σ∈{+,−}, else two-sided |
| AxT2 | (0.1, 2.0, 2) | **TBD by P1** | one-sided if σ∈{+,−}, else two-sided |
| AxT4 | (0.1, 2.0, 4) | **TBD by P1** | one-sided if σ∈{+,−}, else two-sided |

An INDETERMINATE cell moves GREEN to the two-sided column (16b/B96: 1.153·sd vs one-sided 1.047·sd) and **cannot band RED until 32 blocks** (κ_2s<0 at 16b; §2.3).

---

## 7. `band_cell()` + `pivot_licensed()` pseudocode (v3.2 — magnitude bound added to RED)

Reference implementation for the additive functions in `analyze()`. Pure analysis; touches no harness physics. All arithmetic in units of `sd_cell`.

```python
def band_cell(mu_hat, sd_cell, n_blocks, B_conf, sigma_cell, stable_cell):
    """
    Band one scout cell on the PRIMARY statistic (quad_loop_rate).
    Returns (band, aligned_bound, floor_c), band in {GREEN, AMBER, RED, ANOMALOUS}.
    INCONCLUSIVE_AT_CEILING is set by the caller's terminal ladder (sec 4).
    sigma_cell in {+1, -1, None}; None => two-sided (P1 INDETERMINATE).
    stable_cell in {True, False} (P1 sign-stability); consumed at the pivot.
    """
    Z = 3.858                                   # z_{0.995} + z_{0.90}, verified
    df = n_blocks - 1
    two_sided = (sigma_cell is None)
    t = t_student(df, one_sided=not two_sided, alpha=0.05)   # sec 2.2 table

    def floor_c(sd):  return Z * sd * sqrt(2.0 / B_conf)      # sec 0.1
    def SE(sd):       return sd * sqrt(1.0/n_blocks + 1.0/64) # estimand (a), sec 2.1

    sd_up = sd_cell * chi2_upper_factor(df)     # sqrt((n-1)/chi2_{0.05,n-1}); sec 3.3

    x = abs(mu_hat) if two_sided else sigma_cell * mu_hat     # prediction-aligned

    # GREEN: sign-aligned lower CB clears the confirmatory floor (candidate-selection)
    if x - t * SE(sd_cell) > floor_c(sd_cell):
        return ("GREEN", x - t*SE(sd_cell), floor_c(sd_cell))

    # ANOMALOUS: SIGNIFICANT wrong-sign excursion (one-sided cells only) -> not RED;
    #            keyed on significance against 0 (Finding 4); triggers sec 8 state machine.
    if (not two_sided) and (x < -t * SE(sd_cell)):
        return ("ANOMALOUS", x - t*SE(sd_cell), floor_c(sd_cell))

    # RED (v3.2): aligned coupled-upper conjunction (v3.1, kept) AND the MAGNITUDE
    #             coupled-upper conjunction on |mu_hat| (NEW -- bounds the wrong-sign axis).
    #             |mu_hat| >= x, so the magnitude pair implies the aligned pair; both are
    #             written to preserve the Q3-PASS form and make the bound explicit.
    aligned = (x        + t*SE(sd_cell) < floor_c(sd_cell)) and \
              (x        + t*SE(sd_up)   < floor_c(sd_up))
    magnitude = (abs(mu_hat) + t*SE(sd_cell) < floor_c(sd_cell)) and \
                (abs(mu_hat) + t*SE(sd_up)   < floor_c(sd_up))
    if aligned and magnitude:
        return ("RED", abs(mu_hat) + t*SE(sd_cell), floor_c(sd_cell))

    return ("AMBER", x + t*SE(sd_cell), floor_c(sd_cell))


def pivot_licensed(cell_bands, stable_flags):
    """Sec 5: pivot to closed no-reset NESS (RAW-CURRENT claim) iff ALL hold.
    Guarded against vacuous truth, compute-ceiling-minted null, AND wrong-sign
    magnitude leak (the magnitude leak is closed inside band_cell's RED: a RED
    band already implies |mu_hat| < kappa -- the BELT; STABLE is the SUSPENDERS)."""
    if any(b == "ANOMALOUS" for b in cell_bands.values()):
        return False                             # (0) resolve via sec 8 first
    if any(b == "INCONCLUSIVE_AT_CEILING" for b in cell_bands.values()):
        return False                             # (0') no ceiling-minted absence
    if not cell_bands:
        return False                             # nothing to bound the space
    if any(b == "GREEN" for b in cell_bands.values()):
        return False                             # register at the GREEN cell instead
    if not all(b == "RED" for b in cell_bands.values()):
        return False                             # AMBER cells -> run sec 4 ladder first
    # (ii) SUSPENDERS: every counted RED must be on a STABLE cell
    if not all(stable_flags[c] for c, b in cell_bands.items() if b == "RED"):
        return False                             # UNSTABLE RED at M=400 does not license
    return True
```

`omega_roi` (secondary, D1′) runs through the same `band_cell()` for the record but its band is **descriptive** — excluded from `pivot_licensed`.

**Key diff from v3.1 pseudocode:** `band_cell`'s RED now requires the **magnitude** coupled-upper conjunction on `|mu_hat|` in addition to the aligned one. That single change is the re-pass repair in code; `pivot_licensed` is byte-identical to v3.1 (the belt lives inside `band_cell`; the suspenders is §5(ii), unchanged).

---

## 8. Anomaly-resolution state machine (Q2 — frozen, unchanged from v3.1)

*(Verbatim from v3.1 §8 — the frozen state machine, discriminator, disposition table, amendment rule, and selftest requirement are unchanged. Reproduced here for completeness of the standalone document.)*

**Trigger.** A cell bands ANOMALOUS (§3, `x < −t·SE`). The pivot is blocked (condition (0)) until this machine terminates the cell in one of {GRID-ARTIFACT re-banded, TRUE-OPPOSITE-PHYSICS, SIGN-PRECONDITION-FAILURE excluded, UNRESOLVED}.

```
STATE A (entry): cell is ANOMALOUS at M=400.
  --> Rerun at the predeclared higher-M / seed-averaged-grid recipe (the SAME remedy
      declared for that cell in P1; sec 1.1 r1/r2), in precond namespace.
STATE B (rerun result):
  - Wrong-sign significance VANISHES at higher M --> GRID-ARTIFACT. Re-band under the
    higher-M recipe (a predeclared recipe supersede via the sec 8-step-4 amendment path).
  - Wrong-sign significance PERSISTS at higher M --> STATE C.
STATE C (persistent dynamical wrong-sign): compare to P1's registered high-M sigma_cell,
         re-examine sigma_cell's high-M reference robustness:
  - Persistent sign OPPOSES sigma_cell AND sigma_cell's high-M reference is robust
    (P1-B still >= 12/16) --> TRUE-OPPOSITE-PHYSICS. NOT a null; escalate to a Movement-3
    two-sample contrast in the OBSERVED direction. Never counts toward an all-RED pivot.
  - Re-examination shows sigma_cell was mis-registered --> SIGN-PRECONDITION-FAILURE.
    Cell EXCLUDED from the pivot; P1 re-run only via a formal amendment.
STATE D (higher-M infeasible OR B/C inconclusive) --> UNRESOLVED. Cell blocks the pivot
         indefinitely; scout terminates in outcome 3 with the anomaly named.
```

| Classification | Disposition | Counts toward pivot? |
|---|---|---|
| GRID-ARTIFACT | re-band under higher-M recipe (amendment) | yes, at the re-banded higher-M result |
| TRUE-OPPOSITE-PHYSICS | Movement-3 contrast in observed direction | **no** |
| SIGN-PRECONDITION-FAILURE | cell excluded; P1 re-run only via amendment | **no** (until amended prereg) |
| UNRESOLVED | scout halts in outcome 3, anomaly named | **no** |

**Step 4 — amendment rule (frozen).** Any change to a cell's resolution, M, seed recipe, or σ_cell registration requires a **formal preregistration amendment**: regenerate the config, record the new `config_hash` + `source_sha` + prereg sha256, verify readback, **then** run (law #1). Corrections **supersede**, never erase (law #9). No informal "investigate and re-band" path.

**Selftest requirement (law #2).** The anomaly gate must demonstrably **fire** on a planted wrong-sign artifact and **block** the pivot — asserted in the OC simulation (§9, scenario S5).

> **v3.2 note — the anomaly machine is the *suspenders' backstop*, not the belt.** The re-pass block proved the anomaly **screen** cannot be the sole wrong-sign guarantee (it has only ~0.61 power at floor). v3.2's guarantee is the magnitude bound + STABLE; the §8 machine is what *dispositions* the anomalies that do fire (including the extra terminal anomalies the magnitude bound routes into the ladder). Its selftest (S5) now checks **joint** protection, not standalone screen power (§9.3).

---

## 9. OC SIMULATION SPECIFICATION (Q4/Q7; the next build phase implements this — v3.2 REQUIRES P1 modeling + corrected acceptance)

ChatGPT (Q4) required the selftest operate on the **entire frozen state machine**, not per-contrast power, with **predeclared acceptance criteria**. This section is that specification, updated for the v3.2 magnitude bound and the belt-and-suspenders guarantee. It is registered as part of the prereg (§10) and **must run and pass before the scout is licensed** (after P1/P2, before the scout). *The v3.1 OC sim (`oc_simulation_v31.py`) and its report are the prior-phase artifacts that surfaced the re-pass block; the v3.2 OC sim is a **new** artifact implementing this §9.*

**Why joint + full-loop is non-optional (law #3).** Analytic per-contrast power lies under a multi-look ladder (v4.3: 0.998 analytic vs 0.655 compound). The acceptance criteria are **compound / whole-loop** operating characteristics, all six cells simulated jointly.

### 9.1 Simulation model (implementable — v3.2 additions in **bold**)

- **Null-SD calibration (receipt 06).** Per-block SD of `quad_loop_rate`: Tc1 = 5.03e-5, Tc2 = 6.29e-5 (×1.25), Tc4 = 8.15e-5 (×1.62). Band arithmetic is scale-free in `sd_cell`; SDs enter only the Tc-heteroscedastic and equal-arm-offset scenarios.
- **Draw model.** For a cell with true contrast Δ (in `sd_cell` units): each block statistic ~ N(Δ, 1); μ̂₁₆ = mean of the first 16 draws; the 32-block extension **reuses those 16 and appends 16 new** (accumulation dependence preserved). sd̂ from the sample SD; `sd_upper` from the χ² factor. B96→B128 re-bands the **same 32-block** sample.
- **`band_cell` with the v3.2 magnitude bound.** RED requires the aligned **and** the magnitude coupled-upper conjunctions (§3, §7). The **SE_FACTOR n=8 constant is 0.375** (= √(1/8+1/64)); the v3.1 sim comment read `0.39528` (= √(1/8+1/32)) — **a stale comment to correct in the v3.2 sim** (law #4). Values used were already 0.375; only the comment string is wrong.
- **P1 modeling (NEW — v3.2 REQUIRES this; v3.1 hardcoded STABLE=True):** the sim must model, per cell,
  (a) **σ_cell registration** (one-sided vs two-sided assignment) from P1-A; and
  (b) **STABLE from N=16 coupled M=400 per-seed curls that SHARE the cell's underlying current with the scout.** Concretely: draw the 16 P1-B per-seed curls from a distribution whose sign-agreement-with-σ_cell is **coupled to the same true contrast Δ** driving the scout blocks (a wrong-sign true current ⇒ fewer than 12/16 agree ⇒ UNSTABLE). Declare the coupling explicitly (**HQ proposal:** per-seed curl ~ N(Δ_curl, σ_curl²) with Δ_curl = ρ·Δ mapped to the sign-agreement probability, ρ a stated coupling constant) and **sensitivity-test ρ** over a predeclared range (e.g. ρ ∈ {0.5, 1.0, 2.0}) so the joint protection is not an artifact of one coupling value.
- **STABLE-then-pivot.** `pivot_licensed` consumes the modeled STABLE flags (not an all-True vector), so the OC sim measures the **joint** wrong-sign protection (belt + suspenders), which v3.1 could not.
- **Correlated-noise question (flagged, not assumed).** The §2.1 four-points degeneracy is claim-scope; the baseline OC sim draws **independent** per-cell block noise (reproduces the receipt-06 anchors). Whether to additionally model **correlated block noise across A≡B / C≡D** is a predeclared sensitivity item — it would move both the joint pivot rate and the six-cell false-anomaly rate and must be **measured**, not asserted.
- **Trials + rng.** ≥ 1×10⁵ per scenario (≥ 1×10⁶ for the false-GREEN / invalid-pivot / wrong-sign tail estimates), rng pinned (proposal `seed = 20260707`), `/usr/bin/python3` numpy 2.0.2. Report Monte Carlo standard errors on every rate.

### 9.2 Scenarios (all six cells simulated jointly — v3.2 sharpens S5)

| # | Scenario | Construction |
|---|---|---|
| S1 | **Global null** | all six cells Δ = 0, Tc-calibrated SDs. Measures: false-GREEN, false-anomaly (terminal, t₁₅), joint pivot-under-null. |
| S2 | **One-cell predicted-direction at floor** | one cell Δ = +floor(96) = +0.557; rest null. Measures P(invalid pivot) — the predicted-direction safety gate. |
| S3 | **One-cell supra-floor sweep** | one cell Δ ∈ {+1×, +2×, +3×} floor; rest null. Compound GREEN power + supra-floor invalid pivot. |
| S4 | **Multi-signal / GREEN tie-break** | ≥2 supra-floor cells → forces multiple GREENs so the tie-break resolves. |
| **S5** | **Wrong-sign current AT FLOOR (v3.2 — the re-pass scenario)** | one cell **Δ = −1×floor** (a real opposite-direction current at the two-arm MDE, **the exact magnitude the block probes — NOT a weakened larger artifact**); rest null. The wrong-sign cell's **STABLE is modeled from coupled P1-B draws** (it tends UNSTABLE). Measures the **joint** invalid-pivot rate (belt + suspenders). **Sub-cases:** −1×, **−1.45×** (anomaly-screen 0.90-power point), **−2×** floor. |
| S6 | **Tc-heteroscedastic** | Tc cells at receipt-06 SD scaling; tests that per-cell `sd_cell` banding neutralizes Tc growth. |
| S7 | **Nonzero equal-arm offset** | inject μ_eq ∈ {0.10, 0.30}·floor → sizes how a real offset perturbs the raw-current pivot (the Q1 raw-vs-contrast gap). |

### 9.3 Predeclared acceptance criteria (v3.2 — hard gates 5a/5b restated; HQ-recommended, pending Anthony)

**Hard gates (registration blocked if violated) — the safety criteria:**

| # | Criterion | Scenario | Tolerance (HQ-rec) | Expected (measured this session, §13) |
|---|---|---|---|---|
| 1 | **P(any false GREEN)** | S1 global null | ≤ 0.01 | ~0.002 |
| 2 | **P(invalid pivot) — predicted-direction at floor** | S2 (Δ=+floor) | ≤ 0.02 | **0.0067** |
| 3a | P(invalid pivot) — predicted-direction 2× floor | S3 (+2×) | ≤ 0.005 | ~3×10⁻⁶ |
| 3b | P(invalid pivot) — predicted-direction 3× floor | S3 (+3×) | ≤ 0.005 | ~0 |
| 4 | **P(registrable GREEN)** compound power | S3 (+3× floor) | ≥ 0.90 | ~1.00 |
| **5** | **P(invalid pivot) — WRONG-SIGN at floor** *(replaces v3.1 5a/5b)* | S5 (Δ=−floor), STABLE coupled | **≤ 0.02** | **0.0066 (belt)**, ~0 (belt+suspenders) |
| **5′** | **P(invalid pivot) — WRONG-SIGN ≥2× floor** | S5 (Δ=−2×floor) | **≤ 0.005** | ~3×10⁻⁶ |
| 6a | Partition completeness (no limbo) | S1–S7 | = 0 | 0 |
| 6b | Zero cells terminate AMBER (deadlock) | S1–S7 | = 0 | 0 |
| 7 | law #2 — planted +3× signal breaks pivot (cell non-RED) | S3 (+3×) | ≥ 0.90 | ~1.00 |

> **Why 5/5′ replace v3.1's 5a/5b (re-pass fix 3 — legitimate restatement, not a dodge).**
> - **v3.1 5a** demanded `P(wrong-sign ANOMALOUS) ≥ 0.90` at −1×floor. The anomaly **screen** (one-sided α=0.05 against 0) has power only **~0.61** at floor (~0.90 at −1.45×floor) — the criterion **could not be met by the scenario it was attached to**. v3.2 does **not** put the guarantee on the screen; it puts it on the **joint** invalid-pivot rate (gate 5), symmetric with the predicted-direction gate 2. The screen power is reported honestly as advisory (below).
> - **v3.1 5b** demanded `P(pivot) == 0`, which is mechanically impossible (a finite tail always lands in RED). v3.2 restates it as `P(invalid pivot | wrong-sign at floor) ≤ 0.02` (≤0.005 at ≥2×). **This restatement is legitimate only because the magnitude bound actually closes the leak** (measured 0.161 → 0.0066 at floor; 0.386 → 0.033 wrong-sign RED-banding) — it is NOT the v3.1-OC-report dodge (which tried to *normalize* the S5 failure by redefining the scenario to a weaker −1.79× artifact; **that was refused**). Gate 5 probes `|current|` **AT the floor**, the exact magnitude the block resolves.

**Reported / advisory operating characteristics (informative, NOT hard-gated):**

| Characteristic | Scenario | Advisory | Expected (§13) |
|---|---|---|---|
| **P(correct pivot)** | S1 calibrated null | advisory (low is legitimate) | **~0.148** (v3.2 operating point; §11 fork 2) |
| **P(≥1 INCONCLUSIVE_AT_CEILING)** | S1 | report | higher than v3.1 (per-cell 0.126→0.225) |
| **P(≥1 false anomaly)** | S1 | **advisory — non-blocking**; 0.254 breaches the **standing 0.20** cap (false anomalies are conservative: pivot-blocking, never verdict-flipping); cap value 0.20-vs-0.30 is an Anthony call (fork 9) | ~0.254 (6-indep, terminal t₁₅) |
| **anomaly-SCREEN power (standalone)** | S5 | report — this is the WEAK layer, not the guarantee | **~0.61 at −floor, ~0.90 at −1.45×floor** |
| **anomaly TERMINAL rate through the ladder** | S5 | report (favorable side effect, not relied upon) | ~0.87 at −floor, ~0.99 at −1.45×floor |
| **P(correct tie-break \| ≥2 GREEN)** | S4 | advisory ≥0.90 (separated slate) | tie-break exercised only by S4 |
| **raw-vs-contrast gap** | S7 | report pivot/GREEN shift vs offset | sizes the Q1 gap |

**Interpretation of the split.** Only the **safety** criteria (false GREEN, invalid pivot in **both** directions, partition, compound power, law-#2 failability) are hard gates. **P(correct pivot | null) is deliberately advisory** and now **~0.148** — the magnitude bound (belt) further suppresses RED under null on top of the Q4 INCONCLUSIVE repair; hard-gating a high pivot rate would pressure the design back toward minting absence. The load-bearing gates are the **two symmetric invalid-pivot bounds** (gate 2 predicted-direction, gate 5 wrong-sign) — both measured at ~0.0066.

### 9.4 Boundary / cutpoint selftests (Q7 item 7 — v3.2 adds the magnitude-bound cutpoints)

Deterministic assertions on `band_cell()`/`pivot_licensed()`:

- **Equality at each cutpoint** — μ̂ exactly at `floor_c ± t·SE`, at `floor_c`, and **at ±κ (the magnitude-RED edge, both signs)** resolve to the predeclared side.
- **Magnitude-bound wrong-sign check (NEW)** — μ̂ = −floor_c (a wrong-sign-at-floor current, σ=+1) must **NOT** band RED (it must be ANOMALOUS or AMBER); μ̂ = −(κ+ε) must not band RED; μ̂ = −(κ−ε) at a value that is not ANOMALOUS must band RED (magnitude within κ, both signs symmetric).
- **One-sided vs two-sided branch** — two-sided RED unreachable at 16b (κ_2s<0), reachable at 32b.
- **Wrong-sign anomaly boundary** — μ̂ = −t·SE flips ANOMALOUS exactly at the significance edge; RED and ANOMALOUS never co-fire (κ < t·SE).
- **SD-upper factors per block count** — 1.797 / 1.437 / 1.268; the RED conjunction selects the harder ceiling.
- **Empty / anomaly-only / inconclusive-only pivot guard** — all False.
- **Terminal-ceiling behavior** — a cell held AMBER through the ladder emits `INCONCLUSIVE_AT_CEILING`, blocks the pivot, never RED.
- **UNSTABLE-RED blocks the pivot (suspenders)** — `pivot_licensed([RED]*6, [True]*5+[False])` = False.

---

## 10. Scope of changes if ratified (→ config_hash / prereg re-issue) — Q7

| Artifact | Change | Hash impact |
|---|---|---|
| `SCOUT_DECLARATION.md` decision-rule section | Replaced by §1–§8 of this document | none (declaration) |
| `analyze()` in `v44_scout.py` | Add `band_cell()` (**with the v3.2 magnitude-bound RED**) + `pivot_licensed()` (§7) with `INCONCLUSIVE_AT_CEILING` — additive, does not touch the v4.3-inherited estimator or forward physics | new `source_sha` |
| `CFG["scout"]["blocks"]` | 8 → **16** (D2) | **new `config_hash` → re-issue prereg → new sha256** |
| B_conf convention | 64 → **96** (D4) | new `config_hash` if surfaced in CFG; else declaration-only |
| **P1 config** (§1.1) | high-M reference (N_avg=32@M4000), robustness (N=16@M400), ≥12/16 STABLE, per-cell remedy | part of config_hash / prereg |
| **P2 config** (§1.2) | Tc∈{1,2,4}×M∈{400,4000}, n=40/arm, bootstrap (10000, rng999, 90%CI), R-ratio criteria, action table | part of config_hash / prereg |
| **Anomaly SOP** (§8) | frozen state machine + amendment rule | part of prereg |
| **OC simulation script + expected-OC report** (§9) | **new v3.2 simulator** (magnitude-bound RED, **P1/STABLE coupled modeling**, corrected 5/5′ acceptance) | part of prereg (new artifact) |
| **Baseline / equal-arm conditions** (§2.1, §6.1) | Q1 option chosen (default option 2) + licensing conditions | part of prereg |
| **Stale-prose flag (law #4):** comments hard-coding "B=64 floor", the sim's `0.39528` SE_FACTOR n=8 comment, and any per-cell-97.5%-as-joint prose | Update to B_conf=96/128, SE_FACTOR n=8 = **0.375**, and the honest joint headline (§13); the selftest grep-check must grep the operative t-convention, B_conf, `INCONCLUSIVE_AT_CEILING`, P1/P2 thresholds, **and the RED magnitude-bound `|μ̂| < κ` form** | part of config_hash / prereg |

**Claim limits (Q7 item 8 — frozen, v3.2-scoped):**
- **A GREEN is candidate-selection**, not a measured contrast, until the Movement-3 two-sample contrast runs.
- **A raw-current RED is not automatically a contrast RED** — only under the baseline/equal-arm condition (option 1/3 or Movement 3).
- **The all-RED pivot (option 2) claims raw mismatch currents are sub-floor AT THE PROBED CONFIGURATIONS** (the six cells ≈ four independent design points; §2.1, §6.1) — **not** across the (τx,τy,Tc) continuum, and **not** the tunable contrast.
- **A Tc>1 GREEN requires a measured two-sample contrast** at confirmatory.

**Unchanged and hash-frozen:** the forward-path harness (`pilot_pair`, Tc threading, the v4.3-inherited estimator), the six cells + geometry, the `v44pilot::` seed namespace, the never-pooled rule. This is an **analysis + declaration recalibration**, not a physics-instrument edit. Re-issue per law #1: regenerate `prereg_v44.json` from `--plan`, record new `config_hash` + `source_sha` + prereg sha256, verify readback, **then** run — **P1 and P2 first, OC simulation (v3.2) passes, scout last.**

---

## 11. Ratification checklist + genuine forks left for Anthony

**Resolved into spec.** Every ChatGPT BLOCK/AMEND (Q1–Q7) and the HQ re-pass BLOCK have a frozen repair above (§12, §14).

**Genuine forks — HQ recommends, Anthony ratifies:**

1. **Q1 contrast-licensing option.** HQ writes v3.2 around **option 2** (all-RED pivot = raw-current claim only, scoped to the probed points). Options 1 and 3 documented and available. **HQ rec: option 2.**
2. **The operating point (the headline consequence — v3.2 restated honestly).** Two honest repairs stack: the Q4 `INCONCLUSIVE_AT_CEILING` repair and the v3.2 RED magnitude bound. **Joint-to-joint** pivot-under-null: v3 (ceiling counted as RED) **0.808** = 0.965⁶ → v3.1 (INCONCLUSIVE blocks) **0.349** → **v3.2 (magnitude bound) ≈ 0.148**. The per-cell "97.5%" figure is dropped (it mixed a per-cell rate with a joint rate). **Fork:** accept the ~0.15-pivot / high-INCONCLUSIVE operating point, OR raise B_max / add seed-averaged-grids-per-block to resolve more cells. **HQ rec: accept it** — the magnitude bound buys wrong-sign safety (invalid pivot 0.161→0.0066); the lower reachability and the false-anomaly rise to ~0.25 (6-indep) are the honest, conservative (pivot-blocking, never verdict-flipping) price. (The advisory false-anomaly cap value — keep the standing 0.20 or widen to 0.30 to reflect this price — is a separate Anthony call, fork 9; it is non-blocking either way.)
3. **P1 seed sets + threshold + coupling.** HQ proposes N_avg=32 (77001–77032@M4000) for σ_cell, N=16 robustness (78001–78016@M400), STABLE ≥12/16, **and the OC-sim STABLE↔Δ coupling ρ (sensitivity ρ∈{0.5,1,2})**. Revisable.
4. **P2 estimator + criteria.** As v3.1 (Tc∈{1,2,4}, n=40/arm→80, bootstrap 10000/rng999/90%CI, material-grid ⇔ R CI-lower>1.10, equivalence [0.909,1.10]). Revisable.
5. **OC acceptance tolerances (§9.3).** HQ proposes false-GREEN ≤0.01, **invalid-pivot ≤0.02 (floor, BOTH directions) / ≤0.005 (≥2× floor)**, compound GREEN power ≥0.90 at 3×, correct-pivot advisory, anomaly soft cap ≤0.30. Revisable.
6. **Equal-arm choice (§6.1).** τy-matched at matched-Tc (Q6-i). Alternatives: (τx,τx)-matched or dual-reference.
7. **B_max = 128** (Q6-ii) — revisable; couples to Movement-3 compute budget.
8. **Correlated block-noise across A≡B / C≡D (NEW fork).** Baseline OC sim uses independent per-cell noise (reproduces anchors). Whether to model correlated noise — which would move both the joint pivot and the six-cell false-anomaly rate — is a sensitivity item HQ recommends **measuring** in the v3.2 OC sim before freezing the six-cell rates. **Framed neutrally:** the A≡B/C≡D degeneracy is in the *mean* prediction; whether the *block noise* is also shared is not obvious (blocks are plausibly separate trajectory ensembles → independent noise, in which case 0.254 stands). This is a **measure-it** item, **not** a rescue for the false-anomaly cap. Revisable.
9. **Advisory false-anomaly cap value (NEW fork).** v3.2's terminal six-cell false-anomaly (~0.254) breaches the standing **0.20** soft cap. The cap is **advisory / non-blocking** (a false anomaly blocks the pivot, never flips a verdict). **Fork:** keep the standing 0.20 and record the breach as the accepted reachability cost, OR widen the cap to **0.30** to reflect that cost. **HQ rec: keep 0.20 and record the breach** — leaving the acceptance table's stated threshold un-moved is the re-pass-cleaner optic; the safety guarantees are §9.3's two invalid-pivot bounds, not this advisory cap. Anthony's call either way.

---

## 12. ChatGPT Q1–Q7 reconciliation (all v3.1 satisfactions PRESERVED in v3.2)

| ChatGPT Q | v3.1 resolution | v3.2 status |
|---|---|---|
| **Q1** — contrast-proxy estimand | raw-current claim (option 2); estimand-(a) refused for Tc>1; GREEN=candidate-selection | **preserved + tightened:** pivot claim scoped to the probed configurations (≈4 independent design points), not a continuum (§2.1, §5, §10) |
| **Q2** — four-band / ANOMALOUS | frozen anomaly state machine; false-anomaly corrected off the nominal 5% | **preserved + corrected to Student-t₁₅:** screen 0.0344/cell; terminal (v3.2) ~0.048; §8 machine unchanged |
| **Q3** — RED conjunction / MC | coupled-upper conjunction kept exactly; 4M-draw MC | **preserved verbatim; the same coupled-upper form now also applied to `|μ̂|`** (§3.3) — the aligned MC is unchanged |
| **Q4** — sequential loop / pivot | `INCONCLUSIVE_AT_CEILING` blocks the pivot; four honest outcomes | **preserved;** the STANDING RULE names Q4 as the compute-ceiling instance of the same category error the v3.2 magnitude bound fixes on the wrong-sign axis |
| **Q5-P1** | high-M seed-averaged σ_cell; STABLE ≥12/16 vs high-M ref | **preserved + operationalized in the OC sim:** STABLE now modeled from coupled M=400 draws (the suspenders), not hardcoded True (§1.1, §9.1) |
| **Q5-P2** | fully operationalized gate; P2 before the scout | **preserved verbatim** (§1.2) |
| **Q6** — open leans | τy-matched equal arm; B_max=128; refuse Tc>1 estimand-(a); 16 blocks; P1 pin | **preserved** (§1.1, §4, §6.1) |
| **Q7** — re-issue scope / claim limits | claim limits stated; prereg scope expanded; boundary selftests | **preserved + expanded:** magnitude-bound cutpoint selftests added; grep extended to the `|μ̂|<κ` form (§9.4, §10) |

---

## 13. v3.2 measured operating characteristics (this session — analytic full-loop check; the v3.2 OC sim is the registration-grade instrument)

*Measured with a throwaway full-loop simulation of the v3.2 rule (`/usr/bin/python3`, numpy 2.0.2, base seed matched to the v3.1 sim, 1×10⁶ tail trials). It reproduces the v3.1 anchors exactly, then measures the v3.2 magnitude-bound rule. **This is an HQ arithmetic check, not the registration OC sim** — §9 specifies the registration-grade instrument (which adds the coupled STABLE modeling this check approximates by hardcoding the belt-alone and belt+suspenders bounds).*

**Anchor reproduction (v3.1 rule) — confirms the check is calibrated:**

| Quantity | v3.1 OC report | this check |
|---|---|---|
| per-cell terminal RED (null) | 0.839 | **0.839** |
| per-cell INCONCLUSIVE (null) | 0.126 | **0.126** |
| per-cell ANOMALOUS (null) | 0.0346 | **0.0345** |
| joint P(pivot \| null) | 0.349 | **0.349** |
| wrong-sign-at-floor: cell RED | 0.386 | **0.388** |
| wrong-sign-at-floor: invalid pivot | 0.160 | **0.161** |

**v3.2 rule (magnitude-bounded RED):**

| Quantity | v3.1 | **v3.2** |
|---|---|---|
| single-pass 16b RED (null) | 0.570 | **0.207** |
| per-cell terminal RED (null) | 0.839 | **0.727** |
| per-cell terminal INCONCLUSIVE (null) | 0.126 | **0.225** |
| per-cell terminal ANOMALOUS (null) | 0.0345 | **0.048** |
| **joint P(pivot \| null)** | 0.349 | **0.148** |
| six-cell false-anomaly (6-indep) | 0.190 | **0.254** |

**Wrong-sign protection (the re-pass fix — cell 0 at −Δ, other five null):**

| Δ (wrong sign) | metric | v3.1 (aligned RED) | v3.2 belt (magnitude RED) | v3.2 belt+suspenders (cell UNSTABLE)* |
|---|---|---|---|---|
| −1× floor | cell bands RED | 0.388 | **0.033** | 0.033 |
| −1× floor | terminal ANOMALOUS | 0.612 | 0.873 | 0.873 |
| −1× floor | **P(invalid pivot)** | **0.161** | **0.0066** | **~0** |
| −2× floor | cell bands RED | — | 2×10⁻⁵ | 2×10⁻⁵ |
| −2× floor | terminal ANOMALOUS | — | 1.000 | 1.000 |
| −2× floor | **P(invalid pivot)** | — | **3×10⁻⁶** | **0** |

*\*belt+suspenders here hardcodes the wrong-sign cell UNSTABLE as an illustration; the registration OC sim (§9.1) **models** STABLE from coupled P1-B draws and measures this jointly with a sensitivity-tested coupling.*

*The post-fix wrong-sign RED-banding reads **0.033** in this HQ check vs HQ's own **0.027** — a small difference in the residual `|μ̂|∈(−κ,κ)` tail attributable to modelling detail (the ladder's 16→32 accumulation and whether the coupled-upper conjunction binds on the magnitude leg at 32b). It does not affect gate-clearance: the invalid-pivot rate is **0.0066 ≤ 0.02** in either accounting, and the registration OC sim (§9) is the number of record.*

**Symmetry restored (both at floor magnitude):** predicted-direction invalid pivot (S2, +floor) = **0.0067**; wrong-sign invalid pivot (S5, −floor, belt) = **0.0066**. The directionality asymmetry that triggered the re-pass block is gone; both clear the ≤0.02 gate.

**Anomaly-screen honesty:** the standalone one-sided α=0.05 screen has power **0.61 at −floor**, **~0.90 at −1.45×floor** — too weak to be the guarantee (the v3.1 error). The magnitude bound routing borderline cells into the ladder raises the **terminal** anomaly rate to 0.87 at floor (a favorable side effect, not relied upon).

---

## 14. v3.1 re-pass reconciliation (HQ diverse-lens BLOCK → v3.2 disposition)

| Re-pass finding | Severity | v3.2 disposition | § |
|---|---|---|---|
| **RED bounds only `x=σμ̂`, never `|μ̂|`; wrong-sign-at-floor bands RED ~39% → invalid pivot ~16%** | **BLOCKER (3 lenses)** | **RED magnitude bound:** aligned conjunction (kept) AND `|μ̂|+t·SE<floor_c` coupled-upper conjunction. Measured invalid pivot 0.161→0.0066; RED-banding 0.388→0.033. STANDING RULE added. | §3, §3.3, §5, §7, STANDING RULE |
| **STABLE hardcoded, never measured; wrong-sign protection is single-layer** | **BLOCKER (belt-and-suspenders)** | belt (magnitude bound) + suspenders (STABLE); OC sim **models STABLE from coupled M=400 draws**, stated+sensitivity-tested coupling, measures the joint rate; §5(ii) + magnitude both required to count a RED. | §1.1, §5, §9.1, couple 5 |
| **Hard gate 5a (`P(wrong-sign ANOMALOUS)≥0.90`) mis-specified at −floor (only ~0.61 achievable)** | **BLOCKER (mis-spec gate)** | guarantee moved to the joint `P(invalid pivot | wrong-sign at floor) ≤ 0.02`; screen power reported honestly as advisory (0.61 / 0.90 at −1.45×). | §9.3 gate 5, advisory row |
| **Hard gate 5b (`P(pivot)==0`) mechanically impossible** | **major** | restated `P(invalid pivot | ≥1 real contrast at/above floor) ≤ 0.02` (≤0.005 at ≥2×), probing `|current|` AT the floor — legitimate because the belt closes the leak, not a scenario-weakening dodge (the v3.1-OC-report normalization is refused). | §9.3 gate 5/5′ |
| **Pivot claim over-scoped as a (τx,τy,Tc) continuum** | **major (inferential)** | scoped to "raw currents sub-floor at the probed configurations"; A≡B, C≡D share the mixed-partial to 4 s.f. ⇒ ≈4 independent design points; matches v4.3 bounded-null-over-a-grid. | §2.1, §5, §6.1, §10 |
| **Headline "97.5%→38%" mixes a per-cell rate with a joint rate** | **major (arithmetic)** | honest joint-to-joint: v3 0.808 (=0.965⁶) → v3.1 0.349 → v3.2 0.148; per-cell 97.5% dropped. | §11 fork 2, §13 |
| **False-anomaly normal-approx 0.0251/0.141; sim SE_FACTOR n=8 comment 0.39528; two-sided RED reachability unstated** | **minor (arithmetic, law #4)** | Student-t₁₅ screen **0.0344**/cell, terminal (v3.2) **~0.048**, six-cell **~0.254** (breaches the standing 0.20 soft cap — non-blocking; cap value 0.20-vs-0.30 deferred to Anthony, fork 9); SE_FACTOR n=8 = **0.375**; two-sided RED **unreachable at 16b/B96 (κ<0)** documented. | §3 note, §2.3, §9.1, §9.3 |

**Note on internal consistency (law #4).** All *stochastic* operating-characteristic rates in this document (joint pivot 0.148, six-cell false-anomaly 0.254) use the **independent per-cell block-noise** model that reproduces the receipt-06 anchors. The "≈4 independent design points" (§2.1, §6.1) is a **claim-scope** statement about physical design-space coverage (the A≡B/C≡D mixed-partial degeneracy) and is **never** applied to soften a stochastic rate — doing so would understate the false-anomaly cost. Whether the block noise is itself correlated across A≡B/C≡D is a flagged OC-sim sensitivity item (fork 8).

---

## 15. Antigravity re-audit target (carried from v3.1 §13, updated)

Antigravity R2 audited v3 and returned "RATIFIABLE AS-IS" but **normalized the then-invalid Q4 `RED_AT_CEILING`** (it did not independently catch the Q4 conversion ChatGPT blocked). v3.1 fixed Q4; **the HQ diverse-lens re-pass then caught the wrong-sign RED leak that neither ChatGPT nor Antigravity R2 flagged** — the mirror-image category error. v3.2 fixes it.

**Re-audit target for the next Antigravity pass (v3.2):**
1. The **RED magnitude bound** (§3, §7) — verify `|μ̂|+t·SE<floor_c` is applied under the coupled-upper conjunction and that wrong-sign-at-floor cannot band RED (independently re-derive 0.161→0.0066).
2. The **belt-and-suspenders** modeling (§9.1) — verify the OC sim's coupled STABLE draws and the ρ sensitivity, and that belt-alone already clears the ≤0.02 gate.
3. The **restated hard gates 5/5′** (§9.3) — verify they are not a scenario-weakening dodge (the acceptance scenario probes `|current|` AT the floor).
4. The **honest joint-to-joint headline** (0.808→0.349→0.148) and the **t₁₅ false-anomaly** rise to ~0.254, reported against the **standing 0.20** cap (non-blocking; cap value deferred to Anthony, fork 9).
5. The **claim-scope vs noise-independence** separation (§2.1 scope note, §14 note) — verify no stochastic rate was softened by the four-points degeneracy.
6. The **two-sided RED unreachability at 16b** and the **SE_FACTOR n=8 = 0.375** correction.

---

*End v3.2 draft. Status: DRAFT for ChatGPT re-review + Antigravity re-audit + Anthony final-say. Not registered, not chronicled, no harness bytes edited. v3 (`138d109`), v3.1, and `v44_scout.py` (`source_sha 0b65a9ee92b9fe2c`) remain unmodified. The registration-grade v3.2 OC simulation (§9) is the next build phase.*
