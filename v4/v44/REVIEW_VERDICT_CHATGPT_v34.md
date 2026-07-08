# v4.4 Scout v3.4 — ChatGPT Deep Research Verdict + HQ Verification

*HQ (Mac Studio Claude Code seat, arbiter/provenance), 2026-07-08. ChatGPT ran a Deep Research methodology re-review of v3.4 using `REVIEW_PACKET_CHATGPT_v34.md`. Source review: iCloud `Tier 27/V4/deep-research-report.md` (2026-07-08 08:41 EDT). This file records ChatGPT's terminal verdict and HQ's independent verification of the one load-bearing quantitative finding. NOT registered — registration waits for Anthony after the Antigravity audit + a consolidated revision.*

## ChatGPT terminal verdict: **APPROVE WITH SUBSTANTIVE REVISIONS — not a BLOCK**

The packet's calibration worked as designed: a real defect surfaced, no perfectionist spin, a clean terminal verdict. ChatGPT's read: the five-axis whole-object closure "mostly does hold on the face of the v3.4 text" — the v3.3 omega-look bug is genuinely repaired, the cell-denominator leak is addressed, occupancy is now guarded. It found **one** quantitative inconsistency (classed correction-required / REVISE, not fatal) plus a set of REVISE-class robustness/evidence items.

## THE ONE LOAD-BEARING FINDING — HQ-VERIFIED (must-fix before ratification)

**Claim in v3.4:** the powered rerun at `n_rerun = 40` achieves **power 0.912 ≥ 0.90** at ±1×floor(96) (§2.2/§2.3/§8/§8-Ω/§13; gates 9 & 9Ω assert "powered dispositions").

**ChatGPT:** recomputing from the rule's OWN numbers (effect 0.557·sd, SE 0.2016·sd, t₃₉=1.685) via noncentral-t gives ≈0.86, below the ≥0.90 guarantee.

**HQ independent verification (`/usr/bin/python3`, three methods, seed 20260708):**
| method | power |
|---|---|
| normal approx Φ(ncp−crit), ncp=2.763, crit=1.685 | 0.8595 |
| scipy noncentral-t, P(nct(df=39, nc=2.763) > 1.685) | 0.8576 |
| Monte-Carlo noncentral-t, N=4×10⁶ | 0.8575 ± 0.0002 |

**CONFIRMED: true per-rerun power ≈ 0.858, not 0.912.** The claimed number is inflated by ~0.055 and does NOT meet the ≥0.90 the gates assert. This is the exact class of error experimental law #3 exists to catch (analytic per-contrast power lied in v4.3: 0.998 claimed vs 0.655 compound). ChatGPT's Deep Research caught a fresh instance; HQ verified it.

**Fix (known, mechanical) — n_rerun needed for power ≥ 0.90 at effect = floor(96):**
| n_rerun | SE=sd·√(1/n+1/64) | t_{n−1,.95} | power |
|---|---|---|---|
| 40 | 0.2016 | 1.685 | 0.858 |
| 48 | 0.1909 | 1.678 | 0.891 (short) |
| **56** | **0.1830** | **1.673** | **0.913 (clears)** |
| 64 | 0.1768 | 1.669 | 0.930 (margin) |

**Correction touches:** §2.2 t-table (df 39 → 55 or 63), §2.3 rerun row (SE, significance edge, κ₄₀), §8/§8-Ω (n_rerun 40 → 56/64), gates 9/9Ω prose, §13 power numbers. And per law #3 the disposition's **compound** power (all clauses jointly) must be Monte-Carlo'd, not asserted per-contrast. Does NOT materially threaten gate 5 (invalid-pivot) or gate 8 (omega escape) — those don't hinge on the rerun power — but the "powered ≥0.90" LABEL is currently false and must be corrected.

## REVISE-class items (fold into the consolidated revision; none block)
1. **[Highest]** Correct the n_rerun power (above) with an explicitly specified exact method; update gates 9/9Ω + dependent arithmetic.
2. **[Highest]** Promote the §9 OC simulator from scratch draft-check script to a **registration-grade versioned artifact** (pinned code, seeds, hashes, scenario outputs with Monte-Carlo SEs). *(Aligns with our own standing plan — registration-grade OC sim is the next build phase.)*
3. **[High]** Robustness arms: non-Gaussian / heavy-tail / heteroscedastic equal-arm mismatch / correlated A/B & C/D noise.
4. **[High]** Methods appendix citing external basis (t thresholds, χ² SD inflation, TOST/equivalence, bootstrap CI choice, simulation-based adaptive calibration).
5. **[High]** Justify the percentile-bootstrap choice and the [0.909, 1.10] P2 equivalence band (or compare alternatives).
6. **[Medium]** Stress-test the STABLE threshold at 11/12/13/14-of-16, incl. the ρ≤0 arms.
7. **[Medium]** Formal sensitivity branch making occupancy symmetric with omega; quantify cost/benefit vs the current asymmetry.
8. **[Medium]** Replace "cannot fail" with narrower language ("cannot deadlock" / "always returns one predeclared disposition under the stated model"). *(Claim hygiene — matches law #8 discipline.)*
9. **[Medium]** Surface internal empirical anchors (receipt-06/07, v4.3 occupancy precedent) as appendices/linked exhibits so the ratification packet is self-supporting.

## HQ disposition + recommended sequence
- The power erratum is **must-fix-before-ratification** (law #3 nerve). Verified; fix is a bounded mechanical correction (n_rerun → ~56 + recompute + compound-power MC).
- Everything else is fold-in revision; several match our own known next-build items.
- **Sequence:** (1) [done] record this verified verdict. (2) Run the Antigravity pre-reg audit (prep its packet next). (3) Consolidated **v3.5** = power fix + agreed REVISE items from BOTH reviews → this is the ratification candidate. (4) Anthony final-say → register. Heavy drafting waits for Fable reset (9th) or HQ drafts the mechanical power fix directly.
- NOT registered. No frozen bytes touched.
