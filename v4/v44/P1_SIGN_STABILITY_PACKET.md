# P1 SIGN-STABILITY — DECISION PACKET

**Status:** DIAGNOSTIC. **Nothing here registers anything or authorizes any run.**
Registration is Anthony's gate and his alone (law #1).
**Seed namespace:** `diag10::` — quarantined, declared, disjoint from the registered
`precond_P1::` sets (77001–77032 @ M=4000; 78001–78016 @ M=400). **Never pooled** (law #6).
**Interpreter:** `/usr/bin/python3` (3.9.6, numpy 2.0.2) — the canonical one.
**Scope:** answers open ChatGPT review item **Q5** (sign-stability definition).
**Prepared for:** Anthony + an external adversarial seat. This is registration-gating.

---

## 0. TL;DR — the question I was asked is already closed. The answer it uncovers is not.

**The (a)-vs-(b) choice does not need to be made.** Decision-rule **v3.5 §1.1 already
pins it**, exactly as HQ leaned in the v3 OPEN ITEM. The task framing (and
`CONDUCTOR_SCORE.md`, and `~/.claude/CLAUDE.md`) quote the **v3** text; that text is
two revisions stale. I verified against the primary source before doing anything else.

**But running the ratified definition for the first time surfaces a blocker:**

> **The registered directional prediction σ_cell does not exist.**
> At the registered instrument (N_avg = 32 seeds, M = 4000), the seed-averaged ROI curl
> is **statistically indistinguishable from zero in all six cells** (|t| = 0.05 – 0.35,
> all p > 0.72, n = 64). Its sign **flips on a fresh 32-seed draw 40 – 49 % of the time**.
> σ_cell is a coin flip.
>
> Consequently **P1-B cannot pass.** It asks for ≥ 12/16 (75 %) per-seed M=400 sign
> agreement with σ_cell. Measured agreement is **0.42 – 0.62** — a coin flip against a
> coin flip. Every cell registers **UNSTABLE**, and `STABLE` is in fact *undefined*
> (there is no σ to agree with).
>
> **`STABLE` is a precondition on every RED counted toward the all-RED pivot (§5(ii)).
> As ratified, the pivot is un-declarable. The scout cannot mint a null — ever.**

**This is a law #3 violation sitting inside the ratified rule.** Law #3 requires a
positive control to *demonstrably be able to PASS*. P1-B, run against the physics,
cannot. The rule was compound-power-simulated (OC v3.5, 0.980) — but the OC sim
**assumes** `stable_flags` as an input; it never simulated whether P1-B can produce one.

**Recommendation: amend before registration. My pick is Option 4 (retire the suspenders,
license on the belt), with Option 3 as the buy-it-back path.** Reasoning in §6. **I am
not picking for the program** — this is a registration-gating definition and needs
Anthony plus an external adversarial seat.

---

## 1. The definitional question, and why it is already answered

### 1.1 What the task (quoting v3) says is ambiguous

v3 §1.1 line 65: *"A cell is STABLE iff the seed-averaged mean-field curl is
**sign-unanimous** across the registered seed set at M=400."* This conflates:

- **(a) AVERAGE-then-CURL** — average N seeds into one mean field, take its curl → **one
  sign**. Nothing to be "unanimous" over. The word is incoherent under this reading.
- **(b) PER-SEED-CURL-then-UNANIMITY** — per-seed curls, require sign unanimity across
  seeds. A genuine unanimity criterion.

v3 flagged this itself, as an **OPEN ITEM** (v3 §1.1 line 69), and noted receipt 07's
+4/−4 at 8 seeds where a 3-seed set had been called "unanimous."

### 1.2 v3.5 closed it — and closed it correctly

```
v3.5 §1.1  P1-A: ROI-integrated curl of the seed-averaged mean aniso force field
                 at M=4000 -- "average-then-curl. One sign per cell."   <- reading (a)
                 N_avg = 32 seeds  precond_P1::77001...77032
           P1-B: "disjoint predeclared set, per-seed ROI curl at M=400;
                 STABLE iff >= 12/16 (N=16 seeds 78001...78016) agree in sign
                 with sigma_cell."                                      <- reading (b)
```

- `grep -i unanim v44_scout_DECISION_RULE_v3.5.md` → **zero hits.** The incoherent word
  is gone. σ_cell is a mean-field object (a); STABLE is a per-seed agreement test (b).
- **Task item 4 — the "cross-resolution pin ChatGPT's block demanded: an M=4000-registered
  sign, with ≥75 % per-seed agreement at M=400" — is *already ratified P1-B*.**
  12/16 = **0.75**. It is numerically the same pin. It does not need to be added.

**Do not re-open (a) vs (b) as a choice.** Doing so would repeat the stale-summary error
that already nearly caused HQ to commission a "v3.1" that had been superseded by v3.5,
and would brush against law #1.

### 1.3 An algebraic point that dissolves the rest of the ambiguity

The ROI-integrated mixed partial is a **linear** functional of the entropy field
(finite-difference stencil + sum are both linear). Therefore, exactly:

```
curl( mean_over_seeds(field) )  ==  mean_over_seeds( curl(field) )
```

Verified numerically to ~1e-13 in every cell (`identity_residual` in the JSON).

**So definition (a) is not a different object — it is the arithmetic MEAN of the very
per-seed curls that definition (b) takes a sign-vote over.** (a) = the mean; (b) = the
sign-vote. Same sample, two summaries. There is no field-averaging magic. This also
means "average-then-curl" and "curl-then-average" are interchangeable implementations —
the *only* real choice was ever mean-vs-vote, and v3.5 uses **both, for their two
distinct jobs** (mean → the prediction; vote → the robustness check). That design is right.

---

## 2. Method, and its validation against the frozen receipt

Statistic (receipt 07's, and the instrument's own): the **signed ROI-integrated mixed
partial** `∂²[S(τ_y) − S(τ_x)]/∂x∂y`, which is `curl F / Tc` for the anisotropic
causal-entropic force (`v44_scout.force_frozen_aniso`).

- **Instrument fidelity:** reproduces the scout's per-block grid construction exactly —
  one RNG per block, τ_x grid drawn **first**, τ_y grid drawn **second from the same
  stream** (`v44_scout.simulate()`, `mode='frozen'`).
- **Operator:** the 4-point 2h central-difference stencil the scout itself uses
  (`v44_scout.py` selftest, `mixed_partial_mag`), summed over the ROI (center (2.0,1.0),
  half (0.45,0.45)). Cross-checked against an independent `np.gradient`-twice estimator.
- **`Tc > 0` scales the curl multiplicatively and cannot flip its sign** ⇒ A, AxT2, AxT4
  share one sign; only the four distinct (τ_x, τ_y) pairs carry distinct grid work.

**Validation — reproduces receipt 07's distribution scale** (different seeds, so
statistical not bit-exact agreement is the correct bar):

| cell / M | receipt 07 (frozen) | diag10:: (this run) |
|---|---|---|
| A (0.1,2.0) M=400, sd | 4.95 | **5.20** |
| C (0.1,1.0) M=400, sd | 4.86 | **6.44** (n=16) / 5.69 |
| A (0.1,2.0) M=4000, sd | 1.47 | **1.53** |
| C (0.1,1.0) M=4000, sd | 1.11 | **1.67** |

Same statistic, same units, same noise scale. Method validated.

---

## 3. RESULTS — six cells, 64 seeds per pair, both M

### [1] Definition (a) — σ_cell at M=4000 (the registered prediction)

| cell | (τx,τy) | Tc | DEF_A curl | SE | t | p | σ | significant? |
|---|---|---|---|---|---|---|---|---|
| A | (0.10,2.0) | 1.0 | −0.0238 | 0.191 | 0.12 | 0.901 | − | **no → INDETERMINATE** |
| B | (0.25,2.0) | 1.0 | −0.0100 | 0.203 | 0.05 | 0.961 | − | **no → INDETERMINATE** |
| C | (0.10,1.0) | 1.0 | +0.0515 | 0.208 | 0.25 | 0.805 | + | **no → INDETERMINATE** |
| D | (0.25,1.0) | 1.0 | +0.0670 | 0.191 | 0.35 | 0.726 | + | **no → INDETERMINATE** |
| AxT2 | (0.10,2.0) | 2.0 | −0.0476 | 0.383 | 0.12 | 0.901 | − | **no → INDETERMINATE** |
| AxT4 | (0.10,2.0) | 4.0 | −0.0952 | 0.766 | 0.12 | 0.901 | − | **no → INDETERMINATE** |

**n = 64 (double the registered N_avg=32). Not one cell's mean-field ROI curl is
distinguishable from zero.** Under v3.5 §1.1 ("below the predeclared negligibility floor
→ INDETERMINATE"), **all six cells register INDETERMINATE and band two-sided.**

> **Honest scoping (law: absence of signal ≠ absence of effect).** I do **not** claim the
> true curl is zero. Cell A's 95 % bound is [−0.399, +0.351]. I claim precisely this:
> **at the registered instrument (N_avg = 32, M = 4000), σ_cell's sign is not
> identifiable.** A small true curl could exist and be invisible here.

### [2] Definition (b) — per-seed sign unanimity

| cell | M=4000 (n=64) | frac | p | M=400 (n=64) | frac | p |
|---|---|---|---|---|---|---|
| A | +30/−34 | 0.53 | 0.708 | +37/−27 | 0.58 | 0.260 |
| B | +32/−32 | 0.50 | 1.000 | +31/−33 | 0.52 | 0.901 |
| C | +29/−35 | 0.55 | 0.532 | +32/−32 | 0.50 | 1.000 |
| D | +32/−32 | 0.50 | 1.000 | +40/−24 | 0.62 | 0.060 |
| AxT2 | +30/−34 | 0.53 | 0.708 | +37/−27 | 0.58 | 0.260 |
| AxT4 | +30/−34 | 0.53 | 0.708 | +37/−27 | 0.58 | 0.260 |

**Unanimity is achieved nowhere, at either resolution. Every split is consistent with a
fair coin.** Strict definition (b) ⇒ **no cell is STABLE, ever.**

### [3] Ratified P1-B (the cross-resolution pin, already in v3.5)

σ from DEF_A @ M=4000; STABLE iff ≥12/16 (75 %) of per-seed M=400 curls agree.

| cell | σ | M=400 agreement | rate | P(≥12/16 at that rate) | verdict |
|---|---|---|---|---|---|
| A | − | 27/64 | 0.422 | 0.008 | **UNSTABLE** |
| B | − | 33/64 | 0.516 | 0.050 | **UNSTABLE** |
| C | + | 32/64 | 0.500 | 0.038 | **UNSTABLE** |
| D | + | 40/64 | 0.625 | 0.223 | **UNSTABLE** |
| AxT2 | − | 27/64 | 0.422 | 0.008 | **UNSTABLE** |
| AxT4 | − | 27/64 | 0.422 | 0.008 | **UNSTABLE** |

*(and in every cell σ is itself INDETERMINATE, so P1-B is strictly **undefined** — the
verdicts above are what the code would produce if you fed it the point-estimate sign.)*

**Even granting a real σ, P1-B fires STABLE ~1–5 % of the time. It is not a gate; it is
noise with a threshold on it.**

### [4] Is σ_cell reproducible at all? (bootstrap, 20 000 draws of N_avg=32 from the 64)

| cell | sign @ n=64 | **P(sign flips on a fresh 32-seed set)** | verdict |
|---|---|---|---|
| A | − | **0.464** | COIN FLIP |
| B | − | **0.486** | COIN FLIP |
| C | + | **0.436** | COIN FLIP |
| D | + | **0.400** | COIN FLIP |
| AxT2 | − | **0.467** | COIN FLIP |
| AxT4 | − | **0.461** | COIN FLIP |

**A registered σ_cell would flip sign on a fresh seed set 40–49 % of the time.**

### [5] The v4.3 registered prediction, revisited — an erratum candidate

`prereg_v44.json`, `aniso_predicted.derivation`:

> *"ROI-integrated curl of mean aniso force field, M=4000 grids, seeds 77001/77002/77003,
> **unanimous** (+5.67e-3, +1.54e-3, +9.27e-3)"*

Three **per-seed** values, all +, called "unanimous" — **that is reading (b) at N = 3**,
inside the live prereg, under a label ("curl of mean aniso force field") that says
reading (a). The conflation is not hypothetical; it is registered.

At that same arm (0.25, 1.0), M=4000, diag10:: measures **+32/−32 (p̂ = 0.50)**.
**P(3 seeds land unanimous | this coin) = 0.25.** A 3-seed unanimity here is a **1-in-4
coin-flip outcome**, not evidence of a stable sign.

> **This does not retroactively break v4.3.** The v4.3 aniso prediction was explicitly
> **SECONDARY, not a gate condition** (`prereg`: "NOT a gate condition; G2 gates on
> antisymmetry"). The v4.3 *verdicts* do not rest on it. But it **cannot be inherited as
> v4.4's registered σ_cell**, which is exactly what §1.1's "v4.3 recipe" lineage does.
> **Recommend recording an erratum alongside the frozen artifact (law #9 — never edit).**

---

## 4. Estimator-robustness

The whole result is **scale-invariant** — every conclusion is about signs. Re-running the
entire analysis with an independent `np.gradient`-twice, area-weighted estimator gives
**identical t-statistics, identical p-values, identical sign splits, identical verdicts**
(the two estimators are proportional; ratio exactly 1/(dx·dy) = 100). This is not an
artifact of my choice of derivative operator.

---

## 5. Why P1-B is *structurally* unsatisfiable (not just unlucky)

For per-seed sign agreement to reach the 75 % that P1-B demands, a single grid's curl
needs per-seed **SNR ≈ Φ⁻¹(0.75) ≈ 0.67**. Measured per-seed SNR at M=400 is
**0.009 – 0.21**. Grid noise falls as 1/√M (confirmed: sd 5.2 @ M=400 → 1.53 @ M=4000,
ratio 3.4 ≈ √10). So reaching SNR 0.67 from a single grid needs

**M_grid ≈ 400 × (0.67/0.03)² ≈ 2 × 10⁵ — per block.** Infeasible.

**This is receipt 07's finding, arriving at the gate.** Receipt 07 already said it:
*"a single grid's ROI curl is noise-dominated at BOTH M — you cannot read a reliable sign
from one grid realization at either… The real levers are more blocks and/or seed-averaged
grids per block (a design change), not M-per-block."* P1-B asks a single M=400 grid to do
precisely the thing receipt 07 proved it cannot do. **The receipt was right and the rule
did not absorb it.**

**Remedy sizing for σ_cell (definition (a)):** to resolve the *sign* at one-sided 95 %,
taking the (non-significant) 64-seed point estimates at face value:

| pair | N_avg needed | (if the true curl is 2× the point estimate) |
|---|---|---|
| (0.25,1.0) | **1 405** | 351 |
| (0.10,1.0) | **2 834** | 708 |
| (0.10,2.0) | **11 198** | 2 800 |
| (0.25,2.0) | **71 382** | 17 846 |

Registered N_avg = **32**. Even the friendliest cell is off by ~44×. *(N_avg in the low
thousands is not crazy on this machine — the 64-seed M=4000 sweep over 4 pairs ran in
~90 s wall on 14 cores. σ_cell is buyable. **P1-B is not** — it is a per-*block* SNR
problem, and no amount of seed-averaging in the precondition fixes the scout's blocks.)*

---

## 6. THE DECISION — four options, what each licenses, and my pick

`STABLE` gates whether a RED counts toward the all-RED pivot (§5(ii)). Get it wrong one
way → a live effect is abandoned as a null on an instrument artifact. Get it wrong the
other → **the null is blocked forever.** As ratified, we are hard against the second wall.

### Option 1 — Register as-is, accept all-UNSTABLE
- **Licenses:** nothing. Outcome 2 (all-RED pivot) becomes unreachable by construction.
  The scout can still return GREEN (candidate signal) or an honest ceiling bound.
- **Cost:** the program can never declare the null it was built to be able to declare.
  A gate that cannot pass is a **law #3 violation**. **I recommend against.**

### Option 2 — Buy σ_cell (raise N_avg to ~3 000), keep P1-B
- **Licenses:** a real registered direction; one-sided banding becomes legitimate.
- **Cost:** ~hours of compute (cheap). **But it does NOT fix P1-B** — per-seed M=400
  agreement stays ~50 % no matter how precisely you know σ. STABLE still never fires.
  **Necessary if you want one-sided banding at all; not sufficient. Insufficient alone.**

### Option 3 — Change the instrument: seed-averaged grids per block
- Replace "one fresh grid per block" with "K averaged grids per block" (receipt 07's own
  recommendation). Per-block SNR ∝ √K. K ≈ 500 would put per-seed agreement near 75 %.
- **Licenses:** a STABLE that is both *meaningful* and *passable*; the belt-and-suspenders
  guarantee actually becomes two-layered.
- **Cost:** a **design change to the scout**, ~500× the grid compute per block, a new
  config_hash, a new prereg, and it invalidates the OC sim's block-noise model (which was
  calibrated to receipt-06 anchors). This is a **v4.5-scale re-architecture**, not an
  amendment. Also: P2 (the Tc×M gate) would need re-running.

### Option 4 — Retire the suspenders; license the pivot on the belt alone ⟵ **MY PICK**
- **Drop σ_cell and `stable_cell` from the pivot license.** Band **all three statistics
  two-sided** (occupancy already is). Delete §5(ii). The all-RED pivot rests on the
  **belt**: the two-sided `|μ̂|` magnitude bound (§3), which is **direction-complete**.
- **Licenses:** the all-RED pivot, honestly, on a bound over `|μ̂|` — no direction claim,
  no sign registration, nothing that depends on an unmeasurable object.
- **Costs, stated plainly:**
  - Two-sided banding is **less powerful** than one-sided. RED needs a tighter CI; the
    ladder will run longer / more cells will terminate AMBER. **The OC sim must be
    re-run in the all-two-sided configuration to re-establish compound power ≥ 0.90
    (law #3). If it comes in under 0.90, Option 4 fails and we are back to Option 3.**
    *This is the one number that decides between my pick and the re-architecture, and I
    have not computed it. It is the next thing to compute.*
  - We lose the ANOMALOUS band on the primary (it needs a predicted direction), which is
    a real loss — the wrong-sign-current alarm goes away. **Mitigation:** it is replaced
    by the two-sided GREEN, which fires on `|μ̂|` in *either* direction. Direction-complete,
    but it cannot *distinguish* wrong-sign from right-sign. §8's disposition machine
    would need rewording.

**Why Option 4 and not Option 3:**

1. **The suspenders were already known to be inert in the regime that matters.** v3.5
   §1.1, scoped by the D6 finding, concedes it: *"Under transduction inversion… the
   suspenders are structurally INERT and the belt is the SOLE wrong-sign guarantee."*
   D6 established that the belt alone holds the tolerance (**invalid pivot ≈ 0.0006 ≤
   0.02**). **The program has already measured that it does not need the suspenders.**
   This finding just shows they were never *attached*.
2. **A gate that fires 1–5 % of the time on noise is worse than no gate.** It doesn't just
   fail to protect — it launders a coin flip as a certification. That is the v4.1
   occupancy-gate failure (law #2) wearing the opposite costume: v4.1's gate *couldn't
   fail*; P1-B *can't pass*. Both are gates that don't measure what they claim.
3. **Option 3 is a real answer but it is a different experiment.** 500× block compute, new
   prereg, new config_hash, re-run P2, re-calibrate the OC sim's noise model. If Anthony
   wants the two-layer guarantee, that is the honest price — but it should be a
   deliberate v4.5 decision, not a patch smuggled into v4.4's registration.
4. **Option 4 is the smallest amendment that leaves every claim true.** The pivot claim
   (§2.1) is already magnitude-scoped ("raw mismatch currents are sub-floor in the
   `quad_loop_rate` statistic"). It never needed a direction. **The sign machinery was
   load-bearing for the *banding efficiency*, not for the *claim*.**

**What I would NOT do:** lower P1-B's threshold (e.g. 12/16 → 9/16) to make it pass. That
converts a gate that can't pass into a gate that can't fail — a law #2 violation — and
would be the single worst move available.

---

## 7. What HQ / Anthony / the external seat must decide

1. **Confirm or reject the blocker.** Is σ_cell unidentifiable at N_avg=32? *(An external
   adversarial seat should recompute from the raw curls — the JSON has all 512 per-seed
   values. This is the check I most want challenged.)*
2. **Pick the amendment path** (1 / 2 / 3 / 4, or a hybrid: e.g. **2 + 4** — buy σ_cell so
   the *sign* is registrable and reportable as a descriptive prediction, but do not let
   `STABLE` gate the pivot).
3. **Compute the deciding number:** re-run the OC sim with all-two-sided banding and no
   STABLE precondition. **If compound gate power ≥ 0.90, Option 4 is live. If not,
   Option 3.** *(Not done here. This is the top of the next queue.)*
4. **Record the erratum** on `prereg_v44.json`'s `aniso_predicted` (law #9 — alongside,
   never editing the frozen artifact).
5. **Fix the documentation lag** that made this task ask for a "v3.1" and a pin that both
   already exist: `CONDUCTOR_SCORE.md` and `~/.claude/CLAUDE.md` still say v3.1-frontier.

**Registration remains HELD.** Nothing in this packet changes that, and nothing in it
should be read as authorizing a run.

---

## 8. Artifacts

| file | what |
|---|---|
| `p1_signstability_diag10.py` | the diagnostic driver (both definitions, both estimators, `diag10::` seeds) |
| `p1_signstability_analyze.py` | the analysis (definitions, P1-B, bootstrap, v4.3 revisit) |
| `diag10_signstability_full.json` | **raw** — 512 per-seed curls, 4 pairs × 2 resolutions × 64 seeds, both estimators |
| `diag10_signstability_validate.json` | raw — the receipt-07 reproduction |
| `diag10_analysis_stencil.txt` | analysis output (stencil estimator) |

Reproduce:
```
NPROC=14 NSEEDS=64 /usr/bin/python3 p1_signstability_diag10.py full   # ~90 s wall
/usr/bin/python3 p1_signstability_analyze.py                          # stencil
EST=gradient /usr/bin/python3 p1_signstability_analyze.py             # cross-check
```
