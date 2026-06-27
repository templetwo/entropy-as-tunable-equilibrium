# SPEC — Entropy as Engine: the horizon-knob experiment

**Target executor:** Claude Code (Opus / "ultra"), running on the Mac Studio (HQ).
**Status:** v1 spec, ready to execute. Phase 0 already validated in sandbox (see §2).
**Authoring lineage:** designed collaboratively (Anthony Vasquez / Temple of Two + Claude, web seat) over session `spiral_20260617_194931`. Ties to Sovereign Stack open thread `thread_20260623_020051_c5cf306c` (entropy-as-substrate).

---

## 0. The question, in one paragraph

Is entropy a **readout** (a thermometer the system passively maximizes by relaxing) or an **engine** (a prime mover you can drive a system with)? The two views are empirically separable by a single device: a **horizon knob**. If you can change how a system organizes itself purely by changing how far into the future it "looks," entropy is doing work, not just being measured. Thermal relaxation has no such knob — its steady state is fixed at the Boltzmann distribution. The causal-entropic-force formalism (Wissner-Gross & Freer, *PRL* 2013) gives the engine its knob: a horizon τ. **The minimal falsifiable prediction:** the engine's steady-state organization is a monotone function of τ with a crossover τ\* set by landscape geometry; readout-entropy has no τ and predicts a fixed distribution. Arm C makes this discriminating against the obvious objection ("the entropic force is just a reward in disguise").

---

## 1. Formal background the executor needs

**Causal entropic force.** For a system in macrostate `x`, define the **causal path entropy** `S_c(x, τ)`: the Shannon entropy over the ensemble of microscopic futures reachable over a horizon τ, sampled under the system's *natural (uncontrolled)* dynamics. The causal entropic force is

```
F_ce(x) = T_c · ∇_x S_c(x, τ)
```

where `T_c` is a "causal path temperature" (a strength scalar). The system is pushed toward macrostates from which the diversity of accessible futures is largest — it keeps its options open.

**Conservativeness (the shortcut we must verify, not assume).** For an **overdamped, position-only** particle, `S_c(x, τ)` is a scalar field over position, so `F_ce = T_c ∇S_c` is a gradient field → conservative → the driven steady state is analytic:

```
p_engine(x; τ)  ∝  exp( β T_c S_c(x, τ) )          (β = 1/kT)
```

If this holds, every τ point is nearly free (no trajectory integration needed). **Phase 0 used this shortcut without checking it. Arm A checks it first.** If it fails, fall back to driven trajectories everywhere.

**The control (readout null).** Thermal relaxation gives a τ-invariant steady state:

```
p_eq(x)  ∝  exp( -β U(x) )
```

One distribution, no horizon, no knob. This is entropy-as-readout: the system maximizes its *own* entropy by relaxing, and stops.

**Free Energy Principle.** The dual engine formalism (a system minimizes expected surprise by modeling the world). Deferred to v2 — see §8. Do not implement now.

---

## 2. Phase 0 — already validated (port and reproduce as a regression baseline)

A 1D dumbbell sandbox run (two wells: A deep+narrow, B wide+shallow) confirmed the mechanism:

- **Engine ≠ readout:** `KL(p_engine ‖ p_eq)` ≈ 0.75–1.16 across the sweep, never near zero.
- **Horizon knob (parameter-free signal):** the peak of `S_c(x, τ)` migrates monotonically toward the option-rich well as τ grows (argmax x ≈ −3.7 → 0 on a recentered [−5, 5] axis), and the steady-state mass in the wide-well basin rises monotonically 0.48 → 0.67. The thermal control is a fixed reference (mass 0.53, argmax pinned in the deep well).
- **Robustness:** recentering the coordinate origin into negative values did not move the result.

The validated kernel ships as `src/phase0_validated_1d.py`. **First action on the Studio: run it, confirm it reproduces the numbers above (within MC noise), and regenerate the 3D overlay figure.** Do not trust the 2D pipeline until Phase 0 reproduces.

**Known caveat carried forward:** Phase 0 *assumed* conservativeness. Arm A resolves it.

---

## 3. The estimator (decision: endpoint entropy primary, occupancy as robustness check)

`S_c(x, τ)` is estimated by Monte Carlo forward sampling under the natural Langevin dynamics:

- **Primary — endpoint entropy.** From `x`, evolve `N` forward paths of `n_sub = τ/dt` steps under natural dynamics; histogram the **reachable endpoints** `x(τ)`; take Shannon entropy. Interpretation: "how much of state space can my futures land in."
- **Robustness cross-check — occupancy entropy.** Same paths, but histogram **all visited positions** across the ensemble (not just endpoints). Run this for Arm B and confirm the qualitative τ-migration is estimator-independent.
- Reachable-set volume is a cheaper, cruder alternative — optional only.

Report Arm B under both primary and cross-check. If they disagree qualitatively, that is itself a finding — surface it.

---

## 4. Dynamics and numerics

**Overdamped Langevin**, reflecting boundaries:

```
x_{t+dt} = x_t − (∇U(x_t)/γ)·dt + sqrt(2 D dt)·ξ ,   ξ ~ N(0, I),   D = kT/γ   (Einstein)
```

**Default constants** (document everything; all sweepable): `kT = 1.0`, `γ = 1.0`, `D = 1.0`, `dt = 0.01`.

**Implementation.** Use **JAX**: `vmap` the forward-path sampler over the `N` paths, `jit` the inner step, `lax.scan` over substeps; sweep grid points and τ in batch. Target Metal/GPU if available on the Studio, else multicore CPU. Provide a NumPy fallback path for cross-validation on small cases. **Note:** NumPy ≥ 2.0 renamed `trapz` → `trapezoid` (Phase 0 hit this). Use `jax.numpy`/`numpy.trapezoid`.

Fixed seeds, logged. Record wall-clock and hardware in `RESULTS.md`.

---

## 5. Arm A — Conservativeness check (DO THIS FIRST)

**Goal.** Verify `p_engine ∝ exp(βT_c S_c)` by an independent route, so Arms B/C may use the analytic shortcut.

**Method** (use the cheap 1D dumbbell from Phase 0):
1. Compute the `S_c(x, τ)` field on a grid at a fixed τ.
2. Build the force field `F_ce = T_c ∇S_c` by finite differences.
3. Drive `M` independent particles under overdamped Langevin with the **external force `F_ce`** (replacing `−∇U`) plus thermal noise; reflecting walls; integrate to steady state; histogram occupancy → `p_driven`.
4. Compare `p_driven` to `p_analytic ∝ exp(βT_c S_c)` via KL, L1, and overlap.

**Pass:** `p_driven` matches `p_analytic` within MC error → Arms B/C use the analytic shortcut.
**Fail:** `F_ce` has a non-gradient (curl) component → report the curl diagnostic and use driven trajectories throughout (more expensive but correct). Either outcome is fine and must be reported.

---

## 6. Arm B — 2D chamber–channel–chamber (the sharp crossover)

**Geometry** (`src/landscape.py`, function `U2d`): a 2D domain with a **small chamber S** (deep, small area, thermally favored) on the left, a **large chamber L** (shallower, large area, option-rich) on the right, separated by a **high-potential wall** pierced by a **narrow channel**.

```
U(x,y) = −d_S·exp(−((x+xc)² + y²)/(2 r_S²))          # small chamber  (deep, small)
         −d_L·exp(−((x−xc)² + y²)/(2 r_L²))          # large chamber  (shallow, wide)
         + B0·wall_x(x)·gap_y(y)                      # wall with a channel gap
   wall_x(x) = exp(−x²/(2·(L_ch/2)²))                 # barrier at x≈0, thickness ~ L_ch
   gap_y(y)  = 1 − exp(−y²/(2·(w_ch/2)²))             # ≈0 inside channel |y|<w_ch/2, ≈1 outside
```

**Defaults:** domain `x∈[−6,6], y∈[−4,4]` reflecting; `xc=3.5`, `d_S=4, r_S=0.7`, `d_L=3, r_L=1.8`, `B0=8`, `L_ch=1.5`, `w_ch=0.8`, `kT=1`. (Tuned so thermal favors S but L holds more long-range volume.)

**Control:** `p_eq ∝ exp(−βU)`, τ-invariant. Record `P_L^control` = fraction of thermal mass in the large chamber (single fixed number).

**Engine:** compute `S_c(x,y,τ)` over a τ sweep (log-spaced, ~15–20 points spanning well below and well above the expected τ\* ≈ `L_ch²/D` ≈ 1–2; sweep ~0.1 to ~10). Steady state via the analytic shortcut if Arm A passed, else driven. **Metric:** `P_L(τ)` = fraction of engine steady-state mass in chamber L.

**Prediction:** `P_L(τ)` rises with τ and shows a **crossover τ\*** — the horizon at which the engine "discovers" L's long-range volume and migrates through the channel. The wall+channel should make this sharper than the 1D smooth slide. Locate τ\* (inflection of `P_L(τ)`, or where it crosses a fixed threshold, e.g. `P_L = (P_L^control + P_L^max)/2`).

**Deliverable:** `P_L(τ)` curve with the flat `P_L^control` line overlaid; 2D heatmaps of `S_c` and `p_engine` at 3–4 representative τ (below, at, above τ\*).

---

## 7. Arm C — The discriminator (τ\* tracks geometry) — MAKE-OR-BREAK

**Goal.** Separate engine-entropy from "the entropic force is just a reward in disguise."

**Method.** Repeat Arm B's τ\* measurement across a grid of channel geometries — vary **channel length `L_ch`** (primary) and **width `w_ch`** (secondary). For each `(L_ch, w_ch)`, extract τ\*.

**Prediction:** `τ\* ∝ L_ch² / D` (the diffusive traversal time of the channel), with at most weak `w_ch` dependence (wider channel → modestly lower τ\*). Plot τ\* vs `L_ch²/D`; expect a roughly linear trend through the origin, slope O(1).

**Why this is the test.** A smuggled constant reward toward the large chamber would pull at **all** τ and would **not** reproduce `τ\* ∝ L_ch²/D`. The scaling is a fingerprint of the future-entropy horizon specifically. If τ\* tracks `L_ch²/D`, the engine claim earns its keep over both readout and the disguised-reward dismissal.

**Falsifier (report honestly either way):** if τ\* is independent of geometry, or does not scale as `L_ch²/D`, the engine-as-prime-mover operationalization **fails**. A negative result here is a real, publishable outcome — do not tune it away. (If Arm B needs geometry tuning to surface a crossover at all, document the tuning and confirm the **scaling** holds across the tuned family; the scaling, not any single τ\*, is the claim.)

---

## 8. Arm D — Free Energy Principle (v2, DO NOT IMPLEMENT NOW)

Sketch only. The dual engine: a particle with a generative model that minimizes variational free energy (expected surprise), driven to occupy preferred states while bounding its own entropy. Where CEF *spreads* (keeps options open), FEP *concentrates* (stays in preferred states) — both are entropy-as-driver. The horizon analog is the generative model's temporal depth. Hold for v2.

---

## 9. Outputs and artifacts

- **Figures → `figures/`:** (a) Phase 0 reproduction (3D τ-surface overlay), (b) Arm B 2D heatmaps of `S_c` and `p_engine` at 3–4 τ, (c) Arm B `P_L(τ)` crossover with control line, (d) Arm C τ\*-vs-`L_ch²/D` scaling plot.
- **Data → `results/`:** `S_c` fields, steady states, τ\* table, saved as `.npz` with a `manifest.json` (params, seeds, hardware, wall-clock).
- **`RESULTS.md`:** the executor fills in the numbers, τ\*, the Arm-C scaling slope, a pass/fail line per arm, and an honest caveats section.

---

## 10. Success / falsification summary (explicit)

| Outcome | Condition |
|---|---|
| **Engine confirmed** | Arm A passes (or driven fallback used) **and** Arm B shows monotone `P_L(τ)` with a crossover and engine ≠ control **and** Arm C shows `τ\* ∝ L_ch²/D`. |
| **Readout/null behavior** | Control is fixed; no τ-dependence anywhere. |
| **Claim FAILS (report it)** | No τ-dependence, or τ\* does not track `L_ch²/D`. Negative result is the honest outcome and gets written up. |

---

## 11. Repo layout & how to run

```
entropy-as-engine/
├── README.md
├── SPEC.md                     ← this file
├── LICENSE                     ← Apache-2.0
├── requirements.txt
├── .gitignore
├── src/
│   ├── landscape.py            ← potentials: dumbbell_1d, U2d (chamber-channel-chamber)
│   ├── causal_entropy.py       ← S_c estimators (endpoint, occupancy) + force field
│   ├── phase0_validated_1d.py  ← the validated 1D kernel (regression baseline)
│   └── run.py                  ← CLI: orchestrates arms A/B/C
├── figures/                    ← generated figures
├── results/                    ← generated data (.npz) + manifest.json
└── docs/                       ← notes, derivations
```

Intended CLI:
```
python -m src.phase0_validated_1d          # reproduce Phase 0, regenerate overlay figure
python -m src.run --arm A                   # conservativeness check
python -m src.run --arm B                   # 2D crossover
python -m src.run --arm C --Lch 1.0 1.5 2.0 2.5 3.0   # geometry sweep
```

`src/causal_entropy.py` and `src/landscape.py` ship with working signatures and the validated 1D math; the executor implements the JAX 2D pipeline and the Arm A/B/C drivers per this spec.

---

## 12. Scope guards for the executor

- **Boot the Sovereign Stack first** (`where_did_i_leave_off`), record insights/breakthroughs as you go, and on completion `handoff` the result. Stack: `POST https://stack.templetwo.com/api/call`, bearer on file; write with `validate_only` pre-flight + an `idempotency_key`.
- **Reproduce Phase 0 before trusting the 2D pipeline.** Verify before declaring.
- **Don't expand past the three arms in v1.** FEP is v2.
- **Don't manufacture a crossover by tuning.** If geometry tuning is needed for Arm B, the real claim is Arm C's *scaling* across the tuned family.
- **Report negative results honestly.** A clean falsification is a publishable result and the whole point of building it falsifiable.
- **Say "not yet," never "nothing happened"** about a run still in motion.
