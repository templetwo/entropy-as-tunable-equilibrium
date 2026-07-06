#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v4.3 Harness, version v4h-1.3.0
Temple of Two / Anthony J. Vasquez Sr. entropy-as-tunable-equilibrium program.

POWERED VORTEX CONTROL + FIRST ANISOTROPIC-HORIZON ENGINE TEST.

Two registered questions, with an explicit dependency:
  G1 (instrument): the v4.2 vortex positive control had 8%/25% power at its
      registered gate (measured post hoc from the canonical block variance).
      v4.3 re-runs it POWERED: 10x unit length (rate-statistic variance falls
      as 1/n_steps) and 32 blocks/arm. Projected power >99% (k8), ~99% (k4).
  G2 (engine): the v4.2 structural result fences every scalar-gradient
      estimator into conservativity. The minimal exit from that class is a
      PER-COORDINATE horizon: F = (Tc dS_c(.;tau_x)/dx, Tc dS_c(.;tau_y)/dy).
      The components are gradients of DIFFERENT scalar fields, so
      curl F = Tc d2/dxdy [S_c(tau_y) - S_c(tau_x)]. Horizon dependence of
      S_c (v3's central finding) makes a nonzero anisotropic curl generically
      POSSIBLE; the selftest's field-smoke test verifies it is nonzero in the
      implemented geometry before any confirmatory unit is interpreted.
      Registered prediction: current appears, REVERSES SIGN under
      tau_x <-> tau_y (exact antisymmetry of the curl), and vanishes at
      tau_x == tau_y (which is precisely the v4.2 null).
      ORIENTATION CONVENTION (registered): positive = COUNTERCLOCKWISE, as
      implemented by QuadrantLoop's winding angle ("CCW positive"). Secondary
      directional prediction, derived BEFORE registration from the
      ROI-integrated curl of the mean aniso field (M=4000 grids, seeds
      77001/77002/77003, unanimous): arm (tau_x,tau_y)=(0.25,1.0) circulates
      CCW (+); the swapped arm (1.0,0.25) circulates CW (-). This is reported
      as a labeled secondary, NOT a gate condition; G2 gates on antisymmetry.
      SCOPE BOUNDARY (registered): a G2 pass establishes coherent circulation
      in the RESET-DEFINED TRANSPORT PROTOCOL of this harness. It does NOT
      establish a stationary NESS in a closed, no-reset system; that protocol
      belongs to the v4.4+ lineage and every result label must keep the
      distinction.
  DEPENDENCY (pre-declared): the G2 verdict is interpretable ONLY if G1
      passes in the same campaign. G1 fail -> campaign inconclusive on G2
      regardless of its numbers.

  Plus a powered occupancy re-test: v4.2 left the matched-arm occupancy at
  p = 0.048 with B=16/arm; v4.3 re-runs at B=32/arm under fresh seeds. Not
  gated as a fork; registered as a confirmatory re-test of the marginal.

FAMILIES:
  C0   Brownian gyrator calibration (unchanged, fresh seeds).
  C1m  matched arms frozen vs online, B=32/arm (occupancy re-test; FPT
       reported descriptively, NOT gated -- fork (a) was settled in v4.2).
  C4v  vortex positive control, kappa in {0,2,4,8}, B=32/arm, 10x length.
  C5a  anisotropic-horizon frozen force, pairs (tau_x, tau_y) in
       {(0.25,1.0), (1.0,0.25), (1.0,1.0)}, B=32/arm, 10x length.
       The equal-tau control computes TWO INDEPENDENT grids at tau=1.0 so
       its estimator-noise structure matches the mismatch arms; it doubles
       as the test that two-grid noise alone fakes no current.

DESIGN RULES CARRIED FORWARD, PLUS ONE NEW:
  - Every gate must be demonstrably capable of failing on null data
    (selftest, from v4.2).
  - NEW (the v4.2 lesson): every POSITIVE CONTROL must carry a power
    calculation showing >= 90% power at the registered alpha, computed from
    measured variance and executed in the selftest. A control that cannot
    pass is not a control.
  - Fresh seed namespace "v43::" -- no unit shares a seed with any prior
    campaign. Declared pilot units live in "v43pilot::" and are NEVER pooled
    into confirmatory analysis.

PRE-REGISTERED OUTCOME MAP:
  G1  C4v means monotone in kappa; Holm(p_k4, p_k8) < 0.01 (one-sided,
      block permutation); sign consistency >= 24/32 at k4 AND k8.
  G2  (requires G1) each mismatch arm vs equal-tau arm: Holm-corrected
      two-sided block-permutation p < 0.01 on quad_loop_rate; sign
      consistency >= 24/32 within each mismatch arm; AND the two mismatch
      arm means have OPPOSITE signs. Fire -> genuine steady current from a
      non-conservative causal-entropic force (engine demonstrated in the
      minimal extension class).
  G3  G1 passes, G2 does not -> bounded null: no anisotropic-horizon current
      at the design's detection floor (reported in analyze output).
  G4  G1 fails -> inconclusive on G2; instrument redesign required.
  OCC B=32 matched-arm occupancy: block-permutation p reported; matched if
      p > 0.05. Confirmatory re-test of the v4.2 marginal, not a fork gate.

USAGE:
  python v43_harness.py --plan          # pre-registration manifest (JSON)
  python v43_harness.py --list          # unit ids only
  python v43_harness.py --selftest      # miniature of everything + power calc
  python v43_harness.py --pilot         # declared pilot: 4 aniso blocks, sd + floor
  python v43_harness.py --unit UNIT_ID  # run one work unit
  python v43_harness.py --batch a:b     # run units [a:b)
  python v43_harness.py --analyze F.ndjson   # registered verdict
"""

import sys, json, math, time, hashlib, warnings
warnings.filterwarnings('ignore')
import numpy as np

VERSION = "v4h-1.3.1"
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
        "matched_M": 256, "matched_blocks": 32,
        "K_powered": 100, "K_small": 50,
        "c4v_kappas": [0.0, 2.0, 4.0, 8.0], "c4v_blocks": 32, "c4v_tau": 1.0,
        "c4v_scale": 10.0,           # 10x unit length: rate variance ~ 1/n_steps
        # aniso_blocks=64 set from the DECLARED PILOT (v43pilot::, 4 blocks):
        # measured block sd 3.84e-5 at 10x scale -> floor 3.7e-5 at B=32,
        # 2.6e-5 at B=64. Pilot mean -1.7e-5 (n.s.) is indistinguishable from
        # zero AND from a sub-3.7e-5 current, so the arms are doubled BEFORE
        # registration rather than discovered underpowered after (v4.2 lesson).
        "aniso_pairs": [[0.25, 1.0], [1.0, 0.25], [1.0, 1.0]],
        "aniso_blocks": 64, "aniso_scale": 10.0,
        "c0_blocks": ["sb0", "sb1", "sb2", "sb3"],
    },
    "thresholds": {
        "ks_alpha": 0.01,
        "occ_gate_min_p": 0.05,      # occupancy must EXCEED this (a real p-value)
        "sign_consistency": 24,      # of 32 blocks (C4v arms)
        "sign_consistency_aniso": 48,  # of 64 blocks (same 0.75 proportion)
        "vortex_alpha": 0.01,        # Holm across {k4 vs k0, k8 vs k0}
        "aniso_alpha": 0.01,         # Holm across the two mismatch contrasts
        "n_perm": 20000,
    },
    "power": {
        # Measured from the v4.2 canonical (sha256 3139ceb11c5c6572...):
        # per-block quad_loop_rate sd at scale=1, pooled across kappa arms,
        # and the observed vortex effect sizes. The selftest computes the
        # analytic power of the registered design from these and MUST show
        # >= power_target for both contrasts, or the design is rejected.
        "c4v_block_sd_scale1": 2.15e-4,
        "delta_k4": 9.355e-5,
        "delta_k8": 1.416e-4,
        "alpha_worst": 0.005,        # Holm worst case: 0.01 / 2
        "power_target": 0.90,
        # v4.2 canonical per-arm means, used by the COMPOUND gate-power
        # simulation (Holm + monotonicity + sign consistency, the exact G1
        # logic) executed in the selftest and preserved as an artifact.
        "c4v_means_v42": {"0.0": 3.217e-5, "2.0": 4.003e-5,
                          "4.0": 1.257e-4, "8.0": 1.738e-4},
    },
    "aniso_predicted": {
        # Secondary directional prediction, derived BEFORE registration.
        # NOT a gate condition; G2 gates on antisymmetry (opposite arm signs).
        "convention": "CCW positive (QuadrantLoop winding angle)",
        "arm1_pair": [0.25, 1.0], "arm1_sign": 1,
        "arm2_pair": [1.0, 0.25], "arm2_sign": -1,
        "derivation": "ROI-integrated curl of mean aniso force field, "
                      "M=4000 grids, seeds 77001/77002/77003, unanimous "
                      "(+5.67e-3, +1.54e-3, +9.27e-3); M=400 grids are NOT "
                      "sign-stable (documented), so the prediction rests on "
                      "the M=4000 mean-field estimate.",
    },
    "vortex": {"center": [2.0, 1.0], "sigma": [0.40, 0.30]},
    "roi": {"center": [2.0, 1.0], "half": [0.45, 0.45], "cells": 6},
}

def config_hash():
    s = json.dumps(CFG, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(s.encode()).hexdigest()[:16]

def unit_seed(unit_id):
    # v4.3 namespace: no unit shares a seed with any prior campaign
    h = hashlib.sha256(("v43::" + unit_id).encode()).digest()
    return int.from_bytes(h[:8], "big")

def pilot_seed(unit_id):
    # declared pilot namespace; pilot results are NEVER pooled into analysis
    h = hashlib.sha256(("v43pilot::" + unit_id).encode()).digest()
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

def force_frozen_aniso(geom, Sx, Sy, xs, ys, r):
    """Anisotropic-horizon causal-entropic force: the x-component is the
    gradient of S_c(.; tau_x), the y-component the gradient of S_c(.; tau_y).
    For tau_x != tau_y the components are gradients of DIFFERENT scalar
    fields, so the mean force has curl Tc d2/dxdy [S(tau_y) - S(tau_x)] != 0
    generically -- the minimal exit from the conservative estimator class
    fenced off by the v4.2 structural result."""
    e = CFG["entropy"]
    i = np.clip(np.searchsorted(xs, r[0]) - 1, 1, len(xs) - 2)
    j = np.clip(np.searchsorted(ys, r[1]) - 1, 1, len(ys) - 2)
    hx, hy = xs[1] - xs[0], ys[1] - ys[0]
    Fx = e["Tc"] * (Sx[i + 1, j] - Sx[i - 1, j]) / (2 * hx)
    Fy = e["Tc"] * (Sy[i, j + 1] - Sy[i, j - 1]) / (2 * hy)
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
                vortex_kappa=0.0, tau_y=None):
    """mode: 'frozen' | 'online'. Returns FPT + occupancy + current stats.
    tau_y: if set (frozen mode only), the y force component comes from an
    INDEPENDENTLY estimated S_c grid at horizon tau_y (anisotropic force).
    Two grids are computed even when tau_y == tau, so the equal-tau control
    carries the same estimator-noise structure as the mismatch arms."""
    b = CFG["box"]; f = CFG["fpt"]; e = CFG["entropy"]; dyn = CFG["dyn"]
    geom = Geom(b["Lx"], b["Ly"], ch_w if ch_w else b["wall_t"], b["ch_w_default"])
    rng = np.random.default_rng(seed)
    S = S2 = xs = ys = None
    if mode == "frozen":
        S, xs, ys = frozen_grid(geom, tau, rng, M=M_grid_ov)
        if tau_y is not None:
            S2, _, _ = frozen_grid(geom, tau_y, rng, M=M_grid_ov)
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
                if S2 is not None:
                    Fcache = force_frozen_aniso(geom, S, S2, xs, ys, pos)
                else:
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
    for k in sw["c4v_kappas"]:
        for sb in range(sw["c4v_blocks"]):
            units.append(f"C4v_frozen_k{k}_tau{sw['c4v_tau']}_sb{sb}")
    for tx, ty in sw["aniso_pairs"]:
        for sb in range(sw["aniso_blocks"]):
            units.append(f"C5a_frozen_tx{tx}_ty{ty}_sb{sb}")
    return units

def run_unit(unit_id, scale=1.0, seed_fn=None):
    t0 = time.time()
    seed = (seed_fn or unit_seed)(unit_id)
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
    elif parts[0] == "C4v":
        k = float(parts[2][1:]); tau = float(parts[3][3:])
        res = run_chamber("frozen", tau, seed, scale=scale * sw["c4v_scale"],
                          vortex_kappa=k)
    elif parts[0] == "C5a":
        tx = float(parts[2][2:]); ty = float(parts[3][2:])
        res = run_chamber("frozen", tx, seed, scale=scale * sw["aniso_scale"],
                          tau_y=ty)
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

def _inv_norm(p):
    from statistics import NormalDist
    return NormalDist().inv_cdf(p)

def _power_of_design(delta, sd_block, B, alpha):
    """Analytic normal-approx power of a one-sided two-sample block test."""
    from statistics import NormalDist
    se = sd_block * math.sqrt(2.0 / B)
    return 1.0 - NormalDist().cdf(_inv_norm(1 - alpha) - delta / se)

def _detection_floor(sd_block, B, alpha, power):
    """Smallest |delta| detectable at given alpha with given power."""
    return (_inv_norm(1 - alpha) + _inv_norm(power)) * sd_block * math.sqrt(2.0 / B)

def analyze(args):
    th = CFG["thresholds"]; sw = CFG["sweeps"]; pw = CFG["power"]
    rows = {}
    for line in open(args[0]):
        if line.strip().startswith("{"):
            d = json.loads(line)
            if d.get("type") == "result":
                rows[d["unit"]] = d
    rep = {"version": VERSION, "config_hash": config_hash(),
           "n_units": len(rows)}
    t = sw["matched_tau"]; M = sw["matched_M"]; B = sw["matched_blocks"]
    Bv = sw["c4v_blocks"]; Ba = sw["aniso_blocks"]
    hot = [abs(rows[f"C0_hot_sb{i}"]["data"]["ang_mom_rate"]) for i in range(4)]
    ctl = [abs(rows[f"C0_ctrl_sb{i}"]["data"]["ang_mom_rate"]) for i in range(4)]
    rep["C0"] = {"hot_mean": float(np.mean(hot)), "ctrl_mean": float(np.mean(ctl)),
                 "ratio": float(np.mean(hot) / (np.mean(ctl) + 1e-12))}
    def times(uid): return np.array(rows[uid]["data"]["fpt"]["times"])
    def occv(uid):
        v = np.array(rows[uid]["data"]["occupancy_x"], float); return v / v.sum()
    def quadr(uid): return rows[uid]["data"]["quad"]["quad_loop_rate"]
    # --- OCC: powered occupancy re-test (confirmatory re-test, not a fork) ---
    OF = [occv(f"C1m_frozen_M{M}_tau{t}_sb{i}") for i in range(B)]
    OO = [occv(f"C1m_online_M{M}_c1_tau{t}_sb{i}") for i in range(B)]
    p_occ = block_perm_p(OF, OO, occ_chi2_stat)
    tv = float(0.5 * np.abs(np.mean(OF, 0) - np.mean(OO, 0)).sum())
    rep["occupancy"] = {"p_occ": p_occ, "tv": tv, "blocks_per_arm": B,
                        "matched": bool(p_occ > th["occ_gate_min_p"])}
    # --- FPT matched arms: DESCRIPTIVE ONLY (fork (a) settled in v4.2) ---
    F = [times(f"C1m_frozen_M{M}_tau{t}_sb{i}") for i in range(B)]
    O = [times(f"C1m_online_M{M}_c1_tau{t}_sb{i}") for i in range(B)]
    fm = [x.mean() for x in F]; om = [x.mean() for x in O]
    g = float((np.mean(om) - np.mean(fm)) /
              math.sqrt((np.var(fm, ddof=1) + np.var(om, ddof=1)) / 2))
    rep["fpt_descriptive"] = {"shift": float(np.mean(om) - np.mean(fm)), "g": g,
                              "note": "not gated; fork (a) settled in v4.2"}
    # --- G1: powered vortex positive control ---
    vk = {}
    for k in sw["c4v_kappas"]:
        vk[k] = [quadr(f"C4v_frozen_k{k}_tau{sw['c4v_tau']}_sb{i}") for i in range(Bv)]
    means = {k: float(np.mean(vk[k])) for k in vk}
    # Monotonicity is gated on the POWERED arms only (k0 <= k4 <= k8): the
    # compound-gate power simulation showed that including k2 (true effect
    # ~0.7 block-SE) makes the gate a coin flip on true signal -- another
    # control-that-cannot-pass, caught by the power rule before registration.
    # k2 remains a descriptive dose point.
    mono = (means[0.0] <= means[4.0] + 1e-12) and (means[4.0] <= means[8.0] + 1e-12)
    def one_sided(base, arm):
        return block_perm_p([[v] for v in base], [[v] for v in arm],
                            lambda A, Bb: np.mean([b[0] for b in Bb]) - np.mean([a[0] for a in A]),
                            one_sided=True)
    p4 = one_sided(vk[0.0], vk[4.0]); p8 = one_sided(vk[0.0], vk[8.0])
    p2 = one_sided(vk[0.0], vk[2.0])
    h48 = holm([p4, p8])
    sc4 = sum(1 for v in vk[4.0] if v > 0); sc8 = sum(1 for v in vk[8.0] if v > 0)
    rep["vortex"] = {"means": {str(k): means[k] for k in means},
                     "p_k2_vs_k0": p2, "p_k4_vs_k0": p4, "p_k8_vs_k0": p8,
                     "holm_k4_k8": h48, "sign_pos_k4": sc4, "sign_pos_k8": sc8,
                     "monotone": bool(mono), "blocks_per_arm": Bv}
    G1 = bool(mono and max(h48) < th["vortex_alpha"]
              and sc4 >= th["sign_consistency"] and sc8 >= th["sign_consistency"])
    rep["G1_control_pass"] = G1
    # --- G2: anisotropic-horizon engine test ---
    (txa, tya), (txb, tyb), (txe, tye) = sw["aniso_pairs"]
    A1 = [quadr(f"C5a_frozen_tx{txa}_ty{tya}_sb{i}") for i in range(Ba)]
    A2 = [quadr(f"C5a_frozen_tx{txb}_ty{tyb}_sb{i}") for i in range(Ba)]
    EQ = [quadr(f"C5a_frozen_tx{txe}_ty{tye}_sb{i}") for i in range(Ba)]
    def two_sided(base, arm):
        return block_perm_p([[v] for v in base], [[v] for v in arm],
                            lambda A, Bb: abs(np.mean([b[0] for b in Bb]) - np.mean([a[0] for a in A])))
    pa1 = two_sided(EQ, A1); pa2 = two_sided(EQ, A2)
    ha = holm([pa1, pa2])
    m1, m2, me = float(np.mean(A1)), float(np.mean(A2)), float(np.mean(EQ))
    s1 = max(sum(1 for v in A1 if v > 0), sum(1 for v in A1 if v < 0))
    s2 = max(sum(1 for v in A2 if v > 0), sum(1 for v in A2 if v < 0))
    opposite = bool((m1 - me) * (m2 - me) < 0)
    # detection floor from the MEASURED equal-arm block sd in this run
    sd_eq = float(np.std(EQ, ddof=1))
    floor = _detection_floor(sd_eq, Ba, pw["alpha_worst"], pw["power_target"])
    pred = CFG["aniso_predicted"]
    dir_match_1 = bool((m1 - me) * pred["arm1_sign"] > 0)
    dir_match_2 = bool((m2 - me) * pred["arm2_sign"] > 0)
    rep["aniso"] = {"arm1": {"pair": [txa, tya], "mean": m1, "p_vs_eq": pa1, "sign_consistency": int(s1)},
                    "arm2": {"pair": [txb, tyb], "mean": m2, "p_vs_eq": pa2, "sign_consistency": int(s2)},
                    "equal": {"pair": [txe, tye], "mean": me, "sd_block": sd_eq},
                    "holm": ha, "opposite_signs": opposite,
                    "directional_secondary": {"predicted": [pred["arm1_sign"], pred["arm2_sign"]],
                                              "matched": [dir_match_1, dir_match_2],
                                              "note": "secondary prediction, not gating"},
                    "detection_floor_90pct": floor, "blocks_per_arm": Ba}
    G2 = bool(G1 and max(ha) < th["aniso_alpha"]
              and s1 >= th["sign_consistency_aniso"] and s2 >= th["sign_consistency_aniso"]
              and opposite)
    rep["G2_aniso_fire"] = G2
    rep["G3_bounded_null"] = bool(G1 and not G2)
    rep["G4_inconclusive"] = bool(not G1)
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
    th_cfg = CFG["thresholds"]; sw = CFG["sweeps"]; pw = CFG["power"]
    # scale 0.25 (500k steps): the 0.05 mini was flaky under fresh v43 seeds
    r0h = run_unit("C0_hot_sb0", scale=0.25); r0c = run_unit("C0_ctrl_sb0", scale=0.25)
    ok_gyr = abs(r0h["data"]["ang_mom_rate"]) > 3 * abs(r0c["data"]["ang_mom_rate"])
    r2 = run_unit("C1m_frozen_M256_tau0.25_sb0", scale=0.06)
    r3 = run_unit("C1m_online_M256_c1_tau0.25_sb0", scale=0.06)
    ok_fpt = (r2["data"]["fpt"]["n"] >= 1) and (r3["data"]["fpt"]["n"] >= 1)
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
    # gate-can-fail (occupancy), carried from v4.2
    rng = np.random.default_rng(7)
    base = np.ones(24) / 24
    null_A = [rng.multinomial(4000, base) / 4000 for _ in range(8)]
    null_B = [rng.multinomial(4000, base) / 4000 for _ in range(8)]
    tilt = base * (1 + 0.15 * np.linspace(-1, 1, 24)); tilt = tilt / tilt.sum()
    shift_B = [rng.multinomial(4000, tilt) / 4000 for _ in range(8)]
    p_null = block_perm_p(null_A, null_B, occ_chi2_stat, n_perm=2000, seed=5)
    p_shift = block_perm_p(null_A, shift_B, occ_chi2_stat, n_perm=2000, seed=5)
    ok_gate = (p_null > th_cfg["occ_gate_min_p"]) and (p_shift < 0.01)
    print(f"# gate-can-fail(occ): null p={p_null:.3f} (must pass) | shifted p={p_shift:.4f} (must fail)")
    # NEW (v4.3): positive-control power check. The registered design must
    # give >= power_target on BOTH vortex contrasts, using the v4.2-measured
    # block sd scaled by 1/sqrt(c4v_scale) (rate variance ~ 1/n_steps).
    sd10 = pw["c4v_block_sd_scale1"] / math.sqrt(sw["c4v_scale"])
    pow4 = _power_of_design(pw["delta_k4"], sd10, sw["c4v_blocks"], pw["alpha_worst"])
    pow8 = _power_of_design(pw["delta_k8"], sd10, sw["c4v_blocks"], pw["alpha_worst"])
    floor = _detection_floor(sd10, sw["aniso_blocks"], pw["alpha_worst"], pw["power_target"])
    print(f"# power(analytic, per-contrast): k4={pow4:.4f} k8={pow8:.4f} "
          f"| projected aniso floor ~{floor:.2e}")
    # COMPOUND gate power: Monte Carlo of the EXACT G1 logic (monotone means
    # + Holm-corrected one-sided block permutations + sign consistency),
    # synthetic normal blocks at the v4.2-measured arm means and the scaled
    # sd. This is the power of the gate as registered, not of a bare t-test.
    mu = {float(k): v for k, v in pw["c4v_means_v42"].items()}
    kap = sw["c4v_kappas"]; Bv = sw["c4v_blocks"]
    rngP = np.random.default_rng(2026)
    n_sim = 200; hits = 0
    for s in range(n_sim):
        vk = {k: list(rngP.normal(mu[k], sd10, Bv)) for k in kap}
        mns = {k: np.mean(vk[k]) for k in kap}
        mono = (mns[0.0] <= mns[4.0] + 1e-12) and (mns[4.0] <= mns[8.0] + 1e-12)
        if not mono:
            continue
        def osided(base, arm, sd_):
            return block_perm_p([[v] for v in base], [[v] for v in arm],
                                lambda A, Bb: np.mean([x[0] for x in Bb]) - np.mean([x[0] for x in A]),
                                n_perm=1000, seed=1000 + s)
        h = holm([osided(vk[0.0], vk[4.0], sd10), osided(vk[0.0], vk[8.0], sd10)])
        sc4s = sum(1 for v in vk[4.0] if v > 0); sc8s = sum(1 for v in vk[8.0] if v > 0)
        if (max(h) < th_cfg["vortex_alpha"] and sc4s >= th_cfg["sign_consistency"]
                and sc8s >= th_cfg["sign_consistency"]):
            hits += 1
    compound_power = hits / n_sim
    ok_power = compound_power >= pw["power_target"]
    print(f"# power(COMPOUND G1 gate, n_sim={n_sim}): {compound_power:.3f} "
          f"(target {pw['power_target']}) -- preserve this line as the artifact")
    # NEW (v4.3): aniso equal-grid consistency -- with the SAME grid passed
    # twice, the aniso force must equal the isotropic force exactly.
    b = CFG["box"]
    geom = Geom(b["Lx"], b["Ly"], b["wall_t"], b["ch_w_default"])
    rngA = np.random.default_rng(99)
    Sm, xsm, ysm = frozen_grid(geom, 0.25, rngA, M=40)
    pts = [(1.0, 1.0), (2.0, 1.0), (3.0, 0.6), (0.7, 1.6)]
    ok_consist = all(
        np.allclose(force_frozen(geom, Sm, xsm, ysm, np.array(p)),
                    force_frozen_aniso(geom, Sm, Sm, xsm, ysm, np.array(p)))
        for p in pts)
    # NEW (v4.3): aniso curl smoke test -- the mixed partial of the
    # difference field S(tau_y) - S(tau_x) must be non-degenerate (this is
    # the theorem's premise made empirical), and vanish when tau_y == tau_x.
    Sm2, _, _ = frozen_grid(geom, 1.0, rngA, M=40)
    hx, hy = xsm[1] - xsm[0], ysm[1] - ysm[0]
    def mixed_partial_mag(D):
        mp = (D[2:, 2:] - D[2:, :-2] - D[:-2, 2:] + D[:-2, :-2]) / (4 * hx * hy)
        return float(np.nanmean(np.abs(mp)))
    curl_mismatch = mixed_partial_mag(Sm2 - Sm)
    curl_self = mixed_partial_mag(Sm - Sm)
    ok_curl = (curl_mismatch > 10 * max(curl_self, 1e-15))
    print(f"# aniso curl smoke: |d2(S1.0 - S0.25)/dxdy| ~ {curl_mismatch:.3e} "
          f"(self-difference {curl_self:.1e})")
    # NEW (v4.3): aniso gate-can-fail -- synthetic null blocks must NOT fire
    # the G2 logic; synthetic opposite-sign signal blocks MUST fire.
    rngG = np.random.default_rng(11)
    Ba = sw["aniso_blocks"]; alpha = th_cfg["aniso_alpha"]; scmin = th_cfg["sign_consistency_aniso"]
    def g2_fire(A1, A2, EQ):
        def two_sided(base, arm):
            return block_perm_p([[v] for v in base], [[v] for v in arm],
                                lambda A, Bb: abs(np.mean([x[0] for x in Bb]) - np.mean([x[0] for x in A])),
                                n_perm=2000, seed=13)
        ha = holm([two_sided(EQ, A1), two_sided(EQ, A2)])
        m1, m2, me = np.mean(A1), np.mean(A2), np.mean(EQ)
        s1 = max(sum(1 for v in A1 if v > 0), sum(1 for v in A1 if v < 0))
        s2 = max(sum(1 for v in A2 if v > 0), sum(1 for v in A2 if v < 0))
        return bool(max(ha) < alpha and s1 >= scmin and s2 >= scmin
                    and (m1 - me) * (m2 - me) < 0)
    sd_syn = 1.0
    null_fire = g2_fire(list(rngG.normal(0, sd_syn, Ba)),
                        list(rngG.normal(0, sd_syn, Ba)),
                        list(rngG.normal(0, sd_syn, Ba)))
    sig_fire = g2_fire(list(rngG.normal(+4 * sd_syn, sd_syn, Ba)),
                       list(rngG.normal(-4 * sd_syn, sd_syn, Ba)),
                       list(rngG.normal(0, sd_syn, Ba)))
    ok_g2gate = (not null_fire) and sig_fire
    print(f"# gate-can-fail(aniso G2): null fires={null_fire} (must be False) | "
          f"signal fires={sig_fire} (must be True)")
    allok = (ok_gyr and ok_fpt and ok_fields and ok_quadsynth and ok_vortex
             and ok_gate and ok_power and ok_consist and ok_curl and ok_g2gate)
    print(f"# gyr:{ok_gyr} fpt:{ok_fpt} fields:{ok_fields} quad_synth:{ok_quadsynth} "
          f"vortex_sign:{ok_vortex} occ_gate:{ok_gate} power:{ok_power} "
          f"aniso_consist:{ok_consist} aniso_curl:{ok_curl} g2_gate:{ok_g2gate} "
          f"| {round(time.time()-t0,1)}s")
    print("# SELFTEST " + ("PASS" if allok else "FAIL"))

def pilot():
    """Declared pilot: 4 blocks of the (0.25, 1.0) mismatch arm at full scale,
    seed namespace v43pilot::, NEVER pooled into confirmatory analysis.
    Purpose: measure the aniso block sd and observed mean BEFORE freezing the
    registration, so the detection-floor claim in the prereg is empirical."""
    sw = CFG["sweeps"]; pw = CFG["power"]
    tx, ty = sw["aniso_pairs"][0]
    vals = []
    for i in range(4):
        uid = f"C5a_frozen_tx{tx}_ty{ty}_sb{i}"
        r = run_unit(uid, seed_fn=pilot_seed)
        vals.append(r["data"]["quad"]["quad_loop_rate"])
    m = float(np.mean(vals)); sd = float(np.std(vals, ddof=1))
    floor = _detection_floor(sd, sw["aniso_blocks"], pw["alpha_worst"], pw["power_target"])
    print(f"# PILOT (v43pilot:: namespace, 4 blocks, pair ({tx},{ty})):")
    print(f"# blocks = {[f'{v:.3e}' for v in vals]}")
    print(f"# mean = {m:.3e}  sd = {sd:.3e}")
    print(f"# implied 90%-power detection floor at B={sw['aniso_blocks']}: {floor:.3e}")
    print(f"# observed |mean| vs floor: {'ABOVE' if abs(m) > floor else 'below'}")

def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__); return
    if a[0] == "--plan":
        print(json.dumps({"type": "preregistration", "source_sha_at_registration": SOURCE_SHA, "version": VERSION,
                          "config_hash": config_hash(), "config": CFG,
                          "units": build_units(),
                          "outcome_map": [
                              "G1 powered vortex control: monotone over POWERED arms (k0<=k4<=k8; k2 descriptive) + Holm(p_k4,p_k8)<0.01 + sign>=24/32 both (compound-gate power simulated in selftest)",
                              "G2 aniso engine (requires G1): Holm two-sided p<0.01 both mismatch arms vs equal-tau + sign>=48/64 each + OPPOSITE arm signs (antisymmetry gate)",
                              "SECONDARY (not gating): directional prediction CCW(+) for (0.25,1.0), CW(-) for (1.0,0.25), derived pre-registration from M=4000 mean-field ROI curl",
                              "G3 bounded null: G1 pass, G2 no-fire -> no aniso current at reported detection floor",
                              "G4 G1 fail -> inconclusive on G2, instrument redesign",
                              "OCC powered occupancy re-test at B=32 (confirmatory re-test of v4.2 p=0.048, not a fork gate)",
                              "SCOPE: any G2 pass = coherent circulation in the reset-defined transport protocol; NOT a stationary closed-system NESS claim (v4.4+ lineage)"]},
                         indent=2)); return
    if a[0] == "--list":
        for u in build_units(): print(u)
        return
    if a[0] == "--selftest":
        selftest(); return
    if a[0] == "--pilot":
        pilot(); return
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
