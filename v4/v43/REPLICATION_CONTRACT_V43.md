# v4.3 External-Seat Contract (issued 2026-07-06, HQ conductor)

Two independent work orders. Raw output is the only valid channel. Prose
claims of completion carry zero weight; the v4.1 execution-integrity study
found 3 of 4 external seats fabricating, and the seat that returned only
what it actually ran became the trusted auditor. That is the conduct bar.

Source of truth (fetch, do not trust pasted copies):
- https://raw.githubusercontent.com/templetwo/entropy-as-tunable-equilibrium/main/v4/v43/v43_harness.py
- https://raw.githubusercontent.com/templetwo/entropy-as-tunable-equilibrium/main/v4/v43/prereg_v43.json
- https://raw.githubusercontent.com/templetwo/entropy-as-tunable-equilibrium/main/v4/v43/MANIFEST.sha256

## Part A — Grok Build: deterministic replication (48 units)

1. Environment: Python 3.9+ with numpy. Report `numpy.__version__` in a log
   line. numpy 2.0.2 gives byte-exact match to canonical; other versions may
   differ by ~1e-19 float-reduction drift (known, documented in v4.2) — this
   is why full-field diffing is done by HQ, not by you.
2. Verify the harness you fetched: sha256 of the file must be
   `1b950383ae01243147111dfe3c22ef0917d21b481fe447229ec80edfda858dda`.
   If it is not, STOP and report the mismatch — do not run.
3. Run EXACTLY these 48 units, one NDJSON result line each, raw stdout only:
   - All 8 C0 units (`C0_hot_sb0..sb3`, `C0_ctrl_sb0..sb3`)
   - C4v k8 arm, blocks sb0..sb15 (16 units):
     `python v43_harness.py --unit C4v_frozen_k8.0_tau1.0_sb{N}`
   - C5a arm 1, blocks sb0..sb15 (16 units):
     `python v43_harness.py --unit C5a_frozen_tx0.25_ty1.0_sb{N}`
   - C5a equal arm, blocks sb0..sb7 (8 units):
     `python v43_harness.py --unit C5a_frozen_tx1.0_ty1.0_sb{N}`
4. Return: the raw NDJSON (as a file or verbatim block), your numpy version,
   and nothing else. Units you did not complete are reported as not run.
   Expected wall time: roughly 3-5 minutes of compute (units are seconds
   each; C0 units ~6s).

## Part B — Antigravity: adversarial analyzer audit (no execution)

Do not run any units. Read `v43_harness.py` (functions `analyze`,
`block_perm_p`, `holm`, `selftest`) and the gates text in `prereg_v43.json`
(`outcome_map` + `config.thresholds`). Hunt for and report, with line
references:
1. Any gate that cannot fail on null data, or any control that cannot pass
   on true signal (the two failure classes this program has already been
   burned by — a malformed occupancy gate in v4.1, an underpowered control
   in v4.2, a coin-flip monotonicity clause caught pre-registration in v4.3).
2. Any statistic compared against the wrong null (distance vs p-value class
   errors; one-sided/two-sided mismatches between code and registered text).
3. Pseudo-replication: any place pooled observations are treated as
   independent when the seed block is the true unit.
4. Any disagreement between what `analyze()` computes and what the
   registered gate text says it computes (G1 monotonicity is over k0<=k4<=k8
   with k2 descriptive — check the code honors exactly that).
5. The permutation machinery itself: `block_perm_p` uses `random.Random`
   sampling of index subsets — check the one-sided path, tie handling, and
   the +1/(n+1) floor are sound.
Written findings only, most severe first, each with the specific line and a
concrete failure scenario. Findings will be verified by HQ against raw data
before acceptance; "no findings" is an acceptable result if true.

## Return channel

Hand results to Anthony (any format he can relay), or if a seat has GitHub
access, a gist/PR against `templetwo/entropy-as-tunable-equilibrium` under
`v4/v43/replication/<seat-name>/`. HQ performs all diffs and verdicts.
Credit: plain provenance ("production replication: Grok Build (xAI)";
"analyzer audit: Antigravity (Google)") per standing policy.
