# Antigravity Mission — v4.4 Movement 2 Scout: Pre-Registration Audit

*Issued by HQ (Mac Studio Claude Code seat, provenance/final-say), 2026-07-07. Antigravity's lane in the v4.x pipeline is **adversarial audit, pre-registration** — it audits the scout **before** HQ chronicles/registers it and before Grok runs it. No seat grades its own work; Antigravity did not build this, HQ did. Precedent: the v4.3 analyzer audit (5 findings, 0 affecting registered verdicts, 1 real erratum) is the model for the deliverable.*

## Your charge

Adversarially audit the v4.4 scout **pre-registration** and try to **falsify** it before it is registered. The scout is a signal-sizing pilot (6 mismatch cells over Δτ × T_c, frozen anisotropic-horizon chamber, `v44pilot::` seed namespace, never pooled). Its decision rule was already found once to be self-defeating (the registered "3× floor" gate pre-committed the pilot to a null); v3 is the recalibration. **Your job is to break v3 the way v2's rule was broken — find the next such defect, or certify there isn't one.**

## Audit surface (all on branch `v4.4-scout-draft`, dir `v4/v44/`)

- `v44_scout_DECISION_RULE_v3.md` — **the primary target**: the ratifiable four-band rule (GREEN/AMBER/RED/ANOMALOUS), pivot logic, estimand pin, precondition runs.
- `v44_scout_DECISION_RULE_v2_DRAFT.md` — the reasoning trail + the defect v3 fixes (context, not the target).
- `receipts/06_scale10_diagnostics.md`, `receipts/07_signstability.md` — HQ's measured evidence; audit the claims against the numbers.
- `v44_scout.py` (frozen, source_sha `0b65a9ee92b9fe2c`), `prereg_v44.json`, `SCOUT_DECLARATION.md`, `MANIFEST.sha256`.
- Canonical interpreter `/usr/bin/python3` (numpy 2.0.2). Reproduce, don't trust prose.

## Falsification targets (attack these specifically)

1. **Can the rule reach BOTH outcomes on the right data?** This is the load-bearing check — v2 failed it. Simulate: (a) inject a true effect at ~1×, ~2×, ~3× floor and confirm GREEN fires with sane probability at the registrable sizes; (b) inject a true null and confirm the pivot can fire (after extension) — but ONLY through the legitimate path. If either the register branch is unreachable for plausible effects, or the pivot fires on an underpowered non-null, that is a blocking finding. (Law #2 / #3: gates must be able to fail on null AND pass on signal — compound, not per-contrast.)
2. **Estimand coherence.** Independently re-derive the GREEN threshold under option (a): two-arm `floor(B_conf)` vs one-arm-plus-reference SE. Is `sd·√(1/8+1/64)` the right SE, or does the equal-arm-≈0 assumption hide variance? Recompute `floor(96)=0.557·sd` and every stated multiple. If the pinned estimand is still mixing one-arm/two-arm quantities, flag it.
3. **The sign-stability precondition (the one HQ flagged as load-bearing).** v3 gates the pivot on a seed-averaged per-cell mean-field sign check. Attack it: is the unanimity criterion defined with a threshold? Is seed-averaging actually sufficient given a single grid's ROI curl is noise-dominated at M=400 *and* M=4000 (receipt 07)? Could a cell pass the precondition yet still have a self-cancelling realized 16-block mean? If the precondition can rubber-stamp an M=400 artifact, the whole null branch is compromised.
4. **ANOMALOUS + wrong-sign handling.** Confirm a large wrong-sign current cannot band RED and feed the pivot. Confirm per-cell predicted signs are actually pre-registered (not derived post hoc), or that the two-sided fallback is used with the correct 2.30× threshold.
5. **AMBER terminal / finiteness.** Confirm the extend→escalate→ceiling loop is finite and not a sequential-testing leak that inflates false-register. Check the B_conf escalation (96→128) is arithmetically consistent with the floor drop.
6. **T_c cells.** Verify the linear-response claim (signal ∝ Tc, net mean/floor up ~2–2.5× at Tc=4) against the code (`force_frozen_aniso`, F ∝ tc). Confirm the SD-vs-Tc growth is not being over- or under-interpreted, and that a Tc-cell "win" is labeled a drive-amplitude claim, not geometric.
7. **Law #4 grep.** Every numeric threshold in prose vs config: the frozen t₇ convention, the GREEN/RED multiples, and the stale "B=64 floor" hard-coded in `CFG["scout"]` comments + `pilot_pair` docstring if B_conf moves to 96/128 (config_hash + prereg re-issue).
8. **Frozen-artifact + quarantine invariants.** Confirm v3 changes are additive (harness/prereg/manifest byte-untouched, per law #9), that `config_hash` covers the full swept design, and that `v44pilot::` units are never pooled into any confirmatory analysis (law #6).

## Deliverable

A findings list, each ranked by **verdict-impact** (does it change whether the scout should register/run, or is it an erratum?), each with a **concrete falsification scenario** (inputs → wrong outcome), following the v4.3 audit format. Close with a one-line verdict: **ratifiable as-is / ratifiable with the listed fixes / not ratifiable**, and name the single most load-bearing fix if any.

## Out of scope (do NOT)

- Do not register or chronicle the scout (HQ registers after your audit clears).
- Do not run the scout itself, edit the frozen harness, or grade your own future work.
- Do not resolve Anthony's open design decisions (M_grid/primary/blocks/B_conf) — audit the rule's *coherence under whatever he picks*, and flag where a decision materially changes your findings.

## Standing law you audit against (violate-none)

Prereg-before-run + hash anchors (#1); gates fail-on-null (#2); compound-power ≥0.90 (#3); prose/config grep (#4); one centering reference = equal-arm mean (#5); pilots quarantined + never pooled (#6); raw NDJSON primary (#7); reset-vs-closed-NESS label distinction (#8); hash-frozen artifacts never edited, errata alongside (#9). Full text in `~/.claude/CLAUDE.md` "Standing experimental law."
