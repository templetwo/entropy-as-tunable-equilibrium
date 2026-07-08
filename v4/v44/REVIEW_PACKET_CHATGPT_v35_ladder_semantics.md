# v4.4 Scout — §4 Shared-Ladder Semantics: Narrow Adjudication (for ChatGPT)

*Prepared by HQ (Temple of Two, Mac Studio Claude Code seat). Hand this whole document to ChatGPT. It is self-contained. Nothing here is registered — registration is human-gated and waits for Anthony after your verdict.*

---

## 0. Your role, and the ONE question this packet exists to answer

You are the **external methodology reviewer**. You already reviewed v3 (BLOCK) and v3.4 (APPROVE-WITH-REVISIONS) of this decision rule, and arbitrated the n_rerun=40 rerun-power dispute. The rule is **ratified at v3.5**.

This is **not** a full re-review. It is a **single, surgical adjudication**. While building the registration-grade operating-characteristics (OC) simulator — the instrument of record that §9 always specified would *replace* the throwaway draft-check numbers currently in §13 — HQ hit a genuine ambiguity in the **§4 shared-ladder** semantics. The reading you pick changes the scout's operating characteristics materially. It is a **rule-interpretation + design-soundness** call, and Anthony asked for your read before HQ proceeds.

**Answer only this.** Do not re-litigate v3.5's ratified content. Do not hunt for new findings elsewhere. One question, adjudicated cleanly, is the entire deliverable.

---

## 1. Calibration — the valid answers (do not manufacture a defect, do not rubber-stamp)

This is a spec-interpretation question with a design-soundness rider. **All of the following are legitimate terminal answers** — pick the one the text and the methodology actually support:

- **Reading A is correct and sound** — §4 means the literal "single terminal rung," and re-banding the primary there is fine.
- **Reading A is what §4 literally says, but it is a design defect** — recommend a rule clarification to Reading B (or another fix). (This is the "the literal text produces a perverse result" answer.)
- **Reading B is the correct reading** — §4, read in full context, already means the primary keeps its earned band.
- **The distinction is immaterial** — both readings land the same verdict on real data; pick either and document it.

There is no pressure toward "block." There is no pressure toward "approve." Tell us which reading the rule *means*, and whether the literal reading is *sound*. If the honest answer is "the literal text is fine," say so plainly.

---

## 2. Context you need (brief)

- **What the scout is:** a signal-sizing *screening* pilot over a 6-cell (Δτ, T_c) sweep, three statistics per cell (`quad_loop_rate` = primary, `omega_roi` = secondary/veto, `occupancy_x` = recorded/veto). It ends in one of four honest outcomes: GREEN candidate / all-actual-RED pivot to a bounded raw-current null / anomaly-or-veto flag / INCONCLUSIVE at the compute ceiling. Outcome 4 (inconclusive) is a *designed, legitimate* result, not a failure.
- **What HQ found while building the OC sim (two things, the second is your question):**
  1. **A floor-scaling erratum (already logged, not your question, given for context).** The committed compound-power script `oc_sim_v35.py` (the 0.980 gate-9/9Ω number) froze the detection floor at sd=1, where §7's `band_cell` and the earlier reviewed `oc_simulation_v32.py` both scale it by the sample sd̂. Corrected, the compound is 0.940 (still ≥ 0.90; gate still passes; ratification untouched). Faithful re-derivation shifts §13's tail-rate numbers ~1.6–3.4×.
  2. **§13's numbers do not reproduce under any faithful reading of §4/§7 (your question).** §13 is explicitly a "throwaway draft-check, quarantined, not the instrument of record" (§13 line 624). Its per-cell "pivot-compatible ≈ 0.507" reproduces under **none** of four faithful variants (see §6). The residual, after the floor is corrected, is the **§4 shared-ladder ambiguity below.**

---

## 3. The §4 text under question (verbatim)

> **§4 — AMBER terminal rule + B_conf escalation → INCONCLUSIVE_AT_CEILING (SHARED ladder).**
> The ladder is driven by the primary AND the omega secondary. The terminal ladder, per cell, in order:
> 1. **One block-extension: 16 → 32 blocks** (accumulation). Taken iff the primary OR `omega_roi` is AMBER at 16b/B96 (exception: a primary GREEN or primary ANOMALOUS short-circuits the ladder … omega is stamped at that rung, an AMBER omega there recorded UNRESOLVED …).
> 2. **Still (primary OR omega) AMBER against floor(96) at 32 blocks → escalate B_conf 96 → 128** (re-band the same 32-block sample).
> 3. **Still AMBER against floor(128) at 32 blocks → `INCONCLUSIVE_AT_CEILING`** for whichever statistic(s) remain AMBER. B_max = 128.
>
> **All three statistics are stamped at the cell's single terminal rung** (one look of record per statistic per cell — the sim and `analyze()` share this one pinned rule, couple 7).

And couple 7 / the D1 hazard (§7): *"a sim that ladders omega while the run stamps it at the primary's terminal count certifies a veto the run does not implement"* — the pin exists to keep the sim and the live `analyze()` bit-identical.

---

## 4. The mechanics that make the reading matter (verbatim numbers)

`band_cell` (§7) uses an **sd̂-scaled floor** and an **sd̂-scaled SE**:

```
floor_c(sd) = 3.858 · sd · sqrt(2 / B_conf)
SE(sd)      = sd · sqrt(1/n + 1/64)          # reference-uncertain estimand
RED ⇔ |μ̂| + t·SE(sd̂) < floor_c(sd̂)  AND  |μ̂| + t·SE(sd_up) < floor_c(sd_up)  AND not ANOMALOUS
```

The frozen floor/cutpoint table (§2.3), two-sided:

| rung | (n, B_conf) | floor_c(sd=1) | two-sided RED κ = floor − t·SE |
|---|---|---|---|
| 16b/B96 | (16, 96)  | 0.557 | **−0.039 → RED UNREACHABLE** |
| 32b/B96 | (32, 96)  | 0.557 | **+0.115** |
| 32b/B128 (ceiling) | (32, 128) | **0.482** | **+0.040** |

**The crux:** escalating B_conf 96 → 128 *lowers* the floor (0.557 → 0.482), so the RED region *shrinks* (κ 0.115 → 0.040). A cell that is confidently RED at 32b/B96 (|μ̂| between 0.040 and 0.115) becomes AMBER at 32b/B128 — i.e. `INCONCLUSIVE_AT_CEILING`.

Now the ambiguity. Suppose at 32b/B96 the **primary is RED** but **omega is still AMBER**. Step 2 says "(primary OR omega) AMBER → escalate," so the cell escalates to B128 on omega's account. What happens to the primary?

- **Reading A (literal "single terminal rung"):** the terminal rung is now 32b/B128; **all three statistics are re-stamped there**; the primary is re-banded at B128 and — if 0.040 < |μ̂| < 0.115 — **loses its RED and becomes INCONCLUSIVE.** An omega-driven escalation can un-RED a primary that already cleared its own RED bound.
- **Reading B (primary keeps its earned terminal band):** each statistic locks the first rung at which *it* reaches a terminal band; omega continues laddering for its own veto, but a primary that REDs at 32b/B96 **stays RED**. "Single terminal rung" is read as "one look of record per statistic," per-statistic, not one shared rung for all three.

---

## 5. The evidence (why this is not the floor bug, and what each reading costs)

Faithful re-implementation of §4/§7 (canonical interpreter, N ≥ 1e6), per-cell terminal primary-RED under a global two-sided null:

| ladder reading | faithful sd̂-floor | fixed floor (the erratum) |
|---|---|---|
| **A** (re-band primary at single terminal rung) | 0.316 | 0.051 |
| **B** (primary keeps earned RED) | 0.402 | 0.105 |

§13's throwaway draft-check per-cell "pivot-compatible" = **0.507** — reproduces under **none** of the four. So §13 used yet another (unrecoverable; its script is gone) model, and the live question is A vs B, both *below* §13.

**Operating-point consequence** (this is the design-soundness rider): pivot-to-null ≈ (per-cell pivot-compatible)^6 over the six cells. Under Reading A the correct-pivot-under-null rate is ≈ **0.0002**; §13's draft-check claimed ≈ **0.017** (≈100× higher). Reading B is higher than A but still ≪ 0.017. **Under either faithful reading the scout mints a clean bounded-null pivot far more rarely than the draft-check implied — it will predominantly return INCONCLUSIVE_AT_CEILING** (a legitimate outcome-4 bound), unless a real signal is present.

**Safety direction (please confirm the reasoning):** both readings give *lower* pivot rates than the draft-check. The hard safety gates bound *invalid* pivots (a real/wrong-sign effect pivoted away to a null). A rule that pivots *less* readily makes those gates *easier* to pass. So the correction cannot threaten registrability on the safety axis — it only reduces the scout's *power to deliver a clean null* (an advisory operating characteristic, §9.3 fork 2). Is that reasoning sound?

---

## 6. What to deliver back (exact shape)

1. **The §4 reading:** A / B / immaterial — which does the rule *mean*, and (if A) is the literal reading **sound** or a **defect to clarify**? Cite the text you're relying on.
2. **The perversity check:** is it methodologically acceptable for an **omega-driven B96→B128 escalation to un-RED a primary that already cleared its own RED bound** (Reading A), or should a primary's earned RED be sticky (Reading B)? One-paragraph rationale.
3. **Operating point:** is a screening pilot that predominantly returns INCONCLUSIVE (rarely a clean null pivot) methodologically acceptable as-is, or does the operating point need adjustment before registration? (This is advisory-class, i.e. a power/design concern, not a validity defect — flag it as such.)
4. **Safety confirmation:** one sentence — does the "both readings are safer than the draft-check, so registrability is not threatened" argument hold?

---

## 7. Out of scope (do not block or opine on these)

- **Registration** — Anthony's human-gated call after your verdict. Your read is an input, not the trigger.
- **The floor-scaling erratum** — already found, logged, and corrected by HQ; given only as context for why §13 doesn't reproduce. Not your question.
- **Frozen artifacts** (`v44_scout.py`, `prereg_v44.json`, `MANIFEST.sha256`) and preconditions P1/P2 — not under review here.
- The full v3.5 rule (for context; the §4 text you need is quoted verbatim above):
  `https://raw.githubusercontent.com/templetwo/entropy-as-tunable-equilibrium/v4.4-scout-draft/v4/v44/v44_scout_DECISION_RULE_v3.5.md`

*One clean adjudication of the §4 reading is the whole job. Nothing here is registered.*
