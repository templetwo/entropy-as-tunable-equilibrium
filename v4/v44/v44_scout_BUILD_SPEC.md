# v44_scout.py — Build Spec (diff-level, delegated)

*HQ (Mac Studio Claude Code seat, overwatch/provenance) build spec derived from `v44_scout_DESIGN.md` + an advisor pass, 2026-07-06. `v44_scout.py` currently is a **byte-exact copy of the registered v4.3 harness** (`v43_harness.py`, source_sha `1b950383ae012431`, 971 lines, VERSION `v4h-1.3.1`). All edits are SURGICAL against that base. Two agents, disjoint function sets, sequential. HQ reviews each diff and runs `--selftest` / `--plan` / byte-identity itself.*

---

## BLOCKING invariants (put verbatim in every delegation; HQ verifies on the returned diff)

1. **Tc is a per-cell config value, NEVER mutated mid-run.** The scout cells — *including each cell's Tc* — live in `CFG["scout"]`, exactly the way v4.3 puts `aniso_pairs` in CFG. `config_hash()` then covers the full swept design and stays constant across the whole run. Do NOT assign to `CFG["entropy"]["Tc"]` at runtime (that detaches lines from their harness identity). Thread Tc as a **runtime override argument** that defaults to `CFG["entropy"]["Tc"]`.
2. **Byte-identity of the confirmatory path.** With Tc unset (default), the confirmatory units (C1m / C4v / C5a) must produce a **byte-identical `data` physics payload** to the pre-edit file. If any existing unit's physics shifts, the Tc threading leaked into the default path. (HQ diffs a `--batch` run of a few C4v/C5a units before/after; only the `data` object is compared — `config_hash`/`version`/`source_sha` metadata are expected to differ.)
3. **Cell-D replica trap.** "D reproduces the v4.3 (0.25,1.0) point" is a **statistical consistency check, not bit-identity.** The scout runs in the `v44pilot::` seed namespace — a DIFFERENT namespace from v4.3, so it MUST differ per the never-pooled rule (law #6). Do NOT wire in a bit-identity assertion (it will falsely fail) and do NOT reuse v4.3 seeds to force it (violates quarantine). Cell D is verified later by HQ as consistent-within-noise with the v4.3 arm.
4. **Never pool the pilot.** Scout units are NOT added to `build_units()` (which feeds the confirmatory `--batch`). `--pilot-pair` builds and runs them directly, `v44pilot::` seeds.

---

## AGENT 1 — Scout forward-path build (touches ONLY: VERSION, CFG, a new `scout_seed`, `force_frozen`, `force_frozen_aniso`, `run_chamber`, a new `pilot_pair`, `main`). Does NOT touch `analyze` / `selftest` / `block_perm_p` / `perm_p`.

### 1a. VERSION bump
`VERSION = "v4h-1.3.1"` → `VERSION = "v4h-1.4.0"` (line ~96).

### 1b. CFG — add a `"scout"` block (place it right after the `"roi"` entry, before the closing `}` of CFG at line ~188)
```python
    "scout": {
        # v4.4 Movement 2 transduction scout. Pilot namespace v44pilot::,
        # NEVER pooled into any confirmatory analysis (law #6). Sizes the
        # SIGNAL -- aniso current vs horizon mismatch (Delta-tau) and drive
        # amplitude (Tc) -- not the noise. Cells stand alone; no cross-cell
        # aggregation. Each cell is compared only to its own B=64 floor.
        "blocks": 8,
        "scale": 10.0,
        "cells": [
            {"label": "A",    "tx": 0.1,  "ty": 2.0, "Tc": 1.0},  # widest horizon mismatch
            {"label": "B",    "tx": 0.25, "ty": 2.0, "Tc": 1.0},  # mismatch mid
            {"label": "C",    "tx": 0.1,  "ty": 1.0, "Tc": 1.0},  # amplitude-only
            {"label": "D",    "tx": 0.25, "ty": 1.0, "Tc": 1.0},  # replica bridge to v4.3 (0.25,1.0)
            {"label": "AxT2", "tx": 0.1,  "ty": 2.0, "Tc": 2.0},  # Tc sweep at widest pair
            {"label": "AxT4", "tx": 0.1,  "ty": 2.0, "Tc": 4.0},  # Tc sweep at widest pair
        ],
    },
```

### 1c. Add `scout_seed` (right after `pilot_seed`, line ~202)
```python
def scout_seed(unit_id):
    # v4.4 scout pilot namespace; scout results are NEVER pooled into analysis
    h = hashlib.sha256(("v44pilot::" + unit_id).encode()).digest()
    return int.from_bytes(h[:8], "big")
```

### 1d. Thread Tc as a runtime override into the two FROZEN force functions
`force_frozen(geom, S, xs, ys, r)` → add `Tc=None`; inside, `tc = e["Tc"] if Tc is None else Tc` and use `tc` in place of `e["Tc"]` on both component lines.
`force_frozen_aniso(geom, Sx, Sy, xs, ys, r)` → add `Tc=None`; same `tc = e["Tc"] if Tc is None else Tc`; use `tc` on both lines.
**Leave `force_online` untouched** — the scout is frozen-mode only.

### 1e. `run_chamber` — add `Tc_ov=None` param and pass it into the two frozen force calls
Signature gets `Tc_ov=None` (append to the existing kwargs). At the two frozen call sites (currently lines ~531/533):
```python
    Fcache = force_frozen_aniso(geom, S, S2, xs, ys, pos, Tc=Tc_ov)
    ...
    Fcache = force_frozen(geom, S, xs, ys, pos, Tc=Tc_ov)
```
(Default `Tc_ov=None` → `Tc=None` → `e["Tc"]` → byte-identical to before. Invariant #2.)

### 1f. Add `pilot_pair()` (place near `pilot()`, ~line 930)
```python
def pilot_pair():
    """v4.4 Movement 2 transduction scout. Runs CFG['scout'] cells in the
    v44pilot:: seed namespace (NEVER pooled). One NDJSON line per block,
    recording quad_loop_rate + omega_roi + occupancy per cell. Cells stand
    alone; each is later compared only to its own B=64 detection floor. Not
    gated -- a pilot declaration, chronicled at registration."""
    sc = CFG["scout"]
    for cell in sc["cells"]:
        tx, ty, Tc = cell["tx"], cell["ty"], cell["Tc"]
        for sb in range(sc["blocks"]):
            uid = f"C6s_{cell['label']}_tx{tx}_ty{ty}_Tc{Tc}_sb{sb}"
            seed = scout_seed(uid); t0 = time.time()
            res = run_chamber("frozen", tx, seed, scale=sc["scale"],
                              tau_y=ty, Tc_ov=Tc)
            out = {"type": "scout", "cell": cell["label"], "unit": uid,
                   "tx": tx, "ty": ty, "Tc": Tc, "block": sb, "seed": seed,
                   "config_hash": config_hash(), "version": VERSION,
                   "source_sha": SOURCE_SHA, "numpy": np.__version__,
                   "python": PYVER, "scale": sc["scale"],
                   "runtime_s": round(time.time() - t0, 1),
                   "quad_loop_rate": res["quad"]["quad_loop_rate"],
                   "omega_roi": res["roij"]["omega_roi"],
                   "occupancy_x": res["occupancy_x"]}
            print(json.dumps(out, separators=(",", ":")))
```
(Keys `res["quad"]["quad_loop_rate"]`, `res["roij"]["omega_roi"]`, `res["occupancy_x"]` are already confirmed present — `analyze()` and `selftest()` read them.)

### 1g. `main()` — add a `--pilot-pair` branch (beside `--pilot`, ~line 953)
```python
    if a[0] == "--pilot-pair":
        pilot_pair(); return
```

### Agent-1 done ⇒ HQ verifies: `--selftest` still PASS, `--plan` shows the scout cells under config, byte-identity of C4v/C5a `data` payloads vs the clean v43 copy, then commit.

---

## AGENT 2 — Analysis + selftest hardening (runs AFTER agent 1 is committed; touches ONLY: `perm_p`, `block_perm_p` + its call sites, `analyze`, `selftest`)

### 2a. Dead-code strip (v4.3 audit findings 1 & 5) — CONFIRM no live call sites first
- **`perm_p` (line ~643):** grep confirms only the `def` exists, no `perm_p(` call site. **Delete the whole function.** (`ks_stat` stays — it is used by the deleted fn only? re-grep `ks_stat(` before deleting `ks_stat`; if `ks_stat` is only used by `perm_p`, delete both; if used elsewhere, keep it.)
- **`one_sided` flag on `block_perm_p` (line ~767):** the ternary `if (v >= obs) if not one_sided else (v >= obs):` is a genuine **no-op** (both branches identical). Directionality actually lives in the **stat function** passed by the caller (signed-diff = one-sided for the vortex gate, abs-diff = two-sided for aniso). So: remove the `one_sided=False` param, make the line `if v >= obs:`, and remove the `one_sided=True` kwarg at every call site the grep found (in `analyze`'s nested `one_sided()` helper and `selftest`'s `osided`). **Semantics are unchanged** — note this in the commit so nobody later thinks the strip altered a test.

### 2b. Rule 3 — unified centering (Antigravity finding 4) — a REAL bug in current `analyze`
Currently `sign_consistency` centers on **zero** (`sum(1 for v in A1 if v > 0)`) while `opposite_signs` centers on the **equal-arm mean** (`(m1-me)*(m2-me)`). Unify **both** engine-gate clauses on the **equal-arm mean**. In `analyze` (aniso block, ~lines 738-739) and in `selftest`'s `g2_fire` (~lines 889-890), change the sign-consistency counts to be relative to the equal-arm mean `me`:
```python
    s1 = max(sum(1 for v in A1 if v > me), sum(1 for v in A1 if v < me))
    s2 = max(sum(1 for v in A2 if v > me), sum(1 for v in A2 if v < me))
```
(The C4v/vortex `sign_pos_k4/k8` counts stay `v > 0` — those are one-arm-vs-zero positive-control counts, a different reference by design. Only the ANISO engine-gate clauses unify on the equal-arm mean.)

### 2c. Rule 2 — prose/config grep-check in `selftest`
Add a check that extracts every numeric threshold from CFG and fails the selftest if any prose statement (the `--plan` `outcome_map` strings + docstrings) disagrees. Concretely: assert the `outcome_map` strings in `main()`'s `--plan` block agree with `CFG["thresholds"]["sign_consistency"]` (24/32) and `sign_consistency_aniso` (48/64) and the alphas — i.e. the numbers written in prose match the frozen config. Emit a `# prose/config grep-check: PASS/FAIL` line and fold `ok_grep` into `allok`. (Origin: Antigravity finding 3 — docstring said 24/32 while config+code said 48/64 inside a hash-frozen artifact.)

### 2d. Rule 1 — compound power: CARRY, do not exercise on aniso in the scout
Compound-gate power (all clauses jointly, MC ≥0.90) is **already implemented for the G1 vortex gate** (selftest lines ~827-853) — leave it intact. Compound power for the **aniso** gate needs measured effect sizes the scout hasn't produced yet; that is a **Movement 3 (registration)** computation, not a scout one. Do NOT try to fully exercise rule 1 on the aniso gate here. Just leave a comment marking it as carried-to-registration.

### Agent-2 done ⇒ HQ verifies: `--selftest` PASS (all gates incl. new grep-check), the centering change doesn't flip any existing selftest gate, then commit.

---

## After both agents (HQ, provenance lane — NOT delegated)
- Run `--selftest` (must PASS) and `--pilot-pair` at reduced scale as a smoke test.
- Compute final `source_sha` from the committed bytes; generate `prereg_v44.json` (from `--plan`) + `MANIFEST.sha256`.
- **Design note for the reviewers (flag, do not adjudicate):** Tc is a *linear* prefactor on the mean-field curl (`curl F = Tc·∂²/∂x∂y[S(τy)−S(τx)]`), so the Tc cells test a clean linear prediction; a cell that clears its floor "because Tc=4" is a **different scientific claim** than a geometric (Δτ) win. Record this in the prereg/design notes so ChatGPT (methodology) and Antigravity (pre-reg) can weigh it. HQ surfaces it; the physics-review seats adjudicate.
- Route: ChatGPT (methodology) → Antigravity (pre-reg audit) → HQ chronicles the pilot declaration + registers → Grok Build runs under contract (raw NDJSON only, HQ diffs).
