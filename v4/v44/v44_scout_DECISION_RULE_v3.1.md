# v4.4 Scout — Decision Rule v3.1 (BLOCK-clearing revision of v3, for re-review + ratification)

*HQ (Mac Studio Claude Code seat, overwatch/provenance), 2026-07-07. **This is a DRAFT for re-review (ChatGPT methodology) + Antigravity re-audit + Anthony final-say. It is NOT registered, NOT chronicled, and edits NO harness bytes.** It revises `v44_scout_DECISION_RULE_v3.md` (hash-frozen; never edited) to clear the ChatGPT v3 methodology BLOCK captured in `REVIEW_VERDICT_CHATGPT_v3.md`. HQ upheld that block. Every repair below is keyed to a ChatGPT disposition (Q1–Q7); the mapping is §12.*

*The frozen v4.3 artifacts and the `v44_scout.py` physics path stay hash-frozen. v3 (`v44_scout_DECISION_RULE_v3.md`, commit `138d109`) is hash-frozen and is not modified — this is a new file. All numeric thresholds are grep-consistent with v3 except where a repair changes them, and every such change is flagged inline. All §0 decisions remain **revisable at re-review / audit / Anthony final-say.***

---

## CHANGE SUMMARY — what v3.1 changes vs v3 (per ChatGPT Q1–Q7)

| Q | v3 state | v3.1 repair | §  |
|---|---|---|---|
| **Q1** | all-RED pivot made a **contrast** claim ("space bounded sub-floor") on a proxy measured only at (1,1)@Tc1 | all-RED pivot restricted to a **RAW-CURRENT** claim (ChatGPT option 2, HQ-recommended-pending-Anthony); options 1 & 3 documented; estimand-(a) **refused** as contrast licensing for Tc>1 | §2.1, §5, §10 |
| **Q2** | "may be re-banded out of ANOMALOUS after investigation" (open-ended) | frozen **anomaly-resolution state machine** with a predeclared 3-way discriminator; any recipe change = formal prereg amendment; false-anomaly rate corrected **~26% → ~14.1%** (planning approx, independence) | §8, §3 |
| **Q3** | RED conjunction + local MC — PASS | **kept exactly** as v3 §3.3; added the two documentation caveats ChatGPT named | §3.3 |
| **Q4** | terminal AMBER→`RED_AT_CEILING`, counts toward pivot (invalid conversion) | replaced by `INCONCLUSIVE_AT_CEILING` that **BLOCKS** the pivot; scout has **four** honest terminal outcomes | §3, §4, §5 |
| **Q5-P1** | average-then-curl vs per-seed-unanimity **ambiguous**; stability against itself | frozen pin: σ_cell from ROI curl of **high-res seed-averaged mean field @M=4000**; STABLE iff **≥12/16** predeclared M=400 per-seed curls agree in sign **with σ_cell**; failing cells excluded until a predeclared remedy runs | §1.1 |
| **Q5-P2** | "M-invariant" / "pending" — no gate | fully operationalized **gate**: sample size, SD estimator + bootstrap, M-sensitivity ratio, material-grid-noise criterion, equivalence margin, **action table**, inconclusive branch; **P2 completes before the scout**, then Tc M-choice + claim class frozen | §1.2 |
| **Q6** | leans listed | leans **adopted** (all revisable at Anthony): τy-matched equal arm at matched Tc (conditional on Q1); B_max=128 but terminal AMBER stays inconclusive; refuse estimand-(a) contrast for Tc>1; first-pass 16 blocks; P1 pin | §1.1, §4, §6.1 |
| **Q7** | re-issue scope = band_cell/blocks/B_conf | added **claim limits** + expanded prereg scope (OC sim script, expected-OC report, P1/P2 config, anomaly SOP, baseline/equal-arm conditions); boundary/cutpoint selftests | §9, §10 |
| **NEW** | — | dedicated **OC SIMULATION SPECIFICATION** (§9): joint six-cell full-state-machine scenarios + predeclared numeric acceptance tolerances | §9 |

**One headline scientific consequence (see the Fork in §11):** the Q4 repair (a compute ceiling cannot mint evidence of absence) drops correct-pivot-under-global-null from ~97.5% (v3, where `RED_AT_CEILING` counted) to **~38%**, with **~55%** of runs now landing in the legitimate `INCONCLUSIVE_AT_CEILING` outcome. That is the honest price of the repair, not a defect.

---

## 0. Identity + adopted decisions

### 0.1 Instrument identity (verify before any run — unchanged from v3)

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

### 0.2 Adopted decisions (all revisable at re-review / Anthony)

| # | Decision | Value | Rationale / coupling |
|---|---|---|---|
| D1 | Primary statistic | `quad_loop_rate` | Continuity with the v4.3 **G1 vortex-control calibration**. Rests on that continuity, **not** on the 2.2σ κ-suppression point estimate (§1.3). |
| D1′ | Secondary statistic | `omega_roi` (**descriptive only**) | Banded for information; **does not gate the pivot**. `occupancy_x` recorded, not banded. |
| D2 | First-pass blocks | **16** per cell | At 8 blocks RED is unreachable (κ<0, §3.3); 16 gives a usable first surface. (Q6-iv adopted.) |
| D3 | M_grid | **400** for geometric cells A/B/C/D, **GATED** on P1 sign-stability (§1.1). Tc cells AxT2/AxT4 **M frozen by P2 before the scout** (§1.2) — v3's "pending" state is retired (Q5-P2). | M does **not** lower the floor (DIAG 1); the M concern is grid-generated-signal fidelity, addressed by blocks/seed-averaging. |
| D4 | B_conf (floor projection) | **96** working default; escalation 96→128 ceiling for persistent AMBER (§4). | floor(96)=0.557·sd, floor(128)=0.482·sd. |
| D5 | Estimand | **Option (a)** — raw mismatch current as **screening/triage** statistic | μ̂ vs two-arm floor(B_conf); honest SE = sd·√(1/B_scout + 1/64). **v3.1 restricts what (a) may claim** (Q1): it sizes a candidate signal and licenses a **raw-current** pivot only — **not** the mismatch-minus-equal contrast (§2.1, §5). |

### 0.3 Four couplings that must not drift apart

1. **sign precondition ↔ per-cell predicted signs ↔ pivot license** — one chain (§1.1, §6.2, §5).
2. **estimand ↔ B_conf ↔ AMBER escalation ceiling** — share `floor_c` (§2, §4, §5).
3. **M_grid ↔ primary statistic** — one decision: quad@M400 (D1+D3; §1.3).
4. **claim class ↔ what was measured** (NEW, Q1/Q7) — a raw-current RED pivot is a raw-current claim; a contrast claim requires the equal arm; a Tc GREEN requires a measured two-sample contrast at confirmatory (§2.1, §5, §10).

---

## 1. Precondition runs (gate the scout — complete and register BEFORE the scout)

These are **diagnostics, not scout results**. They run the mean-field / equal-τ rig in a declared, quarantined precondition namespace (`precond_P1::`, `precond_P2::`), **NEVER** pooled into `v44pilot::` or any confirmatory (experimental law #6). Their outputs (per-cell signs, sign-stability flags, Tc×M attribution + the frozen Tc-cell M and claim class) are registered as part of the frozen prereg, because the scout's banding, pivot license, and claim class depend on them. **Both preconditions must terminate and register before the scout is licensed** (Q5-P2 "pending" conflict resolved: P2 finishes first, then the Tc-cell M and claim class are frozen — §1.2).

### 1.1 Precondition P1 — per-cell predicted signs + sign-stability (fully pinned — Q5-P1)

The v3 spec carried an **open ambiguity**: "average N seeds into one mean field then take one curl" vs "take per-seed curls then require unanimity." These can disagree (receipt 07: the 8-seed per-seed M=4000 check came out +4/−4 where CFG's 3-seed set was called unanimous). ChatGPT (Q5) required this be killed before registration, because `stable_cell` gates the pivot (§5) and *within-M400 agreement alone does not prove M400 has the right sign* — every M400 seed can share the same resolution-induced bias. v3.1 **freezes ChatGPT's pin**, adopting a high-resolution reference against which stability is judged:

**P1-A — register the directional prediction σ_cell (the physical, mean-field object):**
- For each of the six cells, compute the **ROI-integrated curl of the seed-averaged mean aniso force field at M=4000** — i.e. **average-then-curl**: average the aniso force field over a predeclared high-M seed set into one mean field, then take the single ROI mixed-partial. This yields **one** sign per cell (nothing to be "unanimous" over — that was the v3 category error).
- **σ_cell ∈ {+, −}** := sign of that high-M seed-averaged ROI curl. A cell with a high-M curl indistinguishable from 0 (magnitude below a predeclared negligibility floor) registers **σ_cell = INDETERMINATE** and bands **two-sided** (§3).
- **Predeclared high-M reference set (HQ proposal, revisable — fork §11):** average over **N_avg = 32** seeds `precond_P1::77001…77032` at **M=4000**. σ_cell = sign of the ROI curl of that averaged field.

**P1-B — the sign-stability robustness test (STABLE against a higher-resolution reference, not against itself):**
- Take a **separate, disjoint, predeclared seed set**, evaluate the ROI curl **per seed at M=400** (the scout's operating resolution).
- **STABLE iff ≥ 75% of those M=400 per-seed curls agree in sign with the registered high-M σ_cell.** (Agreement is with σ_cell, not internal unanimity — this is the load-bearing fix: stability = "does the low-resolution instrument preserve the high-resolution physical prediction," not "do the low-res seeds agree with each other," which they could do while all sharing a bias.)
- **Predeclared robustness set + threshold (HQ proposal, revisable — fork §11):** **N = 16** seeds `precond_P1::78001…78016` at M=400; **STABLE iff ≥ 12/16** agree in sign with σ_cell. (Lean N=16, ≥12/16 rather than treating an 8-seed split as decisive — ChatGPT Q5/Q6-v; Antigravity R2 concurs.)

**Consequence for the pivot (frozen):** a cell with **`stable_cell = UNSTABLE`** (< 12/16) **does not count toward the all-RED pivot** from an M=400 null (§5). It may only count after a **predeclared remedy** runs: re-band the cell using either (r1) a **higher M per block** or (r2) **seed-averaged grids per block**, whichever is declared in the frozen prereg for that cell. Running the remedy is a config change and follows the amendment path (§8 step 4). No informal reclassification of UNSTABLE→STABLE.

**Why STABLE gates even a raw-current pivot (non-obvious — stated for reviewers):** the aniso current is *generated by* the grid curl (receipt 07). If the per-block grid-curl sign is unstable, the block-mean can partially **self-cancel**, so a small raw mismatch current at an UNSTABLE cell can be a **masked real effect**, not a true sub-floor null. STABLE is what licenses reading a small raw current there as genuinely sub-floor. This is why P1-B gates the pivot in **both** the option-2 raw-current reading and any contrast reading.

**Note (receipt 07, unchanged):** the quick per-seed SNR metric is *informative but not the instrument* — a single grid's ROI curl is noise-dominated at **both** M=400 and M=4000. The average-then-curl high-M recipe above is what establishes σ_cell; the per-seed check does not substitute for it.

### 1.2 Precondition P2 — crossed Tc×M diagnostic, operationalized as a GATE (Q5-P2)

v3 left P2 as a purpose without a decision criterion ("SD growth shrinks with M," "M-invariant") and left the Tc-cell M "pending." ChatGPT (Q5) required a full gate and demanded the pending conflict be resolved. v3.1 pins P2 as a gate that **completes before the scout**; its output **freezes the Tc-cell M and claim class into the registered prereg** — there is no "pending" state at scout time.

**Design.** Crossed `{Tc ∈ 1, 2, 4} × {M ∈ 400, 4000}` = **6 arms**, equal-τ, same rig as receipt 06 (DIAG 2). *(Deviation from v3, flagged: v3 specified `{Tc ∈ 1,4}`. v3.1 adds Tc=2 so that **each** scout Tc cell — AxT2 at Tc=2 and AxT4 at Tc=4 — gets its own M-sensitivity read rather than interpolating. Defensible improvement; revisable at audit.)*

**Frozen estimator + sampling (HQ proposal, revisable — fork §11):**
- **n = 40 blocks/arm** (registration-grade; up from receipt-06 scouting n≈20).
- **SD estimator:** sample block-SD of the per-block primary statistic (`quad_loop_rate`), per arm.
- **Bootstrap:** percentile bootstrap, **10 000 resamples**, **rng pinned = 999**, **90% two-sided CI** on every ratio below.

**M-sensitivity statistic.** Per Tc, the M-sensitivity ratio
```
R(Tc) = SD(Tc, M=400) / SD(Tc, M=4000)
```
R ≈ 1 ⇒ SD is **M-invariant** (dynamical: a stronger drift reshapes the trajectory/ROI ensemble even on a perfect grid) → M=400 is adequate. R > 1 ⇒ **grid-noise contribution** (finer grid reduces SD) → M=400 inflates the floor.

**Frozen criteria (HQ proposal, revisable — fork §11):**
- **Material grid-noise contribution** ⇔ the **90% CI lower bound of R(Tc) > 1.10** (≥10% SD inflation attributable to grid, significant).
- **M-invariant enough** (equivalence / noninferiority) ⇔ the **90% CI for R(Tc) lies entirely within [0.909, 1.10]** (TOST-style equivalence, ±10% margin).
- **Inconclusive** ⇔ neither of the above (CI straddles 1.10, or the equivalence test fails without material grid-noise).

**Action table (frozen — every branch predeclared, including inconclusive):**

| P2 result for a Tc cell | Higher-M feasible? | Frozen action → registered into prereg |
|---|---|---|
| **M-invariant** (equivalence passes) | — | Tc cell runs at **M=400**; claim class = **full-sensitivity probe** (still subject to the Tc contrast refusal, §2.1). |
| **Material grid-noise** | yes | Tc cell runs at the **M that restores equivalence** (default M=4000; the minimal M with R equivalence if declared); claim class = full-sensitivity probe. |
| **Material grid-noise** | no | Tc cell **demoted to DESCRIPTIVE**: banded for the record, **does not gate the pivot**; a Tc GREEN is candidate-only and requires a measured two-sample contrast at confirmatory. |
| **Inconclusive** | — | **Bump n once** to the predeclared **n = 80/arm** and re-test. Still inconclusive ⇒ **demote to DESCRIPTIVE** (conservative default). |

**No pending state.** After P2 terminates, the Tc-cell M and claim class are **frozen constants** in the registered prereg. The scout consumes them; it never re-decides M at scout time.

### 1.3 Diagnostic language (frozen at n=20 reality — unchanged from v3)

- **Floor is trajectory-limited even at scale 10** (DIAG 1: SD@400/SD@2000 = 1.19 [0.80,1.74] quad, 0.87 [0.61,1.25] omega). Raising M does **not** lower the floor.
- **κ-injection suppression is NOT established:** quad ratio 0.90 (~0.5σ); omega ratio 0.67 (~2.2σ uncorrected p≈0.03, does **not** survive Holm across ~8 diagnostic contrasts). The quad-primary choice (D1) rests on v4.3 G1-calibration continuity, suppression as supporting color only — never the 2.2σ point estimate.
- **Net relative sensitivity at M=400:** quad ≈ 0.90, omega ≈ 0.83 → quad wins at M=400 (couples D1↔D3).

---

## 2. Estimand + exact thresholds

### 2.1 Pinned estimand — option (a), a **screening/triage** statistic (Q1 licensing repair)

μ̂ (per cell, per statistic) = the mean of the **raw mismatch current** over the scout blocks. It is a **screening proxy** that sizes a candidate signal. The honest SE folds in the v4.3 64-block equal-arm reference:

```
SE(B_scout) = sd_cell · √(1/B_scout + 1/64)
```

**Two distinct roles of "the equal arm" — do not conflate (auditor trip-wire, unchanged from v3):**
1. **floor_c's SD source.** The scout runs **no equal arm** (all six cells are mismatch), so `floor_c` is projected from **the cell's own measured block SD** (`sd_cell`, n=B_scout) as a **homoscedastic proxy** for the confirmatory's equal-arm SD.
2. **The named equal-arm config (§6.1)** defines the **contrast estimand** and the **confirmatory's second arm** at Movement 3. It is *not* used in the scout's floor arithmetic.

**Q1 — what estimand (a) may and may not claim (frozen):**

ChatGPT's Q1 finding: a small raw mismatch current does **not by itself bound the contrast** Δ = μ_mis − μ_eq, because μ_eq is verified ≈ 0 **only at (1.0,1.0)@Tc=1**, while the pivot's reference configs include (2.0,2.0) and the Tc cells change drive amplitude. A nonzero equal-arm offset could hide or inflate the contrast. Therefore:

- A **GREEN** sizes a **candidate signal**; it triggers Movement-3 registration, and **Movement 3 is the independent two-sample contrast test**. A GREEN is candidate-selection, not a measured contrast (§10 claim limits).
- An **all-RED pivot** is restricted to a **RAW-CURRENT claim** (ChatGPT **option 2**, **HQ-recommended-pending-Anthony**): *"raw mismatch currents are sub-floor across the accessible design space."* It is **explicitly not** a contrast claim. The contrast test belongs to Movement 3.
- **Tc cells (Tc>1): estimand-(a) is REFUSED as contrast licensing (Q6-iii, frozen).** Any high-Tc GREEN requires a **measured two-sample contrast** (estimand (c)) at confirmatory. Tc-cell raw currents may support the raw-current pivot (if STABLE and full-sensitivity per §1.2) but never a Tc contrast claim.

**Options for the contrast-licensing question (Anthony ratifies — fork §11).** HQ writes v3.1 around **option 2**. The other two options ChatGPT named, documented for completeness:
- **Option 1 — pre-scout equal-arm calibration gates.** Before the scout, measure the equal-arm current at every distinct reference config used by the pivot — **(1.0,1.0)@Tc=1, (2.0,2.0)@Tc=1, (2.0,2.0)@Tc=2, (2.0,2.0)@Tc=4** — with a **predeclared negligibility bound** (e.g. |μ_eq| < 0.10·floor at that config) establishing the equal arm is negligible relative to the relevant floor. Passing all four would **license the all-RED pivot as a contrast claim** (upgrading option 2's raw-current claim).
- **Option 3 — measure the equal arm in-scout, two-sample.** Each cell runs its named equal arm (§6.1) alongside the mismatch arm; band the **two-sample contrast** directly (estimand (c), two-arm SE = sd·√(2/B), higher GREEN bar). This makes every band a contrast statement at the cost of ~2× the scout compute.

If reviewers/Anthony pick option 1 or 3, the raw-current restriction in §5 is upgraded to a contrast claim per that option; the τy-matched equal-arm choice (§6.1) then becomes operative **in-scout** (option 3) or as the calibration target (option 1).

### 2.2 Frozen convention (law #4 grep-consistency — unchanged from v3)

One-sided **Student-t at (n−1) df, α=0.05** for GREEN/RED in the predicted direction; two-sided Student-t at (n−1) df, α=0.05 for INDETERMINATE-sign cells.

| df (n−1) | one-sided t (0.95) | two-sided t (0.975) |
|---|---|---|
| 7  (8 blocks)  | 1.895 | 2.365 |
| 15 (16 blocks) | **1.753** | **2.131** |
| 31 (32 blocks) | 1.696 | 2.040 |

### 2.3 Exact thresholds table (unchanged from v3; all grep-consistent)

`floor_c` and `SE` are in units of the cell's own block SD, `sd_cell`. GREEN threshold on μ̂ = `floor_c + t·SE`. RED ceiling on μ̂ = `floor_c − t·SE` (point-governed where κ = floor_c − t·SE > 0; §3.3 for the robust-both-sd form).

| Config (blocks / B_conf) | floor_c | SE = sd·√(1/B+1/64) | **GREEN μ̂ >** (1-sided) | **GREEN μ̂ >** (2-sided) | RED μ̂ < (point) |
|---|---|---|---|---|---|
| **16 / 96  (OPERATIVE first pass)** | 0.557·sd | 0.2795·sd | **1.047·sd = 1.88× floor** | **1.153·sd = 2.07× floor** | **0.067·sd** |
| 8 / 96   (legacy-block reference) | 0.557·sd | 0.3750·sd | 1.267·sd = 2.28× floor | 1.444·sd = 2.59× floor | unreachable (κ<0) |
| 32 / 96  (AMBER block-extension) | 0.557·sd | 0.2165·sd | 0.924·sd = 1.66× floor | 0.998·sd = 1.79× floor | 0.190·sd |
| 32 / 128 (AMBER B_conf escalation, ceiling) | 0.482·sd | 0.2165·sd | 0.849·sd = 1.76× floor | 0.924·sd = 1.92× floor | 0.115·sd |
| *8 / 64 (v2 legacy reference only)* | *0.682·sd* | *0.375·sd* | *1.393·sd = 2.04× floor* | *1.569·sd = 2.30× floor* | *unreachable (κ<0)* |

**Operative frozen GREEN for the primary (`quad_loop_rate`, 16 blocks, B_conf=96, one-sided in the registered predicted direction): μ̂ > 1.047·sd_cell (= 1.88× floor(96)).**

---

## 3. The four-band rule (exact inequalities)

Banded on the **primary statistic** (`quad_loop_rate`) only; `omega_roi` gets the same arithmetic **descriptively** (does not gate the pivot). Let `t = t*(n−1 df)` per §2.2, `SE` per §2.1, `floor_c` per §2.3, and σ_cell the registered predicted sign (P1). The terminal ceiling label is **`INCONCLUSIVE_AT_CEILING`** (Q4 — replaces v3's `RED_AT_CEILING`).

**One-sided cells (σ_cell ∈ {+,−}).** Work in signed units aligned to the prediction: `x = σ_cell · μ̂` (`x > 0` = current in the predicted direction).

- **GREEN** — register a confirmatory (candidate-selection, §10): `x − t·SE > floor_c`.
- **RED** — bounded sub-floor raw current (robust form §3.3): `x + t·SE < floor_c` **AND** not a significant wrong-sign excursion.
- **ANOMALOUS** — a **significant** wrong-sign current; does **not** count toward the pivot; triggers the §8 state machine: `x < −t·SE` (significant against **0**, one-sided α=0.05).
- **AMBER** — promising but not separated; extend (§4): none of the above.

Partition (complete, no gap): ANOMALOUS `(−∞, −t·SE)`, RED `[−t·SE, floor_c−t·SE)`, AMBER `[floor_c−t·SE, floor_c+t·SE]`, GREEN `(floor_c+t·SE, ∞)`.

> **Finding-4 correction (Antigravity, retained from v3).** ANOMALOUS keys on significance against **0** (`x < −t·SE`), not the floor magnitude — this catches a significant wrong-sign artifact (e.g. `μ̂ = −1.0·sd` at 16b/B96 is a 3.6σ wrong-sign excursion) that the floor-keyed form would have laundered into RED. Verified at operative 16b/B96 by Antigravity R1 and R2.

> **Anomaly-rate arithmetic (Q2 correction — v3's ~26% is wrong).** The honest SE = sd·√(1/16+1/64) = 0.2795·sd is **conservative** relative to μ̂'s true sampling SD = sd/√16 = 0.25·sd. So the effective ANOMALOUS z-threshold is 1.753·(0.2795/0.25) = 1.960 ⇒ **per-cell false-anomaly rate ≈ 2.5%** under a true null (not the nominal 5%). Across **six independent one-sided cells** the chance of ≥1 false anomaly is 1−(1−0.0251)⁶ = **≈ 14.1%** — **a planning approximation** under the independence + six-one-sided-cells assumption, **not** a universal operating rate. (v3 stated ~26% by using the nominal 5%; that is superseded.) The real cells are **not** independent — A≡B and C≡D share the ROI mixed-partial to 4 s.f. (receipt 07), and any INDETERMINATE cell has no anomaly branch — so the *actual* joint rate is **lower** than 14.1%; treat 14.1% as a conservative planning ceiling. A false anomaly **blocks** the pivot pending the §8 state machine (the conservative, don't-pivot-on-an-artifact direction), it does not produce a wrong verdict.

**Two-sided cells (σ_cell = INDETERMINATE from P1).** Use the two-sided `t`; ANOMALOUS does not apply (no predicted direction):
- **GREEN**: `|μ̂| − t·SE > floor_c`.
- **RED**: `|μ̂| + t·SE < floor_c` (robust form §3.3).
- **AMBER**: otherwise.

### 3.1 GREEN meaning
The scouting-grade sign-aligned lower confidence bound clears the confirmatory's minimum detectable effect. **A GREEN is candidate-selection** (§10): it names where to run the Movement-3 two-sample contrast, it is not itself a measured contrast.

### 3.2 ANOMALOUS meaning
A large wrong-direction current is a grid-artifact / transduction-breakdown signal, carved out of RED so it cannot launder into the null bucket. It triggers the frozen §8 state machine (not registration, not a silent re-band).

### 3.3 RED robustness — kept EXACTLY as v3 (Q3 PASS) + two documentation caveats

**This subsection is unchanged from v3 §3.3** (ChatGPT Q3 = PASS; Antigravity R2 reproduced the 4M-draw Monte Carlo). Reproduced verbatim in substance:

- v2's mental model was **coupled** (a single `sd` moving `floor_c` and `SE` together); upper-sd makes RED harder only while κ = floor_c − t·SE ≤ 0 (true at 8 blocks).
- At the adopted **16-block / B_conf=96** config, **κ = +0.067·sd > 0**, so a **floor-only** upper-sd read makes RED **easier**, driving the false-null rate for an at-floor effect from **3.9% (point-sd)** to **18.9% (floor-only upper-sd)** — ~5× worse, anti-conservative, unacceptable.

**Frozen RED rule (always conservative at every config):**
```
RED  ⇔  ( x + t·SE(sd̂)      < floor_c(sd̂)      )   AND
        ( x + t·SE(sd_upper) < floor_c(sd_upper) )
```
The conjunction always selects the harder ceiling. `sd_upper = sd̂ · √((n−1)/χ²_{0.05,n−1})`, factors **1.797 (n=8), 1.437 (n=16), 1.268 (n=32)**. Monte Carlo (4×10⁶ draws, Δ = floor(96), operative config, `/usr/bin/python3` numpy 2.0.2): point-sd 3.95%, floor-only upper-sd 18.86%, coupled-upper 4.93%, **conjunction 3.95%**. Antigravity R2 reproduced: 3.951% / 18.860% / 4.933% / 3.951%.

**Operative RED (16b/B96): `x < 0.067·sd_cell`** (point governs).

> **Q3 documentation caveats (added in v3.1, per ChatGPT — these do not change the rule, they scope its warrant):**
> 1. **The Monte Carlo validates the LOCAL false-null behavior of the RED rule only; it does NOT validate the full six-cell sequential loop.** The whole-loop validation is the OC simulation (§9) with predeclared acceptance criteria. "The §3.3 MC passes" is necessary but not sufficient for registration.
> 2. **The Monte Carlo assumes the cell's own block SD (`sd_cell`) is a reasonable proxy for the equal-arm SD.** That homoscedasticity assumption is precisely the Q1 calibration/validation work (§2.1); it is stated, not proven, by §3.3. Under option 1/3 it is measured; under option 2 it is carried as a stated assumption bounding only the raw-current claim.

---

## 4. AMBER terminal rule + B_conf escalation → INCONCLUSIVE_AT_CEILING (Q4)

A cell may not sit in AMBER forever (no sequential-testing leak). The terminal ladder, per AMBER cell, in order:

1. **One block-extension: 16 → 32 blocks.** SE shrinks 0.2795·sd → 0.2165·sd; re-band against floor(96) with the 32-block row. **The 32-block sample CONTAINS the 16-block first pass** (accumulation, not an independent redraw) — this dependence is preserved in the OC simulation (§9).
2. **Still AMBER against floor(96) at 32 blocks → escalate B_conf 96 → 128.** floor_c drops 0.557·sd → 0.482·sd; a persistent AMBER may resolve **GREEN** against the larger confirmatory. Re-band with the 32/128 row.
3. **Still AMBER against floor(128) at 32 blocks → `INCONCLUSIVE_AT_CEILING`.** B_max = 128 is the **declared compute ceiling**.

**Q4 repair (the block-clearing change).** v3 relabeled terminal AMBER as `RED_AT_CEILING` and **counted it as RED** toward the pivot. ChatGPT (Q4, BLOCK): *"a resource ceiling cannot turn insufficient evidence into evidence of absence."* An AMBER at the ceiling means the confidence interval still overlaps the floor — the cell is **unresolved at the authorized compute**, not **bounded below the floor**. v3.1:

- The terminal state is **`INCONCLUSIVE_AT_CEILING`**.
- **It BLOCKS the pivot** (it is not RED, not GREEN, not ANOMALOUS — §5).
- It is a **scientifically legitimate outcome**: a bound on what this compute allocation resolves, **not** a null.

Escalation order is fixed (blocks first, then B_conf) so the compute budget is bounded and the terminal state well-defined. B_max = 128 is the working ceiling (Q6-ii adopted; revisable at ratification).

---

## 5. The pivot rule — four honest terminal outcomes (Q4) + raw-current claim (Q1)

The scout ends in exactly one of **four** honest terminal outcomes:

1. **GREEN candidate** — ≥1 cell GREEN → **register the Movement-3 two-sample contrast** at the tie-break cell (do not pivot). Candidate-selection, §10.
2. **All-actual-RED pivot** — pivots to the closed no-reset NESS protocol **iff all pivot conditions below hold**. The claim is a **RAW-CURRENT claim** (Q1 option 2): *"raw mismatch currents are sub-floor across the accessible design space,"* **not** a contrast claim.
3. **ANOMALOUS → investigate** — ≥1 cell ANOMALOUS → run the §8 state machine; **no pivot and no terminal-null decision while an anomaly is open**.
4. **INCONCLUSIVE at compute ceiling** — ≥1 cell `INCONCLUSIVE_AT_CEILING` (and no GREEN/ANOMALOUS forcing outcomes 1/3) → the scout **halts with a legitimate bound**: *"at B_max=128 the design space is not resolved to sub-floor at these cells."* **This is not a null and not a failure** — it is a statement about the compute allocation. **It blocks the pivot.**

**Pivot conditions for outcome 2 (ALL must hold — outcome 2 is licensed only when none of outcomes 1/3/4 fires):**
- **(0) No open anomaly (blocks the pivot):** **no** cell is ANOMALOUS. (Defeats the vacuous-truth failure — "every non-ANOMALOUS cell is RED" is vacuously true when there are no non-anomalous cells.) A cell leaves ANOMALOUS **only** through the §8 state machine, never by informal re-band.
- **(0′) No open inconclusive (blocks the pivot — Q4):** **no** cell is `INCONCLUSIVE_AT_CEILING`. A compute ceiling cannot mint evidence of absence.
- **(i) Terminal-band condition:** at least one cell was banded, and **every** cell is **actual RED** (§3, §4). Given (0) and (0′), "every cell" excludes ANOMALOUS and INCONCLUSIVE — no vacuous set, no ceiling-minted null.
- **(ii) Instrument precondition:** **`stable_cell` = STABLE** (P1, §1.1) for **every** cell whose RED is counted. An UNSTABLE RED at M=400 does not license the pivot until its predeclared remedy runs (§1.1) — this closes the one path by which a self-cancelling live effect could be abandoned on an instrument artifact.

**In words:** a raw-current null (pivot) is earned only when **no cell showed an unexplained wrong-sign current**, **no cell was left unresolved at the compute ceiling**, the design space is confidently sub-floor in **raw mismatch current**, and the instrument was demonstrably reading a **stable-sign** signal everywhere it called RED. The scout still "cannot fail": it finds a registrable candidate, or it bounds the raw-current space with a stable instrument, or it names an anomaly to investigate, or it honestly reports the compute allocation did not resolve the space.

**Upgrading the pivot to a contrast claim** ("the tunable space is bounded sub-floor") requires the **baseline/equal-arm condition** — option 1 (pre-scout calibration gates pass) or option 3 (in-scout two-sample) of §2.1, or the Movement-3 confirmatory. Under the HQ-recommended option 2, the scout **does not** make that upgrade; Movement 3 does.

**GREEN tie-break (outcome 1):** if several cells are GREEN, the registration cell is the one with the highest `x − t·SE` margin above `floor_c` on the primary statistic. A Tc-cell GREEN is a **drive-amplitude** registration **requiring a measured two-sample contrast** (§2.1); a geometric-cell GREEN is a **Δτ** registration — recorded as distinct claims.

---

## 6. Per-cell configuration tables

### 6.1 Equal-arm config per candidate cell (Q6-i adopted — τy-matched at matched Tc, conditional on Q1)

**Adopted: τy-matched equal arm** — the equal-τ config at the cell's **larger horizon** τy, at the **same Tc**. Rationale (receipt-07 noise argument): the ROI mixed-partial of the small-τx grid is ≈ 0, so the curl and its block-SD noise are carried by the larger-horizon τy grid; the τy-matched arm is the closest noise-match. Matched-Tc is **non-optional** for the Tc cells (DIAG 2). **Conditional on Q1:** under option 2 this config defines only the **Movement-3 second arm** (not used in-scout); under option 1 it is the calibration target; under option 3 it runs in-scout.

| Cell | (τx, τy) | Tc | Role | Equal-arm config (τy-matched, matched-Tc) |
|---|---|---|---|---|
| A    | (0.1, 2.0)  | 1 | widest horizon mismatch | (2.0, 2.0) @ Tc=1 |
| B    | (0.25, 2.0) | 1 | mismatch mid            | (2.0, 2.0) @ Tc=1 |
| C    | (0.1, 1.0)  | 1 | amplitude-only          | (1.0, 1.0) @ Tc=1 |
| D    | (0.25, 1.0) | 1 | replica bridge to v4.3  | (1.0, 1.0) @ Tc=1  ← coincides with v4.3's equal arm; genuine bridge-consistency |
| AxT2 | (0.1, 2.0)  | 2 | Tc sweep at widest pair | (2.0, 2.0) @ Tc=2 |
| AxT4 | (0.1, 2.0)  | 4 | Tc sweep at widest pair | (2.0, 2.0) @ Tc=4 |

**Reviewer alternatives (fork §11):** (τx,τx)-matched, or a dual-reference design against both (τx,τx) and (τy,τy).

### 6.2 Predicted-sign table (all TBD until P1 registers)

Per-cell one-sided banding requires σ_cell from P1 (§1.1). Until P1 runs, **no cell has a registered sign** and none may band one-sided.

| Cell | (τx, τy, Tc) | Registered σ_cell | Banding |
|---|---|---|---|
| A    | (0.1, 2.0, 1) | **TBD by P1** (receipt-07 quick check leaned `+`, inconclusive) | one-sided if σ∈{+,−}, else two-sided |
| B    | (0.25, 2.0, 1) | **TBD by P1** | one-sided if σ∈{+,−}, else two-sided |
| C    | (0.1, 1.0, 1) | **TBD by P1** (leaned `+`, inconclusive) | one-sided if σ∈{+,−}, else two-sided |
| D    | (0.25, 1.0, 1) | **TBD by P1** (v4.3 arm1 τx<τy ⇒ `+`, re-derive per cell) | one-sided if σ∈{+,−}, else two-sided |
| AxT2 | (0.1, 2.0, 2) | **TBD by P1** | one-sided if σ∈{+,−}, else two-sided |
| AxT4 | (0.1, 2.0, 4) | **TBD by P1** | one-sided if σ∈{+,−}, else two-sided |

An INDETERMINATE cell moves GREEN to the two-sided column (16b/B96: 1.153·sd = 2.07× floor, vs one-sided 1.047·sd = 1.88× floor).

---

## 7. `band_cell()` + `pivot_licensed()` pseudocode

Reference implementation for the additive functions in `analyze()` (§10 scope). Pure analysis; touches no harness physics. All arithmetic in units of `sd_cell`.

```python
def band_cell(mu_hat, sd_cell, n_blocks, B_conf, sigma_cell, stable_cell):
    """
    Band one scout cell on the PRIMARY statistic (quad_loop_rate).
    Returns (band, aligned_bound, floor_c) where band in
    {GREEN, AMBER, RED, ANOMALOUS}.
    INCONCLUSIVE_AT_CEILING is set by the caller's terminal ladder (sec 4),
    NOT by a single band_cell() call.
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

    x = abs(mu_hat) if two_sided else sigma_cell * mu_hat

    # GREEN: sign-aligned lower CB clears the confirmatory floor (candidate-selection)
    if x - t * SE(sd_cell) > floor_c(sd_cell):
        return ("GREEN", x - t*SE(sd_cell), floor_c(sd_cell))

    # ANOMALOUS: SIGNIFICANT wrong-sign excursion (one-sided cells only) -> not RED;
    #            keyed on significance against 0 (Finding 4); triggers sec 8 state machine.
    if (not two_sided) and (x < -t * SE(sd_cell)):
        return ("ANOMALOUS", x - t*SE(sd_cell), floor_c(sd_cell))

    # RED: sign-aligned upper CB below floor under BOTH point and coupled-upper sd (sec 3.3)
    red_point = (x + t * SE(sd_cell) < floor_c(sd_cell))
    red_upper = (x + t * SE(sd_up)   < floor_c(sd_up))
    if red_point and red_upper:
        return ("RED", x + t*SE(sd_cell), floor_c(sd_cell))

    return ("AMBER", x + t*SE(sd_cell), floor_c(sd_cell))


def pivot_licensed(cell_bands, stable_flags):
    """Sec 5: pivot to closed no-reset NESS (RAW-CURRENT claim) iff ALL hold.
    Guarded against vacuous truth AND against a compute-ceiling-minted null."""
    # (0) an open ANOMALOUS cell blocks the pivot (sec 8: resolve first)
    if any(b == "ANOMALOUS" for b in cell_bands.values()):
        return False
    # (0') an INCONCLUSIVE_AT_CEILING cell blocks the pivot (Q4: no ceiling-minted absence)
    if any(b == "INCONCLUSIVE_AT_CEILING" for b in cell_bands.values()):
        return False
    if not cell_bands:
        return False                             # nothing to bound the space
    if any(b == "GREEN" for b in cell_bands.values()):
        return False                             # register at the GREEN cell instead
    # (i) every remaining cell must be ACTUAL RED (INCONCLUSIVE no longer counts, Q4)
    if not all(b == "RED" for b in cell_bands.values()):
        return False                             # AMBER cells -> run sec 4 ladder first
    # (ii) instrument precondition: every counted RED must be on a STABLE cell
    if not all(stable_flags[c] for c, b in cell_bands.items() if b == "RED"):
        return False                             # UNSTABLE RED at M=400 does not license
    return True
```

`omega_roi` (secondary, D1′) is run through the same `band_cell()` for the record but its band is **descriptive** — excluded from `pivot_licensed`.

**Key diff from v3 pseudocode:** the terminal set was `("RED", "RED_AT_CEILING")`; it is now `"RED"` alone, and an explicit `INCONCLUSIVE_AT_CEILING` guard (0′) blocks the pivot. That single change is the Q4 repair in code.

---

## 8. Anomaly-resolution state machine (Q2 — frozen, preregistered)

v3 said a cell "may be re-banded out of ANOMALOUS after investigation." ChatGPT (Q2) BLOCKED that as too open-ended for preregistration. v3.1 **freezes a state machine**: what counts as investigation, the predeclared discriminator, the disposition, and the rule that any recipe change is a formal amendment. **No outcome-dependent repair may convert an anomaly into a pivot-supporting RED without this frozen procedure.**

**Trigger.** A cell bands ANOMALOUS (§3, `x < −t·SE`). The pivot is blocked (condition (0)) until this machine terminates the cell in one of {GRID-ARTIFACT re-banded, TRUE-OPPOSITE-PHYSICS, SIGN-PRECONDITION-FAILURE excluded, UNRESOLVED}.

**Predeclared discriminator — higher-M survival, then P1-reference robustness:**

```
STATE A  (entry): cell is ANOMALOUS at M=400.
  --> Rerun the anomalous cell at the predeclared higher-M / seed-averaged-grid recipe
      (the SAME remedy declared for that cell in P1; sec 1.1 r1/r2), in precond namespace.

STATE B  (rerun result):
  - Wrong-sign significance VANISHES at higher M (band no longer ANOMALOUS)
        --> classify GRID-ARTIFACT.
            Re-band the cell UNDER THE HIGHER-M RECIPE (a predeclared recipe supersede,
            recorded via the sec 8-step-4 amendment path -- NOT an informal re-band).
            The re-banded result (RED/AMBER/GREEN at higher M) then flows normally.
  - Wrong-sign significance PERSISTS at higher M --> STATE C.

STATE C  (persistent dynamical wrong-sign): compare the persistent sign to P1's registered
         high-M sigma_cell, and re-examine sigma_cell's high-M reference robustness:
  - Persistent sign OPPOSES sigma_cell AND sigma_cell's high-M reference is robust on
    re-examination (P1-B robustness set still >= 12/16 with sigma_cell)
        --> classify TRUE-OPPOSITE-PHYSICS.  This is NOT a null and NOT a grid bug:
            it is a finding. Escalate to a Movement-3 two-sample contrast in the OBSERVED
            direction. The cell never counts toward an all-RED pivot.
  - Re-examination shows sigma_cell was mis-registered (high-M curl now sign-unstable, or
    the P1-B robustness set now disagrees with the registered sigma_cell)
        --> classify SIGN-PRECONDITION-FAILURE.  The cell is EXCLUDED from the pivot.
            P1 may be re-run ONLY under a formal prereg amendment (sec 8 step 4).

STATE D  (higher-M infeasible OR STATE B/C inconclusive)
        --> classify UNRESOLVED. The cell blocks the pivot indefinitely; the scout
            terminates in outcome 3 (sec 5) with the anomaly named as an open finding.
```

**Disposition summary (frozen):**

| Classification | Disposition | Counts toward pivot? |
|---|---|---|
| GRID-ARTIFACT | re-band under higher-M recipe (amendment) | yes, at the re-banded higher-M result |
| TRUE-OPPOSITE-PHYSICS | Movement-3 contrast in observed direction (a finding) | **no** |
| SIGN-PRECONDITION-FAILURE | cell excluded; P1 re-run only via amendment | **no** (until amended prereg) |
| UNRESOLVED | scout halts in outcome 3, anomaly named | **no** |

**Step 4 — the amendment rule (frozen, spans all classifications).** Any change to a cell's resolution, M, seed recipe, or σ_cell registration requires a **formal preregistration amendment**: regenerate the affected config, record the **new `config_hash` + `source_sha` + prereg sha256**, verify readback, **then** run (experimental law #1). Corrections **supersede**, never erase (law #9). There is **no informal "investigate and re-band" path**.

**Selftest requirement (law #2).** The anomaly gate must demonstrably be able to **fire** on a planted wrong-sign artifact and demonstrably **block** the pivot — asserted in the OC simulation (§9, scenario 5).

---

## 9. OC SIMULATION SPECIFICATION (NEW — Q4/Q7; the next build phase implements this)

ChatGPT (Q4) required that the selftest operate on the **entire frozen state machine**, not per-contrast power, with **predeclared acceptance criteria** — *"without predeclared tolerances, 'selftest passes' is not yet an experimental decision rule."* This section is that specification. It is registered as part of the prereg (§10). It **must run and pass before the scout is licensed** (after P1/P2, before the scout).

**Why joint + full-loop is non-optional (experimental law #3).** Analytic per-contrast power lies under a multi-look ladder — v4.3's own lesson: 0.998 analytic per-contrast vs **0.655 compound**. The 16→32→B128 ladder here is exactly such a multi-look. The acceptance criteria below are therefore **compound / whole-loop** operating characteristics, measured by simulating **all six cells jointly** through the full state machine.

### 9.1 Simulation model (implementable)

- **Null-SD calibration (receipt 06).** Per-block SD of `quad_loop_rate`: Tc1 = **5.03e-5**, Tc2 = **6.29e-5** (×1.25), Tc4 = **8.15e-5** (×1.62). (`omega_roi` secondary: Tc1 4.45e-5, Tc2 6.67e-5 ×1.50, Tc4 8.90e-5 ×2.00.) All banding is scale-free in `sd_cell`, so the SDs enter only the Tc-heteroscedastic and equal-arm-offset scenarios; the band arithmetic is simulated in `sd_cell` units.
- **Draw model.** For a cell with true contrast Δ (in `sd_cell` units): each block statistic ~ N(Δ, 1); first-pass μ̂₁₆ = mean of the **first 16** block draws; the 32-block extension **reuses those 16 and appends 16 new** (accumulation dependence preserved — load-bearing for the invalid-pivot rate). sd̂ from the sample SD of the realized blocks (~ √(χ²_df/df)); `sd_upper` from the χ² factor (§3.3). B96→B128 escalation re-bands the **same 32-block** sample against the lower floor.
- **State machine.** Every draw flows through: P1 sign/stability assignment → `band_cell()` → §4 terminal ladder (16→32→B128 → INCONCLUSIVE_AT_CEILING) → §8 anomaly machine (for planted wrong-sign) → §5 `pivot_licensed()` / GREEN tie-break. P2-driven M for Tc cells is applied as the frozen constant.
- **Trials + rng.** ≥ **1×10⁵** trials per scenario (≥ **1×10⁶** for the false-GREEN and invalid-pivot tail estimates), **rng pinned** (proposal `seed = 20260707`), `/usr/bin/python3` numpy 2.0.2. Report Monte Carlo standard errors on every rate.

### 9.2 Scenarios (all six cells simulated jointly)

| # | Scenario | Construction |
|---|---|---|
| S1 | **Global null** | all six cells Δ = 0, Tc-calibrated SDs |
| S2 | **One-cell at-floor** | one cell Δ = floor(96) = 0.557; rest null |
| S3 | **One-cell supra-floor sweep** | one cell Δ ∈ {1×, 2×, 3×} floor; rest null (three sub-scenarios) |
| S4 | **Multi-signal / GREEN tie-break** | **≥2 supra-floor cells** (e.g. two cells at 2× and 3× floor, one further at 2.5× floor, rest null) → forces **multiple simultaneous GREENs** so the highest-`x − t·SE` tie-break (§5) actually resolves and is checked. (S3 with one signal never triggers the tie-break; S4 is the only scenario that exercises it.) |
| S5 | **Wrong-sign artifact** | one cell Δ = −1× floor (significant wrong direction); rest null → must trip ANOMALOUS + block the pivot (§8 **entry + blocking**). *Note: S5 validates anomaly **detection + pivot-blocking** in-sim; the §8 **classification** branches (grid-artifact / true-opposite-physics / sign-precondition-failure) require real higher-M reruns and are validated at execution time, not in the null-draw OC sim.* |
| S6 | **Tc-heteroscedastic** | Tc cells drawn with receipt-06 SD scaling (AxT2 ×1.25, AxT4 ×1.62); tests that per-cell `sd_cell` banding neutralizes the Tc growth |
| S7 | **Nonzero equal-arm offset** | inject μ_eq ≠ 0 (e.g. 0.10·floor and 0.30·floor) into the raw current → sizes how a real offset perturbs the raw-current pivot and quantifies the Q1 gap between raw-current and contrast |

### 9.3 Predeclared acceptance criteria (HQ-recommended numeric tolerances — pending Anthony; fork §11)

**Hard gates (registration blocked if violated) — the safety criteria:**

| Criterion | Scenario | Tolerance (HQ-recommended) | Expected (from §-arithmetic) |
|---|---|---|---|
| **P(any false GREEN)** | S1 global null | **≤ 0.01** | ~2×10⁻⁴ (per-cell z≈4.19) |
| **P(invalid pivot)** — at floor | S2 (Δ=floor) | **≤ 0.02** | ~1.8% (0.0395 × 0.852⁵) |
| **P(invalid pivot)** — supra-floor | S3 (Δ≥2× floor) | **≤ 0.005** | ≈0 (RED false-null collapses above floor) |
| **P(registrable GREEN)** — compound power | S3 (Δ=3× floor) | **≥ 0.90** | 0.994 first-pass; law #3 compound-gate ≥0.90 |
| **P(ANOMALOUS flagged + pivot blocked)** | S5 wrong-sign | **≥ 0.90** | 3.6σ wrong-sign trips reliably |
| **Partition completeness** (no un-banded limbo) | S1–S7 | **= 1.00** | complete partition (§3) |
| **law #2 — gate can FAIL on signal** | S2/S3 | planted signal **breaks** all-RED pivot in ≥1 cell (assertion) | by construction |

**Reported / advisory operating characteristics (informative, NOT hard-gated — hard-gating these would fight the Q4 repair):**

| Characteristic | Scenario | Advisory | Expected |
|---|---|---|---|
| **P(correct pivot)** | S1 calibrated null | advisory **≥ 0.30** (low is acceptable; complement is legitimate INCONCLUSIVE) | ~0.38 (0.852⁶) |
| **P(≥1 INCONCLUSIVE_AT_CEILING)** | S1 | report | ~0.55 (1−0.877⁶) |
| **P(≥1 false anomaly)** | S1 | report (planning ceiling); soft cap **≤ 0.20** | ~0.141 (independence upper bound) |
| **P(registrable GREEN)** power curve | S3 | report at 1×/2× floor | ~0.025 (1×), ~0.605 (2×) |
| **P(correct tie-break selection \| ≥2 GREEN)** | S4 | report; advisory **≥ 0.90** (highest true-margin cell chosen) | tie-break path exercised only by S4 |
| **raw-vs-contrast gap** | S7 | report pivot/GREEN shift vs offset | sizes the Q1 gap |

**Interpretation of the split.** Only the **safety** criteria (false GREEN, invalid pivot, wrong-sign flagging, partition, compound power, law-#2 failability) are hard gates — they are the "don't mint absence, don't miss signal" guarantees. **P(correct pivot | null) is deliberately advisory:** the Q4 repair *intends* a large fraction of null runs to land in INCONCLUSIVE rather than pivot, because at B_max=128 those cells genuinely are not resolved. Hard-gating a high correct-pivot rate would pressure the design back toward minting absence — exactly the error Q4 removes. The invalid-pivot criterion (≤0.02 at floor) is the load-bearing gate: it is the direct measure of the "mint evidence of absence" error the whole repair exists to prevent.

### 9.4 Boundary / cutpoint selftests (Q7 item 7 — required before re-issue)

Distinct from the OC rates; deterministic assertions on `band_cell()`/`pivot_licensed()`:

- **Equality at each cutpoint** — μ̂ exactly at `floor_c ± t·SE` and at `floor_c` (GREEN/AMBER, AMBER/RED, and the ANOMALOUS `−t·SE` edge) resolve to the predeclared side (strict `>`/`<` per §3).
- **One-sided vs two-sided branch** — σ_cell ∈ {+1,−1} vs None route through the correct t and the correct GREEN/RED/ANOMALOUS logic (two-sided has no ANOMALOUS).
- **Wrong-sign anomaly boundary** — μ̂ = −t·SE/σ (just inside/outside) flips ANOMALOUS exactly at the significance edge.
- **SD-upper factors per block count** — assert 1.797 (n=8), 1.437 (n=16), 1.268 (n=32) and that the RED conjunction selects the harder ceiling at κ<0 and κ>0.
- **Empty-cell / anomaly-only pivot guard** — `pivot_licensed({})` = False; all-ANOMALOUS = False; all-INCONCLUSIVE = False (no vacuous-truth, no ceiling-minted null).
- **Terminal-ceiling behavior** — a cell that reaches 32/128 still AMBER emits `INCONCLUSIVE_AT_CEILING` and blocks the pivot (never `RED`).

---

## 10. Scope of changes if ratified (→ config_hash / prereg re-issue) — Q7

| Artifact | Change | Hash impact |
|---|---|---|
| `SCOUT_DECLARATION.md` decision-rule section | Replaced by §1–§8 of this document (human-readable; not hash-frozen) | none (declaration) |
| `analyze()` in `v44_scout.py` | Add `band_cell()` + `pivot_licensed()` (§7) with the `INCONCLUSIVE_AT_CEILING` label — additive, testable, does **not** touch the v4.3-inherited estimator or forward physics | new `source_sha` |
| `CFG["scout"]["blocks"]` | 8 → **16** (D2) | **new `config_hash` → re-issue `prereg_v44.json` → new sha256** |
| B_conf convention for the floor projection | 64 → **96** (D4) | new `config_hash` if surfaced in CFG; else declaration-only |
| **P1 config** (§1.1) | high-M reference set (N_avg=32 @M=4000), robustness set (N=16 @M=400), ≥12/16 STABLE threshold, per-cell remedy | part of config_hash / prereg |
| **P2 config** (§1.2) | Tc∈{1,2,4}×M∈{400,4000}, n=40/arm, bootstrap (10000, rng=999, 90%CI), R-ratio criteria, action table | part of config_hash / prereg |
| **Anomaly SOP** (§8) | the frozen state machine + amendment rule | part of prereg |
| **OC simulation script + expected-OC report** (§9) | the joint full-loop simulator, scenarios, and predeclared acceptance criteria | part of prereg (new artifact) |
| **Baseline / equal-arm conditions** (§2.1, §6.1) | the Q1 option chosen (default option 2) + its licensing conditions | part of prereg |
| **Stale-prose flag (law #4):** `CFG["scout"]` comments + `pilot_pair` docstring hard-code "B=64 floor" | Update to B_conf = 96/128 wherever the floor is quoted; the selftest grep-check (law #4) must grep the **operative** t-convention + B_conf **and the new `INCONCLUSIVE_AT_CEILING` label + P1/P2 thresholds** — not the stale 24/32, 48/64, B=64 strings | part of config_hash / prereg |

**Claim limits (Q7 item 8 — frozen, stated explicitly):**
- **A GREEN is candidate-selection**, not a measured contrast, until the Movement-3 two-sample contrast is run at that cell.
- **A raw-current RED is not automatically a contrast RED** — it becomes a contrast statement only under the baseline/equal-arm condition (option 1/3 or Movement 3).
- **The all-RED pivot (option 2) claims raw mismatch currents are sub-floor** across the accessible design space; it does **not** claim the tunable contrast is bounded sub-floor.
- **A Tc>1 GREEN requires a measured two-sample contrast** at confirmatory (estimand-(a) refused as Tc contrast licensing).

**Unchanged and hash-frozen:** the forward-path harness (`pilot_pair`, Tc threading, the v4.3-inherited estimator), the six cells + geometry, the `v44pilot::` seed namespace, and the never-pooled rule. This is an **analysis + declaration recalibration**, not a physics-instrument edit. Re-issue per law #1: regenerate `prereg_v44.json` from `--plan`, record new `config_hash` + `source_sha` + prereg sha256, verify readback, **then** run — **P1 and P2 first, OC simulation passes, scout last.**

---

## 11. Ratification checklist + genuine forks left for Anthony

**Resolved into spec (maps to ChatGPT Q1–Q7 → §12).** Every BLOCK/AMEND disposition has a frozen repair above.

**Genuine forks — HQ recommends, Anthony ratifies (these are not settled):**

1. **Q1 contrast-licensing option (the big one).** HQ writes v3.1 around **option 2** (all-RED pivot = raw-current claim only; contrast belongs to Movement 3). Alternatives fully documented: **option 1** (pre-scout equal-arm calibration gates at (1,1)@Tc1, (2,2)@Tc1, (2,2)@Tc2, (2,2)@Tc4 with a predeclared negligibility bound → licenses a contrast pivot) and **option 3** (measure the equal arm in-scout, two-sample → every band is a contrast, ~2× compute). **HQ rec: option 2** — cheapest, honest, and the contrast is Movement 3's declared job anyway.
2. **The Q4 operating point (the headline consequence).** The INCONCLUSIVE_AT_CEILING repair drops correct-pivot-under-null from ~97.5% to **~38%**, with ~55% legitimate INCONCLUSIVE at B_max=128. **Fork:** accept the ~38%-pivot / ~55%-inconclusive operating point, OR raise B_max / add seed-averaged-grids-per-block to resolve more cells. **HQ rec: accept it** — INCONCLUSIVE is honorable; chasing a higher pivot rate spends the honesty the Q4 repair bought.
3. **P1 seed sets + threshold.** HQ proposes N_avg=32 (77001–77032 @M4000) for σ_cell, N=16 robustness (78001–78016 @M400), STABLE ≥12/16. Revisable: exact seeds, N_avg, robustness N, threshold fraction.
4. **P2 estimator + criteria.** HQ proposes Tc∈{1,2,4} (v3 had {1,4}), n=40/arm (→80 on inconclusive), bootstrap 10000/rng999/90%CI, material-grid ⇔ R CI-lower > 1.10, equivalence band [0.909, 1.10]. Revisable: the ±10% margin, n, the Tc set.
5. **OC acceptance tolerances (§9.3).** HQ proposes false-GREEN ≤0.01, invalid-pivot ≤0.02 (floor) / ≤0.005 (≥2× floor), compound GREEN power ≥0.90 at 3× floor, wrong-sign flag ≥0.90; correct-pivot advisory ≥0.30. Revisable numbers.
6. **Equal-arm choice (§6.1).** HQ adopts τy-matched at matched-Tc (Q6-i). Alternatives: (τx,τx)-matched or dual-reference.
7. **B_max = 128** (Q6-ii adopted) — revisable at ratification; couples to Movement-3 compute budget.

---

## 12. ChatGPT Q1–Q7 reconciliation table

| ChatGPT Q | v3 disposition | v3.1 resolution | Where |
|---|---|---|---|
| **Q1** — contrast-proxy estimand | AMEND-BEFORE-REGISTRATION | All-RED pivot restricted to a **raw-current claim** (option 2, HQ-rec-pending-Anthony); options 1 & 3 documented with the four calibration configs + negligibility bound; **estimand-(a) refused as contrast licensing for Tc>1**; GREEN is candidate-selection; claim-class coupling added (D5, coupling 4) | §2.1, §5, §6.1, §10, fork 1 |
| **Q2** — four-band / ANOMALOUS disposition | AMEND-BEFORE-REGISTRATION | **Frozen anomaly-resolution state machine** with a predeclared 3-way discriminator (higher-M survival → P1-reference robustness → grid-artifact / true-opposite-physics / sign-precondition-failure / unresolved); amendment rule (no informal re-band); false-anomaly rate **corrected ~26% → ~14.1%** as a planning approximation (independence, conservative) | §8, §3 anomaly-rate note |
| **Q3** — RED conjunction / MC | PASS | **Kept exactly** (verbatim substance of v3 §3.3; Antigravity R2 reproduced the 4M-draw MC); added the **two documentation caveats** (MC validates local false-null only, not the six-cell loop; assumes cell-SD ≈ equal-arm SD) | §3.3 |
| **Q4** — sequential loop / pivot | BLOCK | `RED_AT_CEILING` → **`INCONCLUSIVE_AT_CEILING` that BLOCKS the pivot**; **four honest terminal outcomes**; pivot condition (0′) added; pseudocode terminal set = `"RED"` only; consequence surfaced as fork 2 | §3, §4, §5, §7 |
| **Q5-P1** | BLOCK | **Killed the ambiguity:** σ_cell = sign of **high-M (M=4000) seed-averaged ROI curl** (average-then-curl, single sign); **STABLE iff ≥12/16 predeclared M=400 per-seed curls agree with σ_cell** (against the high-res reference, not itself); exact seed sets pinned; failing cells excluded until predeclared remedy | §1.1, fork 3 |
| **Q5-P2** | BLOCK | **Fully operationalized gate:** n=40/arm, block-SD + percentile bootstrap (10000, rng999, 90%CI), R(Tc)=SD400/SD4000, material-grid ⇔ CI-lower>1.10, equivalence band [0.909,1.10], **action table** incl. inconclusive branch; **pending conflict resolved — P2 completes before the scout, Tc M + claim class frozen** | §1.2, fork 4 |
| **Q6** — open leans | Leans below | **Adopted (revisable):** τy-matched equal arm at matched-Tc (conditional on Q1); B_max=128 with terminal AMBER inconclusive; refuse estimand-(a) contrast for Tc>1; first-pass 16 blocks; the P1 high-M/robustness pin | §1.1, §4, §6.1, forks 3/6/7 |
| **Q7** — re-issue scope / claim limits | BLOCK | **Claim limits stated** (GREEN=candidate-selection; raw-current RED ≠ contrast RED without baseline); **prereg scope expanded** to OC sim script, expected-OC report, P1/P2 config, anomaly SOP, baseline/equal-arm conditions; **boundary/cutpoint selftests** specified; **grep extended** to the new label + P1/P2 thresholds | §9, §10 |

---

## 13. Antigravity reconciliation (carried; R2 cleared v3)

Antigravity's **Round-2** pre-reg audit (`AUDIT_VERDICT_ANTIGRAVITY_R2.md`, Gemini 3.5 Flash) audited **v3** (commit `138d109`) and returned **"RATIFIABLE AS-IS"**: all six R1 findings CONFIRMED CLOSED, and the §3.3 4M-draw Monte Carlo reproduced (3.951% / 18.860% / 4.933% / 3.951%). **Note (law #7 — external output is input, HQ diffs):** AG R2 **normalized the (then-invalid) Q4 `RED_AT_CEILING` state** in its Finding-1 null simulation (it reported cells resolving "RED (85.2%) or RED-at-ceiling (12.3%) → combined 97.5%" as a *pass*), i.e. AG did not independently catch the Q4 invalid conversion that ChatGPT BLOCKED. v3.1's Q4 repair supersedes that normalization: under `INCONCLUSIVE_AT_CEILING`, the 12.3% ceiling cells **block** the pivot, so the null-run correct-pivot rate is ~38%, not 97.5% (§9.3). AG's leans (τy-matched equal arm, B_max=128, refuse Tc>1 estimand-(a), adopt 16 blocks, averaging-then-curl + ≥75% seed agreement) all align with the Q6 adoptions above.

AG's own R2 numbers that v3.1 folds in: per-cell false-anomaly **2.51%**, six-cell **14.1%** (AG confirmed this independently — it is the figure v3.1 uses, correcting v3's 26%).

**Re-audit target for the next Antigravity pass:** this document (v3.1), specifically (a) the Q4 `INCONCLUSIVE_AT_CEILING` blocking behavior and its ~38%/~55% operating point, (b) the §8 anomaly state machine's 3-way discriminator, (c) the §1.1 P1 high-M-reference stability pin, (d) the §1.2 P2 gate action table, and (e) the §9 OC simulation acceptance criteria (which AG should re-derive, as it did for §3.3).

---

*End v3.1 draft. Status: DRAFT for ChatGPT re-review + Antigravity re-audit + Anthony final-say. Not registered, not chronicled, no harness bytes edited. v3 (`138d109`) and `v44_scout.py` (`source_sha 0b65a9ee92b9fe2c`) remain hash-frozen.*
