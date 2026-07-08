# v4.4 Scout Decision Rule v3.4 — External Methodology Review Packet (for ChatGPT)

*Prepared by HQ (Temple of Two, Mac Studio Claude Code seat) for external methodology re-review. Hand this whole document to ChatGPT. It is self-contained. Nothing here is registered — registration is human-gated and waits for Anthony after your verdict.*

---

## 0. Your role, and the ONE thing this packet exists to prevent

You are the **external methodology reviewer**. You already reviewed **v3** of this decision rule and issued a BLOCK across your questions Q1–Q7. This is the **re-review of v3.4**, which was drafted to clear that block and then hardened through three further independent internal passes.

Your job is to render a **ratifiability verdict** — not to maximize the number of findings.

**Hold this calibration. It is the reason this packet was written.** There are two symmetric failure modes:

- **Under-review:** approving a rule that mints a scientific claim the data does not earn.
- **Over-review:** withholding approval from a *sound* rule by perpetually surfacing "one more" hypothetical refinement.

A finite-threshold decision rule can **always** have some edge configuration constructed against it. Treating every such construction as blocking makes approval mathematically unreachable — and that is itself a failure we are explicitly guarding against. Our internal reviewers were adversarially prompted to "find the next costume of the error," and by construction they never hit zero findings. That is expected and does **not** mean the rule is unsound.

**It is OK — indeed it is the correct outcome — to APPROVE a methodologically sound rule.** "This is good enough to ratify" is a real, valid verdict. Do not confuse "I can imagine a further refinement" with "this rule is invalid."

---

## 1. Verdict rubric — classify each finding, then render ONE terminal verdict

Classify **every** issue you raise into exactly one class:

- **BLOCK** — a *validity-breaking* defect. You must supply a **concrete failing configuration** (per-cell means, signs, SDs, T_c, coupling, block counts) under which the rule **mints a claim the data does not earn**: a real effect pivoted away to a null, a false register, a mislabeled anomaly, a silently-shrunk claim denominator, or a gate whose power is too low to catch a live effect it asserts is absent. If you cannot exhibit an input where the rule outputs something *false*, it is not a BLOCK.
- **REVISE** — a clarity, robustness, or conservatism improvement that **does not change any terminal verdict on real data**. Tighten wording, add a caveat, document an assumption, name a number. The rule is still valid without it. (A finding that the rule is *too conservative* — blocks or goes INCONCLUSIVE too readily — is REVISE-class at most: over-conservatism costs power, it does not mint a false claim.)
- **APPROVE-level** — no defect; the disposition is sound as written.

**Then render exactly one terminal verdict:**
- **APPROVE** — sound for its stated purpose; residual items are REVISE-class or below.
- **APPROVE-WITH-REVISIONS** — sound; list the REVISE items you'd like folded in, but they do not gate ratification.
- **BLOCK** — you produced **at least one BLOCK-class finding with a concrete failing config**. Name it explicitly.

If your findings are all REVISE-class, the correct terminal verdict is **APPROVE** or **APPROVE-WITH-REVISIONS**, not BLOCK.

---

## 2. What the rule IS (judge it against THIS purpose, not a grander one)

The v4.4 scout is a **signal-sizing pilot**. It sizes the realized anisotropic-horizon current across a 6-cell (Δτ, T_c) sweep. It is a **screening/triage** instrument, not a confirmatory contrast test.

It is designed so it **cannot fail** — it always ends in exactly one of four honest terminal outcomes:
1. **GREEN candidate** → register a Movement-3 two-sample contrast (no pivot).
2. **All-actual-RED pivot** → a bounded **raw-current null** over the surviving design points (NOT a contrast claim, NOT a continuum claim, NOT a claim about any other statistic).
3. **Anomaly / veto flag** → investigate (powered disposition), no pivot.
4. **Inconclusive at the compute ceiling** → an honest bound, not a null, not a failure.

Judge whether the rule's dispositions are **valid for this screening purpose**. Do not hold it to the standard of a confirmatory experiment — that is Movement 3, explicitly downstream and out of scope.

---

## 3. The standing test to apply — the recurring category error (with its guard)

The one error this program keeps making, in new costumes: **a bound on one direction / one statistic / a subset of cells asserted as a null over the WHOLE claimed object.**

Grep every null / RED / pivot claim against this sentence:

> A null/RED/pivot claim must bound the effect **MAGNITUDE** over the **WHOLE claimed object** — all directions, all statistics *named in the claim*, all cells *in the claim denominator* — never a projection or a silently-shrunk subset.

v3.4 states it has closed this on **five axes** (compute-ceiling, direction/wrong-sign, statistic, cell-roster, and the "look" axis) plus two recorded-statistic/coupling-regime extensions. **Your highest-value work is to test whether that closure actually holds** — can you still construct a config where a real effect escapes the guards and the rule mints a null? If yes → BLOCK with the config. If you can only argue "it could be even more thorough" → REVISE.

**Guard:** a finding that the rule is *too conservative* (e.g., it goes INCONCLUSIVE or blocks the pivot more often than strictly necessary) is **not** a BLOCK — the pilot honestly reporting "inconclusive" is a designed, safe outcome.

---

## 4. What changed v3 → v3.4 (re-review against your OWN prior verdict, not from scratch)

Your v3 review is the baseline. Check that each is genuinely resolved:
- **Q3 (RED robustness under sd uncertainty)** — you PASSED it at v3; the coupled-upper conjunction + magnitude bound is retained verbatim. Confirm it still holds.
- **Q4 (compute-ceiling laundered into a null)** — fixed: `INCONCLUSIVE_AT_CEILING` now blocks the pivot instead of counting as RED.
- **Direction axis** — fixed: RED now bounds `|μ̂|` (magnitude), not just the sign-aligned component.
- **Statistic axis** — the pivot claim is scoped to `quad_loop_rate`; `omega_roi` carries a pivot veto on a shared secondary ladder; `occupancy_x` (the statistic that carried v4.3's only confirmed effect) is now banded two-sided with a GREEN veto.
- **Cell-roster + dict-denominator axes** — the claim shrinks to surviving design points on demotion, and `pivot_licensed()` asserts full-roster coverage on every consumed dict.
- **Coupling-regime** — the STABLE-gate sweep now includes ρ ≤ 0 (transduction inversion), where the rule states the magnitude bound (the "belt") is the sole guarantee.
- **Powered dispositions** — anomaly reband tests are pinned at n_rerun = 40 (power ≥ 0.90) for both the primary and omega.
- Every hard-gate expected value is stated as **computed** (Monte Carlo, named seeds), not asserted.

If any of these is not actually resolved by the text → BLOCK with the config. If resolved but improvable → REVISE.

---

## 5. The artifact to review

Full v3.4 decision rule (public draft branch, unreviewed by design):
`https://raw.githubusercontent.com/templetwo/entropy-as-tunable-equilibrium/v4.4-scout-draft/v4/v44/v44_scout_DECISION_RULE_v3.4.md`

(Human-readable view: same path with `/blob/` instead of `/raw/`.) Read §0 (adopted decisions), §3 (four-band rule), §5 (pivot conditions), §7 (`band_cell` / `pivot_licensed` pseudocode), §9 (the operating-characteristics simulation), §13 (the computed gate numbers). The `v44_scout.py` harness bytes are **frozen and NOT under review** — you are reviewing the decision rule, not the physics path.

---

## 6. Out of scope for you (do not block on these)

- **Registration.** You do not register anything. Registration is Anthony's human-gated call after your verdict + the Antigravity re-audit. Your verdict is an input, not the trigger.
- **Preconditions P1/P2.** The sign-registration and T_c×M gate runs are separate diagnostics that complete before the scout; you may flag their design but they are not the decision rule.
- **Frozen artifacts** (`v44_scout.py`, `prereg_v44.json`, `MANIFEST.sha256`). Not editable, not under review.

---

## 7. Deliver back (exact shape)

1. **Terminal verdict:** APPROVE / APPROVE-WITH-REVISIONS / BLOCK.
2. **Per-finding table:** each finding with its class (BLOCK / REVISE), a one-line summary, and — for every BLOCK — the concrete failing configuration and the wrong output it produces.
3. **One sentence** on whether the five-axis closure of the category error holds.

If you reach APPROVE or APPROVE-WITH-REVISIONS, say so plainly. A sound rule deserves a clean approval, and rendering one is doing your job correctly.
