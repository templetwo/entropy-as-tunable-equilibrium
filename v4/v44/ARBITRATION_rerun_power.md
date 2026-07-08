# HQ Arbitration — rerun-power contradiction (ChatGPT/HQ 0.858 vs Antigravity 0.911)

*HQ (Mac Studio Claude Code seat, arbiter/final-say), 2026-07-08. Two external reviewers of v4.4 scout v3.4 reached opposite conclusions on ONE load-bearing number: the power of the powered rerun (n_rerun=40) to detect a wrong-sign current at 1×floor(96)=0.55685·sd. This file records HQ's resolution. NOT registered. A verification workflow (independent MC + textual adjudication + adversarial steelman of Antigravity) is confirming in parallel; this document stands on the decisive evidence already in hand.*

## The contradiction
- **ChatGPT + HQ:** power ≈ **0.858** — noncentral-t, ncp = δ/SE = 0.55685/0.2016 = 2.763, crit t₃₉=1.685, SE = sd·√(1/40+1/64). Flagged as an inflated claim (rule says 0.912).
- **Antigravity (R3):** power ≈ **0.911** — argues the rerun redraws only the 40 mismatch blocks (no new equal-arm blocks), so the numerator's true variance is sd²/40 (numerator SD = sd/√40 = 0.1581), a "scaled noncentral-t"; 10⁷-run MC gives 0.91125.

## HQ resolution: **the honest, preregisterable power is 0.858. ChatGPT/HQ are correct.**

### Decisive MC (`/usr/bin/python3`, numpy 2.0.2, N=5×10⁶, seed 20260708)
End-to-end simulation of the rerun as a t-test (sd estimated from the 40 blocks), true wrong-sign current δ = −0.55685·sd:

| model | rerun power | H0 one-sided α (true current = 0) |
|---|---|---|
| reference UNCERTAIN — draw a fresh finite 64-block reference each rep | **0.8576** | **0.0496** (calibrated at 0.05 ✓) |
| reference PERFECT — reference = exact true value, zero error (Antigravity) | 0.9112 | 0.0188 (conservative ✗) |

**The entire 0.858↔0.911 gap is one thing: whether the finite 64-block reference's own σ²/64 uncertainty is counted.**

### Why Antigravity's 0.911 is not the honest guarantee — two independent proofs
1. **Conditional vs marginal power.** The equal-arm reference c is a realized estimate from 64 blocks: c = μ_eq + ε, ε ~ N(0, σ²/64), fixed-but-unknown. In the rerun μ̂ = M̄ − c, so μ̂ ~ N(δ − ε, σ²/40). Antigravity computes power **conditional on ε = 0** (a perfect reference): Φ((0.217)·√40) = 0.915. The honest **marginal** power over ε ~ N(0, σ²/64) is Φ(1.372/√(1+(6.325·0.125)²)) = Φ(1.076) = **0.858**. A preregistered "≥0.90 power" guarantee must use the marginal power — you cannot assume your one frozen reference happened to be exact.
2. **The α-tell (dispositive).** The rule's rejection edge (0.340·sd) is calibrated to α=0.05 **using SE = sd·√(1/40+1/64)**. If the numerator's true SD were sd/√40 (Antigravity's assumption), the test's actual false-positive rate is **α = 0.0188, not 0.05** (MC above). So Antigravity's "0.911" is the power of a *more conservative* test running at α≈0.019 — not comparable to a 0.05-level guarantee. Critically, Antigravity's OWN confirmations (partition = 1.0, every gate's fail-on-null rate) were computed with the SE-based thresholds, i.e. it used the reference-uncertain model **everywhere except this one power calc**. Its verdict is internally inconsistent: if sd/√40 were the true numerator SD, every cutpoint and gate rate it just certified would also be miscalibrated.

**Antigravity's error, stated fairly:** it did a real, careful derivation, but computed the rerun power *conditional on an error-free frozen reference*, dropping the σ²/64 reference uncertainty from the numerator's true (marginal) variance while keeping it in the denominator SE. That yields the best-case conditional power (0.911), not the honest preregisterable marginal power (0.858).

## Convergent fix (both reviewers agree): **n_rerun = 56**
Independently of who is right on the 40-block framing, both ChatGPT/HQ and Antigravity offer **n_rerun = 56** as a clean resolution (SE=0.1830·sd, t₅₅=1.673 → power 0.913 under the honest noncentral-t). v3.5 will:
1. Bump **n_rerun 40 → 56** in §2.2/§2.3/§8/§8-Ω (t df 39 → 55) and recompute §13 power numbers with the honest (reference-uncertain) noncentral-t.
2. Correct the §13 power prose (0.912 → the honest value) and add the compound-power MC (law #3), not per-contrast.
3. Fix the §9.3 Gate-11 notation erratum (Antigravity Finding 2, minor).

## Antigravity R3 — the rest of the audit (accepted)
Antigravity's non-power findings are accepted and strengthen confidence: partition = 1.0 (dense-scan), every hard gate demonstrably fails-on-null (Gate1 0.19% / Gate2 0.058% / Gate5 0.06% / Gate8 1.3e-11 / Gate11 1.4e-5), compound GREEN power 0.9999, five-axis category-error closure holds, no config found where a real effect escapes all guards. Verdict: APPROVE-WITH-REVISIONS — matching ChatGPT. Raw deliverable preserved at `AUDIT_VERDICT_ANTIGRAVITY_R3.md`.

## VERIFICATION WORKFLOW — CONFIRMED (4 independent agents, unanimous)
A parallel workflow (run wf_4b51ba95) independently re-derived this. All four agents converge on **0.858 = honest, ChatGPT/HQ correct**:
- **Textual/semantic:** the rule uses SE=sd·√(1/40+1/64) to set both cutpoints and the α=0.05 gate calibration; §2.1 declares it "folds in the 64-block reference." Reference-uncertain is the only model consistent with the rule's own α (nominal α=0.04999); 0.912 is an erratum vs the rule's estimand.
- **Independent MC** (fresh code, seed 20260701, N=3×10⁶): power_uncertain=0.858 (α=0.0500 ✓), power_perfect=0.9115 (α=0.0189 ✗). Reproduces the noncentral-t to 3 decimals.
- **Adversarial steelman of Antigravity** (tasked to prove HQ wrong): Antigravity's 0.911 **not defensible**. Sharpened the diagnosis — **0.911 is a "chimera": it uses the reference-perfect numerator SD (0.1581) with the reference-uncertain rejection edge (0.340, derived from the inflated SE).** A self-consistent fixed-reference test at α=0.05 would use edge 0.266 → power 0.967; the honest α=0.05 test uses edge 0.340 → power 0.858. 0.911 is the power of a test actually running at α≈0.019. "Not redrawn is not error-free"; the fresh 40 blocks are independent of the reference error ε, so the variances add to SE².
- **Arbiter:** honest power 0.858; and note 0.858 is only the **per-contrast** figure and fails law #3 (≥0.90) → v3.5 must raise n_rerun to ≥56 (n=56→0.913 per-contrast, n=50→0.897 misses) **and re-verify the COMPOUND six-cell power ≥0.90 by Monte-Carlo before registration** (not per-contrast).

## Net pipeline state
Both external reviews return **APPROVE-WITH-REVISIONS**, converging on the same rule as sound. The one load-bearing dispute (rerun power) is HQ-resolved: honest power 0.858, fix = n_rerun 56. Consolidated **v3.5** = power fix + Gate-11 notation + the agreed REVISE items from both reviews → Anthony final-say → register. NOT registered; no frozen bytes touched.
