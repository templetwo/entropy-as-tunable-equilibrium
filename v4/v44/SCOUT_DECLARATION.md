# v4.4 Movement 2 — Pilot Scout Declaration

*HQ (Mac Studio Claude Code seat, overwatch/provenance), 2026-07-06. This is the human-readable pilot declaration that accompanies the machine-reproducible `prereg_v44.json`. The scout is a **pilot**: it is **chronicled, not gated**. The confirmatory gates come at the v4.4 registration (Movement 3), informed by what this scout finds. Per experimental law: this draft goes to ChatGPT (methodology) → Antigravity (pre-registration audit) → HQ chronicles the declaration + registers → Grok Build runs it under contract (raw NDJSON only, HQ diffs). Nothing here is registered or chronicled yet.*

---

## Identity anchors (verify before any run)

| Anchor | Value | How to reproduce |
|---|---|---|
| `version` | `v4h-1.4.0` | in CFG + every NDJSON line |
| `config_hash` | `a344d6c47c8a22c1` | `sha256(json.dumps(CFG, sort_keys=True, separators=(",",":")))[:16]` |
| `source_sha` | `0b65a9ee92b9fe2c` | `sha256(v44_scout.py bytes)[:16]` — the harness self-hashes at line ~98 |
| `prereg_v44.json` | `b7c5aeb6bd21b70036f7fb6841f199fbf923aa984cba3d30a71943c75e9a2a2b` | `python3 v44_scout.py --plan \| shasum -a 256` (reproducible, byte-identical) |

Canonical interpreter: **`/usr/bin/python3`** (Python 3.9.6, numpy **2.0.2** — the pinned version). Grok pins numpy 2.0.2.

## What `--pilot-pair` runs

Six cells, seed namespace **`v44pilot::`** (declared, **NEVER pooled** — each cell stands alone; no cross-cell aggregation), **8 blocks/cell at 10× scale**, frozen anisotropic-horizon chamber. Each block emits one NDJSON line recording **`quad_loop_rate` + `omega_roi` + `occupancy_x`** (both current statistics carried per the Opus arbiter's note that omega's floor ran ~19% lower on the v4.3 canonical; occupancy carried because T_c rescales U_eff — physics, not nuisance).

| Cell | (τx, τy) | T_c | Role |
|---|---|---|---|
| A | (0.1, 2.0) | 1 | widest horizon mismatch |
| B | (0.25, 2.0) | 1 | mismatch mid |
| C | (0.1, 1.0) | 1 | amplitude-only |
| D | (0.25, 1.0) | 1 | replica bridge to v4.3 |
| AxT2 | (0.1, 2.0) | 2 | T_c sweep at widest pair |
| AxT4 | (0.1, 2.0) | 4 | T_c sweep at widest pair |

## Decision rule (declared before the run)

- **Any cell whose measured pilot current clears 3× its own B=64 detection floor** → that cell is the v4.4 registration candidate (Movement 3 registers there).
- **No cell clears** → the sweep is itself a **publishable result** ("aniso currents are sub-floor across the accessible design space"), and v4.4 **pivots to the closed no-reset NESS protocol** — the scope boundary v4.3 explicitly declined to claim.

The scout cannot "fail": it either finds a measurable design point or bounds the design space. Each cell is compared **only to its own B=64 floor**, never pooled.

## Flags for the reviewers (HQ surfaces; the physics-review seats adjudicate)

1. **T_c is a LINEAR prefactor on the mean-field FORCE (not necessarily on the realized current).** In this harness the causal temperature enters as a pure multiplier on the causal-entropic force (`F = Tc·∇S`), so `curl F = Tc·∂²/∂x∂y[S(τy) − S(τx)]`. HQ verified the override is **exactly** linear at the force level: `force_frozen` / `force_frozen_aniso` scale 2×/4× with T_c to bit precision (max deviation `0.00e+00`). But the **realized current is NOT expected to scale exactly with T_c** — the thermal noise (`√(2Dδt)`) does **not** scale with T_c, so raising T_c raises the drive-to-noise ratio. Whether the realized current tracks the linear force growth **is precisely the transduction question the scout measures** — do not pre-assume it. Consequences for the reviewers: (a) the T_c cells (AxT2, AxT4) probe the drive-amplitude axis at fixed geometry; (b) a cell that clears its floor **"because T_c = 4"** is a **different scientific claim** — a drive-amplitude win — than a **geometric (Δτ) win**, and the two must not be conflated at the Movement-3 registration. **T_c is threaded as a per-cell runtime override; it is NEVER mutated on the global CFG mid-run**, so `config_hash` covers the full swept design and stays constant across the run.
2. **Cell D is a consistency check, not a bit-identity check.** "D reproduces the v4.3 (0.25,1.0) point" means its mean current should be **consistent-within-block-sd** with the v4.3 arm1 — it MUST differ at the sample level because the scout runs in the `v44pilot::` namespace (a different seed stream from v4.3's `v43::`), per the never-pooled rule. Do NOT expect or assert bit-identity with v4.3, and do NOT reuse v4.3 seeds to force it. **Reference value** (from the v4.3 canonical run `v43_run.ndjson`, arm1 `C5a_frozen_tx0.25_ty1.0`, n=64): `quad_loop_rate` mean **2.94e-06**, block sd (ddof=1) **5.86e-05**; `omega_roi` mean **−3.00e-05**, block sd **4.54e-05**. Cell D at B=8 is consistent if its mean falls within ~±(block sd)/√8 ≈ ±2.1e-05 of that, i.e. indistinguishable from the ~3e-6 v4.3 value (itself ~10× under the 3.67e-5 floor).
3. **The prose/config grep-check (selftest rule 2) is a minimal forward seed** — it confirms the CFG-derived ratios (24/32, 48/64) appear verbatim in the source. It does not yet verify each ratio sits in the correct gate context. This is deliberately left for **Antigravity to harden** at audit (origin: Antigravity finding 3).
4. **Confirmatory path proven unperturbed.** The T_c threading defaults to the original `e["Tc"]`; HQ verified byte-identity of the `data` physics payloads for a C4v and a C5a confirmatory unit between the pristine v4.3 harness and this file (default `Tc_ov=None` path). The scout additions did not touch the v4.3-inherited estimator.

## Pre-route verification (HQ, run before this draft was released to the reviewers)

Each independently run and confirmed by HQ (overwatch), not taken from the coding agents' self-reports:
- **`--selftest` PASS** under `/usr/bin/python3` — all v4.3 gates + the new prose/config grep-check (`grep:True`); the aniso G2 gate-can-fail still holds after the centering fix (null does not fire, opposite-sign signal fires).
- **Confirmatory path byte-identical.** `data` payloads for a C4v (`force_frozen`) and a C5a (`force_frozen_aniso`) unit are bit-identical between the pristine v4.3 harness and this file on the default (`Tc_ov=None`) path — the scout additions did not perturb the v4.3-inherited estimator.
- **T_c threading is exactly linear at the force level.** `force_frozen`/`force_frozen_aniso` scale 2×/4× with T_c to `0.00e+00` deviation; default `None` == T_c=1 exactly; forces non-degenerate. The drive-amplitude axis is genuinely wired through (not silently dropped to T_c=1).
- **Full-sweep finite smoke.** A reduced-scale run of all six cells (incl. T_c=2 and T_c=4, which drive the integrator 2×/4× harder than v4.3 ever ran) emits finite, non-degenerate `quad_loop_rate`/`omega_roi` for every cell — no NaN, no wholesale censoring.
- **`prereg_v44.json` reproducible** — `python3 v44_scout.py --plan` is byte-identical on re-run (sha256 `b7c5aeb6…`).

These establish only that the **instrument runs as declared**. They are NOT a result — the scout's result is the measured current-vs-(Δτ, T_c) surface Grok produces under contract, judged against the decision rule above.

## Selftest gates carried (v4.3 + the three v4.4 rules)

`--selftest` PASS covers: gyrator sign, FPT, field presence, quad synthesis, vortex sign, occupancy gate-can-fail, **compound G1-gate power** (Monte Carlo of the exact gate logic, ≥0.90 — aniso compound power is carried to Movement 3, not exercised here), aniso equal-grid consistency, aniso curl smoke, **aniso G2 gate-can-fail** (null must not fire, opposite-sign signal must fire), and the new **prose/config grep-check**. Unified centering (rule 3) fixes a real bug: the aniso sign-consistency now references the equal-arm mean, matching the opposite-signs clause (single centering reference, law #5).

## Build provenance

`v44_scout.py` began as a **byte-exact copy of the registered v4.3 harness** (`v43_harness.py`, source_sha `1b950383ae012431`). All edits are surgical against that base (116 changed lines across two disjoint scopes — forward path + analysis hardening), each HQ-reviewed. The v4.3 `v4/v43/` artifacts stay **hash-frozen**; this is a copy, not an edit of them.
