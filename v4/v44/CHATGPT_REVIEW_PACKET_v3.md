# v4.4 Movement 2 Scout — Methodology Review Packet R2: decision-rule v3 (paste into ChatGPT)

**Your role:** independent METHODOLOGY review of the **frozen decision-rule spec v3** for the v4.4 scout, before HQ registers anything. Same contract as the last packet: you cannot fetch the repo, so everything you need is inlined below **byte-faithful** (Appendix A is the full v3 document, not a summary). The mechanical/bytes lane — manifest `shasum -c`, harness selftest, `--plan` hash recompute, Monte-Carlo re-derivation — has already run twice on a repo-accessible seat; those receipts are inlined too (Appendices B, C). Your job is the science and the statistics, not the bytes.

**Return:** per-question **PASS / BLOCK / AMEND-BEFORE-REGISTRATION**, a stated **lean on each open call** in Q6, and a one-line overall verdict — so HQ can diff your pass against the other reviewer's two rounds.

---

## 0. What changed since the packet you were sent earlier today (5:26 PM ET)

The decision rule in that packet ("any cell clearing 3× its own B=64 floor at 8 blocks → registration candidate, else pivot") is **dead**. After the packet went out it was found self-defeating at the operative config: the register branch was effectively unreachable for plausible true effects at the pilot's power, i.e. the rule pre-committed the pilot to a null — the same class of defect that invalidated v4.1's occupancy gate, relocated into the trigger. The sweep/design itself is unchanged (6 mismatch cells over Δτ × T_c, frozen anisotropic-horizon chamber, quarantined `v44pilot::` seeds never pooled, sizing the SIGNAL not the noise).

Since then, in order:

1. **v2 draft** named the defect and mapped the recalibration space (kept as trail; not your target).
2. **v3 froze the recalibrated rule** (Appendix A, your review target): pinned estimand (contrast-proxy, option a), a complete four-band partition (GREEN / AMBER / RED / ANOMALOUS), a direction-corrected always-conservative RED rule (§3.3), a finite AMBER terminal loop with B_conf escalation (§4), and a pivot gated on two registered preconditions plus a no-open-anomaly clause (§1, §5).
3. **Antigravity adversarial audit, round 1** (repo-accessible lab seat, Gemini 3.5 Flash — Appendix B): 6 findings — 1 blocker (banding gap deadlock: a true null could freeze unbanded, unable to register, extend, or pivot), 3 major (grid-curl sign instability at M=400; T_c noise-scaling miss in floor/SE; ANOMALOUS threshold keyed on the floor let a significant wrong-sign current launder into RED), 2 minor. All six reconciled into v3 — §10 of Appendix A has the per-finding disposition table; Findings 1+4 changed the band inequalities, the rest were already covered by the v3 build or scoped into the §8 re-issue.
4. **Round 2 re-audit of v3** (Appendix C): all 6 findings **CONFIRMED CLOSED**; the §3.3 Monte Carlo independently re-derived (3.951% / 18.860% vs HQ's 3.9% / 18.9%); a 100k-run true-null sweep simulation found no deadlock; verdict **RATIFIABLE AS-IS**, plus leans on every open item.
5. **Nothing is registered or chronicled yet** (standing law #1). The frozen v4.3 artifacts and `v44_scout.py` are byte-untouched (manifest verified in both audit rounds); v3 is additive documentation on branch `v4.4-scout-draft` (commits `138d109`, `15a5d52`). Registration happens only after your pass and Anthony's ratification of the open calls, via the config_hash + prereg re-issue scoped in §8.

---

## 1. The methodology questions HQ wants weighed (answer each: PASS / BLOCK / AMEND)

**Q1 — Pinned estimand (§2.1, option a "contrast-proxy").** Each cell's banding statistic is the mismatch-arm mean against the registered equal-arm reference, with SE and floor_c computed from the cell's **own** block sd (`sd_cell`, closing round-1 Finding 3). Is this the right estimand for a signal-*sizing* scout? Weigh the licensing assumption (equal-arm current ≈ 0, verified only at T_c=1) and the reviewer lean already on record (refuse the assumption for T_c>1 cells: any high-T_c GREEN requires two-sample contrast validation at confirmatory).

**Q2 — The four-band partition (§3, §7 `band_cell()`).** ANOMALOUS is keyed on significance against **0** (`x < −t·SE`), not against the floor, and any open ANOMALOUS **blocks** a terminal-null pivot (§5 clause 0). Cost on a true null: ≈2.5% per cell (Appendix C's derivation; HQ has **not** independently re-derived that one number — the doc's conservative nominal is 5%), so ≈14% chance across 6 cells that a null sweep stalls pending investigation instead of pivoting cleanly. Reviewer lean on record: keep significance-against-0, no magnitude margin. Is that the right key, and is stall-don't-pivot the right failure direction?

**Q3 — §3.3 RED-direction conjunction rule.** RED fires only if the sign-aligned upper confidence bound is below floor_c under BOTH the point sd̂ AND the coupled upper-CI sd_upper. Rationale: the naive "use upper-sd for RED" reading flips from conservative to anti-conservative when κ = floor_c − t·SE changes sign — at the operative 16-block/B96 config κ = +0.067·sd, and a floor-only upper-sd read inflates the at-floor false-null rate 3.9% → 18.9% (≈5×). Monte-Carlo receipts: HQ 3.9% / 18.9%; independent re-derivation 3.951% / 18.860% / 4.933% (coupled-upper alone) / 3.951% (conjunction). MC spec, verbatim from §3.3: 4×10⁶ draws, true contrast Δ = floor(96) = 0.557·σ, μ̂ ~ N(Δ, σ·√(1/16+1/64)), sd̂ ~ σ·√(χ²₁₅/15), sd_upper = 1.437·sd̂. Two asks: is the conjunction the right *general* fix (conservative at every config, not just this one), and any objection to the MC design itself?

**Q4 — Sequential-testing integrity (§4, §5).** The loop: AMBER → extend blocks → escalate B_conf 96→128 (floor drops ∝ 1/√B) → hard ceiling; the pivot additionally requires extension, P1 sign-stability, and no open anomaly. Is this an optional-stopping false-register leak, or acceptably bounded given the loop is finite and every threshold is frozen at re-issue? Name explicitly what the re-issue selftest **must simulate** before the run is licensed (standing law #2/#3: gates must demonstrably fail on null AND pass on signal, compound across the whole loop, not per-contrast — the per-contrast-power lie is exactly how v4.3's positive control went wrong).

**Q5 — Preconditions as registration gates (§1).** P1 registers per-cell predicted signs σ_cell and a stability flag from the seed-averaged mean-field curl (non-unanimous → the cell bands two-sided; UNSTABLE → the cell cannot license an all-RED pivot from an M=400 null). The §1.1 OPEN ITEM: two operationally distinct recipes — average-seeds-then-take-curl vs per-seed-curls-then-unanimity — can disagree (receipt 07: an 8-seed per-seed check split +4/−4 where the 3-seed set had been called unanimous). Reviewer lean on record: mean-field-then-curl registers σ_cell; per-seed sign agreement ≥75% declares STABLE. P2 is a crossed T_c×M diagnostic attributing SD-vs-T_c growth (grid-noise vs dynamical) that gates the T_c cells' M_grid. Are these the right gates, and which P1 operational pin should register?

**Q6 — The open calls (Anthony ratifies; give one lean each).**
(i) Equal-arm reference: τy-matched vs (τx,τx) vs dual (other reviewer: τy-matched).
(ii) B_max ceiling = 128 (other reviewer: keep).
(iii) Estimand-(a) licensing for T_c>1 cells (other reviewer: refuse; require two-sample at confirmatory).
(iv) First-pass blocks 8 vs 16 (other reviewer: adopt 16 — makes κ>0 on the first pass so true nulls can resolve RED without entering the extension loop).
(v) The P1 pin from Q5.

**Q7 — BLOCK-scan.** Anything else that must change before HQ re-issues config_hash + prereg (§8 scope) and registers, and Grok Build executes under contract? Anything missing from the §8 re-issue scope itself?

---

## 2. Reading order

Appendix A (full v3 spec) is the review target; its §10 cross-references Appendix B. Appendix C is the round-2 close-out with the re-derivations. The open items for your Q6 leans live in Appendix A §0.2, §1.1 (OPEN ITEM), and §9.

---

# APPENDIX A — `v44_scout_DECISION_RULE_v3.md` (the review target; byte-faithful, commit 138d109)

# v4.4 Scout — Decision Rule v3 (ratifiable pre-registration spec)

*HQ (Mac Studio Claude Code seat, overwatch/provenance), 2026-07-07. This document **is the rule**, written to survive an adversarial pre-registration audit (Antigravity), not to narrate the v2 defect. It resolves every open item in `v44_scout_DECISION_RULE_v2_DRAFT.md` §7 into a frozen spec: the estimand, the exact banding inequalities, the precondition runs that gate the scout, and the `band_cell()` pseudocode. It supersedes the decision-rule section of `SCOUT_DECLARATION.md` **only when ratified** (Anthony final say + ChatGPT methodology + Antigravity pre-reg audit). No harness bytes are edited by this document; the frozen v4.3 artifacts and `v44_scout.py` physics path stay hash-frozen. Nothing here is registered or chronicled yet.*

*All decisions in §0 are **ratified-pending-Antigravity** (Anthony, working) and therefore **revisable** at audit. Where v3 deviates from a v2 one-liner, the deviation is flagged inline for the reviewers, not applied silently.*

---

## 0. Identity + adopted decisions

### 0.1 Instrument identity (verify before any run — unchanged from `SCOUT_DECLARATION.md`)

| Anchor | Value |
|---|---|
| `version` | `v4h-1.4.0` |
| `config_hash` | `a344d6c47c8a22c1` (recomputed if any CFG block changes — see §8) |
| `source_sha` | `0b65a9ee92b9fe2c` |
| `prereg_v44.json` sha256 | `b7c5aeb6bd21b70036f7fb6841f199fbf923aa984cba3d30a71943c75e9a2a2b` (re-issued if CFG changes — §8) |
| interpreter | `/usr/bin/python3` (Python 3.9.6, numpy 2.0.2 pinned) |

Detection floor, verified against `_detection_floor` (line 670) — a **two-arm** minimum-detectable-effect:

```
floor(B, sd) = (z_{1-α_worst} + z_{power_target}) · sd · √(2/B)
             = (z_{0.995} + z_{0.90}) · sd · √(2/B)
             = 3.858 · sd · √(2/B)                    [CFG["power"]: alpha_worst=0.005, power_target=0.90, verified]
```

| B | floor(B) = 3.858·sd·√(2/B) |
|---|---|
| 64  | 0.682·sd |
| 96  | **0.557·sd**  (adopted B_conf default) |
| 128 | 0.482·sd  (escalation ceiling B_max) |

### 0.2 Adopted decisions (build on these; all revisable at Antigravity)

| # | Decision | Value | Rationale / coupling |
|---|---|---|---|
| D1 | **Primary statistic** | `quad_loop_rate` | Continuity with the v4.3 **G1 vortex-control calibration** (the powered positive control is calibrated on quad). Rests on that continuity, **not** on the 2.2σ κ-suppression point estimate (§1.3). |
| D1′ | **Secondary statistic** | `omega_roi` (pre-registered, **descriptive only**) | Carried per Opus arbiter's ~19%-lower-floor note; banded for information, **does not gate the pivot**. `occupancy_x` also recorded (T_c rescales U_eff) but not banded. |
| D2 | **First-pass blocks** | **16** per cell | At 8 blocks RED is unreachable (κ<0, §3.3); 16 gives a usable first surface. Couples to the thresholds table (§2.2). |
| D3 | **M_grid** | **400** for geometric cells A/B/C/D, **GATED** on the sign-stability precondition (§1.1). T_c cells AxT2/AxT4 **KEPT at M=400** pending the crossed T_c×M diagnostic (§1.2). | M does **not** lower the floor (DIAG 1, trajectory-limited); the real M concern is grid-generated-signal fidelity, addressed by blocks/seed-averaging, not M-per-block. |
| D4 | **B_conf (floor projection)** | **96** working default | floor(96) = 3.858·sd·√(2/96) = **0.557·sd**. Escalation 96→128 for persistent AMBER (§4). |
| D5 | **Estimand** | **Option (a)** — raw mismatch current as contrast-proxy | μ̂ vs two-arm floor(B_conf); honest SE = sd·√(1/B_scout + 1/64); equal-arm treated as an **estimate** (v4.3 μ_eq ≈ 3e-6), assumption stated (§2.1). |

### 0.3 Three couplings that must not drift apart

1. **sign precondition ↔ per-cell predicted signs ↔ pivot license** — one chain (§1.1, §6.2, §5).
2. **estimand ↔ B_conf ↔ AMBER escalation ceiling** — share `floor_c` (§2, §4, §6.1).
3. **M_grid ↔ primary statistic** — one decision: quad@M400 (D1+D3; §1.3).

---

## 1. Precondition runs (gate the scout — must complete and register BEFORE the scout runs)

These are **diagnostics, not scout results**. They run the mean-field / equal-τ rig, in a throwaway quarantined seed namespace (`diag10::` / a declared precondition namespace), **NEVER** pooled into `v44pilot::` or any confirmatory. Their outputs are registered (per-cell signs, sign-stability flags, T_c×M attribution) as part of the frozen prereg, because the scout's banding and pivot license depend on them.

### 1.1 Precondition P1 — per-cell predicted signs + sign-stability (the load-bearing one)

**Recipe (v4.3):** for each of the six cells, compute the ROI-integrated curl of the **seed-averaged mean aniso force field** at **M=4000** (many seeds averaged into the mean field, then the ROI mixed-partial taken — *not* per-single-grid; receipt 07 showed a single grid's curl is noise-dominated at both M=400 and M=4000). v4.3 used seeds 77001/77002/77003 and required **sign unanimity**.

**Two registered outputs per cell:**

- **Predicted sign σ_cell ∈ {+, −, NON-UNANIMOUS}.** If the seed set is sign-unanimous → register σ_cell and the cell bands **one-sided** in that direction (§3). If not unanimous → the cell bands **two-sided** (§3, §2.2). This retires the forking path (v2 §7 item 1): no cell may band one-sided without a pre-registered σ_cell.
- **Sign-stability flag stable_cell ∈ {STABLE, UNSTABLE}.** A cell is STABLE iff the seed-averaged mean-field curl is sign-unanimous across the registered seed set at M=400 (i.e. M=400 does not corrupt the *sign* of the grid-generated signal for that cell). UNSTABLE cells **cannot license an all-RED pivot from an M=400 null** (§5) and must run at higher M or with seed-averaged grids per block before a RED there counts.

**Note (receipt 07):** the quick per-seed check is *informative but not the instrument* — it found cell A(0.1,2.0) and cell C(0.1,1.0) both leaned `+` at M=4000 (means +0.45, +0.23) but per-seed sign split evenly (SNR 0.2–0.5). The seed-averaged mean-field recipe above is what establishes the registered sign; the per-seed check does **not** substitute for it and does **not** retire the precondition.

> **OPEN ITEM to pin at audit (flagged, not settled).** The recipe above conflates two operationally distinct procedures that can **disagree**: (a) **average N seeds into one mean field, then take its curl** (yields a *single* sign — nothing to be unanimous over), vs (b) **take per-seed curls across N seeds, then require sign unanimity** (the "77001/77002/77003 unanimous" phrasing). Receipt 07 showed these can split: its 8-seed per-seed M=4000 check came out +4/−4 where CFG's 3-seed set was called unanimous. Because `stable_cell` gates the pivot (§5(ii)), P1 must pin **one** operational definition before registration: (N seeds, M per seed, averaging-then-curl **or** per-seed-then-unanimity, and the exact STABLE threshold). HQ leans (a) for σ_cell (the registered directional prediction is a mean-field object) with (b) as the STABLE *robustness* check (per-seed sign agreement ≥ a declared fraction) — but this is a reviewer call, inherited-ambiguous from task item 1, and must not read as decided.

### 1.2 Precondition P2 — crossed T_c×M diagnostic (gates the T_c cells' M_grid)

**Recipe:** 4 cells, `{T_c ∈ 1,4} × {M ∈ 400, 4000}`, equal-τ, same rig as receipt 06 (DIAG 2), n≈20/arm, block-SD with bootstrap CIs. **Purpose:** attribute the measured SD-vs-T_c growth (DIAG 2: quad ×1.62, omega ×2.00 at T_c=4, CIs excluding 1) as **grid-noise** (SD growth shrinks with M → raise M for T_c cells) **vs dynamical** (SD growth M-invariant → a 4× stronger drift reshapes the trajectory/ROI ensemble even on a perfect grid → M=400 is fine).

**Gate:** until P2 runs, AxT2/AxT4 are **kept at M=400** and interpreted with the caveat that a T_c-cell win is a **drive-amplitude** claim, not geometric (§6.1). If P2 shows the SD growth is grid-noise **and** higher M is infeasible, the T_c cells demote to descriptive; otherwise they stay as the highest-sensitivity probes (mean force linear in T_c → signal ~4× at T_c=4 vs SD growth 1.6–2× → net mean/floor up ~2–2.5×).

### 1.3 Diagnostic language (frozen at n=20 reality — v2 §7 item 7)

Any prose accompanying the scout must state the diagnostics at their measured strength, not rounded up:

- **Floor is trajectory-limited even at scale 10** (DIAG 1: SD@400/SD@2000 = 1.19 [0.80,1.74] quad, 0.87 [0.61,1.25] omega — consistent with 1). Raising M does **not** lower the floor.
- **κ-injection suppression is NOT established:** quad ratio 0.90 (~0.5σ, consistent with zero suppression); omega ratio 0.67 (**~33% nominal but weak — ~2.2σ at n=20, uncorrected p≈0.03, does NOT survive Holm** across the ~8 diagnostic contrasts). **The quad-primary choice (D1) rests on v4.3 G1-calibration continuity, with suppression as supporting color only — never on the 2.2σ point estimate.**
- **Net relative sensitivity at M=400:** quad ≈ 0.90, omega ≈ 0.83 → **quad wins at M=400** (couples D1↔D3).

---

## 2. Estimand + exact thresholds

### 2.1 Pinned estimand — option (a), contrast-proxy

μ̂ (per cell, per statistic) = the mean of the **raw mismatch current** over the scout blocks. It is a **proxy for the confirmatory contrast** Δ = μ_mis − μ_eq, valid under **equal-arm current ≈ 0** (v4.3 measured μ_eq ≈ 3e-6 = 8.2% of floor). The equal arm is treated as an **estimate** (v4.3's B=64 equal arm), not a zero-variance constant, so the honest SE folds in its 64-block reference:

```
SE(B_scout) = sd_cell · √(1/B_scout + 1/64)
```

**Two distinct roles of "the equal arm" — do not conflate (auditor trip-wire):**

1. **floor_c's SD source.** The scout runs **no equal arm** (all six cells are mismatch), so `floor_c` **cannot** use `sd_eq` the way `analyze()` line 749 does. `floor_c` is projected from **the cell's own measured block SD** (`sd_cell`, n=B_scout) used as the **homoscedastic proxy** for the confirmatory's equal-arm SD. This is the assumption behind the entire §6.1 "T_c cells inflate their own floor" discussion — stated explicitly here.
2. **The named equal-arm config (§6.2)** defines the **contrast estimand** and the **confirmatory's second arm** at Movement 3. It is *not* used in the scout's floor arithmetic. Two different jobs for the phrase "equal arm."

**Licensing assumption (stated, revisable):** equal-arm current ≈ 0 is v4.3-grounded but **verified only at (1.0,1.0), T_c=1**. If any protocol offset is force-mediated it scales with T_c, so this must be re-stated (or re-measured) for the T_c cells. If reviewers decline the assumption, fall back to estimand (c) — a per-cell measured equal arm, two-arm SE = sd·√(2/B) — which raises the GREEN bar (~2.39× floor at 8b/B64 legacy).

### 2.2 Frozen convention (law #4 grep-consistency)

**Convention frozen as *form*, so it survives block-count changes:** one-sided **Student-t at (n−1) df, α=0.05** for GREEN/RED in the predicted direction; two-sided Student-t at (n−1) df, α=0.05 for non-unanimous-sign cells. The per-config t-values coexist without contradiction:

| df (n−1) | one-sided t (0.95) | two-sided t (0.975) |
|---|---|---|
| 7  (8 blocks)  | 1.895 | 2.365 |
| 15 (16 blocks) | **1.753** | **2.131** |
| 31 (32 blocks) | 1.696 | 2.040 |

*The task brief's "t₇ ⇒ 2.04×/2.30× floor" figures are **v2 8-block/B_conf=64 legacy** and are superseded by the operative 16-block/B_conf=96 numbers below. Both appear in the table so any grep resolves consistently; the operative row is marked.*

### 2.3 Exact thresholds table

`floor_c` and `SE` are both in units of the cell's own block SD, `sd_cell`. GREEN threshold on μ̂ = `floor_c + t·SE`. RED ceiling on μ̂ = `floor_c − t·SE` (point-governed where κ = floor_c − t·SE > 0; see §3.3 for the robust-both-sd form).

| Config (blocks / B_conf) | floor_c | SE = sd·√(1/B+1/64) | **GREEN μ̂ >** (1-sided) | **GREEN μ̂ >** (2-sided) | RED μ̂ < (point) |
|---|---|---|---|---|---|
| **16 / 96  (OPERATIVE first pass)** | 0.557·sd | 0.2795·sd | **1.047·sd = 1.88× floor** | **1.153·sd = 2.07× floor** | **0.067·sd** |
| 8 / 96   (legacy-block, if 16 not adopted) | 0.557·sd | 0.3750·sd | 1.267·sd = 2.28× floor | 1.444·sd = 2.59× floor | unreachable (κ<0) |
| 32 / 96  (AMBER block-extension) | 0.557·sd | 0.2165·sd | 0.924·sd = 1.66× floor | 0.998·sd = 1.79× floor | 0.190·sd |
| 32 / 128 (AMBER B_conf escalation, ceiling) | 0.482·sd | 0.2165·sd | 0.849·sd = 1.76× floor | 0.924·sd = 1.92× floor | 0.115·sd |
| *8 / 64 (v2 legacy reference only)* | *0.682·sd* | *0.375·sd* | *1.393·sd = 2.04× floor* | *1.569·sd = 2.30× floor* | *unreachable (κ<0)* |

**Operative frozen GREEN for the primary (`quad_loop_rate`, 16 blocks, B_conf=96, one-sided in the registered predicted direction): μ̂ > 1.047·sd_cell (= 1.88× floor(96)).**

---

## 3. The four-band rule (exact inequalities)

Banded on the **primary statistic** (`quad_loop_rate`) only; `omega_roi` gets the same arithmetic **descriptively** (does not gate the pivot). Let `t = t*(n−1 df)` per §2.2, `SE` per §2.1, `floor_c` per §2.3, and σ_cell the registered predicted sign (P1).

**One-sided cells (σ_cell unanimous).** Work in signed units aligned to the prediction: let `x = σ_cell · μ̂` (so `x > 0` means the current runs in the predicted direction).

- **GREEN** — register a confirmatory here:
  `x − t·SE > floor_c`.
- **RED** — bounded sub-floor (see §3.3 for the robust form):
  `x + t·SE < floor_c` **AND** the effect is **not** a large wrong-sign excursion.
- **ANOMALOUS** — a **significant** wrong-sign current, does **not** count toward the pivot; triggers investigation:
  `x < −t·SE`  (the sign-aligned estimate is significantly negative at one-sided α=0.05 — i.e. significant *against 0*, not against the floor).
- **AMBER** — promising but not separated; extend (§4):
  none of the above (the CI straddles `floor_c`, or a small wrong-sign current consistent with sub-floor).

> **Finding-4 correction (Antigravity, applied 2026-07-07).** v3 originally keyed ANOMALOUS on `|μ̂| − t·SE > floor_c` (clear the floor *magnitude*). Antigravity's audit showed that laundered a significant wrong-sign artifact into RED: at 16b/B96 a `μ̂ = −1.0·sd` current (a 3.6σ wrong-sign excursion) gives `1.0 − 0.490 = 0.510 < 0.557 = floor_c`, misses the old ANOMALOUS, and bands RED — where it would count toward the all-RED pivot, licensing the very null it contradicts. Keying ANOMALOUS on significance against **0** (`x < −t·SE`) catches it. The partition stays complete: ANOMALOUS `(−∞, −t·SE)`, RED `[−t·SE, floor_c−t·SE)`, AMBER `[floor_c−t·SE, floor_c+t·SE]`, GREEN `(floor_c+t·SE, ∞)`. **Tradeoff flagged for reviewers:** on a true null, ~5% of cells per statistic trip a false ANOMALOUS (≈26% chance across 6 cells), which *blocks* the pivot pending investigation rather than producing a wrong verdict — the conservative (don't-pivot-on-an-artifact) direction. If that investigation overhead is too high, tighten to `x < −t·SE − c·floor_c` (a magnitude margin) at audit; HQ leans to keep Antigravity's form.

**Two-sided cells (σ_cell NON-UNANIMOUS from P1).** Use the two-sided `t`; ANOMALOUS does not apply (no predicted direction to violate):

- **GREEN**: `|μ̂| − t·SE > floor_c`.
- **RED**: `|μ̂| + t·SE < floor_c` (robust form §3.3).
- **AMBER**: otherwise.

### 3.1 GREEN meaning
The scouting-grade lower confidence bound on the (sign-aligned) current clears the confirmatory's minimum detectable effect: we are ≥95%-one-sided confident the true effect is at least what a B_conf-block confirmatory is designed to catch. Register Movement 3 at this cell.

### 3.2 ANOMALOUS meaning
A large current in the **wrong** direction is not a win — it is a grid artifact / transduction-breakdown signal. It is carved out of RED so it **cannot launder into the null bucket** and cannot license the pivot (§5). Triggers investigation (grid artifact vs dynamical), not registration.

### 3.3 RED robustness — deviation from v2 §5 (flagged for Antigravity)

**v2 §5 said "use the *upper* end of the sd CI" for RED.** v3 pins this precisely and **corrects its direction at the operative config**, because the literal reading re-introduces the exact pathology v2 exists to kill (a rule that manufactures nulls), just relocated from the trigger to the RED band:

- v2's mental model was **coupled** (a single `sd`, whose CI moves `floor_c` and `SE` together). Under that model, upper-sd makes RED *harder* **only while** κ = `floor_c − t·SE` **≤ 0** — true at 8 blocks (κ<0, RED already unreachable), which is the regime v2 reasoned in.
- At the adopted **16-block / B_conf=96** config, **κ = +0.067·sd > 0**, so the sign flips: a **floor-only** upper-sd reading (inflate `floor_c`, keep point `SE`) makes RED **easier**, driving the false-null (wrongly-abandon-a-real-effect) rate for an at-floor effect from **3.9% (point-sd)** to **18.9% (floor-only upper-sd)** — ~5× worse. That is anti-conservative and unacceptable in the provenance lane. *(Rates from a Monte Carlo at the operative config: 4×10⁶ draws, true contrast Δ = floor(96) = 0.557·σ, μ̂ ~ N(Δ, σ·√(1/16+1/64)), sd̂ ~ σ·√(χ²₁₅/15), `sd_upper` = 1.437·sd̂ random. HQ, `/usr/bin/python3` numpy 2.0.2, 2026-07-07. Reviewers should re-derive.)*

**Frozen RED rule (always conservative at every config):** RED fires **iff the sign-aligned upper confidence bound is below `floor_c` under BOTH the point sd̂ AND the coupled upper-CI sd_upper** (upper-CI applied to the whole `floor_c`+`SE`, since they share one sd):

```
RED  ⇔  ( x + t·SE(sd̂)      < floor_c(sd̂)      )   AND
        ( x + t·SE(sd_upper) < floor_c(sd_upper) )
```

The conjunction always selects the harder ceiling, so RED is conservative whether κ<0 (upper-sd binds, RED unreachable at 8b) or κ>0 (point-sd binds, e.g. `x < 0.067·sd` at 16b/B96). At 16b/B96 the "both" rule holds the false-null at the point-sd rate (**3.9%** in the Monte Carlo above), vs 18.9% for the literal floor-only read. `sd_upper` = upper end of the 90% two-sided CI on sd_cell (χ² on n−1 df): `sd_upper = sd̂ · √((n−1)/χ²_{0.05, n−1})`, factors **1.797 (n=8), 1.437 (n=16), 1.268 (n=32)**. (v2 §5 mitigation 1 — shrink/pool sd_cell toward the near-equal cells to stabilize `floor_c` — remains an available option; the frozen rule above is the per-cell floor.)

**Operative RED (16b/B96): `x < 0.067·sd_cell`** (point governs). At 8 blocks RED is unreachable for any non-negative aligned estimate — this is anti-false-null by design and is why D2 raises the first pass to 16 and why the pivot always requires extension (§4, §5).

---

## 4. AMBER terminal rule + B_conf escalation (makes the loop finite)

A cell may not sit in AMBER forever (no sequential-testing leak). The terminal ladder, per AMBER cell, in order:

1. **One block-extension: 16 → 32 blocks.** SE shrinks 0.2795·sd → 0.2165·sd; re-band against floor(96) with the 32-block row.
2. **Still AMBER against floor(96) at 32 blocks → escalate B_conf 96 → 128.** floor_c drops 0.557·sd → 0.482·sd, so a persistent AMBER may resolve **GREEN** against the larger confirmatory (the cell is real but needs a bigger Movement-3 run). Re-band with the 32/128 row.
3. **Still AMBER against floor(128) at 32 blocks → RED-at-ceiling.** B_max = 128 is the **declared compute ceiling**. Past the ceiling the cell is "bounded below floor(B_max)" and **counts as RED** for the pivot condition (§5).

Escalation order is fixed (blocks first, then B_conf) so the compute budget is bounded and the terminal state is well-defined. B_max = 128 is the working ceiling (revisable at ratification; couples to the Movement-3 registration compute budget, §0.2 D4).

---

## 5. The pivot rule (two preconditions)

The scout **pivots to the closed no-reset NESS protocol** (the scope boundary v4.3 declined to claim) **iff ALL THREE** hold (the anomaly guard is stated first and separately to defeat the vacuous-truth failure — "every non-ANOMALOUS cell is RED" is *vacuously true* when there are no non-anomalous cells, which would let an all-anomalous outcome license the very null it contradicts):

- **(0) No open anomaly (blocks the pivot):** **no** cell is ANOMALOUS. A large wrong-sign current is an unexplained instrument/transduction signal, not a bounded null (§3.2); it **blocks any terminal-null decision until resolved**. A cell may be re-banded out of ANOMALOUS after investigation — only then is the pivot reconsidered. (So `5 RED + 1 ANOMALOUS` does **not** license the pivot; the anomaly is an open finding.)
- **(i) Terminal-band condition:** at least one cell was banded, and **every** cell is **RED or RED-at-ceiling** (§3, §4). (Given (0), no cell is ANOMALOUS at this point, so "every cell" and "every non-anomalous cell" coincide — no vacuous set.)
- **(ii) Instrument precondition:** the per-cell **sign-stability flag `stable_cell` = STABLE** (P1, §1.1) for **every** cell whose RED is counted toward the pivot.

**Otherwise:**
- If any cell is **ANOMALOUS** → **investigate first** (grid artifact vs dynamical breakdown); no pivot and no registration decision is made while an anomaly is open (condition (0)).
- If any cell is **GREEN** → **register Movement 3 at that cell** (do not pivot). If several are GREEN, the registration cell is chosen by the pre-registered tie-break: highest `x − t·SE` margin above `floor_c` on the primary statistic; a T_c-cell GREEN is a **drive-amplitude** registration, a geometric-cell GREEN is a **Δτ** registration (§6.1) — recorded as distinct claims.
- If the best non-RED cell is **AMBER** → run the §4 terminal ladder before any pivot decision.
- If a cell is RED at M=400 but **`stable_cell` = UNSTABLE** → that RED **does not license the pivot**; the cell must run at higher M (or seed-averaged grids per block) and re-band before its RED counts. This is the one path by which a live effect could be abandoned on an instrument artifact — precondition (ii) closes it.

**In words:** a null (pivot) is only earned when **no cell showed an unexplained wrong-sign current**, the design space is *confidently* sub-floor, **and** the instrument was demonstrably reading a stable-sign signal everywhere it called RED. The scout still "cannot fail" — it finds a registrable cell, or it bounds the space with a stable instrument, or it names an anomaly to investigate.

---

## 6. Per-cell configuration tables

### 6.1 Equal-arm config per candidate cell (defines the contrast estimand + confirmatory's second arm)

**HQ recommendation: τy-matched equal arm** — the equal-τ config at the cell's **larger horizon** τy, at the **same T_c**. Rationale is the **receipt-07 noise argument**, not v4.3 precedent: the ROI mixed-partial of the small-τx grid is ≈ 0, so the curl *and its block-SD noise* are carried by the larger-horizon τy grid; the τy-matched equal arm is therefore the closest noise-match, making `floor_c` the correct forecast target. Matched-T_c is **non-optional** for the T_c cells (DIAG 2: SD grows with T_c, so an equal arm at a different T_c would misstate `floor_c`).

*Caveat for reviewers:* v4.3's equal arm (1.0,1.0) is the **shared-corner** value of the swap pair (τy of arm1 = τx of arm2 = 1.0) — τy-matched for arm1 but τx-matched for arm2. Scout cells have **no swap**, so "v4.3 did τy-matching" over-claims; the τy choice here rests on the noise argument above. **Reviewer alternatives:** (τx,τx)-matched, or a **dual-reference** design comparing against both (τx,τx) and (τy,τy). To be ratified at audit.

| Cell | (τx, τy) | T_c | Role | **Equal-arm config (τy-matched, matched-T_c)** |
|---|---|---|---|---|
| A    | (0.1, 2.0)  | 1 | widest horizon mismatch | (2.0, 2.0) @ T_c=1 |
| B    | (0.25, 2.0) | 1 | mismatch mid            | (2.0, 2.0) @ T_c=1 |
| C    | (0.1, 1.0)  | 1 | amplitude-only          | (1.0, 1.0) @ T_c=1 |
| D    | (0.25, 1.0) | 1 | replica bridge to v4.3  | (1.0, 1.0) @ T_c=1  ← **coincides with v4.3's (1.0,1.0) equal arm; genuine bridge-consistency** |
| AxT2 | (0.1, 2.0)  | 2 | T_c sweep at widest pair | (2.0, 2.0) @ T_c=2 |
| AxT4 | (0.1, 2.0)  | 4 | T_c sweep at widest pair | (2.0, 2.0) @ T_c=4 |

Reminder (§2.1): this named equal arm defines the **contrast estimand and the Movement-3 second arm**; it is **not** the scout's `floor_c` SD source (that is the cell's own `sd_cell`).

### 6.2 Predicted-sign table (all TBD until P1 registers)

Per-cell one-sided banding requires σ_cell from precondition P1 (§1.1). Until P1 runs, **no cell has a registered sign** and none may band one-sided.

| Cell | (τx, τy, T_c) | Registered predicted sign σ_cell | Banding |
|---|---|---|---|
| A    | (0.1, 2.0, 1) | **TBD by P1** (receipt-07 quick check leaned `+`, inconclusive) | one-sided if unanimous, else two-sided |
| B    | (0.25, 2.0, 1) | **TBD by P1** | one-sided if unanimous, else two-sided |
| C    | (0.1, 1.0, 1) | **TBD by P1** (receipt-07 quick check leaned `+`, inconclusive) | one-sided if unanimous, else two-sided |
| D    | (0.25, 1.0, 1) | **TBD by P1** (v4.3 arm1 orientation τx<τy ⇒ `+`, but must be re-derived per cell) | one-sided if unanimous, else two-sided |
| AxT2 | (0.1, 2.0, 2) | **TBD by P1** | one-sided if unanimous, else two-sided |
| AxT4 | (0.1, 2.0, 4) | **TBD by P1** | one-sided if unanimous, else two-sided |

A non-unanimous cell moves GREEN to the two-sided column of §2.3 (16b/B96: 1.153·sd = 2.07× floor, vs one-sided 1.047·sd = 1.88× floor).

---

## 7. `band_cell()` pseudocode

Reference implementation for the additive `band_cell()` in `analyze()` (see §8 scope). Pure analysis; touches no harness physics. All arithmetic in units of `sd_cell`.

```python
def band_cell(mu_hat, sd_cell, n_blocks, B_conf, sigma_cell, stable_cell):
    """
    Band one scout cell on the PRIMARY statistic (quad_loop_rate).
    Returns (band, aligned_lower_cb, floor_c) where band in
    {GREEN, AMBER, RED, RED_AT_CEILING, ANOMALOUS}.
    sigma_cell in {+1, -1, None}; None => two-sided (P1 non-unanimous).
    stable_cell in {True, False} (P1 sign-stability); consumed at the pivot,
    not here.  RED-at-ceiling is set by the caller's terminal ladder (sec 4),
    not by a single band_cell() call.
    """
    Z = 3.858                                   # z_{0.995} + z_{0.90}, verified
    df = n_blocks - 1
    two_sided = (sigma_cell is None)
    t = t_student(df, one_sided=not two_sided, alpha=0.05)   # sec 2.2 table

    def floor_c(sd):  return Z * sd * sqrt(2.0 / B_conf)      # sec 0.1
    def SE(sd):       return sd * sqrt(1.0/n_blocks + 1.0/64) # estimand (a), sec 2.1

    sd_up = sd_cell * chi2_upper_factor(df)     # sqrt((n-1)/chi2_{0.05,n-1}); sec 3.3

    if two_sided:
        x = abs(mu_hat)                          # magnitude; no predicted direction
    else:
        x = sigma_cell * mu_hat                  # align to predicted direction

    # GREEN: sign-aligned lower CB clears the confirmatory floor
    if x - t * SE(sd_cell) > floor_c(sd_cell):
        return ("GREEN", x - t*SE(sd_cell), floor_c(sd_cell))

    # ANOMALOUS: SIGNIFICANT wrong-sign excursion (one-sided cells only) -> not RED,
    #            does NOT count toward the pivot; triggers investigation (sec 3.2).
    #            Keyed on significance against 0 (Finding 4, Antigravity), NOT the floor.
    if (not two_sided) and (x < -t * SE(sd_cell)):
        return ("ANOMALOUS", x - t*SE(sd_cell), floor_c(sd_cell))

    # RED: sign-aligned upper CB below floor under BOTH point and coupled-upper sd
    #      (sec 3.3 -- always the harder/conservative ceiling)
    red_point = (x + t * SE(sd_cell) < floor_c(sd_cell))
    red_upper = (x + t * SE(sd_up)   < floor_c(sd_up))
    if red_point and red_upper:
        return ("RED", x + t*SE(sd_cell), floor_c(sd_cell))

    # otherwise: promising-but-unseparated, or small wrong-sign consistent w/ sub-floor
    return ("AMBER", x + t*SE(sd_cell), floor_c(sd_cell))


def pivot_licensed(cell_bands, stable_flags):
    """Sec 5: pivot to closed no-reset NESS iff BOTH conditions hold.
    Guarded against vacuous truth: an OPEN anomaly, or no cells at all,
    must NOT license a terminal null (all([]) == True is the bug this avoids)."""
    # An open ANOMALOUS cell blocks the pivot (sec 3.2: investigate, do not pivot)
    if any(b == "ANOMALOUS" for b in cell_bands.values()):
        return False                             # resolve the anomaly first
    if not cell_bands:
        return False                             # nothing to bound the space
    if any(b == "GREEN" for b in cell_bands.values()):
        return False                             # register at the GREEN cell instead
    # every (now non-anomalous) cell must be terminal-RED
    if not all(b in ("RED", "RED_AT_CEILING") for b in cell_bands.values()):
        return False                             # AMBER cells -> run sec 4 ladder first
    # instrument precondition (ii): every counted RED must be on a STABLE cell
    if not all(stable_flags[c] for c, b in cell_bands.items()
               if b in ("RED", "RED_AT_CEILING")):
        return False                             # UNSTABLE RED at M=400 does not license
    return True
```

`omega_roi` (secondary, D1′) is run through the same `band_cell()` for the record but its band is **descriptive** — excluded from `pivot_licensed`.

---

## 8. Scope of changes if ratified (→ config_hash / prereg re-issue)

| Artifact | Change | Hash impact |
|---|---|---|
| `SCOUT_DECLARATION.md` decision-rule section | Replaced by §1–§6 of this document (human-readable; not hash-frozen) | none (declaration) |
| `analyze()` in `v44_scout.py` | Add `band_cell()` + `pivot_licensed()` (§7) — additive, testable, does **not** touch the v4.3-inherited estimator or the forward physics path | new `source_sha` |
| `CFG["scout"]["blocks"]` | 8 → **16** (D2) | **new `config_hash` → re-issue `prereg_v44.json` → new sha256** |
| B_conf convention for the floor projection | 64 → **96** (D4) | if surfaced in CFG, new `config_hash`; else declaration-only |
| **Stale-prose flag (law #4):** `CFG["scout"]` comments + `pilot_pair` docstring hard-code **"B=64 floor"** | Update to B_conf = 96/128 wherever the floor is quoted; the selftest grep-check (rule 2, Antigravity finding 3) must be extended to grep the **operative** t-convention + B_conf, not the stale 24/32, 48/64, B=64 strings | part of the config_hash / prereg re-issue |

**Unchanged and hash-frozen:** the forward-path harness (`pilot_pair`, T_c threading, the v4.3-inherited estimator), the six cells + geometry, the `v44pilot::` seed namespace, and the never-pooled rule. This is an **analysis + declaration recalibration**, not a physics-instrument edit. Re-issue sequence per experimental law #1: regenerate `prereg_v44.json` from `--plan`, record the new `config_hash` + `source_sha` + prereg sha256, verify readback, **then** run — preconditions P1/P2 first, scout second.

---

## 9. Ratification checklist (maps to v2 §7 — all resolved into spec above)

| v2 §7 item | Status in v3 |
|---|---|
| 1. Per-cell predicted signs (or two-sided fallback) | §1.1 (P1) + §6.2 + §3 (two-sided branch) |
| 2. ANOMALOUS band blocks the pivot | §3 + §3.2 + §7 (`pivot_licensed` excludes ANOMALOUS) |
| 3. AMBER terminal + B_conf escalation → RED-at-ceiling | §4 |
| 4. M=400 sign-stability precondition on the pivot (load-bearing) | §1.1 (`stable_cell`) + §5(ii) |
| 5. Name the equal-arm config per cell | §6.1 |
| 6. Crossed T_c×M diagnostic before any T_c demotion | §1.2 (P2) |
| 7. Diagnostic language at n=20 reality | §1.3 |
| 8. Prose/config grep-consistency (frozen convention) | §2.2 + §8 stale-prose flag |

**Open reviewer calls carried into audit (revisable):** equal-arm choice τy-matched vs (τx,τx) vs dual (§6.1); B_max ceiling = 128 (§4); estimand (a) licensing assumption for the T_c cells (§2.1); retain 8-block or adopt 16 (D2). The RED-direction correction (§3.3) is HQ's flagged deviation from v2 §5 for Antigravity to ratify.

---

## 10. Antigravity audit reconciliation (HQ diff, 2026-07-07)

Antigravity's pre-reg audit (`AUDIT_VERDICT_ANTIGRAVITY.md`, Gemini 3.5 Flash lab seat) ran against **v2** (v3 was still building) and returned 6 findings, verdict "ratifiable with the listed fixes." HQ verified each against the artifact (law #7 — external output is input, HQ diffs) and reconciled into this v3:

| # | Antigravity finding | Severity | v3 disposition |
|---|---|---|---|
| 1 | Banding GAP deadlock (`[floor−t·SE, floor]` unbanded; 98.4% null deadlock) | Blocker | **Resolved before raised** — v3's AMBER is the residual catch-all (§3, `band_cell`), fully partitioning the line; at 16 blocks RED is reachable (κ=+0.067). HQ re-derived the 50.3%/98.4% and the fix. |
| 2 | Grid-curl sign inversion at M=400 → false null | Major | **Covered** by P1 sign-stability + §5(ii) UNSTABLE-can't-pivot. *HQ caveat: Antigravity reads receipt-07's −2.6→+0.45 as physical inversion; that metric is noise-dominated at both M (receipt 07), so the concern/fix are right, the "inversion is physical" framing over-reads.* |
| 3 | T_c SD miss → 75× false-register inflation | Major | **Moot in v3** — §2.1 pins `floor_c`/SE to each cell's **own** block SD (captures T_c growth); the 75× only arises under a global T_c=1 reference SD, which v3 does not use. |
| 4 | Defective ANOMALOUS threshold (floor-keyed) launders significant wrong-sign into RED | Major | **Applied** — §3 + §7 now key ANOMALOUS on significance against 0 (`x < −t·SE`). Verified at operative 16b/B96. |
| 5 | Equal-arm-zero bias at T_c>1 | Minor | **Covered** — §2.1 licensing assumption flagged Tc-only-verified; fall back to estimand (c) for T_c cells. |
| 6 | Stale "B=64" comments/docstrings under B_conf escalation | Minor | **Covered** — §8 stale-prose flag + selftest grep extension. |

Net: 1 & 3 were already fixed by the v3 build; 4 applied; 2, 5, 6 already carried as preconditions/caveats. **The v3 spec incorporates the full audit.** Re-audit target: this document (v3), specifically the Finding-4 ANOMALOUS partition and §3.3 RED-direction deviation.

---

# APPENDIX B — `AUDIT_VERDICT_ANTIGRAVITY.md` (round 1, ran against the v2-era rule; byte-faithful)

# v4.4 Scout Pre-Registration Audit Report — Antigravity

**Audit Target:** v4.4 Movement 2 Scout Design and Decision Rules (branch `v4.4-scout-draft`, dir `v4/v44/`)  
**Auditor:** Antigravity (Google, Gemini 3.5 Flash, lab seat)  
**Verification Environment:** macOS, `/usr/bin/python3` (numpy 2.0.2)  
**Status:** Pre-Registration Audit Complete  

---

## Verdict: RATIFIABLE WITH THE LISTED FIXES

We have conducted a thorough, adversarial audit of `v44_scout.py`, `prereg_v44.json`, `SCOUT_DECLARATION.md`, `v44_scout_DECISION_RULE_v2_DRAFT.md` (the "v3" recalibrated rule), and the associated scale-10 receipts. 

We identified **6 key findings** (1 Blocker, 3 Major, and 2 Minor/Errata). The single most load-bearing fix is **Closing the Banding GAP Deadlock (Finding 1)**, which currently prevents the NESS pivot from ever firing under a true null. Once the blocker and major fixes are applied, the scout package is fully ratifiable.

---

## Summary of Findings

| # | Finding | Severity | Verdict-Impact |
|---|---|---|---|
| 1 | **Banding GAP Deadlock:** The interval $[floor_c - t^* \cdot SE_8, floor_c]$ is unbanded, causing null sweeps to freeze in limbo (cannot register, extend, or pivot). | **Blocker** | Blocks the NESS pivot on true nulls; 98.4% chance of sweep deadlock. |
| 2 | **Grid-Curl Sign-Inversion at M=400:** Grid roughness at $M_{grid}=400$ causes the curl sign to invert compared to the physical limit ($M=4000$), laundering true signal into false nulls. | **Major** | Grid artifact causes false null (RED) verdicts. |
| 3 | **$T_c$-scaling Noise Miss:** Flat $T_c=1$ equal-arm SD reference underestimates $T_c=4$ block noise by $1.62\times$, inflating false-registration rate by $75\times$. | **Major** | Inflates false-registration rate on high-$T_c$ cells. |
| 4 | **Defective ANOMALOUS Band Threshold:** Using the floor rather than significance against 0 allows highly significant wrong-sign currents to launder into RED (null). | **Major** | Permits significant wrong-sign anomalies to trigger the NESS pivot. |
| 5 | **Equal-Arm-Zero Assumption Bias at $T_c > 1$:** Causal force offsets scale with $T_c$, making the $\mu_{eq} \approx 0$ assumption unverified for the $T_c > 1$ sweep cells. | **Minor** | One-sided bias in high-$T_c$ cells. |
| 6 | **Stale Comments/Docstrings:** CFG comments and docstrings hardcode "B=64 floor" which goes stale under $B_{conf}$ escalation (96/128). | **Minor** | Prose/config consistency erratum. |

---

## Detailed Findings

### Finding 1: Banding GAP Deadlock
*   **Severity:** **Blocker**
*   **Description:** The proposed decision rule defines the bands as:
    *   **GREEN**: $\hat{\mu} - t^* \cdot SE_8 > floor_c$ (i.e., $\hat{\mu} > floor_c + t^* \cdot SE_8$)
    *   **AMBER**: $\hat{\mu} > floor_c$ and $\hat{\mu} - t^* \cdot SE_8 \le floor_c$
    *   **RED**: $\hat{\mu} + t^* \cdot SE_8 < floor_c$ (i.e., $\hat{\mu} < floor_c - t^* \cdot SE_8$)
    
    This leaves the interval $[floor_c - t^* \cdot SE_8, floor_c]$ completely unbanded (the "GAP"). Under the $N=8$ scout, $floor_c = 0.682\cdot sd$ and $t_7 \cdot SE_8 = 1.895 \cdot 0.375\cdot sd = 0.711\cdot sd$. The GAP covers $[-0.029\cdot sd, 0.682\cdot sd]$.
*   **Concrete Falsification Scenario:**
    *   **True Input:** True null ($\mu_i = 0$ for all cells).
    *   **Observed Behavior:** Each cell has a $50.3\%$ probability of falling into this GAP.
    *   **Wrong Outcome:** With 6 cells, the probability that at least one cell falls in the GAP is $1 - (1-0.503)^6 \approx 98.4\%$. A cell in the GAP is not RED (preventing the all-RED NESS pivot from firing) and not AMBER (so it is not extended). The sweep freezes in permanent deadlock.
*   **Concrete Fix:** Define AMBER to cover the entire uncertainty interval:
    $$\text{AMBER} = [floor_c - t^* \cdot SE, floor_c + t^* \cdot SE]$$
    This partitions the real line fully (RED for $\hat{\mu} < floor_c - t^* \cdot SE$, GREEN for $\hat{\mu} > floor_c + t^* \cdot SE$, and AMBER for everything in between).

### Finding 2: Grid-Curl Sign-Inversion at M=400
*   **Severity:** **Major**
*   **Description:** Causal forces are generated by the grid. The diagnostics in [07_signstability.md](file:///Users/tony_studio/Projects/entropy-as-tunable-equilibrium/v4/v44/receipts/07_signstability.md) show that the curl sign of cell A flips from negative at $M=400$ to positive at $M=4000$. Since the scout is run with $M_{grid}=400$, the grid curl will have the wrong sign in many seeds, causing the realized current to flow in the wrong direction and falsely trigger RED (null) or ANOMALOUS.
*   **Concrete Falsification Scenario:**
    *   **True Input:** A true physical CCW (+) current exists at the widest horizon (cell A) when run at sufficient grid resolution ($M=4000$).
    *   **Wrong Outcome:** Because the harness is run at $M=400$, the grid-roughness artifact flips the curl of the estimated force field to negative. The simulation runs, producing a negative current $\hat{\mu} < 0$. Under the one-sided positive CCW prediction, a negative current cannot clear the GREEN threshold, forcing the cell into RED or ANOMALOUS, leading to a false null verdict.
*   **Concrete Fix:** Run the proper seed-averaged mean-field curl sign check (v4.3 recipe) per-cell before starting the scout to verify the sign is stable at $M=400$. If a cell's sign is unstable, that cell must be run at $M=4000$ (as a local override) or the scout must run at 16/32 blocks to average out grid noise.

### Finding 3: $T_c$-scaling Noise Miss in Floor and SE Calculations
*   **Severity:** **Major**
*   **Description:** The decision rule uses a flat equal-arm reference SD (from $T_c=1$) to compute the standard error ($SE_8 = 0.375\cdot sd$) and confirmatory floor ($floor_c = 0.682\cdot sd$) for all cells. However, the diagnostics in [06_scale10_diagnostics.md](file:///Users/tony_studio/Projects/entropy-as-tunable-equilibrium/v4/v44/receipts/06_scale10_diagnostics.md) prove that the block SD scales with $T_c$ (growing by $1.62\times$ at $T_c=4$ for quad).
*   **Concrete Falsification Scenario:**
    *   **True Input:** True null ($\mu = 0$) run at cell AxT4 ($T_c = 4$).
    *   **Wrong Outcome:** Because the SD at $T_c=4$ is $1.62\times$ larger, the actual standard error of the observed mean is $0.573\cdot sd$ instead of $0.354\cdot sd$. But the rule uses the $T_c=1$ GREEN threshold ($1.393 \cdot sd$). The probability of false registration (GREEN) for this null cell rises from $0.01\%$ to $0.75\%$ (a $75\times$ inflation). Under the null, we are highly likely to falsely register the $T_c=4$ cell.
*   **Concrete Fix:** The reference SD used to calculate $SE$ and $floor_c$ for each cell must scale with that cell's $T_c$ (e.g. $sd(T_c) = sd(T_c=1) \cdot \text{scale\_factor}(T_c)$ derived from DIAG 2, or using the cell's own raw block SD with a pooling shrinkage estimator).

### Finding 4: Defective ANOMALOUS Band Threshold
*   **Severity:** **Major**
*   **Description:** The ANOMALOUS band is designed to catch large wrong-sign currents and prevent them from laundering into RED (null). The proposed definition is $| \hat{\mu} | - t^* \cdot SE > floor_c$ with the wrong sign. This threshold is too high because it requires the wrong-sign current to clear the confirmatory floor, rather than checking if it is statistically significant against 0.
*   **Concrete Falsification Scenario:**
    *   **True Input:** An anomalous grid artifact generates a highly significant wrong-sign current at $\hat{\mu} = -1.0 \cdot sd$.
    *   **Wrong Outcome:** The statistic is $2.82$ standard errors below 0 (highly significant anomaly). However, since $|-1.0| - 0.711 = 0.289 < 0.682$, it does not clear the ANOMALOUS threshold. But since $\hat{\mu} + t^* \cdot SE = -1.0 + 0.711 = -0.289 < 0.682$, it bands RED. The significant anomaly is falsely classified as RED (null), allowing a faulty instrument state to license the NESS pivot.
*   **Concrete Fix:** Define the ANOMALOUS band using statistical significance against 0 rather than the floor:
    $$\hat{\mu} < -t^* \cdot SE \quad (\text{for a predicted positive sign}) $$

### Finding 5: Equal-Arm-Zero Assumption Bias at $T_c > 1$
*   **Severity:** **Minor / Erratum**
*   **Description:** The contrast-proxy SE formulation ($SE_8 = 0.375\cdot sd$) rests on the licensing assumption that the equal-arm current is $\approx 0$. While verified at $T_c=1$, any systematic protocol offsets/currents will scale with $T_c$. At $T_c=4$, the equal-arm current is unmeasured but likely scales up, introducing a one-sided bias.
*   **Concrete Falsification Scenario:**
    *   **True Input:** A true contrast of $\Delta = 0.5 \cdot floor_c$, but with a $T_c$-scaled equal-arm current of $0.15 \cdot sd$.
    *   **Wrong Outcome:** The raw mismatch mean $\hat{\mu}_{mis}$ is shifted upward by the equal-arm offset, causing the contrast-proxy to over-estimate the true contrast and falsely register.
*   **Concrete Fix:** Pre-register that a $T_c$-cell green-light requires a two-sample contrast validation (option c) or verify the equal-arm magnitude at $T_c > 1$ before registering.

### Finding 6: Stale Comments and Docstring Grep-Check Mismatch
*   **Severity:** **Minor / Erratum**
*   **Description:** If the decision rule escalates $B_{conf}$ to 96 or 128 as proposed, the comments in `CFG["scout"]` and the docstring of `pilot_pair()` (which hardcode "B=64 floor") will become stale and contradict the active configuration, which violates Standing Law #4 (prose/config agreement).
*   **Concrete Falsification Scenario:**
    *   **True Input:** $B_{conf}$ escalates to 128 under the AMBER rule.
    *   **Wrong Outcome:** The selftest or grep-checks fail because the prose says "B=64" while the code evaluates against $floor(128)$.
*   **Concrete Fix:** Generalize the prose in CFG comments and docstrings to "implied confirmatory floor" rather than hardcoding "B=64".

---

## Verifications Executed

We have verified all physical and mechanical constraints on the target branch:
1.  **Manifest Verification:** `shasum -a 256 -c MANIFEST.sha256` passes with all 5 files OK.
2.  **Harness Selftest:** `/usr/bin/python3 v44_scout.py --selftest` runs and reports `SELFTEST PASS` for all 11 gates.
3.  **Plan Check:** `python3 v44_scout.py --plan | shasum -a 256` produces the exact preregistration hash `b7c5aeb6bd21b70036f7fb6841f199fbf923aa984cba3d30a71943c75e9a2a2b`.
4.  **Quarantine Check:** Scout cells are correctly quarantined under `v44pilot::` and are not pooled into the 392 confirmatory units.
5.  **Force linearity:** verified that `force_frozen` / `force_frozen_aniso` scale exactly linear with $T_c$ overrides.

---

# APPENDIX C — `AUDIT_VERDICT_ANTIGRAVITY_R2.md` (round 2, re-audit of v3; byte-faithful)

# v4.4 Scout Pre-Registration Audit Report (Round 2) — Antigravity

**Audit Target:** v4.4 Movement 2 Scout Design and Decision Rules v3 (`v44_scout_DECISION_RULE_v3.md`, commit `138d109`)  
**Auditor:** Antigravity (Google, Gemini 3.5 Flash, lab seat)  
**Verification Environment:** macOS, `/usr/bin/python3` (numpy 2.0.2)  
**Status:** Pre-Registration Re-Audit Complete  

---

## Verdict: RATIFIABLE AS-IS

We have conducted a thorough, adversarial re-audit of the revised $v4.4$ scout decision rule spec (`v44_scout_DECISION_RULE_v3.md`) on the `v4.4-scout-draft` branch. 

All 6 findings from our Round 1 audit have been **CONFIRMED CLOSED**. We also successfully reproduced the 4-million-draw Monte Carlo simulation in §3.3, confirming the exact false-null rates of the conjunction RED rule. 

There are no remaining blocking or major issues. The decision rule is mathematically and logically sound, complete, and ready for registration.

---

## Status of Round 1 Findings

### Finding 1: Banding GAP Deadlock — CONFIRMED CLOSED
*   **Verification:** The revised $v3$ rule defines AMBER as the residual catch-all between RED and GREEN, fully partitioning the real line:
    $$\text{ANOMALOUS } (-\infty, -t\cdot SE) \cup \text{RED } [-t\cdot SE, floor_c-t\cdot SE) \cup \text{AMBER } [floor_c-t\cdot SE, floor_c+t\cdot SE] \cup \text{GREEN } (floor_c+t\cdot SE, \infty)$$
    We simulated a true null ($\mu = 0$) across $100,000$ runs using the operative 16b/B96 config. Cells resolved to RED ($85.2\%$) or RED-at-ceiling ($12.3\%$) with a combined probability of **$97.5\%$**. No cells were trapped in limbo.
*   **Resolution:** Sound partition implemented.

### Finding 2: Grid-Curl Sign-Inversion at M=400 — CONFIRMED CLOSED
*   **Verification:** Checked that the pivot rule (§5(ii)) gates the pivot on `stable_cell` = STABLE for every cell. Unstable cells at $M=400$ are barred from licensing the pivot, preventing grid artifacts from laundering into false nulls.
*   **Resolution:** Precondition P1 sign-stability check successfully integrated.

### Finding 3: $T_c$-scaling Noise Miss — CONFIRMED CLOSED
*   **Verification:** §2.1 now defines both $SE$ and $floor_c$ using each cell's **own** block standard deviation (`sd_cell`) rather than a global flat $T_c=1$ reference SD. This automatically and correctly scales the thresholds with the measured $T_c$ noise growth.
*   **Resolution:** Dynamic $T_c$-scaled reference SD implemented.

### Finding 4: Defective ANOMALOUS Band Threshold — CONFIRMED CLOSED
*   **Verification:** Tested $\hat{\mu} = -1.0\cdot sd$ (the 3.6σ wrong-sign excursion scenario) under 16b/B96:
    $$x = -1.0\cdot sd < -t_{15}\cdot SE_{16} = -0.490\cdot sd$$
    The cell correctly bands ANOMALOUS and is barred from the RED band.
*   **Resolution:** ANOMALOUS threshold now keys on significance against 0 rather than the floor.

### Finding 5: Equal-Arm-Zero Assumption Bias at $T_c > 1$ — CONFIRMED CLOSED
*   **Verification:** Handled via the explicit licensing caveat in §2.1 and §6.1, allowing fallback to a two-sample contrast (estimand c) at confirmatory.
*   **Resolution:** Documented and verified.

### Finding 6: Stale Comments and Docstring Grep-Check Mismatch — CONFIRMED CLOSED
*   **Verification:** Scoped into the §8 config_hash/prereg re-issue, requiring the selftest grep-check to assert the active t-convention and B_conf.
*   **Resolution:** Covered.

---

## Pre-Registration Verifications & Re-derivations

### 1. §3.3 RED-Direction Conjunction Rule Re-derivation
We executed a 4-million-draw Monte Carlo simulation of the point-sd vs floor-only upper-sd vs conjunction-rule false-null rates for a true effect at the floor ($\Delta = floor_c$) at 16b/B96:
*   **Point-sd RED rate:** **3.951%** (Expected: ~3.9%)
*   **Floor-only upper-sd RED rate:** **18.860%** (Expected: ~18.9%)
*   **Coupled upper-sd RED rate:** **4.933%**
*   **Conjunction RED rate:** **3.951%** (Expected: ~3.9%)

The results confirm that the conjunction rule successfully holds the false-null rate at the point-sd level when $\kappa > 0$, avoiding the $5\times$ inflation of the floor-only read, while dynamically selecting the conservative coupled-upper-sd bound when $\kappa < 0$.

### 2. The ANOMALOUS Tradeoff
Under the point-significance form (`x < -t*SE`), the conservative contrast-proxy SE formulation naturally shifts the effective per-cell false ANOMALOUS rate from $5\%$ to **$2.51\%$** under a true null. Across 6 cells, the probability of at least one cell tripping a false anomaly is **$14.1\%$** (rather than the nominal $26.5\%$). 
*   **Our Lean:** We recommend keeping the point-significance form **without a magnitude margin**. A $14.1\%$ sweep block rate under the null is highly manageable, and keeps the anomaly gate clean and strictly significance-grounded.

---

## Leans on Flagged Open Items (§1.1 / §9)

*   **P1 Sign Recipe (§1.1):** We lean toward **averaging-then-curl** to register $\sigma_{cell}$ (as the physical prediction is a mean-field object), combined with a **$\ge 75\%$ seed sign unanimity** threshold (e.g., $\ge 6/8$ seeds or $\ge 12/16$ seeds) for `stable_cell` to be declared STABLE. This prevents single-grid flukes from falsely declaring stable physical cells as UNSTABLE.
*   **Equal-Arm Choice (§9):** We lean toward the **$\tau_y$-matched equal arm** at matched-$T_c$. The noise variance of the contrast is dominated by the wider time horizon $\tau_y$; pairing it with a $(\tau_y, \tau_y)$ reference provides the most homoscedastic control.
*   **$B_{max}$ Compute Ceiling (§9):** We support the working default of **$B_{max} = 128$**. This bounds the total compute time of the extension loop while providing a significant $14\%$ reduction in the detection floor.
*   **$T_c$ Licensing Assumption (§9):** We lean to **refuse the $\mu_{eq} \approx 0$ assumption for $T_c > 1$ cells**. Systematic force-mediated currents are expected to scale with $T_c$; any high-$T_c$ green-light should require two-sample contrast validation (estimand c) at confirmatory.
*   **First-pass block count (D2):** We strongly support **adopting 16-blocks** for the first pass. Making $\kappa > 0$ on the first pass enables true null cells to resolve to RED directly without entering the AMBER extension loop, saving substantial compute time.
