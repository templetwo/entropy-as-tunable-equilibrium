# v4.3 Analyzer Audit Verdict — Antigravity (Part B)

HQ verified each of the 5 reported findings against the registered artifact
(v43_harness.py, source_sha 1b950383ae012431; prereg_v43.json), 2026-07-06.

| # | Finding | Verified? | Impact on registered results |
|---|---------|-----------|------------------------------|
| 1 | `block_perm_p` ternary `(v>=obs) if not one_sided else (v>=obs)` — both branches identical, `one_sided` param dead (L776) | **Confirmed** | **None.** Sidedness is encoded in each stat function (abs() = two-sided, signed = one-sided upper); every call site audited, all correct. Cosmetic; parameter should be removed in v4.4. |
| 2 | Plaquette circulation stencil in `CurrentAcc`/`run_gyrator` geometrically unconventional | **Partially fair** | **None.** Corner-sampled rotational stencil is a valid (if nonstandard) circulation proxy; it gates nothing in v4.3 — C0 gates on `ang_mom_rate`, the registered current statistic is `QuadrantLoop`. Descriptive fields only. |
| 3 | Docstring says G2 sign consistency "24/32" (L72) while config (`sign_consistency_aniso: 48`), the registered `outcome_map` ("48/64"), and the analyzer code all use 48/64 | **Confirmed — the real catch** | **None on inference** (analysis ran at the correct, stricter 48/64; stale prose predates the pilot-driven B=64 bump). But it is an internal inconsistency inside a hash-anchored registered artifact. Erratum recorded here; artifact cannot be edited (hash-frozen). v4.4 rule: grep-check prose/config agreement in selftest. |
| 4 | Mixed centering in G2: sign consistency counts blocks about zero; opposite-signs check centers on the equal-arm mean | **Confirmed** (design note) | **None here** — equal-arm mean (−2.7e-6) is ~0 vs block sd (5.4e-5). Under a large common winding background the two clauses could disagree. v4.4: center both on the equal-arm mean. |
| 5 | `perm_p` (pooled-KS helper) defined, never invoked | **Confirmed** | **None.** v4.2 leftover; v4.3 dropped the pooled KS path. Dead code; remove in v4.4. |

**Bottom line: 5/5 findings are real observations; 0/5 alter any registered
verdict.** G1 pass / G3 bounded null stand. Findings 3 and 4 are genuine
blemishes carried forward as registered v4.4 design rules. The gates survived
adversarial audit by a fourth independent seat.

Analyzer audit: Antigravity (Google, Gemini 3.5 Flash). Verification: HQ.
