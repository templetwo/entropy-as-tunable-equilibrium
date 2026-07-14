# v4.4 Scout — Decision Rule v3.6 (dead-wood removal + estimand registration + outcome-2 conditionality; revision of v3.5; dispositions RATIFIED by Anthony 2026-07-13)

*Lane B (fable 3/3, mesh-20260713 audit night), finalized 2026-07-13 ~22:45 EDT from
`laneB/v44_scout_DECISION_RULE_v3.6_DRAFT.md` after Anthony's ratification — verbatim,
spacing preserved: `honesty  prevails    make it real` — as read by the anchor into five
dispositions, **each revisable on Anthony's sight** (`RATIFICATION_v3.6.md` beside this
file is the receipt). `v44_scout_DECISION_RULE_v3.5.md` remains RATIFIED-and-frozen
history (law #9); this is a NEW file and the canonical rule text going forward,
**pending no veto on sight**. It disposes of audit-night blockers 3 and 4 against the
executable rule at pin `7a02eb5` (`v44_scout.py` sha256 `1fe9fa1c9d203c50…e35d`) and
states explicitly the outcome-2 conditionality Lane A's certification surfaced.
**Ratifying this rule text does NOT register the scout and does NOT authorize a run —
registration remains HELD, a separate explicit gate on Anthony's clock (law #1).**
Registration-time code changes (the `band_cell` simplification, the `R_occ` machinery —
Lane A's enactment lane) change `source_sha`; the prereg v2 re-issue and pin staging are
the anchor's lane; MANIFEST is rewritten last. Proofs, powered probes, raw NDJSON:
`laneB/LANEB_FINDINGS.md` + receipts. Everything not named in the change summary is
**retained verbatim from v3.5 by reference.***

---

## CHANGE SUMMARY — v3.5 → v3.6 (dispositions per Anthony's 2026-07-13 ratification)

| # | v3.5 state (ratified 2026-07-08) | v3.6 change | Status | § |
|---|---|---|---|---|
| **1** | §3.3 RED requires the four-conjunct coupled-upper conjunction (Q3 PASS, v3.1 4M-draw MC). | Coupled-upper + aligned conjuncts REMOVED from the normative rule; **RED ⇔ `\|μ̂\| + t·SE(sd̂) < floor_c(sd̂)`** (after the GREEN/ANOMALOUS branches). PROVEN verdict-identical: homogeneity theorem + 3,734,500 probes of the real `band_cell` (0 differences; 67,030-difference positive control). Zero impact on any §13 number. Historical §3.3 kept as annotation; v3.1's own MC had already exhibited the identity (conjunction 3.95% = point-sd 3.95%). | **RATIFIED (fork 14 = remove; strengthening alternative CLOSED, kept documented)** | §3.3, §7, §9.4, §12 Q3 |
| **2** | §5(iii′) occupancy veto satisfiable through an unregistered reduction (demonstrated: one CLI flag licenses a full PIVOT_ALL_RED; the veto's answer flips with the estimand choice on identical data). | **`R_occ` is a REGISTERED object** — name + exact formula frozen in the re-issued `prereg_v44.json` (field `occ_reduction`); `analyze()`/`scout_report` WITHHOLD on absent/unregistered/mismatched reduction; `pivot_licensed()` asserts registration mechanically (integrity flag, never a null); §2.1 claim wording scoped to `R_occ` with its blind spot STATED. | **RATIFIED (fork 15 = `lr_asymmetry`, blind spot stated in-claim)** | §0.2 D1″′, §2.1, §5(iii′), §7, §9, §10 |
| **3** | STANDING RULE spans five axes. | **Sixth axis added — the ESTIMAND axis:** every banded statistic's reduction/estimator is itself registered; a guard evaluated on an analyst-chosen estimand is not a guard. | enacted with rows 1–2 | STANDING RULE |
| **4** | Law #2 tested at gate/assertion granularity; §3.3 carried three unbindable conjuncts through three re-audits and a ratification. | **§9.4 bindability-witness discipline:** every conjunct of every normative gate ships a witness input that flips the verdict, or an emptiness proof + removal. Plus the verdict-identity regression pinning row 1 forever. *(The law-#2-vs-FIXTURE standing-law amendment remains an OPEN THREAD for its own human-gated ceremony — not enacted here.)* | enacted | §9.4 |
| **5** | `RULE["green_16_96_2s"] = 1.153` (derives only from exact-t, not the frozen 2.131 table). | Constant restated **1.152** — every derived constant reproduces from the frozen inputs beside it. No verdict impact (4th decimal). | **RATIFIED (1.152)** | §2.3 |
| **6** | §13's null headline (joint P(pivot\|null) ≈ 0.017) implicitly conditions on §5(ii) STABLE firing; Lane A's certification of the executable rule measured **0 licensed pivots in 10⁶ six-cell true-null passes with STABLE at chance**, 0.0163 with STABLE forced true; the pinned P1-B re-run measures per-cell sign agreement 0.41–0.63 against the required 12/16 = 0.75, with σ_cell itself estimator-dependent (stencil vs stencil_clean flips its sign on 2 of 4 probed pairs). | **The outcome-2 conditionality is STATED EXPLICITLY (§13 note below): under the current P1-B design at M=400, STABLE is empirically near-unreachable, so OUTCOME 2 (PIVOT_ALL_RED) is effectively unreachable unless P1 is amended.** The rule does not silently carry a terminal outcome it cannot reach. The P1 physics amendment is **fork 16 — NAMED OPEN**, not resolved tonight (a redesign of a registered precondition is its own reviewed, ratified change). | **RATIFIED (honest disposition; fork 16 OPEN)** | §11, §13 |
| **7** | Title/provenance = v3.5. | Retitled v3.6; provenance records the ratification, the revisable-on-sight caveat, and the held registration gate. | — | header, §10 |

**Kept from v3.5 unchanged (everything else):** the shared ladder (§4), pivot conditions
(0)/(0′)/(i)/(ii)/(iii)/(iv)/(v) as written (only (iii′) amended), n_rerun=56 and all
§8/§8-Ω machinery, P1/P1-A(ω)/P2 as registered designs (fork 16 names the open
amendment; nothing is redesigned here), all §9 scenarios and gates, all §13 numbers
(row 1 provably moves none; row 6 adds a conditionality statement, not a recalculation),
forks 1–13 as ratified at v3.5, and every historical change table.

---

## ★ STANDING RULE — SIXTH AXIS ADDED **[v3.6]**

> *(Five-axis text retained verbatim from v3.5, with this appended:)*
>
> **[v3.6] — and every banded statistic's REDUCTION/ESTIMATOR is itself a registered
> object.** A guard whose operative scalar is chosen at analysis time is not a guard:
> the same blocks can raise or silence the veto depending on an unregistered choice
> (demonstrated live: `laneB/occ_veto_demo_raw.ndjson`, run C). The registered object
> is part of the claim's identity — "occupancy nowhere GREEN" means nothing until the
> map from recorded data to banded scalar is frozen. **Estimand axis** (v3.5 → v3.6,
> Lane B audit): the occupancy veto — §5(iii′), a pivot precondition — was satisfiable
> through a reduction the code itself labeled NOT REGISTERED. Repaired by registering
> `R_occ` + mechanical withhold-on-mismatch (§5(iii′), §7, §10).
>
> Whenever a future rule declares a null, the five-axis grep sentence gains a sixth
> question: **is every reduction that produced a banded scalar frozen in the prereg —
> and would the analysis REFUSE to run under any other?**

---

## §3.3 (REPLACES v3.5 §3.3) — RED robustness: the magnitude bound, dead wood removed **[v3.6, RATIFIED]**

**Normative rule.** Within the §3 partition (priority GREEN → ANOMALOUS → RED → AMBER,
evaluated in that order at the cell's terminal rung):

```
RED  ⇔  |μ̂| + t·SE(sd̂) < floor_c(sd̂)
```

with `t` from the frozen §2.2 table for the statistic's sidedness, `SE(sd) =
sd·√(1/n + 1/64)` (§2.1), `floor_c(sd) = 3.858·sd·√(2/B_conf)` (§0.1). Equivalently
`|μ̂| < κ·sd̂` with κ from the frozen §2.3 table; κ ≤ 0 rungs (16b two-sided, all
8-block configs) leave RED unreachable, exactly as v3.5 documents. RED/ANOMALOUS
disjointness is structural at every reachable-RED rung (κ < t·SE, all four verified in
`laneB/law4_grepcheck.txt`); the partition priority enforces the rest.

**What was removed, and why it is safe (the theorem).** v3.5's §3.3 conjunction
contained three conjuncts that PROVABLY cannot bind. `floor_c` and `SE` are both
homogeneous of degree 1 in sd, so each sd_up conjunct is its point-sd twin with the
threshold scaled by `c = sd_up/sd̂ > 1`: strictly looser wherever κ > 0, irrelevant
wherever κ ≤ 0 (RED already unreachable through the magnitude conjunct). The aligned
point conjunct is implied by the magnitude point conjunct (`x = σ·μ̂ ≤ |μ̂|`). Full
proof, the 3,734,500-probe identity on the real `band_cell` (0 differences,
67,030-difference positive control proving probe power), and the observation that
v3.1's certifying MC had already exhibited the identity: `laneB/LANEB_FINDINGS.md` §1.

**Verdict identity ⇒ zero operating-characteristic impact.** Every §13 number, §9.3
gate expectation, the null headline, compound power (incl. Lane A's executable-rule
0.98114), and the INCONCLUSIVE mass are computed over verdicts; the verdicts are
unchanged on all inputs. Row 1 is an honesty repair, not a recalibration.

**Historical annotation (law #9 — superseded, not erased).** The coupled-upper clause
entered at v3.1 (Q3), survived v3.2–v3.5 and ratification, doing no work at any point.
The v3.1 4×10⁶-draw MC and per-clause rates remain in the v3.5 file. §12's Q3 row is
superseded: "kept exactly" certified scaffolding, not protection — the empty clause
READ as robustness, which is exactly why it may not stay in the normative text.

**Fork 14 — RATIFIED 2026-07-13: REMOVE. The strengthening alternative is CLOSED (not
adopted), kept documented:** a binding upper clause requires the inflation on the SE
side only (threshold `sd̂·(F − c·t·S)`): at 16b/B96 one-sided that is negative (−0.147)
— RED unreachable at the operative first rung; at 32b/B96 the RED region roughly halves
(0.092 vs 0.190). Every §13 number would move and the whole rule would need
re-certification by the registration-grade OC instrument. Removal is verdict-identical;
strengthening was a redesign. Anthony ratified removal.

---

## §5(iii′) (REPLACES v3.5 §5(iii′)) — occupancy veto, bound to the registered reduction **[v3.6, RATIFIED]**

- **(iii′) Occupancy veto (recorded-statistic axis; estimand-registered [v3.6]):** in
  every cell (gating and demoted), the `occupancy_x` two-sided band at the cell's
  terminal rung — **stamped from the REGISTERED reduction `R_occ` and no other** — is
  **not GREEN**. An occupancy GREEN: pivot BLOCKED, HQ-escalated, dispositioned via
  §8-Ω under the same powered/amendment discipline. A terminal occupancy AMBER does not
  block but **must** appear in the claim caveat (§2.1). **If no reduction is registered,
  or the analysis was invoked with a reduction other than `R_occ` (by name or by
  implementation), the DECISION IS WITHHELD — withheld-for-registration, which is not a
  null, not outcome 4, and licenses nothing.** The asymmetry vs (iii) remains documented
  at D1″ and stands as ratified at v3.5 (forks 12/13 closed there). *(v3.5 pinned the
  veto's existence but not its estimand; the executable path could license a
  PIVOT_ALL_RED from a reduction whose own docstring said NOT REGISTERED — Lane B
  finding 2, blocker 4; closed.)*

**D1″′ [v3.6] (extends §0.2 D1″) — `R_occ`, RATIFIED (fork 15): `lr_asymmetry`.**
The registered per-block scalar reduction of the 24-bin `occupancy_x` histogram:

```
R_occ(v) = ( Σ_{i=12}^{23} v_i  −  Σ_{i=0}^{11} v_i ) / Σ_{i=0}^{23} v_i
```

Signed and mean-zero under the null — the only candidate shape consistent with
`band_cell`'s two-sided arithmetic and the existing S10 Δ_occ model. **Known blind
spot, stated in the claim rather than papered over:** left/right-symmetric occupancy
shape change moves `lr_asymmetry` by ~0 and is invisible to this veto (demonstrated:
`laneB/occ_veto_demo_raw.ndjson` run C — a 25× center→edges shift, scalar ≈ 0).
Documented alternatives (a null-calibrated distributional distance; dual reductions
with shared veto α) were before Anthony at ratification and are closed for v4.4; they
remain available to a future amendment through the normal reviewed path.

**§2.1 claim wording (amends the frozen scoped wording — occupancy clause only):**

> *"… and `occupancy_x` **banded two-sided under the registered reduction `R_occ`
> (lr_asymmetry) and nowhere GREEN** (not bounded; unresolved (AMBER) at cells {…}
> where applicable; `R_occ` is blind to left/right-symmetric shape change — the claim
> asserts nothing about occupancy movement outside the registered scalar)."*

---

## §7 (AMENDS the v3.5 pseudocode — two deltas; Lane A's enactment lane implements)

1. **`band_cell` body** (registration-time code change; new `source_sha`): the RED
   branch becomes

   ```python
   # sec 3.3 [v3.6, ratified]: single magnitude conjunct -- the coupled-upper and
   # aligned conjuncts are PROVEN empty (homogeneity theorem; verdict-identical,
   # receipts in laneB/).
   if abs(mu_hat) + t * se_c < f_c:
       return ("RED", abs(mu_hat) + t * se_c, f_c)
   ```

2. **`pivot_licensed` signature + first guard** gains the estimand assertion (defense
   in depth behind the `scout_report` withhold):

   ```python
   def pivot_licensed(gating_bands, stable_flags, omega_bands, occupancy_bands,
                      descriptive_bands, REGISTERED_GATING_ROSTER,
                      REGISTERED_FULL_ROSTER,
                      occ_reduction_name, REGISTERED_OCC_REDUCTION):   # [v3.6]
       # (0'') ESTIMAND REGISTRATION [v3.6] -- before any band is read:
       if REGISTERED_OCC_REDUCTION is None:
           return (False, "no registered occupancy reduction (OCC_REDUCTION_GAP)")
       if occ_reduction_name != REGISTERED_OCC_REDUCTION:
           return (False, "occupancy bands stamped from unregistered reduction %r"
                          % (occ_reduction_name,))
       ...  # v3.5 body unchanged from here
   ```

   `scout_report` passes the invoked reduction's name; the registered name comes from
   the re-issued prereg. A mismatch is a **registration-integrity flag, never a null**.

---

## §9 / §9.4 (ADDITIONS — selftests; all v3.5 items retained)

- **S10 / gate 11 note [v3.6]:** Δ_occ is planted **in the registered scalar `R_occ`**
  (histogram-level construction whose lr_asymmetry equals the planted shift), so the
  sim certifies the veto that runs. *(Lane A interaction: the registration-grade OC sim
  imports `R_occ` from the same source as `band_cell` under the same sha assert.)*
- **Estimand-registration failability (law #2) [v3.6]:** (a) full pivot-compatible
  bands + NO registered reduction ⇒ decision WITHHELD (assert the exact
  `OCC_REDUCTION_GAP` reason); (b) same + invoked reduction ≠ registered ⇒
  `pivot_licensed` False with the unregistered-reduction reason; (c) the run-B exploit
  shape from the Lane B demo must WITHHOLD under the v3.6 machinery (regression pinned
  to `laneB/occ_veto_demo_raw.ndjson`).
- **Bindability witnesses [v3.6]:** every conjunct of every normative gate ships a
  deterministic witness input where that conjunct alone flips the verdict, or a
  documented emptiness proof + removal. Witness list for the simplified §3.3: the
  magnitude conjunct's ±κ cutpoint pairs (already in §9.4); the removed conjuncts carry
  the theorem instead of witnesses.
- **Verdict-identity regression [v3.6]:** the simplified `band_cell` equals the v3.5
  four-conjunct arithmetic on the frozen probe grid (seeded subset of
  `laneB/sec33_inertness_probe.py`'s sweep; expected differences = 0) — the row-1
  change is pinned as behavior-preserving in the selftest itself, forever.

---

## §10 (ADDITIONAL ROWS — scope of changes; enactment staged, registration HELD)

| Artifact | Change | Hash impact |
|---|---|---|
| `band_cell()` in `v44_scout.py` | §3.3 simplification (row 1; verdict-identical, regression-pinned) — Lane A enactment | **new `source_sha`** |
| `scout_report()` / `pivot_licensed()` in `v44_scout.py` | `R_occ` registration plumbing + withhold-on-mismatch (row 2) — Lane A enactment | **new `source_sha`** |
| `CFG["scout"]["blocks"]` in `v44_scout.py` | **8 → 16** — verified provenance, not folklore: the ratified ladder's first rung is `RULE["blocks_first"] = 16` while the scout's collection config still carries the pre-ratification 8; the prereg, mirroring CFG faithfully on all 79 keys, registers the starved value (**anchor finding 6**, mesh-20260713 prereg audit, verified by import-and-diff at `7a02eb5`). Fix rides Lane A's change; plus the **cross-assert selftest `CFG["scout"]["blocks"] == RULE["blocks_first"]`** so config-vs-rule drift can never again pass silently | **new `config_hash`** — Lane A enactment |
| `prereg_v44.json` | v2 re-issue: field `occ_reduction` = {name: `lr_asymmetry`, formula: D1″′}, new pins (source_sha, recomputed config_hash per finding 6's delta list, OC-sim hash — which v3.5's MANIFEST never contained), `rule_version` named explicitly in the envelope, the DIAG-3 additive-diff provenance note | **new sha256** — anchor's staging lane |
| `MANIFEST.sha256` | rewritten **LAST**, covering all artifacts incl. the OC sim | anchor's lane |
| **Stale-prose flag (law #4), rows added** | any normative "coupled-upper" language outside historical/erratum context; any occupancy claim clause not naming `R_occ`; any occupancy band from a non-registered reduction; `green_16_96_2s` = **1.152** (row 5, ratified); any statement of §13's null headline without the STABLE conditionality (row 6) | selftest grep items |

---

## §11 (FORKS — 14/15 RESOLVED, 16 OPENED)

14. **[v3.6] §3.3 disposition — RATIFIED: REMOVE** (verdict-identical, proof attached).
    Strengthening alternative closed, documented in §3.3.
15. **[v3.6] `R_occ` — RATIFIED: `lr_asymmetry`** with the stated symmetric blind spot.
    Alternatives closed for v4.4, documented in D1″′.
16. **[v3.6, NEW — OPEN] The P1 physics amendment.** The pinned P1 evidence (Lane A,
    blocker 5 lifted: 1,536 curls bit-exact under pin) shows per-cell M=400 sign
    agreement 0.41–0.63 against P1-B's required 12/16 = 0.75, only 2/48 sixteen-seed
    windows firing STABLE, and σ_cell flipping sign between stencil estimators on 2 of
    4 probed pairs — σ_cell as currently defined is estimator-dependent and near-
    unidentifiable at M=400. Consequently outcome 2 is effectively unreachable (§13
    note). **Options for a future, separately-reviewed amendment (none adopted
    tonight):** redesign P1-B (estimator, M, threshold, or windowing), redefine σ_cell
    against a pinned estimator with demonstrated identifiability, or accept outcome-2
    unreachability as the honest operating point (the scout can still terminate GREEN /
    INVESTIGATE / INCONCLUSIVE). Any choice re-opens P1's registered design and must
    walk the full review + ratification path. **Anthony's call, on Anthony's clock.**

---

## §12 (ROW SUPERSEDED)

| ChatGPT Q | v3.5 status | v3.6 status |
|---|---|---|
| **Q3** — RED conjunction / MC | "coupled-upper conjunction kept exactly (Q3 PASS); 4M-draw MC" | **Superseded by proof of emptiness (row 1, ratified).** The Q3 MC itself measured the identity (conjunction 3.95% = point-sd 3.95%) — the PASS certified scaffolding that did no work. The magnitude bound (v3.2, the belt) is retained verbatim; only the dead conjuncts leave the normative text. The whole-loop instrument remains the §9 OC sim. |

---

## §13 (NOTE APPENDED — one conditionality made explicit; no numbers recomputed)

**[v3.6] Verdict identity (row 1):** every v3.5 §13 number is carried forward unchanged
and un-recomputed — the §3.3 removal is provably behavior-preserving and the §9.4
regression keeps it that way. Row 2 adds no new rates (the withhold is deterministic);
S10/gate-11 expectations are unchanged, re-expressed in `R_occ` units and certified
against the registered scalar by the Lane A instrument.

**[v3.6] OUTCOME-2 CONDITIONALITY — stated explicitly (row 6, the honest disposition).**
Every pivot-rate number in this section — including the ≈0.017 null headline and Lane
A's executable-rule 0.0163 — **conditions on §5(ii): every counted RED sits on a STABLE
cell.** That conditioning was implicit through v3.5. It is now measured: the executable
`scout_outcome` licensed **0 pivots in 10⁶ six-cell true-null passes with STABLE at
chance**; and the **pinned** P1 evidence (fork 16) measures M=400 per-cell sign
agreement at 0.41–0.63 against the required 0.75, with 2/48 windows firing STABLE and
σ_cell itself estimator-dependent. **Under the current registered P1-B design, STABLE
is empirically near-unreachable, and therefore OUTCOME 2 (PIVOT_ALL_RED) is effectively
unreachable unless P1 is amended (fork 16 — named, open, not resolved tonight).** The
scout's other three terminal outcomes are unaffected. This is stated in the rule
because a rule must not silently carry a terminal outcome it cannot reach: the
composition P(pivot | true null) ≲ 1×10⁻¹⁰ as currently registered is *conservatism*,
but only if it is *disclosed* — undisclosed, it is the inert-clause disease at the
scale of an outcome. (Law-#4 grep row added in §10: the null headline may not be quoted
without this conditionality.)

---

## CONSTANTS APPENDIX — the frozen tables, restated verbatim in the operative document **[v3.6, added per anchor finding 7]**

*A ratified rule document must be SELF-CONTAINED in its constants (law #4, generalized
by finding 7: the integration selftest's prose-vs-config grep correctly refuses
retained-by-reference tables — and the v3.5 reference chain still carries the
superseded 1.153, so following references would verify the harness against a superseded
constant). Every threshold the rule enforces is restated here with the ratified values.
Honest date pair: base tables ratified with v3.5 on 2026-07-08; the v3.6 dispositions
(including `green_16_96_2s` → 1.152) ratified 2026-07-13. `rule_version = v3.6`.*

### A.1 Detection floor (§0.1) — `floor(B, sd) = Z·sd·√(2/B)`, `Z = 3.858` (z₀.₉₉₅ + z₀.₉₀), `alpha = 0.05`

| B | floor(B) |
|---|---|
| 64  | **0.682**·sd |
| 96  | **0.557**·sd (B_conf working default; `blocks_first = 16`, `blocks_extended = 32`) |
| 128 | **0.482**·sd (`B_max = 128`, the declared compute ceiling) |

Honest SE (§2.1): `SE(sd, n) = sd·√(1/n + 1/ref_blocks)`, `ref_blocks = 64`.

### A.2 Frozen Student-t convention (§2.2), α = 0.05

| df (n−1) | one-sided t (0.95) | two-sided t (0.975) |
|---|---|---|
| 7  (8 blocks)  | **1.895** | **2.365** |
| 15 (16 blocks) | **1.753** | **2.131** |
| 31 (32 blocks) | **1.696** | **2.040** |
| 55 (56 blocks — §8/§8-Ω powered rerun) | **1.673** | **2.004** |

### A.3 Exact thresholds (§2.3) — per statistic, units of sd_cell; RED per the ratified §3.6 single magnitude conjunct (`|μ̂| < κ`)

| Config (blocks / B_conf) | floor_c | SE | GREEN x > (1-sided) | GREEN \|μ̂\| > (2-sided) | RED κ (1-sided) | RED κ (2-sided) |
|---|---|---|---|---|---|---|
| **16 / 96 (OPERATIVE first pass)** | 0.557 | **0.2795** (`se_16_96`) | **1.047** (`green_16_96_1s`) | **1.152** (`green_16_96_2s` — **ratified row 5; supersedes v3.5's 1.153**) | **0.067** (`kappa_16_96_1s`) | **−0.039** (`kappa_16_96_2s` < 0 → two-sided RED UNREACHABLE at 16b) |
| 8 / 96 (legacy reference) | 0.557 | **0.375** (`se_8_96`) | 1.267 | 1.444 | κ < 0 → unreachable | κ < 0 → unreachable |
| 32 / 96 (AMBER extension) | 0.557 | **0.2165** (`se_32_96`) | 0.924 | 0.998 | **0.190** (`kappa_32_96_1s`) | **0.115** (`kappa_32_96_2s`) |
| 32 / 128 (B_conf escalation, ceiling) | 0.482 | 0.2165 | 0.849 | 0.924 | **0.115** (`kappa_32_128_1s`) | 0.041 |
| **56 (§8/§8-Ω powered rerun — significance vs 0 only, never a banding config)** | 0.557 (B96 projection) | **0.1830** (`se_56`) | *(fires at \|x\| > t₅₅·SE₅₆ = **0.306** — `rerun_edge`)* | *(n/a)* | *(reband-look κ₅₆ = 0.557 − 0.306 = **0.251** — `kappa_56`)* | *(n/a)* |

Powered rerun: `n_rerun = 56`, honest noncentral-t power at ∓1×floor(96) = **0.913**
(`rerun_power`); law #3 additionally requires **compound six-cell MC power ≥ 0.90**
(`compound_power_target`) — certified for v3.5-as-executable at **0.98114** by the Lane
A instrument, to be re-confirmed under the v3.6 `source_sha`.

### A.4 χ²-upper factors (§3.3 historical annotation + the verdict-identity regression)

`sd_up = sd·√((n−1)/χ²_{0.05,n−1})`: df 7 → **1.797**, df 15 → **1.437**, df 31 →
**1.268** (`chi2_upper`). These no longer enter any normative verdict (ratified row 1
removed the coupled-upper conjuncts); they remain frozen because the §9.4
**verdict-identity regression** reproduces the v3.5 four-conjunct arithmetic against
the simplified rule, and the historical §3.3 annotation cites them.

*Cross-check receipt: every constant in this appendix re-derived from `Z`, the t table,
and the SE formula in `laneB/law4_grepcheck.txt` (19/20 reproduce within 5×10⁻⁴; the
20th is exactly the ratified 1.153 → 1.152 correction this appendix carries).*
