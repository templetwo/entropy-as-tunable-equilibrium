# v4.4 Scout — Decision Rule v2 (DRAFT for ratification)

*HQ (Mac Studio Claude Code seat, overwatch/provenance), 2026-07-07. This is a **proposal**, not a registration. It supersedes nothing until Anthony + the physics-review seats (ChatGPT methodology, Antigravity pre-reg) ratify it. Origin: Fable-5 independent advisor review found the registered scout's decision rule is arithmetically self-defeating — it pre-commits the pilot to a null outcome under the reviewers' own effect-size priors. No harness bytes or `prereg_v44.json` are edited by this draft; if ratified, the change lands as (a) a revised `SCOUT_DECLARATION.md` decision-rule section and (b) a small banding function in `analyze()`. The frozen v4.3 artifacts stay hash-frozen.*

---

## 0. The exact instrument (verified against the code, not the prose)

Detection floor (`_detection_floor`, line 670), a **two-arm** minimum-detectable-effect:

```
floor(B) = (z_{1-α} + z_power) · sd_block · √(2/B)
         = (z_{0.995} + z_{0.9}) · sd_block · √(2/B)      [α_worst=0.005, power_target=0.90, verified CFG]
         = 3.858 · sd_block · √(2/B)
```

| B | two-arm floor `3.858·sd·√(2/B)` | one-arm floor `3.858·sd·√(1/B)` |
|---|---|---|
| 64  | **0.682·sd** | 0.482·sd |
| 96  | 0.557·sd | 0.394·sd |
| 128 | 0.482·sd | 0.341·sd |

Scout runs **8 blocks/cell** (`CFG["scout"]["blocks"]=8`), so a per-arm pilot mean has standard error **SE₈ = sd/√8 = 0.354·sd** (a two-arm *contrast* estimate would carry `sd·√(2/8)=0.5·sd`).

**Key identity that the whole recalibration turns on:** by construction, a B-block confirmatory has ≥90% power at α=0.005 to detect *any* true effect ≥ floor(B). So `floor(B)` is not a "comfortable" bar — it is the *smallest effect the confirmatory is designed to catch*. Any real effect between 1× and 3× floor is squarely inside the confirmatory's detection range.

**Estimand (verified against the code, must be pinned before the inequalities are frozen):** all six scout cells are **mismatch** (tx<ty); there is **no paired equal-τ arm** in `pilot_pair`, and the floor's `sd_eq` is borrowed from the confirmatory aniso equal arm (`analyze` line 749). But the aniso *effect* is a **contrast** — mismatch minus equal — which is exactly why the code's floor carries the two-arm `√(2/B)`. So the scout's raw mismatch current μ̂ is a **proxy for the contrast Δ = μ_mis − μ_eq**, valid under **equal-arm current ≈ 0** (v4.3 measured μ_eq ≈ 3e-6, ~10× under floor). Pinning this fixes the √2 ambiguity in the GREEN threshold (see §2).

---

## 1. The defect in the registered rule

Registered rule (`SCOUT_DECLARATION.md`): *"Any cell whose measured pilot current clears 3× its own B=64 detection floor → registration candidate; else publishable null → pivot to NESS."*

Trigger threshold = 3 · floor(64) = 3 · 0.682·sd = **2.05·sd**, judged from an 8-block mean whose SE is 0.354·sd. Trigger probability as a function of the *true* effect μ (in units of sd):

| true μ | as ×floor(64) | P(8-block mean ≥ 2.05·sd) |
|---|---|---|
| 0.682·sd | 1× floor | **6e-5** |
| 1.37·sd  | 2× floor | 0.025 |
| 2.05·sd  | 3× floor | 0.50 |
| 2.50·sd  | 3.66× floor | 0.90 (reliable) |

So the rule needs the **true** effect to sit at ~3.7× the confirmatory floor before it fires reliably. Now overlay ChatGPT's own most-optimistic effect-size heuristic — Tc=4 at 10–16× the v4.3 bridge mean (2.94e-6) ≈ 4.7e-5, which is only **~1.3× the v4.3 floor (3.67e-5)**. Under the reviewers' *own priors*, no cell reaches even 2× floor, and the registration branch fires with probability well under 0.1% across all six cells.

**Consequence:** the "pivot to NESS null" outcome is very nearly predetermined, and every effect in the 1×–3× floor band — exactly the effects a B=64 confirmatory exists to detect — is mislabeled "null." That is a design choice wearing an empirical result's clothes. The scout as written cannot report the one finding (a small-but-registrable current) that would actually advance the program.

Two secondary defects compound it:
- The floor is estimated from **n=8** blocks, so `sd_block` carries roughly **±27% relative error** (χ² on 7 df). Borderline calls are randomized by SD-estimation noise alone.
- The rule says "measured pilot current" but the scout records **two** statistics per block (`quad_loop_rate`, `omega_roi`). Six cells × two statistics is an unspecified forking path.

---

## 2. Recalibrated rule (proposal)

The scout's job is a **three-way triage** on the response surface, not a single pass/fail gate. Report μ̂ = 8-block mean ± SE₈ per cell (that *is* the deliverable — the current-vs-(Δτ,Tc) surface). Then band each cell on the **pre-specified primary statistic** against its own projected confirmatory floor `floor_c = floor(B_conf, sd_cell)`:

- **GREEN — register a confirmatory at this cell.**
  Lower scouting-grade bound clears the confirmatory floor: **μ̂ − 2·SE₈ > floor_c**.
  (We are reasonably confident the true effect is at least what a B_conf run can detect.)
- **AMBER — promising; extend blocks, do NOT call null.**
  Point estimate above floor but not separated from it: **μ̂ > floor_c** and **μ̂ − 2·SE₈ ≤ floor_c**.
  Action: add blocks at this cell (e.g. 8 → 32) and re-band. The pilot is simply underpowered here.
- **RED — bounded sub-floor.**
  Confident the effect is below what the confirmatory could catch: **μ̂ + 2·SE₈ < floor_c**.

**Pivot rule (this is the actual fix):** pivot to the closed no-reset NESS protocol **only if ALL cells are RED** — i.e. every cell is confidently bounded sub-floor *after* AMBER cells have been extended. If any cell is GREEN, register there. If the best cell is AMBER, extend before deciding. This closes the hole where an AMBER (real-but-underpowered) cell was laundered into the RED/null bucket.

Sign handling: the mismatch cells carry a **predicted** sign, so band one-sided in the predicted direction. A large *wrong-sign* value is not a win — see the ANOMALOUS band below. (The "− 2·SE₈" in the band definitions above is shorthand; the frozen bound is **− t*·SE** with the estimand-pinned SE of §2.1.)

### 2.2 Red-team addenda (Fable) — band-logic holes and terminal rules

Four gaps in the skeleton above; all land in the declaration + `band_cell()`, none touch harness physics:

1. **RED is unreachable on a first pass, by construction — state it and budget for it.** At 8 blocks, RED needs μ̂ + t₇·SE < floor ⇒ μ̂ < (0.682 − 1.895·0.375)·sd ≈ **0.0·sd** (and with §5's conservative upper-sd floor, literally impossible). So pass one is effectively "GREEN or extend" for any cell with a non-negative estimate; **the all-RED pivot cannot fire without extending cells**. This is anti-false-null by design, but the declaration must say so and budget the extension compute. (At 16 blocks RED needs μ̂ < 0.24·sd; at 32, < 0.56·floor.)
2. **AMBER needs a terminal rule (no infinite extension / sequential-testing leak).** Pre-specify: **one** extension (8/16 → 32 blocks) per AMBER cell; a cell still AMBER against floor(64) then **escalates B_conf** (64 → 96 → 128; the floor drops 0.682→0.557→0.482·sd, so a persistent AMBER may resolve GREEN against a larger confirmatory) up to a **declared compute ceiling B_max**. Past the ceiling it becomes "bounded below floor(B_max)" = **RED-at-ceiling**. This makes the loop finite and the pivot condition well-defined, and couples to decision-4 (which B_conf).
3. **ANOMALOUS band (blocks the pivot).** With one-sided banding a large *wrong-sign* current has signed μ̂ far below floor and would band RED, laundering an artifact into the null bucket. Add a fourth band: **ANOMALOUS = |μ̂| − t*·SE > floor_c with the wrong sign** → does **not** count toward the all-RED pivot; triggers investigation (grid artifact / transduction breakdown).
4. **Pivot needs an instrument precondition.** all-RED licenses the NESS pivot **only if** the per-cell seed-averaged mean-field sign-stability check (§4.1, receipt 07) passed for every cell. Otherwise a RED reads "RED at M=400" and at least one higher-M (or seed-averaged-grid) cell must run before pivoting. This is the one path by which a live effect could be abandoned on an instrument artifact — it must be closed.

**Per-cell predicted signs do not exist yet (forking-path risk).** One-sided banding needs a per-cell sign, but τ-swap oddness gives only the *relative* sign between a pair and its swap, and all six scout cells are tx<ty (no swapped arm runs). The registered v4.3 signs were derived cell-specifically from the M=4000 seed-averaged mean-field curl (unanimous). So either (i) **derive per-cell signs by that recipe before the run** (shares compute with the §4.1 precondition), or (ii) **band two-sided**, which moves GREEN to t₇(two-sided)=2.365 ⇒ **≈2.30× floor** at 8 blocks (using the 0.375·sd SE). Decide before registration.

### 2.1 Pinning the estimand and the exact GREEN bar (fixes the √2)

The bound "μ̂ − t*·SE" only has one right form once we say *what* μ̂ estimates and *which* floor it faces. Three coherent choices; they move the GREEN bar between 1.69× and 2.39× the named two-arm floor (one-sided t₇), which is exactly the register-vs-extend edge, so it must be pinned:

Convention frozen for every number below (so the law-#4 prose/config grep-check passes): **one-sided t at (n−1) df**, t₇ = 1.895 (8 blocks), t₁₅ = 1.753 (16), and GREEN = μ̂ − t*·SE > floor. All thresholds in units of the named two-arm floor(B=64) = 0.682·sd.

| Framing | μ̂ is… | floor yardstick | honest SE at 8 blocks | GREEN threshold (t₇) |
|---|---|---|---|---|
| **(a) contrast-proxy — RECOMMENDED** | raw mismatch current, μ_eq from v4.3's B=64 equal arm (not zero-variance) | two-arm `floor(B_conf)` (what Movement 3 runs) | `sd·√(1/8 + 1/64) = 0.375·sd` | μ̂ > **2.04× floor** (>1.39·sd) |
| (b) one-sample | raw mismatch current, tested ≠ 0 | one-arm `0.482·sd` (B=64) | one-arm `0.354·sd` | μ̂ > 1.69× the two-arm floor — but forecasts a one-arm confirmatory M3 won't run |
| (c) measured contrast | mismatch − equal, both measured fresh | two-arm `floor(B_conf)` | two-arm `0.5·sd` | μ̂ > **2.39× floor** (>1.63·sd) |

**HQ recommends (a).** It compares the pilot's lower confidence bound on the true contrast Δ against the *future confirmatory's* minimum detectable Δ — the correct predictive-power construction (Fable confirmed the mixed √(2/B_conf) floor with a one-arm-ish SE is coherent once the estimand is pinned this way, not an inconsistency). The honest SE folds in v4.3's B=64 equal-arm reference (`0.375·sd`, vs the naive zero-variance `0.354·sd` — a 3% shift, 1.98× → **2.04× floor**), so μ_eq is treated as an *estimate*, not a magic zero. Licensing assumption — **equal-arm current ≈ 0** — is v4.3-grounded (μ_eq ≈ 3e-6 = 8.2% of floor, one-sided known-direction bias) but **verified only at (1.0,1.0), T_c=1**: if any protocol offset is force-mediated it scales with T_c, so this must be re-stated (or re-measured) for the T_c cells if they are kept. If reviewers decline the assumption, fall back to (c) at 2.39× floor (a per-cell equal arm, 2× blocks).

**floor_c must be named per candidate cell.** "The bar the confirmatory must clear" is only defined once each cell's confirmatory equal-arm config is named — cell A (0.1,2.0) compares against *which* equal arm, (0.1,0.1) or (2.0,2.0)? at what T_c for AxT2/AxT4? The declaration must name the equal-arm config per candidate cell, or the forecast target is ambiguous. (Open item.)

The bound self-completes: as AMBER cells gain blocks, SE shrinks and they resolve GREEN or RED (t₁₅ → 1.64× floor at 16 blocks; see §3 for the extension/terminal rule). Nothing above ~1× floor gets a null stamp without earning more blocks first.

*Multiplicity note (footnote-level, non-blocking):* six cells selected-on-GREEN carries mild false-register inflation, but AMBER-as-default makes false-GREEN the low-consequence error (a wasted confirmatory, not a killed result), so acknowledging it in the declaration suffices; no α-spend needed at the pilot.

Optional but recommended: raise the first-pass scout to **16 blocks/cell** (SE₈→SE₁₆ = 0.25·sd) so fewer cells start in AMBER and the surface is better resolved. Blocks at scale 10 are cheap relative to a mis-scoped registration.

---

## 3. Pre-specify the primary statistic (one decision needed)

Pick **one** primary before the run; the other is descriptive/secondary. The two candidates:

- **`quad_loop_rate` (continuity choice).** It is the v4.3 registered primary; the C4v vortex positive control and the G1 gate are calibrated on it. Keeping it primary means the scout is read on the same instrument the program already proved powered.
- **`omega_roi` (sensitivity choice).** The Opus arbiter noted its floor ran ~19% lower on the v4.3 canonical (more sensitive → smaller detectable effect), and the pilot data argue it is trajectory-limited. Fable recommends it as primary.

HQ leans **quad primary / omega pre-registered secondary** for instrument continuity with the powered v4.3 G1 control, but omega's sensitivity edge is real. **This is a reviewer/Anthony call** — the only requirement Fable's critique imposes is that it be *pre-committed*, not resolved post hoc when one clears and the other doesn't.

---

## 4. T_c cells: interpretation + self-defeat gate

A GREEN on **AxT2/AxT4** is a **drive-amplitude** claim (Tc raised the causal-entropic force), *not* a geometric (Δτ) claim. The two must not be conflated at Movement-3 registration.

Moreover the T_c cells are only interpretable if they are not self-defeating: T_c multiplies the grid-noise curl exactly as it multiplies the true curl, so if the block SD carries a grid-noise component, each T_c cell's own floor inflates with T_c and mean/floor becomes ~T_c-invariant — the amplitude axis then measures little new at M=400.

**Measured (HQ scale-10 diagnostics, equal-τ, n=20/arm, 2026-07-07): the T_c cells' floor inflates with T_c, but they remain the highest-sensitivity cells in the design.** Block SD *grows* with T_c — quad 1.25× (T_c=2), 1.62× [1.15,2.39] (T_c=4); omega 1.50×, 2.00× [1.37,2.84] (T_c=4), both T_c=4 CIs excluding 1. **The net arithmetic (Fable's correction to an earlier HQ over-read):** the mean aniso force is *linear* in T_c (`force_frozen_aniso`, F ∝ tc), so under linear response the signal scales ~4× at T_c=4 while the measured SD (hence floor) grows only 1.6–2×. Net **mean/floor improves ~2–2.5× at T_c=4.** So "self-defeating" is true only relative to the naive 4× hope — the T_c cells are *not* to be discarded; they are the best expected-sensitivity probes. Two caveats: (a) the SD growth is measured at *equal-τ*, where it could be T_c-scaled grid-noise curl **or** purely dynamical (a 4× stronger drift reshapes the trajectory/ROI-residence ensemble even with a perfect grid); these demand different remedies and are separated only by a **crossed T_c×M diagnostic** (4 cells, same rig) — not yet run. (b) A T_c-cell "win" is a **drive-amplitude** claim, not geometric. Recommendation: **keep AxT2/AxT4**; run the crossed T_c×M diagnostic before deciding whether they need higher M_grid; demote to descriptive only if that diagnostic shows the SD growth is grid-noise (not dynamical) AND higher M is infeasible.

### 4.1 M_grid, informed by the diagnostics (all scale-10) — with one channel still open

The diagnostics reassign the *reason* to raise M, but Fable's red-team surfaced that they do not yet test the load-bearing channel:
- **Floor is NOT the reason.** SD-vs-M at scale 10: ratio 400/2000 = 1.19 [0.80,1.74] quad, 0.87 [0.61,1.25] omega — consistent with 1, nowhere near √5. Raising M does **not** meaningfully lower the floor. ChatGPT's stated "beat-the-floor" motivation is refuted with data at the real scale.
- **External-drive scattering (measured, but the wrong channel):** κ-injection puts a *known external* vortex through the chamber; its realized response is lower at M=400 — ratio 0.90 quad (**~0.5σ, not established — consistent with zero suppression**), 0.67 omega (**~33% nominal but weak: ~2.2σ at n=20, uncorrected p≈0.03, does not survive Holm across the ~8 diagnostic contrasts**). Directionally consistent with the v4.2 roughness mechanism; not declarative. **But this measures scattering of an external force — it is NOT the aniso signal's channel.**
- **The channel that matters (grid-generated signal, UNMEASURED until now):** the aniso current is *generated by* the grid — it is the curl of the estimated S(τy)−S(τx) field. The harness's own config documents this channel is fragile: *"M=400 grids are NOT sign-stable; the prediction rests on the M=4000 mean-field estimate."* If the realized mean-field ROI curl flips sign block-to-block at M=400 (each block draws a fresh grid), the 8-block mean **self-cancels** and no number of blocks recovers it — a false null by construction. **HQ ran a quick grid-only check** (signed ROI-integrated mixed partial per scout geometry, M=400 vs M=4000; receipt `07_signstability.md`). Finding, honestly labeled inconclusive-but-informative: a **single grid's ROI curl is noise-dominated at BOTH M** (SNR ~0.3–0.5; the mixed partial amplifies grid MC noise, inflating the M=400 magnitude ~6× — the curl is −2.6 at M=400 vs +0.45 at M=4000, converging toward a small true value). The registered v4.3 prediction got a stable sign only by **seed-averaging** the field. So the per-block sign is unreliable at M=400 *and* M=4000 — meaning **raising M per block is not the clean fix; more blocks (AMBER-extension) or seed-averaged grids per block are.** The quick per-seed metric is not the right instrument (M=4000 came out *less* stable than M=400, backwards for pure MC noise), so it does **not** retire the precondition: the proper seed-averaged mean-field sign-per-cell check (v4.3 recipe) must run before the scout, and it also supplies the per-cell predicted signs §3 needs.

**Net M_grid recommendation (provisional, pending sign-stability):** the M question is **not** "does M lower the floor" (it doesn't) but "does M=400 corrupt the grid-generated signal." Until the per-cell sign-stability check clears, **do not** call M=400 "defensible for the geometric cells." If any scout cell's mean-field curl is sign-unstable at M=400, that cell must run at higher M (or the all-RED pivot must not be licensed from an M=400 null there — see §3). Cell-D still bridges v4.3 at M=400 by design, but that makes cell-D a bridge, not a clean signal point, if D is among the unstable geometries.

**Primary-statistic ↔ M coupling (§3):** these are one decision, not two. Net relative sensitivity at M=400 is roughly quad ≈ 0.90 vs omega ≈ 0.83 (omega's lower floor offset by its larger external-scattering suppression), so **quad wins at M=400, omega wins at higher M**. Decide M first, then the primary follows. And do not rest a pre-registered primary on a 2.2σ point estimate — quad-primary should rest on the v4.3 G1-calibration continuity argument, with suppression as supporting color only.

---

## 5. Floor-estimate robustness (n=8)

`sd_cell` from 8 blocks has ±27% relative error, so `floor_c` is itself noisy. Two mitigations:
1. **Shrink/pool** the block-SD estimate across the near-equal cells (or use the equal-arm reference SD) rather than each cell's raw 8-block sd, to stabilize `floor_c`.
2. Treat any cell within one SE-width of a band edge as **AMBER by default** (extend before committing). RED especially — declaring a cell sub-floor — should use the *upper* end of the sd CI so we don't call null on an underpowered SD fluke.

---

## 6. What changes if ratified (scope)

- `SCOUT_DECLARATION.md` decision-rule section → replaced by §2–§5 here. (Human-readable declaration; not hash-frozen.)
- `analyze()` → add a `band_cell(μ̂, se, sd, B_conf)` returning GREEN/AMBER/RED + the pivot-only-if-all-RED logic. Small, testable, additive; does not touch the v4.3-inherited estimator or the forward path.
- Optionally `CFG["scout"]["blocks"] 8 → 16` (config change → new config_hash; re-issue prereg). Only if we adopt the higher first-pass.
- `prereg_v44.json` → re-generated from `--plan` after the above; new sha256 recorded. The six cells, seed namespace, and never-pooled rule are unchanged.

The forward-path harness (`pilot_pair`, Tc threading, frozen estimator) is **untouched** by the rule change. This is an analysis/declaration recalibration, not a physics-instrument edit.

---

## 7. Required before Antigravity (Fable red-team, verified) — the draft is NOT yet ratifiable

The §1 defect analysis and the three-band skeleton + estimand (a) are verified sound. But Fable's red-team found the draft not yet ratifiable; these must land in `SCOUT_DECLARATION.md` + `band_cell()` first (none touch harness physics):

1. **Per-cell predicted signs** pre-registered (seed-averaged M=4000 mean-field recipe) — or fall back to two-sided banding at ≈2.30× floor. Currently a forking path (§2.2, §4.1).
2. **ANOMALOUS band** that blocks the pivot on wrong-sign currents (§2.2).
3. **AMBER terminal rule**: one extension + B_conf escalation to a compute ceiling → RED-at-ceiling (§2.2).
4. **M=400 sign-stability precondition** on the pivot, run properly (seed-averaged, per cell) before the scout — *the load-bearing one* (§4.1, receipt 07).
5. **Name the equal-arm config per candidate cell** so `floor_c` is a defined forecast target (§2.1).
6. **Crossed T_c×M diagnostic** to attribute the SD-vs-T_c growth (grid-noise vs dynamical) before any T_c-cell demotion; keep AxT2/AxT4 meanwhile (§4).
7. **Diagnostic language** stays at n=20 reality (quad suppression not established; omega 33% nominal/weak) in any frozen text (§4.1).
8. **Prose/number grep-consistency** (law #4): the frozen t₇ convention throughout; note `CFG["scout"]` comments + `pilot_pair` docstring hard-code "B=64 floor" and go stale if decision-4 picks 96/128.

## 8. Open decisions for Anthony (final say)

1. **Adopt the three-band + pivot-only-if-all-RED rule?** (HQ recommends yes — it is the core fix. The §7 items are the conditions to make it audit-ready.)
2. **M_grid + primary statistic — ONE coupled decision** (Fable): quad wins as primary at M=400, omega wins at higher M. Decide M first (M=400 first pass vs raise for the geometric cells), and the primary follows. HQ leans quad-primary/omega-secondary for v4.3 G1-calibration continuity.
3. **First-pass blocks: keep 8, or raise to 16?** (HQ leans 16 — at 8 blocks RED is unreachable on pass one, so the pivot always requires extension anyway.)
4. **B_conf for the floor projection: 64, 96, or 128?** Couples to the Movement-3 registration design and to §7 item 3 (AMBER escalation ceiling).

The three scale-10 diagnostics + the sign-stability check have run (HQ, 2026-07-07; receipts 06, 07). Net: the floor is trajectory-limited even at scale 10 (M won't lower it); the T_c cells inflate their own floor but stay the highest-sensitivity probes (linear signal outruns the SD growth ~2–2.5×); and the real M concern is not the floor but the noise-dominated per-block grid curl, which more blocks (not higher M-per-block) addresses.
