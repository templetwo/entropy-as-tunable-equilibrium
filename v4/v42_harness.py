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

VERSION = "v4h-1.2.0"
import platform as _plat
SOURCE_SHA = hashlib.sha256(open(__file__, "rb").read()).hexdigest()[:16]
PYVER = _plat.python_version()

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
        "matched_tau": 0.25,
        "matched_M": 256, "matched_blocks": 16,
        "m_sweep": [64, 128], "sweep_blocks": 8,
        "cache_ctrl": 20, "ctrl_blocks": 8,
        "grid_ctrl_M": 96,
        "K_powered": 100, "K_small": 50,
        "c3_channel_lengths": [0.15, 0.30, 0.60, 1.20],
        "c3_tau": 1.0, "c3_blocks": 4,
        "c4v_kappas": [0.0, 2.0, 4.0, 8.0], "c4v_blocks": 16, "c4v_tau": 1.0,
        "c0_blocks": ["sb0", "sb1", "sb2", "sb3"],
    },
    "thresholds": {
        "ks_alpha": 0.01,
        "occ_gate_min_p": 0.05,      # occupancy must EXCEED this (a real p-value)
        "quad_z": 3.0,
        "sign_consistency": 12,      # of 16 blocks
        "kramers_slope": [1.7, 2.3], # on effective length L+0.2, raw block means
        "vortex_alpha": 0.01,        # Holm across {k4 vs k0, k8 vs k0}
        "rough_alpha": 0.01,         # one-sided slope of shift vs log(1/M)
        "n_perm": 20000,
    },
    "vortex": {"center": [2.0, 1.0], "sigma": [0.40, 0.30]},
    "roi": {"center": [2.0, 1.0], "half": [0.45, 0.45], "cells": 6},
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

def frozen_grid(geom, tau, rng, M=None):
    """Precompute S_c on a grid; return (S, xs, ys). Conservative by construction."""
    e = CFG["entropy"]
    xs = np.linspace(0.05, geom.Lx - 0.05, e["grid_nx"])
    ys = np.linspace(0.05, geom.Ly - 0.05, e["grid_ny"])
    S = np.full((e["grid_nx"], e["grid_ny"]), np.nan)
    for i, x in enumerate(xs):
        for j, y in enumerate(ys):
            if geom.blocked(np.array([[x, y]]))[0]:
                continue
            S[i, j] = endpoint_entropy(geom, (x, y), tau, (M if M is not None else e["M_grid"]), rng,
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

class QuadrantLoop:
    """v4.2 closed-loop statistic: winding angle about the mouth center,
    accumulated only inside the pre-declared ROI box. Robust to diffusive
    steps (no quadrant-skip failure mode). CCW positive.
    quad_loop_rate = accumulated angle / (2 pi * n_steps)."""
    def __init__(self, cx, cy, hx, hy):
        self.cx, self.cy, self.hx, self.hy = cx, cy, hx, hy
        self.th = None; self.total = 0.0
    def _inside(self, x, y):
        return abs(x - self.cx) <= self.hx and abs(y - self.cy) <= self.hy
    def add(self, r):
        x, y = r[0], r[1]
        if not self._inside(x, y):
            self.th = None; return
        th = math.atan2(y - self.cy, x - self.cx)
        if self.th is not None:
            d = th - self.th
            if d > math.pi: d -= 2 * math.pi
            elif d < -math.pi: d += 2 * math.pi
            self.total += d
        self.th = th
    def stats(self, n_steps):
        two_pi = 2 * math.pi
        return {"quad_loops": int(self.total / two_pi),
                "quad_loop_rate": self.total / (two_pi * max(n_steps, 1)),
                "quad_angle": round(self.total, 6)}

class ROIJ:
    """Coarse current field restricted to the mouth ROI, with integrated curl."""
    def __init__(self, cx, cy, hx, hy, n=6):
        self.cx, self.cy, self.hx, self.hy, self.n = cx, cy, hx, hy, n
        self.Jx = np.zeros((n, n)); self.Jy = np.zeros((n, n))
    def add(self, r_old, r_new):
        mx, my = 0.5 * (r_old[0] + r_new[0]), 0.5 * (r_old[1] + r_new[1])
        if abs(mx - self.cx) > self.hx or abs(my - self.cy) > self.hy: return
        i = min(int((mx - self.cx + self.hx) / (2 * self.hx) * self.n), self.n - 1)
        j = min(int((my - self.cy + self.hy) / (2 * self.hy) * self.n), self.n - 1)
        self.Jx[i, j] += r_new[0] - r_old[0]; self.Jy[i, j] += r_new[1] - r_old[1]
    def stats(self, n_steps):
        omega = 0.0
        for i in range(self.n - 1):
            for j in range(self.n - 1):
                omega += (self.Jy[i + 1, j] - self.Jy[i, j]) - (self.Jx[i, j + 1] - self.Jx[i, j])
        s = max(n_steps, 1)
        return {"omega_roi": omega / s,
                "Jx": [[round(v / s, 9) for v in row] for row in self.Jx.tolist()],
                "Jy": [[round(v / s, 9) for v in row] for row in self.Jy.tolist()]}

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
                curl_bias=0.0, M_grid_ov=None, M_online_ov=None, cache_ov=None,
                vortex_kappa=0.0):
    """mode: 'frozen' | 'online'. Returns FPT + occupancy + current stats."""
    b = CFG["box"]; f = CFG["fpt"]; e = CFG["entropy"]; dyn = CFG["dyn"]
    geom = Geom(b["Lx"], b["Ly"], ch_w if ch_w else b["wall_t"], b["ch_w_default"])
    rng = np.random.default_rng(seed)
    S = xs = ys = None
    if mode == "frozen":
        S, xs, ys = frozen_grid(geom, tau, rng, M=M_grid_ov)
    dt = dyn["dt"]; sig = math.sqrt(2 * CFG["bath"]["D"] * dt)
    start = np.array([b["Lx"] * f["start_frac"][0], b["Ly"] * f["start_frac"][1]])
    target_x = geom.wx1 + f["target_margin"]
    pos = start.copy(); t_run = 0.0; t_launch = 0.0
    fpt = FPTAcc(); occ = np.zeros(CFG["occupancy"]["bins_x"], dtype=int)
    cur = CurrentAcc(geom, CFG["current"]["cells_x"], CFG["current"]["cells_y"])
    mouth = MouthFlux(geom)
    _roi = CFG["roi"]
    quad = QuadrantLoop(_roi["center"][0], _roi["center"][1], _roi["half"][0], _roi["half"][1])
    roij = ROIJ(_roi["center"][0], _roi["center"][1], _roi["half"][0], _roi["half"][1], _roi["cells"])
    n_cache = cache_ov if cache_ov is not None else dyn["n_force_cache"]
    Fcache = np.zeros(2); k_since = n_cache
    in_channel = False; t_enter = 0.0
    K_target = max(3, int(f["K_target"] * scale)); T_max = f["T_max"] * scale
    n_force_evals = 0
    _v = CFG["vortex"]; vcx, vcy = _v["center"]; vsx, vsy = _v["sigma"]
    while len(fpt.times) < K_target and t_run < T_max:
        if k_since >= n_cache:
            if mode == "frozen":
                Fcache = force_frozen(geom, S, xs, ys, pos)
            else:
                Fcache = force_online(geom, pos, tau, rng,
                                      (M_online_ov if M_online_ov is not None else e["M_online"]), bias=bias,
                                      curl_bias=curl_bias)
                n_force_evals += 1
            k_since = 0
        noise = rng.standard_normal(2) * sig
        if vortex_kappa != 0.0:
            dxv = pos[0] - vcx; dyv = pos[1] - vcy
            env = math.exp(-(dxv*dxv/(2*vsx*vsx) + dyv*dyv/(2*vsy*vsy)))
            Fv = vortex_kappa * env * np.array([-dyv, dxv])
        else:
            Fv = 0.0
        new = step_reflect(geom, pos[None, :].copy(), (Fcache + Fv) * dt, noise[None, :])[0]
        cur.add(pos, new)
        mouth.add(pos, new)
        quad.add(new)
        roij.add(pos, new)
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
                Fcache = np.zeros(2); k_since = n_cache  # regenerative reset (v4.2 audit fix)
        else:
            if pos[0] >= target_x:
                fpt.add(t_run - t_launch)
                pos = start.copy(); t_launch = t_run
                Fcache = np.zeros(2); k_since = n_cache  # regenerative reset (v4.2 audit fix)
    return {"fpt": fpt.summary(), "occupancy_x": occ.tolist(),
            "current": cur.circulation_stats(),
            "mouth": mouth.stats(cur.n_steps),
            "quad": quad.stats(cur.n_steps),
            "roij": roij.stats(cur.n_steps),
            "censored": bool(len(fpt.times) < K_target),
            "t_total": round(t_run, 1), "n_force_evals": n_force_evals}

# ----------------------------------------------------------------------------
# Unit registry
# ----------------------------------------------------------------------------
def build_units():
    sw = CFG["sweeps"]; units = []
    t = sw["matched_tau"]; M = sw["matched_M"]
    for v in ["hot", "ctrl"]:
        for sb in sw["c0_blocks"]:
            units.append(f"C0_{v}_{sb}")
    for sb in range(sw["matched_blocks"]):
        units.append(f"C1m_frozen_M{M}_tau{t}_sb{sb}")
    for sb in range(sw["matched_blocks"]):
        units.append(f"C1m_online_M{M}_c1_tau{t}_sb{sb}")
    for Ms in sw["m_sweep"]:
        for sb in range(sw["sweep_blocks"]):
            units.append(f"C1s_online_M{Ms}_c1_tau{t}_sb{sb}")
    for sb in range(sw["ctrl_blocks"]):
        units.append(f"C1c_online_M{M}_c{sw['cache_ctrl']}_tau{t}_sb{sb}")
    for sb in range(sw["ctrl_blocks"]):
        units.append(f"C1g_frozen_M{sw['grid_ctrl_M']}_tau{t}_sb{sb}")
    for L in sw["c3_channel_lengths"]:
        for sb in range(sw["c3_blocks"]):
            units.append(f"C3e_frozen_L{L}_tau{sw['c3_tau']}_sb{sb}")
    for k in sw["c4v_kappas"]:
        for sb in range(sw["c4v_blocks"]):
            units.append(f"C4v_frozen_k{k}_tau{sw['c4v_tau']}_sb{sb}")
    return units

def run_unit(unit_id, scale=1.0):
    t0 = time.time()
    seed = unit_seed(unit_id)
    parts = unit_id.split("_")
    sw = CFG["sweeps"]
    kpow = scale * sw["K_powered"] / CFG["fpt"]["K_target"]
    if parts[0] == "C0":
        res = run_gyrator(parts[1], seed, scale=scale)
    elif parts[0] == "C1m" and parts[1] == "frozen":
        tau = float(parts[3][3:])
        res = run_chamber("frozen", tau, seed, scale=kpow,
                          M_grid_ov=int(parts[2][1:]))
    elif parts[0] == "C1m" and parts[1] == "online":
        tau = float(parts[4][3:])
        res = run_chamber("online", tau, seed, scale=kpow,
                          M_online_ov=int(parts[2][1:]), cache_ov=int(parts[3][1:]))
    elif parts[0] == "C1s":
        tau = float(parts[4][3:])
        res = run_chamber("online", tau, seed, scale=kpow,
                          M_online_ov=int(parts[2][1:]), cache_ov=int(parts[3][1:]))
    elif parts[0] == "C1c":
        tau = float(parts[4][3:])
        res = run_chamber("online", tau, seed, scale=kpow,
                          M_online_ov=int(parts[2][1:]), cache_ov=int(parts[3][1:]))
    elif parts[0] == "C1g":
        tau = float(parts[3][3:])
        res = run_chamber("frozen", tau, seed, scale=kpow,
                          M_grid_ov=int(parts[2][1:]))
    elif parts[0] == "C3e":
        L = float(parts[2][1:]); tau = float(parts[3][3:])
        res = run_chamber("frozen", tau, seed, ch_w=L, scale=scale,
                          transit_clock=True)
    elif parts[0] == "C4v":
        k = float(parts[2][1:]); tau = float(parts[3][3:])
        res = run_chamber("frozen", tau, seed, scale=scale, vortex_kappa=k)
    else:
        raise ValueError("unknown unit: " + unit_id)
    out = {"type": "result", "unit": unit_id, "seed": seed,
           "config_hash": config_hash(), "version": VERSION,
           "numpy": np.__version__, "python": PYVER, "source_sha": SOURCE_SHA, "scale": scale,
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

def analyze(args):
    th = CFG["thresholds"]; sw = CFG["sweeps"]
    rows = {}
    for line in open(args[0]):
        if line.strip().startswith("{"):
            d = json.loads(line)
            if d.get("type") == "result":
                rows[d["unit"]] = d
    rep = {"version": VERSION, "config_hash": config_hash(),
           "n_units": len(rows)}
    t = sw["matched_tau"]; M = sw["matched_M"]
    hot = [abs(rows[f"C0_hot_sb{i}"]["data"]["ang_mom_rate"]) for i in range(4)]
    ctl = [abs(rows[f"C0_ctrl_sb{i}"]["data"]["ang_mom_rate"]) for i in range(4)]
    rep["C0"] = {"hot_mean": float(np.mean(hot)), "ctrl_mean": float(np.mean(ctl)),
                 "ratio": float(np.mean(hot) / (np.mean(ctl) + 1e-12))}
    def times(uid): return np.array(rows[uid]["data"]["fpt"]["times"])
    def occv(uid):
        v = np.array(rows[uid]["data"]["occupancy_x"], float); return v / v.sum()
    F = [times(f"C1m_frozen_M{M}_tau{t}_sb{i}") for i in range(16)]
    O = [times(f"C1m_online_M{M}_c1_tau{t}_sb{i}") for i in range(16)]
    allt = np.sort(np.concatenate(F + O))
    grid = allt[np.linspace(0, len(allt) - 1, 400).astype(int)]
    E = np.array([np.searchsorted(np.sort(x), grid, side="right") / len(x) for x in (F + O)])
    obs = float(np.max(np.abs(E[:16].mean(0) - E[16:].mean(0))))
    rng = np.random.default_rng(123); ex = 0
    for _ in range(th["n_perm"]):
        pm = rng.permutation(32)
        if float(np.max(np.abs(E[pm[:16]].mean(0) - E[pm[16:]].mean(0)))) >= obs:
            ex += 1
    p_ks = (ex + 1) / (th["n_perm"] + 1)
    OF = [occv(f"C1m_frozen_M{M}_tau{t}_sb{i}") for i in range(16)]
    OO = [occv(f"C1m_online_M{M}_c1_tau{t}_sb{i}") for i in range(16)]
    p_occ = block_perm_p(OF, OO, occ_chi2_stat)
    tv = float(0.5 * np.abs(np.mean(OF, 0) - np.mean(OO, 0)).sum())
    fm = [x.mean() for x in F]; om = [x.mean() for x in O]
    g = float((np.mean(om) - np.mean(fm)) /
              math.sqrt((np.var(fm, ddof=1) + np.var(om, ddof=1)) / 2))
    rep["matched"] = {"ks": obs, "p_ks": p_ks, "shift": float(np.mean(om) - np.mean(fm)),
                      "g": g, "p_occ": p_occ, "tv": tv}
    rep["fork_a_clean"] = bool(p_ks < th["ks_alpha"] and p_occ > th["occ_gate_min_p"])
    rep["confound_persists"] = bool(p_ks < th["ks_alpha"] and p_occ <= th["occ_gate_min_p"])
    qf = [rows[f"C1m_frozen_M{M}_tau{t}_sb{i}"]["data"]["quad"]["quad_loop_rate"] for i in range(16)]
    qo = [rows[f"C1m_online_M{M}_c1_tau{t}_sb{i}"]["data"]["quad"]["quad_loop_rate"] for i in range(16)]
    z2 = float((np.mean(qo) - np.mean(qf)) /
               math.sqrt(np.var(qo, ddof=1) / 16 + np.var(qf, ddof=1) / 16 + 1e-30))
    p_q = block_perm_p([[v] for v in qf], [[v] for v in qo],
                       lambda A, B: abs(np.mean([b[0] for b in B]) - np.mean([a[0] for a in A])))
    pos = sum(1 for v in qo if v > 0); neg = 16 - pos
    rep["current"] = {"z2": z2, "p_perm": p_q, "sign_consistency": int(max(pos, neg))}
    rep["fork_b"] = bool(abs(z2) >= th["quad_z"] and p_q < th["ks_alpha"]
                         and max(pos, neg) >= th["sign_consistency"])
    vk = {}
    for k in sw["c4v_kappas"]:
        vk[k] = [rows[f"C4v_frozen_k{k}_tau{sw['c4v_tau']}_sb{i}"]["data"]["quad"]["quad_loop_rate"]
                 for i in range(sw["c4v_blocks"])]
    means = {k: float(np.mean(vk[k])) for k in vk}
    mono = all(means[a] <= means[b] + 1e-12 for a, b in
               zip(sw["c4v_kappas"][:-1], sw["c4v_kappas"][1:]))
    def one_sided(base, arm):
        return block_perm_p([[v] for v in base], [[v] for v in arm],
                            lambda A, B: np.mean([b[0] for b in B]) - np.mean([a[0] for a in A]),
                            one_sided=True)
    p4 = one_sided(vk[0.0], vk[4.0]); p8 = one_sided(vk[0.0], vk[8.0])
    p2 = one_sided(vk[0.0], vk[2.0])
    h48 = holm([p4, p8])
    sc4 = sum(1 for v in vk[4.0] if v > 0); sc8 = sum(1 for v in vk[8.0] if v > 0)
    rep["vortex"] = {"means": {str(k): means[k] for k in means},
                     "p_k2_vs_k0": p2, "p_k4_vs_k0": p4, "p_k8_vs_k0": p8,
                     "holm_k4_k8": h48, "sign_pos_k4": sc4, "sign_pos_k8": sc8,
                     "monotone": bool(mono)}
    rep["vortex_control_pass"] = bool(mono and max(h48) < th["vortex_alpha"]
                                      and sc4 >= th["sign_consistency"]
                                      and sc8 >= th["sign_consistency"])
    base_f = float(np.mean(fm))
    xs, ys = [], []
    for Ms, uids in [(64, [f"C1s_online_M64_c1_tau{t}_sb{i}" for i in range(8)]),
                     (128, [f"C1s_online_M128_c1_tau{t}_sb{i}" for i in range(8)]),
                     (256, [f"C1m_online_M{M}_c1_tau{t}_sb{i}" for i in range(16)])]:
        for u in uids:
            xs.append(math.log(1.0 / Ms)); ys.append(times(u).mean() - base_f)
    xs = np.array(xs); ys = np.array(ys)
    slope = float(np.polyfit(xs, ys, 1)[0])
    rng2 = np.random.default_rng(321); ex2 = 0
    for _ in range(th["n_perm"]):
        yp = rng2.permutation(ys)
        if float(np.polyfit(xs, yp, 1)[0]) >= slope:
            ex2 += 1
    p_rough = (ex2 + 1) / (th["n_perm"] + 1)
    rep["roughness"] = {"slope_vs_log_invM": slope, "p_one_sided": p_rough}
    rep["roughness_pass"] = bool(slope > 0 and p_rough < th["rough_alpha"])
    Ls = sw["c3_channel_lengths"]
    Tm = [float(np.mean([rows[f"C3e_frozen_L{L}_tau{sw['c3_tau']}_sb{i}"]["data"]["fpt"]["mean"]
                          for i in range(sw["c3_blocks"])])) for L in Ls]
    sl = float(np.polyfit(np.log(np.array(Ls) + 0.2), np.log(Tm), 1)[0])
    lo, hi = th["kramers_slope"]
    rep["C3e"] = {"slope_effective": sl, "points": list(zip(Ls, Tm)),
                  "in_band": bool(lo <= sl <= hi)}
    print(json.dumps(rep, indent=1))

def occ_chi2_stat(A, B):
    pa = np.mean(A, axis=0); pb = np.mean(B, axis=0)
    return float(np.sum((pa - pb) ** 2 / (pa + pb + 1e-12)))

def block_perm_p(A, B, stat, n_perm=None, seed=123, one_sided=False):
    import random as _rnd
    n_perm = n_perm or CFG["thresholds"]["n_perm"]
    allb = list(A) + list(B); nf = len(A)
    obs = stat(A, B); r = _rnd.Random(seed); ex = 0
    idx = list(range(len(allb)))
    for _ in range(n_perm):
        pm = r.sample(idx, nf); s = set(pm)
        v = stat([allb[i] for i in pm], [allb[i] for i in idx if i not in s])
        if (v >= obs) if not one_sided else (v >= obs):
            ex += 1
    return (ex + 1) / (n_perm + 1)

def holm(ps):
    ps = list(ps); m = len(ps)
    order = list(np.argsort(ps)); out = [0.0] * m; run = 0.0
    for r, i in enumerate(order):
        run = max(run, min(1.0, (m - r) * ps[i])); out[i] = run
    return out

def selftest():
    t0 = time.time()
    r0h = run_unit("C0_hot_sb0", scale=0.05); r0c = run_unit("C0_ctrl_sb0", scale=0.05)
    print(json.dumps(r0h, separators=(",", ":"))); print(json.dumps(r0c, separators=(",", ":")))
    ok_gyr = abs(r0h["data"]["ang_mom_rate"]) > 3 * abs(r0c["data"]["ang_mom_rate"])
    r2 = run_unit("C1m_frozen_M256_tau0.25_sb0", scale=0.06)
    r3 = run_unit("C1m_online_M256_c1_tau0.25_sb0", scale=0.06)
    print(json.dumps(r2, separators=(",", ":"))); print(json.dumps(r3, separators=(",", ":")))
    ok_fpt = (r2["data"]["fpt"]["n"] >= 1) and (r3["data"]["fpt"]["n"] >= 1)
    r5 = run_unit("C3e_frozen_L0.3_tau1.0_sb0", scale=0.06)
    ok_transit = r5["data"]["fpt"]["n"] >= 1 and r5["data"]["fpt"]["mean"] < r2["data"]["fpt"]["mean"]
    ok_fields = all(k in r3["data"] for k in ("quad", "roij", "mouth"))
    q = QuadrantLoop(2.0, 1.0, 0.45, 0.45)
    for i in range(0, 401):
        th = 2 * math.pi * i / 100.0
        q.add((2.0 + 0.3 * math.cos(th), 1.0 + 0.3 * math.sin(th)))
    qs = q.stats(400)
    ok_quadsynth = abs(qs["quad_angle"] - 8 * math.pi) < 1e-6
    rv = run_chamber("frozen", 1.0, seed=12345, scale=0.4, vortex_kappa=8.0)
    ok_vortex = rv["quad"]["quad_angle"] > 0
    print(f"# vortex mini: quad_loops={rv['quad']['quad_loops']} "
          f"omega_roi={rv['roij']['omega_roi']:.3e}")
    rng = np.random.default_rng(7)
    base = np.ones(24) / 24
    null_A = [rng.multinomial(4000, base) / 4000 for _ in range(8)]
    null_B = [rng.multinomial(4000, base) / 4000 for _ in range(8)]
    tilt = base * (1 + 0.15 * np.linspace(-1, 1, 24)); tilt = tilt / tilt.sum()
    shift_B = [rng.multinomial(4000, tilt) / 4000 for _ in range(8)]
    p_null = block_perm_p(null_A, null_B, occ_chi2_stat, n_perm=2000, seed=5)
    p_shift = block_perm_p(null_A, shift_B, occ_chi2_stat, n_perm=2000, seed=5)
    ok_gate = (p_null > CFG["thresholds"]["occ_gate_min_p"]) and (p_shift < 0.01)
    print(f"# gate-can-fail: null p={p_null:.3f} (must pass) | shifted p={p_shift:.4f} (must fail)")
    allok = ok_gyr and ok_fpt and ok_transit and ok_fields and ok_quadsynth and ok_vortex and ok_gate
    print(f"# gyr:{ok_gyr} fpt:{ok_fpt} transit<search:{ok_transit} fields:{ok_fields} "
          f"quad_synth:{ok_quadsynth} vortex_sign:{ok_vortex} gate_can_fail:{ok_gate} "
          f"| {round(time.time()-t0,1)}s")
    print("# SELFTEST " + ("PASS" if allok else "FAIL"))

def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__); return
    if a[0] == "--plan":
        print(json.dumps({"type": "preregistration", "source_sha_at_registration": SOURCE_SHA, "version": VERSION,
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
