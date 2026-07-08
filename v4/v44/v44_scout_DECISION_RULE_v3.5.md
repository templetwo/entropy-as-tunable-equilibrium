# v4.4 Scout — Decision Rule v3.5 (rerun-power arbitration fix, revision of v3.4, for Anthony ratification)

*HQ (Mac Studio Claude Code seat, overwatch/provenance), 2026-07-08. **This is a DRAFT for Anthony final-say ratification. It is NOT registered, NOT chronicled, and edits NO harness bytes.** It revises `v44_scout_DECISION_RULE_v3.4.md` (a draft, not frozen) to close the one load-bearing dispute left standing after v3.4's two independent re-reviews (ChatGPT methodology pass + Antigravity R3 audit — both **APPROVE-WITH-REVISIONS**): the powered STATE-B rerun's power at n_rerun=40 was stated as **0.912**, but the honest (reference-uncertain, marginal) noncentral-t power consistent with the rule's own α=0.05 calibration is **0.858** — Antigravity's 0.911 was power *conditional* on an error-free 64-block reference, i.e. a test actually running at α≈0.019, not the rule's α=0.05 (see `ARBITRATION_rerun_power.md` — HQ-arbitrated, independently verified by 4 agents: textual/semantic, independent MC, an adversarial steelman of Antigravity, and the arbiter). **[v3.5]** raises **n_rerun 40 → 56** (honest power 0.913 ≥ 0.90, clearing law #3's per-contrast floor), corrects the erratum wherever the superseded 0.912 number appeared, fixes a minor Gate-11 notation issue (Antigravity R3 Finding 2), requires gates 9/9Ω to assert **compound six-cell Monte-Carlo power ≥ 0.90** (law #3) rather than the per-contrast analytic figure alone, and adopts HQ-recommended (explicitly revisable) defaults for the two forks left open in §0.2/§11. The frozen v4.3 artifacts, the `v44_scout.py` physics path, `prereg_v44.json`, and v3/v3.1/v3.2/v3.3/v3.4 are **not modified** — this is a new file. Every prior disposition (§12 ChatGPT Q1–Q7, §14 v3.1 re-pass, §16 v3.2→v3.3, §17 v3.3→v3.4) stays in force; the v3.4→v3.5 changes are keyed to the reconciliation table directly below. **Raising n_rerun 40→56 touches `CFG["scout"]` and will require re-issuing `prereg_v44.json` with a new sha256 at registration (§10) — flagged here, NOT done in this draft.** Every number below was re-verified this session with `/usr/bin/python3` (scipy.stats.t / scipy.stats.nct, numpy 2.0.2); every change from v3.4 is flagged inline as **[v3.5]**. All §0 decisions remain revisable at Anthony final-say.*

---

## CHANGE SUMMARY — v3.4 → v3.5 (rerun-power arbitration fix; DRAFT, not yet re-reviewed) **[v3.5]**

*Source: `ARBITRATION_rerun_power.md` (HQ resolution of the ChatGPT/HQ-vs-Antigravity power contradiction, 4-agent verified) and `AUDIT_VERDICT_ANTIGRAVITY_R3.md` (Antigravity's Finding 2, minor notation). Both external reviews of v3.4 returned APPROVE-WITH-REVISIONS; this table disposes of every REVISE item plus the two genuine forks HQ is recommending defaults for.*

| # | v3.4 state | v3.5 change | § |
|---|---|---|---|
| **1 — load-bearing** | Powered rerun at **n_rerun=40**: SE=0.2016·sd, t₃₉=1.685, edge=0.340·sd, κ₄₀=0.217·sd, stated power **0.912 ≥ 0.90**. | **n_rerun raised to 56**: SE=**0.1830·sd**, t₅₅ one-sided=**1.673** (two-sided **2.004**), edge=**0.306·sd**, κ₅₆=**0.251·sd**, honest noncentral-t power at ncp=3.043 = **0.913 ≥ 0.90**. Propagated everywhere n_rerun=40 was load-bearing spec (not historical narrative). | §2.2, §2.3, §4, §5(iii), §8, §8-Ω, §13 |
| **2 — erratum** | v3.4 asserted 0.912 ≥ 0.90 at n_rerun=40 as the rule's honest power. | **ERRATUM, recorded, not erased (law #9):** the honest α=0.05 noncentral-t power at n_rerun=40 is **0.858**, not 0.912. Antigravity's 0.911 (→ rounded "0.912" in v3.4 prose) was power conditional on an error-free 64-block reference — a test actually running at α≈0.019, not the rule's stated α=0.05. HQ-arbitrated, 4-agent verified. This erratum is WHY n_rerun is raised to 56. | change-summary (here), §13 |
| **3 — compound power** | Gates 9/9Ω asserted **per-contrast** analytic power (0.912, later 0.913) as if it satisfied law #3. | Gates 9/9Ω now require **compound six-cell power ≥ 0.90 verified by Monte-Carlo** (law #3 — analytic per-contrast power lied before: v4.3's 0.998 vs 0.655 compound). Per-contrast 0.913 is necessary evidence, not sufficient; the registration-grade OC simulator (§9, separate build) must verify the compound MC before registration. | §8, §8-Ω, §9.3 |
| **4 — minor notation** | §9.3 Gate-11 row folded the +3×floor sub-case rate into the +2×floor row's parenthetical notes. | Reformatted as a distinct sub-case line inside the Gate-11 cell so the +2× and +3× rates read as separate, unambiguous entries (Antigravity R3 Finding 2). | §9.3 |
| **5a — fork default** | Occupancy guard-strength listed as an open fork (§11 item 12) with no default flagged. | **HQ-recommended-pending-Anthony (revisable at ratification):** keep the current asymmetry — occupancy GREEN-veto + mandatory caveat, weaker than omega's ladder-driving INCONCLUSIVE-blocking guard. Rationale retained (no registered sign, no calibrated transfer function, protocol-bound direction per law #8). Symmetric alternative stays listed. | §0.2 D1″, §11 fork 12 |
| **5b — fork default** | Operating point (fork 2) restated the v3.3→v3.4 cascade with alternatives but no HQ default flagged as such. | **HQ-recommended-pending-Anthony (revisable at ratification):** the conservative operating point that preserves ≥0.90 compound power and the honest reference-uncertain belt guarantee (the ≈0.017 one-sided-omega / high-INCONCLUSIVE point). Compute-cost note and alternatives retained. | §0.2, §11 fork 2 |
| **6 — this table** | — | This reconciliation table added, matching the style of the §24-37 (v3.4) and §17 (v3.3→v3.4) tables. | here |
| **7 — identity/header** | Title + provenance identified the file as v3.4. | Retitled v3.5; provenance line restates HQ seat / DRAFT-for-Anthony-ratification / not registered / no harness bytes edited; flags that n_rerun 40→56 requires a `prereg_v44.json` re-issue (new sha256) at registration — not performed in this draft. | header, §10 |

**Kept from v3.4 unchanged (HQ-recommended-pending-Anthony):** everything not named above — the shared omega ladder (D1), P1-A(ω) sidedness registration (D2), the occupancy veto's existence (D3), the §8-Ω machine itself (D4, only its rerun size changes), full-roster completeness (D5), the extended ρ-sweep (D6), and the computed-expectation discipline (D7). All five STANDING RULE axes, all §12/§14/§16/§17 dispositions, and every v3.3/v3.4 number not touched by n_rerun or the two forks above stand as written.

---

## ★ STANDING RULE (extended in v3.4 — the recurring category error, now stated over FIVE axes)

> **A null / RED / pivot claim must bound the effect MAGNITUDE over the WHOLE claimed object — all directions, all statistics named in the claim, all cells in the claim denominator, [v3.4] all block-count LOOKS the claim's guards depend on, and [v3.4] all coupling regimes the guards' guarantees are asserted over — never a projection and never a silently-shrunk subset. If a cell is demoted or excluded, the claim MUST shrink to the surviving design points, and pivot membership — [v3.4] for EVERY dict the license consumes, not only the gating dict — must be pinned in the pseudocode. [v3.4] Every RECORDED statistic is either banded-and-guarded or named unbounded WITH a documented rationale for the asymmetry — "recorded and unexamined" is the costume "descriptive and excluded" wore last revision. [v3.4] Every hard-gate "expected" value must be COMPUTED (MC or exact), never asserted.**
>
> "Absence of a predicted-direction signal" is **not** "evidence of absence of an effect." The same category error has now been caught on **five axes**, at least once per revision:
> - **Compute-ceiling axis** (v3 → v3.1, ChatGPT Q4): an AMBER at the compute ceiling was converted into `RED_AT_CEILING` and counted as a null. Repaired by `INCONCLUSIVE_AT_CEILING` blocking the pivot.
> - **Direction axis** (v3.1 → v3.2, HQ re-pass BLOCK): a one-sided RED bounded only the sign-aligned component `x = σ·μ̂`, never `|μ̂|`. Repaired by the **RED magnitude bound** (§3).
> - **Statistic axis** (v3.2 → v3.3, whole-object audit BLOCKER): the pivot claim bounded only `quad_loop_rate` while `omega_roi` could sit GREEN. Repaired by the statistic-scoped claim + the **omega veto** (§5(iii)).
> - **Cell-roster axis** (v3.2 → v3.3, MAJOR): a null over 4 design points could be minted from bounds on 2. Repaired by the roster-parametric claim + roster assertion (§2.1, §7).
> - **[v3.4] Look axis** (v3.3 → v3.4, whole-object re-pass BLOCKER): the omega veto existed on paper but omega was **stamped only at the primary's terminal block count** — the primary's ladder throttled the guard's resolution, so a real +2×floor omega current escaped the veto ~21–24% per cell and gate 8 was breached (measured 0.0075 > 0.005) while its "expected ≲ 10⁻³" was asserted, not computed. Repaired by the **shared secondary ladder** (§4: an omega AMBER extends the cell exactly like a primary AMBER) + **omega `INCONCLUSIVE_AT_CEILING` blocks the pivot on a gating cell** (§5(iii)) — under which gate 8's residual is ≈ 10⁻¹¹ (computed, §13) and is **robust to omega sidedness by construction**.
> - **[v3.4] Recorded-statistic axis** (same re-pass, MAJOR — the next costume): `occupancy_x` — the one statistic that carried v4.3's CONFIRMED effect, the very precedent §2.1 cites to justify the omega veto — was "recorded and unbounded" with no band and no veto and no documented rationale. Repaired by **banding `occupancy_x` two-sided + an occupancy GREEN veto** (§5(iii′)) + scenario S10 + hard gate 11, with the omega/occupancy guard-strength asymmetry now explicitly rationalized (§0.2 D1″) and forked for Anthony (§11 forks 12/13).
> - **[v3.4] Coupling-regime axis** (same re-pass, MAJOR): the ρ sensitivity sweep {0.5, 1, 2} was all-positive — it certified the belt+suspenders JOINT guarantee from a subset of coupling space in which the suspenders structurally cannot fail; under **transduction inversion** (curl right, curl→current response inverted) P1-B — which measures CURL agreement, sharing the curl, not the response — passes 16/16 while the true current opposes σ_cell, and the protection is belt-only. Repaired by **ρ ∈ {−1, 0, 0.5, 1, 2}** (§9.1), the §1.1 prose scoped to non-inverted transduction, and an S5 inversion sub-case with the belt-only number named (§9.2).
>
> Whenever a future rule declares a null, grep it against this sentence on ALL FIVE AXES: does the condition bound `|μ̂|`? does the claim name exactly the statistic(s) actually bounded — and is every OTHER recorded statistic either guarded or rationalized? does the claim denominator equal the set of cells that actually gated — in EVERY dict the license reads? does every guard get a LOOK sized to its own job, not throttled by another statistic's ladder? is every guarantee measured over the coupling regimes where it can actually fail? and is every expected number computed?

---

## CHANGE SUMMARY (historical) — what v3.4 changed vs v3.3 (whole-object re-pass: 1 blocker + 8 majors, deduplicated across three audit lenses to 7 defects) **[retained verbatim from v3.4]**

| # | v3.3 state | v3.4 repair | § |
|---|---|---|---|
| **D1 — BLOCKER (look axis): omega veto throttled by the primary's ladder** | Omega was banded **once at the cell's terminal block count set by the primary's ladder** (§5(iii)/§7) — often 16b, where one-sided GREEN needs 1.88×floor. A real Δ_ω = +2×floor current misses the veto ~21–24%/cell (terminal AMBER); measured P(pivot \| S8) ≈ 0.0075 (one-sided omega, ρ_qω=0) — **breaching gate 8's own ≤ 0.005**, ~7× the asserted-not-computed "≲ 10⁻³". Secondary hazard: a sim builder who gives omega its own ladder passes gate 8 while the real `analyze()` stamps omega at the primary's count — the gate certifies a veto the run does not implement. | **Shared secondary ladder (one pinned implementation, §4):** the cell's §4 ladder extends while **EITHER** the primary **OR** `omega_roi` is AMBER (primary GREEN/ANOMALOUS short-circuit — their outcomes preempt); **both statistics are stamped at the cell's single terminal rung**. An omega AMBER surviving the full ladder → **omega `INCONCLUSIVE_AT_CEILING`, which BLOCKS the pivot on a gating cell** (§5(iii)) — the "nowhere GREEN/ANOMALOUS" clause of the claim is assertable only where omega was RESOLVED. Under this design a super-floor omega current can escape the veto only by banding omega **RED** — P ≈ 1.4×10⁻⁵/cell at +2×floor — so **gate 8's computed expected ≈ 10⁻¹¹ (MC-zero at 4×10⁴ cells/arm), robust to sidedness** (§13). The §9 sim must implement the ladder **as `analyze()` will** (one code path, S8 asserts it). | §4, §5, §7, §9, §13 |
| **D2 — major (sidedness): omega banding sign undefined + §13 non-reconciling** | §3 said omega uses "the omega field's own P1-registered sign where declared, else two-sided," but §1.1 P1 registered exactly ONE σ_cell (the force-field curl) and never an omega sign — so as written omega defaulted **two-sided in every cell**, where ANOMALOUS "does not apply": the veto's ANOMALOUS arm was dead code, and §13's omega numbers (0.049/cell, 0.26 six-cell, joint 0.11) reconciled **only** under the one-sided branch — a law-#4 non-reconciliation between prose numbers and the default branch. | **P1-A(ω) omega sign registration (§1.1):** σ^ω_cell registered per cell from the **same** N_avg=32 seed-averaged M=4000 mean field (the sign of its ROI-integrated net vorticity; same negligibility floor → INDETERMINATE → two-sided) — no new compute. Omega bands one-sided where σ^ω_cell ∈ {+,−}, two-sided where INDETERMINATE; **both branches' numbers are now stated in §13** (null pivot-compatible/cell: 0.509 one-sided vs 0.335 two-sided; gate 8 residual ≈ 10⁻¹¹ vs ≈ 10⁻¹⁸ — **the D1 repair makes gate 8 sidedness-robust**, because the escape path is omega-RED, not the ANOMALOUS arm). v3.3's 0.049/0.26/0.11 arithmetic is **superseded** (it assumed the throttled single stamp). | §1.1, §3, §13 |
| **D3 — major (recorded-statistic axis): `occupancy_x` unexamined** | `occupancy_x` recorded, never banded, no veto — though the doc itself cites "v4.3's real effect loaded on occupancy alone" as the precedent for the omega veto, and the veto's own rationale sentence applies verbatim. No rationale for the omega/occupancy asymmetry; no fork. Outcome 2 could pivot away from the line with a +3×floor occupancy current in every cell, invisible to every gate. | **`occupancy_x` is BANDED (two-sided, §3) at the cell's terminal rung, and an occupancy GREEN in ANY cell (gating or demoted) BLOCKS the pivot** (§5(iii′)), HQ-flagged, formal disposition required. Two-sided banding is direction-complete (GREEN on `|μ̂|`), so no occupancy sign registration is needed (rationale: v4.3's occupancy direction is protocol-bound — reset vs closed-NESS, law #8 — and does not transfer as a prediction). **Documented asymmetry** (D1″): omega gets the stronger guard (INCONCLUSIVE blocks; near-primary sensitivity 0.83) while occupancy gets GREEN-veto + mandatory caveat (its non-GREEN terminal bands do not block; forks 12/13 give Anthony the stronger alternatives). Failability: scenario **S10** + **hard gate 11** — P(pivot \| occupancy-only +2×floor in all six cells) ≤ 0.005, **computed expected ≈ 1.4×10⁻⁵** (per-cell occupancy GREEN 0.741 at +2×, 0.9945 at +3× — §13). Claim text updated: "`occupancy_x` **banded two-sided and nowhere GREEN**; not bounded" replaces "recorded and unbounded". | §0.2, §2.1, §3, §5, §7, §9, §13 |
| **D4 — major (disposition axis): omega-ANOMALOUS un-block path unpowered** | §5(iii) routed an omega ANOMALOUS to an unspecified "§8-style investigation"; the powered n_rerun=40 vanish test was pinned ONLY for the primary. A formal disposition could reband omega non-ANOMALOUS off an **unpowered** look (power ~0.61 at −1×floor — the same number that motivated the §8 fix) and un-block the pivot over a live wrong-sign omega current — the evidence-destruction defect re-entering one statistic over, through a channel absent from every gate's accounting. | **§8-Ω (§8): the omega disposition machine is the SAME powered machine applied to the omega statistic.** An omega ANOMALOUS (or an omega GREEN being challenged) can be rebanded **only** through a STATE-B rerun at the predeclared **n_rerun = 40** fresh blocks (t₃₉ = 1.685, SE = 0.2016·sd, edge 0.340·sd — identical, statistic-agnostic arithmetic; power 0.912 ≥ 0.90 at ∓1×floor), via formal amendment. **Gate 9 extended (9 + 9Ω)** to assert the powered rerun for both statistics; the **omega-reband channel is counted** in S8's number of record; an S8 sub-case plants a wrong-sign Δ_ω = −1×floor omega current (per-cell veto-or-block 0.982, measured — §13). | §5(iii), §8, §9, §13 |
| **D5 — major (dict-denominator): completeness asserted for the gating dict only** | `pivot_licensed()` asserted membership only for `gating_bands`; `omega_bands`/`descriptive_bands` had NO completeness assertion — the v3.2 silent-shrink leak recurring one dict over. A demoted AxT4 absent from `omega_bands` (built by iterating the gating roster — a one-line plumbing omission) passes `any()` unexamined; the emitted claim ("omega recorded and nowhere GREEN in any cell") is **false**. §9.4's selftests planted wrong keys in the gating dict and GREEN/ANOMALOUS values PRESENT in the other dicts — never a MISSING key. | **Full-roster assertions on every consumed dict (§7):** `pivot_licensed()` takes `REGISTERED_FULL_ROSTER` (all registered cells, gating ∪ demoted — frozen pre-P2) and asserts `set(omega_bands) == FULL`, `set(occupancy_bands) == FULL`, `set(descriptive_bands) == FULL − GATING`, alongside the existing gating assertion. Any missing/extra key in ANY dict → False (registration-integrity flag, not a null). **§9.4 selftests now plant MISSING keys in each dict** (gate 10 extended); S9 gains assertion (d): AxT4 demoted + absent from `omega_bands` ⇒ False. | §7, §9.2, §9.4 |
| **D6 — major (coupling-regime): all-positive ρ sweep certifies inert suspenders** | §9.1's STABLE coupling sweep ρ ∈ {0.5, 1, 2} asserted the belt+suspenders joint guarantee over the whole coupling space from a subset where the suspenders cannot fail. §1.1's prose ("a cell whose true current opposes its registered σ_cell will tend to fail ≥12/16") is **false under transduction inversion**: P1-B measures CURL sign agreement — it shares the curl, not the response — so an inverted curl→current transduction gives STABLE 16/16 with a true −1×floor current, and the protection is belt-only. (No tolerance breach — belt-only invalid pivot ≈ 0.0006 under the v3.4 ladder, ≤ 0.02 — the defect is a certified two-layer guarantee whose second layer is provably inert in a physically probed regime.) | **ρ sweep extended to {−1, 0, 0.5, 1, 2}** (§9.1) — ρ = 0 (uncoupled) and ρ = −1 (inverted transduction) are mandatory arms; **§1.1's prose is scoped** ("…will tend to fail ≥12/16 *when the curl→current transduction is not inverted*; under inversion the suspenders are inert and the belt is the sole guarantee — measured belt-only"); **S5 gains the inversion sub-case** (STABLE 16/16 forced by construction, Δ = −1×floor) and gate 5's number of record is reported per ρ arm including ρ ≤ 0. | §1.1, §5, §9.1, §9.2 |
| **D7 — major (uncomputed expectations + stale operating point)** | Gate 8's "expected ≲ 10⁻³" was asserted without computation and was wrong by ~7× (actual ≈ 0.0075 as stamped, 0.004–0.019 across sidedness/terminal-mix variants — straddling the tolerance). §13's omega arithmetic and the ≈ 0.11 headline assumed the throttled stamp. | **Every §9.3 hard-gate expected value recomputed this session through the v3.4 shared ladder** (MC, 4×10⁴ cells/arm, seeds 20260708/20260709, §13): gate 1 ≈ 0.002, gate 2 ≈ 0.0006, gate 5 ≈ 0.0006 (+ reband channel ≈ 4×10⁻⁵), gate 5′ MC-zero, gate 8 ≈ 10⁻¹¹, gate 9/9Ω = 0.912, gate 11 ≈ 1.4×10⁻⁵. **Honest joint headline extended: 0.808 → 0.349 → 0.148 → (v3.3's ≈ 0.11 superseded) → ≈ 0.017** at ρ_qω = 0 with one-sided omega (§13; ≈ 0.0014 on the all-two-sided branch) — the operating point is restated as fork 2 for Anthony with the compute cost (expected blocks/cell ≈ 31 vs ≈ 28). | §9.3, §11, §13 |

**Kept from v3.3 unchanged (HQ-recommended-pending-Anthony):** the statistic-scoped + roster-parametric claim wording machinery (§2.1), the omega veto's existence and blocking strength (fork 10), the demotion consequences (§1.2), the powered primary §8 vanish test (n_rerun=40), gates 9/10, the RED magnitude bound + coupled-upper conjunction (§3/§3.3), belt-and-suspenders (couple 5), restated gates 5/5′, Student-t₁₅ false-anomaly correction, SE_FACTOR n=8 = 0.375, two-sided-RED-unreachability documentation, and everything §12/§14/§16 list as preserved.

---

## CHANGE SUMMARY (historical) — v3.2→v3.3 and earlier

*Retained by reference for the audit trail: see the v3.3 file's change-summary table (statistic-axis blocker → statistic-scoped claim + omega veto; cell-roster leak → roster-parametric claim; unpowered §8 vanish test → n_rerun=40) and the v3.2 file for the v3.1→v3.2 table. All of it remains in force in v3.4 except where a v3.4 row above explicitly supersedes a number or a stamp rule.*

---

## 0. Identity + adopted decisions

### 0.1 Instrument identity (verify before any run — unchanged from v3.1/v3.2/v3.3)

| Anchor | Value |
|---|---|
| `version` | `v4h-1.4.0` |
| `config_hash` | `a344d6c47c8a22c1` (recomputed if any CFG block changes — §10) |
| `source_sha` | `0b65a9ee92b9fe2c` |
| `prereg_v44.json` sha256 | `b7c5aeb6bd21b70036f7fb6841f199fbf923aa984cba3d30a71943c75e9a2a2b` (re-issued if CFG changes — §10) |
| interpreter | `/usr/bin/python3` (Python 3.9.6, numpy 2.0.2 pinned) |

Detection floor, verified against `_detection_floor` (line 670) — a **two-arm** minimum-detectable-effect:

```
floor(B, sd) = (z_{0.995} + z_{0.90}) · sd · √(2/B) = 3.858 · sd · √(2/B)
```

| B | floor(B) = 3.858·sd·√(2/B) |
|---|---|
| 64  | 0.682·sd |
| 96  | **0.557·sd**  (adopted B_conf default; 2×floor(96) = 1.114·sd) |
| 128 | 0.482·sd  (escalation ceiling B_max) |

### 0.2 Adopted decisions (all revisable at re-review / Anthony — D1′ amended and D1″ added in v3.4)

| # | Decision | Value | Rationale / coupling |
|---|---|---|---|
| D1 | Primary statistic | `quad_loop_rate` | Continuity with the v4.3 **G1 vortex-control calibration**. Rests on that continuity, **not** on the 2.2σ κ-suppression point estimate (§1.3). The pivot claim is scoped to this statistic (§2.1). |
| D1′ | Secondary statistic | `omega_roi` — **banded on the SHARED ladder + pivot veto [v3.4 amended]** | Banded through the same `band_cell()` arithmetic, **at the cell's terminal rung of the shared §4 ladder — an omega AMBER extends the cell exactly like a primary AMBER [v3.4]**; sidedness from **P1-A(ω)** (§1.1 [v3.4]). Does **not certify** the pivot claim, **but an omega GREEN or ANOMALOUS in any cell BLOCKS the pivot** (§5(iii)), **and [v3.4] an omega `INCONCLUSIVE_AT_CEILING` on a GATING cell also BLOCKS** — the claim's "omega nowhere GREEN/ANOMALOUS" clause is assertable only where omega was resolved. *(v3.3 stamped omega once at the primary's terminal count — the look-axis blocker, D1.)* |
| **D1″ [v3.4]** | **Tertiary statistic** | **`occupancy_x` — banded two-sided + GREEN veto. [v3.5] HQ-recommended-pending-Anthony (revisable at ratification): keep the current asymmetry.** | The only statistic that ever carried a confirmed v4.x effect (v4.3 occupancy micro-shift, p=0.024) must not sit unexamined under a minted null. Banded **two-sided** by the same `band_cell()` at the cell's terminal rung (no sign registration: v4.3's occupancy direction is protocol-bound — reset vs closed-NESS, law #8 — and does not transfer; two-sided GREEN on `|μ̂|` is direction-complete). **An occupancy GREEN in any cell BLOCKS the pivot** (§5(iii′)), HQ-flagged, dispositioned via §8-Ω. **Asymmetry vs omega, rationalized:** occupancy does NOT drive the ladder and its AMBER does NOT block at the ceiling — it is a lower-sensitivity channel with no registered sign and no calibrated transfer function, and its v4.3 direction is protocol-bound (law #8) so it does not warrant the stronger symmetric guard; its non-GREEN terminal bands are recorded with a **mandatory claim caveat** instead ("banded two-sided, nowhere GREEN, not bounded; unresolved (AMBER) at cells {…}"). **The stronger symmetric alternative remains available and KEPT as Anthony's fork** (forks 12/13). Failability: S10 + hard gate 11 (§9). |
| D2 | First-pass blocks | **16** per cell | At 8 blocks RED is unreachable (κ<0, §3.3); 16 gives a usable first surface. (Q6-iv adopted.) |
| D3 | M_grid | **400** for geometric cells A/B/C/D, **GATED** on P1 sign-stability (§1.1). Tc cells AxT2/AxT4 **M frozen by P2 before the scout** (§1.2). | M does **not** lower the floor (DIAG 1); the M concern is grid-generated-signal fidelity, addressed by blocks/seed-averaging. |
| D4 | B_conf (floor projection) | **96** working default; escalation 96→128 ceiling for persistent AMBER (§4). | floor(96)=0.557·sd, floor(128)=0.482·sd. |
| D5 | Estimand | **Option (a)** — raw mismatch current as **screening/triage** statistic | μ̂ vs two-arm floor(B_conf); honest SE = sd·√(1/B_scout + 1/64). Restricts what (a) may claim (Q1): sizes a candidate signal and licenses a **raw-current** pivot only — **not** the mismatch-minus-equal contrast (§2.1, §5). |

### 0.3 Couplings that must not drift apart (seventh added in v3.4)

1. **sign precondition ↔ per-cell predicted signs ↔ pivot license** — one chain (§1.1, §6.2, §5). **[v3.4] P1-A(ω) joins the chain: omega sidedness is registered, never defaulted silently.**
2. **estimand ↔ B_conf ↔ AMBER escalation ceiling** — share `floor_c` (§2, §4, §5).
3. **M_grid ↔ primary statistic** — one decision: quad@M400 (D1+D3; §1.3).
4. **claim class ↔ what was measured** (Q1/Q7) — a raw-current RED pivot is a raw-current claim (§2.1, §5, §10).
5. **RED magnitude bound ↔ STABLE gate ↔ wrong-sign protection** (v3.2) — belt + suspenders are one guarantee, measured jointly by the OC sim (§9). **[v3.4] The guarantee's coupling-regime domain is part of the coupling: the sweep MUST include ρ ≤ 0, where the suspenders are inert and the belt is sole (§9.1); the §1.1 prose is scoped accordingly.**
6. **claim scope ↔ gating roster ↔ omega veto** (v3.3) — one whole-object guarantee (§1.2/§2.1/§5(iii)/§7). **[v3.4] Extended: the roster assertion covers EVERY dict `pivot_licensed()` consumes (full-roster completeness, §7), not the gating dict alone.**
7. **[v3.4] guard ↔ look** — every pivot-blocking guard (omega veto, occupancy veto) is stamped from a look sized by ITS OWN resolution need: omega drives the shared ladder (§4) and blocks at the ceiling if unresolved; occupancy's weaker look is a documented, forked asymmetry (D1″). The §9 OC sim and the real `analyze()` implement the ladder through **one pinned rule** — S8 asserts the sim's ladder is the run's ladder (the "gate certifies a veto the run does not implement" hazard, D1).

---

## 1. Precondition runs (gate the scout — complete and register BEFORE the scout)

These are **diagnostics, not scout results**. They run in declared, quarantined namespaces (`precond_P1::`, `precond_P2::`), **NEVER** pooled (law #6). Both preconditions terminate and register before the scout is licensed (P2 finishes first, then the Tc-cell M, claim class, gating roster + surviving-design-point claim scope are frozen — §1.2).

### 1.1 Precondition P1 — per-cell predicted signs + sign-stability (Q5-P1; P1-A(ω) added, prose scoped [v3.4])

**P1-A — register the directional prediction σ_cell (unchanged from v3.2/v3.3):**
- For each of the six cells, compute the **ROI-integrated curl of the seed-averaged mean aniso force field at M=4000** — average-then-curl. One sign per cell.
- **σ_cell ∈ {+, −}** := sign of that high-M seed-averaged ROI curl; below the predeclared negligibility floor → **INDETERMINATE**, bands two-sided (§3).
- **Predeclared high-M reference set (HQ proposal, revisable — fork §11):** **N_avg = 32** seeds `precond_P1::77001…77032` at **M=4000**.

**[v3.4] P1-A(ω) — register the omega sign σ^ω_cell (closes the sidedness hole, D2):**
- From the **same** N_avg=32 seed-averaged M=4000 mean field (no new compute), compute the **ROI-integrated net vorticity of the omega field**; **σ^ω_cell ∈ {+, −}** := its sign, with the **same negligibility floor** → **INDETERMINATE** → omega bands **two-sided** in that cell (where ANOMALOUS does not apply — §3; the veto remains failable there through GREEN and the blocking `INCONCLUSIVE_AT_CEILING`, D1).
- *(v3.3 said "the omega field's own P1-registered sign where declared" but registered no omega sign anywhere — so omega silently defaulted two-sided in every cell, the ANOMALOUS veto arm was dead code, and §13's one-sided arithmetic did not reconcile with the default branch. Closed: the sign is now a registered P1 output, and §13 states both branches.)*
- **No P1-B analogue for omega:** STABLE gates only cells whose primary RED **certifies** the claim; omega (and occupancy) only ever **block** — a veto needs no stability precondition to be conservative.

**P1-B — the sign-stability robustness test (unchanged):** disjoint predeclared set, per-seed ROI curl at M=400; **STABLE iff ≥ 12/16** (**N = 16** seeds `precond_P1::78001…78016`) agree in sign with σ_cell.

**Consequence for the pivot (frozen, unchanged):** an **UNSTABLE** cell does not count toward the all-RED pivot from an M=400 null (§5); remedy path via §8 step 4 only.

**Why STABLE is the *suspenders* — SCOPED [v3.4]:** the aniso current is *generated by* the grid curl (receipt 07). Because P1-B's per-seed M=400 curls share the underlying **curl field** with the scout, a cell whose true current opposes its registered σ_cell will tend to fail the ≥12/16 agreement and register UNSTABLE — ***when the curl→current transduction is not inverted* [v3.4 scope]. Under transduction inversion (the curl is right; the transduced `quad_loop_rate` responds with the opposite sign), P1-B — which measures CURL sign agreement, i.e. shares the curl, NOT the response — passes 16/16 while the true current opposes σ_cell: in that regime the suspenders are structurally INERT and the belt (the `|μ̂|` magnitude bound, §3) is the SOLE wrong-sign guarantee** (measured belt-only invalid pivot ≈ 0.0006 under the v3.4 ladder, reband channel ≈ 4×10⁻⁵ — §13; ≤ 0.02, gate 5). The OC sim measures the joint rate over **ρ ∈ {−1, 0, 0.5, 1, 2}** — the inverted and uncoupled regimes are mandatory arms, not optional sensitivity (§9.1) — *(v3.3's all-positive sweep {0.5, 1, 2} certified the two-layer guarantee only where the second layer cannot fail — D6, closed)*.

**Note (receipt 07, unchanged):** the quick per-seed SNR metric is informative but not the instrument.

### 1.2 Precondition P2 — crossed Tc×M diagnostic as a GATE (Q5-P2 — unchanged from v3.3; full-roster registration made explicit [v3.4])

Crossed `{Tc ∈ 1, 2, 4} × {M ∈ 400, 4000}` = 6 arms, equal-τ, receipt-06 rig (DIAG 2). P2 completes before the scout; its output freezes the Tc-cell M, claim class, **gating roster**, and the pivot claim's surviving design points.

**Frozen estimator + sampling (unchanged):** n = 40 blocks/arm; sample block-SD of per-block `quad_loop_rate` per arm; percentile bootstrap 10 000 resamples, rng 999, 90% two-sided CI. `R(Tc) = SD(Tc, M=400) / SD(Tc, M=4000)`. **Material** ⇔ 90% CI lower bound > 1.10; **M-invariant** ⇔ 90% CI within [0.909, 1.10] (TOST); **Inconclusive** ⇔ neither → bump once to n=80 → still inconclusive ⇒ demote.

**Action table (frozen — unchanged from v3.3):** M-invariant → run at M=400, stays gating; material + feasible → run at the M restoring equivalence (default 4000), stays gating; material + infeasible OR persistently inconclusive → **demoted to DESCRIPTIVE** with the pinned consequences below.

**DEMOTION CONSEQUENCES (v3.3, retained in full; clause 3 extended [v3.4]):**

1. **Leaves the gating roster.** The registered post-P2 gating roster is written into the prereg as an explicit list and asserted by `pivot_licensed()` (§7). **[v3.4] The prereg ALSO registers the FULL roster (gating ∪ demoted = all cells the scout runs); `pivot_licensed()` asserts `omega_bands` and `occupancy_bands` cover the FULL roster and `descriptive_bands` covers exactly FULL − GATING** (D5).
2. **Shrinks the pivot claim** per the §2.1 design-point map (AxT2/AxT4 sole carriers; their points leave the claim). Roster-parametric claim text, never hardcoded.
3. **Still banded, for the record, on ALL THREE statistics [v3.4]**, with pinned dispositions:
   - Primary GREEN → forces outcome 1 (no pivot). Primary ANOMALOUS → §8, blocks until dispositioned.
   - `omega_roi` GREEN or ANOMALOUS → omega veto (§5(iii)), blocks, HQ-flagged. **[v3.4] `omega_roi` `INCONCLUSIVE_AT_CEILING` on a DEMOTED cell: recorded, non-blocking (its design point is outside the claim), mandatory caveat** *("omega unresolved at demoted cell(s) {…}")*.
   - **[v3.4] `occupancy_x` GREEN → occupancy veto (§5(iii′)), blocks, HQ-flagged** — same reach as the omega veto: a super-floor current anywhere the scout looked, in any banded statistic, must never coexist with a minted null.
   - Primary RED / AMBER / `INCONCLUSIVE_AT_CEILING` → recorded, non-gating, **mandatory verdict caveat** that its design point is unbounded (law-#4 grep item, §10).
4. **Selftest (law #2):** S9 (§9.2) plants a super-floor current at a demoted cell; asserts the claim never covers its design point, a demoted-cell GREEN forces outcome 1, **and [v3.4] a demoted cell MISSING from `omega_bands`/`occupancy_bands`/`descriptive_bands` returns False (assertion (d))**.

**No pending state.** After P2, the Tc-cell M, claim class, gating roster, full roster, and claim scope are frozen constants in the registered prereg.

### 1.3 Diagnostic language (frozen at n=20 reality — unchanged from v3.1/v3.2/v3.3)

- Floor is trajectory-limited even at scale 10 (DIAG 1); raising M does **not** lower the floor.
- κ-injection suppression NOT established: quad 0.90 (~0.5σ); omega 0.67 (~2.2σ uncorrected, does not survive Holm). Quad-primary rests on v4.3 G1 continuity.
- Net relative sensitivity at M=400: quad ≈ 0.90, omega ≈ 0.83 → quad wins (D1↔D3). Omega's 0.83 is why the claim is statistic-scoped and the omega veto exists — **[v3.4] and why omega gets the stronger (ladder-driving, INCONCLUSIVE-blocking) guard while occupancy — no stated sensitivity calibration, no registered sign — gets the GREEN-veto + caveat guard (D1″ asymmetry rationale; forks 12/13).**

---

## 2. Estimand + exact thresholds

### 2.1 Pinned estimand — option (a), a **screening/triage** statistic (Q1; claim wording extended to occupancy [v3.4])

μ̂ (per cell, per statistic) = the mean of the **raw mismatch current** over the scout blocks. Screening proxy; honest SE folds in the v4.3 64-block equal-arm reference:

```
SE(B_scout) = sd_cell · √(1/B_scout + 1/64)
```

**Two distinct roles of "the equal arm" — do not conflate (auditor trip-wire, unchanged):** (1) `floor_c`'s SD source is the cell's own measured block SD as homoscedastic proxy; (2) the named equal-arm config (§6.1) defines the contrast estimand at Movement 3 only.

**Q1 — what estimand (a) may and may not claim (frozen; claim text re-worded [v3.4]):**
- A **GREEN** sizes a **candidate signal**; Movement 3 is the independent two-sample contrast test.
- An **all-RED pivot** is restricted to a **RAW-CURRENT claim** (ChatGPT option 2, HQ-recommended-pending-Anthony), with the **[v3.4] frozen whole-object-scoped wording:**

  > *"Raw mismatch currents are sub-floor **in the `quad_loop_rate` statistic** at the **N_g gating configurations** (the surviving design points **D_surv**), with `omega_roi` **banded on the shared ladder and resolved in every gating cell, nowhere GREEN/ANOMALOUS**, and `occupancy_x` **banded two-sided and nowhere GREEN** (not bounded; unresolved (AMBER) at cells {…} where applicable)."*

  where **N_g** and **D_surv** are the registered post-P2 gating roster and its design points (§1.2). In the no-demotion case this instantiates to the six cells ≈ **four independent design points** {(τy=2,Tc=1), (τy=1,Tc=1), (τy=2,Tc=2), (τy=2,Tc=4)} (A≡B, C≡D share the ROI mixed-partial to 4 s.f., receipt 07), NOT a continuum. **Under demotion the claim SHRINKS** per the design-point map (§2.1 of v3.3, retained verbatim: A/B and C/D mutually cover; AxT2/AxT4 are sole carriers whose points leave the claim). The pivot does **not** claim coverage of interior/unprobed (τx, τy, Tc) values, does **not** bound `omega_roi` or `occupancy_x` (it asserts only that neither raised a veto and omega was resolved), and is **not** a contrast claim.
- **Tc cells (Tc>1): estimand-(a) REFUSED as contrast licensing (Q6-iii, frozen).** Any high-Tc GREEN requires a measured two-sample contrast at confirmatory.

> **Scope note (v3.2, retained).** "≈ four independent design points" is claim-scope (physical degeneracy), never applied to soften a stochastic rate; OC rates use independent per-cell block noise (reproduces receipt-06 anchors).

> **Statistic-scope note (v3.3, extended [v3.4]).** The claim names ONE bounded statistic. What it asserts about omega is the veto + **resolution** clause; what it asserts about occupancy is the banding + no-GREEN clause + explicit non-boundedness. *(v3.3's "occupancy recorded and unbounded" — a recorded statistic with no band and no guard — was the recorded-statistic costume of the same category error; superseded, D3.)*

**Options for the contrast-licensing question (Anthony ratifies — fork §11):** unchanged; HQ writes v3.4 around option 2.

### 2.2 Frozen convention (law #4 grep-consistency — unchanged from v3.3)

One-sided Student-t at (n−1) df, α=0.05 for GREEN/RED in the predicted direction; two-sided at (n−1) df, α=0.05 for INDETERMINATE-sign cells (primary via σ_cell; **omega via σ^ω_cell [v3.4]**; **occupancy always two-sided [v3.4]**).

| df (n−1) | one-sided t (0.95) | two-sided t (0.975) |
|---|---|---|
| 7  (8 blocks)  | 1.895 | 2.365 |
| 15 (16 blocks) | **1.753** | **2.131** |
| 31 (32 blocks) | 1.696 | 2.040 |
| **55 (56 blocks — §8/§8-Ω powered rerun) [v3.5 — raised from 39/40]** | **one-sided 1.673** | **two-sided 2.004** |

### 2.3 Exact thresholds table (unchanged from v3.3 — all grep-consistent; applies per statistic)

| Config (blocks / B_conf) | floor_c | SE = sd·√(1/B+1/64) | **GREEN x >** (1-sided) | **GREEN \|μ̂\| >** (2-sided) | **RED \|μ̂\| < κ (magnitude bound)** |
|---|---|---|---|---|---|
| **16 / 96  (OPERATIVE first pass)** | 0.557·sd | 0.2795·sd | **1.047·sd = 1.88× floor** | 1.153·sd = 2.07× floor | **0.067·sd** (one-sided κ) — two-sided κ = **−0.039 < 0 → RED unreachable** |
| 8 / 96   (legacy-block reference) | 0.557·sd | **0.3750·sd** | 1.267·sd = 2.28× floor | 1.444·sd | one-sided κ<0 → **unreachable** |
| 32 / 96  (AMBER block-extension) | 0.557·sd | 0.2165·sd | 0.924·sd = 1.66× floor | 0.998·sd | one-sided κ = **0.190·sd**; two-sided κ = **0.115·sd** (reachable) |
| 32 / 128 (AMBER B_conf escalation, ceiling) | 0.482·sd | 0.2165·sd | 0.849·sd = 1.76× floor | 0.924·sd | one-sided κ = **0.115·sd** |
| **56 / 96 (§8/§8-Ω powered rerun — significance test against 0 only, not a banding config) [v3.5 — raised from 40]** | 0.557·sd | **0.1830·sd** | *(fires at \|x\| > t·SE = 1.673·0.1830 = **0.306·sd**)* | *(n/a)* | *(reband-look κ₅₆ = 0.557 − 0.306 = **0.251·sd** [v3.5 — supersedes v3.4's κ₄₀=0.217·sd; used in the reband-channel accounting, §13])* |
| *8 / 64 (v2 legacy reference only)* | *0.682·sd* | *0.375·sd* | *1.393·sd = 2.04× floor* | *1.569·sd* | *unreachable (κ<0)* |

**Operative frozen GREEN (primary, 16b/B96, one-sided): x > 1.047·sd_cell. Operative frozen RED (16b/B96): `|μ̂| < 0.067·sd_cell`.** Two-sided RED unreachable at 16b (κ_2s = −0.039 < 0), reachable at 32b (κ_2s = +0.115) — v3.2 documentation retained; **[v3.4] note this now matters for omega and occupancy too: an INDETERMINATE-omega or occupancy cell cannot resolve RED before 32 blocks, which the shared ladder accommodates (§4) and §13's two-sided-branch numbers reflect.**

---

## 3. The four-band rule (exact inequalities — v3.2 magnitude bound retained verbatim; per-statistic sidedness pinned [v3.4])

Banded per statistic by the same arithmetic: **primary** `quad_loop_rate` with σ_cell (P1-A); **[v3.4] `omega_roi` with σ^ω_cell (P1-A(ω)) — one-sided where declared, two-sided where INDETERMINATE (ANOMALOUS does not apply two-sided; the omega veto stays failable there via GREEN + the blocking `INCONCLUSIVE_AT_CEILING`, §5(iii))**; **[v3.4] `occupancy_x` always two-sided (D1″ — no registered sign; GREEN on `|μ̂|` is direction-complete; ANOMALOUS does not apply)**. All three are stamped at the cell's single terminal rung of the shared §4 ladder. Let `t = t*(n−1 df)` per §2.2, `SE` per §2.1, `floor_c` per §2.3. Terminal ceiling label `INCONCLUSIVE_AT_CEILING` (Q4).

**One-sided (σ ∈ {+,−}).** Aligned statistic `x = σ · μ̂`.
- **GREEN**: `x − t·SE > floor_c`.
- **RED**: BOTH `x + t·SE < floor_c` AND `|μ̂| + t·SE < floor_c` (coupled-upper conjunction, §3.3) AND not ANOMALOUS.
- **ANOMALOUS**: `x < −t·SE` (significant against 0, one-sided α=0.05).
- **AMBER**: none of the above; extend (§4).

**Partition (complete, no gap), one-sided:** with κ = floor_c − t·SE > 0 at 16b/B96, RED = `|μ̂| < κ`; ANOMALOUS = `x < −t·SE`; GREEN = `x > floor_c + t·SE`; AMBER = remainder. RED/ANOMALOUS disjoint (κ < t·SE).

**Two-sided (σ = INDETERMINATE, and always for occupancy [v3.4]):** GREEN `|μ̂| − t·SE > floor_c`; RED `|μ̂| + t·SE < floor_c` (unreachable at 16b, §2.3); AMBER otherwise; ANOMALOUS n/a.

> **The v3.2 RED repair (retained):** the magnitude conjunction binds; a wrong-sign current at floor magnitude cannot band RED. **Finding-4 correction (retained):** ANOMALOUS keys on significance against 0. **Anomaly-rate arithmetic (v3.2 t₁₅ correction, retained in substance):** screen ≈ 0.0344/cell at 16b under null; **[v3.4] terminal rates under the SHARED ladder are re-measured in §13 (primary terminal ANOMALOUS ≈ 0.047/cell; six-cell ≈ 0.25 — the standing 0.20 soft-cap breach carries over unchanged, advisory/non-blocking, fork 9).**

**§3.1 GREEN meaning (retained):** candidate-selection (§10); a demoted-cell GREEN forces outcome 1; an omega GREEN is a veto + HQ-flagged omega candidate consideration; **[v3.4] an occupancy GREEN is a veto + HQ-flagged occupancy candidate consideration (same amendment discipline — occupancy is not the calibrated primary).**

**§3.2 ANOMALOUS meaning (retained):** significant wrong-direction current; triggers §8 (primary) or **§8-Ω (omega) [v3.4]** — both **powered** (**n_rerun=56 [v3.5 — raised from 40]**).

### 3.3 RED robustness — v3.1 coupled-upper conjunction kept EXACTLY (Q3 PASS), applied to `|μ̂|` (v3.2) — unchanged in v3.4

```
RED  ⇔  ( x   + t·SE(sd̂)      < floor_c(sd̂)      )  AND  ( x   + t·SE(sd_upper) < floor_c(sd_upper) )   # aligned (v3.1, verbatim)
   AND  ( |μ̂| + t·SE(sd̂)      < floor_c(sd̂)      )  AND  ( |μ̂| + t·SE(sd_upper) < floor_c(sd_upper) )   # magnitude (v3.2)
   AND  ( NOT ANOMALOUS )
```
`sd_upper = sd̂ · √((n−1)/χ²_{0.05,n−1})`, factors **1.797 (n=8), 1.437 (n=16), 1.268 (n=32)**. The 4×10⁶-draw §3.3 MC (point-sd 3.95%, floor-only upper-sd 18.86%, coupled-upper 4.93%, conjunction 3.95%; Antigravity R2 reproduced) is unchanged. Q3 caveats retained: the MC validates LOCAL behavior; the whole-loop instrument is the §9 OC sim; sd_cell-as-equal-arm-proxy is a stated assumption under option 2.

---

## 4. AMBER terminal rule + B_conf escalation → INCONCLUSIVE_AT_CEILING (Q4 — SHARED ladder [v3.4])

A cell may not sit in AMBER forever. **[v3.4] The ladder is now driven by the primary AND the omega secondary — the D1 repair.** The terminal ladder, per cell, in order:

1. **One block-extension: 16 → 32 blocks** (accumulation, not redraw — preserved in the OC sim). **[v3.4] Taken iff the primary OR `omega_roi` is AMBER at 16b/B96** (exception: a primary GREEN or primary ANOMALOUS short-circuits the ladder — outcome 1 / §8 preempt; omega is stamped at that rung, an AMBER omega there recorded UNRESOLVED with the pivot already off the table; after a §8 GRID-ARTIFACT reband, omega is re-stamped from the same powered **n_rerun=56 [v3.5]** blocks).
2. **Still (primary OR omega) AMBER against floor(96) at 32 blocks → escalate B_conf 96 → 128** (re-band the same 32-block sample).
3. **Still AMBER against floor(128) at 32 blocks → `INCONCLUSIVE_AT_CEILING`** for whichever statistic(s) remain AMBER. B_max = 128 is the declared compute ceiling.

**All three statistics are stamped at the cell's single terminal rung** (one look of record per statistic per cell — the sim and `analyze()` share this one pinned rule, couple 7). `occupancy_x` does **not** drive the ladder (D1″ asymmetry, forked): it is banded at whatever rung the cell terminates on; a terminal occupancy AMBER is recorded + caveated, never laddered further and never `INCONCLUSIVE_AT_CEILING`.

**Q4 repair (retained + extended [v3.4]).** A **primary** `INCONCLUSIVE_AT_CEILING` on a gating cell BLOCKS the pivot (unchanged). **[v3.4] An OMEGA `INCONCLUSIVE_AT_CEILING` on a gating cell ALSO BLOCKS the pivot** (§5(iii)): the claim asserts omega was "nowhere GREEN/ANOMALOUS", which is only assertable where omega was resolved — an omega CI still overlapping the floor at the ceiling is an unresolved secondary, not a cleared one. On a **demoted** cell, omega INCONCLUSIVE is recorded + caveated, non-blocking (its design point is outside the claim; §1.2 clause 3).

> **Why this is the D1 fix and not a compute blow-up:** the omega-driven extension raises expected blocks/cell only from ≈ 28 to ≈ 31 (+~9%; measured rung distribution under null, ρ_qω=0: 8.4% terminate at 16b, 49.2% at 32b/B96, ~0% at 32b/B128 re-band, 42.4% reach the ceiling — §13), because most omega AMBERs resolve on the same 32-block extension the primary ladder already takes. What it buys: a +2×floor omega current can now escape the veto **only by banding omega RED** (P ≈ 1.4×10⁻⁵/cell) — never by running out of looks — which is what drives gate 8 from a measured **breach (≈ 0.0075 > 0.005)** under the v3.3 stamp rule to **≈ 10⁻¹¹** (§13), robustly across sidedness branches.

---

## 5. The pivot rule — four honest terminal outcomes + whole-object guards (v3.4: shared-ladder omega veto, occupancy veto, powered dispositions, full-roster assertions)

The scout ends in exactly one of **four** honest terminal outcomes:

1. **GREEN candidate** — ≥1 cell GREEN on the primary (gating OR demoted) → register the Movement-3 two-sample contrast at the tie-break cell (no pivot).
2. **All-actual-RED pivot** — pivots to the closed no-reset NESS protocol **iff all pivot conditions below hold**. The claim is the **[v3.4] frozen scoped wording of §2.1** — not a contrast claim, not a continuum claim, not a claim about any statistic other than `quad_loop_rate`, not a claim about any demoted design point.
3. **ANOMALOUS / omega-flag / occupancy-flag → investigate** — ≥1 primary ANOMALOUS (gating or demoted), or ≥1 omega veto (omega GREEN/ANOMALOUS in any cell), **or [v3.4] ≥1 occupancy veto (occupancy GREEN in any cell)** → §8 (primary) / **§8-Ω (omega/occupancy — powered [v3.4])**; no pivot and no terminal-null decision while any flag is open.
4. **INCONCLUSIVE at compute ceiling** — ≥1 gating cell `INCONCLUSIVE_AT_CEILING` **on the primary OR [v3.4] on `omega_roi`** (and no GREEN/ANOMALOUS/veto forcing outcomes) → the scout halts with a legitimate bound. Not a null, not a failure.

**Pivot conditions for outcome 2 (ALL must hold; conditions quantify over the REGISTERED POST-P2 GATING ROSTER except where a demoted-cell disposition (§1.2 clause 3) or the vetoes (iii)/(iii′) explicitly reach wider):**
- **(0) No open anomaly:** no gating cell ANOMALOUS on the primary, and no demoted cell with an open primary ANOMALOUS. Exit from ANOMALOUS only via the powered §8 machine.
- **(0′) No open inconclusive (Q4, extended [v3.4]):** no gating cell `INCONCLUSIVE_AT_CEILING` **on the primary or on `omega_roi`**.
- **(i) Terminal-band condition:** gating roster non-empty; every cell in it is actual RED on the primary (magnitude bound intrinsic — the belt).
- **(ii) Instrument precondition (the suspenders):** `stable_cell = STABLE` for every counted RED. *(Scoped [v3.4]: the suspenders' guarantee holds only in non-inverted transduction regimes; in inverted/uncoupled regimes the belt is sole and is measured there — §1.1, §9.1.)*
- **(iii) Omega veto (statistic axis; look-fixed [v3.4]):** in every cell (gating and demoted), the `omega_roi` band **stamped at the cell's terminal rung of the SHARED ladder** is neither GREEN nor ANOMALOUS, **and on every GATING cell omega is RESOLVED (not `INCONCLUSIVE_AT_CEILING`)**. If an omega GREEN/ANOMALOUS is recorded: pivot BLOCKED, HQ-escalated; disposition — omega GREEN → Movement-3 omega candidate consideration via formal amendment; omega ANOMALOUS → **§8-Ω, whose STATE-B vanish test is the SAME powered n_rerun=56 test [v3.4 mechanism; n_rerun raised 40→56 in v3.5]** (an omega reband can un-block the pivot ONLY through that powered look + formal amendment; the channel is counted in S8's number of record, §13). *(v3.3 routed this to an unspecified "§8-style investigation" — an unpowered look could reband omega and un-block, D4; closed.)*
- **(iii′) [v3.4] Occupancy veto (recorded-statistic axis):** in every cell (gating and demoted), the `occupancy_x` two-sided band at the cell's terminal rung is **not GREEN**. An occupancy GREEN: pivot BLOCKED, HQ-escalated, dispositioned via §8-Ω under the same powered/amendment discipline. A terminal occupancy AMBER does not block but **must** appear in the claim caveat (§2.1). *(Asymmetry vs (iii) documented at D1″; stronger symmetric option is fork 12/13.)*
- **(iv) Roster assertion (cell axis):** the set evaluated in (0)–(ii) is exactly the registered gating roster — asserted mechanically (§7).
- **(v) [v3.4] Full-roster completeness (dict-denominator axis):** `omega_bands` and `occupancy_bands` cover **exactly the registered FULL roster** (gating ∪ demoted) and `descriptive_bands` covers exactly FULL − GATING — asserted mechanically (§7). A missing or extra key in ANY consumed dict returns False (registration-integrity flag, not a null). *(v3.3 asserted completeness for the gating dict only — the silent-shrink leak one dict over, D5; closed.)*

**Belt-and-suspenders + whole-object scope (restated [v3.4]):** a raw-current null is earned only when no cell showed a significant wrong-sign primary current (powered disposition), no sub-significance wrong-sign current at floor magnitude banded RED (the belt — the sole guarantee in inverted-transduction regimes, measured there), no gating cell was unresolved at the ceiling **on either the primary or omega**, no cell anywhere showed omega GREEN/ANOMALOUS **at a look sized by omega's own ladder**, no cell anywhere showed occupancy GREEN, every consumed dict covered its registered denominator exactly, and the registered gating cells are confidently sub-floor in `quad_loop_rate` magnitude with a stable-sign instrument. The claim covers exactly the surviving design points, one named statistic, two guarded secondaries, nothing more. The scout still "cannot fail": candidate, or bounded raw-current, or a named flag, or an honest ceiling bound.

**Upgrading to a contrast claim** requires option 1/3 or Movement 3 (unchanged). **GREEN tie-break** (outcome 1) unchanged from v3.3, demoted-cell GREENs included.

---

## 6. Per-cell configuration tables (unchanged from v3.3)

### 6.1 Equal-arm config per candidate cell (Q6-i adopted — τy-matched at matched Tc, conditional on Q1)

| Cell | (τx, τy) | Tc | Role | Equal-arm config (τy-matched, matched-Tc) | Design point carried |
|---|---|---|---|---|---|
| A    | (0.1, 2.0)  | 1 | widest horizon mismatch | (2.0, 2.0) @ Tc=1 | (τy=2, Tc=1) — shared with B |
| B    | (0.25, 2.0) | 1 | mismatch mid            | (2.0, 2.0) @ Tc=1 | (τy=2, Tc=1) — shared with A |
| C    | (0.1, 1.0)  | 1 | amplitude-only          | (1.0, 1.0) @ Tc=1 | (τy=1, Tc=1) — shared with D |
| D    | (0.25, 1.0) | 1 | replica bridge to v4.3  | (1.0, 1.0) @ Tc=1 | (τy=1, Tc=1) — shared with C |
| AxT2 | (0.1, 2.0)  | 2 | Tc sweep at widest pair | (2.0, 2.0) @ Tc=2 | (τy=2, Tc=2) — **sole carrier** (leaves the claim if demoted, §1.2) |
| AxT4 | (0.1, 2.0)  | 4 | Tc sweep at widest pair | (2.0, 2.0) @ Tc=4 | (τy=2, Tc=4) — **sole carrier** (leaves the claim if demoted, §1.2) |

Design-space degeneracy (A≡B, C≡D via receipt-07 mixed-partial, ≈ four independent design points in the no-demotion case), claim-shrink rule, and reviewer alternatives: retained verbatim from v3.3 §6.1.

### 6.2 Predicted-sign table (all TBD until P1 registers — omega column added [v3.4])

| Cell | (τx, τy, Tc) | Registered σ_cell (P1-A) | **Registered σ^ω_cell (P1-A(ω)) [v3.4]** | Banding |
|---|---|---|---|---|
| A    | (0.1, 2.0, 1) | **TBD by P1** (receipt-07 quick check leaned `+`, inconclusive) | **TBD by P1-A(ω)** | per statistic: one-sided if its σ∈{+,−}, else two-sided |
| B    | (0.25, 2.0, 1) | **TBD by P1** | **TBD by P1-A(ω)** | " |
| C    | (0.1, 1.0, 1) | **TBD by P1** (leaned `+`, inconclusive) | **TBD by P1-A(ω)** | " |
| D    | (0.25, 1.0, 1) | **TBD by P1** (v4.3 arm1 τx<τy ⇒ `+`, re-derive per cell) | **TBD by P1-A(ω)** | " |
| AxT2 | (0.1, 2.0, 2) | **TBD by P1** | **TBD by P1-A(ω)** | " |
| AxT4 | (0.1, 2.0, 4) | **TBD by P1** | **TBD by P1-A(ω)** | " |

`occupancy_x`: **always two-sided, no registered sign** (D1″). An INDETERMINATE cell (either statistic) uses the two-sided column and cannot band RED before 32 blocks (§2.3).

---

## 7. `band_cell()` + `pivot_licensed()` pseudocode (v3.4 — full-roster completeness + occupancy veto + omega-INCONCLUSIVE block added; `band_cell` unchanged from v3.2/v3.3)

Reference implementation for the additive functions in `analyze()`. Pure analysis; touches no harness physics. All arithmetic in units of `sd_cell`.

```python
def band_cell(mu_hat, sd_cell, n_blocks, B_conf, sigma_cell, stable_cell):
    """
    Band one scout cell on ONE statistic
    (called for quad_loop_rate AND omega_roi AND occupancy_x  [v3.4]).
    Returns (band, aligned_bound, floor_c), band in {GREEN, AMBER, RED, ANOMALOUS}.
    INCONCLUSIVE_AT_CEILING is set by the caller's terminal ladder (sec 4).
    sigma_cell in {+1, -1, None}; None => two-sided (P1 INDETERMINATE;
    always None for occupancy_x  [v3.4]).
    stable_cell in {True, False} (P1 sign-stability); consumed at the pivot.
    [BODY UNCHANGED from v3.2/v3.3 -- the magnitude-bound RED is retained verbatim.]
    """
    Z = 3.858                                   # z_{0.995} + z_{0.90}, verified
    df = n_blocks - 1
    two_sided = (sigma_cell is None)
    t = t_student(df, one_sided=not two_sided, alpha=0.05)   # sec 2.2 table

    def floor_c(sd):  return Z * sd * sqrt(2.0 / B_conf)      # sec 0.1
    def SE(sd):       return sd * sqrt(1.0/n_blocks + 1.0/64) # estimand (a), sec 2.1

    sd_up = sd_cell * chi2_upper_factor(df)     # sqrt((n-1)/chi2_{0.05,n-1}); sec 3.3

    x = abs(mu_hat) if two_sided else sigma_cell * mu_hat     # prediction-aligned

    if x - t * SE(sd_cell) > floor_c(sd_cell):
        return ("GREEN", x - t*SE(sd_cell), floor_c(sd_cell))

    if (not two_sided) and (x < -t * SE(sd_cell)):
        return ("ANOMALOUS", x - t*SE(sd_cell), floor_c(sd_cell))

    aligned = (x        + t*SE(sd_cell) < floor_c(sd_cell)) and \
              (x        + t*SE(sd_up)   < floor_c(sd_up))
    magnitude = (abs(mu_hat) + t*SE(sd_cell) < floor_c(sd_cell)) and \
                (abs(mu_hat) + t*SE(sd_up)   < floor_c(sd_up))
    if aligned and magnitude:
        return ("RED", abs(mu_hat) + t*SE(sd_cell), floor_c(sd_cell))

    return ("AMBER", x + t*SE(sd_cell), floor_c(sd_cell))


def pivot_licensed(gating_bands, stable_flags, omega_bands, occupancy_bands,
                   descriptive_bands,
                   REGISTERED_GATING_ROSTER, REGISTERED_FULL_ROSTER):
    """Sec 5 [v3.4]: pivot to closed no-reset NESS iff ALL hold. Guarded against
    vacuous truth, compute-ceiling-minted null (primary AND omega), wrong-sign
    magnitude leak (belt; STABLE suspenders), statistic-projection null (omega
    veto AT THE SHARED-LADDER LOOK + occupancy veto -- [v3.4]), and
    shrunk-denominator null on EVERY consumed dict (full-roster completeness
    -- [v3.4]; v3.3 asserted the gating dict only).

    gating_bands:      {cell: band} primary bands, registered post-P2 GATING roster
    stable_flags:      {cell: bool} P1-B STABLE, gating roster
    omega_bands:       {cell: band} omega_roi bands stamped at each cell's terminal
                       rung of the SHARED sec-4 ladder, REGISTERED FULL ROSTER
                       (gating AND demoted); may contain INCONCLUSIVE_AT_CEILING
    occupancy_bands:   {cell: band} occupancy_x two-sided bands at each cell's
                       terminal rung, REGISTERED FULL ROSTER          [v3.4]
    descriptive_bands: {cell: band} primary bands of P2-DEMOTED cells; must cover
                       exactly FULL - GATING (empty dict iff no demotion)
    REGISTERED_GATING_ROSTER: frozenset frozen into the prereg by P2 (sec 1.2)
    REGISTERED_FULL_ROSTER:   frozenset of ALL registered cells (gating u demoted),
                       frozen pre-P2                                  [v3.4]
    """
    GATING = set(REGISTERED_GATING_ROSTER)
    FULL   = set(REGISTERED_FULL_ROSTER)
    DEMOTED = FULL - GATING

    # (iv) ROSTER ASSERTION (v3.3) + (v) FULL-ROSTER COMPLETENESS [v3.4]:
    #     EVERY consumed dict's key set must equal its registered denominator.
    #     A silently-dropped or extra cell in ANY dict can never shrink the claim.
    if set(gating_bands.keys())      != GATING:   return False
    if set(omega_bands.keys())       != FULL:     return False   # [v3.4]
    if set(occupancy_bands.keys())   != FULL:     return False   # [v3.4]
    if set(descriptive_bands.keys()) != DEMOTED:  return False   # [v3.4]
    if not GATING <= FULL:                        return False   # registration sanity
    if not gating_bands:
        return False                             # nothing to bound the space

    # (iii) OMEGA VETO at the shared-ladder look [v3.4]:
    #   GREEN/ANOMALOUS anywhere blocks (as v3.3); AND an omega unresolved at the
    #   ceiling on a GATING cell blocks (the claim's "nowhere GREEN/ANOMALOUS"
    #   clause is assertable only where omega was RESOLVED -- the D1 repair).
    if any(b in ("GREEN", "ANOMALOUS") for b in omega_bands.values()):
        return False
    if any(omega_bands[c] == "INCONCLUSIVE_AT_CEILING" for c in GATING):
        return False                             # [v3.4] unresolved secondary
    # (demoted-cell omega INCONCLUSIVE: recorded + caveated, non-blocking, sec 1.2)

    # (iii') OCCUPANCY VETO [v3.4]: two-sided GREEN anywhere blocks.
    #   Terminal occupancy AMBER: non-blocking, MANDATORY claim caveat (sec 2.1).
    if any(b == "GREEN" for b in occupancy_bands.values()):
        return False

    # Demoted-cell primary dispositions (sec 1.2 clause 3):
    if any(b in ("GREEN", "ANOMALOUS") for b in descriptive_bands.values()):
        return False

    # (0) / (0') / outcome-1 guard over the gating roster:
    if any(b == "ANOMALOUS" for b in gating_bands.values()):
        return False                             # resolve via powered sec 8 first
    if any(b == "INCONCLUSIVE_AT_CEILING" for b in gating_bands.values()):
        return False                             # no ceiling-minted absence
    if any(b == "GREEN" for b in gating_bands.values()):
        return False                             # register at the GREEN cell instead
    if not all(b == "RED" for b in gating_bands.values()):
        return False                             # AMBER cells -> sec 4 ladder first
    # (ii) SUSPENDERS: every counted RED must be on a STABLE cell
    if not all(stable_flags[c] for c, b in gating_bands.items() if b == "RED"):
        return False
    return True
```

**[v3.4] Key diff from v3.3 pseudocode:** `band_cell` is **byte-identical** to v3.2/v3.3 (docstring updated only). `pivot_licensed` gains: **(v) full-roster completeness** on `omega_bands`, `occupancy_bands` (new dict), and `descriptive_bands` — v3.3 asserted only `set(gating_bands) == GATING`, so a demoted cell silently absent from the omega/descriptive dicts passed `any()` unexamined and the emitted claim ("omega … in any cell") could be false (D5); the **omega `INCONCLUSIVE_AT_CEILING` gating-cell block** (D1); and the **occupancy veto** (D3). The claim text emitted on `True` derives from `REGISTERED_GATING_ROSTER` via the §2.1 map (never hardcoded) **and [v3.4] must enumerate the terminal-occupancy-AMBER cells in the mandatory caveat.** The stamping of `omega_bands`/`occupancy_bands` at the shared-ladder terminal rung is part of the pinned interface: **the OC sim (§9) and `analyze()` must produce these dicts through the same §4 code path** (couple 7 — the D1 secondary hazard: a sim that ladders omega while the run stamps it at the primary's count certifies a veto the run does not implement).

---

## 8. Anomaly-resolution state machine (Q2 — structure unchanged; §8-Ω extension for omega/occupancy flags [v3.4])

*(State machine, discriminator, disposition table, amendment rule, selftest requirement carry over from v3.3 — including the POWERED STATE-B vanish test: **[v3.5] n_rerun = 56 fresh blocks** (raised from 40 — the rerun-power arbitration fix) under the cell's predeclared remedy recipe (precond namespace), one-sided **t₅₅ = 1.673** against 0, **SE = sd·√(1/56+1/64) = 0.1830·sd**, significance edge |x| > **0.306·sd**, honest (reference-uncertain, marginal) noncentral-t power **0.913 ≥ 0.90** at ∓1×floor(96) (ncp = 0.55685/0.1830 = 3.043), residual mislabel ≈ **0.087**, hard gate 9. **[v3.5 erratum, law #9 — corrects, does not erase]** v3.4 stated this power as 0.912 at n_rerun=40; that figure was Antigravity's power *conditional on an error-free 64-block reference* (a test actually running at α≈0.019). The honest α=0.05 power at n_rerun=40 is **0.858**, which fails law #3's compound-power precondition — hence the raise to 56 (`ARBITRATION_rerun_power.md`, HQ-arbitrated, 4-agent verified). The reband channel is counted in the numbers of record — **[v3.5]** recomputed for n_rerun=56 under the honest model throughout (the v3.4 reband-RED sub-probability had itself been computed under the same reference-conditional model as the erratum, an inconsistency now closed): reband-look RED needs |μ̂₅₆| < κ₅₆ = 0.251·sd, so P(reband lands RED | real −1×floor, honest model) ≈ **0.047**; channel contribution to gate 5 ≈ **1.2×10⁻⁴** (immaterial to the ≤0.02 tolerance either way), §13.)*

```
STATE A (entry): cell is ANOMALOUS at M=400 (primary statistic).
  --> Powered rerun: n_rerun = 56 FRESH blocks [v3.5, raised from 40], remedy recipe, precond namespace.
STATE B (powered vanish test): wrong-sign significance FAILS --> GRID-ARTIFACT
  (mislabel ~0.087 at -1x floor [v3.5 -- honest power 0.913 at n=56;
  v3.4's 0.088 was derived from the erratum 0.912 at n=40]); re-band under
  the higher-M recipe via amendment;
  [v3.4] omega_roi and occupancy_x are RE-STAMPED from the same 56 rerun blocks [v3.5]
  (a powered look -- no throttled secondary re-entry). Reband channel counted
  (gate 5 / S5). Significance PERSISTS --> STATE C.
STATE C: persistent sign OPPOSES robust sigma_cell --> TRUE-OPPOSITE-PHYSICS
  (Movement-3 contrast in observed direction; never counts toward the pivot).
  sigma_cell mis-registered --> SIGN-PRECONDITION-FAILURE (cell excluded =
  demoted; claim SHRINKS per sec 1.2; roster assertion consumes amended roster).
STATE D: infeasible / inconclusive --> UNRESOLVED; blocks indefinitely; outcome 3.
```

**[v3.4] §8-Ω — the omega/occupancy disposition machine (closes D4).** An **omega ANOMALOUS**, a challenged **omega GREEN**, or a challenged **occupancy GREEN** dispositions through the **same machine applied to that statistic**: STATE-B rerun at the **same predeclared powered size, n_rerun = 56 fresh blocks [v3.5, raised from 40]** (t₅₅ = 1.673, SE = 0.1830·sd, edge 0.306·sd — the arithmetic is statistic-agnostic; **honest noncentral-t power 0.913 ≥ 0.90 at ∓1×floor(96)** for the flagged statistic, asserted **per-contrast** in-sim as **gate 9Ω**; **[v3.5] gate 9Ω additionally requires the COMPOUND six-cell power ≥ 0.90 verified by Monte-Carlo (law #3), not the per-contrast analytic figure alone** — the registration-grade OC simulator (§9, a separate build) must confirm this before registration). A flagged secondary can be rebanded non-vetoing — and the pivot un-blocked — **ONLY** through this powered look + formal amendment (law #1/#9). *(v3.3 §5(iii) routed omega ANOMALOUS to an unspecified "§8-style investigation" with the powered n pinned only for the primary: a ~0.61-power look could formally disposition a real −1×floor omega current as artifact, reband it AMBER, and un-block the pivot through a channel absent from every gate's numbers — the §8 evidence-destruction defect re-entering on the omega branch. Closed: the omega-reband channel is simulated in S8's wrong-sign sub-case and counted in S8's number of record, §13.)* **[v3.5]** *(v3.4's n_rerun=40 gave a stated power of 0.912; the honest α=0.05 figure was 0.858, which does not clear law #3 compound-power — see the erratum in §13 and `ARBITRATION_rerun_power.md`.)*

| Classification | Disposition | Counts toward pivot? |
|---|---|---|
| GRID-ARTIFACT | re-band under higher-M recipe (amendment) — only after failing the POWERED **n_rerun=56 [v3.5, raised from 40]** vanish test; **[v3.4] secondaries re-stamped from the powered blocks** | yes, at the re-banded result — channel counted (S5/S8) |
| TRUE-OPPOSITE-PHYSICS | Movement-3 contrast in observed direction; retention ≈ 0.91 given surfaced (**[v3.5] 0.913 honest, n_rerun=56**) | **no** |
| SIGN-PRECONDITION-FAILURE | cell excluded (= demoted); claim shrinks with the roster | **no** (until amended prereg) |
| UNRESOLVED | scout halts in outcome 3, flag named | **no** |
| **[v3.4] Ω-flag ARTIFACT** (omega/occupancy flag fails the powered rerun) | secondary rebanded via amendment; pivot re-evaluable | n/a (veto lifted through the powered path only) |
| **[v3.4] Ω-flag REAL** (flag persists at the powered rerun) | omega GREEN → Movement-3 omega candidate; occupancy GREEN → Movement-3 occupancy candidate; omega ANOMALOUS → HQ escalation (transduction / sign investigation) | **no — pivot stays blocked** |

**Step 4 — amendment rule (frozen, unchanged):** config regeneration, new `config_hash` + `source_sha` + prereg sha256, verify readback, then run; corrections supersede, never erase; a roster-changing amendment re-issues the claim-scope text.

**Selftest requirement (law #2, extended [v3.4]):** the OC sim must simulate the **entire** §8 loop for the primary (S5) **and the §8-Ω loop for a planted wrong-sign omega current (S8 sub-case)** — both powered reruns, both reband re-entries.

---

## 9. OC SIMULATION SPECIFICATION (Q4/Q7; the next build phase implements this — v3.4: shared-ladder implementation pin, extended ρ/ρ_qω grids, S10, gates 8/9Ω/11, missing-key selftests)

The selftest operates on the **entire frozen state machine** with predeclared acceptance criteria (law #3: analytic per-contrast power lies — v4.3: 0.998 analytic vs 0.655 compound; **[v3.4] and gate 8's own "≲ 10⁻³" was asserted-not-computed and wrong by ~7× — every expected value below is now computed, §13**). Registered as part of the prereg; must run and pass before the scout is licensed.

### 9.1 Simulation model (implementable — v3.4 additions in **bold**)

- **Null-SD calibration (receipt 06).** Per-block SD of `quad_loop_rate`: Tc1 = 5.03e-5, Tc2 = 6.29e-5 (×1.25), Tc4 = 8.15e-5 (×1.62). Band arithmetic scale-free in `sd_cell`.
- **Draw model.** Each block statistic ~ N(Δ, 1) per statistic; 32-block extension reuses the first 16 and appends 16 (accumulation); B96→B128 re-bands the same 32-block sample. sd̂ sample SD; `sd_upper` via χ² factor.
- **[v3.4] Shared-ladder pin (the D1 secondary hazard).** The sim's per-cell termination rule IS §4's: extend while primary OR omega is AMBER (primary GREEN/ANOMALOUS short-circuit); all three statistics stamped at the single terminal rung. **The sim and `analyze()` must share this one code path (or byte-identical logic verified by the S8 assertion): a sim that ladders omega while the run stamps it at the primary's terminal count certifies a veto the run does not implement.** S8 asserts the stamped-look block counts recorded in the output equal the ladder's terminal rung for both statistics.
- `band_cell` with the magnitude bound (v3.2). SE_FACTOR n=8 = **0.375** (law #4).
- **P1 modeling (extended [v3.4]):** σ_cell from P1-A; STABLE from N=16 coupled M=400 per-seed curls sharing the cell's true CURL (per-seed curl ~ N(Δ_curl, σ_curl²), Δ_curl = ρ·Δ); **sensitivity ρ ∈ {−1, 0, 0.5, 1.0, 2.0} — the ρ = −1 (inverted transduction: curl agrees with σ_cell while the transduced current opposes it, STABLE passes by construction) and ρ = 0 (uncoupled) arms are MANDATORY**, because they are the regimes where the suspenders are inert and the belt must carry the guarantee alone (D6). Gate 5's number of record is reported per ρ arm. **σ^ω_cell from P1-A(ω) [v3.4]; both sidedness branches (one-sided and INDETERMINATE/two-sided omega) are simulated and reported.**
- **Omega joint modeling (v3.3, retained):** each block carries a (quad, omega) pair; ρ_qω ∈ {0, 0.3, 0.6} predeclared sweep. **[v3.4] Each block additionally carries `occupancy_x`; quad↔occupancy correlation ρ_qc swept over the same grid {0, 0.3, 0.6}** (same trajectories — independence never silently assumed).
- **§8 loop modeling (v3.3, retained + extended [v3.4]):** full powered STATE-B rerun + reband re-entry for the primary (S5) **and for the omega branch (§8-Ω; S8 wrong-sign sub-case)**; reband channels counted in gates 5 and 8's numbers of record.
- **Demotion modeling (v3.3, retained + extended [v3.4]):** roster-parametric claim emission asserted; **the missing-key plants (S9 assertion (d), §9.4) exercise every consumed dict.**
- **Correlated A≡B/C≡D noise:** baseline independent (reproduces receipt-06 anchors); correlated model = fork 8 sensitivity item.
- **Trials + rng.** ≥ 1×10⁵ per scenario (≥ 1×10⁶ for tail estimates), rng pinned (**proposal seed = 20260710 [v3.4 — new sim, new pinned seed; the §13 draft-check seeds 20260708/20260709 are this session's HQ arithmetic, quarantined from the registered sim]**), `/usr/bin/python3` numpy 2.0.2. MC standard errors on every rate.

### 9.2 Scenarios (all six cells simulated jointly — S5/S8 extended, S10 NEW [v3.4])

| # | Scenario | Construction |
|---|---|---|
| S1 | **Global null** | all six cells Δ = Δ_ω = Δ_occ = 0. Measures: false-GREEN, false-anomaly (terminal), omega-veto null rate + **omega-INCONCLUSIVE null rate [v3.4]** + **occupancy-GREEN null rate [v3.4]** at each ρ_qω/ρ_qc, joint pivot-under-null, **rung distribution / expected blocks per cell [v3.4]**. |
| S2 | **One-cell predicted-direction at floor** | one cell Δ = +floor(96); rest null. P(invalid pivot) — gate 2. |
| S3 | **One-cell supra-floor sweep** | Δ ∈ {+1×, +2×, +3×} floor. Compound GREEN power + supra-floor invalid pivot — gates 3a/3b/4/7. |
| S4 | **Multi-signal / GREEN tie-break** | ≥2 supra-floor cells. |
| S5 | **Wrong-sign primary current at floor — full §8 loop, ρ grid [v3.4 extended]** | one cell Δ = −1×floor; rest null; STABLE from coupled P1-B draws **at every ρ ∈ {−1, 0, 0.5, 1, 2} — the ρ = −1 sub-case forces STABLE 16/16 by construction with a true opposing current (transduction inversion) and reports the BELT-ONLY invalid-pivot number** (D6). Full §8 machine (powered rerun, reband re-entry). Sub-cases −1×, −1.45×, −2× floor. Gates 5/5′/9. |
| S6 | **Tc-heteroscedastic** | receipt-06 SD scaling. |
| S7 | **Nonzero equal-arm offset** | μ_eq ∈ {0.10, 0.30}·floor. |
| S8 | **Omega-only current (statistic/look-axis failability, law #2) [v3.4 extended]** | quad Δ = 0 all six; cells A, B carry Δ_ω = +2×floor(96) = 1.114·sd; swept over ρ_qω and BOTH omega sidedness branches. The veto must block: **gate 8** = P(pivot \| S8) ≤ 0.005 — **now with omega banded on the shared ladder as `analyze()` stamps it** (the v3.3 throttled stamp measured 0.0075 here — the BLOCKER). Sub-cases: Δ_ω = +1×floor (advisory); **Δ_ω = −1×floor wrong-sign omega (the §8-Ω powered-disposition loop runs in-sim; measures the omega-reband channel and the veto-or-block rate) [v3.4]**. **Assertion: stamped omega look == ladder terminal rung (the sim-vs-run implementation pin, §9.1).** |
| S9 | **Demoted-cell leak (cell-axis failability) [v3.4 extended]** | AxT4 demoted (roster = 5); AxT4 carries Δ = +2×floor; gating cells null. Asserts: (a) licensed-pivot claim scope excludes (τy=2, Tc=4); (b) AxT4's descriptive GREEN forces outcome 1 / blocks; (c) roster assertion rejects AxT4-as-gating; **(d) [v3.4] AxT4 MISSING from `omega_bands`, from `occupancy_bands`, or from `descriptive_bands` (each planted separately) ⇒ `pivot_licensed` returns False — the D5 missing-key plants.** |
| **S10** | **[v3.4 NEW] Occupancy-only current (recorded-statistic-axis failability, law #2)** | quad Δ = Δ_ω = 0 all six; **all six cells carry Δ_occ = +2×floor** (the audit's construction: transduction manifests exactly as v4.3 — occupancy alone moves, quad and omega quiet). The occupancy veto must block: **gate 11** = P(pivot \| S10) ≤ 0.005. Sub-case Δ_occ = +3×floor reported. Swept over ρ_qc. Also planted at a **demoted** cell (veto reach). |

### 9.3 Predeclared acceptance criteria (v3.4 — every expected value COMPUTED this session, §13; HQ-recommended, pending Anthony)

**Hard gates (registration blocked if violated):**

| # | Criterion | Scenario | Tolerance (HQ-rec) | Expected (**computed** — MC this session under the v3.4 shared ladder, §13) |
|---|---|---|---|---|
| 1 | **P(any false GREEN)** | S1 | ≤ 0.01 | **≈ 0.002** (per-cell 0.0003, six-cell 0.0019) |
| 2 | **P(invalid pivot) — predicted-direction at floor** | S2 (Δ=+floor) | ≤ 0.02 | **≈ 0.0006** (carrier pivot-compatible 0.017 × null⁵ 0.034) *(v3.2's 0.0067 superseded by the shared ladder)* |
| 3a | P(invalid pivot) — predicted-direction 2× floor | S3 (+2×) | ≤ 0.005 | ≲ 10⁻⁶ (carrier primary-RED ≪ gate-2 case; MC-zero at 4×10⁴) |
| 3b | P(invalid pivot) — predicted-direction 3× floor | S3 (+3×) | ≤ 0.005 | ~0 (MC-zero) |
| 4 | **P(registrable GREEN)** compound power | S3 (+3× floor) | ≥ 0.90 | **≈ 0.9999** (per-carrier GREEN, measured) |
| 5 | **P(invalid pivot) — WRONG-SIGN at floor, incl. §8 reband channel, [v3.4] reported per ρ arm incl. ρ ∈ {−1, 0} (belt-only regimes)** | S5 (Δ=−floor), full §8 loop | ≤ 0.02 | **≈ 0.0007 belt-only [v3.5]** (carrier pivot-compatible 0.017 × null⁵ 0.034 ≈ 0.00057) **+ reband channel ≈ 1.2×10⁻⁴** (0.874 ANOM × 0.087 mislabel [n_rerun=56, honest power 0.913] × 0.047 reband-RED at κ₅₆=0.251 × null⁵); ~0 at ρ > 0 (belt+suspenders) *(v3.2/v3.3's ≈ 0.007 superseded; v3.4's ≈ 4×10⁻⁵ reband-channel figure superseded — it was computed at n_rerun=40 under the same reference-conditional model as the power erratum, §13)* |
| 5′ | **P(invalid pivot) — WRONG-SIGN ≥2× floor** | S5 (Δ=−2×floor) | ≤ 0.005 | MC-zero at 4×10⁴ (carrier pivot-compatible 0 observed) |
| 6a | Partition completeness (no limbo) | S1–S10 | = 0 | 0 |
| 6b | Zero cells terminate AMBER on a LADDERED statistic (deadlock) | S1–S10 | = 0 | 0 (terminal occupancy AMBER is a pinned, caveated non-laddered state, not a deadlock — §4) |
| 7 | law #2 — planted +3× primary signal breaks pivot | S3 (+3×) | ≥ 0.90 | ≈ 1.00 |
| **8** | **Omega veto failability — P(pivot \| omega-only +2×floor on A,B), AS STAMPED BY THE SHARED LADDER, at every ρ_qω and BOTH sidedness branches [v3.4]** | S8 | ≤ 0.005 | **≈ 10⁻¹¹ one-sided / ≈ 10⁻¹⁸ two-sided (computed: escape requires omega-RED, P ≈ 1.4×10⁻⁵/cell one-sided at 16b, ≈ 8×10⁻⁹/cell two-sided at 32b; MC-zero at 4×10⁴ cells/arm)** *(v3.3's stamp rule measured 0.0075 — BREACH; its "≲ 10⁻³" was asserted, not computed — D1/D7)* |
| 9 | **§8 vanish-test power at −1×floor (primary)** | S5 STATE-B | ≥ 0.90 **per-contrast, AND compound six-cell power ≥ 0.90 by MC [v3.5, law #3]** | **0.913** (n_rerun=56 [v3.5, raised from 40]; honest noncentral-t, ncp=3.043; per-contrast) — **compound six-cell MC power TBD by the registration-grade OC sim (§9), not yet computed** |
| **9Ω** | **[v3.4] §8-Ω vanish-test power at ∓1×floor (omega/occupancy branch)** | S8 wrong-sign sub-case | ≥ 0.90 **per-contrast, AND compound six-cell power ≥ 0.90 by MC [v3.5, law #3]** | **0.913** (same statistic-agnostic arithmetic at n_rerun=56, asserted per-contrast in-sim) — **compound MC TBD, same instrument as gate 9** |
| 10 | **Roster/demotion integrity — S9 assertions (a)(b)(c) [v3.4] + (d) missing-key plants on every consumed dict** | S9 | = pass (deterministic) | pass |
| **11** | **[v3.4] Occupancy veto failability — P(pivot \| occupancy-only +2×floor in all six cells)** | S10 | ≤ 0.005 | **Primary sub-case (+2×floor, hard-gated): ≈ 1.4×10⁻⁵** (per-cell occupancy GREEN 0.741). **[v3.5] Reported sub-case (+3×floor, NOT separately hard-gated, listed distinctly per Antigravity R3 Finding 2): ≈ 7×10⁻¹⁶** (per-cell occupancy GREEN 0.9945). *(v3.4 nested the +3× rate inside the +2× row's parenthetical; reformatted here as a distinct sub-case.)* |

**Reported / advisory operating characteristics (informative, NOT hard-gated):**

| Characteristic | Scenario | Advisory | Expected (**computed**, §13) |
|---|---|---|---|
| **P(correct pivot)** | S1 calibrated null | advisory (low is legitimate) | **≈ 0.017** at ρ_qω=0, one-sided omega (per-cell pivot-compatible 0.506–0.509); **≈ 0.0014** on the all-two-sided-omega branch. *(v3.3's ≈ 0.11 superseded — it priced the throttled stamp; positive ρ_qω raises the rate: the sweep is the number of record.)* **The operating point is Anthony's fork 2.** |
| P(≥1 gating-cell INCONCLUSIVE, primary or omega) | S1 | report | per-cell primary 0.306, omega 0.299 (shared ladder) |
| P(≥1 false anomaly, primary) | S1 | non-blocking; six-cell ≈ 0.25 breaches the 0.20 soft cap (fork 9) | per-cell terminal ≈ 0.047 |
| omega-veto null firing (GREEN/ANOM) | S1 | report at each ρ_qω | per-cell ≈ 0.030; six-cell ≈ 0.17 at ρ_qω=0 |
| **[v3.4] occupancy-veto null firing (GREEN)** | S1 | report at each ρ_qc | per-cell ≈ 10⁻⁴ (two-sided); six-cell ≈ 6×10⁻⁴ — negligible null cost |
| **[v3.4] expected blocks/cell (compute cost of the shared ladder)** | S1 | report | ≈ 31 (rungs: 8.4% @16b, 49.2% @32b/B96, ~0% resolve at B128 re-band, 42.4% ceiling) vs ≈ 28 under the primary-only ladder (+~9%) |
| anomaly-SCREEN power (standalone 16b) | S5 | report | ~0.61 at −floor |
| TRUE-OPPOSITE-PHYSICS retention | S5 | report | ≈ 0.874 × 0.913 ≈ 0.80 end-to-end at −1×floor **[v3.5 — 0.913 honest power at n_rerun=56, supersedes v3.4's 0.912@n_rerun=40]** |
| **[v3.4] wrong-sign omega veto-or-block** | S8 (Δ_ω=−1×floor) | report | per-cell ≈ 0.982 = 1 − P(omega falsely RED ≈ 0.018); components: ANOMALOUS 0.847 + blocking INCONCLUSIVE 0.119 (+ non-pivot short-circuit cells 0.015) |
| P(correct tie-break \| ≥2 GREEN) | S4 | advisory ≥0.90 | S4 |
| raw-vs-contrast gap | S7 | report | sizes the Q1 gap |

**Interpretation of the split (extended [v3.4]).** Only the safety criteria are hard gates. **P(correct pivot | null) falls again — ≈ 0.148 (v3.2) → ≈ 0.11 (v3.3, superseded arithmetic) → ≈ 0.017 (v3.4, one-sided omega, ρ_qω=0)** — the shared ladder + blocking omega-INCONCLUSIVE buy the look axis at a real reachability price. This is deliberately advisory: hard-gating a high pivot rate would pressure the design back toward minting absence. Anthony's fork 2 restates the choice with the alternatives (annotate-only omega-INCONCLUSIVE — which re-opens a 0.004–0.019 gate-8 straddle — documented and NOT HQ-recommended). The load-bearing gates: symmetric invalid-pivot bounds (2 ≈ 0.0006, 5 ≈ 0.0007 [v3.5]), omega failability at the implemented look (8 ≈ 10⁻¹¹), occupancy failability (11 ≈ 1.4×10⁻⁵), powered dispositions (9/9Ω per-contrast = 0.913 at n_rerun=56 [v3.5, raised from 40; honest power, supersedes v3.4's 0.912] — **AND compound six-cell MC ≥0.90 required by law #3, TBD by the registration-grade OC sim [v3.5]**), roster + dict integrity (10).

### 9.4 Boundary / cutpoint selftests (Q7 item 7 — v3.4 adds missing-key, occupancy, and shared-ladder cutpoints)

Deterministic assertions on `band_cell()`/`pivot_licensed()` — all v3.3 items retained (cutpoint equalities incl. ±κ; wrong-sign magnitude checks; one-vs-two-sided branches; anomaly boundary; sd-upper factors; empty/anomaly-only/inconclusive-only guards; terminal-ceiling behavior; UNSTABLE-RED block; omega-veto value cutpoints; roster missing/extra-cell; powered-rerun edge at **0.306·sd with n_rerun grep = 56 [v3.5, raised from 0.340·sd / 40]**), **plus [v3.4]:**

- **Missing-key plants (D5):** all-RED gating + full `omega_bands` minus ONE key ⇒ False; `occupancy_bands` minus one key ⇒ False; `descriptive_bands` missing a demoted cell ⇒ False; an EXTRA key in any of the three ⇒ False. *(v3.3's selftests planted only wrong gating keys and GREEN/ANOMALOUS values PRESENT in the other dicts — never a missing key.)*
- **Omega-INCONCLUSIVE block:** all-RED gating + omega `INCONCLUSIVE_AT_CEILING` on a GATING cell ⇒ False; same on a DEMOTED cell only ⇒ not blocked by that clause (caveat asserted present in the emitted claim).
- **Occupancy cutpoints:** all-RED gating + one occupancy GREEN (any cell, incl. demoted) ⇒ False; occupancy AMBER ⇒ no veto AND the emitted claim's caveat enumerates that cell; occupancy two-sided GREEN edge at `|μ̂| = floor_c + t·SE` resolves to the predeclared side.
- **Shared-ladder stamp:** a cell whose primary REDs at 16b while omega is AMBER at 16b must NOT be terminal at 16b (extends); both stamps at the terminal rung equal (n_blocks, B_conf) of that rung; **κ₅₆ grep = 0.251·sd [v3.5, raised from κ₄₀ = 0.217·sd]**.
- **σ^ω_cell branch:** an omega INDETERMINATE cell uses two-sided omega arithmetic; omega ANOMALOUS unreachable there (and the veto still failable via GREEN + INCONCLUSIVE-block — asserted).

---

## 10. Scope of changes if ratified (→ config_hash / prereg re-issue) — Q7

| Artifact | Change | Hash impact |
|---|---|---|
| `SCOUT_DECLARATION.md` decision-rule section | Replaced by §1–§8 of this document | none (declaration) |
| `analyze()` in `v44_scout.py` | Add `band_cell()` + `pivot_licensed()` (§7 — **[v3.4] with full-roster completeness, occupancy veto, omega-INCONCLUSIVE block**) + the **shared §4 ladder driving on primary OR omega [v3.4]** + `INCONCLUSIVE_AT_CEILING` — additive, does not touch the v4.3-inherited estimator or forward physics | new `source_sha` |
| `CFG["scout"]["blocks"]` | 8 → **16** (D2) | **new `config_hash` → re-issue prereg → new sha256** |
| **[v3.5]** `CFG["scout"]["n_rerun"]` (or equivalent §8/§8-Ω powered-rerun size) | 40 → **56** (rerun-power arbitration fix; honest power 0.858 at 40 → 0.913 at 56) | **new `config_hash` → re-issue `prereg_v44.json` → new sha256** (flagged now, NOT performed in this draft — do not touch the frozen `prereg_v44.json`) |
| B_conf convention | 64 → **96** (D4) | new `config_hash` if surfaced in CFG; else declaration-only |
| **P1 config** (§1.1) | high-M reference (N_avg=32@M4000), robustness (N=16@M400), ≥12/16 STABLE, per-cell remedy — **[v3.4] + P1-A(ω) omega sign registration (same seed set, ROI net vorticity, same negligibility floor)** | part of config_hash / prereg |
| **P2 config** (§1.2) | unchanged criteria + pinned demotion consequences + registered gating roster + claim scope — **[v3.4] + the registered FULL roster** | part of config_hash / prereg |
| **Anomaly SOP** (§8) | frozen machine + powered STATE-B (**n_rerun=56 [v3.5, raised from 40], honest power 0.913 per-contrast + compound MC ≥0.90 required [v3.5, law #3]**) — **[v3.4] + §8-Ω (same powered machine for omega/occupancy flags; gate 9Ω)** | **new** `config_hash` **[v3.5 — CFG["scout"] rerun size changes]** / prereg re-issue |
| **OC simulation script + expected-OC report** (§9) | **new v3.4 simulator** (shared-ladder pin, ρ ∈ {−1,0,0.5,1,2}, ρ_qω/ρ_qc sweeps, both omega sidedness branches, §8 + §8-Ω loops, S8 extended, S10, gates 8/9/9Ω/10/11, missing-key selftests) | part of prereg (new artifact) |
| **Baseline / equal-arm conditions** (§2.1, §6.1) | Q1 option (default option 2) | part of prereg |
| **Stale-prose flag (law #4)** | All v3.3 grep items retained (statistic qualifier in every pivot-claim string; roster-parametric claim generation; no hardcoded "six cells/four points"; demotion caveats; **n_rerun=56 / t₅₅=1.673 / 0.1830 / 0.306 [v3.5, raised from 40 / 1.685 / 0.2016 / 0.340]**), **plus [v3.4]:** any omega band stamped at a look other than the shared-ladder terminal rung; any "occupancy recorded and unbounded" without banding (must read "banded two-sided and nowhere GREEN"); any missing terminal-occupancy-AMBER caveat; any omega disposition without the powered **n_rerun=56 [v3.5]**; any completeness assertion covering fewer than ALL consumed dicts; **κ₅₆ = 0.251 [v3.5, raised from κ₄₀ = 0.217]**; any ρ sweep lacking the {−1, 0} arms; any §1.1 suspenders prose unscoped to non-inverted transduction; any hard-gate expected value not traceable to a computation; **[v3.5] any stale "0.912"/"n_rerun=40"/"t₃₉"/"0.2016"/"0.340"/"κ₄₀=0.217" string outside an explicitly historical or erratum context; any gate 9/9Ω assertion that cites per-contrast power alone without the compound-MC requirement** | Update per §13; the selftest grep-check must grep every constant named in this row | **new** `config_hash` **[v3.5]** / part of config_hash / prereg |

**Claim limits (Q7 item 8 — frozen, v3.4-scoped):** all v3.3 limits retained; the all-RED pivot claims sub-floor **in `quad_loop_rate`** at the registered gating configurations only, asserts about `omega_roi` only "banded on the shared ladder, resolved in every gating cell, nowhere GREEN/ANOMALOUS," asserts about `occupancy_x` only "banded two-sided, nowhere GREEN, not bounded" **with the terminal-AMBER cell list [v3.4]**, and says nothing about demoted design points beyond the mandatory unboundedness caveat.

**Unchanged and hash-frozen:** the forward-path harness (`pilot_pair`, Tc threading, the v4.3-inherited estimator), the six cells + geometry, the `v44pilot::` seed namespace, the never-pooled rule. Analysis + declaration recalibration only. Re-issue per law #1; **P1 (incl. P1-A(ω)) and P2 first, OC simulation (v3.4) passes, scout last.**

---

## 11. Ratification checklist + genuine forks left for Anthony

**Resolved into spec.** Every ChatGPT BLOCK/AMEND (Q1–Q7), the HQ re-pass BLOCK (v3.2), the whole-object audit findings (v3.3), and the whole-object re-pass findings (v3.4, §17) have a frozen repair above.

**Genuine forks — HQ recommends, Anthony ratifies:**

1. **Q1 contrast-licensing option.** HQ rec: option 2 (unchanged).
2. **The operating point (restated for v3.4 — the biggest call in this revision). [v3.5] HQ-recommended-pending-Anthony (revisable at ratification): the conservative operating point that preserves ≥0.90 compound power and the honest reference-uncertain belt guarantee.** Four honest repairs stack: Q4 ceiling, v3.2 magnitude bound, v3.3 omega veto, **[v3.4] shared ladder + blocking omega-INCONCLUSIVE**. Joint pivot-under-null: v3 **0.808** → v3.1 **0.349** → v3.2 **0.148** → v3.3 ≈ 0.11 (superseded arithmetic) → **v3.4 ≈ 0.017** (one-sided omega, ρ_qω=0; ≈ 0.0014 all-two-sided; positive ρ_qω raises it — OC sim is the number of record). **Alternatives, kept listed:** demote the omega-INCONCLUSIVE block to a mandatory claim caveat (documented, NOT recommended — re-opens a measured 0.004–0.019 gate-8 straddle), OR raise B_max above 128 to resolve more omega AMBERs. Compute cost of the shared ladder: ≈ +9% blocks/cell. **[v3.5] The honest-belt-guarantee criterion is now explicit: the operating point must be evaluated at the honest (reference-uncertain) SE throughout, consistent with the n_rerun=56 fix — not at any reference-conditional shortcut.**
3. **P1 seed sets + threshold + coupling** (unchanged) — **[v3.4] plus the P1-A(ω) negligibility floor** (HQ proposal: same floor as P1-A). Revisable.
4. **P2 estimator + criteria** (unchanged). Revisable.
5. **OC acceptance tolerances (§9.3).** Unchanged values; **[v3.4] gate 8 now measured at the implemented look (expected ≈ 10⁻¹¹), gate 9Ω ≥ 0.90, gate 11 ≤ 0.005 at +2×floor.** Revisable.
6. **Equal-arm choice (§6.1)** (unchanged).
7. **B_max = 128** (unchanged; couples to fork 2's INCONCLUSIVE mass).
8. **Correlated A≡B/C≡D block noise** (unchanged; measure-not-assert).
9. **Advisory false-anomaly cap value** (unchanged; six-cell ≈ 0.25 vs 0.20 soft cap; the omega-veto null channel ≈ 0.17 six-cell reported under the same discussion).
10. **Omega-veto strength** (v3.3): blocking (HQ rec) vs annotate-only. Unchanged.
11. **§8 rerun size n_rerun = 56 [v3.5, raised from 40 — the load-bearing rerun-power arbitration fix, no longer a live fork].** Honest noncentral-t power 0.913 ≥ 0.90 per-contrast at ∓1×floor(96) (power table §13); compound six-cell power ≥ 0.90 by Monte-Carlo still required (law #3) and TBD by the registration-grade OC sim. Revisable at ratification like every other adopted number, but not offered here as an open alternative-vs-alternative fork — see `ARBITRATION_rerun_power.md`.
12. **[v3.4 NEW] Occupancy guard strength. [v3.5] HQ-recommended-pending-Anthony (revisable at ratification): the current asymmetry as written.** HQ writes v3.4/v3.5 with occupancy **banded two-sided + GREEN veto + mandatory caveat for terminal AMBER** (D1″). Alternatives, documented and KEPT: (a) weaker — record-only with caveat (rejected by HQ: re-creates the D3 costume); (b) stronger — occupancy drives the ladder and its INCONCLUSIVE blocks, symmetric with omega (costs: pivot-under-null collapses further, ≈ 3×10⁻⁴ ballpark, and +compute; buys: a sub-GREEN occupancy current can no longer coexist with a pivot). **HQ rec: the middle option as written** — occupancy has no registered sign, no calibrated sensitivity, and no v4.4-estimand standing; GREEN-veto + caveat guards the super-floor-visible case (the audit's scenario) at negligible null cost; and its v4.3 direction is protocol-bound (law #8), so it does not warrant the stronger symmetric guard. The symmetric alternative (b) remains available as Anthony's fork. Anthony's call.
13. **[v3.4 NEW] Occupancy sidedness.** HQ pins two-sided/no-sign-registration (direction-complete; v4.3's direction is protocol-bound, law #8). Alternative: register σ^occ from the v4.3 record and band one-sided (rejected by HQ: imports a reset-protocol direction into a closed-NESS prediction — a law-#8 category mix). Anthony's call.

---

## 12. ChatGPT Q1–Q7 reconciliation (all v3.1/v3.2/v3.3 satisfactions PRESERVED in v3.4)

| ChatGPT Q | v3.1–v3.3 resolution | v3.4 status |
|---|---|---|
| **Q1** — contrast-proxy estimand | raw-current claim (option 2); Tc>1 refusal; GREEN=candidate-selection; statistic-scoped + roster-parametric claim | **preserved + completed:** the claim's secondary-statistic clauses now match what is actually guarded (omega resolved + nowhere GREEN/ANOMALOUS; occupancy banded + nowhere GREEN) (§2.1, §5, §10) |
| **Q2** — four-band / ANOMALOUS | frozen anomaly machine; t₁₅ correction; powered STATE-B (v3.3) | **preserved + extended:** §8-Ω applies the same powered machine to omega/occupancy flags (gate 9Ω) — no unpowered disposition path remains anywhere (§8) |
| **Q3** — RED conjunction / MC | coupled-upper conjunction kept exactly; 4M-draw MC; applied to `\|μ̂\|` | **preserved verbatim** (§3.3) |
| **Q4** — sequential loop / pivot | `INCONCLUSIVE_AT_CEILING` blocks; four honest outcomes; STANDING RULE | **preserved + extended:** the ceiling guard now covers the omega secondary on gating cells (§4, §5(0′)); STANDING RULE enumerates five axes |
| **Q5-P1** | high-M seed-averaged σ_cell; STABLE ≥12/16; coupled OC modeling | **preserved + completed:** P1-A(ω) registers the omega sign the v3.3 text referenced but never produced; the suspenders prose is scoped to its actual regime of validity (§1.1) |
| **Q5-P2** | operationalized gate; demotion consequences pinned | **preserved + completed:** the FULL roster is registered alongside the gating roster and asserted on every consumed dict (§1.2, §7) |
| **Q6** — open leans | τy-matched equal arm; B_max=128; Tc>1 refusal; 16 blocks; P1 pin | **preserved** |
| **Q7** — re-issue scope / claim limits | claim limits; prereg scope; boundary selftests; law-#4 greps | **preserved + expanded:** missing-key/occupancy/shared-ladder selftests; greps extended to the look-stamp rule, occupancy strings, κ₄₀, ρ-grid arms, and computed-expectation traceability (§9.4, §10) |

---

## 13. Measured / derived operating characteristics (v3.2/v3.3 session numbers retained as history; v3.4 numbers COMPUTED that session; **[v3.5] rerun-power numbers recomputed this session under the honest model** — the registration-grade OC sim, §9, remains the instrument of record)

*The v3.4 additions were computed this session with a throwaway full-loop MC of the v3.4 shared-ladder rule (`/usr/bin/python3`, numpy 2.0.2, `numpy.random.default_rng` seeds **20260708 / 20260709**, 4×10⁴ cells/arm; script quarantined to the HQ scratch area, not a registered artifact). They are HQ arithmetic checks, not the registration OC sim — §9 specifies the instrument of record. The v3.1/v3.2 anchor tables and the v3.3 vanish-test power table are retained below unchanged. **v3.3's omega-veto ballpark arithmetic (0.049/cell; 0.26 six-cell; joint ≈ 0.11) is SUPERSEDED** — it priced omega stamped once at the primary's terminal count (the D1 blocker) and reconciled only on the one-sided branch (D2). **[v3.5]** The n_rerun=40→56 power/reband arithmetic below was independently re-verified this session with `/usr/bin/python3` (`scipy.stats.t`, `scipy.stats.nct`) against the exact frozen values in `ARBITRATION_rerun_power.md`; **v3.4's n_rerun=40 "0.912 ≥ 0.90" is an ERRATUM (law #9 — corrected, not erased): the honest α=0.05 power there is 0.858**, which is why n_rerun is raised to 56 (honest power 0.913).*

**Anchor reproduction (v3.1/v3.2 rules) — retained verbatim from v3.3:** per-cell terminal RED 0.839→0.727, INCONCLUSIVE 0.126→0.225, ANOMALOUS 0.0345→0.048, joint P(pivot|null) 0.349→0.148, wrong-sign-at-floor invalid pivot 0.161→0.0066 (v3.1→v3.2 columns; see the v3.3 file §13 for the full tables). The v3.4 draft-check MC reproduces the v3.2 primary-only-ladder anchors before switching the ladder on.

**[v3.4] Null operating characteristics under the SHARED ladder (per cell; ρ_qω = ρ_qc = 0):**

| Quantity | one-sided omega (σ^ω declared) | two-sided omega (INDETERMINATE) |
|---|---|---|
| primary terminal RED | 0.647 | 0.584 |
| primary terminal INCONCLUSIVE | 0.306 | 0.368 |
| primary terminal ANOMALOUS | 0.047 | 0.048 |
| omega terminal RED | 0.641 | 0.388 |
| omega terminal INCONCLUSIVE (blocks on gating) | 0.299 | 0.571 |
| omega terminal GREEN/ANOMALOUS (veto) | 0.030 | 0.0001 (GREEN only — no ANOMALOUS branch) |
| occupancy terminal GREEN (veto) | ≈ 10⁻⁴ | ≈ 10⁻⁴ |
| **per-cell pivot-compatible** (primary RED ∧ omega RED ∧ occ ¬GREEN) | **0.506–0.509** (two seeds) | **0.335** |
| **joint P(pivot \| null) ≈ p⁶** | **≈ 0.017** | **≈ 0.0014** |
| rung distribution (16b / 32b-B96 / 32b-B128 / ceiling) | 0.084 / 0.492 / ~0 / 0.424 | — |
| expected blocks/cell | ≈ 31 (vs ≈ 28 primary-only ladder) | — |

**[v3.4] Hard-gate expected values (every one computed — D7):**

| Gate | Construction | Computed expected |
|---|---|---|
| 1 | S1 any false GREEN | per-cell 0.0003 → six-cell **0.0019** |
| 2 | Δ=+1×floor carrier (primary bands: GREEN 0.118, INCONCLUSIVE 0.862, RED 0.020) | carrier pivot-compatible 0.017 × p_null⁵ (0.509⁵ = 0.034) = **0.00058** |
| 4 | Δ=+3×floor carrier GREEN | **0.9999** |
| 5 (belt-only, ρ ∈ {−1, 0}) | Δ=−1×floor carrier (primary: ANOMALOUS 0.874, INCONCLUSIVE 0.107, falsely-RED 0.0195); carrier pivot-compatible 0.0166 | 0.0166 × 0.034 = **0.00057**; **reband channel [v3.5, recomputed at n_rerun=56 under the honest model]** ≈ 0.874 × 0.087 × 0.047 × 0.034 ≈ **1.2×10⁻⁴** (reband-look RED needs \|μ̂₅₆\| < κ₅₆ = 0.557 − 0.306 = 0.251·sd; honest-model P ≈ 0.047 at a real −1×floor) → total ≈ **0.0007 ≤ 0.02**. *(v3.4's ≈ 4×10⁻⁵/0.0006 figures used n_rerun=40 and a reband-RED sub-probability [0.016] computed under the same reference-conditional model as the power erratum — superseded; the correction is immaterial to the ≤0.02 tolerance either way.)* |
| 5′ | Δ=−2×floor carrier | carrier pivot-compatible **0 observed** at 4×10⁴ (MC-zero) |
| 8 | S8: Δ_ω=+2×floor(96)=1.114·sd on A,B; carrier omega bands GREEN 0.896 / INCONCLUSIVE 0.086 / RED **0 observed at 4×10⁴** (analytic escape P(omega RED) ≈ Φ((0.067−1.114)/0.25) ≈ 1.4×10⁻⁵/cell at 16b) | ≈ 0.509⁴ × (1.4×10⁻⁵)² ≈ **1.3×10⁻¹¹** one-sided; two-sided branch (carrier GREEN 0.814 / INCONCLUSIVE 0.164 / RED analytic ≈ 8×10⁻⁹ at 32b) ≈ **10⁻¹⁸**. *(Under v3.3's throttled stamp the same construction measures ≈ 0.0075 > 0.005 — the BLOCKER, reproduced before repair. Gate 8's arithmetic is independent of n_rerun — the shared ladder, not the powered rerun, carries this guarantee — so it is unaffected by the v3.5 fix.)* |
| 9 / 9Ω | **[v3.5]** n_rerun=**56** powered rerun at ∓1×floor, honest noncentral-t | **0.913** per-contrast (table below); **compound six-cell power ≥0.90 by MC required (law #3), TBD by the registration-grade OC sim** — not yet computed |
| 11 | S10: Δ_occ=+2×floor all six cells; per-cell occupancy GREEN **0.741** (+3×: **0.9945**); per-cell pivot-compatible (primary RED ∧ omega RED ∧ occ ¬GREEN) **0.156** (+3×: 0.0029) | joint = 0.156⁶ ≈ **1.4×10⁻⁵** at +2× (hard-gated); 0.0029⁶ ≈ **7×10⁻¹⁶** at +3× (reported sub-case, not separately hard-gated — [v3.5] notation fix, Antigravity R3 Finding 2) |

**[v3.4] Wrong-sign omega current (S8 sub-case, Δ_ω = −1×floor, one-sided):** omega terminal ANOMALOUS 0.847, INCONCLUSIVE 0.119, falsely-RED 0.018 → per-cell veto-or-block **0.982**; if cell C sole carrier, P(pivot) ≈ 0.509⁵ × 0.0157 ≈ **5×10⁻⁴** (advisory). The §8-Ω powered rerun retains a real wrong-sign omega at **0.913** given the flag surfaced (**[v3.5] n_rerun=56, honest power — supersedes v3.4's 0.912@n_rerun=40**) — the un-block path can no longer launder it at ~0.61 power (D4).

**§8/§8-Ω vanish-test power vs rerun size — [v3.5] RECOMPUTED under the HONEST (reference-uncertain, marginal) noncentral-t model** (`/usr/bin/python3`, `scipy.stats.t`/`scipy.stats.nct`; statistic-agnostic):

| n_rerun | t₀.₉₅(n−1) | SE factor | honest power at ∓1×floor [v3.5] | *(v3.4's reference-conditional figure, superseded)* |
|---|---|---|---|---|
| 16 | 1.753 | 0.2795 | 0.601 | *(0.613)* |
| 24 | 1.714 | 0.2394 | 0.730 | *(0.762)* |
| 32 | 1.696 | 0.2165 | 0.808 | *(0.854)* |
| 40 | 1.685 | 0.2016 | **0.858 — ERRATUM: v3.4 stated 0.912; fails law #3, does not clear ≥0.90** | *(0.912/0.911 — Antigravity's figure, power conditional on an error-free reference, i.e. α≈0.019, not the rule's α=0.05)* |
| 48 | 1.678 | 0.1909 | 0.890 (misses) | *(0.947)* |
| 50 | 1.677 | 0.1887 | 0.897 (misses) | *(reported by Antigravity as the naive-formula near-miss)* |
| **56 (ADOPTED [v3.5])** | **1.673** | **0.1830** | **0.913 ≥ 0.90** — mislabel 0.087 | *(0.967 under the old, now-rejected conditional model)* |

**All rows above use the HONEST model** (numerator variance folds in the 64-block reference uncertainty, matching the SE used everywhere else in this rule and the test's actual α=0.05 calibration — see `ARBITRATION_rerun_power.md`). The right-hand column is retained for the audit trail only; it is NOT the rule's power and must not be cited as such (law #9 — corrections supersede, never erase).

**TRUE-OPPOSITE-PHYSICS retention at −1×floor [v3.5 re-measured, n_rerun=56]:** ≈ 0.874 (anomaly surfaces through the shared ladder) × 0.913 (honest powered-rerun persistence) ≈ **0.80 end-to-end**. *(v3.4's 0.912@n_rerun=40 superseded.)*

**Anomaly-screen honesty (retained):** standalone 16b screen power 0.61 at −floor — too weak to be the guarantee; the magnitude bound (+ STABLE where transduction is not inverted — §1.1 scope) carries it, and the powered reruns stop the survivors from being mislabeled on the way out.

---

## 14. v3.1 re-pass reconciliation (HQ diverse-lens BLOCK → v3.2 disposition — retained, all in force)

Retained verbatim from v3.3 §14 (RED magnitude bound; coupled-STABLE modeling; gates 5/5′ restatement; claim scoping; honest joint headline; t₁₅ / SE_FACTOR / two-sided-reachability minors). The consistency note stands: stochastic OC rates use independent per-cell block noise; "≈4 design points" is claim-scope only; **[v3.4] the ρ_qω / ρ_qc sweeps and the ρ ∈ {−1, 0} STABLE-coupling arms are the mandatory analogues.**

---

## 15. Antigravity re-audit target (updated for v3.4)

The lineage: ChatGPT caught the ceiling axis; the HQ re-pass caught the direction axis; the whole-object audit caught the statistic + cell-roster axes and the unpowered vanish test; **the whole-object re-pass caught the look axis (the throttled omega stamp), the recorded-statistic costume (occupancy), the unpowered omega disposition, the dict-denominator recurrence, the all-positive coupling sweep, and the asserted-not-computed gate expectation (this revision)**. Each pass found the error the previous passes normalized.

**Re-audit target for the next Antigravity pass (v3.4):**
1. **The shared ladder + gate 8** (§4, §5(iii), §9.1) — verify the sim and `analyze()` stamp omega through ONE code path; reproduce the v3.3 breach (≈ 0.0075 under the throttled stamp) and the v3.4 repair (≈ 10⁻¹¹); verify the escape path is omega-RED (≈ 1.4×10⁻⁵/cell at +2×floor one-sided) and that gate 8 holds on BOTH sidedness branches.
2. **P1-A(ω) + sidedness reconciliation** (§1.1, §3, §13) — verify every §13 omega number is labeled with its branch; verify the two-sided branch's ANOMALOUS unreachability is documented and the veto's failability there rests on GREEN + the blocking INCONCLUSIVE; check no prose number silently assumes one-sidedness.
3. **The occupancy guard** (§0.2 D1″, §5(iii′), §9.2 S10, gate 11) — construct the v4.3-shaped scenario (occupancy alone at +2×/+3×floor, quad and omega quiet) and confirm the veto blocks; verify the asymmetry rationale and forks 12/13 are genuinely forked; grep for any residual "recorded and unbounded" occupancy string.
4. **§8-Ω** (§8, §13) — verify no disposition path anywhere can reband a flagged statistic off a look smaller than n_rerun=40; recompute the omega-reband channel and κ₄₀ = 0.217.
5. **Full-roster completeness** (§7, §9.4) — plant missing keys in every consumed dict and verify False; verify S9(d).
6. **The ρ grid** (§1.1, §9.1, S5) — verify the ρ = −1 arm forces STABLE 16/16 with an opposing true current and that gate 5's belt-only number (≈ 0.0006 + 4×10⁻⁵) is measured there, not inherited from ρ > 0.
7. **Computed-expectation traceability (D7)** — for every §9.3 hard gate, trace the expected value to §13's computation; report any asserted number.
8. **v3.2/v3.3 items still standing** (magnitude bound, coupled-upper conjunction, powered primary vanish test, roster-parametric claim, demotion dispositions, honest joint headline 0.808→0.349→0.148→≈0.017).
9. **The extended STANDING RULE itself** — grep every terminal claim against all five axes and report any residual projection, shrunk denominator, throttled look, unexamined recorded statistic, or uncomputed expectation this revision missed.

---

## 16. v3.2 → v3.3 reconciliation (whole-object scope audit → dispositions) — retained historical

Retained verbatim by reference from the v3.3 file §16 (three deduplicated defects: statistic-axis blocker → statistic-scoped claim + omega veto; cell-roster leak → roster-parametric claim + pinned demotions + roster assertion; unpowered vanish test → n_rerun=40 + gate 9 + reband-channel accounting). All three repairs remain in force; where v3.4 supersedes a NUMBER produced under the v3.3 stamp rule (the 0.049/0.26/0.11 omega arithmetic; gate 8's asserted "≲ 10⁻³"; gate 2/5's ≈ 0.007), the superseding value and its computation are in §13 (corrections supersede, never erase — law #9).

---

## 17. v3.3 → v3.4 reconciliation (whole-object re-pass findings → dispositions) — [v3.4]

Three independent audit lenses returned nine findings; deduplicated they resolve to **seven defects** (D1–D7 of the change summary). Every finding row is dispositioned:

| # | Audit finding (lens) | Severity | v3.4 disposition | § |
|---|---|---|---|---|
| 1 | **Omega veto throttled by the primary's ladder:** omega banded once at the primary's terminal block count; a real +2×floor omega current misses the veto ~21–24%/cell (terminal AMBER at a 16b look where GREEN needs 1.88×floor); measured P(pivot \| S8) ≈ 0.0075 > 0.005 — **the spec as written cannot pass its own gate 8**, whose stated expectation was wrong by ~7×. Secondary hazard: a sim that "fixes" this with its own omega ladder certifies a veto the run does not implement. *(Lens 3; BLOCKER.)* | **BLOCKER** | **D1:** shared §4 ladder (extends while primary OR omega AMBER; single terminal-rung stamp for all statistics); omega `INCONCLUSIVE_AT_CEILING` on a gating cell BLOCKS (§5(iii)); sim/run one-code-path pin + S8 stamped-look assertion (§9.1, couple 7). Gate 8 recomputed: ≈ 10⁻¹¹ (escape only via omega-RED ≈ 1.4×10⁻⁵/cell), sidedness-robust. v3.3 breach reproduced before repair (§13). | §4, §5, §7, §9, §13 |
| 2 | **Omega sidedness undefined / internally inconsistent:** §3 said "P1-registered omega sign where declared" but §1.1 registered no omega sign — literal reading = two-sided everywhere, ANOMALOUS veto arm dead code, §13's 0.049/0.26/0.11 reconciling only one-sided (law-#4 non-reconciliation); a wrong-direction omega current at a 16b-terminal cell escapes ~54% via the only live (two-sided GREEN) channel. *(Lenses 2+3; two majors.)* | **major** | **D2:** P1-A(ω) registers σ^ω_cell from the same M=4000 mean field (ROI net vorticity, same negligibility floor → INDETERMINATE → two-sided); §6.2 gains the omega column; §13 states BOTH branches (pivot-compatible 0.509 vs 0.335; joint 0.017 vs 0.0014); v3.3's one-sided-only arithmetic superseded; the D1 blocking-INCONCLUSIVE design makes gate 8 robust on both branches, and the wrong-sign omega case is guarded by ANOMALOUS (one-sided) or blocking-INCONCLUSIVE + §8-Ω (two-sided) — measured veto-or-block 0.982 at −1×floor. | §1.1, §3, §6.2, §13 |
| 3 | **`occupancy_x` is the next statistic-axis costume:** recorded but never banded, no veto — while the document itself cites v4.3's occupancy-loaded real effect as the omega veto's precedent and the veto's rationale sentence applies verbatim; no asymmetry rationale, no fork. Real transduction shaped exactly like v4.3 (occupancy +3×floor everywhere, quad/omega quiet) → pivot mints, invisible to every gate incl. S8. *(Lens 2; major.)* | **major** | **D3:** occupancy banded two-sided (D1″ — no sign registration; direction-complete; law-#8 rationale) at the terminal rung; **occupancy GREEN in any cell BLOCKS** (§5(iii′)), dispositioned via powered §8-Ω; claim text re-worded ("banded two-sided and nowhere GREEN" + terminal-AMBER caveat); asymmetry vs omega documented (D1″) and forked (forks 12/13); failability scenario S10 + hard gate 11 ≤ 0.005 (computed ≈ 1.4×10⁻⁵ at +2×floor; 0.9945 per-cell veto at +3×). | §0.2, §2.1, §3, §5, §7, §9, §11, §13 |
| 4 | **Omega-ANOMALOUS disposition unpowered:** §5(iii)'s "§8-style investigation" left n unpinned for omega; a ~0.61-power look could formally disposition a real −1×floor omega current as artifact, reband it AMBER, and un-block the pivot — the §8 evidence-destruction defect re-entering on the omega branch, through a channel absent from gates 5/8 and §13. *(Lens 1; major.)* | **major** | **D4:** §8-Ω — the SAME powered machine (n_rerun=40, t₃₉=1.685, SE 0.2016, edge 0.340; power 0.912) applied to the flagged statistic; un-block only via powered look + formal amendment; gate 9Ω asserts the power in-sim; S8's wrong-sign sub-case (Δ_ω=−1×floor) simulates the loop; omega-reband channel counted in S8's number of record; secondaries re-stamped from powered blocks after a primary reband. | §5(iii), §8, §9, §13 |
| 5 | **`pivot_licensed()` completeness asserted for the gating dict only:** `omega_bands`/`descriptive_bands` had no completeness assertion — a demoted AxT4 absent from omega_bands (roster-iteration plumbing omission) passes `any()` unexamined; emitted claim text ("in any cell") false; §9.4 selftests never planted a MISSING key. *(Lenses 2+3; two majors — the v3.2 silent-shrink leak one dict over.)* | **major** | **D5:** `REGISTERED_FULL_ROSTER` frozen pre-P2 and passed to `pivot_licensed()`; completeness asserted on **every** consumed dict (`omega_bands` == FULL, `occupancy_bands` == FULL, `descriptive_bands` == FULL − GATING); §9.4 missing-key plants (each dict, missing AND extra); S9 assertion (d); gate 10 extended. STANDING RULE extended ("for EVERY dict the license consumes"). | §1.2, §7, §9.2, §9.4 |
| 6 | **Transduction inversion defeats the suspenders and the all-positive ρ sweep cannot see it:** ρ ∈ {0.5, 1, 2} certifies belt+suspenders where the suspenders cannot fail; §1.1's prose is false under inverted curl→current transduction (P1-B shares the curl, not the response — STABLE 16/16 with a true −1×floor current); no tolerance breach (belt-only ≈ 0.0006 ≤ 0.02) but S5's number of record certified a two-layer guarantee with one provably inert layer in a physically probed regime. *(Lens 3; major.)* | **major** | **D6:** ρ sweep extended to **{−1, 0, 0.5, 1, 2}** with ρ = −1 and ρ = 0 mandatory arms (§9.1); §1.1 prose scoped ("when the transduction is not inverted; under inversion the suspenders are inert and the belt is sole — measured belt-only"); S5 inversion sub-case (STABLE 16/16 by construction, Δ = −1×floor); gate 5 reported per ρ arm; §5(ii) carries the scope note; STANDING RULE extended ("all coupling regimes"). | §1.1, §5, §9.1, §9.2 |
| 7 | **Gate 8's expected value asserted, not computed** ("residual ≲ 10⁻³" vs measured 0.004–0.019 across variants — straddling/exceeding the tolerance ~4–19×), with the omega sign-registration gap directly moving the gate; ratification package carried wrong expected arithmetic for the load-bearing new guard, inviting post-hoc tolerance pressure. *(Lenses 2+3, folded into findings 1/3's arithmetic.)* | **major** | **D7:** every §9.3 hard-gate expected value computed this session and traced in §13 (gates 1, 2, 4, 5, 5′, 8, 9/9Ω, 11); the STANDING RULE and the §10 grep row now require computed-expectation traceability; the joint headline is restated from the computed numbers (≈ 0.017), and fork 2 puts the operating-point cost to Anthony explicitly. | §9.3, §10, §11, §13 |

**Whole-object clean-scope check (the re-pass's own axis, applied to v3.4):** the pivot claim names its statistic (`quad_loop_rate`), its exact cell denominator (registered roster, asserted on every consumed dict), its direction coverage (`|μ̂|` bound), its guarded secondaries at their implemented looks (omega: shared ladder, resolved-or-blocked; occupancy: banded, GREEN-vetoed, caveated), its explicit non-claims (omega/occupancy magnitudes, demoted points, interior continuum, contrasts), and every guard's guarantee is measured in the regimes where it can fail (ρ ≤ 0 arms; both sidedness branches; the ladder as implemented). No terminal claim in this document asserts more than its gating arithmetic bounds, and no hard-gate expectation is asserted without a computation behind it.

---

*End v3.5 draft. Status: DRAFT for Anthony final-say ratification (both external re-reviews of v3.4 — ChatGPT methodology, Antigravity R3 audit — returned APPROVE-WITH-REVISIONS; this revision disposes of every REVISE item). Not registered, not chronicled, no harness bytes edited, not committed. v3 (`138d109`), v3.1, v3.2, v3.3, v3.4, `prereg_v44.json`, and `v44_scout.py` (`source_sha 0b65a9ee92b9fe2c`) remain unmodified. **[v3.5] Raising n_rerun 40→56 changes `CFG["scout"]` and requires a `prereg_v44.json` re-issue with a new sha256 at registration (§10) — flagged, not performed here.** The registration-grade OC simulation (§9) is the next build phase and is where the compound six-cell power ≥0.90 (law #3, gates 9/9Ω) must be verified by Monte-Carlo before registration; its pinned seed (proposal 20260710) is distinct from the v3.4 session's draft-check seeds (20260708/20260709) and from this session's independent re-verification of the n_rerun=56 arithmetic (`/usr/bin/python3`, scipy.stats).*




