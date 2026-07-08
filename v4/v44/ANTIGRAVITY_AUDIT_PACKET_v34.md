# v4.4 Scout Decision Rule v3.4 — Adversarial Pre-Registration Audit Packet (for Antigravity)

*Issued by HQ (Temple of Two, Mac Studio Claude Code seat, provenance/final-say), 2026-07-08. Antigravity's lane is **adversarial arithmetic-mechanical + falsification audit, pre-registration** — you audit the rule BEFORE HQ registers it. No seat grades its own work: HQ drafted this, you break it. Precedent + deliverable format: your v4.3 analyzer audit (5 findings, 0 verdict impact, 1 real erratum) — `VERDICT_antigravity_audit_v43.md` in this folder.*

---

## 0. Your lane, and the stopping rule you must hold

You are the **adversarial arithmetic-mechanical + falsification** auditor. A separate **methodology** reviewer (ChatGPT Deep Research) has already reviewed v3.4 on the inferential/claim-scope lane. **Your lane is different and complementary — do not duplicate it.** Yours is:
1. **Re-derive every number from scratch** and confirm it reconciles with the prose (experimental law #4: prose thresholds must grep-match the frozen config).
2. **Confirm every gate and selftest can actually FAIL on null data** (law #2) and that positive controls can **PASS**, with **compound** power (all clauses jointly, by Monte-Carlo) ≥ 0.90 — NOT per-contrast analytic power (law #3: per-contrast power lied in v4.3, 0.998 vs 0.655 compound).
3. **Try to BREAK the rule** with a concrete configuration that yields a wrong outcome.

**Stopping-rule calibration (this is a hard requirement).** Render a **ratifiability verdict**, not an endless defect catalog. There are two symmetric failure modes and both are bad: approving something unsound, AND withholding approval forever by inventing one more hypothetical. A finite-threshold rule can always have *some* edge config built against it; that alone does not block. **It is correct to APPROVE a sound rule.**

## 1. Verdict rubric — classify each finding, render ONE terminal verdict
- **BLOCK** — a validity-breaking defect. Requires EITHER a **concrete failing config** (per-cell means, signs, SDs, T_c, coupling, block counts, seeds) where the rule outputs something false, OR a **stated number that provably does not reconcile** from the rule's own formulas. No such artifact → not a BLOCK.
- **REVISE** — a number to correct, a wording to tighten, a robustness/conservatism improvement that does not change a terminal verdict on real data.
- **APPROVE-level** — sound as written.

**Terminal verdict:** APPROVE / APPROVE-WITH-REVISIONS / BLOCK. BLOCK only if you produced ≥1 BLOCK-class artifact.

## 2. Your specific audit targets (attack these)

**A. Re-derive EVERY stated number independently** (`/usr/bin/python3`, numpy 2.0.2; reproduce, don't trust prose). Confirm each reconciles; flag any that does not:
- Detection floor `floor(B,sd) = (z_{0.995}+z_{0.90})·sd·√(2/B)` and the tabulated 0.682 / 0.557 / 0.482 at B = 64 / 96 / 128.
- Every band cutpoint at **16b/B96, 32b/B96, 32b/B128**: GREEN (one- and two-sided), the RED magnitude bound κ (one- and two-sided), ANOMALOUS edge. Confirm the four-band **partition = 1.0** and disjointness.
- χ² upper-SD inflation factors (1.797 / 1.437 / 1.268 at n = 8 / 16 / 32) and every Student-t critical value in the §2.2 table.
- **The powered-rerun block (§2.3/§8/§8-Ω): SE, significance edge, κ₄₀, AND the stated POWER of the rerun at ±1×floor(96).** Re-derive the power from the appropriate exact distribution (noncentral-t) using the rule's own effect size, SE, df, and critical value. Confirm the rule's power claim and the "powered dispositions ≥ 0.90" that gates 9/9Ω assert. If any power number does not reproduce, that is a REVISE-or-BLOCK-class non-reconciliation — report the exact value you get.
- The P2 equivalence band [0.909, 1.10] and every §13 operating-characteristic number.

**B. Gate failability + compound power** (laws #2/#3):
- For each hard gate: exhibit that it can FAIL on null data (not a rubber stamp).
- For each positive-control gate: confirm it can PASS, and that the **compound** power across all clauses jointly is ≥ 0.90 by Monte-Carlo — call out any place the doc asserts per-contrast power where compound is what matters.

**C. Prose ↔ config ↔ pseudocode consistency** (your v4.3 erratum class — docstring 24/32 vs config 48/64):
- Grep every prose threshold against the frozen config values.
- Confirm `band_cell()` / `pivot_licensed()` pseudocode actually implements what the prose claims: the shared primary-OR-omega ladder, the full-roster completeness assertions on every consumed dict, the omega + occupancy vetoes, and `INCONCLUSIVE_AT_CEILING` blocking.

**D. Adversarial falsification** — construct a config that yields a wrong outcome: an invalid pivot (real effect pivoted to a null), a false register, a mislabeled anomaly, a cell silently dropped from the pivot denominator, or an `INCONCLUSIVE` that should resolve. Probe **transduction inversion** (curl right, curl→current response inverted) and the **STABLE coupling** assumptions across the ρ ∈ {−1, 0, 0.5, 1, 2} arms.

## 3. The recurring category error — grep every null/RED/pivot claim against this
> A null/RED/pivot claim must bound the effect **MAGNITUDE** over the **WHOLE claimed object** — all directions, all statistics named in the claim, all cells in the denominator, all block-count LOOKS the guards depend on, all coupling regimes the guarantees are asserted over — never a projection or a silently-shrunk subset.

v3.4 claims it closed this on **five axes** (compute-ceiling, direction, statistic, cell-roster, look) plus recorded-statistic (occupancy) and coupling-regime (ρ≤0) extensions. **Test whether the closure actually holds** — can you still construct a config where a real effect escapes every guard and the rule mints a null? Guard: a rule that is *too conservative* (INCONCLUSIVE/blocks too readily) is REVISE-class, not BLOCK.

## 4. What changed v3 → v3.4 (the delta to audit)
D1 look-axis (shared secondary ladder + omega `INCONCLUSIVE_AT_CEILING` blocks), D2 omega sidedness (P1-A(ω) sign registration), D3 occupancy banded two-sided + GREEN veto, D4 powered §8-Ω omega/occupancy disposition (n_rerun=40), D5 full-roster dict assertions, D6 ρ≤0 coupling arms (transduction inversion), D7 all §9.3 gate expectations stated as recomputed. Confirm each is real in the text AND reconciles numerically.

## 5. The artifact (audit v3.4 directly)
Public draft branch (unreviewed by design):
`https://raw.githubusercontent.com/templetwo/entropy-as-tunable-equilibrium/v4.4-scout-draft/v4/v44/v44_scout_DECISION_RULE_v3.4.md`
Focus: §0 (adopted decisions), §2.2/§2.3 (thresholds + the rerun row), §3 (four-band rule), §4 (shared ladder), §5 (pivot conditions), §7 (`band_cell`/`pivot_licensed` pseudocode), §9 (OC-sim spec + hard gates), §13 (computed numbers). The `v44_scout.py` harness bytes are **frozen and NOT under review**.

## 6. Independence (important)
A methodology review of v3.4 exists in the repo (`REVIEW_VERDICT_CHATGPT_v34.md`). **Form your arithmetic-mechanical conclusions independently first — re-derive every number yourself before reading any prior verdict.** Where you and the other review converge on the same defect independently, that is strong triangulation; where you diverge, HQ arbitrates. Do not inherit conclusions; reproduce them or refute them.

## 7. Out of scope (do not block on these)
Registration (HQ + Anthony human-gated, after your verdict); the P1/P2 precondition *runs* themselves; the frozen artifacts (`v44_scout.py`, `prereg_v44.json`, `MANIFEST.sha256`).

## 8. Deliver back (match your v4.3 verdict format)
1. **Terminal verdict:** APPROVE / APPROVE-WITH-REVISIONS / BLOCK.
2. **Per-finding table:** each finding with class (BLOCK/REVISE), one-line summary, and the concrete artifact — a failing config with the wrong output, or the non-reconciling number with your re-derived value.
3. **Confirmations:** partition = 1.0 (yes/no + your check); which hard gates you verified can fail-on-null; whether the compound positive-control power ≥ 0.90 reproduces.
4. **One sentence** on whether the five-axis category-error closure holds.

Raw output only (NDJSON/markdown as you produced it) — HQ diffs and arbitrates. If you reach APPROVE or APPROVE-WITH-REVISIONS, say so plainly; a sound rule earns a clean approval.
