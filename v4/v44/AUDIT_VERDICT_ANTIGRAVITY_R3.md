# v4.4 Scout Pre-Registration Audit Report (Round 3) — Antigravity

**Audit Target:** v4.4 Movement 2 Scout Design and Decision Rules v3.4 (file `v44_scout_DECISION_RULE_v3.4.md`)  
**Auditor:** Antigravity (Google DeepMind, lab seat)  
**Verification Environment:** macOS, `/usr/bin/python3` (numpy 2.0.2)  
**Status:** Pre-Registration Audit Complete  

---

## Verdict: APPROVE WITH REVISIONS (RATIFIABLE)

We have conducted a thorough, adversarial arithmetic-mechanical audit of the pre-registration Decision Rule v3.4. All core mathematical cutpoints, detection floors, and partition boundaries are internally consistent and correct. The five-axis category-error closure holds.

The only required revisions concern the **rerun power formula discrepancy** (Finding 1): while the physical experiment achieves a power of **91.125%** (validating the claimed 0.912 and clearing the $\ge 0.90$ threshold), the standard noncentral-t formula used by ChatGPT and HQ assumes a non-scaled t-distribution, resulting in a lower nominal power of **85.75%**. We recommend either amending the text to document the scaled t-distribution of the test statistic or increasing $n_{rerun}$ to 56 to satisfy the naive formula.

Once this discrepancy is resolved/documented, the decision rule is fully ratifiable.

---

## Summary of Findings

| # | Finding | Severity | Verdict-Impact | Concrete Artifact / Non-Reconciliation |
|---|---|---|---|---|
| 1 | **Rerun Power Formula Discrepancy:** The text asserts a power of $0.912 \ge 0.90$ at $n_{rerun}=40$. Scipy's standard `nct` formula yields $0.8575$ (fails threshold), but the actual physical experiment yields $0.91125$ (passes) because the test statistic is scaled. | **REVISE** (Substantive) | Clears up discrepancy between naive formulas and physical simulation. | Stated: $0.912$; Naive `nct` formula: $0.8575$; Physical simulation: $0.91125$. |
| 2 | **Minor Notation Erratum in §9.3 Table:** The expected value cell for Gate 11 lists the $+3\times$ floor joint rate in the $+2\times$ row notes instead of formatting it as a separate sub-case. | **REVISE** (Minor) | Cosmetic consistency. | §9.3 table notation mismatch. |

---

## Detailed Findings

### Finding 1: Rerun Power Formula Discrepancy
*   **Severity:** **REVISE** (Substantive)
*   **Description:** 
    The v3.4 text asserts that the powered rerun at $n_{rerun}=40$ achieves a power of $0.912 \ge 0.90$ at an effect of $\pm 1 \times floor(96) = 0.55685\cdot sd$.
    However, the other audit reviews (ChatGPT and HQ) calculated the power using the naive formula:
    $$nc = \frac{\delta}{SE} = \frac{0.55685}{0.20156} = 2.7627, \quad t_{crit} = 1.68488, \quad df = 39$$
    and evaluated the cumulative density function of the standard noncentral-t distribution:
    $$P(T_{df=39, nc=2.7627} > 1.68488) \approx 0.8575$$
    This led them to believe the power was insufficient ($0.858 < 0.90$) and block/request revisions.
    
    **Our physical re-derivation proves that the physical power is indeed 91.125%.**
    The test statistic is:
    $$t = \frac{\bar{X}}{s \cdot \sqrt{1/40 + 1/64}}$$
    Because the rerun only runs the 40 blocks of the mismatch cell (no new equal-arm blocks are drawn in the precondition namespace), the true sampling variance of the numerator $\bar{X}$ is $\sigma^2 / 40$ (not $\sigma^2 \cdot (1/40 + 1/64)$).
    Since the standard error in the denominator is inflated by the constant $1/64$ reference variance, the test statistic is a scaled noncentral-t variable. When correctly scaled:
    *   Scaled critical value: $-2.1478$
    *   True noncentrality parameter: $-3.5219$
    *   True Physical Power: **91.125%** (verified by a $10^7$-run MC simulation)
*   **Concrete Fix:**
    To resolve the discrepancy between the text's analytic formulas and the physical experiment, the pre-registration should either:
    1. Keep $n_{rerun}=40$ and revise the text to explicitly document the scaled t-distribution and its $91.1\%$ physical power.
    2. Increase $n_{rerun}$ to **56** ($SE=0.1830\cdot sd$, $t_{crit}=1.673$) which achieves a nominal power of **91.3%** even under the naive unscaled noncentral-t formula.

---

## Confirmations

1.  **Partition Completeness Check:**
    *   **Partition = 1.0?** **Yes.** 
    *   *Verification:* We dense-scanned the real line for both one-sided and two-sided banding. The bands are mutually exclusive and collectively exhaustive. The transition boundaries (GREEN edge at $1.047\cdot sd$, RED κ edge at $0.067\cdot sd$, and ANOMALOUS edge at $-0.490\cdot sd$ at 16b) partition the domain with no gaps or overlaps.
2.  **Hard Gate Failability Check (Fail-on-Null):**
    *   **Gate 1 (any false GREEN):** Fails on null with $0.19\%$ joint probability.
    *   **Gate 2 (invalid pivot at $1\times$ floor):** Fails on null with $0.058\%$ joint probability.
    *   **Gate 5 (wrong-sign invalid pivot):** Fails on null with $0.06\%$ joint probability.
    *   **Gate 8 (omega escape):** Fails on null with $\approx 1.3 \times 10^{-11}$ probability.
    *   **Gate 11 (occupancy escape):** Fails on null with $\approx 1.4\times 10^{-5}$ probability.
3.  **Positive-Control Power Check:**
    *   **Gate 4 (compound GREEN power at $+3\times$ floor) $\ge 0.90$?** **Yes.** Evaluates to **0.9999**.
    *   **Gate 9/9Ω (powered rerun power at $\mp 1\times$ floor) $\ge 0.90$?** **Yes.** Evaluates to **0.912** physically.

---

## The Standing Rule Check

> **Does the five-axis category-error closure hold?**
> **Yes.** 

Every null or pivot claim in v3.4 bounds the effect magnitude ($|\hat{\mu}|$) over the whole claimed object (all cells, all statistics, all look-counts, all coupling regimes). The introduction of full-roster completeness checks on every dict prevents silent-shrinkage leaks, the shared ladder prevents look-throttling on the secondary statistics, and the $\rho \le 0$ coupling arms ensure the belt is tested in regimes where the suspenders are inert. No config can be constructed where a real effect escapes all guards.
