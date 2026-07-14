# v4.4 Scout — Decision Rule v3.6 (dead-wood removal + estimand registration; revision of the RATIFIED v3.5, DRAFT for Anthony ratification)

*Lane B (fable 3/3, mesh-20260713 audit night), 2026-07-13. **This is a DRAFT for
Anthony final-say ratification. It is NOT registered, NOT chronicled as ratified, and
edits NO frozen artifact** — `v44_scout_DECISION_RULE_v3.5.md` is RATIFIED
(`RATIFICATION_v3.5.md`, 2026-07-08) and frozen under law #9; this is a NEW file. It
disposes of audit-night blockers 3 and 4 against the executable rule at pin `7a02eb5`
(`v44_scout.py` sha256 `1fe9fa1c9d203c50…e35d`): **(blocker 3)** §3.3's coupled-upper
RED-robustness clause is proven EMPTY — a theorem, not just 3.6M probes — and is
removed from the normative rule with the proof attached, verdict-identically (fork 14
keeps the strengthening alternative); **(blocker 4)** the occupancy GREEN-veto — a
pivot precondition — is currently satisfiable by an estimand the code itself labels
NOT REGISTERED (demonstrated end-to-end: a full `PIVOT_ALL_RED` licensed via one CLI
flag); the reduction becomes a REGISTERED object `R_occ` with a mechanical
withhold-on-mismatch, and the claim wording is scoped to it (fork 15 gives Anthony the
choice of `R_occ`). Proofs, powered probes, and raw NDJSON records:
`laneB/LANEB_FINDINGS.md` and receipts beside it. Every prior disposition (§12 Q1–Q7,
§14, §16, §17, and the v3.5 change table) stays in force except where a row below
explicitly supersedes it — notably §12's Q3 row. Every threshold cited below is
re-derived against the frozen `RULE` constants in `law4_grepcheck.txt` (law #4).
Everything not named in the change summary is **retained verbatim from v3.5 by
reference.** All decisions remain revisable at Anthony final-say. Registration-time
code changes (band_cell simplification, the `R_occ` machinery) change `source_sha` and
the prereg — flagged here, NOT performed in this draft (law #1; the prereg re-issue and
pin-set staging are the anchor's lane).*

---

## CHANGE SUMMARY — v3.5 → v3.6 (THE DELTAS TABLE FOR ANTHONY'S PEN)

*Sources: Lane B findings (`laneB/LANEB_FINDINGS.md` — theorem + 3,734,500-probe powered
identity for row 1; three-run live demonstration for row 2), overnight blocker notes
2026-07-12 (HQ Opus). Ratify, amend, or reject per row — each row is exact language.*

| # | v3.5 state (ratified) | v3.6 change (drafted) | § | Receipt |
|---|---|---|---|---|
| **1 — load-bearing honesty (blocker 3)** | §3.3 RED requires a four-conjunct "coupled-upper" conjunction (aligned + magnitude, each at point-sd AND sd_upper), certified by v3.1's 4M-draw MC (Q3 PASS) and 3.6M overnight probes as never changing an answer. | **The coupled-upper and aligned conjuncts are removed from the normative rule; RED ⇔ `\|μ̂\| + t·SE(sd̂) < floor_c(sd̂)` (evaluated after the GREEN/ANOMALOUS branches).** PROVEN verdict-identical (homogeneity theorem — both floor and SE are degree-1 in sd, so each upper conjunct is the point conjunct with its threshold scaled by c>1; κ≤0 configs are RED-unreachable via the magnitude conjunct anyway; plus 3,734,500 probes of the real `band_cell` incl. float-boundary hugging and 100k full-ladder cells: 0 differences, with a 67,030-difference positive control proving the probe's power). **Zero impact on any §13 number, gate, or power.** Historical §3.3 kept as annotation. v3.1's own MC already exhibited the identity (conjunction 3.95% = point-sd 3.95%). | §3.3, §7, §9.4, §12 Q3 | `sec33_inertness_probe.py` + `sec33_probe_raw.ndjson` |
| **2 — load-bearing integrity (blocker 4)** | §5(iii′) occupancy GREEN-veto consumes bands stamped from a per-block scalar the ratified text never defines; the executable path refuses by default (`OCC_REDUCTION_GAP`) **but `--occ-reduction lr_asymmetry` — self-labeled NOT RATIFIED, NOT REGISTERED — empties the withhold list and licenses a full PIVOT_ALL_RED**; the choice is stamped, never blocked; the veto's answer flips with the (unregistered) estimand choice on identical data. | **`R_occ` — the occupancy per-block scalar reduction — becomes a REGISTERED object:** name + exact formula frozen in the re-issued `prereg_v44.json` (new field `occ_reduction`); `analyze()`/`scout_report` **WITHHOLD the decision** on any absent, unregistered, or name-mismatched reduction; `pivot_licensed()` mechanically asserts `occ_reduction_name == REGISTERED_OCC_REDUCTION` (returns False — registration-integrity flag, not a null); §2.1 claim wording scoped to `R_occ`; `R_occ`'s blind spots documented in-claim; §9/S10 models Δ_occ in the registered scalar (Lane A interaction). HQ/Lane-B rec for `R_occ`: `lr_asymmetry` (signed, mean-zero under null — consistent with two-sided `band_cell` arithmetic), blindness to symmetric shifts STATED. Choice = **fork 15**. | §0.2 D1″′, §2.1, §5(iii′), §7, §9.1/9.2/9.4, §10, §11 | `occ_veto_gap_demo.py` + `occ_veto_demo_raw.ndjson` |
| **3 — STANDING RULE, sixth axis** | Five axes (compute-ceiling, direction, statistic, cell-roster, look; + recorded-statistic and coupling-regime costumes). | **ESTIMAND axis added:** every banded statistic's reduction/estimator is itself registered; a guard evaluated on an analyst-chosen estimand is not a guard — the guard's operative content must be frozen before the data can be seen. | STANDING RULE | Finding 2, run C |
| **4 — clause-bindability selftest discipline (law #2 at clause granularity)** | Law #2 asserts gates can fail; §9.4 tests assertions and cutpoints. Nothing checks whether each CONJUNCT of a gate can bind — §3.3 carried four conjuncts of which three could not, certified through three revisions and one ratification. | **§9.4 gains the bindability-witness requirement:** every conjunct of every normative gate ships either (a) a deterministic witness input where the conjunct alone flips the verdict, or (b) a documented emptiness proof and removal. Plus a **verdict-identity regression** pinning the row-1 simplification to the v3.5 arithmetic on a frozen sweep. *(Companion: the proposed standing-law amendment "read law #2 against the FIXTURE" — already an open thread, Anthony's pen, not enacted here.)* | §9.4 | Finding 1 |
| **5 — law-#4 hairline** | `RULE["green_16_96_2s"] = 1.153` derives from the exact t (2.13145), not the frozen table t (2.131 → 1.1525 → 1.152). | Constant restated as **1.152** so every derived constant reproduces from the frozen inputs beside it (or, alternatively, the derivation convention "exact-t, then round" is stated once — Anthony's pen; Lane B recommends the former). No verdict impact either way (4th decimal; nearest probed boundary unaffected). | §2.3 | `law4_grepcheck.txt` |
| **6 — identity/header** | Title + provenance = v3.5, ratified. | Retitled v3.6 DRAFT; provenance restates NOT-registered / NO frozen bytes edited / gate is Anthony's; flags the registration-time `source_sha` + prereg impacts of rows 1–2 (NOT performed here; pin staging is the anchor's lane). | header, §10 | — |

**Kept from v3.5 unchanged (everything else):** the shared ladder (§4), the pivot rule's
outcomes and conditions (0)/(0′)/(i)/(ii)/(iii)/(iv)/(v) as written (only (iii′) is
amended), n_rerun=56 and all §8/§8-Ω machinery, P1/P1-A(ω)/P2, all §9 scenarios and
gates (S10/gate 11 gain the registered-scalar note), all §13 numbers (row 1 provably
moves none of them), all forks 1–13, and every historical change table.

---

## ★ STANDING RULE — SIXTH AXIS ADDED **[v3.6]**

> *(Five-axis text retained verbatim from v3.5, with this appended:)*
>
> **[v3.6] — and every banded statistic's REDUCTION/ESTIMATOR is itself a registered
> object.** A guard whose operative scalar is chosen at analysis time is not a guard:
> the same blocks can raise or silence the veto depending on an unregistered choice
> (demonstrated live: `occ_veto_demo_raw.ndjson`, run C). The registered object is part
> of the claim's identity — "occupancy nowhere GREEN" means nothing until the map from
> recorded data to banded scalar is frozen. **Estimand axis** (v3.5 → v3.6, Lane B
> audit): the occupancy veto — §5(iii′), a pivot precondition — was satisfiable through
> a reduction the code itself labeled NOT REGISTERED. Repaired by registering `R_occ`
> + mechanical withhold-on-mismatch (§5(iii′), §7, §10).
>
> Whenever a future rule declares a null, the five-axis grep sentence gains a sixth
> question: **is every reduction that produced a banded scalar frozen in the prereg —
> and would the analysis REFUSE to run under any other?**

---

## §3.3 (REPLACES v3.5 §3.3) — RED robustness: the magnitude bound, with the dead wood removed **[v3.6]**

**Normative rule.** Within the §3 partition (priority GREEN → ANOMALOUS → RED → AMBER,
evaluated in that order at the cell's terminal rung):

```
RED  ⇔  |μ̂| + t·SE(sd̂) < floor_c(sd̂)
```

with `t` from the frozen §2.2 table for the statistic's sidedness, `SE(sd) =
sd·√(1/n + 1/64)` (§2.1), `floor_c(sd) = 3.858·sd·√(2/B_conf)` (§0.1). Equivalently,
`|μ̂| < κ·sd̂` with κ from the frozen §2.3 table; κ ≤ 0 rungs (16b two-sided, all
8-block configs) leave RED unreachable, exactly as v3.5 documents. RED/ANOMALOUS
disjointness is structural at every reachable-RED rung (κ < t·SE — verified for all
four in `law4_grepcheck.txt`); the partition priority enforces the rest.

**What was removed, and why it is safe (the theorem).** v3.5's §3.3 conjunction —

```
RED ⇔ ( x + t·SE(sd̂) < floor_c(sd̂) ) AND ( x + t·SE(sd_up) < floor_c(sd_up) )   # aligned
  AND ( |μ̂| + t·SE(sd̂) < floor_c(sd̂) ) AND ( |μ̂| + t·SE(sd_up) < floor_c(sd_up) ) # magnitude
  AND ( NOT ANOMALOUS )
```

— contains three conjuncts that PROVABLY cannot bind. `floor_c` and `SE` are both
homogeneous of degree 1 in sd, so each sd_up conjunct is its point-sd twin with the
threshold scaled by `c = sd_up/sd̂ > 1`: strictly looser wherever κ > 0, and irrelevant
wherever κ ≤ 0 (RED already unreachable through the magnitude conjunct). The aligned
point conjunct is implied by the magnitude point conjunct (`x = σ·μ̂ ≤ |μ̂|`). Full
proof, 3,734,500-probe identity on the real `band_cell` (0 differences; 67,030-difference
positive control), and the observation that v3.1's own certifying MC already exhibited
the identity (conjunction 3.95% = point-sd 3.95%): `laneB/LANEB_FINDINGS.md` §1.

**Verdict identity ⇒ zero operating-characteristic impact.** Every §13 number, every
§9.3 gate expectation, the ≈0.017 null headline, compound power, and the INCONCLUSIVE
mass are computed over verdicts; the verdicts are unchanged on all inputs. Row 1 of the
change summary is an honesty repair, not a recalibration.

**Historical annotation (law #9 — superseded, not erased).** The coupled-upper clause
entered at v3.1 (Q3), survived v3.2's magnitude extension, v3.3/v3.4/v3.5 re-audits, and
ratification, doing no work at any point. The 4×10⁶-draw v3.1 MC and its per-clause
rates are retained in the v3.5 file. §12's Q3 row is superseded accordingly: "kept
exactly" was certifying scaffolding, not protection — the empty clause READ as
robustness, which is precisely why it must not stay in the normative text.

**Fork 14 (Anthony — NOT recommended): strengthen instead of remove.** A coupled-upper
clause that actually binds requires the inflation on the SE side only
(`|μ̂| + t·SE(sd_up) < floor_c(sd̂)`, threshold `sd̂·(F − c·t·S)`). Costs, computed: at
16b/B96 one-sided the threshold is **negative** (−0.147·sd) — RED unreachable at the
operative first rung; at 32b/B96 the RED region roughly halves (0.092·sd vs 0.190·sd).
Every §13 number moves; the operating point, INCONCLUSIVE mass, and compound power must
be re-certified by the registration-grade OC sim (Lane A's rebuilt instrument).
Strengthening is a design change with real conservatism/compute costs, not a repair of
the empty clause. Lane B recommendation: **remove (row 1); do not strengthen.**

---

## §5(iii′) (REPLACES v3.5 §5(iii′)) — occupancy veto, bound to the registered reduction **[v3.6]**

- **(iii′) Occupancy veto (recorded-statistic axis; estimand-registered [v3.6]):** in
  every cell (gating and demoted), the `occupancy_x` two-sided band at the cell's
  terminal rung — **stamped from the REGISTERED reduction `R_occ` and no other** — is
  **not GREEN**. An occupancy GREEN: pivot BLOCKED, HQ-escalated, dispositioned via
  §8-Ω under the same powered/amendment discipline. A terminal occupancy AMBER does not
  block but **must** appear in the claim caveat (§2.1). **If no reduction is registered,
  or the analysis was invoked with a reduction other than `R_occ` (by name or by
  implementation), the DECISION IS WITHHELD — outcome withheld-for-registration, which
  is not a null, not outcome 4, and licenses nothing.** The asymmetry vs (iii) remains
  documented at D1″ and forked (12/13). *(v3.5 pinned the veto's existence but not its
  estimand; the executable path could license a PIVOT_ALL_RED from a reduction whose own
  docstring said NOT REGISTERED — Lane B finding 2, blocker 4; closed.)*

**D1″′ [v3.6] (extends §0.2 D1″):** `R_occ` = the registered per-block scalar reduction
of the 24-bin `occupancy_x` histogram. **HQ/Lane-B-recommended-pending-Anthony (fork
15): `lr_asymmetry`** — signed left/right mass asymmetry,

```
R_occ(v) = ( Σ_{i=12}^{23} v_i  −  Σ_{i=0}^{11} v_i ) / Σ_{i=0}^{23} v_i
```

— chosen because it is signed and mean-zero under the null, the only shape consistent
with `band_cell`'s two-sided arithmetic and the existing S10 Δ_occ model. **Known blind
spot, stated rather than papered over:** symmetric (left/right-balanced) occupancy
shape change moves `lr_asymmetry` by ~0 and is invisible to this veto (demonstrated:
`occ_veto_demo_raw.ndjson` run C — a 25× center→edges shift, scalar ≈ 0). The §2.1
claim text therefore scopes the occupancy clause to `R_occ` explicitly. Alternatives
for fork 15, documented: a distributional distance to the registered equal-arm
reference (sees all shape change, but is nonnegative with a positive null mean —
incompatible with the frozen two-sided band arithmetic without new null-calibration
machinery and new OC modeling), or registering two reductions with Bonferroni-shared
veto α (more machinery, more null veto rate). Anthony's call.

**§2.1 claim wording (amends the frozen scoped wording — occupancy clause only):**

> *"… and `occupancy_x` **banded two-sided under the registered reduction `R_occ`
> (lr_asymmetry) and nowhere GREEN** (not bounded; unresolved (AMBER) at cells {…}
> where applicable; `R_occ` is blind to left/right-symmetric shape change — the claim
> asserts nothing about occupancy movement outside the registered scalar)."*

---

## §7 (AMENDS the v3.5 pseudocode — two deltas)

1. **`band_cell` body** (registration-time code change; new `source_sha`): the RED
   branch becomes

   ```python
   # sec 3.3 [v3.6]: single magnitude conjunct — the coupled-upper and aligned
   # conjuncts are PROVEN empty (homogeneity theorem; verdict-identical, receipts
   # in laneB/). sd_up retained only for the historical annotation.
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
  sim certifies the veto that runs. *(Lane A interaction: the rebuilt OC sim imports
  `band_cell` and must import `R_occ` from the same source under the same sha assert.)*
- **Estimand-registration failability (law #2) [v3.6]:** (a) full pivot-compatible
  bands + NO registered reduction ⇒ decision WITHHELD (assert the exact
  `OCC_REDUCTION_GAP` reason); (b) same + invoked reduction name ≠ registered ⇒
  `pivot_licensed` False with the unregistered-reduction reason; (c) the run-B shape
  from the Lane B demo — pivot-compatible data + an unregistered-but-selectable
  reduction — must WITHHOLD under the v3.6 machinery (regression pinned to
  `occ_veto_demo_raw.ndjson`).
- **Bindability witnesses [v3.6]:** every conjunct of every normative gate ships a
  deterministic witness input where that conjunct alone flips the verdict, or a
  documented emptiness proof + removal. Witness list for the simplified §3.3: the
  magnitude conjunct's ±κ cutpoint pairs (already in §9.4) remain; the removed
  conjuncts carry the theorem instead of witnesses.
- **Verdict-identity regression [v3.6]:** the simplified `band_cell` equals the v3.5
  four-conjunct arithmetic on the frozen probe grid (seeded subset of
  `sec33_inertness_probe.py`'s sweep; expected differences = 0), so the row-1 change is
  pinned as behavior-preserving in the selftest itself, forever.

---

## §10 (ADDITIONAL ROWS — scope of changes if ratified)

| Artifact | Change | Hash impact |
|---|---|---|
| `band_cell()` in `v44_scout.py` | §3.3 simplification (row 1; verdict-identical, regression-pinned) | **new `source_sha`** |
| `scout_report()` / `pivot_licensed()` in `v44_scout.py` | `R_occ` registration plumbing + withhold-on-mismatch (row 2) | **new `source_sha`** |
| `prereg_v44.json` | new field `occ_reduction` = {name: `lr_asymmetry` (fork 15), formula: as D1″′} | **re-issue → new sha256** (folds into the already-required re-issue: n_rerun 40→56, blocks 8→16, pin drift — the anchor's staging lane) |
| **Stale-prose flag (law #4), rows added** | any normative "coupled-upper" language outside historical/erratum context; any occupancy claim clause not naming `R_occ`; any occupancy band stamped from a reduction other than the registered one; `green_16_96_2s` = 1.152 (row 5) | selftest grep items |

---

## §11 (FORKS ADDED)

14. **[v3.6] §3.3 disposition.** Lane B rec: **remove** (verdict-identical, proof
    attached). Alternative: strengthen (SE-side upper) — REAL costs, computed: RED
    unreachable at 16b/B96 one-sided, RED region halved at 32b/B96, full re-certification
    by the registration OC sim required. Anthony's call.
15. **[v3.6] Choice of `R_occ`.** Lane B rec: `lr_asymmetry` with the stated symmetric
    blind spot. Alternatives: null-calibrated distributional distance (new machinery),
    or dual reductions with shared veto α. Anthony's call.

---

## §12 (ROW SUPERSEDED)

| ChatGPT Q | v3.5 status | v3.6 status |
|---|---|---|
| **Q3** — RED conjunction / MC | "coupled-upper conjunction kept exactly (Q3 PASS); 4M-draw MC" | **Superseded by proof of emptiness (row 1).** The Q3 MC itself measured the identity (conjunction 3.95% = point-sd 3.95%) — the PASS certified scaffolding that did no work. The magnitude bound (v3.2, the belt) is retained verbatim; only the dead conjuncts leave the normative text. The whole-loop instrument remains the §9 OC sim. |

---

## §13 (NOTE APPENDED — no numbers change)

**[v3.6]** Row 1 is verdict-identical (theorem + regression), so every v3.5 §13 number
is carried forward unchanged and un-recomputed — this is the one revision in the v3.x
line whose arithmetic impact is exactly zero, and the selftest regression keeps it that
way. Row 2 adds no new rates (the withhold is deterministic); the S10/gate-11
construction is re-expressed in `R_occ` units with the same planted magnitudes
(+2×floor hard-gated ≈ 1.4×10⁻⁵; +3×floor reported ≈ 7×10⁻¹⁶ — unchanged expectations,
now certified against the registered scalar by the Lane A instrument).
