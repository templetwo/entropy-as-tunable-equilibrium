# v4.4 Scout Pre-Registration — Independent Adversarial Audit

**Package:** `/Users/tony_studio/Desktop/lab/v44pilot`
**Auditor:** Synthesizer seat (adversarial stance; every check regenerated, receipts not trusted)
**Interpreter:** `/usr/bin/python3` (Python 3.9.6, numpy 2.0.2) for all harness execution; harness loaded as a module via `importlib` so its `__main__` guard does not run.
**Date:** 2026-07-06

---

## Verdict: GAPS_FOUND (2 nits, none blocking) — routable

Three claims audited (completeness, semantic, tc_threading). All three claims HOLD, but **2 CONFIRMED gaps survived verification** — both severity **nit** (cosmetic / packaging hygiene). One reported gap dropped as a **FALSE ALARM**. Because both confirmed gaps are nits with **no blocker or major finding**, the package remains **routable** to external review ("gaps found, none block").

Routing gate: `routable = true` (no CONFIRMED blocker/major finding).

---

## Independently regenerated provenance (load-bearing, all PASS)

| Check | Command | Result |
|---|---|---|
| Manifest integrity | `shasum -a 256 -c MANIFEST.sha256` | 5/5 OK, exit 0 |
| Harness source_sha | `shasum -a 256 v44_scout.py \| cut -c1-16` | `0b65a9ee92b9fe2c` = manifest entry = `prereg.source_sha_at_registration` = runtime `SOURCE_SHA` |
| v4.3 base source_sha | `shasum -a 256 v43_harness.py \| cut -c1-16` | `1b950383ae012431` (matches registered base) |
| Prereg reproducibility | `/usr/bin/python3 v44_scout.py --plan \| diff - prereg_v44.json` | **BYTE-IDENTICAL** (both sha `b7c5aeb6…`) |
| Config identity | importlib `m.config_hash()` vs `prereg.config_hash` | both `a344d6c47c8a22c1`; live `CFG == prereg.config` True |
| Version | `m.VERSION` vs `prereg.version` vs `prereg.config.version` | all `v4h-1.4.0` |
| Selftest | `/usr/bin/python3 v44_scout.py --selftest` | **SELFTEST PASS** — all 11 gates incl. compound-G1 power 1.000, gate-can-fail(occ + aniso G2), and prose/config grep-check (`24/32`, `48/64` present) |
| Diff scope | `diff v43_harness.py v44_scout.py` | 116 changed lines in bounded localized hunks (config additions + `force_frozen`/`force_frozen_aniso` Tc override + scout plumbing) — surgical, not a rewrite |
| Stale drafts | `find … -name '*.bak' -o '*.orig' -o '*~' -o -iname '*copy*'` | none |

---

## Per-claim verdicts

### 1. completeness — HOLDS
Manifest lists exactly the 5 intended content files and verifies clean; harness self-consistent; no stale/superseded drafts. One CONFIRMED nit (.DS_Store), one FALSE ALARM dropped (BUILD_SPEC tense).

### 2. semantic — HOLDS
`prereg.config` deep-equals live `CFG`; VERSION/config_hash/source_sha triangulate; 6 scout cells identical between prereg and code; thresholds (24/32, 48/64) consistent across CFG, `--plan` prose, docstrings, declaration, and machine-enforced by selftest; C6s units built in quarantined `v44pilot::` seed namespace, no leak into the 392 confirmatory units. One CONFIRMED nit (label notation).

### 3. tc_threading — HOLDS (zero findings)
T_c threaded as a per-cell runtime override (`Tc_ov` → `force_frozen`/`force_frozen_aniso`), guarded on `Tc is None` (so `Tc=0.0` is not silently dropped), exactly linear at the force level (2×/4× to bit precision), never mutates global CFG mid-run (config_hash stays constant). Byte-identity preserved on the default (non-override) force paths vs the pristine v4.3 harness. No gap.

---

## CONFIRMED gaps (count against package — both severity nit, non-blocking)

**G1 — Stray `.DS_Store` in package directory** (completeness, nit)
- 6148-byte macOS `.DS_Store`, mtime 2026-07-06 22:55 (≈35 min AFTER the MANIFEST freeze at 22:20; 13 s after the filetree-receipt capture, which is why the receipt omits it).
- **NOT** in `MANIFEST.sha256` and **NOT** in `receipts/00_filetree.txt` (both grep counts = 0), so the "manifest lists exactly the intended files" claim is not violated. Impact is packaging hygiene only: it would ride along in a naive `tar -czf pkg.tgz v44pilot/` unless excluded.
- Reproduce: `ls -la /Users/tony_studio/Desktop/lab/v44pilot | grep DS_Store`
- Fix: `rm /Users/tony_studio/Desktop/lab/v44pilot/.DS_Store` before packaging, or exclude with `--exclude='.DS_Store'`.

**G2 — Scout-cell label notation divergence in DESIGN.md** (semantic, nit)
- `v44_scout_DESIGN.md` writes the two T_c-sweep cells as `A·T2` / `A·T4` using U+00B7 MIDDLE DOT (verified bytes `41 c2 b7 54 32`), while `prereg_v44.json`, `v44_scout.py` (CFG + emitted C6s unit ids), `SCOUT_DECLARATION.md`, and `v44_scout_BUILD_SPEC.md` all write `AxT2` / `AxT4` with ASCII `x`. DESIGN.md is the sole outlier of five artifacts.
- Purely cosmetic: numeric cell defs `(tx=0.1, ty=2.0, Tc=2.0/4.0)` are identical across all sources, and the run emits `AxT2`/`AxT4` in the NDJSON (label comes from CFG, not from DESIGN.md). Cannot affect config_hash, seeds, or a run.
- Reproduce: `grep -n 'A·T2\|AxT2' v44_scout_DESIGN.md SCOUT_DECLARATION.md prereg_v44.json v44_scout.py`
- Fix: normalize DESIGN.md to ASCII `AxT2`/`AxT4` for verbatim cross-artifact string identity.

---

## Dropped FALSE ALARM (does NOT count against package)

**BUILD_SPEC.md line 3 present-tense base description.** Line 3 reads: "`v44_scout.py` currently is a byte-exact copy of the registered v4.3 harness (`v43_harness.py`, source_sha `1b950383ae012431`, 971 lines, VERSION `v4h-1.3.1`). All edits are SURGICAL against that base."
- Independently verified the parenthetical descriptors describe the **BASE** and are all correct: `wc -l v43_harness.py` = 971, base sha prefix = `1b950383ae012431`, base VERSION = `v4h-1.3.1`. The final harness (v4h-1.4.0, 52576 B) legitimately differs.
- This is a diff-level build spec whose job is to name the exact pre-edit base; carrying the base's line count / VERSION / sha is correct build provenance, not stale content. The only stale token is the word "currently," and it is neutralized in the same sentence by "All edits are SURGICAL against that base." Not a completeness defect. Dropped.

---

## Status

**HQ asserts complete + manifest-clean + independent adversarial audit confirms source_sha/config_hash/VERSION triangulate, `--plan` is byte-identical to the registered prereg, selftest passes all 11 gates, and the T_c override is surgical and byte-identity-preserving on the default paths — only 2 cosmetic nits, no blockers; external methodology (ChatGPT) + pre-reg (Antigravity) review remains pending.**

---

## HQ post-audit resolution (2026-07-06)

Both nits resolved before routing (neither was a blocker; `routable` was already true):
- **G1 (.DS_Store):** removed from the package dir. Packaging MUST exclude it (macOS regenerates it) — use `tar --exclude='.DS_Store'`.
- **G2 (label notation):** `v44_scout_DESIGN.md` normalized `A·T2`/`A·T4` (U+00B7) → ASCII `AxT2`/`AxT4`. Verified: no `A·T` cell-label remains in any artifact; all 5 now agree on `AxT2`/`AxT4`. The remaining U+00B7 in the declaration/build-spec is math notation (`Tc·∇S`), not a label.

New `v44_scout_DESIGN.md` sha256[:16] `1ae9c694e23caf5e`; `MANIFEST.sha256` regenerated + verified 5/5 OK; `v44_scout.py` unchanged (`0b65a9ee92b9fe2c`).

**Package verdict:** HOLDS on all three claims, 0 blockers, 0 open nits. Ready to route to ChatGPT (methodology) + Antigravity (pre-reg audit). External review remains pending.
