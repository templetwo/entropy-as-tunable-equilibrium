# v4.4 Scout — Registration-Grade OC Simulator: Build Spec

*HQ (Mac Studio Claude Code seat), 2026-07-08. Queued build against the RATIFIED v3.5 rule (`RATIFICATION_v3.5.md`). This is the one substantial build remaining before registration. Both external reviews named it their top ask (promote the OC evidence from a scratch draft-check script to a versioned, auditable artifact). Best executed on Fable (usage resets the 9th) or a fresh session with headroom. NOT a run of the scout; it is the operating-characteristics instrument that must clear before registration.*

## Goal
A single, versioned, seed/hash-pinned Python simulator that runs the **full v3.5 decision rule end-to-end** (band → shared ladder → pivot_licensed → all four terminal outcomes) across every predeclared scenario, and emits the operating characteristics + hard-gate pass/fail with Monte-Carlo standard errors. It replaces the scratch draft-check MC that currently backs v3.4/v3.5's numbers.

## THE LOAD-BEARING INVARIANT (bake in — do not repeat Antigravity's error)
The estimand μ̂ is a **difference against a finite 64-block equal-arm reference**. Every simulation of μ̂ (banding AND the STATE-B rerun) MUST draw/marginalize the 64-block reference so the numerator's true variance is **σ²(1/B + 1/64)** — i.e. `mu_hat = mean(B blocks) − mean(64-block reference)`, reference redrawn each replication. This makes SE = sd·√(1/B+1/64) the true SD and every gate calibrated at α=0.05. (The rerun-power arbitration: computing power with the reference held error-free gives the wrong, optimistic number and de-calibrates every gate to α≈0.019. See `ARBITRATION_rerun_power.md`.) A selftest MUST assert the realized H0 α ≈ 0.05 for the rerun to lock this in.

## Scenarios (predeclared; each with its acceptance criterion)
Run every cell through the real `analyze()` path. Scenarios: **null**; **at-floor** (±1×floor); **supra-floor** (+2×, +3×floor); **wrong-sign** at floor (S5); **omega-only** current (S8, +2×floor omega, ρ_qω sweep); **occupancy-only** (S10, +2×/+3×floor occupancy); **demotion** (S9 — sole-carrier demoted, claim shrinks, missing-key assertions); **coupling** ρ ∈ {−1, 0, 0.5, 1, 2} (belt-only regimes at ρ≤0); **STATE-B rerun** at **n_rerun=56** (honest reference-uncertain model).

## Hard gates to reproduce (v3.5 §9.3 — with MC SEs)
- Gate 1 (any false GREEN, null) ; Gate 2 (invalid pivot at 1×floor) ; Gate 5 (wrong-sign invalid pivot, incl. §8 reband channel, per ρ arm incl. ρ≤0) ; Gate 5′ ; Gate 8 (omega escape) ; Gate 11 (occupancy escape, +2× and +3× as distinct sub-cases).
- **Gate 4** (compound GREEN power at +3×floor) ≥ 0.90.
- **Gates 9 / 9Ω — THE law-#3 deliverable:** the powered STATE-B rerun must clear **compound six-cell power ≥ 0.90 by Monte-Carlo** (all clauses jointly), not just the per-contrast 0.913. This is the number v3.5 marks TBD; the sim's job is to produce it. If compound < 0.90, n_rerun must rise further (sweep n_rerun until compound clears) — report the required n.

## Laws to honor in the build (selftests, must be able to FAIL)
- **#2:** every gate demonstrably fails-on-null data (selftest injects nulls, asserts non-trigger; and injects the effect, asserts trigger).
- **#3:** compound-gate power (all clauses jointly) ≥ 0.90 in selftest — the whole reason for this build.
- **#4:** grep-check every prose threshold in v3.5 against the frozen sim config; scope the grep to LIVE-SPEC sections (historical reconciliation rows legitimately retain superseded numbers per law #9).
- **#5:** engine-gate clauses use ONE centering reference (equal-arm mean).
- Reference-uncertain α≈0.05 selftest (above).

## Robustness arms (both reviews' REVISE items — run as sensitivity, report separately)
Non-Gaussian / heavy-tailed block metrics; heteroscedastic equal-arm variance mismatch; correlated A/B and C/D cell noise. Report whether the safety gates survive each; these inform (do not gate) registration unless a gate breaks.

## Deliverables
1. `oc_sim_v35.py` — the versioned simulator (pinned `/usr/bin/python3`, numpy 2.0.2; seeds declared in-file; deterministic).
2. `oc_results_v35.json` — per-scenario outputs with MC point + SE, per-gate pass/fail, the **compound six-cell power** number(s).
3. `OC_REPORT_v35.md` — human-readable: gate table, compound-power result, robustness-arm summary, and the exact numbers that populate v3.5's TBD cells.
4. `MANIFEST additions` — sha256 of the sim + results so the evidence is hash-tracked.
5. If compound power < 0.90 at n_rerun=56 → report the n_rerun that clears it (feeds a v3.6 micro-bump before registration).

## Out of scope
Registration itself (human-gated after this clears + P1/P2 + prereg re-issue). The frozen physics harness `v44_scout.py` (the sim calls the analysis path, does not edit harness bytes).

## Suggested execution
Delegate to Fable (medium/high effort) on the 9th with incremental writes + a tight per-scenario spec (Fable succeeded on the earlier OC sim with that pattern); HQ reviews the diff + re-verifies the compound-power number before it populates v3.5. Or a fresh Opus/Sonnet session with usage headroom.
