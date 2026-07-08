# v4.4 Scout Decision-Rule v3 — Methodology Review Verdict — ChatGPT

**Provenance note (HQ):** received 2026-07-07 ~21:00 EDT via Anthony's paste from the ChatGPT seat (chat transport; that seat produces no file artifact and cannot access the repo). Review target was `CHATGPT_REVIEW_PACKET_v3.md` (commit `e8e1f51`), i.e. the full v3 spec + both Antigravity verdicts inlined byte-faithful. Text below is as received; formatting is the paste's own. HQ reconciliation is chronicled separately and lands in the v3.1 revision, not in this file — external seat output stays unmixed (law #7).

---

Methodology review — v4.4 Movement 2 Scout decision-rule v3

I reviewed the inlined v3 rule as the target, not the earlier v2 material or the byte-verification lane. The repaired band partition and the RED-direction correction are sound. The remaining blocker is in the terminal ladder: an AMBER result at the declared compute ceiling cannot become evidence for RED merely because more compute is not authorized.

Question    Disposition    Review finding
Q1 — Contrast-proxy estimand    AMEND-BEFORE-REGISTRATION    Acceptable as a scouting/triage statistic, but not yet sufficient to support a contrast-level pivot or a contrast claim.
Q2 — Four-band partition / ANOMALOUS    AMEND-BEFORE-REGISTRATION    The partition and significance-against-zero anomaly key are right; anomaly disposition must be frozen.
Q3 — RED conjunction / MC    PASS    The conjunction is the correct conservative fix, and the local Monte Carlo is appropriately specified for what it claims.
Q4 — Sequential loop / pivot    BLOCK    "AMBER at ceiling → RED-at-ceiling" is an invalid inferential conversion.
Q5 — Preconditions P1/P2    BLOCK    P1 is operationally ambiguous and P2 lacks a decision criterion capable of serving as a gate.
Q6 — Open calls    Leans below    Several are reasonable once Q1/Q4/Q5 repairs are incorporated.
Q7 — Additional block scan    BLOCK    Re-issue scope needs several additions before registration.

Q1 — Pinned estimand: AMEND-BEFORE-REGISTRATION

Using the raw mismatch-arm mean as a screening proxy is defensible for choosing where to spend confirmatory compute, provided the language remains exactly that: it sizes a candidate signal, not the final mismatch-minus-equal contrast.

The problem is that the rule uses this proxy for more than triage:

* A GREEN can trigger Movement 3 registration, which is fine if Movement 3 is explicitly the independent contrast test.
* But an all-RED outcome licenses a pivot that interprets the space as bounded sub-floor. That conclusion concerns the contrast, while the scout did not measure the relevant equal-arm mean for each cell.
* The zero/equivalence assumption is verified only at (1.0, 1.0), T_c=1, while the candidate equal references include (2.0, 2.0) and the T_c cells change drive amplitude.

A small raw mismatch current does not by itself bound the contrast if the matching equal-arm current may be nonzero. The missing equal-arm offset could either hide or inflate the contrast.

Required amendment: either:

1. Add a pre-scout baseline/equal-arm calibration gate for every distinct reference configuration used by the pivot:
    * (1.0,1.0) @ T_c=1
    * (2.0,2.0) @ T_c=1
    * (2.0,2.0) @ T_c=2
    * (2.0,2.0) @ T_c=4
    with a predeclared bound establishing that the equal-arm current is negligible relative to the relevant floor; or
2. Restrict the scout conclusion to raw mismatch current only, and prohibit an all-RED pivot about the contrast; or
3. Measure the relevant equal arm in the scout and use the two-sample contrast directly.

For the T_c cells, I agree with the existing reviewer lean: do not license estimand (a) as a contrast claim without two-sample confirmation.

Q2 — Four-band partition and ANOMALOUS: AMEND-BEFORE-REGISTRATION

The revised partition is mathematically complete and the corrected ANOMALOUS criterion is right:

x < -t·SE

is the appropriate wrong-sign guard for one-sided cells. It prevents a statistically significant opposite-direction current from being mislabeled as RED and laundering into the pivot.

The "stall rather than pivot" direction is also correct. A wrong-sign result is evidence that the instrument, sign prediction, or physical interpretation may not be behaving as assumed. It should not be silently absorbed into a null conclusion.

The stated ~2.5% per-cell true-null anomaly probability is plausible under the specified conservative proxy SE and Gaussian assumptions. The ~14.1% six-cell rate assumes independence and six one-sided cells, so it should be described as a planning approximation, not a universal operating rate.

Required amendment: freeze an anomaly-resolution protocol. The current wording—

"A cell may be re-banded out of ANOMALOUS after investigation"

—is too open-ended for preregistration. It needs to specify:

* what counts as an investigation;
* which predeclared diagnostic distinguishes grid artifact, sign-precondition failure, or true opposite-direction physics;
* whether the cell is rerun, excluded, moved to higher M, or declared unresolved;
* whether any changed resolution/seed recipe requires a formal preregistration amendment rather than an informal re-band.

No outcome-dependent repair should be allowed to convert an anomaly into a pivot-supporting RED without a frozen procedure.

Q3 — RED-direction conjunction and Monte Carlo: PASS

The conjunction is the right general fix:

RED = [x+tSE(sd̂)<floor(sd̂)] ∧ [x+tSE(sd_upper)<floor(sd_upper)]

It is conservative relative to the point-SD RED rule because it is literally a subset of that rule. This remains true regardless of which of the two ceilings binds. It correctly avoids the sign reversal in conservatism when:

κ = floor_c − tSE

becomes positive.

The listed 16-block/B96 result is internally coherent:

* point-SD RED rate ≈ 3.95%;
* floor-only upper-SD reading ≈ 18.86%;
* coupled-upper alone ≈ 4.93%;
* conjunction ≈ 3.95%.

The Monte Carlo is appropriate for its narrow claim: under independent, approximately Gaussian block means, a homoscedastic equal-arm proxy, and the stated chi-square SD model, it validates the local false-null behavior of the candidate RED rules.

Two caveats belong in the documentation, but do not block this rule:

* It does not validate the entire sequential six-cell procedure; that belongs in Q4's required full-loop simulation.
* It assumes the cell SD is a reasonable proxy for the equal-arm SD. That is part of Q1's needed calibration/validation work.

Q4 — Sequential-testing integrity: BLOCK

The finite ladder by itself does not create an uncontrolled optional-stopping problem, provided the entire state machine, all thresholds, and all stopping rules are frozen before data collection.

But the present terminal step is not statistically valid:

"Still AMBER against floor(128) at 32 blocks → RED-at-ceiling."

AMBER means the relevant confidence interval still overlaps the floor. At the ceiling, the correct statement is:

The cell is unresolved at the authorized compute ceiling.

It is not:

The cell is bounded below the floor.

A resource ceiling cannot turn insufficient evidence into evidence of absence. Relabeling terminal AMBER as RED can allow a genuine but underpowered signal to contribute to an all-RED pivot.

Required repair: replace RED_AT_CEILING with something like:

* INCONCLUSIVE_AT_CEILING, or
* AMBER_AT_CEILING.

That state must block the pivot. The scout can then end in one of four honest outcomes:

1. GREEN candidate for confirmatory contrast testing;
2. all actual RED with all required stability/baseline gates passed, allowing the pivot;
3. ANOMALOUS requiring investigation;
4. INCONCLUSIVE at authorized compute ceiling.

That fourth outcome is scientifically legitimate. It is not a failure of the pilot; it is a bound on what this compute allocation can resolve.

Before licensing the re-issued run, the selftest/simulation must operate on the entire frozen state machine, not individual contrast power. At minimum it should simulate:

* all six cells jointly;
* the actual 16 → 32 accumulation, preserving dependence between first-pass and extension data;
* the B96 → B128 target change;
* estimated SD and the coupled-upper RED rule;
* P1 one-sided/two-sided assignment and stability flags;
* P2-driven M behavior for T_c cells;
* anomaly generation and its terminal handling;
* the GREEN tie-break;
* global null;
* one-cell at-floor and supra-floor alternatives;
* mixed configurations where one cell has a real signal and the rest are null;
* a wrong-sign artifact scenario;
* T_c-heteroscedastic scenarios;
* a nonzero equal-arm offset scenario.

The simulation needs predeclared acceptance criteria, such as:

* global probability of any false GREEN under the global null;
* probability of an invalid pivot when at least one true contrast is at or above the relevant floor;
* probability of a correct pivot under a calibrated global null;
* probability of a registrable GREEN under specified signal configurations;
* anomaly and inconclusive-at-ceiling rates.

Without predeclared tolerances, "selftest passes" is not yet an experimental decision rule.

Q5 — Preconditions P1 and P2: BLOCK

P1

The current P1 text mixes two incompatible operations:

1. average seeds into a field, then take one curl; and
2. take per-seed curls, then assess agreement.

Those are not interchangeable, and a mean field has only one resulting sign—so it cannot itself be "unanimous across seeds."

The deeper issue is that within-M400 agreement alone does not prove M400 has the right sign. Every M400 seed could consistently share a resolution-induced bias. Stability must be defined against a higher-resolution reference, not merely against itself.

Recommended frozen P1 pin:

* Register σ_cell from the ROI curl of a high-resolution, seed-averaged mean field at M=4000.
* Use a separately predeclared seed set, evaluated per seed at M=400, for the robustness test.
* Declare STABLE only when at least 75% of those M400 per-seed curls agree in sign with the registered σ_cell.
* Pin the seed count and exact seeds before registration. I lean toward N=16, threshold ≥12/16, rather than treating an 8-seed split as decisive.
* Any cell failing this criterion must not count toward the all-RED pivot until the predeclared higher-M or seed-averaged-grid remedy is run.

This preserves the intended division: the sign is a mean-field physical prediction; stability is a practical question of whether the low-resolution instrument preserves that prediction.

P2

P2 currently has a useful purpose but not a fully operational gate. Phrases such as "SD growth shrinks with M" and "M-invariant" require a predeclared decision threshold.

It needs to freeze:

* exact sample size per T_c × M arm;
* exact SD estimator and bootstrap procedure;
* the contrast or ratio used to assess M sensitivity;
* a criterion for "material grid-noise contribution";
* an equivalence/noninferiority criterion for "M-invariant enough";
* the action for each possible result;
* the action for an inconclusive P2.

The sentence that T_c cells remain at M400 "pending" P2 also conflicts with the earlier statement that preconditions must complete before the scout. Resolve that explicitly: P2 should finish first, then the T_c-cell M choice and claim class should be frozen.

Q6 — Open-call leans

Open call    Lean
(i) Equal-arm reference    τy-matched, at matched T_c. It is the more defensible noise-matched reference for the stated ROI/curl mechanism. This is conditional on Q1's equal-arm calibration or confirmatory two-sample validation.
(ii) B_max ceiling    Keep 128. It is a reasonable declared compute limit, but terminal AMBER must remain inconclusive rather than becoming RED.
(iii) Estimand-(a) for T_c>1    Refuse as a contrast-level licensing assumption. Any high-T_c GREEN should trigger a measured two-sample contrast validation at confirmatory.
(iv) First-pass blocks    Adopt 16. It makes a real first-pass RED region available and avoids forcing most null resolution through an unnecessary extension loop.
(v) P1 operational pin    High-M seed-averaged mean-field curl for σ_cell; per-seed M400 agreement with that high-M sign, ≥75%, for STABLE. Predeclare exact N and seed list; I lean N=16 and ≥12 agreeing seeds.

Q7 — Additional BLOCK scan and required re-issue scope

Before re-issuing config_hash and preregistration, I would add the following to §8:

1. Replace RED_AT_CEILING with INCONCLUSIVE_AT_CEILING. It must block the pivot.
2. Add the equal-arm calibration/validation rule required for the contrast-proxy's use in both GREEN interpretation and all-RED pivot interpretation.
3. Freeze the anomaly-resolution state machine. No informal "investigate and re-band" path.
4. Pin P1 completely: high-M reference, M400 robustness test, exact seed sets, N, threshold, and failure remedy.
5. Operationalize P2 completely: estimand, decision threshold, bootstrap details, action table, and inconclusive outcome.
6. Add a full-loop Monte Carlo/selftest harness with explicit global operating-characteristic acceptance criteria.
7. Test all implementation boundaries: equality at GREEN/AMBER/RED cutpoints; one-sided versus two-sided branch; wrong-sign anomaly boundary; SD-upper factors at each block count; empty-cell and anomaly-only pivot guard; terminal-ceiling behavior.
8. State claim limits explicitly: a GREEN is a candidate-selection result until the relevant two-sample contrast is measured; a raw-current RED is not automatically a contrast RED without the baseline condition.
9. Update the preregistration scope to include the simulation script, expected operating-characteristic report, P1/P2 configuration, anomaly SOP, and baseline/equal-arm conditions—not just band_cell(), block count, and B_conf prose.

Overall verdict: BLOCK — v3's repaired banding and RED rule are ratifiable, but registration must wait for the terminal-AMBER correction, contrast-proxy licensing repair, and fully pinned P1/P2 and whole-loop operating-characteristic tests.
