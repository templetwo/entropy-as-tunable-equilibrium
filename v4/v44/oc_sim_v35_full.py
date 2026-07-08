#!/usr/bin/env python3
"""
v4.4 scout — REGISTRATION-GRADE OC simulator (v3.5 rule, exhaustive).

Faithful §7 band_cell / §4 shared ladder / §7 pivot_licensed. Reproduces the
§9.3 predeclared expected values and diffs each vs the ratified §13 numbers.

FIDELITY (the one substantive divergence from the committed core, now the erratum):
  §7 band_cell + oc_simulation_v32.py use an sd_hat-SCALED floor
      floor_c(sd_hat) = Z * sd_hat * sqrt(2/B).
  The committed oc_sim_v35.py used a FIXED floor (Z*sqrt(2/B) at sd=1). This
  script uses the faithful sd_hat-scaled floor everywhere.  The sd_up coupled-
  upper RED clause (§3.3) is the tell: a chi2-upper-confidence bound is only
  meaningful on an ESTIMATED sd -> sd_cell is the sample sd_hat -> floor scales.

ESTIMAND INVARIANT (rerun-power arbitration): mu_hat = mean(B blocks) - mean(64
  ref), reference redrawn each replication so var = sd^2(1/B+1/64); SE calibrated
  at alpha=0.05 (selftest asserts H0 alpha ~ 0.05, not ~0.019).

REFERENCE SHARING (§187, §493): baseline = INDEPENDENT per-cell / per-statistic
  noise + reference. Correlated A=B / C=D noise is fork-8 sensitivity (separate).

Interpreter: /usr/bin/python3 (Python 3.9.6, numpy 2.0.2, scipy 1.13.1). Deterministic.
"""
import numpy as np, math, json
from scipy.stats import t as tdist, chi2 as chi2dist

SEED = 20260710                 # §9.1 registered-sim seed
REF  = 64
Z    = 3.858
NS   = Z * math.sqrt(2.0 / 96.0) / 0.4      # STABLE noise scale = floor96/0.4 = 1.3922 (§9.1)
RUNGS = {1: (16, 96), 2: (32, 96), 3: (32, 128)}
CELLS = ("A", "B", "C", "D", "AxT2", "AxT4")

def floor_c(sd, B):  return Z * sd * np.sqrt(2.0 / B)
def se_c(sd, n):     return sd * np.sqrt(1.0 / n + 1.0 / REF)
T1  = {n: float(tdist.ppf(0.95,  n - 1)) for n in (8, 16, 32, 56)}
T2  = {n: float(tdist.ppf(0.975, n - 1)) for n in (8, 16, 32, 56)}
CHI = {n: float(np.sqrt((n - 1) / chi2dist.ppf(0.05, n - 1))) for n in (8, 16, 32, 56)}


def _check_constants():
    assert abs(floor_c(1, 96)  - 0.55685) < 5e-5
    assert abs(floor_c(1, 128) - 0.48225) < 5e-5
    for n, v in ((16, 0.2795), (32, 0.2165), (56, 0.1830), (8, 0.3750)): assert abs(se_c(1, n) - v) < 5e-4
    for n, v in ((16, 1.753), (32, 1.696), (56, 1.673)): assert abs(T1[n] - v) < 5e-4
    for n, v in ((16, 2.131), (32, 2.040), (56, 2.004)): assert abs(T2[n] - v) < 5e-4
    for n, v in ((16, 1.437), (32, 1.268), (8, 1.797)):  assert abs(CHI[n] - v) < 5e-4
    assert abs((floor_c(1, 96) - T1[16] * se_c(1, 16)) - 0.067) < 2e-3   # one-sided RED kappa @16b
    assert abs((floor_c(1, 96) - 0.306) - 0.251) < 2e-3                  # kappa_56 reband edge
    return True


# --------------------------------------------------------------------------
# §7 band_cell (faithful sd_hat-scaled floor; vectorized)
# --------------------------------------------------------------------------
def band(mu, sd, n, B, sigma):
    """Four-band on ONE statistic. sigma in {+1,-1,None(two-sided)}. -> object array."""
    two = sigma is None
    t = T2[n] if two else T1[n]
    fl, se = floor_c(sd, B), se_c(sd, n)
    sd_up = sd * CHI[n]
    fl_up, se_up = floor_c(sd_up, B), se_c(sd_up, n)
    x = np.abs(mu) if two else sigma * mu
    green = (x - t * se) > fl
    anom  = np.zeros(np.shape(mu), bool) if two else (x < -t * se)
    aligned   = (x + t * se < fl) & (x + t * se_up < fl_up)
    magnitude = (np.abs(mu) + t * se < fl) & (np.abs(mu) + t * se_up < fl_up)
    red = (~anom) & aligned & magnitude
    out = np.full(np.shape(mu), 'AMBER', dtype=object)
    out[red] = 'RED'; out[anom] = 'ANOM'; out[green] = 'GREEN'   # GREEN>ANOM>RED (disjoint)
    return out


# --------------------------------------------------------------------------
# §4 shared multi-statistic ladder — quad+omega drive; occ stamped, never drives
# --------------------------------------------------------------------------
def _corr_blocks(rng, N, means, rho_qw, rho_qc, sd):
    """32 blocks x (quad,omega,occ), per-block corr(q,w)=rho_qw, corr(q,occ)=rho_qc, w-occ=0."""
    C = np.array([[1.0, rho_qw, rho_qc], [rho_qw, 1.0, 0.0], [rho_qc, 0.0, 1.0]])
    L = np.linalg.cholesky(C)
    z = rng.standard_normal((N, 32, 3))
    blk = np.asarray(means) + z @ L.T
    return blk * sd            # (N,32,3) in sd_cell units


def sim_cell(rng, N, dq, sq, dw, sw, docc, rho_qw=0.0, rho_qc=0.0, sd=1.0):
    """Run one cell jointly through the shared ladder. Returns dict of terminal
    band arrays for quad/omega/occ + the terminal rung. All three stamped at the
    single terminal rung (couple 7). AMBER at ceiling -> INCONCLUSIVE for the two
    laddered statistics (quad, omega); occ AMBER stays AMBER (never INCONCLUSIVE)."""
    blk = _corr_blocks(rng, N, (dq, dw, docc), rho_qw, rho_qc, sd)
    bq, bw, bo = blk[:, :, 0], blk[:, :, 1], blk[:, :, 2]
    rq = rng.normal(0, sd / math.sqrt(REF), N)   # independent per-statistic 64-block reference
    rw = rng.normal(0, sd / math.sqrt(REF), N)
    ro = rng.normal(0, sd / math.sqrt(REF), N)

    def bands_at(blkX, refX, n, B, sig):
        return band(blkX[:, :n].mean(1) - refX, blkX[:, :n].std(1, ddof=1), n, B, sig)

    # ladder driver: primary (quad) OR omega AMBER extends; primary GREEN/ANOM short-circuits
    q1, w1 = bands_at(bq, rq, 16, 96, sq), bands_at(bw, rw, 16, 96, sw)
    term1 = ((q1 == 'GREEN') | (q1 == 'ANOM')) | (~((q1 == 'AMBER') | (w1 == 'AMBER')))
    q2, w2 = bands_at(bq, rq, 32, 96, sq), bands_at(bw, rw, 32, 96, sw)
    term2 = ((q2 == 'GREEN') | (q2 == 'ANOM')) | (~((q2 == 'AMBER') | (w2 == 'AMBER')))
    rung = np.where(term1, 1, np.where(term2, 2, 3))

    def stamp(blkX, refX, sig):
        b = {r: bands_at(blkX, refX, n, B, sig) for r, (n, B) in RUNGS.items()}
        return np.where(rung == 1, b[1], np.where(rung == 2, b[2], b[3]))
    q, w, o = stamp(bq, rq, sq), stamp(bw, rw, sw), stamp(bo, ro, None)
    q = np.where((rung == 3) & (q == 'AMBER'), 'INCONCLUSIVE', q)
    w = np.where((rung == 3) & (w == 'AMBER'), 'INCONCLUSIVE', w)
    return {"quad": q, "omega": w, "occ": o, "rung": rung}


def stable_flags(rng, N, mu_true, sigma_reg, rho):
    """P1-B STABLE (>=12/16 per-seed curls agree with registered sigma). §9.1 regimes:
    rho=-1 inverted transduction -> curl agrees with sigma_reg by construction (16/16, STABLE True);
    rho=0 uncoupled -> chance p=0.5; rho>0 -> p_true=0.5+0.5*rho*tanh(|mu|/NS), agree=p_true
    if sign(mu)==sigma_reg else 1-p_true (so a wrong-sign current tends UNSTABLE, suspenders bite)."""
    if rho == -1:
        return np.ones(N, bool)
    if mu_true == 0.0:
        p = 0.5
    else:
        p_true = min(max(0.5 + 0.5 * rho * math.tanh(abs(mu_true) / NS), 0.0), 1.0)
        p = p_true if (mu_true > 0) == (sigma_reg > 0) else 1.0 - p_true
    return rng.binomial(16, p, N) >= 12


# --------------------------------------------------------------------------
# §7 pivot_licensed (vectorized over replications)
# --------------------------------------------------------------------------
def pivot_licensed(gating, stable, omega, occ, descriptive, GATING, FULL):
    GATING, FULL = set(GATING), set(FULL); DEMOTED = FULL - GATING
    N = len(next(iter(gating.values())))
    if (set(gating) != GATING or set(omega) != FULL or set(occ) != FULL
            or set(descriptive) != DEMOTED or not (GATING <= FULL) or not gating):
        return np.zeros(N, bool)
    ok = np.ones(N, bool)
    for b in omega.values():        ok &= ~((b == 'GREEN') | (b == 'ANOM'))        # (iii) omega veto
    for c in GATING:                ok &= ~(omega[c] == 'INCONCLUSIVE')            # (0') gating omega unresolved
    for b in occ.values():          ok &= ~(b == 'GREEN')                          # (iii') occupancy veto
    for b in descriptive.values():  ok &= ~((b == 'GREEN') | (b == 'ANOM'))        # demoted primary disposition
    for c in GATING:
        b = gating[c]
        ok &= (b == 'RED')                                                          # (i)+(0)+(0') all-RED, no GREEN/ANOM/INCONC
    for c in GATING:
        ok &= (~(gating[c] == 'RED')) | stable[c]                                   # (ii) suspenders
    return ok


def _rate(mask): return float(np.mean(mask))
def _dist(arr):
    u, c = np.unique(arr, return_counts=True); N = len(arr)
    return {k: round(int(v) / N, 5) for k, v in zip(u, c)}


# --------------------------------------------------------------------------
# S1 — global null (both sidedness branches, rho sweep) : gate 1 + advisories
# --------------------------------------------------------------------------
def scenario_S1(rng, N, branch, rho_qw=0.0, rho_qc=0.0):
    """All six cells null (dq=dw=docc=0). branch='two_sided' (real INDETERMINATE null)
    or 'one_sided' (force-registered sigma=+1 sensitivity, S1b). Reports false-GREEN,
    terminal false-anomaly, omega/occ veto null firing, rung dist, pivot-under-null."""
    sq = sw = (None if branch == 'two_sided' else +1)
    cells = {c: sim_cell(rng, N, 0.0, sq, 0.0, sw, 0.0, rho_qw, rho_qc) for c in CELLS}
    Q = np.stack([cells[c]["quad"] for c in CELLS])
    W = np.stack([cells[c]["omega"] for c in CELLS])
    O = np.stack([cells[c]["occ"] for c in CELLS])
    R = np.stack([cells[c]["rung"] for c in CELLS])
    stable = {c: stable_flags(rng, N, 0.0, +1, rho_qw if False else 1.0) for c in CELLS}  # null: STABLE at chance
    stable = {c: stable_flags(rng, N, 0.0, +1, 0.0) for c in CELLS}                        # rho irrelevant when mu=0
    piv = pivot_licensed({c: cells[c]["quad"] for c in CELLS}, stable,
                         {c: cells[c]["omega"] for c in CELLS},
                         {c: cells[c]["occ"] for c in CELLS}, {}, CELLS, CELLS)
    return {
        "branch": branch, "rho_qw": rho_qw, "rho_qc": rho_qc, "N": N,
        "per_cell_false_green_primary": round(float((Q == 'GREEN').mean()), 6),
        "any_false_green_primary":      round(float(((Q == 'GREEN').any(0)).mean()), 6),
        "per_cell_terminal_false_anom": round(float((Q == 'ANOM').mean()), 5),
        "any_false_anom":               round(float(((Q == 'ANOM').any(0)).mean()), 5),
        "omega_veto_null_per_cell":     round(float(((W == 'GREEN') | (W == 'ANOM')).mean()), 5),
        "omega_veto_null_any":          round(float((((W == 'GREEN') | (W == 'ANOM')).any(0)).mean()), 5),
        "occ_veto_null_per_cell":       round(float((O == 'GREEN').mean()), 6),
        "primary_inconclusive_per_cell":round(float((Q == 'INCONCLUSIVE').mean()), 5),
        "omega_inconclusive_per_cell":  round(float((W == 'INCONCLUSIVE').mean()), 5),
        "rung_dist_per_cell":           {f"rung{r}": round(float((R == r).mean()), 5) for r in (1, 2, 3)},
        "expected_blocks_per_cell":     round(float(np.where(R == 1, 16, 32).mean()), 2),
        "pivot_under_null":             round(float(piv.mean()), 6),
    }


if __name__ == '__main__':
    assert _check_constants(), "law-#4 constant check failed"
    rng = np.random.default_rng(SEED)

    # ---- keep: gate-9 compound reconciliation (faithful floor) ----
    N9 = 4_000_000; f96 = floor_c(1, 96)
    # reuse sim_cell's primary path via a single wrong-sign cell, one-sided sigma=+1
    wc = sim_cell(rng, N9, -f96, +1, 0.0, +1, 0.0)   # omega null; we only read quad
    comp = round(float(1 - (wc["quad"] == 'RED').mean()), 5)
    print(f"[gate9 reconcile] faithful compound (shared-ladder primary) = {comp}  "
          f"(committed fixed-floor 0.980; primary-only skeleton 0.940)")

    # ---- S1 global null: both branches, rho_qw sweep ----
    out = {"seed": SEED, "gate9_compound_faithful": comp, "S1": {}}
    Ns1 = 1_000_000
    for branch in ("two_sided", "one_sided"):
        out["S1"][branch] = {}
        for rqw in (0.0, 0.3, 0.6):
            out["S1"][branch][f"rho_qw={rqw}"] = scenario_S1(rng, Ns1, branch, rho_qw=rqw, rho_qc=rqw)
    print(json.dumps(out["S1"], indent=1))

    # ---- §9.3 diff for S1 ----
    ts0 = out["S1"]["two_sided"]["rho_qw=0.0"]; os0 = out["S1"]["one_sided"]["rho_qw=0.0"]
    print("\n===== §9.3 / §13 DIFF (S1, rho_qw=0) =====")
    def diff(name, got, exp, tol_ratio=0.4):
        rel = abs(got - exp) / exp if exp else abs(got)
        flag = "OK" if rel <= tol_ratio else "SHIFT"
        print(f"  {name:44} faithful={got:<10} §13={exp:<10} {flag}")
    diff("gate1 six-cell false-GREEN (two-sided)", ts0["any_false_green_primary"], 0.0019)
    diff("gate1 per-cell false-GREEN (two-sided)", ts0["per_cell_false_green_primary"], 0.0003)
    diff("per-cell terminal false-anom (one-sided)", os0["per_cell_terminal_false_anom"], 0.047)
    diff("omega-veto null per-cell (one-sided)", os0["omega_veto_null_per_cell"], 0.030)
    diff("occ-veto null per-cell", ts0["occ_veto_null_per_cell"], 1e-4)
    diff("primary INCONCLUSIVE per-cell (one-sided)", os0["primary_inconclusive_per_cell"], 0.306)
    diff("expected blocks/cell (one-sided)", os0["expected_blocks_per_cell"], 31.0)
    diff("rung1 fraction (one-sided)", os0["rung_dist_per_cell"]["rung1"], 0.084)
    diff("pivot under null (one-sided, rho=0)", os0["pivot_under_null"], 0.017)
    diff("pivot under null (two-sided)", ts0["pivot_under_null"], 0.0014)
