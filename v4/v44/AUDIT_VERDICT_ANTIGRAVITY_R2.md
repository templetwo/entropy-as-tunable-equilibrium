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
