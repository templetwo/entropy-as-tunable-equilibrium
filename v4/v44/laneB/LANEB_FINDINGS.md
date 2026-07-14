# Lane B Findings — v4.4 Adversarial Pre-Registration Audit (blockers 3 + 4)

*fable (3/3), mesh-20260713, 2026-07-13 night. Worktree `~/Desktop/lab/mesh-v44-laneB`,
branch `v44-audit-rule` @ `7a02eb5`. Every probe imports the REAL `band_cell` /
`ladder_terminal` / `scout_report` from `v4/v44/v44_scout.py` under a full-sha256 assert
(`1fe9fa1c9d203c50 8fbc4016a8e39e1a 7dc055824a91e293 5b1db9bfbfc0e35d`); nothing here is a
reimplementation. Raw primary records: NDJSON files beside this document (law #7).
This is an AUDIT deliverable. It registers nothing, edits no frozen artifact (law #9),
and the gate remains Anthony's alone (law #1).*

---

## FINDING 1 — §3.3's coupled-upper conjunction is inert: CONFIRMED, and it is a THEOREM

**The overnight claim** (2026-07-12, HQ Opus): the ratified §3.3 "coupled-upper"
RED-robustness clause never changes an answer — 3.6M probes, provably inert. Lane B was
tasked to verify independently: construct a case where the clause binds, or produce the
emptiness proof.

**Verdict: emptiness proof produced. No binding case exists. The 3.6M overnight probes
were sampling a theorem.**

### 1.1 The theorem

Both sides of every §3.3 inequality are homogeneous of degree 1 in the sd argument:

```
floor_c(sd) = Z·sd·√(2/B_conf)        = F·sd      (Z = 3.858, §0.1)
SE(sd)      = sd·√(1/n + 1/64)        = S·sd      (§2.1)
```

Write `κ := F − t·S` (the unit-sd RED margin; the frozen κ table of §2.3) and
`c := √((n−1)/χ²_{0.05,n−1}) > 1` (the §3.3 sd-upper factor). For any statistic value
`y` (aligned `x` or magnitude `|μ̂|`), each §3.3 conjunct has the form:

```
point-sd:  y + t·SE(sd̂)   < floor_c(sd̂)    ⇔   y < sd̂·κ
upper-sd:  y + t·SE(c·sd̂) < floor_c(c·sd̂)  ⇔   y < c·sd̂·κ
```

Inflating sd inflates BOTH sides by the same factor c; the "coupled-upper" test is the
same inequality with its threshold multiplied by c.

- **Case κ > 0** (RED reachable): `c·κ > κ`, so the upper conjunct is strictly LOOSER —
  point-sd implies it. It can never bind. (Frozen values: 16b/B96 1s κ=0.067 →
  c·κ=0.096; 32b/B96 1s 0.190→0.240; 32b/B96 2s 0.115→0.146; 32b/B128 1s 0.115→0.146.)
- **Case κ ≤ 0** (16b two-sided, all 8-block configs): the v3.2 magnitude point conjunct
  `|μ̂| < sd̂·κ ≤ 0` is unsatisfiable, so RED is already unreachable and the conjunction
  is false with or without the upper clauses.

Hence the coupled-upper conjuncts cannot change any verdict, at any rung, on any
sidedness branch, for any data. ∎

**Corollary (more dead wood than the blocker note claimed):** the v3.1 *aligned* point
conjunct is also implied by the v3.2 magnitude point conjunct, since
`x = σ·μ̂ ≤ |μ̂|`. The entire operative content of §3.3 is ONE inequality:

```
RED  ⇔  |μ̂| + t·SE(sd̂) < floor_c(sd̂)        [evaluated after the GREEN and
                                               ANOMALOUS branches, whose priority
                                               the partition already enforces]
```

Three of §3.3's four conjuncts do no work. The `NOT ANOMALOUS` guard is likewise
structurally satisfied at every frozen config (κ < t·SE — RED/ANOMALOUS disjoint,
verified for all four reachable-RED rungs in `law4_grepcheck.txt`).

**The record already exhibited this.** v3.1's own 4×10⁶-draw MC reports: point-sd
3.95%, coupled-upper alone 4.93%, **conjunction 3.95%** — the conjunction equals the
point-sd rate exactly, i.e. the upper clause added nothing, measured, in the very MC
that certified it (Q3 PASS). Nobody read the identity as inertness. This is the
prose-vs-fields lesson wearing Q3's clothes: the clause *reads* as protection; its own
certification numbers *exhibit* that it protects nothing.

### 1.2 The empirical leg (powered — the null is only trusted because the control fires)

`laneB/sec33_inertness_probe.py` → `sec33_probe_raw.ndjson`:

| Leg | Construction | Probes |
|---|---|---|
| grid | dense μ̂ sweeps at five sd scales (1e-6 … 1e6), all frozen rungs (8/16/32 blocks × B64/96/128), all three sidedness branches | 3,555,105 |
| boundary | float-boundary-hugging points (`math.nextafter` ladders) at every cutpoint the rule owns: ±κ·sd, ±c·κ·sd, GREEN edges, ANOMALOUS edges, 0 | 79,395 |
| ladder_random | 100,000 random cells (normal / student-t3 / deep-RED / GREEN-shaped block series) through the real `ladder_terminal`, both statistics, all sidedness combos, seeds {11, 20260713, 424242, 777, 31337} | 100,000 |

- **Clause OFF vs real `band_cell`:** the clause is degenerated through the code's own
  path (`_chi2_upper_factor → 1.0`, making sd_up ≡ sd̂). **0 verdict differences in
  3,734,500 probes.**
- **Positive control (the probe can fail):** a deliberately BINDING variant (SE at
  sd_up, floor at point sd — threshold `sd·(F − c·t·S) < sd·κ`) built from `band_cell`'s
  own source with one surgical substitution: **67,030 verdict differences under the
  identical sweep.** The null above is a powered null.
- **Instructive miss, kept on the record:** the first control attempt inflated only the
  floor (threshold `sd·(c·F − t·S) > κ`) and was itself inert —
  `sec33_probe_raw_run1.ndjson`, `probe_has_power: false`, run refused to certify.
  An accidental second confirmation of the lemma (ANY conjunct `y < sd·θ` with θ ≥ κ is
  dead wood), and a live demonstration of the 2026-07-13 corollary: *state the effect
  size your null test had the power to detect, or the null counts for nothing.*

### 1.3 Disposition recommended to Anthony (drafted as v3.6, fork kept)

- **Remove, don't repair (Lane B recommendation):** replace §3.3's normative conjunction
  with its provably-equivalent single magnitude conjunct. Verdict-identical by theorem +
  3.73M-probe identity ⇒ **zero impact on every computed number in v3.5** (§13 anchors,
  gates 1–11, compound power, INCONCLUSIVE mass all unchanged). Pure dead-wood removal;
  honesty gain: the rule stops wearing empty protection. Historical §3.3 text retained
  as annotation (corrections supersede, never erase).
- **The repair alternative is a REAL fork with REAL costs** (kept for Anthony, NOT
  recommended): making the upper clause bind requires putting sd_up in the SE while the
  floor stays at point-sd — threshold `sd·(F − c·t·S)`: at 16b/B96 that is **negative**
  (−0.147) → one-sided RED unreachable at the operative first rung; at 32b/B96 it
  roughly halves the RED region (0.092 vs 0.190). Every §13 number, the ≈0.017 null
  headline, INCONCLUSIVE mass, and compound power would move; the whole rule would need
  Lane A's rebuilt OC sim to re-certify. Strengthening is a design change, not a fix.

---

## FINDING 2 — the occupancy GREEN-veto is satisfiable by an unregistered estimand: DEMONSTRATED

**The blocker note:** the occupancy GREEN-veto (pivot precondition §5(iii′)) can be
satisfied by an estimand the code itself labels unregistered.

**Verdict: demonstrated end-to-end on the real `scout_report`, three runs, same bytes**
(`laneB/occ_veto_gap_demo.py` → `occ_veto_demo_raw.ndjson`):

| Run | Invocation | Result |
|---|---|---|
| A | no `--occ-reduction` | decision **WITHHELD**, reason `OCC_REDUCTION_GAP` — the code behaving correctly |
| B | `--occ-reduction lr_asymmetry` | decision **EMITTED**, outcome **PIVOT_ALL_RED**, `pivot_licensed: true` |
| C | same flag, occupancy histograms carrying a 25× symmetric center→edges mass shift | pivot **still licensed** (lr_asymmetry ≈ 0 — blind to symmetric change); an alternative edge-mass reduction on the SAME blocks bands **GREEN** (would veto) |

The only difference between run A (withheld) and run B (full pivot license) is one
analysis-time CLI flag selecting `_occ_lr_asymmetry` — whose own docstring reads
**"HQ-PROPOSED CANDIDATE, NOT RATIFIED, NOT REGISTERED."** Downstream, nothing checks
registration: the choice is stamped in the report (`"occ_reduction": "lr_asymmetry"`)
but never blocks. And run C shows the deeper problem: **the veto's answer is a function
of the estimand choice** — identical occupancy data yields "no veto, pivot licensed"
under one reduction and "GREEN, veto" under another. A pivot precondition whose
operative content is chosen at the command line is not a registered guard; it is the
recorded-statistic costume (D3) one layer down, on the ESTIMAND axis.

**Disposition drafted as v3.6:** the reduction becomes a registered object
(`R_occ`: name + exact formula, frozen in the re-issued `prereg_v44.json`);
`analyze()`/`scout_report` **WITHHOLD** on any unregistered or mismatched reduction;
`pivot_licensed()` asserts the registration mechanically (defense in depth); the §2.1
claim wording is scoped to the registered reduction; `R_occ`'s blind spots are
documented in the claim text; the OC sim's Δ_occ is modeled in the registered scalar
(Lane A interaction, flagged). Choice of `R_occ` is Anthony's fork; Lane B recommends
`lr_asymmetry` (signed, mean-zero under the null — the only candidate consistent with
`band_cell`'s two-sided arithmetic and the existing S10 model) with its symmetric-shift
blindness stated rather than papered over.

---

## Incidental finding (law #4, minor)

`RULE["green_16_96_2s"] = 1.153` reproduces only from the EXACT t (2.13145…), not from
the frozen §2.2 table value 2.131 that the code actually bands with (which yields
1.1525 → 1.152). Off by 5×10⁻⁴·sd; no verdict impact at any probed point; but the
constants table should be derivable from the frozen inputs it sits beside. Recorded in
`law4_grepcheck.txt` (19/20 constants reproduce within 5×10⁻⁴; χ² factors and
RED/ANOMALOUS disjointness verified for every reachable-RED rung). Proposed v3.6
deltas-table row, Anthony's pen.

## Receipts

| Artifact | What it is |
|---|---|
| `sec33_inertness_probe.py` | the probe (sha-asserted import, clause-off via the code's own path, powered control) |
| `sec33_probe_raw.ndjson` | primary record, run 2 (SUMMARY: 3,734,500 / 0 / 67,030 / power=true / inertness_confirmed=true) |
| `sec33_probe_raw_run1.ndjson` | run 1 with the inert control — kept: the refusal is the lesson |
| `occ_veto_gap_demo.py` | the three-run demonstration (sha-asserted import) |
| `occ_veto_demo_raw.ndjson` | primary record (RUN_A withheld / RUN_B PIVOT_ALL_RED / RUN_C estimand-dependence / hole_demonstrated=true) |
| `law4_grepcheck.txt` | every threshold cited here re-derived vs the frozen RULE dict |
