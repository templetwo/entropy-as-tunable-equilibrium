# Conductor Score — post-v4.3 (written 2026-07-06, HQ Fable seat, before rotation)

The v4.3 loop is closed on HQ's side: instrument proven (G1), engine bounded
null (G3), occupancy micro-shift confirmed (p=0.024). Canonical + analysis
are public at `github.com/templetwo/entropy-as-tunable-equilibrium/v4/v43/`
and chronicled (canonical sha256 `21eeed5a…`, digest entry tagged
`for-opus-arbiter`). What follows is the full remaining score, one movement
per seat. Any HQ Claude Code seat can execute Movements 1–3 verbatim; the
external seats get Movements 4–5 as contracts.

**Standing law for all movements:** prereg before run; gates must be able to
fail AND controls must prove they can pass (compound-power rule, in selftest);
raw NDJSON is the primary record; corrections supersede, never erase; result
labels keep the reset-protocol vs closed-NESS distinction. Non-Claude seats
are ringed subordinate compute — plain provenance credit, never co-author
(standing policy).

---

## Movement 1 (HQ, ~30 min, no new compute): omega_roi power analysis

**Why:** v4.4's floor might drop for free. The v4.3 canonical already carries
a second circulation statistic per unit (`roij.omega_roi`, integrated curl in
the mouth ROI) that was never power-analyzed. If its block sd (relative to
the vortex effect it shows) beats `quad_loop_rate`'s, v4.4 inherits a lower
detection floor at zero extra compute.

**Steps:**
1. Read `v4/v43/v43_run.ndjson`. For every C4v and C5a unit extract BOTH
   `data.quad.quad_loop_rate` and `data.roij.omega_roi`.
2. Per arm (4 C4v kappas, 3 C5a pairs): block mean, block sd, for both stats.
3. For C4v: compute per-stat signal-to-noise (arm-mean minus k0-mean, over
   block sd) at k2/k4/k8. The better statistic is the one with higher SNR.
4. Compute the 90%-power detection floor for omega_roi at B=64
   (`(z_.995+z_.90)*sd*sqrt(2/64)`) and compare to quad's 3.67e-5 —
   floors only comparable via each stat's own vortex calibration curve, so
   report "minimum kappa cleanly resolved" per stat, not raw floors.
5. Chronicle the verdict (`domain: v4.4-design,omega-roi-power`); it feeds
   Movement 3.

## Movement 2 (HQ, ~1-2 h compute, pilot namespace): transduction study

**Why:** the honest gap named in the v4.3 ruling — the program has NO
quantitative map from mean-field curl to realized circulation, so v4.3's
floor was set by compute, not theory. v4.4 must not be registered until a
transduction estimate says which (delta-tau, geometry, Tc) puts the predicted
current 3x above the floor.

**Steps (all in `v44pilot::` seed namespace, declared, never pooled):**
1. Sweep tau pairs: (0.1,2.0), (0.25,2.0), (0.1,1.0), (0.25,1.0)-replica.
   8 blocks each at 10x scale using `v43_harness.py` C5a machinery with a
   `--pilot-pair tx ty` extension (10-line edit; keep source_sha churn out
   of v4/v43/ — work on a copy named `v44_scout.py`).
2. Also sweep Tc in {1, 2, 4} at the widest pair (force amplitude lever —
   note Tc also rescales U_eff, so occupancy shifts; record it).
3. For each cell: block-mean current (both stats), block sd. Fit
   current-vs-(delta-tau, Tc). If any cell's mean clears 3x its own floor
   at B=64, that cell is the v4.4 registration candidate.
4. If NO cell clears: the result is itself publishable ("anisotropic-horizon
   currents are sub-floor across the accessible design space") and v4.4
   pivots to the closed no-reset NESS protocol instead — see Movement 6.
5. Chronicle the sweep table verbatim (clean-channel discipline).

## Movement 3 (HQ, after 1+2): v4.4 registration

Same discipline as v4.3 (v4h-1.4.x): fresh namespace `v44::`, compound-power
selftest for every gate INCLUDING the aniso arm this time (Movement 2 gives
the magnitude prediction v4.3 lacked), directional secondary from the
mean-field sign at the chosen pair, NESS scope boundary registered, chronicle
before run, hold for Anthony's go. If Movement 2 step 4 fired instead:
register the no-reset NESS protocol (closed box, no regenerative reset,
current measured in stationarity after burn-in; this answers the boundary
v4.3 explicitly declined to claim).

## Movement 4 (Grok Build, contract): v4.3 replication

Contract file: `REPLICATION_CONTRACT_V43.md` (this directory + repo).
Deterministic replication of a pinned 48-unit subset. Grok Build's job is
execution + raw output only — the v4.1 integrity study's conduct standard
(return exactly what ran, claim nothing more). HQ diffs against canonical;
divergence beyond float-reduction tolerance (~1e-12) is data, not failure.

## Movement 5 (Antigravity, contract): adversarial analyzer audit

Same contract file, Part B. Antigravity does NOT run units; it audits the
v4.3 analyzer the way ChatGPT audited v4.1: read `v43_harness.py` analyze()
+ `prereg_v43.json` gates, hunt for (a) gates that cannot fail, (b)
statistics compared against wrong nulls, (c) pseudo-replication, (d) any
place the code disagrees with the registered gate text. Written findings
only. HQ verifies each finding against the raw data before accepting.

## Movement 6 (paper seat, whoever holds Track 2): the v4.3 chapter

The fold gains its final section: instrument repair as a first-class result
(the 8%/25% autopsy -> compound-power rule -> 0.655 coin-flip catch ->
1.000), the aniso construction + bounded null at 3.67e-5, the directional
footnote handled honestly (25% by-chance, labeled unresolved), occupancy
micro-shift now confirmed (p=0.024, TV=0.010). Citation fixes already
verified in chronicle: v3 DOI 10.5281/zenodo.21223845; Jenner et al. real
title "Calculus on MDPs: Potential Shaping as a Gradient" (arXiv 2208.09570);
Ramirez-Ruiz et al. real title "Complex behavior from intrinsic motivation
to occupy future action-state path space" (Nat Commun 15:6368, 2024).
Compile with tectonic (installed, proven on the v3 paper).

## Sequence and gating

1 and 4 and 5 can start immediately, in parallel. 2 starts any time (HQ
compute). 3 waits on 1+2. 6 waits on nothing (v4.3 numbers are final unless
Opus's arbiter pass or Movement 5 finds a defect — hold submission, not
drafting, on those). Opus arbiter verification is pending on its own side;
its receipt closes the two-seat loop on v4.3.

---

## ADDENDUM — 2026-07-12, HQ Opus seat (session `spiral_20260712_030506`)

*Appended, not edited (law #9 — this doc is not hash-pinned in
`v4/v43/MANIFEST.sha256`, so an append is clean; the text above is
untouched). Written to correct a documentation-lag near-miss: this score's
Movement 2/3 framing above (written 2026-07-06) reads as current to anyone
who stops here, and a downstream seat tonight nearly re-drafted work that
already exists because of it. This addendum states where Movement 2/3
actually stand as of `v4.4-scout-draft` @ `e630d6f`.*

**What actually happened since the movements above were written (all in
`v4/v44/`, none of it in this file's original text):**

1. Movement 2 (transduction pilot) ran. It produced a decision-rule
   methodology that went through six drafted revisions —
   `v44_scout_DECISION_RULE_v{2_DRAFT,3,3.1,3.2,3.3,3.4,3.5}.md` — under
   external review (ChatGPT methodology pass, Antigravity adversarial
   audit R1–R3) and an overnight autonomous Fable hardening loop
   (`MORNING_BRIEF.md`).
2. **Decision-rule v3.5 was RATIFIED BY ANTHONY on 2026-07-08**
   (`RATIFICATION_v3.5.md`, artifact `v44_scout_DECISION_RULE_v3.5.md` @
   commit `5df6d98`). This is a **rule** ratification, not a **run**
   registration — the receipt says so explicitly and law #1 still holds:
   registration remains a separate, still-pending Anthony gate.
3. The registration-grade OC simulator (Movement 3 precondition) was
   built and run: `oc_sim_v35.py` on the canonical interpreter, seed
   20260708, N=4×10⁶ (`OC_REPORT_v35.md`, `oc_results_v35.json`).
   **Result: gate 9/9Ω compound power = 0.980 ≥ 0.90 → PASS**, for the
   v3.5 rule *as ratified*. Rerun H0 α = 0.04999 (reference-uncertain
   invariant locked); gate-4 GREEN power @ 3×floor = 0.99991. This fills
   v3.5's one TBD number.
4. **A new, live blocker was then found on 2026-07-12** (today, this
   session's own morning), *inside* the ratified v3.5 rule:
   `P1_SIGN_STABILITY_PACKET.md`. Two distinct problems, not one:
   (a) **σ_cell (sign identifiability) is unidentifiable at the
   registered `N_avg=32`** — the friendliest cell is off by ~44×
   (needs ~2,834–71,382 seeds depending on cell; 32 is nowhere close);
   and (b) **`STABLE`/P1-B has a ~0.37 per-block SNR ceiling that is
   independent of `N_avg`** — it is set by how noisy *one block's grid*
   is, not by how well the precondition knows σ, so buying more
   precondition seeds (fixing (a)) does **not** fix (b). `STABLE`
   gates whether a RED counts toward the all-RED pivot; a precondition
   that cannot pass is a law #3 violation the same way a gate that
   cannot fail is a law #2 violation. Four remediation options are laid
   out; the packet's author recommends **Option 4** (drop
   `STABLE`/σ_cell from the pivot license entirely, band all statistics
   two-sided, rest the all-RED pivot on the belt alone — because Option
   2, buying σ_cell alone, fixes (a) but leaves (b) exactly where it
   is) but is explicit that **this is a recommendation, not a
   decision** — the deciding number (compound gate power ≥0.90 for an
   all-two-sided OC re-run) has **not yet been computed**. Until it is,
   Option 3 (a heavier v4.5-scale re-architecture: seed-averaged grids
   per block, which addresses (b) directly) remains live too.

**So: the 0.980 OC-sim PASS above is real but scoped** — it validates
v3.5 as ratified, not v3.5 as it will read after the P1-B fork resolves.
Do not read "OC sim passes" as "ready to register."

**The actual frontier, as of this addendum (not Movement 2/3 above):**
- P1-B / `STABLE`-gate fork unresolved: Option 4 (recommended — drop
  `STABLE` from the pivot license) vs Option 3 (re-architecture:
  seed-averaged grids per block, fixes the per-block SNR ceiling
  directly) vs Option 2 (buy σ_cell by raising `N_avg`; fixes
  identifiability only, leaves P1-B's ~0.37 per-block ceiling untouched)
  vs Option 1 (register as-is, rejected — kills the null the program
  needs to be able to declare). **Next compute:** re-run the OC sim in
  an all-two-sided, no-`STABLE`-precondition configuration and check
  compound power ≥0.90 (law #3). This is the single number that decides
  the fork.
- Exhaustive OC scenario set (omega-only S8, occupancy-only S10, demotion
  S9, coupling ρ∈{−1,0,0.5,1,2} per-arm) is still outstanding —
  `OC_REPORT_v35.md` confirms only the load-bearing gates, not the full
  registration-artifact scenario grid.
- `band_cell`/`pivot_licensed` machinery implied by the Option-4 fork is
  **not yet in `v44_scout.py`** — it is a proposal in the packet, not
  code.
- P1 definition itself is what's open (two competing definitions +
  three curl estimators are carried in the diagnostic; not yet settled
  which is registered).
- `prereg_v44.json` re-issue (n_rerun=56 + ratified v3.5 forks → new
  sha256, new `MANIFEST.sha256`) has **not** happened; the file on disk
  still reflects the pre-ratification config.
- **Registration remains HELD.** Nothing above authorizes or performs a
  run. Per standing law #1, that gate is Anthony's alone.

**Documentation-lag audit (why this addendum exists):** `~/.claude/CLAUDE.md`'s
"Entropy Program" section (global config, read by every seat at boot) still
says (as of before this addendum) "NEXT: Movement 2 transduction scout ...
gates the v4.4 registration" — the state as of 2026-07-06, i.e. before the
pilot ran, before v3.5 was drafted let alone ratified, before the OC sim
existed. A corrected status block has been drafted for HQ/Anthony review
(not applied — that file is Anthony's) alongside this reconciliation task.
`~/Desktop/lab/v44pilot/` is a frozen v3-era snapshot (decision rule only
through plain `v3.md`, no v3.1–v3.5, no ratification, no OC sim, no P1
finding) — anyone reading it in isolation gets the same stale picture;
flagged, not deleted. `v4/v44/README.md` is also stale in the same
direction (still describes the scout as "at the first review gate").

*This addendum is provenance, not registration, not a methodology ruling
on the P1-B fork (that stays Anthony's + the external seats' to decide),
and not an edit to anything above it.*
