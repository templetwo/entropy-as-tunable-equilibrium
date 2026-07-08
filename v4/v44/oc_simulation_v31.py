#!/usr/bin/env python3
"""
oc_simulation_v31.py  --  Full-loop OPERATING-CHARACTERISTIC simulation of the
v4.4 scout decision rule as frozen in v44_scout_DECISION_RULE_v3.1.md.

This is the instrument ChatGPT's Q4 required: it simulates the ENTIRE frozen
state machine (band_cell -> 16->32 block extension -> B96->B128 escalation ->
INCONCLUSIVE_AT_CEILING terminal -> anomaly generation/blocking -> pivot_licensed
with the GREEN tie-break) over all six cells JOINTLY, so it catches the
category errors that per-contrast analytic power and the local §3.3 Monte Carlo
cannot see (the multi-look ladder, the ceiling-minted-null error, vacuous-truth).

Interpreter: /usr/bin/python3  (Python 3.9.6, numpy 2.0.2).  scipy used ONLY in
the selftest to cross-check the frozen t / chi2 constants; the simulation itself
runs on the hardcoded frozen constants (grep-consistency, experimental law #4).

NOT registered, NOT chronicled, edits NO harness bytes.  Pure analysis of the
draft v3.1 rule.  Prints a machine-readable JSON block at the end for the report.
"""

import numpy as np
import json
import sys

# ----------------------------------------------------------------------------
# FROZEN CONSTANTS (grep-consistent with v3.1 §0.1, §2.2, §2.3, §3.3)
# ----------------------------------------------------------------------------
Z = 3.858  # z_{0.995} + z_{0.90}, the two-arm MDE constant (§0.1)

# floor_c(sd) = Z * sd * sqrt(2 / B_conf)      (§0.1)
FLOOR_FACTOR = {96: np.sqrt(2.0 / 96), 128: np.sqrt(2.0 / 128)}   # 0.14434, 0.12500

# SE(sd) = sd * sqrt(1/n + 1/64)               (estimand (a), §2.1)
SE_FACTOR = {8:  np.sqrt(1.0/8  + 1.0/64),
             16: np.sqrt(1.0/16 + 1.0/64),
             32: np.sqrt(1.0/32 + 1.0/64)}     # 0.39528, 0.27951, 0.21651

# Student-t, alpha=0.05  (§2.2 table, frozen)
T_ONESIDED = {8: 1.895, 16: 1.753, 32: 1.696}   # df = n-1 = 7,15,31 ; t_{0.95}
T_TWOSIDED = {8: 2.365, 16: 2.131, 32: 2.040}   # t_{0.975}

# sd_upper = sd_hat * sqrt((n-1)/chi2_{0.05,n-1})   (§3.3, frozen factors)
CHI2_UPPER = {8: 1.797, 16: 1.437, 32: 1.268}

# Band codes
GREEN, AMBER, RED, ANOMALOUS, INCONCLUSIVE = 0, 1, 2, 3, 4
BAND_NAME = {GREEN: "GREEN", AMBER: "AMBER", RED: "RED",
             ANOMALOUS: "ANOMALOUS", INCONCLUSIVE: "INCONCLUSIVE_AT_CEILING"}

# receipt-06 null block-SD calibration (quad_loop_rate), used only where the
# absolute SD matters (Tc-heteroscedastic S6, equal-arm-offset S7).  Band
# arithmetic is scale-free in sd_cell so S1-S5 run in sd_cell=1 units.
SD_QUAD = {"Tc1": 5.03e-5, "Tc2": 6.29e-5, "Tc4": 8.15e-5}   # x1.00, x1.25, x1.62
TC_SCALE = {"A": 1.0, "B": 1.0, "C": 1.0, "D": 1.0,
            "AxT2": SD_QUAD["Tc2"]/SD_QUAD["Tc1"],   # 1.2505
            "AxT4": SD_QUAD["Tc4"]/SD_QUAD["Tc1"]}   # 1.6203
CELLS = ["A", "B", "C", "D", "AxT2", "AxT4"]

FLOOR96 = Z * FLOOR_FACTOR[96]   # 0.5569 (in sd_cell units)


# ----------------------------------------------------------------------------
# VECTORIZED band_cell  (§3, §7 pseudocode) -- operates on arrays of shape (...,)
# ----------------------------------------------------------------------------
def band_cell_vec(mu, sd, n_blocks, B_conf, sigma, two_sided):
    """
    mu, sd, sigma(+1/-1/0), two_sided(bool) : arrays broadcast to common shape.
    Returns (band_code_array, green_margin_array).
    Priority exactly as §7: GREEN -> ANOMALOUS -> RED -> AMBER.
    green_margin = x - t*SE - floor_c  (the '-x - t*SE above floor_c' tie-break
    quantity of §5, well-defined for every cell, only used where band==GREEN).
    INCONCLUSIVE_AT_CEILING is NOT emitted here -- the caller's ladder sets it.
    """
    t = np.where(two_sided, T_TWOSIDED[n_blocks], T_ONESIDED[n_blocks])
    se = sd * SE_FACTOR[n_blocks]
    floor_c = Z * sd * FLOOR_FACTOR[B_conf]
    sd_up = sd * CHI2_UPPER[n_blocks]
    se_up = sd_up * SE_FACTOR[n_blocks]
    floor_up = Z * sd_up * FLOOR_FACTOR[B_conf]

    # signed, prediction-aligned statistic
    x = np.where(two_sided, np.abs(mu), sigma * mu)

    green = (x - t * se) > floor_c
    anomalous = (~two_sided) & (x < -(t * se))          # significant wrong-sign vs 0 (§3, Finding-4)
    red_point = (x + t * se) < floor_c
    red_upper = (x + t * se_up) < floor_up               # coupled-upper conjunction (§3.3)
    red = red_point & red_upper

    band = np.full(x.shape, AMBER, dtype=np.int8)
    band = np.where(red, RED, band)
    band = np.where(anomalous, ANOMALOUS, band)          # anomalous over red (order per §7)
    band = np.where(green, GREEN, band)                  # green highest priority
    margin = (x - t * se) - floor_c
    return band, margin


# ----------------------------------------------------------------------------
# VECTORIZED terminal ladder (§4)  -- accumulation dependence PRESERVED
# ----------------------------------------------------------------------------
def resolve_ladder(draws, sigma, two_sided):
    """
    draws : (n_trials, n_cells, 32) block statistics (already in sd_cell units,
            i.e. divide out true SD before calling if heteroscedastic).
    sigma : (n_cells,) in {+1,-1,0};  two_sided : (n_cells,) bool.
    Returns (final_band (n_trials,n_cells) int8, green_margin (n_trials,n_cells)).

    16-block first pass uses draws[...,:16]; the 32-block extension REUSES those
    16 and appends the next 16 (draws[...,:32]) -- NOT a fresh independent redraw
    (§4 step 1, §9.1 'accumulation dependence preserved -- load-bearing').
    """
    nt, nc, _ = draws.shape
    sig = sigma[None, :]
    ts = two_sided[None, :]

    mu16 = draws[:, :, :16].mean(axis=2)
    sd16 = draws[:, :, :16].std(axis=2, ddof=1)
    mu32 = draws[:, :, :32].mean(axis=2)
    sd32 = draws[:, :, :32].std(axis=2, ddof=1)

    b16, m16 = band_cell_vec(mu16, sd16, 16, 96, sig, ts)
    b32_96, m32_96 = band_cell_vec(mu32, sd32, 32, 96, sig, ts)
    b32_128, m32_128 = band_cell_vec(mu32, sd32, 32, 128, sig, ts)

    final = b16.copy()
    margin = m16.copy()

    amber1 = (b16 == AMBER)                        # extend 16 -> 32 @ B96
    final = np.where(amber1, b32_96, final)
    margin = np.where(amber1, m32_96, margin)

    amber2 = amber1 & (b32_96 == AMBER)            # escalate B96 -> B128
    final = np.where(amber2, b32_128, final)
    margin = np.where(amber2, m32_128, margin)

    amber3 = amber2 & (b32_128 == AMBER)           # terminal ceiling
    final = np.where(amber3, INCONCLUSIVE, final)
    return final.astype(np.int8), margin


# ----------------------------------------------------------------------------
# VECTORIZED pivot_licensed (§5, §7)
# ----------------------------------------------------------------------------
def pivot_licensed_vec(final, stable):
    """
    final : (n_trials, n_cells);  stable : (n_cells,) bool.
    Pivot to closed no-reset NESS (RAW-CURRENT claim) iff ALL §5 conditions hold:
      (0)  no ANOMALOUS cell
      (0') no INCONCLUSIVE_AT_CEILING cell
      (i)  >=1 cell banded AND every cell is actual RED (non-vacuous)
      (ii) every counted-RED cell is STABLE
    Returns (pivot bool (n_trials,)).
    """
    st = stable[None, :]
    any_anom = (final == ANOMALOUS).any(axis=1)
    any_incon = (final == INCONCLUSIVE).any(axis=1)
    any_green = (final == GREEN).any(axis=1)
    all_red = (final == RED).all(axis=1)           # non-vacuous: 6 real cells always present
    # (ii) every RED cell stable  <=>  no (RED & unstable) cell
    red_unstable = ((final == RED) & (~st)).any(axis=1)
    non_vacuous = final.shape[1] > 0                # >=1 cell banded (§5 cond i)
    pivot = (all_red & non_vacuous & (~any_anom) & (~any_incon)
             & (~any_green) & (~red_unstable))
    return pivot


# ----------------------------------------------------------------------------
# Trial engine -- chunked over trials to bound memory at large N
# ----------------------------------------------------------------------------
def run_scenario(delta, sigma, two_sided, stable, sd_scale, n_trials, seed,
                 chunk=200_000):
    """
    delta   : (n_cells,) true mean of each block statistic in sd_cell units
              (i.e. contrast / true-SD).  For an offset injection, add it here.
    sigma   : (n_cells,) predicted sign {+1,-1,0}
    two_sided,stable : (n_cells,) bool
    sd_scale: (n_cells,) TRUE block SD multiplier (heteroscedastic test).  Draws
              are N(delta*scale, scale); we divide by scale so the analysis sees
              N(delta,1) estimated sd_cell -- exactly what the scale-free banding does.
    Returns dict of accumulated counts + arrays needed by the callers.
    """
    rng = np.random.default_rng(seed)
    nc = len(sigma)
    # accumulators
    band_counts = np.zeros((nc, 5), dtype=np.int64)      # per-cell terminal band histogram
    n_pivot = 0
    n_any_green = 0
    n_any_anom = 0
    n_any_incon = 0
    n_all_red = 0
    n_limbo = 0
    n_blocked_unstable = 0
    # per-cell green indicator (for green-power on a specific signal cell)
    cell_green = np.zeros(nc, dtype=np.int64)
    cell_anom = np.zeros(nc, dtype=np.int64)
    cell_red = np.zeros(nc, dtype=np.int64)
    cell_incon = np.zeros(nc, dtype=np.int64)
    # tie-break bookkeeping: among trials with >=2 GREEN, was argmax-margin the
    # true-highest-delta cell?
    n_multi_green = 0
    n_tiebreak_correct = 0
    true_best = int(np.argmax(delta)) if np.any(delta > 0) else -1

    done = 0
    while done < n_trials:
        m = min(chunk, n_trials - done)
        # draws in TRUE units then normalized to sd_cell=1 view
        raw = rng.standard_normal((m, nc, 32))
        draws = (delta[None, :, None] + raw) * sd_scale[None, :, None]
        draws = draws / sd_scale[None, :, None]          # analysis sees estimated sd_cell
        final, margin = resolve_ladder(draws, sigma, two_sided)

        for c in range(nc):
            counts = np.bincount(final[:, c], minlength=5)
            band_counts[c] += counts
        cell_green += (final == GREEN).sum(axis=0)
        cell_anom += (final == ANOMALOUS).sum(axis=0)
        cell_red += (final == RED).sum(axis=0)
        cell_incon += (final == INCONCLUSIVE).sum(axis=0)

        pivot = pivot_licensed_vec(final, stable)
        any_green = (final == GREEN).any(axis=1)
        any_anom = (final == ANOMALOUS).any(axis=1)
        any_incon = (final == INCONCLUSIVE).any(axis=1)
        all_red = (final == RED).all(axis=1)

        n_pivot += int(pivot.sum())
        n_any_green += int(any_green.sum())
        n_any_anom += int(any_anom.sum())
        n_any_incon += int(any_incon.sum())
        n_all_red += int(all_red.sum())
        n_blocked_unstable += int((all_red & (~pivot)).sum())

        # deadlock / limbo detection: a trial that is none of {pivot, green,
        # anomalous, inconclusive, all-red}.  Must be identically zero.
        classified = pivot | any_green | any_anom | any_incon | all_red
        n_limbo += int((~classified).sum())

        # tie-break: trials with >=2 GREEN
        if true_best >= 0:
            ng = (final == GREEN).sum(axis=1)
            multi = ng >= 2
            if multi.any():
                n_multi_green += int(multi.sum())
                # argmax margin restricted to GREEN cells
                mg = np.where(final == GREEN, margin, -np.inf)
                picked = np.argmax(mg, axis=1)
                n_tiebreak_correct += int((multi & (picked == true_best)).sum())

        done += m

    return dict(
        n_trials=n_trials, band_counts=band_counts,
        n_pivot=n_pivot, n_any_green=n_any_green, n_any_anom=n_any_anom,
        n_any_incon=n_any_incon, n_all_red=n_all_red,
        n_blocked_unstable=n_blocked_unstable, n_limbo=n_limbo,
        cell_green=cell_green, cell_anom=cell_anom, cell_red=cell_red,
        cell_incon=cell_incon, n_multi_green=n_multi_green,
        n_tiebreak_correct=n_tiebreak_correct, true_best=true_best,
    )


def mcse(p, n):
    return float(np.sqrt(max(p, 1e-12) * (1 - p) / n))


# ----------------------------------------------------------------------------
# §9.4 DETERMINISTIC BOUNDARY / CUTPOINT SELFTESTS
# ----------------------------------------------------------------------------
def selftest():
    from scipy import stats
    fails = []

    def approx(a, b, tol, msg):
        if abs(a - b) > tol:
            fails.append(f"{msg}: {a} vs {b} (tol {tol})")

    # frozen constants cross-checked against scipy
    for n in (8, 16, 32):
        df = n - 1
        approx(T_ONESIDED[n], stats.t.ppf(0.95, df), 5e-3, f"t_onesided n={n}")
        approx(T_TWOSIDED[n], stats.t.ppf(0.975, df), 5e-3, f"t_twosided n={n}")
        chi = np.sqrt(df / stats.chi2.ppf(0.05, df))
        approx(CHI2_UPPER[n], chi, 5e-3, f"chi2_upper n={n}")
        if CHI2_UPPER[n] <= 1.0:
            fails.append(f"chi2_upper n={n} not >1 ({CHI2_UPPER[n]})")
    approx(FLOOR96, 0.557, 2e-3, "floor96")
    approx(Z * FLOOR_FACTOR[128], 0.482, 2e-3, "floor128")
    approx(SE_FACTOR[16], 0.2795, 2e-3, "SE16")
    approx(SE_FACTOR[32], 0.21651, 2e-3, "SE32")

    def band1(mu, n=16, B=96, sigma=1, two_sided=False):
        b, _ = band_cell_vec(np.array([mu*1.0]), np.array([1.0]), n, B,
                             np.array([sigma]), np.array([two_sided]))
        return int(b[0])

    # operative 16/96 one-sided cutpoints (sd_cell=1), computed EXACTLY from the
    # frozen factors so the eps-straddle is exact (spec rounds to 1.047/0.067/-0.490):
    se16 = SE_FACTOR[16]; t16 = T_ONESIDED[16]
    green_cut = FLOOR96 + t16 * se16      # ~1.0469
    red_cut = FLOOR96 - t16 * se16        # ~0.06697
    anom_edge = -t16 * se16               # ~-0.48997
    eps = 1e-5
    if band1(green_cut + eps) != GREEN: fails.append("GREEN just above green_cut")
    if band1(green_cut - eps) != AMBER: fails.append("AMBER just below green_cut")
    if band1(red_cut - eps) != RED:     fails.append("RED just below red_cut")
    if band1(red_cut + eps) != AMBER:   fails.append("AMBER just above red_cut")
    if band1(anom_edge - eps) != ANOMALOUS: fails.append("ANOMALOUS just past anom_edge")
    if band1(anom_edge + eps) != RED:   fails.append("RED just inside anom_edge")

    # two-sided (INDETERMINATE) branch: no ANOMALOUS; large |mu| -> GREEN both signs
    if band1(-0.490 - eps, sigma=0, two_sided=True) == ANOMALOUS:
        fails.append("two-sided produced ANOMALOUS")
    #   two-sided GREEN cut 16/96 = floor + t_ts*SE = 0.5569 + 2.131*0.27951 = 1.1526
    if band1(1.1526 + 1e-3, sigma=0, two_sided=True) != GREEN:
        fails.append("two-sided GREEN just above 1.153")
    if band1(-(1.1526 + 1e-3), sigma=0, two_sided=True) != GREEN:
        fails.append("two-sided GREEN negative side (|mu|)")

    # RED conjunction picks the HARDER ceiling at kappa>0 (16/96) and kappa<0 (8/96).
    # 16/96: kappa=+0.067>0 -> point governs (=conjunction).  A value between the
    # point ceiling (0.067) and coupled-upper ceiling should be AMBER not RED.
    #   coupled-upper ceiling = sd_up*(floor - t*SE)/sd = 1.437*0.067 = 0.0963
    if band1(0.08) != AMBER:
        fails.append("16/96 conjunction must bind on point (0.08 -> AMBER)")
    # 8/96: kappa<0, RED unreachable at any x>=... ; a modest positive should not be RED
    if band1(0.05, n=8) == RED:
        fails.append("8/96 RED must be unreachable (kappa<0)")

    # pivot_licensed guards (§9.4): empty / all-anomalous / all-inconclusive -> False;
    # terminal-ceiling AMBER never RED; UNSTABLE-RED blocks pivot.
    def piv(bands, stable):
        return bool(pivot_licensed_vec(np.array([bands]), np.array(stable))[0])
    if piv([RED]*6, [True]*6) is not True: fails.append("all-RED-stable should pivot")
    if piv([ANOMALOUS]*6, [True]*6):       fails.append("all-ANOMALOUS must NOT pivot")
    if piv([INCONCLUSIVE]*6, [True]*6):    fails.append("all-INCONCLUSIVE must NOT pivot")
    if piv([RED]*5 + [INCONCLUSIVE], [True]*6): fails.append("one INCONCLUSIVE must block pivot")
    if piv([RED]*5 + [ANOMALOUS], [True]*6):    fails.append("one ANOMALOUS must block pivot")
    if piv([RED]*5 + [GREEN], [True]*6):        fails.append("a GREEN must block pivot (register)")
    # UNSTABLE RED blocks the pivot (§5 condition ii) -- the two-sided path scenarios
    # never exercise this, so it is asserted here explicitly.
    if piv([RED]*6, [True]*5 + [False]):   fails.append("UNSTABLE RED must block pivot")
    # empty pivot guard
    if bool(pivot_licensed_vec(np.zeros((1,0),dtype=np.int8), np.array([],dtype=bool))[0]):
        fails.append("empty pivot must be False")

    # Terminal-ceiling behavior: a cell held AMBER through the whole ladder emits
    # INCONCLUSIVE_AT_CEILING, never RED.  A genuinely-underpowered cell has mu and
    # sd BOTH O(1) with x/sd parked inside the AMBER band at every stage.  Build 16
    # deterministic blocks with sample mean 0.45 (mid-AMBER) and sample sd 1, tiled
    # to 32 (so first-16 and full-32 both mean 0.45, sd ~1 -> AMBER -> INCONCLUSIVE).
    z16 = np.arange(16, dtype=float); z16 = (z16 - z16.mean()) / z16.std(ddof=1)
    blk = 0.45 + z16
    d = np.concatenate([blk, blk])[None, None, :]      # (1,1,32)
    fb, _ = resolve_ladder(d, np.array([1]), np.array([False]))
    if fb[0, 0] != INCONCLUSIVE:
        fails.append(f"parked-at-floor cell must terminate INCONCLUSIVE, got {BAND_NAME[int(fb[0,0])]}")
    # and it must never be RED at the ceiling
    if fb[0, 0] == RED:
        fails.append("terminal-ceiling cell emitted RED (Q4 regression)")

    return fails


# ----------------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------------
def main():
    SEED = 20260707
    out = {"seed": SEED, "interpreter": sys.version.split()[0],
           "numpy": np.__version__}

    # ---- selftests first (law #2 / §9.4) ----
    st_fails = selftest()
    out["selftest_failures"] = st_fails
    print("SELFTEST:", "PASS" if not st_fails else f"FAIL {st_fails}")
    if st_fails:
        print(json.dumps(out, indent=2))
        sys.exit(1)

    nc = len(CELLS)
    ones = np.ones(nc)
    sig_pos = np.ones(nc, dtype=int)          # all cells predicted sign +1
    ts_false = np.zeros(nc, dtype=bool)        # all one-sided
    stable_all = np.ones(nc, dtype=bool)       # all STABLE
    noscale = np.ones(nc)

    N_MAIN = 200_000
    N_TAIL = 1_000_000     # false-GREEN + invalid-pivot tail estimates (§9.1)

    scen = {}

    # ---- S1 global null (tail N for false-GREEN) ----
    print("Running S1 global null ...")
    s1 = run_scenario(np.zeros(nc), sig_pos, ts_false, stable_all, noscale,
                      N_TAIL, SEED)
    scen["S1"] = s1

    # ---- S2 one-cell at floor (tail N for invalid-pivot) ----
    print("Running S2 one-cell at-floor ...")
    d2 = np.zeros(nc); d2[0] = FLOOR96
    s2 = run_scenario(d2, sig_pos, ts_false, stable_all, noscale, N_TAIL, SEED + 2)
    scen["S2"] = s2

    # ---- S3 one-cell supra-floor sweep 1x/2x/3x ----
    for k in (1, 2, 3):
        print(f"Running S3 supra-floor {k}x ...")
        d = np.zeros(nc); d[0] = k * FLOOR96
        NN = N_TAIL if k in (2, 3) else N_MAIN     # tail N where invalid-pivot must be ~0
        scen[f"S3_{k}x"] = run_scenario(d, sig_pos, ts_false, stable_all, noscale,
                                        NN, SEED + 10 + k)

    # ---- S4 multi-signal tie-break (spec spacing 2x/2.5x/3x) + separated sub-case ----
    print("Running S4 tie-break (2x/2.5x/3x) ...")
    d4 = np.zeros(nc); d4[0] = 3.0*FLOOR96; d4[1] = 2.5*FLOOR96; d4[2] = 2.0*FLOOR96
    scen["S4"] = run_scenario(d4, sig_pos, ts_false, stable_all, noscale, N_MAIN, SEED + 40)
    print("Running S4b tie-break separated (2x/3x/5x) ...")
    d4b = np.zeros(nc); d4b[0] = 5.0*FLOOR96; d4b[1] = 3.0*FLOOR96; d4b[2] = 2.0*FLOOR96
    scen["S4b"] = run_scenario(d4b, sig_pos, ts_false, stable_all, noscale, N_MAIN, SEED + 41)

    # ---- S5 wrong-sign artifact (cell 0 at -1x floor, exactly as spec'd) ----
    # NB: Delta = -1x floor = -0.557 sd is only a 2.2 sigma excursion (mu_hat SD=sd/4).
    # The spec's acceptance row assumes "3.6 sigma trips reliably", which corresponds
    # to mu_hat ~ -1.0 sd = -1.79x floor (Finding-4's example), NOT Delta=-1x floor.
    print("Running S5 wrong-sign artifact (Delta=-1x floor, as spec'd) ...")
    d5 = np.zeros(nc); d5[0] = -1.0 * FLOOR96
    scen["S5"] = run_scenario(d5, sig_pos, ts_false, stable_all, noscale, N_MAIN, SEED + 50)
    # ---- S5-strong: the true 3.6 sigma Finding-4 artifact (mu_hat ~ -1.0 sd) ----
    print("Running S5-strong wrong-sign artifact (Delta=-1.0 sd = -1.79x floor) ...")
    d5s = np.zeros(nc); d5s[0] = -1.0            # -1.0 sd_cell (the Finding-4 magnitude)
    scen["S5_strong"] = run_scenario(d5s, sig_pos, ts_false, stable_all, noscale,
                                     N_MAIN, SEED + 55)

    # ---- S6 Tc-heteroscedastic (null, Tc cells scaled per receipt-06) ----
    print("Running S6 Tc-heteroscedastic ...")
    scale6 = np.array([TC_SCALE[c] for c in CELLS])
    scen["S6"] = run_scenario(np.zeros(nc), sig_pos, ts_false, stable_all, scale6,
                              N_MAIN, SEED + 60)

    # ---- S7 nonzero equal-arm offset (all cells get offset, else null) ----
    for off in (0.10, 0.30):
        print(f"Running S7 equal-arm offset {off}x floor ...")
        d7 = np.full(nc, off * FLOOR96)
        scen[f"S7_{off}"] = run_scenario(d7, sig_pos, ts_false, stable_all, noscale,
                                         N_MAIN, SEED + 70 + int(off*100))

    # ---- Q4-fix demonstration: v3 (count ceiling as RED) vs v3.1 (INCONCLUSIVE) ----
    # Reconstruct, under S1 null, what the pivot rate WOULD be if terminal-AMBER
    # were relabelled RED (the invalid v3 RED_AT_CEILING conversion).
    bc = s1["band_counts"]  # (nc,5)
    per_cell_red = bc[:, RED] / s1["n_trials"]
    per_cell_incon = bc[:, INCONCLUSIVE] / s1["n_trials"]
    per_cell_anom = bc[:, ANOMALOUS] / s1["n_trials"]
    per_cell_green = bc[:, GREEN] / s1["n_trials"]
    # v3.1 pivot rate measured directly; v3 (mislabel) pivot rate = prod over cells
    # of P(cell terminal in {RED or INCONCLUSIVE}) since ceiling would count as RED.
    p_red_or_ceiling = (bc[:, RED] + bc[:, INCONCLUSIVE]) / s1["n_trials"]
    v3_pivot_rate = float(np.prod(p_red_or_ceiling))
    v31_pivot_rate = s1["n_pivot"] / s1["n_trials"]
    out["q4_demo"] = {
        "per_cell_RED": per_cell_red.tolist(),
        "per_cell_INCONCLUSIVE": per_cell_incon.tolist(),
        "per_cell_ANOMALOUS": per_cell_anom.tolist(),
        "per_cell_GREEN": per_cell_green.tolist(),
        "v3_mislabel_pivot_rate_null": v3_pivot_rate,   # ~0.975 (RED_AT_CEILING counted)
        "v31_pivot_rate_null": v31_pivot_rate,          # ~0.38 (INCONCLUSIVE blocks)
    }

    # ---- Q4-fix, protection of a REAL underpowered effect ----
    # A cell carrying a genuine at-floor effect (delta = 1x floor) must, when it
    # fails to resolve, land INCONCLUSIVE (protected) -- NEVER terminal RED that
    # would let it be pivoted away.  Measure that cell's terminal distribution.
    s3_1 = scen["S3_1x"]
    up_bc = s3_1["band_counts"][0]
    out["q4_underpowered_cell"] = {
        "delta": "1x floor (genuine at-floor effect)",
        "P_terminal_RED": float(up_bc[RED] / s3_1["n_trials"]),
        "P_terminal_INCONCLUSIVE": float(up_bc[INCONCLUSIVE] / s3_1["n_trials"]),
        "P_terminal_GREEN": float(up_bc[GREEN] / s3_1["n_trials"]),
        "P_terminal_AMBER_should_be_0": float(up_bc[AMBER] / s3_1["n_trials"]),
        "invalid_pivot_rate": float(s3_1["n_pivot"] / s3_1["n_trials"]),
    }

    # ----------------------------------------------------------------------
    # ASSEMBLE CRITERIA (hard gates from RAW indicators, per advisor item 2)
    # ----------------------------------------------------------------------
    def rate(d, key):
        return d[key] / d["n_trials"]

    crit = []

    # 1. P(any false GREEN) | S1  <= 0.01
    p = rate(s1, "n_any_green"); crit.append(("P(any false GREEN) | S1 global null",
        p, mcse(p, s1["n_trials"]), 0.01, "<=", p <= 0.01))

    # 2. P(invalid pivot) at floor | S2  <= 0.02
    p = rate(s2, "n_pivot"); crit.append(("P(invalid pivot) | S2 one-cell at-floor",
        p, mcse(p, s2["n_trials"]), 0.02, "<=", p <= 0.02))

    # 3. P(invalid pivot) supra-floor | S3 (2x AND 3x)  <= 0.005
    for k in (2, 3):
        d = scen[f"S3_{k}x"]; p = rate(d, "n_pivot")
        crit.append((f"P(invalid pivot) | S3 {k}x floor", p, mcse(p, d["n_trials"]),
                     0.005, "<=", p <= 0.005))

    # 4. P(registrable GREEN)=P(>=1 GREEN) compound power | S3 3x  >= 0.90
    d = scen["S3_3x"]; p = rate(d, "n_any_green")
    crit.append(("P(registrable GREEN) compound | S3 3x floor", p, mcse(p, d["n_trials"]),
                 0.90, ">=", p >= 0.90))

    # 5. P(ANOMALOUS flagged on artifact cell + pivot blocked) | S5  >= 0.90
    d = scen["S5"]
    p_flag = d["cell_anom"][0] / d["n_trials"]
    p_pivot = d["n_pivot"] / d["n_trials"]     # must be 0
    crit.append(("P(wrong-sign cell ANOMALOUS) | S5", float(p_flag), mcse(p_flag, d["n_trials"]),
                 0.90, ">=", p_flag >= 0.90))
    crit.append(("P(pivot fired) | S5 wrong-sign (must be 0)", float(p_pivot),
                 mcse(p_pivot, d["n_trials"]), 0.0, "==0", p_pivot == 0.0))

    # 6. Partition completeness (no un-banded limbo) | all scenarios  == 1.00
    total_limbo = sum(scen[k]["n_limbo"] for k in scen)
    total_amber = sum(int(scen[k]["band_counts"][:, AMBER].sum()) for k in scen)
    crit.append(("Partition completeness: zero limbo trials | S1-S7", float(total_limbo),
                 0.0, 0.0, "==0", total_limbo == 0))
    crit.append(("Zero cells terminate AMBER (deadlock state) | S1-S7", float(total_amber),
                 0.0, 0.0, "==0", total_amber == 0))

    # 7. law #2 -- planted signal breaks all-RED pivot: at 3x floor the signal cell
    #    is non-RED (so pivot cannot include it) in >=0.90 of trials.
    d = scen["S3_3x"]
    p_nonred = 1.0 - d["cell_red"][0] / d["n_trials"]
    crit.append(("law#2: planted 3x signal cell is non-RED (breaks pivot)", float(p_nonred),
                 mcse(p_nonred, d["n_trials"]), 0.90, ">=", p_nonred >= 0.90))

    out["hard_criteria"] = [
        dict(name=n, measured=m, mcse=e, tolerance=f"{op} {tol}", pass_=bool(ok))
        for (n, m, e, tol, op, ok) in crit
    ]

    # ---- advisory / reported operating characteristics ----
    adv = {}
    adv["P(correct pivot) | S1 null (advisory >=0.30)"] = rate(s1, "n_pivot")
    adv["P(>=1 INCONCLUSIVE_AT_CEILING) | S1"] = rate(s1, "n_any_incon")
    adv["P(>=1 false anomaly) | S1 (soft <=0.20)"] = rate(s1, "n_any_anom")
    adv["P(registrable GREEN) | S3 1x floor"] = rate(scen["S3_1x"], "n_any_green")
    adv["P(registrable GREEN) | S3 2x floor"] = rate(scen["S3_2x"], "n_any_green")
    adv["P(registrable GREEN) | S3 3x floor"] = rate(scen["S3_3x"], "n_any_green")
    d = scen["S4"]
    adv["P(>=2 GREEN) | S4 (2x/2.5x/3x)"] = d["n_multi_green"] / d["n_trials"]
    adv["P(correct tie-break | >=2 GREEN) | S4 (advisory >=0.90)"] = (
        d["n_tiebreak_correct"] / d["n_multi_green"] if d["n_multi_green"] else float("nan"))
    d = scen["S4b"]
    adv["P(correct tie-break | >=2 GREEN) | S4b separated 2x/3x/5x"] = (
        d["n_tiebreak_correct"] / d["n_multi_green"] if d["n_multi_green"] else float("nan"))
    # S6 neutralization: false-GREEN + pivot rate should match S1
    adv["S6 P(any false GREEN) [Tc-hetero, expect ~= S1]"] = rate(scen["S6"], "n_any_green")
    adv["S6 P(pivot) [expect ~= S1 0.38]"] = rate(scen["S6"], "n_pivot")
    # S5 flag detail + S5-strong confirmation (is the failure magnitude-specific?)
    d = scen["S5"]
    adv["S5 (Delta=-1x floor): P(wrong-sign cell ANOMALOUS)"] = d["cell_anom"][0]/d["n_trials"]
    adv["S5 (Delta=-1x floor): P(wrong-sign cell terminal RED)"] = d["cell_red"][0]/d["n_trials"]
    adv["S5 (Delta=-1x floor): P(INVALID pivot fired)"] = rate(d, "n_pivot")
    d = scen["S5_strong"]
    adv["S5-strong (Delta=-1.0 sd): P(wrong-sign cell ANOMALOUS)"] = d["cell_anom"][0]/d["n_trials"]
    adv["S5-strong (Delta=-1.0 sd): P(INVALID pivot fired)"] = rate(d, "n_pivot")
    # anomaly-rate discrepancy: sim (t-based) vs spec planning number (normal approx)
    adv["S1 per-cell false-anomaly (sim, t_15)"] = float(s1["band_counts"][0, ANOMALOUS]/s1["n_trials"])
    adv["S1 per-cell false-anomaly (spec planning, normal approx)"] = 0.0251
    # S7 raw-vs-contrast gap: pivot & green shift vs offset
    for off in (0.10, 0.30):
        d = scen[f"S7_{off}"]
        adv[f"S7 offset {off}x: P(pivot)"] = rate(d, "n_pivot")
        adv[f"S7 offset {off}x: P(any GREEN)"] = rate(d, "n_any_green")
        adv[f"S7 offset {off}x: P(any INCONCLUSIVE)"] = rate(d, "n_any_incon")
    out["advisory"] = adv

    # ---- per-cell null terminal distribution (validation vs AG R2) ----
    out["S1_per_cell_terminal"] = {
        CELLS[c]: {BAND_NAME[b]: float(s1["band_counts"][c, b] / s1["n_trials"])
                   for b in (GREEN, AMBER, RED, ANOMALOUS, INCONCLUSIVE)}
        for c in range(nc)
    }
    out["S1_pivot_rate"] = v31_pivot_rate

    # ---- verdict ----
    all_hard_pass = all(c["pass_"] for c in out["hard_criteria"])
    out["verdict"] = "OC-clean" if all_hard_pass else "OC-flags-found"

    print("\n=== HARD CRITERIA ===")
    for c in out["hard_criteria"]:
        print(f"  [{'PASS' if c['pass_'] else 'FAIL'}] {c['name']}: "
              f"{c['measured']:.6g} (tol {c['tolerance']})")
    print(f"\nVERDICT: {out['verdict']}")
    print("\n=== JSON ===")
    print(json.dumps(out, indent=2, default=float))


if __name__ == "__main__":
    main()
