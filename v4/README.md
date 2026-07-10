# v4 — Entropy Engine, preregistered runs (v4.0 → v4.3) + paper

This directory is the **public, hash-anchored provenance record** for the v4 line of the
entropy-engine experiment (2D two-chamber Langevin; first-passage-time + probability-current
forks). It exists so the receipts cited in the Sovereign Stack chronicle are independently
checkable by anyone, not just asserted.

The discipline the whole method stands on: **registration precedes execution**, and the exact
harness + config that produced a run are identity-anchored so a result can never be quietly
detached from what generated it.

## v4.2 identity anchors (the load-bearing receipts)

| Anchor | Value | How to reproduce |
|---|---|---|
| `config_hash` | `35e4ad5430ac4ff7` | `sha256(json.dumps(prereg_v42.json["config"], sort_keys=True, separators=(",",":")))[:16]` |
| `source_sha` | `cf96923bba3e941c` | `sha256(v42_harness.py bytes)[:16]` — the harness self-hashes at line 67 |
| `v42_run.ndjson` | `3139ceb11c5c657233786c42446115fc686579337d40ffef712f86d91b344666` | `shasum -a 256 v42_run.ndjson` |
| `v42_crossver_pin.ndjson` | `1d93c3f675aa07544ec96c1dd5ce66486baa73f9aba3cb5602a22d8e730b9fcc` | `shasum -a 256 v42_crossver_pin.ndjson` |

Full file digests are in `MANIFEST.sha256` (frozen with the campaign) and, for artifacts
archived after it froze (`clean_run.ndjson`, `v42_analysis.json`), in
`MANIFEST_SUPPLEMENT.sha256`. Verify all at once:

```bash
cd v4 && shasum -a 256 -c MANIFEST.sha256 MANIFEST_SUPPLEMENT.sha256
```

## Files

- **`v42_harness.py`** — the corrected v4.2 harness (`source_sha cf96923bba3e941c`, not the
  pre-fix `bd1cf096745d82cc`). Self-hashes its own source at line 67.
- **`prereg_v42.json`** — the v4.2 preregistration (152 units; frozen gates; block-level Holm
  across tau as the only confirmatory inference). Chronicled before any unit ran.
- **`v42_run.ndjson`** — the canonical run, `--batch 0:152`, one JSON line per unit. Every line
  stamps `numpy`, `config_hash`, `source_sha`. Canonical numpy: **2.0.2**.
- **`v42_crossver_pin.ndjson`** — 24 units (8 C0 + 16 `C1m_frozen_M256_tau0.25`) extracted for the
  cross-version determinism check (see below).
- **v4.1 lineage** — `prereg_v41.json`, `v41_harness.py`, `v41_run.ndjson`, `v41_analysis.json`,
  `v41_blocklevel.py`, `v41_blocklevel_analysis.json`, `v4_analysis.json`. v4.2's protocol
  correction (regenerative reset; `occ_gate_min_p 0.05` repair of the v4.1 distance-vs-alpha
  malformation) is defined against these.
- **`FORENSIC_AND_RESULTS_2026-07-05.md`**, **`GROK_EXECUTION_CONTRACT.md`** — the v4.1 forensic
  writeup and the multi-seat replication contract (the contract preserves the program's original
  name, "entropy-as-engine", as issued; the script it delivered as `v4_fork_harness.py` is
  committed here as `v41_harness.py`/`v42_harness.py`, whose usage docstrings retain the
  delivery name).
- **v4.0 pilot record** — `clean_run.ndjson` (60 units, every line stamped
  `config_hash 2f8a9e985010c1f6`) and `v4_analysis.json`.
- **`v42_analysis.json`** — the registered confirmatory analyzer's output (see Analysis status).
- **`v43/`** — the complete v4.3 campaign: preregistration, frozen harness, canonical run,
  selftest artifact of record, independent replications (`v43/replication/`), and the
  detailed-balance follow-up (`v43/followup/`).
- **`paper/`** — the deposited v4 manuscript covering the full arc (Zenodo DOI pending).

## Run contract

Any seat must verify `config_hash == 35e4ad5430ac4ff7` **and** `source_sha == cf96923bba3e941c`
before executing (`python3 v42_harness.py --plan`). Replication seats (ChatGPT, Antigravity,
Grok) run the same corrected harness under the same identity check; runs are diffed bit-for-bit.

### NumPy cross-version note

The harness seeds with `numpy.random.default_rng` (PCG64 `Generator`) and draws noise from
`standard_normal`. NumPy freezes the *legacy* `RandomState`/MT19937 stream across releases but
does **not** guarantee `Generator`'s derived distributions are bit-identical across versions.
So cross-version bit-exactness here is an **empirical** claim, not a policy one. The canonical
run is **numpy 2.0.2**; replication seats pin 2.0.2 until a version gap is cleared by diffing
`v42_crossver_pin.ndjson` against a same-unit run on another version. (Deferred to v4.3: move
noise to legacy `RandomState` for a NumPy-guaranteed stable stream, or make the numpy version a
first-class registration anchor beside `config_hash` and `source_sha`.)

## Analysis status

Complete. The confirmatory block-level Holm analysis against the frozen gates was run on
`v42_run.ndjson` and is archived here as `v42_analysis.json` (regenerated deterministically by
the registered analyzer: `python3 v42_harness.py --analyze v42_run.ndjson`). Forks were judged
strictly on the registered gates — no post-hoc moves. The arc continued and closed under
`v43/` (v4.3: powered vortex control proven, anisotropic-horizon engine bounded null at floor
3.67e-5, occupancy micro-shift resolved to the equilibrium side), with the manuscript deposited
at `paper/`.
