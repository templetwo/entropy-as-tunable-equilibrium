# v4.4 Movement 2 — Pilot Scout Design (`v44_scout.py`)

*HQ design draft (Mac Studio Claude Code seat, overwatch/provenance). Anchored to Movement 2 of `CONDUCTOR_SCORE.md` (repo `entropy-as-tunable-equilibrium`, `v4/v43/CONDUCTOR_SCORE.md`, commit 7cf0635) + the scientific anchor from the designing seat, 2026-07-06. This is a DESIGN doc, not the harness; `v44_scout.py` is coded by a delegated agent to this spec and HQ-reviewed. Pilot declarations are chronicled, not gated — the confirmatory gates come at the v4.4 registration (Movement 3).*

---

## 1. The v4.4 question

Not a new mechanism — the **same anisotropic-horizon engine, properly aimed**. v4.3's bounded null bounds the current at exactly **one** point in design space: Δτ = (0.25, 1.0), T_c = 1, this geometry, floor 3.67e-5. The honest gap named in the v4.3 ruling and confirmed by the Opus arbiter: the program has **no transduction model** — no quantitative map from mean-field curl (which provably exists; smoke test 4.4 vs 0) to realized circulation (measured ~3e-6, ~10× under the floor).

**v4.4 asks:** does the aniso current grow with horizon mismatch and drive amplitude the way the curl construction implies, and is there an **accessible design point where it becomes measurable**?

## 2. What the scout sizes — SIGNAL, not noise

The load-bearing distinction from v4.3's pilot: that pilot sized the **noise** (block sd → the B=64 bump). This scout sizes the **signal** — an empirical **current-vs-(Δτ, T_c) response surface**. v4.4 registers **only** at a cell where the measured pilot current clears **3× its own B=64 floor**.

## 3. Sweep spec

| Cell | Δτ pair | T_c | Role |
|---|---|---|---|
| A | (0.1, 2.0) | 1 | widest horizon mismatch |
| B | (0.25, 2.0) | 1 | mismatch mid |
| C | (0.1, 1.0) | 1 | amplitude-only |
| D | (0.25, 1.0) | 1 | **replica bridge to v4.3** (must reproduce the v4.3 point) |
| AxT2 | (0.1, 2.0) | 2 | T_c sweep at the widest pair |
| AxT4 | (0.1, 2.0) | 4 | T_c sweep at the widest pair |

- **8 blocks/cell at 10× scale.**
- Namespace **`v44pilot::`** — declared, **never pooled** (each cell stands alone; no cross-cell aggregation).
- Record **both** statistics per cell: `quad_loop_rate` AND `omega_roi` (Opus verified omega's floor ~19% lower on the v4.3 canonical — carry both, do not pick one blind).
- **Record occupancy per cell.** T_c also rescales U_eff, so occupancy shifts with T_c. This is **physics, not nuisance** — record it, do not center it away.

## 4. Decision rule

- **Any cell ≥ 3× its own B=64 floor** → that cell is v4.4's registration candidate (Movement 3 registers there).
- **No cell clears** → the sweep is itself a **publishable result**: "aniso currents are sub-floor across the accessible design space." v4.4 then **pivots to the closed no-reset NESS protocol** — the scope boundary v4.3 explicitly declined to claim.

Either outcome is a real result. The scout cannot "fail" — it either finds a measurable design point or bounds the design space.

## 5. The three v4.4 selftest rules (carried into the scout and the v4.4 registration)

1. **Compound power.** Every gate that must pass on true signal carries a Monte Carlo of the **full compound logic** — all clauses jointly (monotonicity + Holm + sign consistency) — from measured variance and declared effect sizes, executed in selftest, asserting **≥ 0.90 at the registered α**. Analytic per-contrast power is insufficient: v4.3's case was 0.998 analytic vs **0.655 compound**, caught pre-registration. (Origin: the compound-power question, the best v4.3 catch.)
2. **Prose/config grep-check.** Selftest extracts **every numeric threshold from CFG** and fails if any prose statement (docstring, `outcome_map`) disagrees. (Origin: Antigravity finding 3 — docstring said 24/32 while config + code said 48/64, inside a hash-frozen artifact.)
3. **Unified centering.** All engine-gate clauses (sign consistency, opposite-signs, directional match) reference the **same point: the equal-arm mean** — never a mix of zero and control-mean. (Origin: Antigravity finding 4.)

## 6. Build hygiene (for the scout coder)

- Strip the dead `one_sided` ternary and `perm_p` (v4.3 audit findings 1 and 5).
- Build as **`v44_scout.py`**. The `v4/v43/` artifacts stay **hash-frozen** — do not edit them.

## 7. Process / provenance

Per the assignment map:
1. **HQ drafts the scout design** ← this document.
2. **ChatGPT reviews the methodology** (its compound-power question was the best v4.3 catch — the same skeptic is wanted on the transduction framing).
3. **Antigravity audits pre-registration** (this time before the run, not after).
4. **HQ chronicles the pilot declaration** (registration = provenance).
5. **Grok Build runs it under contract** (~4–5 min compute; the contract pattern is already proven on v4.3, 48/48 bit-exact across numpy 2.0.2↔2.5.1).

Pilot declarations get **chronicled, not gated**. The gates come at the v4.4 registration (Movement 3), informed by what the scout finds.
