# v4.4 — Movement 2 transduction scout (DRAFT for review)

**Status: pre-registration DRAFT, on the `v4.4-scout-draft` branch, NOT yet registered or run.** This directory exists so the v4.4 Movement 2 pilot scout can be independently reviewed *before* it runs — methodology (ChatGPT) and pre-registration audit (Antigravity) — per the program's standing law: registration precedes execution, and no seat grades its own work. It is deliberately on a draft branch, not `main`, until those reviews clear.

`v4/v43/` stays **hash-frozen** — this is a copy-and-extend of the registered v4.3 harness, never an edit of it.

## What the scout is for

v4.3 bounded the anisotropic-horizon current to a null at one point in design space (Δτ = (0.25,1.0), T_c = 1, floor 3.67e-5) and named the honest gap: no transduction model from mean-field curl (which provably exists) to realized circulation (~10× under the floor). The v4.4 scout **sizes the SIGNAL** — an empirical current-vs-(Δτ, T_c) response surface across 6 cells — rather than the noise (which is what v4.3's pilot sized). Full rationale + decision rule + reviewer flags: **`SCOUT_DECLARATION.md`** (read this first).

## Identity anchors (verify before any run)

| Anchor | Value |
|---|---|
| `version` | `v4h-1.4.0` |
| `config_hash` | `a344d6c47c8a22c1` |
| `source_sha` (v44_scout.py) | `0b65a9ee92b9fe2c` |
| `prereg_v44.json` sha256 | `b7c5aeb6bd21b70036f7fb6841f199fbf923aa984cba3d30a71943c75e9a2a2b` |

Canonical interpreter: **`/usr/bin/python3`** (Python 3.9.6, numpy **2.0.2** — the pinned version). Verify:

```bash
cd v4/v44
shasum -a 256 -c MANIFEST.sha256          # 5/5 OK
/usr/bin/python3 v44_scout.py --selftest  # all gates + prose/config grep-check -> SELFTEST PASS
/usr/bin/python3 v44_scout.py --plan | shasum -a 256   # byte-identical to prereg_v44.json
/usr/bin/python3 v44_scout.py --pilot-pair             # runs the 6-cell v44pilot:: sweep (10x scale)
```

## Files

- **`v44_scout.py`** — the scout harness. Copy of the registered v4.3 harness (`source_sha 1b950383ae012431`) + a surgical `--pilot-pair` 6-cell sweep, per-cell T_c threading, three new selftest rules (compound power carried, prose/config grep-check, unified centering), dead-code strip. Self-hashes at line ~98.
- **`prereg_v44.json`** — reproducible `--plan` machine output (identity anchors + full config incl. the 6 scout cells + confirmatory outcome_map). Scout cells are in `config` but NOT in `units` — the pilot is never pooled into the confirmatory unit list.
- **`SCOUT_DECLARATION.md`** — the pilot declaration: what `--pilot-pair` runs, the decision rule (any cell ≥3× its own B=64 floor → registration candidate; else publishable null → pivot to closed no-reset NESS), the reviewer flags (T_c is a linear force prefactor; cell-D is consistency-not-bit-identity with a captured v4.3 reference), and the HQ pre-route verification record.
- **`v44_scout_DESIGN.md`** — the design rationale (the sweep table, the transduction question).
- **`v44_scout_BUILD_SPEC.md`** — the diff-level build spec (surgical edits + the blocking invariants).
- **`MANIFEST.sha256`** — hash anchor over the five artifacts.
- **`receipts/`** — the HQ verification receipt trail (file tree + hashes, `sha256sum -c`, selftest log, prereg reproducibility, prereg↔harness semantic triangulation) and **`AUDIT.md`**, an independent adversarial audit (three agents each trying to falsify completeness / semantic self-agreement / T_c threading; all three HOLD, 0 blockers).

## Review pipeline (where this is in the flow)

build (HQ) → **methodology review (ChatGPT)** → **pre-registration audit (Antigravity)** → HQ chronicles the pilot declaration + registers → Grok Build runs it under contract (raw NDJSON only, HQ diffs). This draft is at the first review gate.
