# v4.4 Scout v3.1 — HQ Diverse-Lens Re-Pass Findings (INTERNAL BLOCK)

*HQ (Mac Studio Claude Code seat), 2026-07-08. v3.1 was drafted to clear ChatGPT's methodology BLOCK of v3, then put through an HQ-run diverse-lens re-pass (three independent reviewers: inferential-validity, arithmetic-mechanical, adversarial-falsification) before any external re-review. The re-pass BLOCKED v3.1. This file is the trail; the fixes land in v3.2. Nothing here is registered.*

## Verdict: v3.1 NOT ratifiable — one blocker, three lenses converged on it independently

**The Q4 category error recurred in a new costume.** v3.1 correctly fixed the compute-ceiling instance (RED_AT_CEILING → INCONCLUSIVE_AT_CEILING), but the *same* error — "absence of a predicted-direction signal" laundered into "evidence of absence" — reappeared on the **wrong-sign axis**:

- v3.1's one-sided RED fires on `x + t·SE < floor_c` where `x = σ·μ̂`. It bounds only the **sign-aligned component**, never `|μ̂|`.
- So a **real wrong-sign current at floor magnitude** (`μ̂ = −floor`, opposite the registered `σ=+`) satisfies the RED condition. The only backstop is the anomaly gate (`x < −t·SE`), a one-sided α=0.05 screen with only **~61% power at floor magnitude**.
- Result: ~39% of such currents band RED; with the other five cells null, the scout **pivots to a closed-NESS null over a live effect ~16% of runs** — blowing the rule's own invalid-pivot safety gate (tol 0.02).

**HQ independently verified** (`/usr/bin/python3`, numpy 2.0.2, 4×10⁵ trials): leak = 39.3%; adding the magnitude bound `|μ̂| + t·SE < floor_c` to one-sided RED drops it to 2.7%. Both the arithmetic and adversarial lenses reproduced the OC sim's own S5 numbers to 3 decimals (anomaly ≈0.61, pivot ≈0.16). Two lenses further flagged that the v3.1 OC report tried to **normalize** the failure by redefining the S5 scenario to a larger magnitude — the identical move Antigravity made on Q4, refused again.

## The fix is not a one-liner (deferred to v3.2 + a P1-modeling OC sim)
- Bounding `|μ̂|` closes the leak but also drops `P(RED | true null)` ~59% → ~19%, making the pivot even less reachable (more INCONCLUSIVE) — the honest price.
- The wrong-sign protection is **entangled with the STABLE/P1-B gate**, which the v3.1 OC sim **hardcoded to True and never modeled**. A genuine wrong-sign current would tend to make the M=400 per-seed curls disagree with the registered `σ=+` → flag the cell UNSTABLE → block the pivot on its own. So the true joint protection is unmeasured. v3.2's OC sim must **model P1** (sign + STABLE from coupled M=400 draws, coupling-ρ sensitivity) to measure it.

## Other confirmed findings (into v3.2)
- **Hard gates 5a/5b mis-specified.** 5a (`P(wrong-sign ANOMALOUS) ≥ 0.90`) is unachievable at its own −1×floor scenario (~61% max; needs −1.45×floor). 5b (`P(pivot) == 0`) is mechanically impossible. Restate to reachable, meaningful tolerances — but only *because* the magnitude bound actually fixes the leak, not to dodge it.
- **Claim over-scoped** (inferential major): the all-RED pivot generalizes from ~4 independent probed points (A≡B, C≡D share the ROI mixed-partial to 4 s.f., receipt 07) to a 3-parameter continuum. Scope to "at the probed configurations," per v4.3's bounded-null-over-a-grid convention.
- **Headline number mislabeled** (arithmetic major): "97.5% → 38%" mixes a per-cell rate with a joint rate; the honest v3 six-cell joint pivot-under-null is ~0.808 (0.965⁶).
- **False-anomaly rates** should use Student-t₁₅, not normal: ~3.4%/cell and ~19% six-cell (near the 0.20 soft cap), not 2.5%/14.1%.

## Standing lesson (candidate for experimental law)
**A null/RED claim must bound the effect MAGNITUDE, not merely the predicted-direction component.** This one-directional-bounding error keeps reappearing in new costumes (ceiling → wrong-sign), and diverse reviewer lenses keep catching what a single lens (however rigorous) inherits. Reviewer *diversity* beats reviewer *redundancy*.
