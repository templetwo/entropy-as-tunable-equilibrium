# v4.3 Replication Verdict — Grok Build (Part A)

HQ full-field diff against canonical v43_run.ndjson (sha256 21eeed5a…),
2026-07-06, runtime_s and env stamps excluded (machine-dependent by design):

- numpy 2.0.2: **48/48 units bit-exact**
- numpy 2.5.1: **48/48 units bit-exact** (zero float drift — stronger than
  the v4.2 cross-version result, which had one 1e-19 reduction drift)

Contract conduct: exactly the 48 contracted units, correct registered stamps
(config_hash 4e4b68d562b76f8a, source_sha 1b950383ae012431) on every line,
harness copy verified against the registered sha256 before running, nothing
claimed beyond what ran. Production replication: Grok Build (xAI).
