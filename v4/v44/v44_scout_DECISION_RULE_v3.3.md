# v4.4 Scout — Decision Rule v3.3 (whole-object-scope revision of v3.2, for re-review + ratification)

*HQ (Mac Studio Claude Code seat, overwatch/provenance), 2026-07-08. **This is a DRAFT for re-review (ChatGPT methodology) + Antigravity re-audit + Anthony final-say. It is NOT registered, NOT chronicled, and edits NO harness bytes.** It revises `v44_scout_DECISION_RULE_v3.2.md` (a draft, not frozen) to clear the v3.2 whole-object scope audit — one blocker (statistic-axis over-scope of the pivot claim, found independently by three review passes) plus two majors (cell-roster demotion leak; under-powered §8 vanish test). The frozen v4.3 artifacts, the `v44_scout.py` physics path, v3 (`138d109`), v3.1, and v3.2 are **not modified** — this is a new file. Every ChatGPT Q1–Q7 disposition v3.1/v3.2 satisfied stays satisfied (§12), and every v3.1-re-pass repair v3.2 made stays in force (§14). The v3.2→v3.3 changes are keyed to a reconciliation table (§16). All numeric thresholds are grep-consistent (experimental law #4); every change from v3.2 is flagged inline as **[v3.3]**. All §0 decisions remain revisable at re-review / audit / Anthony final-say.*

---

## ★ STANDING RULE (extended in v3.3 — the recurring category error, now stated over ALL THREE AXES)

> **A null / RED / pivot claim must bound the effect MAGNITUDE over the WHOLE claimed object — all directions, all statistics named in the claim, and all cells in the claim denominator — never a projection and never a silently-shrunk subset. If a cell is demoted or excluded, the claim MUST shrink to the surviving design points, and pivot membership MUST be pinned in the pseudocode.**
>
> "Absence of a predicted-direction signal" is **not** "evidence of absence of an effect." The same category error has now been caught on **three axes**, once per revision:
> - **Compute-ceiling axis** (v3 → v3.1, ChatGPT Q4): an AMBER at the compute ceiling was converted into `RED_AT_CEILING` and counted as a null. Repaired by `INCONCLUSIVE_AT_CEILING` blocking the pivot.
> - **Direction axis** (v3.1 → v3.2, HQ re-pass BLOCK): a one-sided RED bounded only the sign-aligned component `x = σ·μ̂`, never `|μ̂|`, so a real opposite-direction current at floor could band RED. Repaired by the **RED magnitude bound** (§3).
> - **[v3.3] Statistic axis** (v3.2 → v3.3, whole-object audit BLOCKER): the pivot claim said "raw mismatch **currents** are sub-floor" while bounding only **one statistic** (`quad_loop_rate`); `omega_roi` — near-equal stated sensitivity (0.83 vs 0.90, §1.3) and the carrier of the 2.2σ κ-suppression lean — was descriptive and could sit GREEN without blocking the pivot. Repaired by **scoping the claim to the quad_loop_rate statistic** AND the **omega veto** (§5(iii)): a descriptive omega GREEN or ANOMALOUS in any gating cell blocks the pivot.
> - **[v3.3] Cell-roster axis** (v3.2 → v3.3, whole-object audit MAJOR): a P2-demoted DESCRIPTIVE Tc cell "does not gate the pivot," but the claim text stayed frozen at "the six cells ≈ four independent design points" — a null over 4 design points could be minted from bounds on 2 or 3. Repaired by **roster-parametric claim scope** (§2.1): the claim shrinks to the surviving design points, `pivot_licensed()` **asserts the registered gating roster** (§7), and every demoted-cell outcome has a pinned disposition (§1.2).
>
> Whenever a future rule declares a null, grep it against this sentence on ALL THREE AXES: does the condition bound `|μ̂|` (not the projection)? does the claim name exactly the statistic(s) actually bounded? does the claim denominator equal the set of cells that actually gated?

---

## CHANGE SUMMARY — what v3.3 changes vs v3.2 (whole-object scope audit: 1 blocker + 2 majors)

| # | v3.2 state | v3.3 repair | § |
|---|---|---|---|
| **BLOCKER (statistic axis; 3 independent passes)** | Pivot claim worded "raw mismatch **currents** are sub-floor at the probed configurations" with no per-statistic qualifier; only `quad_loop_rate` is bounded; `omega_roi` is descriptive and **excluded** from `pivot_licensed` — an omega GREEN at +2×floor (physically realizable: counter-rotating loop pairs cancel loop-rate while leaving net ROI vorticity; precedent: v4.3's real effect loaded on occupancy alone) cannot block the pivot. The quad-vs-omega axis, already caught once in this program, recurring in the claim language. | **(a) Claim scoped to the statistic:** every pivot-claim instance now reads "sub-floor **in the `quad_loop_rate` statistic**" (§2.1, §5, §10). `occupancy_x` named as recorded-and-unbounded. **(b) Omega veto (pivot-blocking, HQ-rec over annotate-only — fork 10):** a descriptive `omega_roi` GREEN **or** ANOMALOUS in any gating cell **blocks the pivot** (§5(iii)), is HQ-flagged, and routes to disposition (omega GREEN → Movement-3 omega candidate consideration; omega ANOMALOUS → §8-style investigation). `pivot_licensed()` consumes the omega bands (§7). Failability selftest added (S8, gate 8). | §0.2 D1′, §2.1, §5, §7, §9, §10 |
| **MAJOR (cell-roster axis — the demotion leak)** | §1.2 can demote AxT2/AxT4 to DESCRIPTIVE ("does not gate the pivot"), but the claim text is frozen unconditionally at "the six cells ≈ four independent design points"; the gating set for conditions (0)/(i) is undefined under demotion; `pivot_licensed()` has no roster assertion; a demoted cell's GREEN/INCONCLUSIVE has no pinned effect. A null over 4 design points could be minted from bounds on 2. | **Roster-parametric claim:** the pivot claim covers exactly the **surviving design points of the registered post-P2 gating roster** (§2.1 map + shrink rule); "six cells ≈ four points" is now the **no-demotion case only**. `pivot_licensed()` **asserts** `set(gating cells) == registered_gating_roster` (§7). Demoted-cell dispositions pinned (§1.2): primary GREEN → forces outcome 1 (no pivot); ANOMALOUS → §8, blocks pivot; RED/AMBER/`INCONCLUSIVE_AT_CEILING` → recorded, non-gating, **mandatory verdict caveat** that its design point is unbounded. Demotion selftest added (S9). | §1.2, §2.1, §5, §6.1, §7, §9 |
| **MAJOR (§8 vanish test under-powered)** | STATE B mints GRID-ARTIFACT when wrong-sign significance fails ONE higher-M rerun with **no predeclared n**; at the 16-block SE a real −1×floor current falsely "vanishes" ~39.5% of the time (screen power ~0.61), silently discarding the TRUE-OPPOSITE-PHYSICS escalation ~39% of the time it surfaces, and the reband re-enters the pivot pool — a channel omitted from §13's 0.0066 and not explicitly required in §9 S5. | **Powered vanish test:** STATE B rerun predeclared at **n_rerun = 40 fresh blocks** under the cell's predeclared remedy recipe (precond namespace), one-sided t₃₉ = 1.685, SE = sd·√(1/40+1/64) = 0.2016·sd → **measured power 0.912 ≥ 0.90 at −1×floor** (MC this session, §13; hard gate 9). Residual mislabel ≈ 0.088 (was 0.395). **§9 S5 must simulate the full §8 rerun/reband loop**, and gate 5's number of record **includes the reband channel** (analytic est: extra cell-RED ≈ 0.0025; invalid pivot ≈ 0.0066 → ≈ 0.007, still ≤ 0.02). | §8, §9.1, §9.2 S5, §9.3, §13 |

**Kept from v3.2 unchanged (HQ-recommended-pending-Anthony):** the STANDING RULE's direction-axis repair (RED magnitude bound, §3/§3.3/§7), belt-and-suspenders (magnitude bound + STABLE, couple 5), restated hard gates 5/5′, the honest joint-to-joint headline (0.808→0.349→0.148, now further reduced by the omega veto — §13), the Student-t₁₅ false-anomaly correction, SE_FACTOR n=8 = 0.375, two-sided-RED-unreachability documentation, and everything §12/§14 list as preserved from v3.1.

---

## CHANGE SUMMARY (historical) — what v3.2 changed vs v3.1

*Retained verbatim from v3.2 for the audit trail; see the v3.2 file for the full table (re-pass BLOCK: RED magnitude bound; belt-and-suspenders STABLE modeling; hard gates 5a/5b restated as joint invalid-pivot bounds 5/5′; pivot claim scoped to probed configurations; honest joint-to-joint headline; Student-t₁₅ / SE_FACTOR / two-sided-RED corrections). All of it remains in force in v3.3.*

---

## 0. Identity + adopted decisions

### 0.1 Instrument identity (verify before any run — unchanged from v3.1/v3.2)

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

### 0.2 Adopted decisions (all revisable at re-review / Anthony — D1′ amended in v3.3)

| # | Decision | Value | Rationale / coupling |
|---|---|---|---|
| D1 | Primary statistic | `quad_loop_rate` | Continuity with the v4.3 **G1 vortex-control calibration**. Rests on that continuity, **not** on the 2.2σ κ-suppression point estimate (§1.3). **The pivot claim is scoped to this statistic (§2.1) — [v3.3].** |
| D1′ | Secondary statistic | `omega_roi` — **descriptive band + pivot veto [v3.3]** | Banded through the same `band_cell()` arithmetic for the record; **does not certify** the pivot claim (the claim never asserts an omega bound), **but an omega GREEN or omega ANOMALOUS in any gating cell BLOCKS the pivot** (§5(iii)) — omega has near-equal stated sensitivity (0.83 vs 0.90, §1.3) and carried the 2.2σ κ-suppression lean; a super-floor current visible in the scout's own recorded secondary statistic must never coexist with a minted null. `occupancy_x` recorded, **not banded, explicitly unbounded by any claim** (§2.1). *(v3.2: omega was descriptive-only and excluded from `pivot_licensed` — the statistic-axis leak.)* |
| D2 | First-pass blocks | **16** per cell | At 8 blocks RED is unreachable (κ<0, §3.3); 16 gives a usable first surface. (Q6-iv adopted.) |
| D3 | M_grid | **400** for geometric cells A/B/C/D, **GATED** on P1 sign-stability (§1.1). Tc cells AxT2/AxT4 **M frozen by P2 before the scout** (§1.2). | M does **not** lower the floor (DIAG 1); the M concern is grid-generated-signal fidelity, addressed by blocks/seed-averaging. |
| D4 | B_conf (floor projection) | **96** working default; escalation 96→128 ceiling for persistent AMBER (§4). | floor(96)=0.557·sd, floor(128)=0.482·sd. |
| D5 | Estimand | **Option (a)** — raw mismatch current as **screening/triage** statistic | μ̂ vs two-arm floor(B_conf); honest SE = sd·√(1/B_scout + 1/64). Restricts what (a) may claim (Q1): sizes a candidate signal and licenses a **raw-current** pivot only — **not** the mismatch-minus-equal contrast (§2.1, §5). |

### 0.3 Six couplings that must not drift apart (sixth added in v3.3)

1. **sign precondition ↔ per-cell predicted signs ↔ pivot license** — one chain (§1.1, §6.2, §5).
2. **estimand ↔ B_conf ↔ AMBER escalation ceiling** — share `floor_c` (§2, §4, §5).
3. **M_grid ↔ primary statistic** — one decision: quad@M400 (D1+D3; §1.3).
4. **claim class ↔ what was measured** (Q1/Q7) — a raw-current RED pivot is a raw-current claim; a contrast claim requires the equal arm; a Tc GREEN requires a measured two-sample contrast at confirmatory (§2.1, §5, §10).
5. **RED magnitude bound ↔ STABLE gate ↔ wrong-sign protection** (v3.2) — the belt (`|μ̂|` bound, §3) and the suspenders (STABLE, §1.1/§5(ii)) are **one** wrong-sign guarantee, measured jointly by the OC sim (§9). Neither may be relaxed without re-measuring the joint invalid-pivot rate.
6. **[v3.3] claim scope ↔ gating roster ↔ omega veto** — the pivot claim's statistic qualifier ("in `quad_loop_rate`", §2.1), its cell denominator (the registered post-P2 gating roster and its surviving design points, §1.2/§2.1), and the omega veto (§5(iii)) are **one** whole-object guarantee: the claim covers exactly what was bounded, `pivot_licensed()` asserts the roster and consumes the omega bands (§7), and the S8/S9 selftests prove both can FAIL (§9.2, law #2). None may drift without re-issuing the claim text.

---

## 1. Precondition runs (gate the scout — complete and register BEFORE the scout)

These are **diagnostics, not scout results**. They run the mean-field / equal-τ rig in a declared, quarantined precondition namespace (`precond_P1::`, `precond_P2::`), **NEVER** pooled into `v44pilot::` or any confirmatory (experimental law #6). Their outputs are registered as part of the frozen prereg, because the scout's banding, pivot license, and claim class depend on them. **Both preconditions must terminate and register before the scout is licensed** (P2 finishes first, then the Tc-cell M, claim class, **and the gating roster + surviving-design-point claim scope [v3.3]** are frozen — §1.2).

### 1.1 Precondition P1 — per-cell predicted signs + sign-stability (fully pinned — Q5-P1; unchanged from v3.2)

The v3 spec carried an open ambiguity ("average-then-curl" vs "per-seed unanimity"). ChatGPT (Q5) required it killed before registration, because `stable_cell` gates the pivot (§5). v3.1 froze ChatGPT's pin; v3.2 kept it verbatim and added the belt-and-suspenders coupling (couple 5); v3.3 keeps all of it verbatim.

**P1-A — register the directional prediction σ_cell (the physical, mean-field object):**
- For each of the six cells, compute the **ROI-integrated curl of the seed-averaged mean aniso force field at M=4000** — **average-then-curl**: average the aniso force field over a predeclared high-M seed set into one mean field, then take the single ROI mixed-partial. One sign per cell.
- **σ_cell ∈ {+, −}** := sign of that high-M seed-averaged ROI curl. A cell with a high-M curl indistinguishable from 0 (below a predeclared negligibility floor) registers **σ_cell = INDETERMINATE** and bands **two-sided** (§3).
- **Predeclared high-M reference set (HQ proposal, revisable — fork §11):** average over **N_avg = 32** seeds `precond_P1::77001…77032` at **M=4000**. σ_cell = sign of the ROI curl of that averaged field.

**P1-B — the sign-stability robustness test (STABLE against a higher-resolution reference, not against itself):**
- Take a **separate, disjoint, predeclared seed set**, evaluate the ROI curl **per seed at M=400** (the scout's operating resolution).
- **STABLE iff ≥ 75% of those M=400 per-seed curls agree in sign with the registered high-M σ_cell.**
- **Predeclared robustness set + threshold (HQ proposal, revisable — fork §11):** **N = 16** seeds `precond_P1::78001…78016` at M=400; **STABLE iff ≥ 12/16** agree in sign with σ_cell.

**Consequence for the pivot (frozen):** a cell with **`stable_cell = UNSTABLE`** (< 12/16) **does not count toward the all-RED pivot** from an M=400 null (§5). It may only count after a **predeclared remedy** runs (r1 higher M per block, or r2 seed-averaged grids per block), following the amendment path (§8 step 4). No informal reclassification.

**Why STABLE is the *suspenders* of the wrong-sign protection (v3.2 — retained verbatim):** the aniso current is *generated by* the grid curl (receipt 07). A **real opposite-direction current** — the exact object the RED magnitude bound (belt, §3) blocks from banding RED — is also the object P1-B is built to catch: because P1-B's per-seed M=400 curls **share the underlying current** with the scout, a cell whose true current opposes its registered σ_cell will tend to fail the ≥12/16 agreement and register **UNSTABLE**, so §5(ii) excludes it from the pivot even in the residual fraction where the belt lets it band RED. **The two layers are one guarantee (couple 5):** belt = "a wrong-sign super-floor current cannot band RED"; suspenders = "even a residual wrong-sign RED sits on an UNSTABLE cell and is excluded." The OC sim (§9) **models P1-B STABLE from coupled M=400 draws that share the scout's underlying current** (with a stated, sensitivity-tested coupling) and **measures the joint** wrong-sign invalid-pivot rate.

**Note (receipt 07, unchanged):** the quick per-seed SNR metric is *informative but not the instrument* — a single grid's ROI curl is noise-dominated at both M=400 and M=4000. Average-then-curl at high M establishes σ_cell; the per-seed check does not substitute for it.

### 1.2 Precondition P2 — crossed Tc×M diagnostic, operationalized as a GATE (Q5-P2 — action table's demotion consequences PINNED in v3.3)

Crossed `{Tc ∈ 1, 2, 4} × {M ∈ 400, 4000}` = **6 arms**, equal-τ, same rig as receipt 06 (DIAG 2). P2 **completes before the scout**; its output **freezes the Tc-cell M, claim class, and — [v3.3] — the GATING ROSTER and the pivot claim's surviving design points** into the registered prereg.

**Frozen estimator + sampling (HQ proposal, revisable — fork §11):**
- **n = 40 blocks/arm** (registration-grade).
- **SD estimator:** sample block-SD of the per-block primary statistic (`quad_loop_rate`), per arm.
- **Bootstrap:** percentile bootstrap, **10 000 resamples**, **rng pinned = 999**, **90% two-sided CI** on every ratio.

**M-sensitivity statistic.** `R(Tc) = SD(Tc, M=400) / SD(Tc, M=4000)`. R ≈ 1 ⇒ M-invariant → M=400 adequate. R > 1 ⇒ grid-noise contribution → M=400 inflates the floor.

**Frozen criteria (HQ proposal, revisable — fork §11):**
- **Material grid-noise contribution** ⇔ the **90% CI lower bound of R(Tc) > 1.10**.
- **M-invariant enough** ⇔ the **90% CI for R(Tc) lies entirely within [0.909, 1.10]** (TOST equivalence, ±10%).
- **Inconclusive** ⇔ neither.

**Action table (frozen — every branch predeclared; demotion consequences pinned [v3.3]):**

| P2 result for a Tc cell | Higher-M feasible? | Frozen action → registered into prereg |
|---|---|---|
| **M-invariant** (equivalence passes) | — | Tc cell runs at **M=400**; claim class = **full-sensitivity probe** (still subject to the Tc contrast refusal, §2.1). Cell stays in the **gating roster**. |
| **Material grid-noise** | yes | Tc cell runs at the **M that restores equivalence** (default M=4000); claim class = full-sensitivity probe. Cell stays in the **gating roster**. |
| **Material grid-noise** | no | Tc cell **demoted to DESCRIPTIVE** — full consequences pinned below **[v3.3]**. |
| **Inconclusive** | — | **Bump n once** to **n = 80/arm** and re-test. Still inconclusive ⇒ **demote to DESCRIPTIVE** (same pinned consequences). |

**[v3.3] DEMOTION CONSEQUENCES (pinned — closes the cell-roster leak; new in v3.3, every clause frozen):**

A cell demoted to DESCRIPTIVE by this table:

1. **Leaves the gating roster.** The **registered post-P2 gating roster** = the six cells minus demoted cells; it is written into the prereg as an explicit list and **asserted by `pivot_licensed()`** (§7). Conditions 0/0′/(i)/(ii)/(iii) of §5 quantify over **exactly** this roster.
2. **Shrinks the pivot claim.** Its design point(s) (§2.1 map: AxT2 alone carries (τy=2, Tc=2); AxT4 alone carries (τy=2, Tc=4)) are **REMOVED from the pivot claim scope**. The claim text is roster-parametric (§2.1): a null is asserted over the **surviving** design points only — never over a point that was probed only descriptively. *(v3.2 froze "the six cells ≈ four independent design points" unconditionally — a null over 4 points could be minted from bounds on 2. Closed.)*
3. **Is still banded, for the record**, on both statistics, with its terminal band's disposition pinned:
   - **Primary (`quad_loop_rate`) GREEN** → **forces outcome 1** (candidate registration at that cell; **no pivot**). A candidate signal anywhere the scout looked — gating or demoted — is a candidate, never background to a null.
   - **Primary ANOMALOUS** → enters the §8 state machine and **blocks the pivot** (condition (0) quantifies over the gating roster, but a demoted-cell anomaly blocks via this clause) until dispositioned.
   - **`omega_roi` GREEN or ANOMALOUS** → triggers the omega veto (§5(iii)) exactly as on a gating cell: **blocks the pivot**, HQ-flagged.
   - **Primary RED / AMBER / `INCONCLUSIVE_AT_CEILING`** → **recorded, non-gating** (its design point is already outside the claim, so nothing is minted from it), **AND the verdict text MUST carry the caveat**: *"the demoted design point(s) {…} were probed descriptively only and remain unbounded."* Omission of this caveat is a law-#4 grep failure (§10).
4. **Selftest (law #2):** OC-sim scenario **S9** (§9.2) plants a real super-floor current at a demoted cell and asserts the pivot claim never covers its design point and a demoted-cell GREEN forces outcome 1.

**No pending state.** After P2 terminates, the Tc-cell M, claim class, gating roster, and surviving-design-point claim scope are **frozen constants** in the registered prereg.

### 1.3 Diagnostic language (frozen at n=20 reality — unchanged from v3.1/v3.2)

- **Floor is trajectory-limited even at scale 10** (DIAG 1: SD@400/SD@2000 = 1.19 [0.80,1.74] quad, 0.87 [0.61,1.25] omega). Raising M does **not** lower the floor.
- **κ-injection suppression is NOT established:** quad ratio 0.90 (~0.5σ); omega ratio 0.67 (~2.2σ uncorrected p≈0.03, does **not** survive Holm across ~8 diagnostic contrasts). The quad-primary choice (D1) rests on v4.3 G1-calibration continuity.
- **Net relative sensitivity at M=400:** quad ≈ 0.90, omega ≈ 0.83 → quad wins at M=400 (couples D1↔D3). **[v3.3] Note the corollary now enforced:** omega's 0.83 is close enough to quad's 0.90 that "sub-floor in quad" is nowhere near "sub-floor in omega" — which is exactly why the claim is statistic-scoped and the omega veto exists (§2.1, §5(iii)).

---

## 2. Estimand + exact thresholds

### 2.1 Pinned estimand — option (a), a **screening/triage** statistic (Q1 licensing repair; v3.3 scopes the pivot claim on the statistic AND cell axes)

μ̂ (per cell, per statistic) = the mean of the **raw mismatch current** over the scout blocks. It is a **screening proxy** that sizes a candidate signal. The honest SE folds in the v4.3 64-block equal-arm reference:

```
SE(B_scout) = sd_cell · √(1/B_scout + 1/64)
```

**Two distinct roles of "the equal arm" — do not conflate (auditor trip-wire, unchanged):**
1. **floor_c's SD source.** The scout runs **no equal arm**, so `floor_c` is projected from the cell's own measured block SD (`sd_cell`, n=B_scout) as a **homoscedastic proxy** for the confirmatory's equal-arm SD.
2. **The named equal-arm config (§6.1)** defines the **contrast estimand** and the confirmatory's second arm at Movement 3. Not used in the scout's floor arithmetic.

**Q1 — what estimand (a) may and may not claim (frozen; claim text re-scoped [v3.3]):**
- A **GREEN** sizes a **candidate signal**; it triggers Movement-3 registration, and **Movement 3 is the independent two-sample contrast test**. A GREEN is candidate-selection, not a measured contrast (§10 claim limits).
- An **all-RED pivot** is restricted to a **RAW-CURRENT claim** (ChatGPT **option 2**, HQ-recommended-pending-Anthony), with the **[v3.3] whole-object-scoped wording (frozen)**:

  > *"Raw mismatch currents are sub-floor **in the `quad_loop_rate` statistic** at the **N_g gating configurations** (the surviving design points **D_surv**), with `omega_roi` recorded and **not** GREEN/ANOMALOUS in any cell, and `occupancy_x` recorded and unbounded."*

  where **N_g** and **D_surv** are the registered post-P2 gating roster and its design points (§1.2). **In the no-demotion case** this instantiates to the v3.2 wording plus the statistic qualifier: the six cells, which — because A≡B and C≡D share the ROI mixed-partial to 4 s.f. (receipt 07) — constitute **≈ four independent design points** {(τy=2,Tc=1), (τy=1,Tc=1), (τy=2,Tc=2), (τy=2,Tc=4)}, NOT a continuum. **Under demotion the claim SHRINKS** per the design-point map below. The pivot **does not** claim coverage of interior or unprobed (τx, τy, Tc) values, does **not** bound `omega_roi` or `occupancy_x` (it asserts only that omega raised no veto), and is explicitly **not** a contrast claim; the contrast test belongs to Movement 3.

  **[v3.3] Design-point map (frozen — the claim-shrink arithmetic):**

  | Cell(s) | Design point carried | If demoted (§1.2), point survives via |
  |---|---|---|
  | A, B | (τy=2.0, Tc=1) | the other of {A, B} (never both demoted — P2 acts on Tc cells only) |
  | C, D | (τy=1.0, Tc=1) | the other of {C, D} (same) |
  | AxT2 | (τy=2.0, Tc=2) | **nothing — point leaves the claim** |
  | AxT4 | (τy=2.0, Tc=4) | **nothing — point leaves the claim** |

  *(v3.2 asserted "the six cells ≈ four independent design points" unconditionally in §2.1/§5/§10 while §1.2 could shrink the gating set — the cell-roster leak. Closed: the claim is a function of the roster.)*
- **Tc cells (Tc>1): estimand-(a) is REFUSED as contrast licensing (Q6-iii, frozen).** Any high-Tc GREEN requires a **measured two-sample contrast** (estimand (c)) at confirmatory.

> **Scope note (v3.2, retained — keep two "independences" apart).** "≈ four independent design points" is a **claim-scope** statement about *physical* design-space coverage (the mixed-partial degeneracy A≡B, C≡D). It is **NOT** a statement about stochastic-noise independence. The OC-sim operating-characteristic rates (§9, §13) are computed with **independent per-cell block noise** — that model reproduces the receipt-06 anchors (§13). Do **not** apply the four-points degeneracy to soften any stochastic rate; whether the block noise is itself correlated across A≡B/C≡D is a separate OC-sim modelling decision (§9.1, flagged).

> **[v3.3] Statistic-scope note (the blocker, closed).** The claim names **one** bounded statistic. `omega_roi` — near-equal stated sensitivity (0.83 vs quad 0.90, §1.3), the carrier of the 2.2σ κ-suppression lean, and physically capable of carrying a current that `quad_loop_rate` misses (counter-rotating loop pairs cancel loop-rate while leaving net ROI vorticity; precedent: v4.3's real effect loaded on occupancy alone) — is **not bounded** by the pivot and the claim must never say "currents" unqualified. What the pivot DOES assert about omega is the **veto clause**: omega was banded in every cell and was nowhere GREEN or ANOMALOUS (§5(iii)). `occupancy_x` is recorded and appears in the claim only as "recorded and unbounded."

**Options for the contrast-licensing question (Anthony ratifies — fork §11).** HQ writes v3.3 around **option 2**. Options 1 (pre-scout equal-arm calibration gates at (1,1)@Tc1, (2,2)@Tc1, (2,2)@Tc2, (2,2)@Tc4 with a predeclared negligibility bound) and 3 (in-scout two-sample, ~2× compute) are documented as in v3.1 §2.1 and remain available. If Anthony picks 1 or 3, the raw-current restriction upgrades to a contrast claim and §6.1's equal arm becomes operative.

### 2.2 Frozen convention (law #4 grep-consistency — unchanged from v3.1/v3.2)

One-sided **Student-t at (n−1) df, α=0.05** for GREEN/RED in the predicted direction; two-sided Student-t at (n−1) df, α=0.05 for INDETERMINATE-sign cells.

| df (n−1) | one-sided t (0.95) | two-sided t (0.975) |
|---|---|---|
| 7  (8 blocks)  | 1.895 | 2.365 |
| 15 (16 blocks) | **1.753** | **2.131** |
| 31 (32 blocks) | 1.696 | 2.040 |
| **39 (40 blocks) [v3.3 — §8 powered rerun]** | **1.685** | 2.023 |

### 2.3 Exact thresholds table (v3.2 magnitude-bound column retained; all grep-consistent)

`floor_c` and `SE` are in units of the cell's own block SD, `sd_cell`. GREEN threshold on the aligned `x`: `floor_c + t·SE`. **RED requires `|μ̂| < floor_c − t·SE = κ`** (point-governed where κ>0; §3.3 for the coupled-upper conjunction) — a **magnitude** bound, symmetric in μ̂.

| Config (blocks / B_conf) | floor_c | SE = sd·√(1/B+1/64) | **GREEN x >** (1-sided) | **GREEN \|μ̂\| >** (2-sided) | **RED \|μ̂\| < κ (magnitude bound)** |
|---|---|---|---|---|---|
| **16 / 96  (OPERATIVE first pass)** | 0.557·sd | 0.2795·sd | **1.047·sd = 1.88× floor** | 1.153·sd = 2.07× floor | **0.067·sd** (one-sided κ) — two-sided κ = **−0.039 < 0 → RED unreachable** |
| 8 / 96   (legacy-block reference) | 0.557·sd | **0.3750·sd** | 1.267·sd = 2.28× floor | 1.444·sd | one-sided κ<0 → **unreachable** |
| 32 / 96  (AMBER block-extension) | 0.557·sd | 0.2165·sd | 0.924·sd = 1.66× floor | 0.998·sd | one-sided κ = **0.190·sd**; two-sided κ = **0.115·sd** (reachable) |
| 32 / 128 (AMBER B_conf escalation, ceiling) | 0.482·sd | 0.2165·sd | 0.849·sd = 1.76× floor | 0.924·sd | one-sided κ = **0.115·sd** |
| **40 / 96 [v3.3 — §8 powered vanish-test rerun (significance test against 0 only; not a banding config)]** | 0.557·sd | **0.2016·sd** | *(n/a — rerun tests significance against 0: fires at \|x\| > t·SE = 1.685·0.2016 = **0.340·sd**)* | *(n/a)* | *(n/a)* |
| *8 / 64 (v2 legacy reference only)* | *0.682·sd* | *0.375·sd* | *1.393·sd = 2.04× floor* | *1.569·sd* | *unreachable (κ<0)* |

**Operative frozen GREEN for the primary (`quad_loop_rate`, 16 blocks, B_conf=96, one-sided): x = σ·μ̂ > 1.047·sd_cell (= 1.88× floor(96)).**
**Operative frozen RED (16 blocks, B_conf=96): `|μ̂| < 0.067·sd_cell`** (magnitude-bounded; point governs at κ>0).

> **Two-sided RED unreachability (v3.2 documentation, retained).** An INDETERMINATE-sign cell uses the two-sided t (2.131 at 16b), giving κ_2s(16/96) = 0.557 − 2.131·0.2795 = **−0.039 < 0**: an INDETERMINATE cell **can never band RED on the 16-block first pass** and must extend. Two-sided RED becomes reachable only at 32 blocks (κ_2s(32/96) = 0.557 − 2.040·0.2165 = **+0.115 > 0**, i.e. `|μ̂| < 0.115`). The one-sided RED magnitude bound is the **same** `|μ̂|` test with the one-sided t (κ = +0.067 > 0, reachable at 16b) plus the ANOMALOUS carve-out.

---

## 3. The four-band rule (exact inequalities — v3.2 magnitude bound retained verbatim; omega's role re-pinned [v3.3])

Banded on the **primary statistic** (`quad_loop_rate`); **[v3.3]** `omega_roi` gets the same arithmetic and its bands are **recorded AND consumed by the omega veto (§5(iii))** — an omega band never *certifies* the pivot claim, but an omega GREEN/ANOMALOUS *blocks* it *(v3.2 said "descriptively (does not gate the pivot)" — superseded)*. Let `t = t*(n−1 df)` per §2.2, `SE` per §2.1, `floor_c` per §2.3, σ_cell the registered predicted sign (P1). Terminal ceiling label **`INCONCLUSIVE_AT_CEILING`** (Q4). For omega banding, σ_cell applies to the omega field's own P1-registered sign where declared, else two-sided **[v3.3 pin]**.

**One-sided cells (σ_cell ∈ {+,−}).** Aligned statistic `x = σ_cell · μ̂` (`x > 0` = predicted direction).

- **GREEN** — register a confirmatory (candidate-selection, §10): `x − t·SE > floor_c`.
- **RED** — bounded sub-floor **in magnitude** (v3.2 repair, retained; robust form §3.3): **BOTH** `x + t·SE < floor_c` (v3.1 aligned form, kept exactly) **AND** `|μ̂| + t·SE < floor_c` **AND** not ANOMALOUS.
- **ANOMALOUS** — a **significant** wrong-sign current; does **not** count toward the pivot; triggers the §8 state machine: `x < −t·SE` (significant against **0**, one-sided α=0.05).
- **AMBER** — none of the above; extend (§4).

> **The v3.2 RED repair, in one line (retained).** Because `|μ̂| ≥ x` always, the magnitude conjunction `|μ̂| + t·SE < floor_c` **implies** the aligned conjunction; the aligned form is kept explicitly (to preserve the Q3-PASS §3.3 verbatim), but the **magnitude conjunction is what binds**. A wrong-sign current at floor magnitude has `|μ̂| ≈ floor_c`, so it **cannot** band RED (it goes ANOMALOUS if significant, else AMBER). This is the STANDING RULE's direction axis enforced in the arithmetic.

**Partition (complete, no gap), one-sided:** with `κ = floor_c − t·SE > 0` at 16b/B96, RED = `|μ̂| < κ`; ANOMALOUS = `x < −t·SE`; GREEN = `x > floor_c + t·SE`; AMBER = the remainder. RED and ANOMALOUS are disjoint (RED requires `|μ̂| < κ < t·SE`, so `x > −κ > −t·SE`, never ANOMALOUS).

> **Finding-4 correction (Antigravity, retained).** ANOMALOUS keys on significance against **0** (`x < −t·SE`), not the floor magnitude. Together with the magnitude bound, the wrong-sign axis is covered by **two** disjoint mechanisms: significant wrong-sign → ANOMALOUS; small-but-real wrong-sign → excluded from RED by the `|μ̂|` bound (→ AMBER → ladder).

> **Anomaly-rate arithmetic (v3.2 — Student-t₁₅; retained verbatim in substance).** The honest SE = sd·√(1/16+1/64) = 0.2795·sd is conservative relative to μ̂'s true sampling SD = 0.25·sd, giving an effective ANOMALOUS z-threshold of 1.753·(0.2795/0.25) = 1.960; but the pivotal quantity is **t₁₅, not z**, so the **anomaly screen at 16b fires at ≈ 0.0344/cell** under a true null (the normal-approx 0.0251 is superseded). The magnitude bound routes borderline wrong-sign null cells (`μ̂ ∈ (−t·SE, −κ)`) through the AMBER ladder, so the **terminal per-cell false-anomaly is ≈ 0.048** (measured, §13). Six-cell, independent-noise: 1−(1−0.048)⁶ = **≈ 0.254**, which **exceeds the 0.20 soft cap** — reported honestly, **non-blocking** (a false anomaly **blocks** the pivot, never mints a wrong verdict); cap value 0.20-vs-0.30 is a deferred Anthony call (§11 fork 9). **Do not** apply the §2.1 four-points degeneracy to reduce 0.254. **[v3.3] The omega veto adds a further conservative blocking channel of the same character** — its null rates and the resulting joint pivot suppression are stated in §13 and measured by the OC sim (§9); the veto, like a false anomaly, can only block a pivot, never mint one.

**Two-sided cells (σ_cell = INDETERMINATE from P1).** Use the two-sided `t`; ANOMALOUS does not apply. RED is already a magnitude bound here:
- **GREEN**: `|μ̂| − t·SE > floor_c`.
- **RED**: `|μ̂| + t·SE < floor_c` (robust form §3.3) — **unreachable at 16b/B96** (κ_2s<0; §2.3), reachable at 32b.
- **AMBER**: otherwise.

### 3.1 GREEN meaning
The scouting-grade sign-aligned lower confidence bound clears the confirmatory's minimum detectable effect. **A GREEN is candidate-selection** (§10): it names where to run the Movement-3 two-sample contrast; it is not itself a measured contrast. **[v3.3]** This holds for a GREEN on a **demoted** cell too (§1.2: forces outcome 1), and an **omega** GREEN is a *veto + HQ-flagged omega candidate consideration* (§5(iii)), not a registered candidate by itself.

### 3.2 ANOMALOUS meaning
A **significant** wrong-direction current is a grid-artifact / transduction-breakdown / sign-precondition signal, carved out of RED so it cannot launder into the null bucket. It triggers the frozen §8 state machine (whose STATE-B vanish test is **powered** as of v3.3 — n_rerun=40, §8). The magnitude bound also catches *sub-significance* wrong-sign currents at floor magnitude, which ANOMALOUS (a significance screen) misses — see §5 and the belt-and-suspenders design (§1.1).

### 3.3 RED robustness — v3.1 coupled-upper conjunction kept EXACTLY (Q3 PASS), applied to `|μ̂|` (v3.2) — unchanged in v3.3

**The coupled-upper conjunction is unchanged from v3/v3.1 §3.3** (ChatGPT Q3 = PASS; Antigravity R2 reproduced the 4M-draw Monte Carlo). Reproduced in substance:

- v2's mental model was **coupled** (a single `sd` moving `floor_c` and `SE` together); upper-sd makes RED harder only while κ = floor_c − t·SE ≤ 0 (true at 8 blocks).
- At **16-block / B_conf=96**, **κ = +0.067·sd > 0**, so a **floor-only** upper-sd read makes RED **easier**, driving the false-null rate for an at-floor effect from 3.9% (point-sd) to 18.9% (floor-only upper-sd) — anti-conservative, unacceptable.

**Frozen RED rule (v3.2, retained verbatim):**
```
RED  ⇔  ( x   + t·SE(sd̂)      < floor_c(sd̂)      )  AND  ( x   + t·SE(sd_upper) < floor_c(sd_upper) )   # aligned (v3.1, verbatim)
   AND  ( |μ̂| + t·SE(sd̂)      < floor_c(sd̂)      )  AND  ( |μ̂| + t·SE(sd_upper) < floor_c(sd_upper) )   # magnitude (v3.2)
   AND  ( NOT ANOMALOUS )
```
Each conjunction selects the harder ceiling. `sd_upper = sd̂ · √((n−1)/χ²_{0.05,n−1})`, factors **1.797 (n=8), 1.437 (n=16), 1.268 (n=32)**. The §3.3 Monte Carlo (4×10⁶ draws, Δ = floor(96), operative config, `/usr/bin/python3` numpy 2.0.2) that validated the **aligned** conjunction is unchanged (point-sd 3.95%, floor-only upper-sd 18.86%, coupled-upper 4.93%, conjunction 3.95%; Antigravity R2 reproduced 3.951% / 18.860% / 4.933% / 3.951%). The **magnitude** conjunction inherits the same coupled-upper conservatism; its whole-loop effect is measured by the OC sim (§9), not by this local MC.

**Operative RED (16b/B96): `|μ̂| < 0.067·sd_cell`** (magnitude bound; point governs at κ>0).

> **Q3 documentation caveats (retained — scope the warrant):**
> 1. **The Monte Carlo validates LOCAL false-null behavior only; it does NOT validate the six-cell loop.** The whole-loop validation is the OC simulation (§9) with predeclared acceptance criteria.
> 2. **The Monte Carlo assumes `sd_cell` is a reasonable proxy for the equal-arm SD.** Under option 2 this is a stated assumption bounding only the raw-current claim; under option 1/3 it is measured.

---

## 4. AMBER terminal rule + B_conf escalation → INCONCLUSIVE_AT_CEILING (Q4 — unchanged from v3.1/v3.2)

A cell may not sit in AMBER forever. The terminal ladder, per AMBER cell, in order:

1. **One block-extension: 16 → 32 blocks.** SE shrinks 0.2795·sd → 0.2165·sd; re-band against floor(96). **The 32-block sample CONTAINS the 16-block first pass** (accumulation, not an independent redraw) — preserved in the OC simulation (§9).
2. **Still AMBER against floor(96) at 32 blocks → escalate B_conf 96 → 128.** floor_c drops 0.557·sd → 0.482·sd; a persistent AMBER may resolve **GREEN** against the larger confirmatory.
3. **Still AMBER against floor(128) at 32 blocks → `INCONCLUSIVE_AT_CEILING`.** B_max = 128 is the declared compute ceiling.

**Q4 repair (retained).** `INCONCLUSIVE_AT_CEILING` **BLOCKS the pivot** (it is not RED/GREEN/ANOMALOUS). An AMBER at the ceiling means the CI still overlaps the floor — the cell is **unresolved at the authorized compute**, not bounded below it. A scientifically legitimate outcome, not a null.

> **v3.2 interaction (retained).** The magnitude bound shifts mass from RED into AMBER at 16b, so **more cells reach the ladder and terminate INCONCLUSIVE** (per-cell INCONCLUSIVE 0.126 → 0.225, §13). This is the intended, honest direction: unresolved magnitude → INCONCLUSIVE, never a minted null. **[v3.3]** A demoted cell's `INCONCLUSIVE_AT_CEILING` is recorded non-gating (§1.2 clause 3) — legitimate because its design point is already outside the claim; a **gating** cell's INCONCLUSIVE blocks the pivot exactly as before.

---

## 5. The pivot rule — four honest terminal outcomes (Q4) + statistic-and-roster-scoped raw-current claim (Q1, [v3.3]) + magnitude+STABLE gate (v3.2) + omega veto ([v3.3])

The scout ends in exactly one of **four** honest terminal outcomes:

1. **GREEN candidate** — ≥1 cell GREEN on the primary (**gating OR demoted** — §1.2 [v3.3]) → **register the Movement-3 two-sample contrast** at the tie-break cell (do not pivot). Candidate-selection, §10.
2. **All-actual-RED pivot** — pivots to the closed no-reset NESS protocol **iff all pivot conditions below hold**. The claim is a **RAW-CURRENT claim** (Q1 option 2) with the **[v3.3] frozen scoped wording (§2.1):** *"raw mismatch currents are sub-floor **in the `quad_loop_rate` statistic** at the **N_g gating configurations** (the surviving design points **D_surv**; in the no-demotion case, the six cells ≈ four independent design points), with `omega_roi` recorded and nowhere GREEN/ANOMALOUS, and `occupancy_x` recorded and unbounded"* — **not** a contrast claim, **not** a continuum claim, **not** a claim about any statistic other than `quad_loop_rate`, and **not** a claim about any demoted design point (§2.1). *(v3.2 wording — "raw mismatch currents are sub-floor at the probed configurations (the six cells ≈ four independent design points)" — is superseded: it bounded one statistic while asserting the whole current object, and hardcoded a cell set §1.2 could shrink.)*
3. **ANOMALOUS / omega-flag → investigate** — ≥1 cell ANOMALOUS on the primary (gating or demoted), **or [v3.3] ≥1 omega veto (omega GREEN or omega ANOMALOUS in any cell)** → run the §8 state machine (primary anomalies) / the omega disposition (below); **no pivot and no terminal-null decision while an anomaly or an un-dispositioned omega flag is open**.
4. **INCONCLUSIVE at compute ceiling** — ≥1 **gating** cell `INCONCLUSIVE_AT_CEILING` (and no GREEN/ANOMALOUS/omega-flag forcing outcomes) → the scout **halts with a legitimate bound**. **This is not a null and not a failure.** It blocks the pivot.

**Pivot conditions for outcome 2 (ALL must hold; conditions quantify over the REGISTERED POST-P2 GATING ROSTER — §1.2 [v3.3] — except where a demoted-cell disposition (§1.2 clause 3) or the omega veto (iii) explicitly reaches wider):**
- **(0) No open anomaly (blocks the pivot):** **no** cell in the gating roster is ANOMALOUS, **and [v3.3] no demoted cell has an open (un-dispositioned) primary ANOMALOUS** (§1.2 clause 3). A cell leaves ANOMALOUS **only** through the §8 state machine (whose vanish test is now powered — §8).
- **(0′) No open inconclusive (blocks the pivot — Q4):** **no** cell in the gating roster is `INCONCLUSIVE_AT_CEILING`.
- **(i) Terminal-band condition:** the gating roster is non-empty, and **every** cell in it is **actual RED** (§3, §4) — every counted RED satisfies the **magnitude bound** (`|μ̂| < κ`; intrinsic to a RED band under §3: **the belt**). Given (0) and (0′), "every gating cell" excludes ANOMALOUS and INCONCLUSIVE — no vacuous set, no ceiling-minted null.
- **(ii) Instrument precondition (the suspenders):** **`stable_cell` = STABLE** (P1, §1.1) for **every** cell whose RED is counted. An UNSTABLE RED at M=400 does not license the pivot until its predeclared remedy runs.
- **(iii) [v3.3] Omega veto (the statistic-axis guard):** in **every** cell (gating **and** demoted — a super-floor omega current anywhere the scout looked contradicts a currents-null), the recorded `omega_roi` band at the cell's terminal block count is **neither GREEN nor ANOMALOUS**. If an omega GREEN/ANOMALOUS is recorded: the pivot is **BLOCKED**, the flag is **HQ-escalated**, and disposition is: omega GREEN → consider a Movement-3 omega-statistic candidate registration (via formal amendment — omega is not the calibrated primary, so it registers as a flagged candidate, not an automatic outcome 1); omega ANOMALOUS → §8-style investigation under the same amendment discipline. Only after the flag is formally dispositioned (superseding record, law #9) can the terminal outcome be re-evaluated. **HQ rec (fork 10): veto = blocking**, not annotate-only — an annotation cannot stop a null from being minted over a live current.
- **(iv) [v3.3] Roster assertion (the cell-axis guard):** the set of cells evaluated in (0)–(iii) is **exactly** the registered post-P2 gating roster — asserted mechanically in `pivot_licensed()` (§7). A missing, extra, or silently-dropped cell returns **False** (and is a registration-integrity flag, not a null).

**Belt-and-suspenders (v3.2, retained) + whole-object scope ([v3.3]).** A cell may count toward the all-RED pivot **only if** it is STABLE (§5(ii)) *and* its RED satisfies the magnitude bound (§3). **Measured joint protection (§13):** wrong-sign-at-floor invalid pivot 0.161 (v3.1) → 0.0066 (belt) → ~0 (belt + suspenders); with the §8 reband channel now counted, the belt-alone analytic estimate is ≈ 0.007, still ≤ 0.02 (gate 5; the OC sim including the §8 loop is the number of record — [v3.3]). The omega veto and roster assertion add the two remaining whole-object axes: no statistic-projection null, no shrunk-denominator null.

**In words [v3.3 restatement]:** a raw-current null (pivot) is earned only when **no cell showed a significant wrong-sign current** (ANOMALOUS guard, dispositioned through a **powered** vanish test), **no cell showed a sub-significance real wrong-sign current at floor magnitude** (the `|μ̂|` bound refuses it a RED), **no cell was left unresolved at the compute ceiling**, **no cell anywhere — gating or demoted — showed a super-floor or significant-wrong-sign current in the recorded secondary statistic `omega_roi`** (the omega veto), the **registered gating cells — and only that exact roster —** are confidently sub-floor **in `quad_loop_rate` magnitude**, and the instrument was demonstrably reading a stable-sign signal everywhere it called RED. The claim then covers **exactly the surviving design points**, one named statistic, nothing more. The scout still "cannot fail": candidate, or bounded raw-current at the surviving points with a stable instrument, or a named anomaly/omega flag, or an honest compute-ceiling bound.

**Upgrading the pivot to a contrast claim** requires the baseline/equal-arm condition (option 1/3 or Movement 3). Under option 2 the scout does not upgrade; Movement 3 does.

**GREEN tie-break (outcome 1):** if several cells are GREEN, the registration cell is the one with the highest `x − t·SE` margin above `floor_c` on the primary. A Tc-cell GREEN is a **drive-amplitude** registration **requiring a measured two-sample contrast** (§2.1); a geometric-cell GREEN is a **Δτ** registration. **[v3.3]** A demoted-cell GREEN enters the tie-break like any other (its demotion barred it from *gating a null*, not from *carrying a candidate*).

---

## 6. Per-cell configuration tables (equal-arm table unchanged; design-point roles annotated [v3.3])

### 6.1 Equal-arm config per candidate cell (Q6-i adopted — τy-matched at matched Tc, conditional on Q1)

**Adopted: τy-matched equal arm** — the equal-τ config at the cell's **larger horizon** τy, at the **same Tc**. Rationale (receipt-07): the ROI mixed-partial of the small-τx grid is ≈ 0, so the curl and its block-SD noise are carried by the larger-horizon τy grid; the τy-matched arm is the closest noise-match. Matched-Tc is **non-optional** for the Tc cells (DIAG 2). Under option 2 this config defines only the Movement-3 second arm.

| Cell | (τx, τy) | Tc | Role | Equal-arm config (τy-matched, matched-Tc) | **Design point carried [v3.3]** |
|---|---|---|---|---|---|
| A    | (0.1, 2.0)  | 1 | widest horizon mismatch | (2.0, 2.0) @ Tc=1 | (τy=2, Tc=1) — shared with B |
| B    | (0.25, 2.0) | 1 | mismatch mid            | (2.0, 2.0) @ Tc=1 | (τy=2, Tc=1) — shared with A |
| C    | (0.1, 1.0)  | 1 | amplitude-only          | (1.0, 1.0) @ Tc=1 | (τy=1, Tc=1) — shared with D |
| D    | (0.25, 1.0) | 1 | replica bridge to v4.3  | (1.0, 1.0) @ Tc=1 | (τy=1, Tc=1) — shared with C |
| AxT2 | (0.1, 2.0)  | 2 | Tc sweep at widest pair | (2.0, 2.0) @ Tc=2 | (τy=2, Tc=2) — **sole carrier** (leaves the claim if demoted, §1.2) |
| AxT4 | (0.1, 2.0)  | 4 | Tc sweep at widest pair | (2.0, 2.0) @ Tc=4 | (τy=2, Tc=4) — **sole carrier** (leaves the claim if demoted, §1.2) |

**Design-space degeneracy (v3.2 fix 4, retained — anchors the no-demotion pivot scope).** A and B (both τy=2.0, Tc=1) and C and D (both τy=1.0, Tc=1) share the ROI mixed-partial to 4 s.f. (receipt 07): the small-τx grid contributes ≈0 curl, so within each pair the curl is set by the common τy grid. The six cells therefore probe **≈ four independent design points** {(τy=2,Tc=1), (τy=1,Tc=1), (τy=2,Tc=2), (τy=2,Tc=4)}. **[v3.3]** The all-RED pivot's raw-current claim is bounded to **the surviving subset of these points after any P2 demotion** (§1.2, §2.1) — the full four-point wording is licensed only when all six cells gate.

**Reviewer alternatives (fork §11):** (τx,τx)-matched, or a dual-reference design.

### 6.2 Predicted-sign table (all TBD until P1 registers — unchanged from v3.1/v3.2)

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

## 7. `band_cell()` + `pivot_licensed()` pseudocode (v3.3 — roster assertion + omega veto added; `band_cell` unchanged from v3.2)

Reference implementation for the additive functions in `analyze()`. Pure analysis; touches no harness physics. All arithmetic in units of `sd_cell`.

```python
def band_cell(mu_hat, sd_cell, n_blocks, B_conf, sigma_cell, stable_cell):
    """
    Band one scout cell on ONE statistic (called for quad_loop_rate AND omega_roi).
    Returns (band, aligned_bound, floor_c), band in {GREEN, AMBER, RED, ANOMALOUS}.
    INCONCLUSIVE_AT_CEILING is set by the caller's terminal ladder (sec 4).
    sigma_cell in {+1, -1, None}; None => two-sided (P1 INDETERMINATE).
    stable_cell in {True, False} (P1 sign-stability); consumed at the pivot.
    [UNCHANGED from v3.2 -- the magnitude-bound RED is retained verbatim.]
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

    # RED (v3.2, retained): aligned coupled-upper conjunction AND the MAGNITUDE
    #                       coupled-upper conjunction on |mu_hat| (bounds the wrong-sign axis).
    aligned = (x        + t*SE(sd_cell) < floor_c(sd_cell)) and \
              (x        + t*SE(sd_up)   < floor_c(sd_up))
    magnitude = (abs(mu_hat) + t*SE(sd_cell) < floor_c(sd_cell)) and \
                (abs(mu_hat) + t*SE(sd_up)   < floor_c(sd_up))
    if aligned and magnitude:
        return ("RED", abs(mu_hat) + t*SE(sd_cell), floor_c(sd_cell))

    return ("AMBER", x + t*SE(sd_cell), floor_c(sd_cell))


def pivot_licensed(gating_bands, stable_flags, omega_bands, descriptive_bands,
                   REGISTERED_GATING_ROSTER):
    """Sec 5 [v3.3]: pivot to closed no-reset NESS (statistic-and-roster-scoped
    RAW-CURRENT claim, sec 2.1) iff ALL hold. Guarded against vacuous truth,
    compute-ceiling-minted null, wrong-sign magnitude leak (belt, inside band_cell's
    RED; STABLE is the suspenders), STATISTIC-PROJECTION null (omega veto -- NEW),
    and SHRUNK-DENOMINATOR null (roster assertion -- NEW).

    gating_bands:      {cell: band} for the registered post-P2 GATING roster only
    stable_flags:      {cell: bool} P1-B STABLE, gating roster
    omega_bands:       {cell: band} descriptive omega_roi bands, ALL cells
                       (gating AND demoted) at each cell's terminal block count
    descriptive_bands: {cell: band} primary-statistic bands of P2-DEMOTED cells
                       (empty dict when no demotion)
    REGISTERED_GATING_ROSTER: frozenset of cell names frozen into the prereg by P2
                       (sec 1.2) -- the claim denominator.
    """
    # (iv) ROSTER ASSERTION [v3.3]: the evaluated set IS the registered denominator.
    #      A silently-dropped or extra cell can never shrink or stretch the claim.
    if set(gating_bands.keys()) != set(REGISTERED_GATING_ROSTER):
        return False                             # registration-integrity flag, not a null
    if not gating_bands:
        return False                             # nothing to bound the space

    # (iii) OMEGA VETO [v3.3]: a super-floor or significant-wrong-sign current in the
    #       recorded secondary statistic, in ANY cell (gating or demoted), blocks the
    #       pivot (HQ-flagged; disposition per sec 5(iii)). Closes the statistic axis.
    if any(b in ("GREEN", "ANOMALOUS") for b in omega_bands.values()):
        return False

    # Demoted-cell primary dispositions (sec 1.2 clause 3) [v3.3]:
    #   GREEN forces outcome 1; ANOMALOUS blocks until dispositioned via sec 8.
    #   RED/AMBER/INCONCLUSIVE on a demoted cell: recorded, non-gating (its design
    #   point is already outside the claim; verdict caveat is mandatory, sec 1.2).
    if any(b in ("GREEN", "ANOMALOUS") for b in descriptive_bands.values()):
        return False

    # (0) / (0') / outcome-1 guard over the gating roster (v3.1/v3.2, unchanged):
    if any(b == "ANOMALOUS" for b in gating_bands.values()):
        return False                             # resolve via sec 8 (powered rerun) first
    if any(b == "INCONCLUSIVE_AT_CEILING" for b in gating_bands.values()):
        return False                             # no ceiling-minted absence
    if any(b == "GREEN" for b in gating_bands.values()):
        return False                             # register at the GREEN cell instead
    if not all(b == "RED" for b in gating_bands.values()):
        return False                             # AMBER cells -> run sec 4 ladder first
    # (ii) SUSPENDERS: every counted RED must be on a STABLE cell
    if not all(stable_flags[c] for c, b in gating_bands.items() if b == "RED"):
        return False                             # UNSTABLE RED at M=400 does not license
    return True
```

**[v3.3] Key diff from v3.2 pseudocode:** `band_cell` is **byte-identical** to v3.2 (comment header updated only). `pivot_licensed` gains three guards: **(iv) the roster assertion** (`set(gating_bands) == REGISTERED_GATING_ROSTER` — pins pivot membership; v3.2 had only `if not cell_bands`, so a demoted cell silently dropped from the dict passed unexamined), **(iii) the omega veto** (v3.2 excluded omega bands from `pivot_licensed` entirely — the statistic-axis leak), and the **demoted-cell disposition guard** (v3.2 never defined whether a demoted cell's GREEN/ANOMALOUS reaches the pivot). The claim TEXT emitted on `True` must be generated from `REGISTERED_GATING_ROSTER` via the §2.1 design-point map — never hardcoded "six cells / four points."

---

## 8. Anomaly-resolution state machine (Q2 — structure unchanged; STATE-B vanish test POWERED in v3.3)

*(The state machine, discriminator, disposition table, amendment rule, and selftest requirement carry over from v3.1/v3.2. **The one v3.3 change is STATE B:** the "vanishes at higher M" test is now a predeclared, powered test — v3.2 left the rerun's n unspecified, so a single 16-block-SE-scale look mislabeled a REAL −1×floor current as GRID-ARTIFACT ~39.5% of the time (screen power ~0.61 — higher M does not lower the floor, DIAG 1), silently discarding the TRUE-OPPOSITE-PHYSICS escalation and letting the reband re-enter the pivot pool through a channel omitted from the §13 accounting.)*

**Trigger.** A cell bands ANOMALOUS (§3, `x < −t·SE`). The pivot is blocked (condition (0)) until this machine terminates the cell in one of {GRID-ARTIFACT re-banded, TRUE-OPPOSITE-PHYSICS, SIGN-PRECONDITION-FAILURE excluded, UNRESOLVED}.

```
STATE A (entry): cell is ANOMALOUS at M=400.
  --> Rerun at the predeclared higher-M / seed-averaged-grid recipe (the SAME remedy
      declared for that cell in P1; sec 1.1 r1/r2), in precond namespace,
      [v3.3] at the PREDECLARED POWERED SIZE: n_rerun = 40 FRESH blocks
      (one-sided t_39 = 1.685 against 0, SE = sd_hat * sqrt(1/40 + 1/64) = 0.2016*sd,
       significance edge |x| > 0.340*sd). Measured power to re-detect a REAL
      wrong-sign current at -1x floor(96): 0.912 >= 0.90 (MC, sec 13; hard gate 9).
STATE B (rerun result) [v3.3 -- powered vanish test]:
  - Wrong-sign significance FAILS the POWERED n_rerun=40 test --> GRID-ARTIFACT.
    Residual mislabel probability for a real -1x-floor current: ~0.088 (was ~0.395
    at the unpowered v3.2 single look). Re-band under the higher-M recipe (a
    predeclared recipe supersede via the sec 8-step-4 amendment path). The re-banded
    cell re-enters the pivot pool; THIS REBAND CHANNEL IS COUNTED in gate 5's
    number of record (sec 9.2 S5, sec 9.3 -- v3.2 omitted it).
  - Wrong-sign significance PERSISTS at the powered rerun --> STATE C.
STATE C (persistent dynamical wrong-sign): compare to P1's registered high-M sigma_cell,
         re-examine sigma_cell's high-M reference robustness:
  - Persistent sign OPPOSES sigma_cell AND sigma_cell's high-M reference is robust
    (P1-B still >= 12/16) --> TRUE-OPPOSITE-PHYSICS. NOT a null; escalate to a Movement-3
    two-sample contrast in the OBSERVED direction. Never counts toward an all-RED pivot.
  - Re-examination shows sigma_cell was mis-registered --> SIGN-PRECONDITION-FAILURE.
    Cell EXCLUDED from the pivot; P1 re-run only via a formal amendment.
    [v3.3] Exclusion = demotion from the gating roster => the pivot claim SHRINKS
    per sec 1.2 clause 2 and the roster assertion (sec 7) consumes the AMENDED roster.
STATE D (higher-M infeasible OR B/C inconclusive) --> UNRESOLVED. Cell blocks the pivot
         indefinitely; scout terminates in outcome 3 with the anomaly named.
```

| Classification | Disposition | Counts toward pivot? |
|---|---|---|
| GRID-ARTIFACT | re-band under higher-M recipe (amendment) — **[v3.3] only after failing the POWERED n_rerun=40 vanish test** | yes, at the re-banded higher-M result — **[v3.3] and this channel is simulated in S5 + counted in gate 5** |
| TRUE-OPPOSITE-PHYSICS | Movement-3 contrast in observed direction — **[v3.3] retention at −1×floor now ≈ 0.91 given the anomaly surfaced (was ≈ 0.61)** | **no** |
| SIGN-PRECONDITION-FAILURE | cell excluded; P1 re-run only via amendment — **[v3.3] claim shrinks with the roster (§1.2)** | **no** (until amended prereg) |
| UNRESOLVED | scout halts in outcome 3, anomaly named | **no** |

**Step 4 — amendment rule (frozen, unchanged).** Any change to a cell's resolution, M, seed recipe, or σ_cell registration requires a **formal preregistration amendment**: regenerate the config, record the new `config_hash` + `source_sha` + prereg sha256, verify readback, **then** run (law #1). Corrections **supersede**, never erase (law #9). No informal "investigate and re-band" path. **[v3.3]** An amendment that changes the gating roster **re-issues the pivot-claim scope text** (§2.1) in the same amendment.

**Selftest requirement (law #2, sharpened [v3.3]).** The anomaly gate must demonstrably **fire** on a planted wrong-sign artifact and **block** the pivot — asserted in the OC simulation (§9, scenario S5), which **must simulate the entire §8 loop including the powered STATE-B rerun and the GRID-ARTIFACT reband re-entry** (v3.2's S5 was not explicit about the rerun/reband path; the reband channel was absent from the 0.0066 accounting).

> **v3.2 note retained — the anomaly machine is the *suspenders' backstop*, not the belt.** The guarantee is the magnitude bound + STABLE; the §8 machine *dispositions* the anomalies that fire. **[v3.3]** With the powered vanish test, the machine also stops *destroying evidence*: a real opposite-direction current that surfaces as ANOMALOUS now survives to TRUE-OPPOSITE-PHYSICS ≈ 91% of the time instead of ≈ 61%.

---

## 9. OC SIMULATION SPECIFICATION (Q4/Q7; the next build phase implements this — v3.3 adds omega joint modeling, the §8 loop, and scenarios S8/S9)

ChatGPT (Q4) required the selftest operate on the **entire frozen state machine**, not per-contrast power, with **predeclared acceptance criteria**. This section is that specification, updated for the v3.2 magnitude bound + belt-and-suspenders AND the v3.3 whole-object guards (omega veto, roster assertion, powered §8 rerun). It is registered as part of the prereg (§10) and **must run and pass before the scout is licensed** (after P1/P2, before the scout). *The v3.1 OC sim surfaced the re-pass block; the v3.2 spec was superseded before implementation by the whole-object audit; the v3.3 OC sim is the artifact to build.*

**Why joint + full-loop is non-optional (law #3).** Analytic per-contrast power lies under a multi-look ladder (v4.3: 0.998 analytic vs 0.655 compound). The acceptance criteria are **compound / whole-loop** operating characteristics, all six cells simulated jointly — **[v3.3] including the §8 rerun/reband loop and the omega bands.**

### 9.1 Simulation model (implementable — v3.3 additions in **bold**)

- **Null-SD calibration (receipt 06).** Per-block SD of `quad_loop_rate`: Tc1 = 5.03e-5, Tc2 = 6.29e-5 (×1.25), Tc4 = 8.15e-5 (×1.62). Band arithmetic is scale-free in `sd_cell`; SDs enter only the Tc-heteroscedastic and equal-arm-offset scenarios.
- **Draw model.** For a cell with true contrast Δ (in `sd_cell` units): each block statistic ~ N(Δ, 1); μ̂₁₆ = mean of the first 16 draws; the 32-block extension **reuses those 16 and appends 16 new** (accumulation dependence preserved). sd̂ from the sample SD; `sd_upper` from the χ² factor. B96→B128 re-bands the **same 32-block** sample.
- **`band_cell` with the magnitude bound** (v3.2, retained). The **SE_FACTOR n=8 constant is 0.375** (= √(1/8+1/64)); the v3.1 sim comment read `0.39528` — corrected (law #4).
- **P1 modeling (v3.2, retained):** σ_cell registration from P1-A; **STABLE from N=16 coupled M=400 per-seed curls sharing the cell's true Δ** (per-seed curl ~ N(Δ_curl, σ_curl²), Δ_curl = ρ·Δ; sensitivity ρ ∈ {0.5, 1.0, 2.0}). `pivot_licensed` consumes modeled STABLE flags.
- **[v3.3] Omega joint modeling (NEW — required):** each block carries a **(quad, omega) pair**. Omega true contrast Δ_ω is a scenario parameter (0 under quad-only scenarios; nonzero in S8). The **quad↔omega block-noise correlation ρ_qω is a declared modelling parameter with a predeclared sensitivity sweep** (HQ proposal: ρ_qω ∈ {0, 0.3, 0.6}) — the two statistics are computed from the same trajectories, so independence must not be silently assumed. `omega_roi` bands are computed by the same `band_cell()` at each cell's terminal block count and fed to `pivot_licensed`'s omega veto. Report the veto's null firing rate and its effect on P(pivot | null) at each ρ_qω.
- **[v3.3] §8 loop modeling (NEW — required):** any ANOMALOUS cell runs the full §8 machine in-sim: the **powered STATE-B rerun (n_rerun = 40 fresh draws at the remedy recipe)**, GRID-ARTIFACT reband on a non-significant rerun (rebanded cell **re-enters the pivot pool**), TRUE-OPPOSITE-PHYSICS on persistence. Gate 5's invalid-pivot number of record **includes the reband channel** (v3.2's 0.0066 did not; analytic estimate with the channel ≈ 0.007, §13).
- **[v3.3] Demotion modeling (NEW — for S9):** the sim must accept a registered gating roster smaller than six cells, band the demoted cell(s) descriptively, and assert the claim-scope object emitted on a licensed pivot equals the surviving design points.
- **Correlated-noise question across A≡B/C≡D (v3.2 flag, retained).** Baseline draws **independent** per-cell block noise (reproduces the receipt-06 anchors); correlated A≡B/C≡D noise is a predeclared sensitivity item — measured, not asserted (fork 8).
- **Trials + rng.** ≥ 1×10⁵ per scenario (≥ 1×10⁶ for the false-GREEN / invalid-pivot / wrong-sign tail estimates), rng pinned (proposal `seed = 20260708` **[v3.3 — new sim, new pinned seed]**), `/usr/bin/python3` numpy 2.0.2. Report Monte Carlo standard errors on every rate.

### 9.2 Scenarios (all six cells simulated jointly — S5 sharpened, S8/S9 NEW [v3.3])

| # | Scenario | Construction |
|---|---|---|
| S1 | **Global null** | all six cells Δ = Δ_ω = 0, Tc-calibrated SDs. Measures: false-GREEN, false-anomaly (terminal, t₁₅), **omega-veto null rate at each ρ_qω [v3.3]**, joint pivot-under-null. |
| S2 | **One-cell predicted-direction at floor** | one cell Δ = +floor(96) = +0.557; rest null. Measures P(invalid pivot) — the predicted-direction safety gate. |
| S3 | **One-cell supra-floor sweep** | one cell Δ ∈ {+1×, +2×, +3×} floor; rest null. Compound GREEN power + supra-floor invalid pivot. |
| S4 | **Multi-signal / GREEN tie-break** | ≥2 supra-floor cells → forces multiple GREENs so the tie-break resolves. |
| **S5** | **Wrong-sign current AT FLOOR — full §8 loop [v3.3 sharpened]** | one cell **Δ = −1×floor** (the exact magnitude the block probes — NOT a weakened larger artifact); rest null. STABLE modeled from coupled P1-B draws. **[v3.3] The §8 machine runs in full: powered n_rerun=40 STATE-B vanish test, GRID-ARTIFACT reband re-entry, TRUE-OPPOSITE-PHYSICS persistence.** Measures: joint invalid-pivot **including the reband channel** (gate 5's number of record), vanish-test power (gate 9), TRUE-OPPOSITE-PHYSICS retention. Sub-cases: −1×, −1.45×, −2× floor. |
| S6 | **Tc-heteroscedastic** | Tc cells at receipt-06 SD scaling; tests that per-cell `sd_cell` banding neutralizes Tc growth. |
| S7 | **Nonzero equal-arm offset** | inject μ_eq ∈ {0.10, 0.30}·floor → sizes how a real offset perturbs the raw-current pivot (the Q1 raw-vs-contrast gap). |
| **S8** | **[v3.3 NEW] Omega-only current (statistic-axis failability, law #2)** | all six cells quad Δ = 0; cells A, B carry **Δ_ω = +2×floor** (the audit's construction: counter-rotating loop pairs cancel loop-rate, net ROI vorticity survives). The omega veto **must** block the pivot: measures P(pivot \| omega-only current at 2×floor) — **gate 8**. Sub-case Δ_ω = +1×floor reported advisory. Swept over ρ_qω. |
| **S9** | **[v3.3 NEW] Demoted-cell leak (cell-axis failability, law #2)** | AxT4 demoted (gating roster = 5 cells); AxT4 carries a real **Δ = +2×floor** current; gating cells null. Asserts: (a) a licensed pivot's emitted claim scope **excludes** (τy=2, Tc=4); (b) AxT4's descriptive GREEN **forces outcome 1 / blocks the pivot** (§1.2 clause 3); (c) the roster assertion rejects any run where AxT4 is passed as gating. |

### 9.3 Predeclared acceptance criteria (v3.3 — gates 8/9 added; gate 5's record includes the reband channel; HQ-recommended, pending Anthony)

**Hard gates (registration blocked if violated) — the safety criteria:**

| # | Criterion | Scenario | Tolerance (HQ-rec) | Expected (analytic/MC this session, §13) |
|---|---|---|---|---|
| 1 | **P(any false GREEN)** | S1 global null | ≤ 0.01 | ~0.002 |
| 2 | **P(invalid pivot) — predicted-direction at floor** | S2 (Δ=+floor) | ≤ 0.02 | **0.0067** |
| 3a | P(invalid pivot) — predicted-direction 2× floor | S3 (+2×) | ≤ 0.005 | ~3×10⁻⁶ |
| 3b | P(invalid pivot) — predicted-direction 3× floor | S3 (+3×) | ≤ 0.005 | ~0 |
| 4 | **P(registrable GREEN)** compound power | S3 (+3× floor) | ≥ 0.90 | ~1.00 |
| **5** | **P(invalid pivot) — WRONG-SIGN at floor, [v3.3] INCLUDING the §8 reband channel** | S5 (Δ=−floor), STABLE coupled, full §8 loop | **≤ 0.02** | **≈ 0.007 (belt, powered rerun, reband counted)**; ~0 (belt+suspenders) |
| **5′** | **P(invalid pivot) — WRONG-SIGN ≥2× floor** | S5 (Δ=−2×floor) | **≤ 0.005** | ~3×10⁻⁶ |
| 6a | Partition completeness (no limbo) | S1–S9 | = 0 | 0 |
| 6b | Zero cells terminate AMBER (deadlock) | S1–S9 | = 0 | 0 |
| 7 | law #2 — planted +3× signal breaks pivot (cell non-RED) | S3 (+3×) | ≥ 0.90 | ~1.00 |
| **8** | **[v3.3] Omega veto failability — P(pivot \| omega-only current at 2×floor)** | S8 (Δ_ω=+2×) | **≤ 0.005** (at every swept ρ_qω) | omega bands GREEN/ANOMALOUS with high prob at 2×floor → veto fires; residual expected ≲10⁻³ (OC sim = number of record) |
| **9** | **[v3.3] §8 vanish-test power at −1×floor (powered rerun)** | S5, STATE-B sub-loop | **≥ 0.90** | **0.912** (n_rerun=40; MC this session, §13) |
| **10** | **[v3.3] Roster/demotion integrity** — S9 assertions (a)(b)(c) all hold | S9 | = pass (deterministic) | pass |

> **Gate 5's number of record (v3.3 restatement).** v3.2 measured 0.0066 **without** the §8 reband channel (a mislabeled GRID-ARTIFACT reband could land RED and re-enter the pivot pool unsimulated). With the **powered** rerun, the analytic channel estimate is extra cell-RED ≈ 0.873·0.088·0.033 ≈ **0.0025**, total invalid pivot ≈ **0.007** — still ≤ 0.02, but the OC sim must **measure** it through the full loop (S5), not assert it. *(At the unpowered v3.2 rerun the same channel gave ≈ 0.009 — also under the gate, so this was never a gate breach; the real costs were the silent ~39% loss of TRUE-OPPOSITE-PHYSICS escalations and an accounting gap in the number of record. Both closed.)*

**Reported / advisory operating characteristics (informative, NOT hard-gated):**

| Characteristic | Scenario | Advisory | Expected (§13) |
|---|---|---|---|
| **P(correct pivot)** | S1 calibrated null | advisory (low is legitimate) | **≈ 0.11** [v3.3 ballpark: v3.2's 0.148 × the omega veto's null pass-rate ≈ (1−0.049)⁶ ≈ 0.74, under quad⊥omega independence; the OC sim at swept ρ_qω is the number of record] |
| **P(≥1 INCONCLUSIVE_AT_CEILING)** | S1 | report | per-cell 0.225 (v3.2, unchanged by the veto) |
| **P(≥1 false anomaly, primary)** | S1 | **advisory — non-blocking**; 0.254 breaches the standing 0.20 cap (conservative: pivot-blocking, never verdict-flipping); cap value 0.20-vs-0.30 is an Anthony call (fork 9) | ~0.254 (6-indep, terminal t₁₅) |
| **[v3.3] omega-veto null firing rate** | S1 | report at each ρ_qω (same conservative character as false anomalies: blocks, never mints) | per-cell ≈ 0.049 terminal (≈0.048 ANOMALOUS + ≈0.001 GREEN); six-cell ≈ 0.26 at ρ_qω=0 |
| **anomaly-SCREEN power (standalone, 16b)** | S5 | report — the weak layer, not the guarantee | ~0.61 at −floor, ~0.90 at −1.45×floor |
| **anomaly TERMINAL rate through the ladder** | S5 | report (favorable side effect, not relied upon) | ~0.87 at −floor, ~0.99 at −1.45×floor |
| **[v3.3] TRUE-OPPOSITE-PHYSICS retention** | S5 | report — ≈ P(anomaly surfaced)·P(powered rerun persists) | ≈ 0.87·0.91 ≈ 0.79 end-to-end at −1×floor (was ≈ 0.87·0.61 ≈ 0.53 unpowered) |
| **P(correct tie-break \| ≥2 GREEN)** | S4 | advisory ≥0.90 (separated slate) | tie-break exercised only by S4 |
| **raw-vs-contrast gap** | S7 | report pivot/GREEN shift vs offset | sizes the Q1 gap |

**Interpretation of the split (v3.2, extended).** Only the **safety** criteria are hard gates. **P(correct pivot | null) is deliberately advisory** and falls again in v3.3 (≈ 0.148 → ≈ 0.11 ballpark) — the omega veto, like the magnitude bound before it, buys whole-object honesty at the price of reachability; hard-gating a high pivot rate would pressure the design back toward minting absence. The load-bearing gates are the **two symmetric invalid-pivot bounds** (2 and 5, both ≈ 0.007 at floor), the **omega failability bound** (8), the **vanish-test power** (9), and the **roster integrity** (10).

### 9.4 Boundary / cutpoint selftests (Q7 item 7 — v3.3 adds omega-veto, roster, and rerun cutpoints)

Deterministic assertions on `band_cell()`/`pivot_licensed()`:

- **Equality at each cutpoint** — μ̂ exactly at `floor_c ± t·SE`, at `floor_c`, and **at ±κ (the magnitude-RED edge, both signs)** resolve to the predeclared side.
- **Magnitude-bound wrong-sign check (v3.2)** — μ̂ = −floor_c (σ=+1) must **NOT** band RED; μ̂ = −(κ+ε) must not band RED; μ̂ = −(κ−ε), not ANOMALOUS, must band RED.
- **One-sided vs two-sided branch** — two-sided RED unreachable at 16b (κ_2s<0), reachable at 32b.
- **Wrong-sign anomaly boundary** — μ̂ = −t·SE flips ANOMALOUS exactly at the significance edge; RED and ANOMALOUS never co-fire (κ < t·SE).
- **SD-upper factors per block count** — 1.797 / 1.437 / 1.268; the RED conjunction selects the harder ceiling.
- **Empty / anomaly-only / inconclusive-only pivot guard** — all False.
- **Terminal-ceiling behavior** — a cell held AMBER through the ladder emits `INCONCLUSIVE_AT_CEILING`, blocks the pivot, never RED.
- **UNSTABLE-RED blocks the pivot (suspenders)** — all-RED gating bands with one STABLE=False ⇒ False.
- **[v3.3] Omega-veto cutpoints** — all-RED gating bands + one omega GREEN ⇒ False; + one omega ANOMALOUS ⇒ False; + omega bands all in {RED, AMBER, INCONCLUSIVE_AT_CEILING} ⇒ veto does not fire.
- **[v3.3] Roster assertion** — gating dict missing one registered cell ⇒ False; gating dict with one extra cell ⇒ False; demoted cell passed in `descriptive_bands` with GREEN or ANOMALOUS ⇒ False.
- **[v3.3] Powered-rerun edge** — STATE-B rerun statistic exactly at |x| = 1.685·0.2016·sd = 0.340·sd resolves to the predeclared side; n_rerun grep-checked = 40.

---

## 10. Scope of changes if ratified (→ config_hash / prereg re-issue) — Q7

| Artifact | Change | Hash impact |
|---|---|---|
| `SCOUT_DECLARATION.md` decision-rule section | Replaced by §1–§8 of this document | none (declaration) |
| `analyze()` in `v44_scout.py` | Add `band_cell()` (magnitude-bound RED) + `pivot_licensed()` (§7 — **[v3.3] with roster assertion, omega veto, demoted-cell guards**) with `INCONCLUSIVE_AT_CEILING` — additive, does not touch the v4.3-inherited estimator or forward physics | new `source_sha` |
| `CFG["scout"]["blocks"]` | 8 → **16** (D2) | **new `config_hash` → re-issue prereg → new sha256** |
| B_conf convention | 64 → **96** (D4) | new `config_hash` if surfaced in CFG; else declaration-only |
| **P1 config** (§1.1) | high-M reference (N_avg=32@M4000), robustness (N=16@M400), ≥12/16 STABLE, per-cell remedy | part of config_hash / prereg |
| **P2 config** (§1.2) | Tc∈{1,2,4}×M∈{400,4000}, n=40/arm, bootstrap (10000, rng999, 90%CI), R-ratio criteria, action table — **[v3.3] + pinned demotion consequences + the registered gating roster + surviving-design-point claim scope** | part of config_hash / prereg |
| **Anomaly SOP** (§8) | frozen state machine + amendment rule — **[v3.3] + powered STATE-B vanish test (n_rerun=40, power 0.912 ≥ 0.90 at −1×floor)** | part of prereg |
| **OC simulation script + expected-OC report** (§9) | **new v3.3 simulator** (magnitude-bound RED, coupled STABLE, **omega joint modeling + ρ_qω sweep, full §8 loop, S8/S9, gates 8/9/10**) | part of prereg (new artifact) |
| **Baseline / equal-arm conditions** (§2.1, §6.1) | Q1 option chosen (default option 2) + licensing conditions | part of prereg |
| **Stale-prose flag (law #4):** comments hard-coding "B=64 floor", the sim's `0.39528` SE_FACTOR n=8 comment, any per-cell-97.5%-as-joint prose, **[v3.3] any unqualified "currents are sub-floor" (must read "in the `quad_loop_rate` statistic"), any hardcoded "six cells / four design points" in claim-emitting code or prose (must derive from the registered roster), any missing demotion caveat (§1.2 clause 3), and any §8 rerun without n_rerun=40** | Update to B_conf=96/128, SE_FACTOR n=8 = **0.375**, honest joint headline (§13); the selftest grep-check must grep the operative t-convention, B_conf, `INCONCLUSIVE_AT_CEILING`, P1/P2 thresholds, the RED magnitude-bound `\|μ̂\| < κ` form, **[v3.3] the statistic qualifier in every pivot-claim string, the roster-parametric claim generation, the omega-veto clauses, and n_rerun=40 / t₃₉=1.685 / 0.2016 / 0.340** | part of config_hash / prereg |

**Claim limits (Q7 item 8 — frozen, v3.3-scoped):**
- **A GREEN is candidate-selection**, not a measured contrast, until the Movement-3 two-sample contrast runs.
- **A raw-current RED is not automatically a contrast RED** — only under the baseline/equal-arm condition (option 1/3 or Movement 3).
- **[v3.3] The all-RED pivot (option 2) claims raw mismatch currents are sub-floor IN THE `quad_loop_rate` STATISTIC at the REGISTERED GATING CONFIGURATIONS ONLY** (the surviving design points per the §2.1 map; the six-cells-≈-four-points wording is licensed only when nothing was demoted) — **not** across the (τx,τy,Tc) continuum, **not** the tunable contrast, **not** any statement about `omega_roi` beyond "recorded and nowhere GREEN/ANOMALOUS," **not** any statement about `occupancy_x` beyond "recorded," and **not** any statement about a demoted design point (whose unboundedness must be stated as a caveat, §1.2).
- **A Tc>1 GREEN requires a measured two-sample contrast** at confirmatory.

**Unchanged and hash-frozen:** the forward-path harness (`pilot_pair`, Tc threading, the v4.3-inherited estimator), the six cells + geometry, the `v44pilot::` seed namespace, the never-pooled rule. This is an **analysis + declaration recalibration**, not a physics-instrument edit. Re-issue per law #1: regenerate `prereg_v44.json` from `--plan`, record new `config_hash` + `source_sha` + prereg sha256, verify readback, **then** run — **P1 and P2 first (P2 freezes the roster + claim scope), OC simulation (v3.3) passes, scout last.**

---

## 11. Ratification checklist + genuine forks left for Anthony

**Resolved into spec.** Every ChatGPT BLOCK/AMEND (Q1–Q7), the HQ re-pass BLOCK (v3.2), and the whole-object audit findings (v3.3, §16) have a frozen repair above.

**Genuine forks — HQ recommends, Anthony ratifies:**

1. **Q1 contrast-licensing option.** HQ writes v3.3 around **option 2** (all-RED pivot = statistic-and-roster-scoped raw-current claim). Options 1 and 3 documented and available. **HQ rec: option 2.**
2. **The operating point (restated for v3.3).** Three honest repairs stack: Q4 `INCONCLUSIVE_AT_CEILING`, the v3.2 RED magnitude bound, and **[v3.3] the omega veto**. Joint-to-joint pivot-under-null: v3 **0.808** → v3.1 **0.349** → v3.2 **0.148** → **v3.3 ≈ 0.11** (ballpark at ρ_qω=0; OC sim is the number of record). **Fork:** accept the ~0.11-pivot / high-INCONCLUSIVE operating point, OR raise B_max / add seed-averaged grids. **HQ rec: accept it** — each reduction bought a closed leak (ceiling, direction, statistic), and every blocking channel is conservative (never verdict-flipping).
3. **P1 seed sets + threshold + coupling.** N_avg=32 (77001–77032@M4000), N=16 robustness (78001–78016@M400), STABLE ≥12/16, OC-sim ρ sensitivity {0.5, 1, 2}. Revisable.
4. **P2 estimator + criteria.** Tc∈{1,2,4}, n=40/arm→80, bootstrap 10000/rng999/90%CI, material ⇔ R CI-lower>1.10, equivalence [0.909,1.10]. Revisable.
5. **OC acceptance tolerances (§9.3).** false-GREEN ≤0.01, invalid-pivot ≤0.02 (floor, both directions) / ≤0.005 (≥2×), compound GREEN power ≥0.90 at 3×, **[v3.3] omega-failability ≤0.005 at 2×floor, vanish-test power ≥0.90**. Revisable.
6. **Equal-arm choice (§6.1).** τy-matched at matched-Tc (Q6-i). Alternatives documented.
7. **B_max = 128** (Q6-ii) — revisable; couples to Movement-3 compute budget.
8. **Correlated block-noise across A≡B / C≡D.** Baseline independent (reproduces anchors); correlated model is a measure-it sensitivity item, not a rescue. Revisable.
9. **Advisory false-anomaly cap value.** v3.2's terminal six-cell ~0.254 breaches the standing 0.20 soft cap (advisory/non-blocking). Keep 0.20 and record the breach (HQ rec) or widen to 0.30. **[v3.3 note:** the omega veto's null firing (~0.26 six-cell at ρ_qω=0) is a second advisory channel of the same conservative character — report it under the same cap discussion.]
10. **[v3.3 NEW] Omega-veto strength.** HQ writes v3.3 with the veto **pivot-BLOCKING** (an omega GREEN/ANOMALOUS anywhere blocks outcome 2; §5(iii)). The weaker alternative — **annotate-only** (pivot proceeds, claim carries a mandatory HQ-flagged omega caveat) — is documented but **HQ rec: blocking**; an annotation cannot stop a null from being minted over a current the scout's own secondary statistic recorded at super-floor. Anthony's call.
11. **[v3.3 NEW] §8 rerun size.** HQ proposes **n_rerun = 40** (power 0.912 at −1×floor; §13 power table gives n=32 → 0.854, n=48 → 0.947). Larger n buys mislabel margin at compute cost. Revisable; the ≥0.90 gate (gate 9) is the invariant.

---

## 12. ChatGPT Q1–Q7 reconciliation (all v3.1/v3.2 satisfactions PRESERVED in v3.3)

| ChatGPT Q | v3.1/v3.2 resolution | v3.3 status |
|---|---|---|
| **Q1** — contrast-proxy estimand | raw-current claim (option 2); estimand-(a) refused for Tc>1; GREEN=candidate-selection; v3.2 scoped the claim to the probed configurations | **preserved + completed:** claim now also scoped on the **statistic axis** ("in `quad_loop_rate`") and the **cell axis** (roster-parametric, shrinks under demotion) (§2.1, §5, §10) |
| **Q2** — four-band / ANOMALOUS | frozen anomaly state machine; Student-t₁₅ false-anomaly correction (v3.2) | **preserved + powered:** the machine's structure is unchanged; STATE B's vanish test is now a predeclared powered test (n_rerun=40, power 0.912 ≥ 0.90) so the machine stops discarding real opposite-physics ~39% of the time (§8) |
| **Q3** — RED conjunction / MC | coupled-upper conjunction kept exactly; 4M-draw MC; v3.2 applied it to `\|μ̂\|` | **preserved verbatim** (§3.3) |
| **Q4** — sequential loop / pivot | `INCONCLUSIVE_AT_CEILING` blocks the pivot; four honest outcomes; STANDING RULE | **preserved;** the STANDING RULE now enumerates all three axes (ceiling, direction, statistic/cell-roster) of the same category error |
| **Q5-P1** | high-M seed-averaged σ_cell; STABLE ≥12/16; coupled OC modeling (v3.2) | **preserved verbatim** (§1.1, §9.1) |
| **Q5-P2** | fully operationalized gate; P2 before the scout | **preserved + completed:** the demotion branch's downstream consequences — roster, claim scope, descriptive-band dispositions — are now pinned (§1.2); v3.2 left them undefined |
| **Q6** — open leans | τy-matched equal arm; B_max=128; refuse Tc>1 estimand-(a); 16 blocks; P1 pin | **preserved** (§1.1, §4, §6.1) |
| **Q7** — re-issue scope / claim limits | claim limits stated; prereg scope expanded; boundary selftests; v3.2 magnitude-bound greps | **preserved + expanded:** omega-veto/roster/rerun cutpoint selftests added; grep extended to the statistic qualifier, roster-parametric claim generation, and n_rerun constants (§9.4, §10) |

---

## 13. Measured / derived operating characteristics (v3.2 session numbers retained; v3.3 additions appended — the v3.3 OC sim is the registration-grade instrument)

*The v3.2 numbers below were measured with a throwaway full-loop simulation of the v3.2 rule (`/usr/bin/python3`, numpy 2.0.2, 1×10⁶ tail trials) that reproduced the v3.1 anchors exactly. **The v3.3 additions (vanish-test power table, reband-channel estimate, omega-veto ballpark) were computed this session** (`/usr/bin/python3`, scipy Student-t + 4×10⁵-draw MC per rerun size, rng 20260708). All are HQ arithmetic checks, not the registration OC sim — §9 specifies the instrument of record.*

**Anchor reproduction (v3.1 rule) — retained:**

| Quantity | v3.1 OC report | v3.2 check |
|---|---|---|
| per-cell terminal RED (null) | 0.839 | **0.839** |
| per-cell INCONCLUSIVE (null) | 0.126 | **0.126** |
| per-cell ANOMALOUS (null) | 0.0346 | **0.0345** |
| joint P(pivot \| null) | 0.349 | **0.349** |
| wrong-sign-at-floor: cell RED | 0.386 | **0.388** |
| wrong-sign-at-floor: invalid pivot | 0.160 | **0.161** |

**v3.2 rule (magnitude-bounded RED) — retained:**

| Quantity | v3.1 | **v3.2** |
|---|---|---|
| single-pass 16b RED (null) | 0.570 | **0.207** |
| per-cell terminal RED (null) | 0.839 | **0.727** |
| per-cell terminal INCONCLUSIVE (null) | 0.126 | **0.225** |
| per-cell terminal ANOMALOUS (null) | 0.0345 | **0.048** |
| **joint P(pivot \| null)** | 0.349 | **0.148** |
| six-cell false-anomaly (6-indep) | 0.190 | **0.254** |

**Wrong-sign protection (v3.2 measurements, retained; reband channel appended [v3.3]):**

| Δ (wrong sign) | metric | v3.1 (aligned RED) | v3.2 belt (magnitude RED) | belt+suspenders* |
|---|---|---|---|---|
| −1× floor | cell bands RED | 0.388 | **0.033** | 0.033 |
| −1× floor | terminal ANOMALOUS | 0.612 | 0.873 | 0.873 |
| −1× floor | **P(invalid pivot), reband channel EXCLUDED (v3.2 accounting)** | **0.161** | **0.0066** | **~0** |
| −1× floor | **[v3.3] P(invalid pivot), reband channel INCLUDED, powered rerun** | — | **≈ 0.007** (extra cell-RED ≈ 0.873·0.088·0.033 ≈ 0.0025; OC sim = number of record) | ~0 |
| −2× floor | cell bands RED | — | 2×10⁻⁵ | 2×10⁻⁵ |
| −2× floor | **P(invalid pivot)** | — | **3×10⁻⁶** | **0** |

*\*belt+suspenders hardcodes the wrong-sign cell UNSTABLE as an illustration; the registration OC sim (§9.1) models STABLE from coupled P1-B draws.*

*(v3.2's note on the 0.033-vs-0.027 residual-tail modelling difference is retained: it does not affect gate-clearance; the OC sim is the number of record.)*

**Symmetry (both at floor magnitude, v3.2, retained):** predicted-direction invalid pivot (S2) = **0.0067**; wrong-sign invalid pivot (S5, belt) = **0.0066** (reband-exclusive) / **≈ 0.007** (reband-inclusive, powered [v3.3]). Both clear the ≤0.02 gate.

**[v3.3] §8 vanish-test power vs rerun size (MC, 4×10⁵ draws per n, one-sided tₙ₋₁ against 0, honest SE = sd·√(1/n+1/64), true Δ = −1×floor(96) = −0.557·sd):**

| n_rerun | t₀.₉₅(n−1) | SE factor | power at −1×floor |
|---|---|---|---|
| 16 | 1.753 | 0.2795 | 0.613 *(the unpowered v3.2 single-look scale — mislabel 0.387)* |
| 24 | 1.714 | 0.2394 | 0.762 |
| 32 | 1.696 | 0.2165 | 0.854 |
| **40 (ADOPTED)** | **1.685** | **0.2016** | **0.912 ≥ 0.90 (gate 9)** — mislabel 0.088 |
| 48 | 1.678 | 0.1909 | 0.947 |

**[v3.3] TRUE-OPPOSITE-PHYSICS retention at −1×floor:** ≈ 0.87 (anomaly surfaces through the ladder) × 0.912 (powered rerun persists) ≈ **0.79 end-to-end** (was ≈ 0.87 × 0.61 ≈ 0.53 at the unpowered rerun — the v3.2 machine silently discarded ~39% of the real opposite-physics that reached it).

**[v3.3] Omega-veto null arithmetic (ballpark, quad⊥omega independence, ρ_qω=0):** per-cell terminal omega GREEN/ANOMALOUS under null ≈ 0.048 + 0.001 = **0.049**; six-cell veto-fires ≈ 1−(1−0.049)⁶ ≈ **0.26**; joint P(pivot | null) ≈ 0.148 × (1−0.049)⁶ ≈ **0.109 ≈ 0.11**. The quad↔omega block-noise correlation ρ_qω (same trajectories!) moves both numbers — the §9.1 sweep is mandatory and the OC sim is the number of record. The veto only ever blocks; it cannot mint.

**Anomaly-screen honesty (v3.2, retained):** the standalone 16b screen has power 0.61 at −floor, ~0.90 at −1.45×floor — too weak to be the guarantee. The magnitude bound + STABLE carry the wrong-sign guarantee; **[v3.3] the powered §8 rerun now also stops the screen's survivors from being mislabeled on the way out.**

---

## 14. v3.1 re-pass reconciliation (HQ diverse-lens BLOCK → v3.2 disposition — retained, all in force)

| Re-pass finding | Severity | v3.2 disposition (unchanged in v3.3) | § |
|---|---|---|---|
| **RED bounds only `x=σμ̂`, never `\|μ̂\|`; wrong-sign-at-floor bands RED ~39% → invalid pivot ~16%** | **BLOCKER (3 lenses)** | RED magnitude bound (aligned conjunction kept AND `\|μ̂\|+t·SE<floor_c` coupled-upper). Invalid pivot 0.161→0.0066; RED-banding 0.388→0.033. STANDING RULE added. | §3, §3.3, §5, §7 |
| **STABLE hardcoded, never measured** | **BLOCKER** | belt (magnitude bound) + suspenders (STABLE); OC sim models STABLE from coupled M=400 draws, ρ sensitivity. | §1.1, §5, §9.1 |
| **Hard gate 5a mis-specified at −floor (~0.61 achievable)** | **BLOCKER** | guarantee moved to the joint `P(invalid pivot \| wrong-sign at floor) ≤ 0.02`; screen power advisory. | §9.3 |
| **Hard gate 5b (`P(pivot)==0`) impossible** | major | restated as ≤0.02 / ≤0.005 at ≥2×, probing \|current\| AT the floor. | §9.3 |
| **Pivot claim over-scoped as a continuum** | major | scoped to the probed configurations (≈4 design points) — **[v3.3] further completed on the statistic + roster axes, §16**. | §2.1, §5, §10 |
| **Headline mixed per-cell with joint rate** | major | honest joint-to-joint 0.808→0.349→0.148 (→≈0.11 in v3.3). | §11 fork 2, §13 |
| **False-anomaly normal-approx; SE_FACTOR comment; two-sided reachability** | minor | Student-t₁₅ 0.0344 screen / ~0.048 terminal / ~0.254 six-cell; SE_FACTOR n=8 = 0.375; two-sided RED unreachable at 16b documented. | §3, §2.3, §9.1 |

**Note on internal consistency (law #4, retained).** All *stochastic* OC rates use the **independent per-cell block-noise** model that reproduces the receipt-06 anchors. "≈4 independent design points" is **claim-scope**, never applied to soften a stochastic rate. Correlated A≡B/C≡D noise is fork 8; **[v3.3]** quad↔omega noise correlation ρ_qω is the analogous mandatory sweep (§9.1).

---

## 15. Antigravity re-audit target (updated for v3.3)

The lineage of caught-then-fixed category errors: ChatGPT caught the ceiling axis (Q4); the HQ diverse-lens re-pass caught the direction axis (v3.2 magnitude bound); **the whole-object scope audit caught the statistic and cell-roster axes plus the unpowered vanish test (this revision)**. Each pass found the error the previous passes normalized.

**Re-audit target for the next Antigravity pass (v3.3):**
1. **The statistic-scoped claim + omega veto** (§2.1, §5(iii), §7) — verify every pivot-claim string carries "in the `quad_loop_rate` statistic"; verify an omega GREEN/ANOMALOUS in any cell (gating or demoted) returns False from `pivot_licensed`; independently construct the S8 omega-only scenario and confirm the veto is failable (gate 8).
2. **The roster-parametric claim + demotion dispositions** (§1.2, §2.1 map, §7) — verify the claim text is generated from the registered roster (grep for hardcoded "six cells"/"four design points" in claim-emitting paths); verify a demoted AxT4 removes (τy=2,Tc=4) from the claim; verify demoted-cell GREEN forces outcome 1 and demoted-cell ANOMALOUS blocks; verify the roster assertion rejects missing/extra cells (S9, gate 10).
3. **The powered §8 vanish test** (§8, §13) — independently recompute the power table (n=40 → 0.912 at −1×floor with t₃₉=1.685, SE factor 0.2016) and the reband-channel arithmetic (≈0.0025 extra cell-RED; invalid pivot ≈0.007 ≤ 0.02); verify S5 simulates the full loop and gate 5's number of record includes the channel.
4. **v3.2 items still standing:** the RED magnitude bound + coupled-upper conjunction (re-derive 0.161→0.0066), belt-and-suspenders coupled-STABLE modeling + ρ sensitivity, restated gates 5/5′ (not a scenario-weakening dodge), the honest joint headline (0.808→0.349→0.148→≈0.11), the t₁₅ false-anomaly ≈0.254 vs the standing 0.20 advisory cap (fork 9), claim-scope vs noise-independence separation, two-sided RED unreachability at 16b, SE_FACTOR n=8 = 0.375.
5. **The extended STANDING RULE itself** — grep every terminal claim in this document against all three axes (direction / statistic / cell set) and report any residual projection or shrunk-denominator wording this revision missed.

---

## 16. v3.2 → v3.3 reconciliation (whole-object scope audit findings → dispositions) — [v3.3]

The audit returned seven findings; deduplicated across the three review passes they resolve to **three defects** (the statistic-axis blocker was found independently by all three passes; the cell-roster major by all three; the vanish-test major by one). Every finding row is dispositioned:

| # | Audit finding (deduplicated source passes) | Severity | v3.3 disposition | § |
|---|---|---|---|---|
| 1 | **Statistic-axis over-scope:** pivot claim "raw mismatch currents are sub-floor at the probed configurations" bounded ONLY `quad_loop_rate`; `omega_roi` (sensitivity 0.83 vs 0.90; carrier of the 2.2σ κ-suppression lean; physically able to carry a current quad misses — counter-rotating loop pairs; v4.3 occupancy precedent) was descriptive and excluded from `pivot_licensed`, so six descriptive omega GREENs at +3×/+2× floor could coexist with a fired pivot. *(All three passes; BLOCKER + two majors.)* | **BLOCKER** | **(a)** Every pivot-claim instance re-worded: sub-floor **"in the `quad_loop_rate` statistic"**; omega and occupancy named in the claim as recorded-and-unbounded (§2.1, §5 outcome 2, §10). **(b)** **Omega veto, pivot-BLOCKING** (HQ rec over annotate-only, fork 10): omega GREEN or ANOMALOUS in ANY cell (gating or demoted) blocks the pivot, HQ-flagged, formal disposition required (§5(iii)); `pivot_licensed` consumes `omega_bands` (§7). **(c)** Failability selftest S8 (omega-only current at 2×floor must block) + hard gate 8 ≤ 0.005 + ρ_qω sweep (§9). STANDING RULE extended to the statistic axis. | §0.2 D1′, §2.1, §3, §5, §7, §9, §10 |
| 2 | **Cell-roster demotion leak:** P2 could demote AxT2/AxT4 to DESCRIPTIVE ("does not gate the pivot") while §2.1/§5/§10 froze the claim at "the six cells ≈ four independent design points"; the gating set for conditions 0/(i) was undefined; `pivot_licensed` had no roster assertion; a demoted cell's GREEN or INCONCLUSIVE had no pinned effect — a null over 4 design points could be minted from bounds on 2 (both Tc points unbounded) or 3 (AxT4 sole-carries (τy=2,Tc=4)). *(All three passes; majors.)* | **major** | **(a)** **Roster-parametric claim:** the registered post-P2 gating roster + surviving design points are frozen into the prereg; claim text derives from the §2.1 design-point map (AxT2/AxT4 are sole carriers; their points LEAVE the claim on demotion); "six cells ≈ four points" licensed only with no demotion (§1.2 clause 2, §2.1, §6.1). **(b)** **Pinned demoted-cell dispositions** (§1.2 clause 3): primary GREEN → forces outcome 1 (no pivot); primary ANOMALOUS → §8, blocks; omega GREEN/ANOMALOUS → veto; RED/AMBER/INCONCLUSIVE → recorded non-gating + **mandatory verdict caveat** naming the unbounded point (law-#4 grep item). **(c)** **Roster assertion in `pivot_licensed`** (§7): evaluated set must equal the registered roster exactly. **(d)** Failability selftest S9 + deterministic gate 10 (§9). STANDING RULE extended with the shrink sentence. | §1.2, §2.1, §5, §6.1, §7, §9, §10 |
| 3 | **Unpowered §8 vanish test:** STATE B minted GRID-ARTIFACT off ONE rerun of unspecified n; at the 16b scale a real −1×floor wrong-sign current falsely "vanished" ~39.5% (screen power ~0.61; higher M does not lower the floor, DIAG 1), silently discarding TRUE-OPPOSITE-PHYSICS ~39% of the time it surfaced; the reband re-entered the pivot pool through a channel omitted from §13's 0.0066 and not explicitly required in §9 S5. Recomputed with the channel: invalid pivot ≈0.009 — under the 0.02 gate (no gate breach), but an evidence-destruction + accounting defect. *(One pass; major.)* | **major** | **(a)** **Powered vanish test:** n_rerun = **40 fresh blocks**, one-sided t₃₉ = 1.685, SE = 0.2016·sd, significance edge 0.340·sd; measured power **0.912 ≥ 0.90** at −1×floor (MC, §13); mislabel 0.395 → 0.088; TRUE-OPPOSITE-PHYSICS end-to-end retention 0.53 → ≈0.79 (§8, §13). **(b)** **Hard gate 9** (vanish-test power ≥ 0.90, asserted in-sim). **(c)** **S5 must simulate the full §8 loop** (rerun + reband re-entry); **gate 5's number of record includes the reband channel** (analytic ≈0.007 ≤ 0.02) (§9.1, §9.2, §9.3). **(d)** n_rerun choice left revisable as fork 11 (table of n vs power in §13). | §8, §9, §13, §2.2/§2.3 (t₃₉ row) |

**Whole-object audit clean-scope check (the audit's own axis, applied to v3.3):** the pivot claim now names its statistic (`quad_loop_rate`), its exact cell denominator (the registered roster, mechanically asserted), its direction coverage (the `|μ̂|` magnitude bound), and its explicit non-claims (omega beyond the veto, occupancy, demoted points, interior continuum, contrasts). No terminal claim in this document asserts more than its gating arithmetic bounds.

---

*End v3.3 draft. Status: DRAFT for ChatGPT re-review + Antigravity re-audit + Anthony final-say. Not registered, not chronicled, no harness bytes edited, not committed. v3 (`138d109`), v3.1, v3.2, and `v44_scout.py` (`source_sha 0b65a9ee92b9fe2c`) remain unmodified. The registration-grade v3.3 OC simulation (§9) is the next build phase.*
