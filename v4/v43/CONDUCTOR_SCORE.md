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

## Status addendum — 2026-07-10 (HQ overwatch seat, post-deposit)

Recorded per the standing law (corrections supersede, never erase); the score above is preserved
as issued 2026-07-06.

- **Movement 4 (Grok Build replication): COMPLETE** — 48/48 bit-exact on numpy 2.0.2 and 2.5.1;
  receipts in `replication/grok-build/` (`VERDICT.md`, pinned by `MANIFEST_SUPPLEMENT.sha256`).
- **Movement 5 (Antigravity audit): COMPLETE** — 5/5 findings real, 0/5 affect registered
  verdicts (repo commit 8453b8e).
- **Arbiter recompute receipt: LANDED** (2026-07-09) — independent replication at
  `replication/claude-recompute/`, 72/72 bit-exact, closing the two-seat loop on v4.3.
- **Movement 6 (paper): DEPOSITED** — `v4/paper/` (commits f289e4f → 97d7725); Zenodo DOI
  pending. The claude-recompute VERDICT's pre-DOI action item (detailed-balance artifact "not
  yet committed") was satisfied by deposit commit f289e4f (`followup/`).
- **Erratum, recorded alongside a frozen file:** `followup/README.md` says the occupancy
  micro-shift is discussed in paper §3.5; the correct section is §3.8 (true both at deposit
  commit f289e4f and at HEAD). The frozen file is preserved as-is per law #9.
- **Movements 1–3 (v4.4 scout → registration) remain the open work**, held on the §4 ladder
  adjudication and decision-rule v3.1 (entropy-v4.4 lineage thread).
