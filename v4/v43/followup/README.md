# Detailed-balance follow-up — matched-τ occupancy micro-shift (2026-07-08)

Resolution of the program's last surviving positive: the v4.3 matched-τ
frozen-vs-online occupancy micro-shift (C1m, B=32/arm, permutation p = 0.024,
TV ≈ 0.010). Referenced by the v4 paper (`v4/paper/paper.tex`: abstract,
§3.5, conclusion, and the data-availability section).

## Artifacts

- **Script:** `../occupancy_microshift_analysis.py` — this deposit lands it
  on `main`; byte-identical (sha256 `9cef2ea77a325b06…`) to the copy landed
  on `v4.4-scout-draft` in commit `4178307` (2026-07-08, chronicle-logged
  with verified receipts).
- **Input:** `../v43_run.ndjson` — the canonical v4.3 run (sha256
  `21eeed5a65189c73…`, covered by `../MANIFEST.sha256`; manifest verified
  clean immediately before this deposit). Read-only; no frozen bytes touched.
- **Output:** `occupancy_microshift_output.txt` — captured stdout of
  `/usr/bin/python3 occupancy_microshift_analysis.py` run from `v4/v43/`
  (numpy 2.0.2, deterministic permutation test, fixed seed). Regenerated
  2026-07-09 for this deposit; verdict identical to the 2026-07-08 run
  recorded in the commit message of `4178307`.

## Verdict

The shift is **real and spatially distributed** (top-3 bins carry 42% of the
displaced mass — not a single-bin/boundary artifact), but **both arms are
loop-current-free with no frozen-vs-online circulation difference**
(quad_loop_rate, omega_roi, mouth_loop_rate all null). It is a ~1%
difference between two near-equilibrium force fields (interpolated-frozen
vs pointwise-online): estimation/numerical, **not** a broken-detailed-balance
engine signature. The last apparent positive of the program resolves, like
every one before it, to the equilibrium side.

Independent confirmation: `../replication/claude-recompute/` re-simulated
all 72 relevant units from archived seeds (72/72 bit-exact) with an
independent transition-count current pipeline and reached the same
resolution (see its `VERDICT.md`).

Note: the script emits one numpy `RuntimeWarning` (zero standard error in
empty occupancy bins produces NaN z-scores, which the |z|>2 filter then
excludes). Behavior is unchanged from the landed script; recorded here for
transparency.
