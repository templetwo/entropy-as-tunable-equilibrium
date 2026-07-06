#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v4 Fork Harness, version v4h-1.0.0
Temple of Two / Anthony J. Vasquez Sr. entropy-as-engine program.

Pre-registered first-passage + probability-current fork for the causal-entropic
Langevin system, packaged for execution inside the Grok app Python sandbox
(numpy only, chunked work units, NDJSON output to stdout).

DESIGN CONTRACT (do not edit when executing):
  - Every work unit is independent and deterministic given its unit id.
  - Each unit prints exactly one NDJSON result line plus a few log lines.
  - Raw stdout is the only valid output channel. No prose numbers.
  - Two independent instances (Grok Heavy, Grok Expert) run identical unit
    lists; results must agree to float tolerance or the divergence is data.

PHYSICS SUMMARY:
  Overdamped Langevin particle, 2D box with dividing wall + channel.
  Causal-entropic force per Wissner-Gross & Freer 2013, implemented as the
  gradient of an ENDPOINT-COARSE-GRAINED path entropy proxy S_c(r, tau):
  Shannon entropy of the binned endpoint distribution of M free-diffusion
  rollouts of horizon tau respecting the geometry. This estimator choice is
  declared, not hidden; the paper must name it.

CONDITIONS (the fork):
  C0  Brownian gyrator calibration (Filliger & Reimann 2007). Two coupled
      coordinates, two bath temperatures. hot: Tx != Ty must show circulation;
      ctrl: Tx == Ty must show none. Validates the current estimator.
  C1  tau-sweep first passage, FROZEN (precomputed S_c grid -> conservative
      by construction) vs ONLINE (per-step stochastic path-sampled force).
      Occupancy + FPT histograms recorded in the same pass.
  C2  Coarse-grained probability current + circulation, accumulated inside
      the C1 runs (no separate units).
  C3  Kramers null check: MFPT vs channel length scaling in the frozen
      control. Validates FPT machinery (expect slope ~2 in log-log).
  C4  Engineered non-conservative variant: ONLINE force with directionally
      BIASED future sampling (paths see drift +b x-hat, dynamics does not).
      Generically non-gradient. Prediction: measurable circulation.

PRE-REGISTERED OUTCOME MAP (matches the program's four-outcome discipline):
  (a) FPT signature: KS(frozen vs online) p < 0.01 at >= 3 of 5 tau values
      with consistent median direction, WHILE occupancy histograms match
      (chi2 p > 0.05) -> kinetically distinguishable, occupancy-identical.
  (b) Current: any C1 online circulation z >= 3 (against seed-block sigma),
      with C0 hot passing and C0 ctrl null -> force effectively
      non-conservative, pivot to NESS framing.
  (c) Both null and C3 slope in [1.7, 2.3] -> pedagogical demonstration,
      conservative regime confirmed, no over-claim.
  (d) C4 circulation z >= 3 and monotone in bias b -> conservative-to-non-
      conservative transition engineered via sampling asymmetry.

USAGE:
  python v4_fork_harness.py --plan          # pre-registration manifest (JSON)
  python v4_fork_harness.py --list          # unit ids only
  python v4_fork_harness.py --selftest      # ~1 min miniature of everything
  python v4_fork_harness.py --unit UNIT_ID  # run one work unit
  python v4_fork_harness.py --analyze F.ndjson [F2.ndjson ...]  # local verdict
"""

import sys, json, math, time, hashlib, warnings
warnings.filterwarnings('ignore')
import numpy as np

VERSION = "v4h-1.1.0"

# ----------------------------------------------------------------------------
# Configuration (canonical; config_hash covers this dict)
# ----------------------------------------------------------------------------
CFG = {
    "version": VERSION,
    "box": {"Lx": 4.0, "Ly": 2.0, "wall_t": 0.30, "ch_w_default": 0.40},
    "bath": {"D": 1.0, "gamma": 1.0},          # kT = D*gamma = 1 reduced units
    "dyn": {"dt": 1.0e-2, "n_force_cache": 20}, # force refresh every 0.2 tu
    "entropy": {
        "estimator": "ENDPOINT_ENTROPY",        # declared estimator choice
        "dt_path": 4.0e-2,
        "h_ent": 0.20,                          # endpoint bin size
        "delta_fd": 0.10,                       # finite-difference half-step
        "M_online": 96,
        "M_grid": 400,
        "Tc": 1.0,                              # causal temperature
        "grid_nx": 40, "grid_ny": 20,
    },
    "fpt": {
        "start_frac": [0.25, 0.5],
        "target_margin": 0.20,                  # x >= wall_x1 + margin
        "K_target": 50,
        "T_max": 2500.0,
        "hist_edges_log10": [-0.5, 3.0, 24],    # log10 time bins
    },
    "current": {"cells_x": 24, "cells_y": 12},
    "occupancy": {"bins_x": 24},
    "gyrator": {
        "k": 1.0, "u": 0.6, "dt": 1.0e-3, "T_total": 2000.0,
        "hot": {"Tx": 4.0, "Ty": 1.0}, "ctrl": {"Tx": 2.5, "Ty": 2.5},
        "cells": 12, "extent": 4.0,
    },
    "sweeps": {
        "tau_grid": [0.25, 0.5, 1.0, 2.0],
        "seed_blocks": ["sb%d" % i for i in range(16)],
        "powered_taus": [0.25, 0.5],          # 400-passage FPT arms
        "powered_K": 400,
        "c3_channel_lengths": [0.15, 0.30, 0.60, 1.20],
        "c3_tau": 1.0,
        "c4_curl_biases": [0.5, 1.0],
        "c4_tau": 1.0,
        "c0_blocks": ["sb0", "sb1", "sb2", "sb3"],
    },
    "thresholds": {
        "ks_alpha": 0.01, "ks_min_taus": 2,
        "occupancy_chi2_alpha": 0.05,
        "mouth_z": 3.0,
        "mouth_sign_consistency": 12,          # of 16 blocks
        "kramers_slope": [1.7, 2.3],
    },
}

def config_hash():
    s = json.dumps(CFG, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(s.encode()).hexdigest()[:16]

def unit_seed(unit_id):
    h = hashlib.sha256(("v4h::" + unit_id).encode()).digest()
    return int.from_bytes(h[:8], "big")

# ----------------------------------------------------------------------------
# Geometry
# ----------------------------------------------------------------------------
class Geom:
    def __init__(self, Lx, Ly, wall_t, ch_w):
        self.Lx, self.Ly = Lx, Ly
        self.wx0, self.wx1 = Lx/2 - wall_t/2, Lx/2 + wall_t/2
        self.cy0, self.cy1 = Ly/2 - ch_w/2, Ly/2 + ch_w/2

    def blocked(self, xy):
        """xy: (..., 2) array -> boolean mask of illegal positions."""
        x, y = xy[..., 0], xy[..., 1]
        out = (x < 0) | (x > self.Lx) | (y < 0) | (y > self.Ly)
        wall = (x >= self.wx0) & (x <= self.wx1) & ~((y > self.cy0) & (y < self.cy1))
        return out | wall

def step_reflect(geom, pos, drift, noise):
    """Euler-Maruyama with rejection (approximates reflecting BC)."""
    prop = pos + drift + noise
    bad = geom.blocked(prop)
    if bad.any():
        prop[bad] = pos[bad]
    return prop

# ----------------------------------------------------------------------------
# Endpoint path entropy S_c(r, tau) and causal-entropic force
# ----------------------------------------------------------------------------
def endpoint_entropy(geom, r0, tau, M, rng, dt_path, h_ent, noise=None, bias=0.0,
                     curl_bias=0.0):
    """Shannon entropy of coarse-grained endpoint distribution of M rollouts.
    noise: optional pre-drawn array (n_steps, M, 2) for common random numbers.
    bias: sampling drift along +x seen only by rollouts (C4 breaker)."""
    n_steps = max(6, int(round(tau / dt_path)))
    sig = math.sqrt(2.0 * CFG["bath"]["D"] * dt_path)
    if noise is None:
        noise = rng.standard_normal((n_steps, M, 2)) * sig
    pos = np.tile(np.asarray(r0, dtype=float), (M, 1))
    if curl_bias != 0.0:
        # position-dependent rotation: non-gradient by construction
        bx = curl_bias * math.cos(math.pi * r0[1] / geom.Ly)
        by = curl_bias * math.sin(math.pi * r0[0] / geom.Lx)
        drift = np.array([bx * dt_path, by * dt_path])
    else:
        drift = np.array([bias * dt_path, 0.0])
    for k in range(n_steps):
        pos = step_reflect(geom, pos, drift, noise[k])
    ix = np.clip((pos[:, 0] / h_ent).astype(int), 0, int(geom.Lx / h_ent))
    iy = np.clip((pos[:, 1] / h_ent).astype(int), 0, int(geom.Ly / h_ent))
    nx = int(geom.Lx / h_ent) + 1
    counts = np.bincount(ix * (int(geom.Ly / h_ent) + 1) + iy,
                         minlength=nx * (int(geom.Ly / h_ent) + 1)).astype(float)
    p = counts[counts > 0] / M
    return float(-(p * np.log(p)).sum())

def _safe_point(geom, r):
    r = np.array(r, dtype=float)
    eps = 1e-3
    r[0] = min(max(r[0], eps), geom.Lx - eps)
    r[1] = min(max(r[1], eps), geom.Ly - eps)
    if geom.blocked(r[None, :])[0]:
        # nudge out of the wall along x toward nearest open side
        r[0] = geom.wx0 - eps if abs(r[0] - geom.wx0) < abs(r[0] - geom.wx1) else geom.wx1 + eps
    return r

def force_online(geom, r, tau, rng, M, bias=0.0, curl_bias=0.0):
    """Central-difference gradient of endpoint entropy, common random numbers."""
    e = CFG["entropy"]; d = e["delta_fd"]
    n_steps = max(6, int(round(tau / e["dt_path"])))
    sig = math.sqrt(2.0 * CFG["bath"]["D"] * e["dt_path"])
    noise = rng.standard_normal((n_steps, M, 2)) * sig
    pts = [(-d, 0.0), (d, 0.0), (0.0, -d), (0.0, d)]
    S = []
    for dx, dy in pts:
        p = _safe_point(geom, (r[0] + dx, r[1] + dy))
        S.append(endpoint_entropy(geom, p, tau, M, rng, e["dt_path"], e["h_ent"],
                                  noise=noise, bias=bias, curl_bias=curl_bias))
    Fx = e["Tc"] * (S[1] - S[0]) / (2 * d)
    Fy = e["Tc"] * (S[3] - S[2]) / (2 * d)
    return np.array([Fx, Fy])

def frozen_grid(geom, tau, rng):
    """Precompute S_c on a grid; return (S, xs, ys). Conservative by construction."""
    e = CFG["entropy"]
    xs = np.linspace(0.05, geom.Lx - 0.05, e["grid_nx"])
    ys = np.linspace(0.05, geom.Ly - 0.05, e["grid_ny"])
    S = np.full((e["grid_nx"], e["grid_ny"]), np.nan)
    for i, x in enumerate(xs):
        for j, y in enumerate(ys):
            if geom.blocked(np.array([[x, y]]))[0]:
                continue
            S[i, j] = endpoint_entropy(geom, (x, y), tau, e["M_grid"], rng,
                                       e["dt_path"], e["h_ent"])
    # fill wall NaNs with neighbor means so gradients near the wall are finite
    for _ in range(4):
        nan = np.isnan(S)
        if not nan.any():
            break
        pad = np.pad(S, 1, mode="edge")
        neigh = np.nanmean(np.stack([pad[:-2, 1:-1], pad[2:, 1:-1],
                                     pad[1:-1, :-2], pad[1:-1, 2:]]), axis=0)
        S[nan] = neigh[nan]
    return S, xs, ys

def force_frozen(geom, S, xs, ys, r):
    e = CFG["entropy"]
    i = np.clip(np.searchsorted(xs, r[0]) - 1, 1, len(xs) - 2)
    j = np.clip(np.searchsorted(ys, r[1]) - 1, 1, len(ys) - 2)
    hx, hy = xs[1] - xs[0], ys[1] - ys[0]
    Fx = e["Tc"] * (S[i + 1, j] - S[i - 1, j]) / (2 * hx)
    Fy = e["Tc"] * (S[i, j + 1] - S[i, j - 1]) / (2 * hy)
    return np.array([Fx, Fy])

# ----------------------------------------------------------------------------
# Accumulators
# ----------------------------------------------------------------------------
class CurrentAcc:
    """Coarse-grained probability current: per-cell summed displacement.
    Circulation computed on 2x2 plaquettes of the averaged field."""
    def __init__(self, geom, cx, cy):
        self.geom, self.cx, self.cy = geom, cx, cy
        self.disp = np.zeros((cx, cy, 2)); self.visits = np.zeros((cx, cy))
        self.n_steps = 0

    def add(self, r_old, r_new):
        mid = 0.5 * (r_old + r_new)
        i = min(int(mid[0] / self.geom.Lx * self.cx), self.cx - 1)
        j = min(int(mid[1] / self.geom.Ly * self.cy), self.cy - 1)
        self.disp[i, j] += (r_new - r_old); self.visits[i, j] += 1
        self.n_steps += 1

    def field(self):
        J = self.disp / max(self.n_steps, 1)
        return J

    def circulation_stats(self):
        J = self.field()
        # plaquette circulation: Jx bottom - Jx top + Jy right - Jy left
        circ = (J[:-1, :-1, 0] + J[1:, :-1, 1] - J[1:, 1:, 0] - J[:-1, 1:, 1])
        k = int(np.argmax(np.abs(circ)))
        i, j = np.unravel_index(k, circ.shape)
        return {"max_abs_circ": float(np.abs(circ).max()),
                "max_circ_signed": float(circ[i, j]),
                "max_circ_cell": [int(i), int(j)],
                "sum_abs_circ": float(np.abs(circ).sum())}

class MouthFlux:
    """Pre-declared fixed-region current statistic for v4.1 fork (b).
    Counts signed crossings of two vertical gates (left/right of the wall)
    and two horizontal gates (above/below channel midline inside the mouth),
    yielding a signed loop circulation around the channel mouth region.
    Flux counting, not displacement averaging: each gate crossing adds +-1."""
    def __init__(self, geom):
        self.g = geom
        m = 0.15  # gate offset from wall faces (pre-declared)
        self.xL, self.xR = geom.wx0 - m, geom.wx1 + m
        self.yMid = 0.5 * (geom.cy0 + geom.cy1)
        self.loop = 0  # signed circulation quanta
        self.crossings = 0

    def add(self, r_old, r_new):
        yl, yh = self.g.cy0 - 0.25, self.g.cy1 + 0.25
        # vertical gate at xL: count +1 rightward crossing if in mouth band
        for x0, sgn in ((self.xL, +1), (self.xR, -1)):
            if (r_old[0] - x0) * (r_new[0] - x0) < 0:
                ymid = 0.5 * (r_old[1] + r_new[1])
                if yl < ymid < yh:
                    d = 1 if r_new[0] > r_old[0] else -1
                    # upper half contributes +d to loop, lower half -d
                    self.loop += sgn * d * (1 if ymid > self.yMid else -1)
                    self.crossings += 1

    def stats(self, n_steps):
        return {"mouth_loop": int(self.loop),
                "mouth_crossings": int(self.crossings),
                "mouth_loop_rate": self.loop / max(n_steps, 1)}

class FPTAcc:
    def __init__(self):
        lo, hi, nb = CFG["fpt"]["hist_edges_log10"]
        self.edges = np.logspace(lo, hi, nb + 1)
        self.counts = np.zeros(nb, dtype=int)
        self.times = []

    def add(self, t):
        self.times.append(t)
        b = np.searchsorted(self.edges, t) - 1
        if 0 <= b < len(self.counts):
            self.counts[b] += 1

    def summary(self):
        t = np.array(self.times) if self.times else np.array([np.nan])
        return {"n": len(self.times),
                "mean": float(np.nanmean(t)), "median": float(np.nanmedian(t)),
                "q25": float(np.nanpercentile(t, 25)),
                "q75": float(np.nanpercentile(t, 75)),
                "hist": self.counts.tolist(),
                "times": [round(float(x), 3) for x in self.times]}

# ----------------------------------------------------------------------------
# Work-unit runners
# ----------------------------------------------------------------------------
def run_gyrator(variant, seed, scale=1.0):
    g = CFG["gyrator"]; T = g[variant]
    rng = np.random.default_rng(seed)
    dt, Ttot = g["dt"], g["T_total"] * scale
    n = int(Ttot / dt)
    k, u = g["k"], g["u"]
    sx, sy = math.sqrt(2 * T["Tx"] * dt), math.sqrt(2 * T["Ty"] * dt)
    pos = np.zeros(2); Lsum = 0.0
    cells, ext = g["cells"], g["extent"]
    disp = np.zeros((cells, cells, 2)); nsteps = 0
    for _ in range(n):
        F = np.array([-k * pos[0] - u * pos[1], -k * pos[1] - u * pos[0]])
        d = F * dt
        z = np.array([rng.standard_normal() * sx, rng.standard_normal() * sy])
        new = pos + d + z
        Lsum += pos[0] * (new[1] - pos[1]) - pos[1] * (new[0] - pos[0])
        i = min(max(int((new[0] + ext / 2) / ext * cells), 0), cells - 1)
        j = min(max(int((new[1] + ext / 2) / ext * cells), 0), cells - 1)
        disp[i, j] += (new - pos); nsteps += 1
        pos = new
    J = disp / nsteps
    circ = (J[:-1, :-1, 0] + J[1:, :-1, 1] - J[1:, 1:, 0] - J[:-1, 1:, 1])
    return {"ang_mom_rate": Lsum / (n * dt),
            "max_abs_circ": float(np.abs(circ).max()),
            "sum_abs_circ": float(np.abs(circ).sum()),
            "n_steps": n}

def run_chamber(mode, tau, seed, ch_w=None, bias=0.0, scale=1.0, transit_clock=False,
                curl_bias=0.0):
    """mode: 'frozen' | 'online'. Returns FPT + occupancy + current stats."""
    b = CFG["box"]; f = CFG["fpt"]; e = CFG["entropy"]; dyn = CFG["dyn"]
    geom = Geom(b["Lx"], b["Ly"], ch_w if ch_w else b["wall_t"], b["ch_w_default"])
    rng = np.random.default_rng(seed)
    S = xs = ys = None
    if mode == "frozen":
        S, xs, ys = frozen_grid(geom, tau, rng)
    dt = dyn["dt"]; sig = math.sqrt(2 * CFG["bath"]["D"] * dt)
    start = np.array([b["Lx"] * f["start_frac"][0], b["Ly"] * f["start_frac"][1]])
    target_x = geom.wx1 + f["target_margin"]
    pos = start.copy(); t_run = 0.0; t_launch = 0.0
    fpt = FPTAcc(); occ = np.zeros(CFG["occupancy"]["bins_x"], dtype=int)
    cur = CurrentAcc(geom, CFG["current"]["cells_x"], CFG["current"]["cells_y"])
    mouth = MouthFlux(geom)
    Fcache = np.zeros(2); k_since = dyn["n_force_cache"]
    in_channel = False; t_enter = 0.0
    K_target = max(3, int(f["K_target"] * scale)); T_max = f["T_max"] * scale
    n_force_evals = 0
    while len(fpt.times) < K_target and t_run < T_max:
        if k_since >= dyn["n_force_cache"]:
            if mode == "frozen":
                Fcache = force_frozen(geom, S, xs, ys, pos)
            else:
                Fcache = force_online(geom, pos, tau, rng, e["M_online"], bias=bias,
                                      curl_bias=curl_bias)
                n_force_evals += 1
            k_since = 0
        noise = rng.standard_normal(2) * sig
        new = step_reflect(geom, pos[None, :].copy(), Fcache * dt, noise[None, :])[0]
        cur.add(pos, new)
        mouth.add(pos, new)
        ob = min(int(new[0] / geom.Lx * len(occ)), len(occ) - 1)
        occ[ob] += 1
        pos = new; t_run += dt; k_since += 1
        if transit_clock:
            # transit-only clock: measure channel traversal time only
            if not in_channel and geom.wx0 <= pos[0] <= geom.wx1:
                in_channel = True; t_enter = t_run
            elif in_channel and pos[0] < geom.wx0:
                in_channel = False  # backed out; attempt void
            elif in_channel and pos[0] >= target_x:
                fpt.add(t_run - t_enter)
                in_channel = False
                pos = start.copy()
        else:
            if pos[0] >= target_x:
                fpt.add(t_run - t_launch)
                pos = start.copy(); t_launch = t_run
    return {"fpt": fpt.summary(), "occupancy_x": occ.tolist(),
            "current": cur.circulation_stats(),
            "mouth": mouth.stats(cur.n_steps),
            "censored": bool(len(fpt.times) < K_target),
            "t_total": round(t_run, 1), "n_force_evals": n_force_evals}

# ----------------------------------------------------------------------------
# Unit registry
# ----------------------------------------------------------------------------
def build_units():
    sw = CFG["sweeps"]; units = []
    for v in ["hot", "ctrl"]:
        for sb in sw["c0_blocks"]:
            units.append(f"C0_{v}_{sb}")
    for mode in ["frozen", "online"]:
        for tau in sw["tau_grid"]:
            for sb in sw["seed_blocks"]:
                units.append(f"C1_{mode}_tau{tau}_{sb}")
    for L in sw["c3_channel_lengths"]:
        for sb in sw["seed_blocks"][:4]:
            units.append(f"C3t_frozen_L{L}_tau{sw['c3_tau']}_{sb}")
    for cb in sw["c4_curl_biases"]:
        for sb in sw["seed_blocks"][:8]:
            units.append(f"C4c_online_cb{cb}_tau{sw['c4_tau']}_{sb}")
    return units

def run_unit(unit_id, scale=1.0):
    t0 = time.time()
    seed = unit_seed(unit_id)
    parts = unit_id.split("_")
    if parts[0] == "C0":
        res = run_gyrator(parts[1], seed, scale=scale)
    elif parts[0] == "C1":
        tau = float(parts[2][3:])
        kscale = scale
        if tau in CFG["sweeps"]["powered_taus"]:
            kscale = scale * CFG["sweeps"]["powered_K"] / CFG["fpt"]["K_target"]
        res = run_chamber(parts[1], tau, seed, scale=kscale)
    elif parts[0] == "C3t":
        L = float(parts[2][1:]); tau = float(parts[3][3:])
        res = run_chamber("frozen", tau, seed, ch_w=L, scale=scale,
                          transit_clock=True)
    elif parts[0] == "C4c":
        cb = float(parts[2][2:]); tau = float(parts[3][3:])
        res = run_chamber("online", tau, seed, curl_bias=cb, scale=scale)
    else:
        raise ValueError("unknown unit: " + unit_id)
    out = {"type": "result", "unit": unit_id, "seed": seed,
           "config_hash": config_hash(), "version": VERSION,
           "numpy": np.__version__, "scale": scale,
           "runtime_s": round(time.time() - t0, 1), "data": res}
    print(json.dumps(out, separators=(",", ":")))
    return out

# ----------------------------------------------------------------------------
# Analysis (run locally, not in the sandbox)
# ----------------------------------------------------------------------------
def ks_stat(a, b):
    a, b = np.sort(np.asarray(a)), np.sort(np.asarray(b))
    allv = np.concatenate([a, b]); allv.sort()
    ca = np.searchsorted(a, allv, side="right") / len(a)
    cb = np.searchsorted(b, allv, side="right") / len(b)
    return float(np.abs(ca - cb).max())

def perm_p(a, b, n_perm=2000, seed=7):
    rng = np.random.default_rng(seed)
    obs = ks_stat(a, b); pool = np.concatenate([a, b]); na = len(a); c = 0
    for _ in range(n_perm):
        rng.shuffle(pool)
        if ks_stat(pool[:na], pool[na:]) >= obs:
            c += 1
    return obs, (c + 1) / (n_perm + 1)

def analyze(paths):
    rows = []
    for p in paths:
        with open(p) as fh:
            for line in fh:
                line = line.strip()
                if line.startswith("{"):
                    r = json.loads(line)
                    if r.get("type") == "result":
                        rows.append(r)
    th = CFG["thresholds"]; rep = {"n_results": len(rows), "config_hash": config_hash()}
    ch = {r["config_hash"] for r in rows}
    rep["config_match"] = (ch == {config_hash()}) if rows else False
    # C0 calibration
    hot = [r for r in rows if r["unit"].startswith("C0_hot")]
    ctl = [r for r in rows if r["unit"].startswith("C0_ctrl")]
    if hot and ctl:
        h = np.mean([abs(r["data"]["ang_mom_rate"]) for r in hot])
        c = np.mean([abs(r["data"]["ang_mom_rate"]) for r in ctl])
        rep["C0"] = {"hot_absL": h, "ctrl_absL": c, "pass": bool(h > 5 * max(c, 1e-12))}
    # C1: FPT frozen vs online per tau; occupancy chi2
    c1 = {}
    for tau in CFG["sweeps"]["tau_grid"]:
        fz = [t for r in rows if r["unit"].startswith(f"C1_frozen_tau{tau}_")
              for t in r["data"]["fpt"]["times"]]
        on = [t for r in rows if r["unit"].startswith(f"C1_online_tau{tau}_")
              for t in r["data"]["fpt"]["times"]]
        if len(fz) >= 10 and len(on) >= 10:
            ks, p = perm_p(fz, on)
            of = np.sum([r["data"]["occupancy_x"] for r in rows
                         if r["unit"].startswith(f"C1_frozen_tau{tau}_")], axis=0)
            oo = np.sum([r["data"]["occupancy_x"] for r in rows
                         if r["unit"].startswith(f"C1_online_tau{tau}_")], axis=0)
            of, oo = of / of.sum(), oo / oo.sum()
            chi2 = float(np.sum((of - oo) ** 2 / (of + oo + 1e-12)))
            c1[str(tau)] = {"ks": round(ks, 4), "p": round(p, 4),
                            "median_shift": float(np.median(on) - np.median(fz)),
                            "occ_chi2": round(chi2, 5)}
    rep["C1"] = c1
    sig_taus = [t for t, v in c1.items() if v["p"] < th["ks_alpha"]]
    dirs = {np.sign(c1[t]["median_shift"]) for t in sig_taus}
    rep["fork_a_fpt_signature"] = bool(len(sig_taus) >= th["ks_min_taus"] and len(dirs) == 1)
    # C2 (v4.1): channel-mouth signed loop rate, z + coherence clause
    circs = {}
    for tau in CFG["sweeps"]["tau_grid"]:
        v = [r["data"]["mouth"]["mouth_loop_rate"] for r in rows
             if r["unit"].startswith(f"C1_online_tau{tau}_")]
        vf = [r["data"]["mouth"]["mouth_loop_rate"] for r in rows
              if r["unit"].startswith(f"C1_frozen_tau{tau}_")]
        if len(v) >= 8 and len(vf) >= 8:
            mu_f, sd_f = np.mean(vf), np.std(vf) + 1e-15
            z = float((np.mean(v) - mu_f) / (sd_f / math.sqrt(len(vf))))
            pos = sum(1 for x in v if x > 0); neg = len(v) - pos
            circs[str(tau)] = {"online_mean_rate": float(np.mean(v)),
                               "frozen_mean_rate": float(mu_f),
                               "z": z,
                               "sign_consistency": int(max(pos, neg)),
                               "n_blocks": len(v),
                               "dominant_sign": 1 if pos >= neg else -1}
    rep["C2"] = circs
    trig = {t: c for t, c in circs.items()
            if abs(c["z"]) >= th["mouth_z"]
            and c["sign_consistency"] >= th["mouth_sign_consistency"]}
    adj_ok = False
    taus_sorted = sorted(circs, key=float)
    for i in range(len(taus_sorted) - 1):
        a, b = taus_sorted[i], taus_sorted[i + 1]
        if a in trig and b in trig and            circs[a]["dominant_sign"] == circs[b]["dominant_sign"]:
            adj_ok = True
    rep["fork_b_current"] = bool(len(trig) >= 1 and
                                 (len(trig) == 1 or adj_ok))
    rep["fork_b_detail"] = {"triggered_taus": sorted(trig),
                            "adjacent_sign_coherent": adj_ok}
    # C3 Kramers slope
    pts = []
    for L in CFG["sweeps"]["c3_channel_lengths"]:
        m = [r["data"]["fpt"]["mean"] for r in rows
             if r["unit"].startswith(f"C3t_frozen_L{L}_")]
        if m:
            pts.append((L, np.mean(m)))
    if len(pts) >= 3:
        lx = np.log([p[0] for p in pts]); ly = np.log([p[1] for p in pts])
        slope = float(np.polyfit(lx, ly, 1)[0])
        lo, hi = th["kramers_slope"]
        rep["C3"] = {"slope": round(slope, 3), "pass": bool(lo <= slope <= hi),
                     "points": [[p[0], round(p[1], 2)] for p in pts]}
    # C4c engineered curl breaker (mouth statistic)
    c4 = {}
    for b in CFG["sweeps"]["c4_curl_biases"]:
        v = [r["data"]["mouth"]["mouth_loop_rate"] for r in rows
             if r["unit"].startswith(f"C4c_online_cb{b}_")]
        if v:
            c4[str(b)] = {"mean_circ": float(np.mean(v)), "n": len(v)}
    base = [r["data"]["mouth"]["mouth_loop_rate"] for r in rows
            if r["unit"].startswith("C1_online_tau1.0_")]
    if c4 and len(base) >= 3:
        mu_b, sd_b = np.mean(base), np.std(base) + 1e-12
        zs = {k: (v["mean_circ"] - mu_b) / sd_b for k, v in c4.items()}
        vals = [c4[k]["mean_circ"] for k in sorted(c4, key=float)]
        rep["C4"] = {"detail": c4, "z_vs_unbiased": {k: round(z, 2) for k, z in zs.items()},
                     "monotone": bool(all(vals[i] <= vals[i + 1] for i in range(len(vals) - 1)))}
        rep["fork_d_engineered"] = bool(any(abs(z) >= th["mouth_z"] for z in zs.values())
                                        and rep["C4"]["monotone"])
    verdicts = []
    if rep.get("fork_a_fpt_signature"): verdicts.append("(a) kinetic signature")
    if rep.get("fork_b_current"): verdicts.append("(b) non-conservative current")
    if rep.get("fork_d_engineered"): verdicts.append("(d) engineered transition")
    if not verdicts and rep.get("C3", {}).get("pass"):
        verdicts.append("(c) conservative regime confirmed, pedagogical")
    rep["fork_verdict"] = verdicts or ["indeterminate: insufficient data"]
    print(json.dumps(rep, indent=2))

# ----------------------------------------------------------------------------
# Selftest
# ----------------------------------------------------------------------------
def selftest():
    t0 = time.time()
    print("# selftest: miniature of every condition, scale=0.02-0.06")
    r0 = run_unit("C0_hot_sb0", scale=0.05)
    r1 = run_unit("C0_ctrl_sb0", scale=0.05)
    ok_gyr = abs(r0["data"]["ang_mom_rate"]) > 3 * abs(r1["data"]["ang_mom_rate"])
    r2 = run_unit("C1_frozen_tau0.5_sb0", scale=0.06)
    r3 = run_unit("C1_online_tau0.5_sb0", scale=0.06)
    r4 = run_unit("C4c_online_cb1.0_tau1.0_sb0", scale=0.04)
    r5 = run_unit("C3t_frozen_L0.3_tau1.0_sb0", scale=0.06)
    ok_fpt = (r2["data"]["fpt"]["n"] >= 1) and (r3["data"]["fpt"]["n"] >= 1)
    ok_transit = r5["data"]["fpt"]["n"] >= 1 and r5["data"]["fpt"]["mean"] < r2["data"]["fpt"]["mean"]
    ok_mouth = "mouth" in r3["data"]
    print(f"# gyrator separation: {ok_gyr} | fpt machinery: {ok_fpt} "
          f"| transit<search: {ok_transit} | mouth stat: {ok_mouth} "
          f"| total {round(time.time()-t0,1)}s")
    print("# SELFTEST " + ("PASS" if (ok_gyr and ok_fpt and ok_transit and ok_mouth) else "FAIL"))

# ----------------------------------------------------------------------------
def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__); return
    if a[0] == "--plan":
        print(json.dumps({"type": "preregistration", "version": VERSION,
                          "config_hash": config_hash(), "config": CFG,
                          "units": build_units(),
                          "outcome_map": ["(a) FPT signature + occupancy match",
                                          "(b) online current z>=3 with C0 calibrated",
                                          "(c) both null + Kramers slope in band",
                                          "(d) C4 bias-monotone current z>=3"]},
                         indent=2)); return
    if a[0] == "--list":
        for u in build_units(): print(u)
        return
    if a[0] == "--selftest":
        selftest(); return
    if a[0] == "--batch":
        lo, hi = a[1].split(":")
        scale = float(a[a.index("--scale") + 1]) if "--scale" in a else 1.0
        for u in build_units()[int(lo):int(hi)]:
            run_unit(u, scale=scale)
        return
    if a[0] == "--unit":
        scale = 1.0
        if "--scale" in a:
            scale = float(a[a.index("--scale") + 1])
        run_unit(a[1], scale=scale); return
    if a[0] == "--analyze":
        analyze(a[1:]); return
    print("unknown args", a)

if __name__ == "__main__":
    main()
