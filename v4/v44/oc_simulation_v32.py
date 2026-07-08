#!/usr/bin/env python3
"""
oc_simulation_v32.py — Operating-characteristic (OC) simulation for the
v4.4 transduction-scout decision rule, FROZEN spec v3.2.

Interpreter: /usr/bin/python3 (numpy 2.0.2). Deterministic, rng pinned.

FROZEN RULE v3.2 (all magnitudes in units of the cell's own block SD, sd_cell=1):
  floor(sd)  = 3.858 * sd * sqrt(2/B)   -> 0.5569 @ B=96, 0.4823 @ B=128
  SE(sd, n)  = sd * sqrt(1/n + 1/64)    -> 0.2795 @ n=16, 0.2165 @ n=32
  Student-t:  n=16 (df 15): one-sided 1.753 / two-sided 2.131
              n=32 (df 31): one-sided 1.696 / two-sided 2.040
  chi2 upper-SD factor (sd_up = sd_hat * factor): 1.437 @ n=16, 1.268 @ n=32

  One-sided (registered sigma in {+1,-1}), x = sigma * mu_hat:
    GREEN      x - t*SE(sd_hat) > floor(sd_hat)
    ANOMALOUS  x < -t*SE(sd_hat)                    [checked BEFORE RED]
    RED        (not GREEN/ANOMALOUS) AND
               |mu_hat| + t*SE(sd_hat) < floor(sd_hat) AND
               |mu_hat| + t*SE(sd_up)  < floor(sd_up)   [v3.2 magnitude belt]
    else AMBER
  Two-sided (sigma = None, INDETERMINATE): GREEN |mu_hat| - t*SE > floor;
    RED same magnitude conjunction; else AMBER; no ANOMALOUS. Two-sided t.

  v3.1 comparator ("aligned-RED, no |mu| bound"): identical except one-sided
  RED uses x = sigma*mu_hat in place of |mu_hat| in both RED clauses.

LADDER: stage1 = 16 blocks @ B=96. AMBER -> stage2 = 32 blocks @ B=96
  (first 16 blocks KEPT, 16 appended). AMBER -> stage3 = the SAME 32-block
  sample re-banded @ B=128 (spec v3.2 sec 9.1 draw model). AMBER at stage3
  -> terminal INCONCLUSIVE_AT_CEILING (blocks the pivot).
  GREEN / RED / ANOMALOUS are terminal at any stage.

PIVOT licensed iff >=1 cell banded AND no ANOMALOUS AND no GREEN AND no
  INCONCLUSIVE_AT_CEILING AND every cell RED AND every direction-registered
  RED cell STABLE (P1-B). Any GREEN -> register; any ANOMALOUS -> investigate;
  any INCONCLUSIVE_AT_CEILING -> no pivot.

MODEL P1 (STABLE is MODELED, not hardcoded — the v3.2 requirement):
  P1-A sigma registration: sigma_cell = sign of the cell's TRUE mean-field
    current. A truly-null cell (mu_true = 0) has no sign -> registers
    INDETERMINATE (sigma = None) and bands two-sided; STABLE is vacuous for
    it (P1-B agreement is measured against a registered direction, which an
    INDETERMINATE cell does not have). Scenario S2 overrides cell A's
    registration to +1 to model a WRONG-SIGN registration.
    (Sensitivity S1b models the alternative: null cells force-registered
    sigma=+1, STABLE at chance.)
  P1-B STABLE: N=16 predeclared per-seed M=400 curls; each seed's curl
    sign-agrees with the cell's TRUE current direction with probability
       p_true = 0.5 + 0.5 * rho * tanh(|mu_true| / NOISE_SCALE)
    rho in {0.0, 0.3, 0.6, 0.9} is the coupling strength (rho=0: per-seed
    sign is a coin flip regardless of truth, STABLE ~ chance = 0.0384;
    rho->1: per-seed sign follows the true current almost surely).
    NOISE_SCALE = floor(96)/0.4 = 1.3922: receipt-07 puts a single-M400-curl
    SNR at ~0.3-0.5 for a floor-magnitude current; 0.4 is taken as midpoint,
    so |mu_true| = floor gives tanh(0.4) = 0.380 per-seed alignment signal.
    Agreement with the REGISTERED sigma: p_true if sign(mu_true) == sigma_reg,
    (1 - p_true) if opposed, 0.5 exactly if mu_true == 0.
    STABLE iff >= 12/16 seeds agree with the REGISTERED sigma_cell.

DATA MODEL (spec sec 9.1): block statistics iid Normal(mu_true, sd_true) in
  block-SD units => mu_hat ~ N(mu_true, sd_true/sqrt(n)) and
  sd_hat ~ sd_true * sqrt(chi2_{n-1}/(n-1)); accumulation dependence
  (16 -> 32) and the B96->B128 same-sample re-band are preserved exactly.
  mu_true is held fixed in block-SD units across the B=96 -> B=128 re-band.
"""
import json
import math

import numpy as np

RNG_SEED = 20260707          # rng pin proposed in DECISION_RULE v3.2 sec 9.1
NOISE_SCALE = 3.858 * math.sqrt(2.0 / 96.0) / 0.4    # = floor(96)/0.4 = 1.3922
STABLE_N, STABLE_K = 16, 12
RHOS = (0.0, 0.3, 0.6, 0.9)
N_MAIN = 50_000              # S1b, S3, S4, S5
N_TAIL = 200_000             # S1, S2 (tail-rate scenarios)

# band codes
AMBER, GREEN, RED, ANOM, INCONC = 0, 1, 2, 3, 4
BAND_NAMES = {GREEN: "GREEN", RED: "RED", ANOM: "ANOMALOUS",
              INCONC: "INCONCLUSIVE_AT_CEILING", AMBER: "AMBER"}

# stage -> (n_blocks, B, t_one_sided, t_two_sided, sd_upper_factor)
STAGES = {
    1: (16, 96, 1.753, 2.131, 1.437),
    2: (32, 96, 1.696, 2.040, 1.268),
    3: (32, 128, 1.696, 2.040, 1.268),
}


def floor_coef(B):
    return 3.858 * math.sqrt(2.0 / B)


def se_coef(n):
    return math.sqrt(1.0 / n + 1.0 / 64.0)


def raw_predicates(mu_hat, sd_hat, sigma, stage, rule):
    """Raw band predicates (no precedence guards). Vectorized.

    Returns (green, anom, red_raw) boolean arrays. AMBER = none of them
    after guards. sigma: +1/-1 one-sided, None two-sided. rule: v32 | v31.
    """
    n, B, t1, t2, fac = STAGES[stage]
    FLc, SEc = floor_coef(B), se_coef(n)
    se = sd_hat * SEc
    fl = sd_hat * FLc
    sd_up = sd_hat * fac
    se_up = sd_up * SEc
    fl_up = sd_up * FLc
    if sigma is None:
        t = t2
        green = np.abs(mu_hat) - t * se > fl
        anom = np.zeros_like(green)
        stat = np.abs(mu_hat)          # two-sided RED is already a |mu| bound
    else:
        t = t1
        x = sigma * mu_hat
        green = x - t * se > fl
        anom = x < -t * se
        stat = np.abs(mu_hat) if rule == "v32" else x   # v3.2 belt vs v3.1
    red_raw = (stat + t * se < fl) & (stat + t * se_up < fl_up)
    return green, anom, red_raw


def band_stage(mu_hat, sd_hat, sigma, stage, rule="v32"):
    """Band one cell at one stage with frozen precedence:
    GREEN, then ANOMALOUS (before RED), then RED, else AMBER."""
    green, anom, red_raw = raw_predicates(mu_hat, sd_hat, sigma, stage, rule)
    return np.where(green, GREEN,
           np.where(anom, ANOM,
           np.where(red_raw, RED, AMBER)))


def run_ladder(rng, n_trials, mu_true, sd_true, sigma, rule="v32"):
    """One cell through the frozen ladder. Returns (final_band, terminal_stage).

    Stage 1: first 16 blocks @ B=96. Stage 2: those 16 KEPT + 16 appended
    (all 32) @ B=96. Stage 3: SAME 32-block sample re-banded @ B=128
    (v3.2 sec 9.1). AMBER at stage 3 -> INCONCLUSIVE_AT_CEILING.
    """
    blocks = rng.normal(mu_true, sd_true, size=(n_trials, 32))
    mu1 = blocks[:, :16].mean(axis=1)
    sd1 = blocks[:, :16].std(axis=1, ddof=1)
    mu2 = blocks.mean(axis=1)
    sd2 = blocks.std(axis=1, ddof=1)
    b1 = band_stage(mu1, sd1, sigma, 1, rule)
    b2 = band_stage(mu2, sd2, sigma, 2, rule)
    b3 = band_stage(mu2, sd2, sigma, 3, rule)   # same sample, B=128 floor
    final = np.where(b1 != AMBER, b1,
            np.where(b2 != AMBER, b2,
            np.where(b3 != AMBER, b3, INCONC)))
    stage = np.where(b1 != AMBER, 1, np.where(b2 != AMBER, 2, 3))
    return final, stage


def stable_flags(rng, n_trials, mu_true, sigma_reg, rho):
    """Model P1-B STABLE for a direction-registered cell (see module docstring).

    Returns (bool array of STABLE, p_agree_registered)."""
    p_true = 0.5 + 0.5 * rho * math.tanh(abs(mu_true) / NOISE_SCALE)
    if mu_true == 0.0:
        p_reg = 0.5
    elif (mu_true > 0) == (sigma_reg > 0):
        p_reg = p_true                 # registration matches the true current
    else:
        p_reg = 1.0 - p_true           # wrong-sign registration
    k = rng.binomial(STABLE_N, p_reg, size=n_trials)
    return k >= STABLE_K, p_reg


def stable_tail_exact(p_reg):
    """Exact P(Binomial(16, p_reg) >= 12) — analytic check on modeled STABLE."""
    return float(sum(math.comb(STABLE_N, k) * p_reg ** k *
                     (1.0 - p_reg) ** (STABLE_N - k)
                     for k in range(STABLE_K, STABLE_N + 1)))


def band_dist(final):
    return {BAND_NAMES[c]: float((final == c).mean())
            for c in (GREEN, RED, ANOM, INCONC)}


def mc_se(p, n):
    return float(math.sqrt(max(p * (1.0 - p), 1.0 / n) / n))


def partition_scan():
    """Hard gate 6a: every (mu_hat, sd_hat) point receives exactly one band.

    Scans a dense mu_hat grid at several sd_hat values, all stages, both
    signs + two-sided, both rules. Also records raw-predicate overlaps
    (which the frozen precedence GREEN > ANOMALOUS > RED resolves).
    """
    mus = np.linspace(-5.0, 5.0, 4001)
    total = 0
    exactly_one = 0
    overlap_counts = {"v32": 0, "v31": 0}
    for stage in (1, 2, 3):
        for sigma in (+1, -1, None):
            rules = ("v32",) if sigma is None else ("v32", "v31")
            for rule in rules:
                for sd in (0.25, 0.5, 1.0, 2.0, 4.0):
                    sd_arr = np.full_like(mus, sd)
                    g, a, r = raw_predicates(mus, sd_arr, sigma, stage, rule)
                    n_pred = g.astype(int) + a.astype(int) + r.astype(int)
                    overlap_counts[rule] += int((n_pred > 1).sum())
                    final = band_stage(mus, sd_arr, sigma, stage, rule)
                    # after precedence: every point maps to exactly one band
                    ok = np.isin(final, (AMBER, GREEN, RED, ANOM))
                    exactly_one += int(ok.sum())
                    total += mus.size
    return {
        "grid_points": total,
        "completeness": exactly_one / total,          # hard gate: must be 1.0
        "raw_predicate_overlaps_v32": overlap_counts["v32"],
        "raw_predicate_overlaps_v31": overlap_counts["v31"],
        "note": ("v3.1 aligned-RED raw predicate overlaps ANOMALOUS by "
                 "construction (x < -t*SE implies x < kappa); the frozen "
                 "ANOMALOUS-before-RED precedence resolves it. v3.2 |mu| "
                 "RED is disjoint from ANOMALOUS (kappa < t*SE at every "
                 "stage), so overlaps must be 0."),
    }


def boundary_selftests():
    """Spec sec 9.4 cutpoint assertions (subset relevant to this OC run)."""
    fl96 = floor_coef(96)
    checks = {}
    # wrong-sign-at-floor must NOT band RED under v3.2 (belt), sigma=+1
    b = band_stage(np.array([-fl96]), np.array([1.0]), +1, 1, "v32")[0]
    checks["wrong_sign_at_floor_not_RED_v32"] = bool(b != RED)
    # ... but v3.1 aligned-RED WOULD have banded it RED were it not ANOMALOUS
    g, a, r = raw_predicates(np.array([-fl96]), np.array([1.0]), +1, 1, "v31")
    checks["wrong_sign_at_floor_raw_red_v31"] = bool(r[0])
    # two-sided RED unreachable at stage 1 (kappa_2s < 0), reachable stage 2
    b1 = band_stage(np.array([0.0]), np.array([1.0]), None, 1, "v32")[0]
    b2 = band_stage(np.array([0.0]), np.array([1.0]), None, 2, "v32")[0]
    checks["two_sided_RED_unreachable_stage1"] = bool(b1 != RED)
    checks["two_sided_RED_reachable_stage2"] = bool(b2 == RED)
    # ANOMALOUS and v3.2 RED never co-fire (kappa < t*SE at every stage)
    ok = True
    for stage in (1, 2, 3):
        mus = np.linspace(-5, 5, 4001)
        sd = np.ones_like(mus)
        g, a, r = raw_predicates(mus, sd, +1, stage, "v32")
        ok &= not bool((a & r).any())
    checks["anom_red_never_cofire_v32"] = ok
    # a cell AMBER at every stage emits INCONCLUSIVE_AT_CEILING: mu_hat at
    # 0.5*floor(96), sd_hat=1 is AMBER at stages 1-3 (one-sided, both rules)
    mu_amber = np.array([0.5 * fl96])
    sd_one = np.array([1.0])
    all_amber = all(band_stage(mu_amber, sd_one, +1, s, r)[0] == AMBER
                    for s in (1, 2, 3) for r in ("v32", "v31"))
    checks["mid_band_cell_is_AMBER_all_stages"] = bool(all_amber)
    return checks


CELLS = ("A", "B", "C", "D", "AxT2", "AxT4")


def joint_masks(finals):
    """finals: list of per-cell final-band arrays (same length)."""
    F = np.stack(finals)
    return {
        "any_green": (F == GREEN).any(axis=0),
        "any_anom": (F == ANOM).any(axis=0),
        "any_inconc": (F == INCONC).any(axis=0),
        "all_red": (F == RED).all(axis=0),
    }


def scenario_S1(rng, n):
    """Global null: all six cells mu_true=0 -> sigma INDETERMINATE (None),
    banded two-sided, STABLE vacuous. Pivot = all six RED."""
    finals = []
    for _ in CELLS:
        f, _s = run_ladder(rng, n, 0.0, 1.0, None, "v32")
        finals.append(f)
    m = joint_masks(finals)
    per_cell_green = float((np.stack(finals) == GREEN).mean())
    out = {
        "trials": n,
        "model": "all null, sigma=None (INDETERMINATE), two-sided banding",
        "per_cell_false_green": per_cell_green,
        "any_cell_false_green": float(m["any_green"].mean()),
        "any_cell_false_green_mc_se": mc_se(float(m["any_green"].mean()), n),
        "pivot_rate": float(m["all_red"].mean()),
        "any_inconclusive_rate": float(m["any_inconc"].mean()),
        "any_anomalous_rate": float(m["any_anom"].mean()),
        "per_cell_band_dist": band_dist(np.stack(finals).ravel()),
    }
    return out


def scenario_S1b(rng, n):
    """Sensitivity: all null but every cell FORCE-registered sigma=+1
    (one-sided) with modeled STABLE (chance, p_reg=0.5). Shows the one-sided
    null operating point incl. the ~0.048/cell terminal false-anomaly."""
    finals = []
    for _ in CELLS:
        f, _s = run_ladder(rng, n, 0.0, 1.0, +1, "v32")
        finals.append(f)
    m = joint_masks(finals)
    pivot = {}
    for rho in RHOS:
        all_st = np.ones(n, dtype=bool)
        for _ in CELLS:
            st, _p = stable_flags(rng, n, 0.0, +1, rho)
            all_st &= st
        pivot[str(rho)] = float((m["all_red"] & all_st).mean())
    return {
        "trials": n,
        "model": "all null, force-registered sigma=+1, STABLE modeled (p=0.5)",
        "per_cell_false_green": float((np.stack(finals) == GREEN).mean()),
        "any_cell_false_green": float(m["any_green"].mean()),
        "per_cell_terminal_false_anomaly":
            float((np.stack(finals) == ANOM).mean()),
        "any_cell_terminal_false_anomaly": float(m["any_anom"].mean()),
        "all_red_rate": float(m["all_red"].mean()),
        "pivot_rate_by_rho": pivot,
        "stable_chance_exact": stable_tail_exact(0.5),
    }


def scenario_S2(rng, n):
    """KEY: wrong-sign-at-floor. Cell A true mu = -floor(96), REGISTERED
    sigma_A = +1 (wrong sign). B..F truly null -> INDETERMINATE two-sided.
    Any pivot here is INVALID. Decomposition (belt = v3.2 RED |mu| bound;
    suspenders = modeled P1-B STABLE):
      (a) full v3.2   : |mu| bound RED + modeled STABLE
      (b) belt only   : |mu| bound RED, STABLE forced True
      (c) suspenders  : v3.1 aligned-RED (no |mu| bound) + modeled STABLE
    Cell A's block sample is SHARED between the v3.2 and v3.1 bandings
    (same data, two rules) and the same modeled STABLE draw serves (a) and
    (c) — variance-reduced, physically coherent (one pilot, one cell)."""
    mu_A = -floor_coef(96)
    blocksA = rng.normal(mu_A, 1.0, size=(n, 32))
    mu1, sd1 = blocksA[:, :16].mean(1), blocksA[:, :16].std(1, ddof=1)
    mu2, sd2 = blocksA.mean(1), blocksA.std(1, ddof=1)
    fA = {}
    for rule in ("v32", "v31"):
        b1 = band_stage(mu1, sd1, +1, 1, rule)
        b2 = band_stage(mu2, sd2, +1, 2, rule)
        b3 = band_stage(mu2, sd2, +1, 3, rule)
        fA[rule] = np.where(b1 != AMBER, b1,
                   np.where(b2 != AMBER, b2,
                   np.where(b3 != AMBER, b3, INCONC)))
    null_finals = []
    for _ in CELLS[1:]:
        f, _s = run_ladder(rng, n, 0.0, 1.0, None, "v32")
        null_finals.append(f)
    nulls_all_red = (np.stack(null_finals) == RED).all(axis=0)
    A_red_v32 = fA["v32"] == RED
    A_red_v31 = fA["v31"] == RED
    decomp = {}
    for rho in RHOS:
        stA, p_reg = stable_flags(rng, n, mu_A, +1, rho)
        inv_full = float((A_red_v32 & stA & nulls_all_red).mean())
        inv_belt = float((A_red_v32 & nulls_all_red).mean())
        inv_susp = float((A_red_v31 & stA & nulls_all_red).mean())
        decomp[str(rho)] = {
            "invalid_pivot_full_v32": inv_full,
            "invalid_pivot_belt_only": inv_belt,
            "invalid_pivot_suspenders_only": inv_susp,
            "mc_se_full": mc_se(inv_full, n),
            "mc_se_belt": mc_se(inv_belt, n),
            "mc_se_susp": mc_se(inv_susp, n),
            "A_red_and_stable_v32": float((A_red_v32 & stA).mean()),
            "A_red_and_stable_v31": float((A_red_v31 & stA).mean()),
            "p_seed_agrees_registered": p_reg,
            "P_stable_exact": stable_tail_exact(p_reg),
        }
    return {
        "trials": n,
        "mu_A_true": mu_A,
        "sigma_A_registered": +1,
        "model": ("wrong-sign at floor; nulls INDETERMINATE two-sided; "
                  "STABLE modeled per module docstring"),
        "A_band_dist_v32": band_dist(fA["v32"]),
        "A_band_dist_v31": band_dist(fA["v31"]),
        "A_red_rate_v32": float(A_red_v32.mean()),
        "A_red_rate_v31": float(A_red_v31.mean()),
        "A_anomalous_rate_v32": float((fA["v32"] == ANOM).mean()),
        "nulls_all_red_rate": float(nulls_all_red.mean()),
        "decomposition_by_rho": decomp,
    }


def scenario_S3(rng, n):
    """One cell ALIGNED at floor: A mu_true=+floor(96), sigma_A=+1 (correct);
    B..F null (INDETERMINATE two-sided). Expectation: A mostly AMBER ->
    extend -> INCONCLUSIVE_AT_CEILING."""
    mu_A = floor_coef(96)
    fA, sA = run_ladder(rng, n, mu_A, 1.0, +1, "v32")
    null_finals = []
    for _ in CELLS[1:]:
        f, _s = run_ladder(rng, n, 0.0, 1.0, None, "v32")
        null_finals.append(f)
    nulls_all_red = (np.stack(null_finals) == RED).all(axis=0)
    pivot = {}
    for rho in RHOS:
        stA, p_reg = stable_flags(rng, n, mu_A, +1, rho)
        pivot[str(rho)] = {
            "pivot_rate": float(((fA == RED) & stA & nulls_all_red).mean()),
            "P_stable_exact": stable_tail_exact(p_reg),
        }
    stage_dist = {f"stage{k}": float((sA == k).mean()) for k in (1, 2, 3)}
    return {
        "trials": n,
        "mu_A_true": mu_A,
        "A_band_dist": band_dist(fA),
        "A_terminal_stage_dist": stage_dist,
        "A_extend_rate_past_stage1": float((sA >= 2).mean()),
        "A_inconclusive_rate": float((fA == INCONC).mean()),
        "pivot_by_rho": pivot,
    }


def scenario_S4(rng, n):
    """GREEN power: cell A aligned at 2x and 3x floor(96), sigma=+1 correct;
    B..F null. Compound (whole-ladder) P(GREEN) — law #3 gate at 3x >= 0.90."""
    out = {"trials": n}
    for mult in (2, 3):
        mu_A = mult * floor_coef(96)
        fA, sA = run_ladder(rng, n, mu_A, 1.0, +1, "v32")
        null_finals = []
        for _ in CELLS[1:]:
            f, _s = run_ladder(rng, n, 0.0, 1.0, None, "v32")
            null_finals.append(f)
        any_green_all = ((np.stack(null_finals) == GREEN).any(axis=0)
                         | (fA == GREEN))
        p_green = float((fA == GREEN).mean())
        out[f"{mult}x"] = {
            "mu_A_true": mu_A,
            "green_power_cell_A": p_green,
            "green_power_mc_se": mc_se(p_green, n),
            "green_by_stage": {
                f"stage{k}": float(((fA == GREEN) & (sA == k)).mean())
                for k in (1, 2, 3)},
            "A_band_dist": band_dist(fA),
            "register_rate_any_green": float(any_green_all.mean()),
            "law2_planted_signal_breaks_pivot":
                float((fA != RED).mean()),   # law #2: gate must be failable
        }
    return out


def scenario_S5(rng, n):
    """Tc-heteroscedastic global null: per-cell sd_true follows the
    receipt-06 quadratic Tc scaling reaching x1.62 at Tc4 --
    sd_true(k) = 1 + 0.62*(k/4)^2 for cell index k = 0..5 (so cell index 4
    sits exactly at x1.62). All mu_true = 0 (INDETERMINATE two-sided).
    Banding is scale-equivariant in sd_cell, so no false GREEN excess."""
    sds = [1.0 + 0.62 * (k / 4.0) ** 2 for k in range(6)]
    finals = []
    for sd in sds:
        f, _s = run_ladder(rng, n, 0.0, sd, None, "v32")
        finals.append(f)
    m = joint_masks(finals)
    return {
        "trials": n,
        "sd_true_per_cell": sds,
        "per_cell_false_green": float((np.stack(finals) == GREEN).mean()),
        "any_cell_false_green": float(m["any_green"].mean()),
        "any_cell_false_green_mc_se": mc_se(float(m["any_green"].mean()), n),
        "pivot_rate": float(m["all_red"].mean()),
        "any_inconclusive_rate": float(m["any_inconc"].mean()),
    }


def main():
    rng = np.random.default_rng(RNG_SEED)
    results = {
        "artifact": "oc_simulation_v32.py",
        "rule": "v4.4 scout decision-rule v3.2 (frozen)",
        "interpreter": "/usr/bin/python3",
        "numpy_version": np.__version__,
        "rng_seed": RNG_SEED,
        "P1_modeled": True,
        "stable_model": {
            "form": "p_true = 0.5 + 0.5*rho*tanh(|mu_true|/noise_scale); "
                    "agree-with-registered = p_true (right sign), 1-p_true "
                    "(wrong sign), 0.5 (null); STABLE iff >=12/16",
            "noise_scale": NOISE_SCALE,
            "rhos": list(RHOS),
            "tanh_at_floor": math.tanh(floor_coef(96) / NOISE_SCALE),
        },
        "constants_check": {
            "floor_96": floor_coef(96), "floor_128": floor_coef(128),
            "SE_16": se_coef(16), "SE_32": se_coef(32),
        },
    }
    print("== partition scan ==", flush=True)
    results["partition"] = partition_scan()
    print(json.dumps(results["partition"], indent=1))
    print("== boundary selftests ==", flush=True)
    results["boundary_selftests"] = boundary_selftests()
    print(json.dumps(results["boundary_selftests"], indent=1))
    assert all(results["boundary_selftests"].values()), "selftest failure"
    assert results["partition"]["completeness"] == 1.0, "partition failure"
    assert results["partition"]["raw_predicate_overlaps_v32"] == 0

    print("== S1 global null ==", flush=True)
    results["S1"] = scenario_S1(rng, N_TAIL)
    print(json.dumps(results["S1"], indent=1))
    print("== S1b one-sided null sensitivity ==", flush=True)
    results["S1b"] = scenario_S1b(rng, N_MAIN)
    print(json.dumps(results["S1b"], indent=1))
    print("== S2 wrong-sign at floor (KEY) ==", flush=True)
    results["S2"] = scenario_S2(rng, N_TAIL)
    print(json.dumps(results["S2"], indent=1))
    print("== S3 aligned at floor ==", flush=True)
    results["S3"] = scenario_S3(rng, N_MAIN)
    print(json.dumps(results["S3"], indent=1))
    print("== S4 GREEN power ==", flush=True)
    results["S4"] = scenario_S4(rng, N_MAIN)
    print(json.dumps(results["S4"], indent=1))
    print("== S5 Tc-heteroscedastic null ==", flush=True)
    results["S5"] = scenario_S5(rng, N_MAIN)
    print(json.dumps(results["S5"], indent=1))

    worst_invalid_full = max(
        results["S2"]["decomposition_by_rho"][str(r)]["invalid_pivot_full_v32"]
        for r in RHOS)
    false_green = max(results["S1"]["any_cell_false_green"],
                      results["S1b"]["any_cell_false_green"],
                      results["S5"]["any_cell_false_green"])
    gates = {
        "false_green_null_le_0.01": {
            "value": false_green, "threshold": 0.01,
            "pass": false_green <= 0.01},
        "invalid_pivot_wrong_sign_at_floor_le_0.02_v32_full": {
            "value": worst_invalid_full, "threshold": 0.02,
            "pass": worst_invalid_full <= 0.02},
        "green_power_3x_ge_0.90": {
            "value": results["S4"]["3x"]["green_power_cell_A"],
            "threshold": 0.90,
            "pass": results["S4"]["3x"]["green_power_cell_A"] >= 0.90},
        "partition_completeness_eq_1.0": {
            "value": results["partition"]["completeness"], "threshold": 1.0,
            "pass": results["partition"]["completeness"] == 1.0},
    }
    results["hard_gates"] = gates
    results["verdict"] = ("clean" if all(g["pass"] for g in gates.values())
                          else "flags-found")
    print("== hard gates ==")
    print(json.dumps(gates, indent=1))
    print("VERDICT:", results["verdict"])

    out_path = ("/Users/tony_studio/Projects/entropy-as-tunable-equilibrium/"
                "v4/v44/oc_results_v32.json")
    with open(out_path, "w") as fh:
        json.dump(results, fh, indent=2)
    print("wrote", out_path)


if __name__ == "__main__":
    main()
