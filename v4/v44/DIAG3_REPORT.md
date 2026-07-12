# DIAG 3 — The Signal-Fidelity M-Sweep

*HQ scout diagnostic, 2026-07-12. **This is a PILOT. It registers nothing, authorizes nothing, and ratifies nothing.** Seed namespace `diag10::` — quarantined from `v44pilot::` and `v43::`, never pooled (law #6). Registration remains Anthony's gate and his alone (law #1).*

---

## 0. Headline

**M = 400 IS SAFE FOR THE SCOUT — on the channel this diagnostic can bound. The registered M should NOT be raised for signal fidelity.**

Across **14 measured cells / 9,800 blocks**, the realized response to a known, calibrated vortex is **essentially M-independent from M=400 out to M=8000** (a 20× grid range). The attenuation factor R lands in **[0.955, 1.021]**; the worst-case 95% inflation of the minimum detectable *true* current is **1.087** — under 9%.

**Scope this correctly.** The vortex is an **external force**. The scout's engine signal is **grid-generated** (a difference of two independently-estimated noisy S_c grids). This diagnostic **bounds the external-force channel** and **reduces — but does not directly bound — the grid-generated channel**. §7 is not boilerplate; read it. The verdict below is *sufficient to proceed at M=400*, not a proof that grid roughness cannot attenuate a grid-generated current.

**Receipt 06's DIAG-3 finding does not replicate.** Its headline — omega suppressed ~33% at M=400 (R = 0.67, ~2.2σ, n=20) — is **excluded at 13–25σ** by this powered measurement. It was a small-n sampling fluctuation, exactly as its own caveat warned ("n=20/arm is scouting-grade … suggestive, not definitive"). That caveat was correct and it did its job.

**Law #9 / supersession:** receipt 06 is **not edited**. This report is recorded *alongside* it. Receipt 06's DIAG 1 and DIAG 2 stand unchallenged; only its **DIAG 3** section is superseded.

---

## 1. What was actually asked

The open thread reads "does M=400 grid noise attenuate the MEAN realized aniso current?" — easily misread as the *floor* question. **DIAG 1 already answered the floor question** (receipt 06): SD ratio M400→M2000 was quad 1.19 [0.80, 1.74], omega 0.87 [0.61, 1.25]. **The floor is trajectory-limited; raising M does not lower it.** Not re-run here.

The live question is **signal fidelity**: does M=400 grid roughness *suppress the realized response* to a real current, such that a true engine current is attenuated below floor by a coarse grid and read as "no engine"? That is a **false null-branch firing** — the single most dangerous failure mode left in this design. It is the v4.2 estimator-roughness mechanism.

---

## 2. Design

| | |
|---|---|
| **Signal source** | Registered c4v vortex arms, **κ ∈ {4, 8}** (`c4v_kappas [0,2,4,8]`) — the v4.3 G1 control, a *calibrated true signal*. κ=0 is the paired null. |
| **Estimand** | **R = increment@M_lo / increment@M_hi**, where increment = mean(y \| κ) − mean(y \| κ=0) at matched (M, block). **R < 1 ⇒ the coarse grid attenuates the realized response.** The quantity of interest is the RATIO OF MEANS, not the SD. |
| **Statistics** | `quad_loop_rate` (primary) **and** `omega_roi` (secondary — the one v4.4 may promote to primary, and the one receipt 06 flagged). Both reported for every cell. |
| **Chamber** | `run_chamber("frozen", τ, seed, scale=10.0, tau_y=…, M_grid_ov=M, Tc_ov=1.0, vortex_kappa=κ)` |
| **CFG** | **NEVER EDITED.** M passed via the **`M_grid_ov` override**, as receipt 06 did. `config_hash` stayed **`a344d6c47c8a22c1`** on every one of the 9,800 rows — verified, identical to `prereg_v44.json`. |
| **Harness** | **PRISTINE, unedited `v44_scout.py`**, `source_sha 0b65a9ee92b9fe2c…`. Snapshotted to a scratch copy **before any work began** and imported from the copy, so this run is pinned to the unedited harness regardless of what later phases do to the worktree. Re-verified pristine at end. |
| **Interpreter** | `/usr/bin/python3` — Python 3.9.6, numpy 2.0.2 (canonical). |
| **Seeds** | `sha256("diag10::" + unit_id)`, mirroring the harness's own convention. Unit id **excludes κ** (see §3) and **includes M and τ** (arms independent across M; no collisions — verified 4,000 unique units, 9,800 unique (unit, κ)). |
| **Bootstrap** | **8,000 resamples**, fixed `rng=999`, resampling the **paired-difference vectors** (§3). |
| **Raw record** | `diag3_raw.ndjson` — 9,800 rows, primary record (law #7). |

### 2.1 Power calculation — stated BEFORE the run

From an n=32 anchor pilot (which also confirmed the seed scheme reproduced receipt-06's *direction*: every cell R < 1):

| cell | sd(d)@400 | sd(d)@2000 | R̂ | combined rel-sd | n for SE(R)=0.025 |
|---|---|---|---|---|---|
| k4 quad | 8.85e-5 | 8.74e-5 | 0.806 | 0.918 | **878** |
| k4 omega | 7.20e-5 | 5.54e-5 | 0.919 | 0.793 | 851 |
| k8 quad | 7.18e-5 | 7.67e-5 | 0.877 | 0.400 | 197 |
| k8 omega | 6.39e-5 | 6.80e-5 | 0.943 | 0.385 | 211 |

**Target: SE(R) ≤ 0.025** (95% CI half-width ≈ 0.05). This resolves receipt 06's R=0.67 at >10σ and gives ≥3σ separation from R=1.0 for any *true* attenuation ≥ 7.5%. **Chose n = 900 blocks per (M, κ) cell**, sized on the worst cell (878).

**Achieved: SE(R) = 0.013–0.027.** Target met.

*(Note — the prior estimate was n=20/arm and omega's suppression was only ~2.2σ. That is 45× less data per cell than this run.)*

---

## 3. Two methodological points that decided the answer

**(a) CRN pairing — attempted, and it bought nothing.** `vortex_kappa` consumes **no RNG** and `frozen_grid` is built before the integration loop without seeing κ, so κ=0/4/8 at the same (M, block) share an identical grid *and* an identical trajectory-noise stream. The paired difference d_i = y_i(κ) − y_i(0) is therefore a legitimate common-random-numbers estimator — same expectation, potentially far lower variance. **Measured CRN variance gain: ×0.95–1.12, i.e. none.** The vortex force decorrelates the trajectories fast enough that sharing the noise stream doesn't help. Reported for the record; no free lunch, n was paid for honestly.

**(b) The bootstrap resamples the paired-difference vectors, not raw y.** Resampling raw y independently would discard the (small) CRN correlation and **overstate** SE(R). Arms are resampled independently across M — correctly, since the RNG stream diverges the moment `frozen_grid`'s draw count changes with M, so same-seed trajectories at different M are *not* paired and must not be treated as such.

---

## 4. Results

### 4.1 Primary — equal-τ (1,1), n = 900 per cell

| cell | incr @ M400 | incr @ M2000 | **R** (95% CI) | σ from 1 |
|---|---|---|---|---|
| **k4 quad** | +1.2912e-4 (se 2.43e-6) | +1.3168e-4 (se 2.51e-6) | **0.981** [0.929, 1.034] | 0.7 |
| **k4 omega** | +1.2696e-4 (se 2.40e-6) | +1.2437e-4 (se 2.23e-6) | **1.021** [0.969, 1.074] | 0.8 |
| **k8 quad** | +2.5859e-4 (se 2.49e-6) | +2.6450e-4 (se 2.58e-6) | **0.978** [0.952, 1.004] | 1.7 |
| **k8 omega** | +2.5282e-4 (se 2.36e-6) | +2.5381e-4 (se 2.27e-6) | **0.996** [0.971, 1.021] | 0.3 |

**All four consistent with R = 1.0 (no attenuation).** Omega — the statistic receipt 06 flagged at R=0.67 — comes in at **1.021** and **0.996**.

### 4.2 Convergence — is M=2000 itself converged? (k8, n=300)

M=2000 is not *a priori* ground truth. **If the response were still rising with M, then R = resp400/resp2000 would OVERSTATE fidelity** — the dangerous direction for precisely this failure mode. So it was tested rather than assumed:

| comparison | quad R (95% CI) | omega R (95% CI) |
|---|---|---|
| M2000 → M5000 | 1.011 [0.973, 1.051] | 0.977 [0.944, 1.012] |
| M2000 → M8000 | 1.013 [0.976, 1.052] | 0.985 [0.952, 1.021] |

**The response is flat from M=2000 to M=8000. M=2000 is effectively converged**, so the caveat is *closed empirically*, not merely flagged. The honest attenuation measured against the **finest grid**:

| **M=400 vs M=8000** (20× range) | quad **0.990** [0.955, 1.028] | omega **0.981** [0.948, 1.016] |
|---|---|---|

### 4.3 Transfer — does this hold in the geometry the scout actually runs? (k8, n=400)

The equal-τ chamber is not where the scout looks. It looks at the **registered mismatch pairs**. Asserting that equal-τ attenuation transfers to the aniso cells would be an unverified transfer — so it was measured:

| aniso arm | quad R (95% CI) | omega R (95% CI) |
|---|---|---|
| **arm1** (τx=0.25, τy=1.0) | 0.996 [0.954, 1.040] | **0.955 [0.920, 0.992]** ← CI excludes 1 |
| **arm2** (τx=1.0, τy=0.25) | 0.974 [0.935, 1.015] | 0.987 [0.947, 1.029] |

**One cell — arm1 omega — shows a small but statistically real attenuation: 4.5% (2.3σ, CI excludes 1.0).** This is reported honestly rather than rounded away. It is the *only* cell of 14 whose CI excludes unity. Its magnitude (4.5%, bounded at 8.0% worst-case) is an order of magnitude below the feared 33%.

---

## 5. The decision — mapping R onto the floor

R is the *input* to the decision, not the decision. The question is: **after a ×R haircut, does a true engine current still clear the floor?**

Using the harness's own floor formula (line 670; decision-rule v3.5 §2):

```
floor(B, sd) = (z_0.995 + z_0.90) · sd · √(2/B) = 3.858 · sd · √(2/B)
```

DIAG 1 established that **sd is ~M-independent**, so the **floor is ~M-independent**. Therefore *all* the M-dependence of detectability flows through the signal attenuation R:

```
minimum detectable TRUE (fine-grid) current at M:   D_min(M) = floor / R(M)
```

M=400 thus inflates the minimum detectable true current by **1/R**. That inflation — not R — is the safety number.

Measured null-arm block sd at M=400: quad **5.469e-5**, omega **5.215e-5** → floor(B=96) = quad **3.046e-5**, omega **2.904e-5**.

> **Label these correctly.** That sd (and hence that floor) is computed from **this diagnostic's equal-τ κ=0 arm**, not from the scout's registered aniso cells. **3.046e-5 is NOT the scout's registered aniso floor** — do not cite it as such. It is harmless here because **the floor cancels in the inflation ratio**: `D_min(M)/D_min(fine) = 1/R`, which is floor-independent. That cancellation is the whole strength of §5 — the safety verdict does not depend on getting the floor exactly right.

| | best estimate | 95% worst case |
|---|---|---|
| **Inflation 1/R, worst of 14 cells** (arm1 omega) | 1.047 | **1.087** |
| k8 quad (tightest) | 1.023 | 1.050 |
| **Feared value from receipt 06** (1/0.67) | — | **1.49** |

**A ≤9% inflation of the minimum detectable true current cannot plausibly convert a real super-floor engine current into a sub-floor null.** The feared 49% inflation could have, and *would* have been a genuine false-null hazard. It is not there.

---

## 6. Verdict

> ### M = 400 IS SAFE FOR THE SCOUT, on the external-force channel. Do not raise the registered M for signal fidelity.

- The floor is trajectory-limited (DIAG 1) — **M does not help the floor.** *Closed.*
- The realized response to an injected vortex is **not meaningfully attenuated at M=400** (DIAG 3, this report) — **M does not help the external-force signal either.** *Closed.*
- The **grid-generated** signal channel is **reduced but NOT directly bounded** (§7) — the aniso-transfer arms put the probe inside the real mismatch geometry and attenuation stayed ≤4.5%, but the signal was still injected, not grid-born. *Open, and not closable with a bounded-null engine.*
- Raising M would cost 5–20× compute for a ≤9%-worst-case, ~2%-best-estimate change in the minimum detectable true current — **on the one channel that was measurable.** There is no measured basis for raising M, and the burden now sits with anyone who wants to.

**This CONFIRMS decision-rule v3.5's D3 row** (`M_grid = 400` for the geometric cells) — and confirms it for a *stronger* reason than the rule currently states. D3's stated rationale is: *"M does not lower the floor (DIAG 1); the M concern is grid-generated-signal fidelity, addressed by blocks/seed-averaging."* That rationale treats signal fidelity as a live concern to be *mitigated*. This measurement says the concern is **~absent for the external-force channel** (≤9% worst case). D3's *choice* stands; its *justification* can be strengthened, and receipt 06's superseded DIAG-3 numbers should stop being cited as the motivation to raise M.

---

## 7. Residual risk — read this before treating the question as fully closed

**The transfer caveat is real and is NOT closed by this run.** The vortex κ is an **external force added on top of** the cached grid force. Grid roughness attenuates it only *indirectly* — by scattering the trajectory and diluting the coherent circulation. The scout's engine current, by contrast, is **generated by the grid itself** (a difference of two independently-estimated, noisy S_c grids at different horizons). Grid noise could in principle wash out that systematic component **more directly** than it dilutes an external force.

So: **DIAG 3 bounds the dilution channel. It does not bound a possible additional washout of the grid-generated signal.** The κ result is a *proxy*, and it is the best available one — because the aniso engine is a **bounded null** (v4.3), there is no known aniso signal whose attenuation could be measured directly. You cannot measure the attenuation of a signal that is zero. This is exactly why the calibrated vortex is the right instrument, and exactly why it cannot fully settle the question.

Two things narrow the gap and are worth weighing:
1. The aniso-transfer arms (§4.3) put the vortex **inside the mismatch geometry** — the same two-grid anisotropic force path the engine uses — and attenuation stayed ≤ 4.5%. The grid-roughness environment the signal must survive is therefore the *real* one, even if the signal itself is injected.
2. The one cell that did show real attenuation (arm1 omega, 4.5%) is in that mismatch geometry — consistent with a *small* extra grid-coupling effect there, bounded at 8%.

**Second named assumption — aniso grid-convergence.** Convergence (§4.2) was verified **only at equal-τ**: the aniso arms stop at M=2000, and arm1-omega — the one real effect — sits exactly there. So §4.3 assumes *grid-convergence transfers to the aniso geometry*. **This does not move the verdict**, and the arithmetic is worth stating rather than waving at: equal-τ's M2000→M8000 omega drift is ~1.5%, so even if arm1 drifts identically, arm1-omega against a fine grid is ≈ 0.955 × 0.985 ≈ **0.94**, inflation ≈ **1.06** — still far from any danger threshold. Flagged as an assumption, not a gap that changes the call.

**Multiple comparisons, stated plainly.** arm1-omega is the **sole significant cell of 14**. It would be defensible to discount it as a look-elsewhere artifact. This report does **not** do that: it treats the effect as possibly-real and uses its *lower* CI bound as the worst case throughout. That is the conservative direction, and for a false-null hazard the conservative direction is the correct one.

**Recommendation:** treat M=400 as safe and proceed. If HQ wants this residual fully retired, the instrument would be a **grid-generated** positive control — e.g. an injected *anisotropy* (a τ-mismatch large enough to produce a known super-floor current) rather than an injected force — measured at M=400 vs M=2000. That is a separate diagnostic and a larger build; it is **not** required to unblock the current decision, and this report does not gate on it.

**Also note (secondary, for the v4.4 promotion decision):** omega's realized increments track quad's closely (2.53e-4 vs 2.59e-4 at k8, equal-τ) with slightly *lower* block sd (5.215e-5 vs 5.469e-5) and hence a slightly *lower* floor (2.904e-5 vs 3.046e-5). Omega is not the fragile statistic receipt 06 made it look like. That is a mild point in favour of promoting it — but it is a promotion argument, not part of this verdict, and belongs to the v4.4 design pass.

---

## 8. Provenance

| | |
|---|---|
| Raw record (law #7) | `diag3_raw.ndjson` — 9,800 rows |
| Analysis | `diag3_analysis.json` |
| Namespace | `diag10::` — 100% of rows; quarantined; **never pooled** |
| `config_hash` | `a344d6c47c8a22c1` — identical on all 9,800 rows, identical to `prereg_v44.json` |
| `source_sha` | `0b65a9ee92b9fe2c` — pristine unedited harness, verified before and after |
| CFG edited? | **No.** M via `M_grid_ov` override only. |
| Frozen artifacts touched? | **None.** `v4/v43/` untouched. Receipt 06 **not edited** — superseded alongside (law #9). |
| Interpreter | `/usr/bin/python3`, Python 3.9.6, numpy 2.0.2 |
| Bootstrap | 8,000 resamples, fixed `rng=999`, on paired-difference vectors |
| Registers / authorizes | **Nothing.** Registration is Anthony's gate (law #1). |
