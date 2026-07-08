# v4.4 Scout Decision Rule v3.5 — RATIFICATION RECEIPT

**Ratified by:** Anthony Vasquez Sr. (Temple of Two — final-say / human gate)
**Date:** 2026-07-08 (America/New_York)
**Ratified artifact:** `v44_scout_DECISION_RULE_v3.5.md` @ commit `5df6d98` (branch `v4.4-scout-draft`)
**Recorded by:** HQ (Mac Studio Claude Code seat, provenance)

---

## What was ratified
The v4.4 scout **decision rule / methodology** at v3.5 is human-signed-off as the canonical rule. This follows two independent external reviews (ChatGPT Deep Research methodology pass + Antigravity R3 adversarial audit — **both APPROVE-WITH-REVISIONS**) and HQ's arbitration + 4-agent verification of the one load-bearing dispute (rerun power → honest 0.858, fixed by n_rerun 40→56).

## Forks confirmed (both were HQ-recommended-pending-Anthony; now RATIFIED)
1. **Occupancy-guard strength → ASYMMETRY KEPT.** Occupancy retains its GREEN-veto + mandatory claim caveat (weaker than omega's ladder-driving, INCONCLUSIVE-blocking guard). Rationale ratified: occupancy has no registered sign, no calibrated transfer function, and its v4.3 direction is protocol-bound (law #8). The symmetric alternative is closed (not adopted).
2. **Operating point → CONSERVATIVE point ADOPTED.** The operating point that preserves ≥0.90 compound power and the honest belt guarantee under the reference-uncertain SE.

## Scope of this ratification (important — rule-ratification ≠ run-registration)
This ratifies the **decision rule**. It does **NOT** register the scout or authorize the run. Per standing law #1, registration is a **separate human gate** that comes only after the remaining build artifacts exist and a second explicit "register" from Anthony. Ratifying v3.5 **unlocks** that build:

## What this unlocks (remaining path to a live run)
1. **Registration-grade OC simulator** — build per `OC_SIM_BUILD_SPEC.md`: runs the full v3.5 rule end-to-end across all predeclared scenarios, produces operating characteristics + the **compound six-cell power MC ≥0.90** (law #3), versioned + seed/hash-pinned. Populates v3.5's TBD compound-power numbers.
2. **P1/P2 preconditions** run + registered (freeze per-cell signs σ_cell/σ^ω_cell, the Tc-cell M, the gating roster).
3. **Re-issue `prereg_v44.json`** with the ratified config (n_rerun=56 + ratified forks) → new sha256; recompute `MANIFEST.sha256`.
4. **HQ registers** with receipts (config_hash + source_sha + prereg sha256, verified readback) — **on Anthony's explicit register-go** (law #1).
5. **Grok runs** the scout — raw NDJSON primary record, HQ diffs.

## Standing law preserved
Prereg before run (#1); registration remains human-gated; frozen artifacts (`v44_scout.py`, current `prereg_v44.json`, `MANIFEST.sha256`) untouched until the registration re-issue; the erratum trail (0.912→0.858) recorded not erased (#9).

*Ratification receipt is provenance, not registration. The scout is not registered and has not run.*
