# v4.4 Scout — Operating-Characteristic Simulation Report (Decision Rule v3.1)

*HQ (Mac Studio Claude Code seat, overwatch/provenance), 2026-07-07. This is the
full-loop OC simulation ChatGPT's Q4 required before the v4.4 scout can register.
It simulates the **entire frozen state machine** of `v44_scout_DECISION_RULE_v3.1.md`
(§9 spec), all six cells jointly, and measures the predeclared acceptance criteria.
**NOT registered, NOT chronicled, edits NO harness bytes.** This is analysis of the
draft v3.1 rule, for ChatGPT re-review + Antigravity re-audit + Anthony final-say.*

- **Simulator:** `oc_simulation_v31.py` (this directory)
- **Raw results:** `oc_results_v31.json` (machine-readable), `oc_sim_output.txt` (console)
- **Interpreter:** `/usr/bin/python3` (Python 3.9.6, numpy 2.0.2), scipy 1.13.1 (selftest cross-check only)
- **RNG:** `numpy.default_rng`, base seed `20260707` (per-scenario offsets pinned in source)
- **Trials:** 1×10⁶ for the false-GREEN / invalid-pivot tail scenarios (S1, S2, S3-2×, S3-3×); 2×10⁵ elsewhere

---

## VERDICT: **OC-flags-found**

Eight of ten hard-gate checks pass. **Two fail, both in the wrong-sign scenario (S5), and they are the same real defect:** the anomaly gate does not adequately protect the pivot against a *floor-magnitude* wrong-sign effect. This is exactly the category error a full-loop OC sim exists to catch — the local §3.3 Monte Carlo and per-contrast analytic power cannot see it. The flag is **magnitude-specific** and **actionable** (details below). The load-bearing safety gate — **P(invalid pivot | a real predicted-direction effect at/above floor)** — **passes** (1.5% at floor ≤ 2%; ~0 above floor).

---

## 1. Whole-loop validation anchor (independent check)

The simulation reproduces the per-cell null terminal distribution that Antigravity R2 recomputed from a different seat (v3.1 §13), confirming the band logic **and** the 16→32 accumulation dependence are correct in one shot:

| Quantity | AG R2 / spec anchor | This sim (S1, 1×10⁶) |
|---|---|---|
| Per-cell terminal RED | 0.852 | **0.839** |
| Per-cell INCONCLUSIVE_AT_CEILING | 0.123 | **0.126** |
| Per-cell ANOMALOUS | 0.025 (planning) | **0.0346** |
| Per-cell GREEN | ~2×10⁻⁴ | **4.0×10⁻⁴** |
| P(pivot \| null), v3.1 | ~0.38 | **0.349** |
| P(≥1 INCONCLUSIVE) \| null | ~0.55 | **0.555** |

The only material deviation is the **anomaly rate** (0.0346 vs the spec's 0.0251) — see Finding B. The extra ~0.9%/cell anomaly mass is what pulls RED from 0.852 to 0.839 and the pivot from 0.38 to 0.35. Everything else lands on the anchor.

---

## 2. Hard-gate acceptance criteria (§9.3)

| # | Criterion | Scenario | Measured (±MCSE) | Tolerance | Pass |
|---|---|---|---|---|---|
| 1 | P(any false GREEN) | S1 global null | 0.00247 ±5e-5 | ≤ 0.01 | **PASS** |
| 2 | **P(invalid pivot) — at floor** | S2 (Δ=floor, predicted dir) | 0.01532 ±1e-4 | ≤ 0.02 | **PASS** |
| 3a | P(invalid pivot) — 2× floor | S3 2× | 8×10⁻⁶ | ≤ 0.005 | **PASS** |
| 3b | P(invalid pivot) — 3× floor | S3 3× | 0 | ≤ 0.005 | **PASS** |
| 4 | P(registrable GREEN) compound power | S3 3× floor | 0.99997 | ≥ 0.90 | **PASS** |
| 5a | P(wrong-sign cell ANOMALOUS) | S5 (Δ=−1×floor) | **0.6137** ±5e-4 | ≥ 0.90 | **FAIL** |
| 5b | P(pivot fired) — must be 0 | S5 (Δ=−1×floor) | **0.1601** ±8e-4 | = 0 | **FAIL** |
| 6a | Partition completeness (no limbo) | S1–S7 | 0 limbo trials | = 0 | **PASS** |
| 6b | Zero cells terminate AMBER (deadlock) | S1–S7 | 0 cells | = 0 | **PASS** |
| 7 | law #2 — planted 3× signal breaks pivot (cell non-RED) | S3 3× | 1.000 | ≥ 0.90 | **PASS** |

**No deadlock / un-banded state at any config:** across all seven scenarios (≈4.6×10⁶ trials × 6 cells), **zero** trials landed in limbo and **zero** cells terminated in AMBER. Every cell resolves to exactly one of {GREEN, RED, ANOMALOUS, INCONCLUSIVE_AT_CEILING} and every trial classifies to exactly one terminal outcome. The four-band partition and the terminal ladder are complete.

---

## 3. The load-bearing safety gate: P(invalid pivot) — a real effect must never be pivoted away

This is the direct measure of the "mint evidence of absence" error the whole Q4 repair exists to prevent, for effects **in the predicted direction**:

| True effect on one cell (predicted direction) | P(invalid pivot) | Interpretation |
|---|---|---|
| Δ = 1× floor (borderline-detectable) | **0.0154** | ≤ 0.02 gate — a real at-floor effect survives the pivot in 98.5% of runs |
| Δ = 2× floor | **8×10⁻⁶** | collapses to ~0 |
| Δ = 3× floor | **0** | never pivoted away |

For predicted-direction effects the pivot is safe: **a real effect at or above the floor is essentially never pivoted away.** The single at-floor case (1.5%) is the honest residual of a borderline-MDE effect and sits inside its predeclared 2% tolerance. This is the number to treat as load-bearing, and it holds.

### Q4 is actually fixed — a genuinely-underpowered real effect terminates INCONCLUSIVE, not RED

A cell carrying a **genuine at-floor effect in the predicted direction** (Δ = 1× floor) terminates:

| Terminal | Probability |
|---|---|
| INCONCLUSIVE_AT_CEILING (protected — blocks pivot) | **0.844** |
| GREEN (registrable) | 0.118 |
| RED (would enable pivot-away) | **0.038** |
| AMBER (deadlock) | 0.000 |

84% of the time the underpowered real effect lands **INCONCLUSIVE_AT_CEILING**, which **blocks** the pivot — it is *not* laundered into RED. Under the old v3 rule those same runs were relabeled `RED_AT_CEILING` and **counted toward the pivot**, minting evidence of absence for a cell whose CI still overlaps the floor. The Q4 repair is verified in the loop:

- **v3 (mislabel ceiling→RED), P(pivot \| null):** ≈ **0.808** (per-cell RED+ceiling = 0.965, joint over six cells; independence approximation)
- **v3.1 (INCONCLUSIVE blocks), P(pivot \| null):** **0.349** (measured)

The ~0.46 drop is precisely the mass of runs where ≥1 cell's confidence interval still overlaps the floor at the B_max=128 compute ceiling. That mass is now honestly reported as INCONCLUSIVE rather than converted to a null. *(Note: v3.1 §11 quotes the v3 operating point as ~97.5%; that figure is the per-cell RED+ceiling rate mis-read as a joint pivot rate — the honest six-cell joint v3 pivot is ~0.80. The direction and magnitude of the repair hold either way.)*

---

## 4. Findings (pathologies surfaced)

### Finding A — LOAD-BEARING: the anomaly gate under-protects the pivot against floor-magnitude wrong-sign effects (S5)

**What the sim shows.** With one cell carrying a **true wrong-sign current at floor magnitude** (Δ = −1× floor, exactly as §9.2 constructs S5):

- P(that cell flagged ANOMALOUS) = **0.614** (criterion wanted ≥ 0.90)
- P(that cell terminates **RED** instead) = **0.386**
- P(the scout **pivots** — a raw-current null declared over a real opposite-direction floor effect) = **0.160**

A wrong-sign effect at floor magnitude is a **real effect** (it sits at the two-arm MDE). The pivot's "no open anomaly" guard (§5 condition 0) is supposed to protect against exactly this, but the anomaly gate is a **one-sided α=0.05 screen** against 0, whose power at floor magnitude is only ~61%, while the floor is a 90%-power / 99%-level MDE. The ~39% of trials the gate misses band the cell **RED** ("sub-floor raw current in the predicted direction"), and when the five null cells also go RED the scout **pivots away from a real effect** ~16% of the time — **10× the predicted-direction invalid-pivot rate (S2, 1.5%).** Directionality matters: an effect in the *unpredicted* direction is an order of magnitude more likely to be pivoted-away than one in the predicted direction.

**The failure is magnitude-specific — confirmed by S5-strong.** Re-running with the *actual* 3.6σ Finding-4 artifact (Δ = −1.0·sd = −1.79× floor, the μ̂≈−1.0·sd excursion the acceptance row assumes):

- P(ANOMALOUS) = **0.974** — the gate trips reliably on an unambiguous artifact
- P(invalid pivot) = **0.011** — nearly closed

So the anomaly gate works as designed for **large** wrong-sign artifacts; it is the **floor-magnitude** wrong-sign region (2.2σ, exactly the region an at-MDE opposite-direction effect lives in) that leaks.

**Two things this exposes, for the reviewers to adjudicate:**
1. **Spec internal inconsistency.** §9.2 constructs S5 at Δ=−1×floor (a 2.2σ excursion), but the §9.3 acceptance row expects "3.6σ trips reliably." Those are different magnitudes; the criterion cannot be met by the scenario it is attached to. Either the scenario should be strengthened to the 3.6σ artifact (then it passes: 97.4% / 1.1%), **or**
2. **Genuine rule gap.** If protecting against *floor-magnitude* wrong-sign effects is the intent (the task's "a real effect must never be pivoted away"), the current one-sided α=0.05 anomaly gate is too weak there. Options: a lower anomaly threshold, a two-sided anomaly rule, or extending RED cells through a confirmatory before letting them count toward the pivot.

Note that even the strong artifact leaves a **1.1% residual invalid pivot** — the `P(pivot)==0` criterion is structurally unachievable for any finite wrong-sign magnitude (there is always a tail where μ̂ lands in the RED bucket), so the `==0` tolerance itself is too strict and should be restated as a small bound (e.g. ≤0.02).

### Finding B — the spec's false-anomaly rate is understated (normal-approx vs t)

Per-cell false-anomaly under the null is **0.0346** (sim), not the spec's **0.0251**. The spec computed Φ(−1.96)=0.025 using a **normal** approximation, but the anomaly statistic is μ̂/(sd̂/4) with sd̂ *estimated*, so the pivotal quantity is **t₁₅**, not z. P(t₁₅ < −1.96) ≈ 0.034. Consequently the six-cell P(≥1 false anomaly) is **0.190** (sim), above the spec's 0.141 planning figure and near the 0.20 soft cap. This is **not a safety failure** — a false anomaly *blocks* the pivot (conservative) and never mints a wrong verdict — but the planning number should be corrected to the t-based ~14% per-look / ~19% six-cell, and the soft cap (0.20) has only a ~0.01 margin. The same t-vs-normal effect makes the false-GREEN rate 0.0025 (sim) vs the spec's ~2×10⁻⁴ — still comfortably inside the 0.01 gate, but ~10× the normal-approx expectation.

### Finding C — GREEN tie-break cannot order adjacent candidates at 16 blocks (advisory, not a defect)

With the spec's S4 spacing (2×/2.5×/3× floor), P(tie-break picks the true-best cell | ≥2 GREEN) = **0.691** (advisory wanted ≥0.90). The 2.5× and 3× cells are 0.278·sd apart while first-pass μ̂ noise is 0.25·sd, so the highest-margin argmax frequently swaps them. This is a **true operating characteristic**, not a bug: with a separated slate (S4b, 2×/3×/5×) the tie-break is correct **0.994** of the time. It is advisory and does not flip the verdict, but registration prose should not claim the tie-break reliably ranks near-neighbor candidates.

### Finding D — the block-extension *raises* GREEN power above the single-pass estimate (benign)

P(registrable GREEN) at 2× floor is **0.917** (sim), well above the spec's first-pass expectation of ~0.605. The 16→32 accumulation ladder adds detection power the per-pass arithmetic omits. Benign and favorable, but the reported power curve should use the whole-loop numbers (1×: 0.12, 2×: 0.92, 3×: ~1.00), not the single-pass ones.

---

## 5. Other reported operating characteristics

### S6 — Tc-heteroscedastic (null, Tc cells scaled ×1.25 / ×1.62 per receipt-06)
Per-cell `sd_cell` banding **neutralizes** the Tc SD growth exactly as intended: false-GREEN = 0.00239 (≈ S1's 0.00247), pivot = 0.347 (≈ S1's 0.349). The scale-free banding removes the heteroscedasticity; the Tc SDs do not perturb the OC.

### S7 — nonzero equal-arm offset (sizes the Q1 raw-vs-contrast gap)
Injecting a real offset into the raw current materially shifts the raw-current pivot — the concrete demonstration of why the option-2 pivot is a raw-current claim and **not** a contrast claim:

| Offset (added to every cell) | P(pivot) | P(any GREEN) | P(any INCONCLUSIVE) |
|---|---|---|---|
| none (S1 baseline) | 0.349 | 0.0025 | 0.555 |
| +0.10× floor | 0.222 | 0.0049 | 0.738 |
| +0.30× floor | 0.041 | 0.0176 | 0.955 |

A +0.30·floor equal-arm offset nearly **eliminates** the raw-current pivot (0.349 → 0.041) and pushes 95% of runs to INCONCLUSIVE. An unmodeled equal-arm offset of this size changes the outcome completely, quantifying the Q1 gap: the raw-current pivot says nothing about the mismatch-minus-equal contrast unless the equal arm is separately measured (options 1/3 or Movement 3).

---

## 6. Bottom line

- **The instrument is sound and complete:** no deadlock, no un-banded state, full four-band partition, terminal ladder terminates, boundary/cutpoint selftests (§9.4) all pass, frozen constants cross-checked against scipy.
- **Q4 is verified fixed:** a genuinely-underpowered real (predicted-direction) effect terminates INCONCLUSIVE_AT_CEILING (84%) and blocks the pivot; it is never laundered into RED. The compute ceiling no longer mints evidence of absence (null pivot 0.35 vs v3's ~0.80).
- **The predicted-direction safety gate holds:** P(invalid pivot | real at-floor effect) = 1.5% ≤ 2%; ~0 above floor.
- **One real flag blocks a clean pass (S5):** the anomaly gate under-protects the pivot against *floor-magnitude wrong-sign* effects (61% detection, 16% invalid pivot), confirmed magnitude-specific by S5-strong (97% / 1%). This must be adjudicated before registration — strengthen the anomaly gate/threshold, or (if the criterion intends only unambiguous artifacts) fix the spec's S5 scenario/criterion inconsistency and restate `P(pivot)==0` as a small bound.
- **Two spec numbers to correct (non-blocking):** false-anomaly ~14%→~19% six-cell (t vs normal); GREEN power curve should use whole-loop, not single-pass, values.

*End OC report v3.1. Status: DRAFT analysis for re-review + re-audit + Anthony final-say. No harness bytes edited; frozen artifacts untouched.*
