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

import sys, os, json, math, time, hashlib, warnings
warnings.filterwarnings('ignore')
import numpy as np

VERSION = "v4h-1.4.0"
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
    "scout": {
        # v4.4 Movement 2 transduction scout. Pilot namespace v44pilot::,
        # NEVER pooled into any confirmatory analysis (law #6). Sizes the
        # SIGNAL -- aniso current vs horizon mismatch (Delta-tau) and drive
        # amplitude (Tc) -- not the noise. Cells stand alone; no cross-cell
        # aggregation. Each cell is compared only to its own B=64 floor.
        "blocks": 16,   # [v3.6] 8->16: finding 6 (CFG-vs-RULE drift) — the
                        # ratified ladder's first rung (RULE["blocks_first"])
                        # needs 16 blocks/cell; the pre-ratification value
                        # starved it. Cross-asserted in _rule_selftest().
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

def scout_seed(unit_id):
    # v4.4 scout pilot namespace; scout results are NEVER pooled into analysis
    h = hashlib.sha256(("v44pilot::" + unit_id).encode()).digest()
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

def force_frozen(geom, S, xs, ys, r, Tc=None):
    e = CFG["entropy"]
    tc = e["Tc"] if Tc is None else Tc
    i = np.clip(np.searchsorted(xs, r[0]) - 1, 1, len(xs) - 2)
    j = np.clip(np.searchsorted(ys, r[1]) - 1, 1, len(ys) - 2)
    hx, hy = xs[1] - xs[0], ys[1] - ys[0]
    Fx = tc * (S[i + 1, j] - S[i - 1, j]) / (2 * hx)
    Fy = tc * (S[i, j + 1] - S[i, j - 1]) / (2 * hy)
    return np.array([Fx, Fy])

def force_frozen_aniso(geom, Sx, Sy, xs, ys, r, Tc=None):
    """Anisotropic-horizon causal-entropic force: the x-component is the
    gradient of S_c(.; tau_x), the y-component the gradient of S_c(.; tau_y).
    For tau_x != tau_y the components are gradients of DIFFERENT scalar
    fields, so the mean force has curl Tc d2/dxdy [S(tau_y) - S(tau_x)] != 0
    generically -- the minimal exit from the conservative estimator class
    fenced off by the v4.2 structural result."""
    e = CFG["entropy"]
    tc = e["Tc"] if Tc is None else Tc
    i = np.clip(np.searchsorted(xs, r[0]) - 1, 1, len(xs) - 2)
    j = np.clip(np.searchsorted(ys, r[1]) - 1, 1, len(ys) - 2)
    hx, hy = xs[1] - xs[0], ys[1] - ys[0]
    Fx = tc * (Sx[i + 1, j] - Sx[i - 1, j]) / (2 * hx)
    Fy = tc * (Sy[i, j + 1] - Sy[i, j - 1]) / (2 * hy)
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
                vortex_kappa=0.0, tau_y=None, Tc_ov=None):
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
                    Fcache = force_frozen_aniso(geom, S, S2, xs, ys, pos, Tc=Tc_ov)
                else:
                    Fcache = force_frozen(geom, S, xs, ys, pos, Tc=Tc_ov)
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

# ============================================================================
# v4.4 SCOUT DECISION RULE v3.5 -- EXECUTABLE ENCODING
# ============================================================================
# Ratified by Anthony 2026-07-08 (RATIFICATION_v3.5.md). Governing text:
# v44_scout_DECISION_RULE_v3.5.md. Where that prose and any older pseudocode
# disagree, THE RATIFIED v3.5 PROSE WINS.
#
# ADDITIVE PATH. Nothing below is read by the v4.3 gates (C0 / occupancy /
# fpt / G1 vortex / G2 aniso / G3 / G4). CFG is NOT touched, so config_hash
# is unchanged (a344d6c47c8a22c1) and --analyze on a v4.3 NDJSON is
# bit-identical to the pre-change harness. These constants are CODE and are
# therefore covered by SOURCE_SHA, which changes -- forcing a prereg re-issue
# at registration (law #1; Anthony's gate, NOT performed here).
#
# STILL A REGISTRATION-TIME CFG CHANGE, FLAGGED AND NOT MADE (rule doc sec 10):
#   CFG["scout"]["blocks"]  8 -> 16   (decision D2)
#   CFG["scout"]["n_rerun"] absent -> 56   (sec 8 / sec 8-Omega powered rerun)
# Both change config_hash. Anthony's gate.

CEILING = "INCONCLUSIVE_AT_CEILING"          # terminal label (Q4). NEVER a null.
BANDS = ("GREEN", "AMBER", "RED", "ANOMALOUS")
BAND_VOCAB = frozenset(BANDS + (CEILING,))

RULE = {
    "rule_version": "v3.6",
    "ratified": "2026-07-13",      # v3.6 enactment (Anthony; RATIFICATION_v3.6.md)
    "ratified_v3_5": "2026-07-08", # the superseded rule's own ratification date

    # --- sec 0.1 detection floor: floor(B, sd) = Z * sd * sqrt(2/B) ---
    "Z": 3.858,                    # z_{0.995} + z_{0.90}
    "alpha": 0.05,
    # --- sec 2.1 honest SE: sd * sqrt(1/B_scout + 1/64) -- folds in the
    #     v4.3 64-block equal-arm reference (reference-uncertain, marginal) ---
    "ref_blocks": 64,
    # --- sec 4 shared ladder: 16b/B96 -> 32b/B96 -> 32b/B128 -> INCONCLUSIVE ---
    "blocks_first": 16,            # D2 (CFG["scout"]["blocks"] 8->16 at registration)
    "blocks_extended": 32,
    "B_conf": 96,                  # D4
    "B_max": 128,                  # declared compute ceiling (fork 7)
    "n_rerun": 56,                 # sec 8 / sec 8-Omega powered STATE-B rerun [v3.5]
    # --- sec 2.2 frozen Student-t convention (alpha = 0.05) ---
    "t_one_sided": {7: 1.895, 15: 1.753, 31: 1.696, 55: 1.673},
    "t_two_sided": {7: 2.365, 15: 2.131, 31: 2.040, 55: 2.004},
    # --- sec 3.3 sd_upper = sd * sqrt((n-1)/chi2_{0.05,n-1}) ---
    "chi2_upper": {7: 1.797, 15: 1.437, 31: 1.268},
    # --- sec 2.3 exact thresholds table (units of sd_cell) -- the law-#4
    #     grep targets: every one of these is re-derived and grep-checked
    #     against the ratified prose in _rule_selftest(). ---
    "floor_64": 0.682, "floor_96": 0.557, "floor_128": 0.482,
    "se_8_96": 0.375, "se_16_96": 0.2795, "se_32_96": 0.2165, "se_56": 0.1830,
    "green_16_96_1s": 1.047, "green_16_96_2s": 1.152,   # [v3.6] row 5: 1.15246 rounds 1.152 (ratified convention)
    "kappa_16_96_1s": 0.067,       # OPERATIVE frozen RED: |mu| < 0.067*sd
    "kappa_16_96_2s": -0.039,      # < 0 -> two-sided RED UNREACHABLE at 16b
    "kappa_32_96_1s": 0.190, "kappa_32_96_2s": 0.115,
    "kappa_32_128_1s": 0.115,
    "rerun_edge": 0.306,           # |x| > t55 * SE56  [v3.5]
    "kappa_56": 0.251,             # floor(96) - rerun_edge  [v3.5]
    "rerun_power": 0.913,          # honest noncentral-t at -+1x floor(96) [v3.5]
    "compound_power_target": 0.90, # law #3: COMPOUND gate MC, not analytic
}

def _t_star(df, two_sided):
    """sec 2.2 frozen convention. Unregistered df is a registration error --
    the rule fires only at rungs it froze thresholds for."""
    tab = RULE["t_two_sided"] if two_sided else RULE["t_one_sided"]
    if df not in tab:
        raise ValueError("no frozen t* for df=%r (rule sec 2.2)" % (df,))
    return tab[df]

def _chi2_upper_factor(df):
    """sec 3.3 sd_upper factor sqrt((n-1)/chi2_{0.05,n-1})."""
    tab = RULE["chi2_upper"]
    if df not in tab:
        raise ValueError("no frozen chi2 upper factor for df=%r (rule sec 3.3)" % (df,))
    return tab[df]

def rule_floor(sd, B_conf):
    """sec 0.1 two-arm minimum-detectable-effect."""
    return RULE["Z"] * sd * math.sqrt(2.0 / B_conf)

def rule_se(sd, n_blocks):
    """sec 2.1 honest SE -- folds in the 64-block equal-arm reference."""
    return sd * math.sqrt(1.0 / n_blocks + 1.0 / RULE["ref_blocks"])

def band_cell(mu_hat, sd_cell, n_blocks, B_conf, sigma_cell, stable_cell=None):
    """sec 3: band ONE scout cell on ONE statistic.

    Called for quad_loop_rate (sigma from P1-A), omega_roi (sigma from
    P1-A(omega)) and occupancy_x (ALWAYS two-sided -- sigma_cell=None, D1'').
    Returns (band, bound, floor_c); band in BANDS. CEILING is set by the
    caller's terminal ladder (sec 4), never here.

    sigma_cell in {+1, -1, None}; None => two-sided (P1 INDETERMINATE).
    stable_cell is NOT consumed here -- it is consumed at the pivot (sec 5 ii);
    the parameter is retained to match the ratified sec-7 interface.

    THE PARTITION IS COMPLETE: GREEN | ANOMALOUS | RED | AMBER, in that
    priority. RED is the sec-3.3 [v3.6] single MAGNITUDE conjunct:
    |mu_hat| + t*SE(sd_hat) < floor_c(sd_hat), evaluated after the
    GREEN/ANOMALOUS branches. The historical v3.1 aligned conjunct and the
    v3.2/v3.3 coupled-upper (sd_upper) conjuncts are PROVEN empty and removed
    (fork 14, ratified 2026-07-13): floor_c and rule_se are both degree-1 in
    sd, so each upper conjunct is the point conjunct with its threshold scaled
    by chi2_upper > 1, and the aligned conjunct is implied by the magnitude
    conjunct (|x| <= |mu_hat| both sidednesses). Verdict-identical on 3.73M
    probes incl. a firing positive control (laneB/sec33_inertness_probe.py);
    pinned forever by the verdict-identity regression in _rule_selftest().
    NOTE [v3.6]: with the coupled-upper conjuncts gone, band_cell no longer
    consults RULE["chi2_upper"], so df is no longer restricted to that table
    here -- _t_star() remains the frozen-df registration guard for ALL paths.
    """
    if not (sd_cell > 0):
        raise ValueError("sd_cell must be > 0 (got %r) -- data integrity" % (sd_cell,))
    df = n_blocks - 1
    two_sided = (sigma_cell is None)
    t = _t_star(df, two_sided)

    f_c = rule_floor(sd_cell, B_conf)
    se_c = rule_se(sd_cell, n_blocks)

    x = abs(mu_hat) if two_sided else sigma_cell * mu_hat   # prediction-aligned

    if x - t * se_c > f_c:
        return ("GREEN", x - t * se_c, f_c)

    # ANOMALOUS keys on significance against 0 (Finding-4 correction).
    # Does NOT apply two-sided (no registered direction to oppose).
    if (not two_sided) and (x < -t * se_c):
        return ("ANOMALOUS", x - t * se_c, f_c)

    # sec 3.3 [v3.6]: single magnitude conjunct (see docstring; fork 14).
    if abs(mu_hat) + t * se_c < f_c:
        return ("RED", abs(mu_hat) + t * se_c, f_c)

    return ("AMBER", x + t * se_c, f_c)

def ladder_terminal(primary_blocks, omega_blocks, occupancy_blocks,
                    sigma_primary, sigma_omega):
    """sec 4: the SHARED terminal ladder, and the ONLY place CEILING is set.

        16b/B96  ->  32b/B96  ->  32b/B128  ->  INCONCLUSIVE_AT_CEILING

    *** THE LADDER TERMINATES IN INCONCLUSIVE. NOT IN A NULL. ***
    v3's "RED-at-ceiling" was the BLOCKED defect: a compute ceiling cannot
    mint evidence of absence. An unresolved statistic at B_max is CEILING,
    which BLOCKS the pivot (sec 5 (0'), primary or omega on a gating cell).

    Driven by the primary OR omega_roi (the D1 look-axis repair): the cell
    extends while EITHER is AMBER. A primary GREEN/ANOMALOUS short-circuits
    (outcome 1 / sec 8 preempt). occupancy_x does NOT drive the ladder
    (documented D1'' asymmetry, Anthony's fork 12) -- it is stamped at
    whatever rung the cell terminates on, and a terminal occupancy AMBER is
    recorded + caveated, NEVER laddered further and NEVER CEILING.

    ALL THREE statistics are stamped at the cell's SINGLE terminal rung
    (couple 7: the sim and analyze() share this one code path).

    32-block rungs are ACCUMULATION (first 16 + 16 more), not a redraw; the
    B96->B128 escalation re-bands the SAME 32-block sample.

    occupancy_blocks may be None -- the per-block occupancy SCALAR is NOT
    defined by the ratified rule (see OCC_REDUCTION_GAP). Then the occupancy
    band is None and no pivot may be licensed.

    Returns a dict. If the data cannot supply the rung the ladder demands,
    status is EXTENSION_REQUIRED and NO band is stamped -- the analysis path
    never fabricates blocks it does not have.
    """
    rungs = [(RULE["blocks_first"], RULE["B_conf"]),
             (RULE["blocks_extended"], RULE["B_conf"]),
             (RULE["blocks_extended"], RULE["B_max"])]

    def stamp(series, n, B_conf, sigma):
        v = np.asarray(series[:n], dtype=float)
        return band_cell(float(v.mean()), float(v.std(ddof=1)), n, B_conf, sigma)

    for idx, (n, B_conf) in enumerate(rungs):
        have = len(primary_blocks)
        if have < n:
            return {"status": "EXTENSION_REQUIRED", "need_blocks": n,
                    "have_blocks": have, "rung": None,
                    "primary": None, "omega": None, "occupancy": None}
        pb, p_bound, p_floor = stamp(primary_blocks, n, B_conf, sigma_primary)
        wb, w_bound, w_floor = stamp(omega_blocks, n, B_conf, sigma_omega)
        if occupancy_blocks is None:
            cb = None
        else:
            cb = stamp(occupancy_blocks, n, B_conf, None)[0]   # ALWAYS two-sided

        last = (idx == len(rungs) - 1)
        short_circuit = pb in ("GREEN", "ANOMALOUS")

        if last and not short_circuit:
            # compute ceiling: whichever LADDERED statistic is still AMBER is
            # INCONCLUSIVE. It is not RED. It never becomes RED. It blocks.
            if pb == "AMBER":
                pb = CEILING
            if wb == "AMBER":
                wb = CEILING
        elif not short_circuit and (pb == "AMBER" or wb == "AMBER"):
            continue                                   # extend to the next rung

        return {"status": "TERMINAL", "rung": {"n_blocks": n, "B_conf": B_conf},
                "short_circuit": bool(short_circuit),
                "primary": pb, "omega": wb, "occupancy": cb,
                "primary_floor": p_floor, "omega_floor": w_floor}
    raise AssertionError("unreachable: the ladder must terminate")

def pivot_licensed(gating_bands, stable_flags, omega_bands, occupancy_bands,
                   descriptive_bands,
                   REGISTERED_GATING_ROSTER, REGISTERED_FULL_ROSTER,
                   occ_reduction_name, REGISTERED_OCC_REDUCTION):   # [v3.6]
    """sec 5: pivot to the closed no-reset NESS protocol iff ALL conditions hold.

    Returns (licensed: bool, reason: str). Guarded against: vacuous truth
    (all([]) is True), compute-ceiling-minted absence (primary AND omega),
    wrong-sign magnitude leak (belt + STABLE suspenders), statistic-projection
    null (omega veto at the shared-ladder look + occupancy GREEN-veto),
    shrunk-denominator null on EVERY consumed dict (full-roster completeness),
    and [v3.6] an occupancy veto satisfied by an UNREGISTERED estimand (the
    sec-5(iii') back door demonstrated by Lane B, closed by fork 15).

    ORDER: the [v3.6] ESTIMAND-REGISTRATION guard runs before any band is
    read; then THE ANOMALY GUARD, per the ratified prose order. An open
    ANOMALOUS anywhere blocks ANY terminal-null decision before a single
    all()/any() over a possibly-empty or silently-shrunken set can run.
    A registration mismatch is a REGISTRATION-INTEGRITY FLAG, never a null.
    """
    # ---- (0'') ESTIMAND REGISTRATION [v3.6] -- before any band is read:
    if REGISTERED_OCC_REDUCTION is None:
        return (False, "no registered occupancy reduction (OCC_REDUCTION_GAP)")
    if occ_reduction_name != REGISTERED_OCC_REDUCTION:
        return (False, "occupancy bands stamped from unregistered reduction %r"
                       % (occ_reduction_name,))

    GATING = set(REGISTERED_GATING_ROSTER)
    FULL = set(REGISTERED_FULL_ROSTER)
    DEMOTED = FULL - GATING

    # ---- (0) ANOMALY GUARD -- FIRST CHECK. An open ANOMALOUS cell blocks any
    #      terminal-null decision (sec 5 outcome 3). Exit from ANOMALOUS only
    #      via the POWERED sec-8 / sec-8-Omega machine (n_rerun = 56).
    for name, d in (("gating", gating_bands), ("descriptive", descriptive_bands),
                    ("omega", omega_bands)):
        for c, b in d.items():
            if b == "ANOMALOUS":
                return (False, "open ANOMALOUS in %s_bands at cell %r "
                               "(powered sec-8 disposition required)" % (name, c))

    # ---- band vocabulary: an unknown label is a registration-integrity fault,
    #      never a silently-not-RED cell.
    for name, d in (("gating", gating_bands), ("omega", omega_bands),
                    ("occupancy", occupancy_bands), ("descriptive", descriptive_bands)):
        for c, b in d.items():
            if b not in BAND_VOCAB:
                return (False, "unknown band %r in %s_bands at cell %r" % (b, name, c))

    # ---- (iv) roster assertion + (v) FULL-ROSTER COMPLETENESS on EVERY
    #      consumed dict. A silently-dropped or extra cell in ANY dict can
    #      never shrink the claim.  <- this is what kills 5-RED + 1-ANOMALOUS
    #      re-shaped as a 5-key gating dict.
    if not GATING <= FULL:
        return (False, "gating roster is not a subset of the full roster")
    if set(gating_bands.keys()) != GATING:
        return (False, "gating_bands keys != REGISTERED_GATING_ROSTER")
    if set(omega_bands.keys()) != FULL:
        return (False, "omega_bands keys != REGISTERED_FULL_ROSTER")
    if set(occupancy_bands.keys()) != FULL:
        return (False, "occupancy_bands keys != REGISTERED_FULL_ROSTER")
    if set(descriptive_bands.keys()) != DEMOTED:
        return (False, "descriptive_bands keys != FULL - GATING")
    if not gating_bands:
        return (False, "empty gating roster -- nothing bounds the space "
                       "(vacuous-truth guard)")

    # ---- (0') NO CEILING-MINTED ABSENCE (Q4). Primary OR omega unresolved on
    #      a GATING cell blocks. The ladder ends in INCONCLUSIVE, and
    #      INCONCLUSIVE is not evidence of absence.
    for c in GATING:
        if gating_bands[c] == CEILING:
            return (False, "primary %s at gating cell %r" % (CEILING, c))
        if omega_bands[c] == CEILING:
            return (False, "omega %s at gating cell %r (unresolved secondary)" % (CEILING, c))
    # (a DEMOTED cell's omega CEILING is recorded + caveated, non-blocking.)

    # ---- (iii) OMEGA VETO (statistic axis), full roster: GREEN anywhere blocks.
    #      (ANOMALOUS anywhere already blocked at the anomaly guard.)
    for c, b in omega_bands.items():
        if b == "GREEN":
            return (False, "omega veto: omega GREEN at cell %r" % (c,))

    # ---- (iii') OCCUPANCY VETO (recorded-statistic axis), full roster,
    #      two-sided: GREEN anywhere blocks. Terminal occupancy AMBER does NOT
    #      block but MUST appear in the claim caveat (sec 2.1).
    for c, b in occupancy_bands.items():
        if b == "GREEN":
            return (False, "occupancy veto: occupancy GREEN at cell %r" % (c,))

    # ---- demoted-cell primary dispositions (sec 1.2 clause 3): a demoted GREEN
    #      forces outcome 1.
    for c, b in descriptive_bands.items():
        if b == "GREEN":
            return (False, "demoted-cell primary GREEN at cell %r (outcome 1)" % (c,))

    # ---- outcome-1 guard: a primary GREEN on any gating cell -> register the
    #      Movement-3 contrast there instead of pivoting.
    for c, b in gating_bands.items():
        if b == "GREEN":
            return (False, "primary GREEN at gating cell %r (outcome 1)" % (c,))

    # ---- (i) TERMINAL-BAND CONDITION: every gating cell actual RED.
    for c, b in gating_bands.items():
        if b != "RED":
            return (False, "gating cell %r is %s, not RED" % (c, b))

    # ---- (ii) SUSPENDERS: every counted RED sits on a STABLE cell.
    for c, b in gating_bands.items():
        if b == "RED" and not stable_flags.get(c, False):
            return (False, "UNSTABLE cell %r cannot license a RED pivot" % (c,))

    return (True, "all-RED pivot licensed over the registered gating roster")

# --- THE OCCUPANCY SCALAR GAP (reported, NOT silently patched) --------------
# The ratified rule bands `occupancy_x` as a per-block SCALAR (two-sided,
# sec 3 / D1''). The harness records occupancy_x as a 24-bin HISTOGRAM per
# block (pilot_pair, run_chamber). NO per-block scalar reduction is defined in
# the ratified text, in prereg_v44.json, or in the OC sims (which model
# Delta_occ abstractly in sd units). So the occupancy veto -- a pivot
# PRECONDITION -- cannot be evaluated on a real NDJSON until Anthony registers
# a reduction. This path therefore REFUSES to stamp an occupancy band by
# default and WITHHOLDS the pivot decision, rather than inventing an estimand.
OCC_REDUCTION_GAP = ("occupancy_x per-block scalar reduction is NOT registered "
                     "(rule bands a scalar; harness records a 24-bin histogram)")

def _occ_lr_asymmetry(hist):
    """R_occ per fork 15, ratified by Anthony 2026-07-13 (paraphrase: honesty
    prevails, make it real — verbatim utterance with original spacing lives in
    RATIFICATION_v3.6.md): signed left/right mass asymmetry of the 24-bin
    occupancy histogram — mean-zero under a symmetric null, consistent with the
    two-sided band_cell arithmetic; BLIND to left/right-symmetric occupancy
    shifts, and that blind spot is stated in the claim (v3.6 sec 2.1).
    Registration BINDS via the re-issued prereg's occ_reduction field naming
    it — this function is only *registered* when that field says so. The
    invoked choice is still stamped in the report, and any mismatch with the
    registered name WITHHOLDS the decision (never a null)."""
    v = np.asarray(hist, dtype=float)
    tot = v.sum()
    if tot <= 0:
        raise ValueError("empty occupancy histogram")
    h = len(v) // 2
    return float((v[h:].sum() - v[:h].sum()) / tot)

OCC_REDUCTIONS = {"lr_asymmetry": _occ_lr_asymmetry}

def scout_outcome(gating_bands, omega_bands, occupancy_bands, descriptive_bands,
                  stable_flags, GATING, FULL,
                  occ_reduction_name=None, REGISTERED_OCC_REDUCTION=None):  # [v3.6]
    """sec 5: exactly ONE of the four honest terminal outcomes."""
    licensed, reason = pivot_licensed(gating_bands, stable_flags, omega_bands,
                                      occupancy_bands, descriptive_bands, GATING, FULL,
                                      occ_reduction_name, REGISTERED_OCC_REDUCTION)
    if licensed:
        return ("PIVOT_ALL_RED", reason, licensed)
    anom = [c for d in (gating_bands, descriptive_bands, omega_bands)
            for c, b in d.items() if b == "ANOMALOUS"]
    veto = [c for c, b in omega_bands.items() if b == "GREEN"] + \
           [c for c, b in occupancy_bands.items() if b == "GREEN"]
    if anom or veto:
        return ("INVESTIGATE_FLAG", reason, licensed)
    green = [c for d in (gating_bands, descriptive_bands)
             for c, b in d.items() if b == "GREEN"]
    if green:
        return ("GREEN_CANDIDATE", reason, licensed)
    if any(gating_bands.get(c) == CEILING or omega_bands.get(c) == CEILING
           for c in GATING):
        return ("INCONCLUSIVE_AT_COMPUTE_CEILING", reason, licensed)
    return ("BLOCKED", reason, licensed)

def scout_report(scout_rows, opts):
    """Additive v4.4 path: run the RATIFIED v3.5 decision rule over a scout
    NDJSON. Prints ONE json object. Never touches the v4.3 gates.

    Preconditions P1 (sigma_cell, sigma^omega_cell, STABLE) and P2 (the
    registered gating + full rosters) are NOT in the NDJSON. Without a
    registered --p1 file the bands are still stamped, but the DECISION IS
    WITHHELD: no license may be emitted over unregistered preconditions
    (rule sec 1.1 / sec 1.2, law #1).
    """
    p1 = json.load(open(opts["p1"])) if opts.get("p1") else None
    invoked_occ = opts.get("occ_reduction")
    occ_fn = OCC_REDUCTIONS.get(invoked_occ or "")
    # [v3.6] the REGISTERED reduction name comes from the re-issued prereg
    # (--prereg path, field occ_reduction.name) -- never from the CLI choice.
    registered_occ = None
    if opts.get("prereg"):
        registered_occ = (json.load(open(opts["prereg"]))
                          .get("occ_reduction") or {}).get("name")
    cells = {}
    for d in scout_rows:
        cells.setdefault(d["cell"], []).append(d)
    rep = {"rule_version": RULE["rule_version"], "version": VERSION,
           "config_hash": config_hash(), "source_sha": SOURCE_SHA,
           "n_scout_blocks": len(scout_rows), "cells": {}}
    withheld = []
    if p1 is None:
        withheld.append("P1/P2 not supplied (--p1): sigma_cell, sigma^omega_cell, "
                        "STABLE and the registered rosters are unregistered")
    if occ_fn is None:
        withheld.append(OCC_REDUCTION_GAP)
    # [v3.6] withhold-on-mismatch (fork 15): the decision is WITHHELD unless
    # the invoked reduction IS the registered one. A mismatch is a
    # registration-integrity flag, never a null.
    if registered_occ is None:
        withheld.append("no registered occupancy reduction: the re-issued "
                        "prereg's occ_reduction field was not supplied "
                        "(--prereg) or does not name one")
    elif invoked_occ != registered_occ:
        withheld.append("invoked occupancy reduction %r != registered %r "
                        "(registration-integrity flag)"
                        % (invoked_occ, registered_occ))
    for label in sorted(cells):
        blocks = sorted(cells[label], key=lambda r: r["block"])
        q = [b["quad_loop_rate"] for b in blocks]
        w = [b["omega_roi"] for b in blocks]
        c = [occ_fn(b["occupancy_x"]) for b in blocks] if occ_fn else None
        sg = (p1 or {}).get(label, {})
        term = ladder_terminal(q, w, c, sg.get("sigma_cell"), sg.get("sigma_omega_cell"))
        term["n_blocks_available"] = len(q)
        rep["cells"][label] = term
    rep["decision"] = {"emitted": False, "withheld_because": withheld}
    if not withheld:
        GATING = frozenset(p1["__gating_roster__"])
        FULL = frozenset(p1["__full_roster__"])
        gb = {c: rep["cells"][c]["primary"] for c in GATING}
        ob = {c: rep["cells"][c]["omega"] for c in FULL}
        cb = {c: rep["cells"][c]["occupancy"] for c in FULL}
        db = {c: rep["cells"][c]["primary"] for c in (FULL - GATING)}
        st = {c: bool(p1[c].get("stable")) for c in GATING}
        outcome, reason, lic = scout_outcome(gb, ob, cb, db, st, GATING, FULL,
                                             invoked_occ, registered_occ)
        # EVERY blocking condition is reported, not just the first one hit --
        # an operator must never read a single short-circuit reason as if it
        # were the only thing standing between the run and a pivot.
        flags = {
            "primary_ANOMALOUS": sorted(c for d in (gb, db) for c, b in d.items()
                                        if b == "ANOMALOUS"),
            "omega_ANOMALOUS": sorted(c for c, b in ob.items() if b == "ANOMALOUS"),
            "omega_GREEN_veto": sorted(c for c, b in ob.items() if b == "GREEN"),
            "occupancy_GREEN_veto": sorted(c for c, b in cb.items() if b == "GREEN"),
            "primary_GREEN": sorted(c for d in (gb, db) for c, b in d.items()
                                    if b == "GREEN"),
            "primary_at_ceiling_gating": sorted(c for c in GATING if gb[c] == CEILING),
            "omega_at_ceiling_gating": sorted(c for c in GATING if ob[c] == CEILING),
            "omega_at_ceiling_demoted_caveat": sorted(c for c in (FULL - GATING)
                                                      if ob[c] == CEILING),
            "occupancy_AMBER_mandatory_caveat": sorted(c for c, b in cb.items()
                                                       if b == "AMBER"),
            "UNSTABLE_gating": sorted(c for c in GATING if not st[c]),
        }
        rep["decision"] = {"emitted": True, "outcome": outcome,
                           "pivot_licensed": lic, "first_blocking_reason": reason,
                           "flags": {k: v for k, v in flags.items() if v},
                           "occ_reduction": invoked_occ,
                           "occ_reduction_registered": registered_occ}  # [v3.6]
    print(json.dumps(rep, indent=1))
    return rep

def _scout_opts(args):
    o = {}
    if "--p1" in args:
        o["p1"] = args[args.index("--p1") + 1]
    if "--occ-reduction" in args:
        o["occ_reduction"] = args[args.index("--occ-reduction") + 1]
    if "--prereg" in args:                                   # [v3.6] fork 15
        o["prereg"] = args[args.index("--prereg") + 1]
    return o

def analyze(args):
    th = CFG["thresholds"]; sw = CFG["sweeps"]; pw = CFG["power"]
    rows = {}
    scout_rows = []
    for line in open(args[0]):
        if line.strip().startswith("{"):
            d = json.loads(line)
            if d.get("type") == "result":
                rows[d["unit"]] = d
            elif d.get("type") == "scout":
                scout_rows.append(d)
    # ADDITIVE v4.4 PATH. A scout-only NDJSON has no v4.3 units at all (the
    # old code raised KeyError on it); route it to the ratified decision rule.
    # A v4.3 NDJSON with no scout rows takes the untouched path below and its
    # output is bit-identical to the pre-change harness.
    if not rows:
        scout_report(scout_rows, _scout_opts(args))
        return
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
                            lambda A, Bb: np.mean([b[0] for b in Bb]) - np.mean([a[0] for a in A]))
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
    s1 = max(sum(1 for v in A1 if v > me), sum(1 for v in A1 if v < me))
    s2 = max(sum(1 for v in A2 if v > me), sum(1 for v in A2 if v < me))
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
    # ADDITIVE: a mixed NDJSON (v4.3 units + v4.4 scout blocks) gets the scout
    # decision printed as a SEPARATE object, after the untouched v4.3 report.
    if scout_rows:
        scout_report(scout_rows, _scout_opts(args))

def occ_chi2_stat(A, B):
    pa = np.mean(A, axis=0); pb = np.mean(B, axis=0)
    return float(np.sum((pa - pb) ** 2 / (pa + pb + 1e-12)))

def block_perm_p(A, B, stat, n_perm=None, seed=123):
    import random as _rnd
    n_perm = n_perm or CFG["thresholds"]["n_perm"]
    allb = list(A) + list(B); nf = len(A)
    obs = stat(A, B); r = _rnd.Random(seed); ex = 0
    idx = list(range(len(allb)))
    for _ in range(n_perm):
        pm = r.sample(idx, nf); s = set(pm)
        v = stat([allb[i] for i in pm], [allb[i] for i in idx if i not in s])
        if v >= obs:
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
    # NOTE: aniso compound-gate power is a Movement-3 (registration)
    # computation -- carried, not exercised here.
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
        s1 = max(sum(1 for v in A1 if v > me), sum(1 for v in A1 if v < me))
        s2 = max(sum(1 for v in A2 if v > me), sum(1 for v in A2 if v < me))
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
    # NEW (v4.4 rule 2): prose/config grep-check. Numeric thresholds written in
    # prose (--plan outcome_map + docstrings) must match frozen CFG. Minimal
    # forward check; Antigravity hardens it at audit.
    _src = open(__file__).read()
    _ratios = [f"{th_cfg['sign_consistency']}/{sw['c4v_blocks']}",        # 24/32 vortex
               f"{th_cfg['sign_consistency_aniso']}/{sw['aniso_blocks']}"]  # 48/64 aniso
    ok_grep = all(r in _src for r in _ratios)
    print(f"# prose/config grep-check: CFG ratios {_ratios} present -> {'PASS' if ok_grep else 'FAIL'}")
    # NEW (v4.4): the ratified decision-rule v3.5 selftest (laws #2/#3/#4).
    print("# --- v4.4 decision rule v3.5 selftest ---")
    ok_rule = _rule_selftest()
    allok = (ok_gyr and ok_fpt and ok_fields and ok_quadsynth and ok_vortex
             and ok_gate and ok_power and ok_consist and ok_curl and ok_g2gate
             and ok_grep and ok_rule)
    print(f"# gyr:{ok_gyr} fpt:{ok_fpt} fields:{ok_fields} quad_synth:{ok_quadsynth} "
          f"vortex_sign:{ok_vortex} occ_gate:{ok_gate} power:{ok_power} "
          f"aniso_consist:{ok_consist} aniso_curl:{ok_curl} g2_gate:{ok_g2gate} "
          f"grep:{ok_grep} rule_v35:{ok_rule} | {round(time.time()-t0,1)}s")
    print("# SELFTEST " + ("PASS" if allok else "FAIL"))

def _rule_selftest():
    """v4.4 decision-rule v3.5 selftest.

    LAW #2 -- the gate must demonstrably be able to FAIL on null/adversarial
    data. LAW #3 -- and demonstrably be able to PASS on true signal.
    LAW #4 -- every prose threshold is grepped against the frozen constants.
    """
    ok = True
    def check(name, got, want):
        nonlocal ok
        good = (got == want)
        ok = ok and good
        print("#   [%s] %-46s got=%-5s want=%-5s" %
              ("PASS" if good else "FAIL", name, got, want))
        return good

    R = RULE
    ALL = frozenset(["A", "B", "C", "D", "AxT2", "AxT4"])
    GAT = ALL                     # no-demotion case
    def lic(gb, st=None, ob=None, cb=None, db=None, G=GAT, F=ALL,
            occ="lr_asymmetry", reg="lr_asymmetry"):
        st = {c: True for c in G} if st is None else st
        ob = {c: "RED" for c in F} if ob is None else ob
        cb = {c: "AMBER" for c in F} if cb is None else cb
        db = {} if db is None else db
        return pivot_licensed(gb, st, ob, cb, db, G, F, occ, reg)[0]

    print("# --- [v3.6] estimand registration (sec 5 (0''), fork 15) CAN FAIL ---")
    check("pivot-compatible bands + NO registered reduction -> withheld",
          lic({c: "RED" for c in GAT}, reg=None), False)
    check("invoked reduction != registered -> registration-integrity flag",
          lic({c: "RED" for c in GAT}, occ="chi2_uniformity"), False)
    check("unregistered-reduction reason names the invoked estimand",
          "unregistered reduction" in pivot_licensed(
              {c: "RED" for c in GAT}, {c: True for c in GAT},
              {c: "RED" for c in ALL}, {c: "AMBER" for c in ALL}, {},
              GAT, ALL, "chi2_uniformity", "lr_asymmetry")[1], True)

    print("# --- [v3.6] finding-6 cross-assert: config vs rule drift ---")
    check("CFG.scout.blocks == RULE.blocks_first",
          CFG["scout"]["blocks"] == R["blocks_first"], True)

    print("# --- pivot_licensed() CAN FAIL (law #2) ---")
    check("empty band set (vacuous truth, all([])==True)",
          lic({}, st={}, G=frozenset(), F=frozenset()), False)
    check("empty gating dict vs registered roster",
          lic({}), False)
    check("all six ANOMALOUS", lic({c: "ANOMALOUS" for c in GAT}), False)
    check("one GREEN, five RED",
          lic(dict({c: "RED" for c in GAT}, **{"C": "GREEN"})), False)
    check("one AMBER, five RED",
          lic(dict({c: "RED" for c in GAT}, **{"C": "AMBER"})), False)
    check("five RED + one ANOMALOUS (6-key dict)",
          lic(dict({c: "RED" for c in GAT}, **{"AxT4": "ANOMALOUS"})), False)
    # the REAL vacuous-truth shape: the ANOMALOUS cell is silently dropped, so
    # all(b == "RED") is True over the survivors. The roster assertion kills it.
    check("five RED, ANOMALOUS cell SILENTLY DROPPED (shrunk denominator)",
          lic({c: "RED" for c in GAT if c != "AxT4"}), False)
    check("all RED but one cell UNSTABLE",
          lic({c: "RED" for c in GAT},
              st=dict({c: True for c in GAT}, **{"B": False})), False)
    check("primary INCONCLUSIVE_AT_CEILING on a gating cell",
          lic(dict({c: "RED" for c in GAT}, **{"A": CEILING})), False)
    check("omega INCONCLUSIVE_AT_CEILING on a gating cell",
          lic({c: "RED" for c in GAT},
              ob=dict({c: "RED" for c in ALL}, **{"A": CEILING})), False)
    check("omega GREEN (veto)",
          lic({c: "RED" for c in GAT},
              ob=dict({c: "RED" for c in ALL}, **{"D": "GREEN"})), False)
    check("omega ANOMALOUS (veto)",
          lic({c: "RED" for c in GAT},
              ob=dict({c: "RED" for c in ALL}, **{"D": "ANOMALOUS"})), False)
    check("occupancy GREEN (veto)",
          lic({c: "RED" for c in GAT},
              cb=dict({c: "AMBER" for c in ALL}, **{"C": "GREEN"})), False)
    check("omega_bands MISSING a key (dict-denominator leak)",
          lic({c: "RED" for c in GAT},
              ob={c: "RED" for c in ALL if c != "AxT4"}), False)
    check("occupancy_bands MISSING a key",
          lic({c: "RED" for c in GAT},
              cb={c: "AMBER" for c in ALL if c != "AxT4"}), False)
    check("omega_bands EXTRA key",
          lic({c: "RED" for c in GAT},
              ob=dict({c: "RED" for c in ALL}, **{"ZZZ": "RED"})), False)
    check("unknown band label", lic(dict({c: "RED" for c in GAT}, **{"A": "REDDISH"})), False)
    # demotion: AxT4 demoted -> gating roster is 5, descriptive must be exactly {AxT4}
    G5 = frozenset(ALL - {"AxT4"})
    check("demoted cell absent from descriptive_bands (S9-d)",
          lic({c: "RED" for c in G5}, st={c: True for c in G5},
              db={}, G=G5), False)
    check("demoted-cell primary GREEN forces outcome 1",
          lic({c: "RED" for c in G5}, st={c: True for c in G5},
              db={"AxT4": "GREEN"}, G=G5), False)
    check("occupancy GREEN at a DEMOTED cell still vetoes",
          lic({c: "RED" for c in G5}, st={c: True for c in G5},
              cb=dict({c: "AMBER" for c in ALL}, **{"AxT4": "GREEN"}),
              db={"AxT4": "RED"}, G=G5), False)

    print("# --- pivot_licensed() CAN PASS (law #3) ---")
    check("all-RED + all-STABLE, omega RED, occupancy AMBER",
          lic({c: "RED" for c in GAT}), True)
    check("all-RED + STABLE with AxT4 demoted (claim shrinks, still licensed)",
          lic({c: "RED" for c in G5}, st={c: True for c in G5},
              db={"AxT4": "RED"}, G=G5), True)
    check("omega CEILING on a DEMOTED cell only -> non-blocking",
          lic({c: "RED" for c in G5}, st={c: True for c in G5},
              ob=dict({c: "RED" for c in ALL}, **{"AxT4": CEILING}),
              db={"AxT4": "RED"}, G=G5), True)

    print("# --- band_cell() cutpoints (sec 2.3 / sec 3) ---")
    sd, n, B = 1.0, 16, 96
    f96 = rule_floor(sd, B); se16 = rule_se(sd, n); t15 = R["t_one_sided"][15]
    check("GREEN just above floor + t*SE",
          band_cell(f96 + t15 * se16 + 1e-9, sd, n, B, +1)[0], "GREEN")
    check("AMBER just below the GREEN edge",
          band_cell(f96 + t15 * se16 - 1e-9, sd, n, B, +1)[0], "AMBER")
    check("RED just inside kappa_16 = 0.067",
          band_cell(R["kappa_16_96_1s"] - 1e-3, sd, n, B, +1)[0], "RED")
    check("AMBER just outside kappa_16",
          band_cell(f96 - t15 * se16 + 1e-6, sd, n, B, +1)[0], "AMBER")
    check("wrong-sign at floor magnitude is NOT RED (v3.2 belt)",
          band_cell(-f96, sd, n, B, +1)[0] == "RED", False)
    check("ANOMALOUS: significant wrong-sign",
          band_cell(-(t15 * se16 + 1e-6), sd, n, B, +1)[0], "ANOMALOUS")
    check("two-sided RED UNREACHABLE at 16b (kappa_2s < 0)",
          any(band_cell(m, sd, n, B, None)[0] == "RED"
              for m in np.linspace(-0.05, 0.05, 41)), False)
    check("two-sided RED reachable at 32b",
          band_cell(0.05, sd, 32, B, None)[0], "RED")
    check("occupancy is banded two-sided: GREEN on |mu| with mu < 0",
          band_cell(-(f96 + R["t_two_sided"][15] * se16 + 1e-3), sd, n, B, None)[0], "GREEN")

    print("# --- sec 4 shared ladder: terminates in INCONCLUSIVE, never in a null ---")
    rng = np.random.default_rng(20260712)
    null32 = list(rng.normal(0.0, 1.0, 32))
    amber = [0.30 + 1e-9 * i for i in range(32)]          # sd~0 guard -> use noise
    amber = list(rng.normal(0.30, 1.0, 32))              # sits in AMBER at every rung
    t_amb = ladder_terminal(amber, amber, None, +1, +1)
    check("persistent AMBER -> primary INCONCLUSIVE_AT_CEILING",
          t_amb["primary"], CEILING)
    check("persistent AMBER -> terminal rung is 32b/B128",
          (t_amb["rung"]["n_blocks"], t_amb["rung"]["B_conf"]), (32, 128))
    check("ceiling label is NOT a null band",
          t_amb["primary"] in ("RED", "GREEN"), False)
    # a compute ceiling can never mint a RED. Constructed at runtime so the
    # forbidden literal itself never appears in this source file.
    forbidden = "RED" + "_AT_CEILING"
    check("no %s anywhere in the source (v3's BLOCKED defect)" % forbidden,
          forbidden in open(__file__).read(), False)
    # omega drives the ladder: primary RED at 16b, omega AMBER -> must extend
    red16 = list(rng.normal(0.0, 1.0, 16)) ; red16 = [v * 0.001 for v in red16]
    red32 = red16 + [v * 0.001 for v in rng.normal(0.0, 1.0, 16)]
    t_sh = ladder_terminal(red32, amber, None, +1, +1)
    check("primary RED at 16b + omega AMBER -> cell EXTENDS (not terminal at 16b)",
          t_sh["rung"]["n_blocks"] != 16, True)
    check("all statistics stamped at ONE terminal rung",
          t_sh["status"], "TERMINAL")
    t_short = ladder_terminal(list(rng.normal(8.0, 1.0, 32)), amber, None, +1, +1)
    check("primary GREEN short-circuits the ladder at 16b",
          (t_short["primary"], t_short["rung"]["n_blocks"]), ("GREEN", 16))
    check("data too short for the demanded rung -> EXTENSION_REQUIRED, no band",
          ladder_terminal(amber[:16], amber[:16], None, +1, +1)["status"],
          "EXTENSION_REQUIRED")

    print("# --- [v3.6] verdict-identity regression: simplified sec 3.3 == v3.5 arithmetic ---")
    # The fork-14 removal is pinned as behavior-preserving HERE, forever: the
    # full v3.5 four-conjunct arithmetic (incl. the coupled-upper sd clauses)
    # is reconstructed from the frozen tables and swept against the live
    # band_cell on a seeded grid plus float-boundary-hugging probes at every
    # cutpoint of BOTH arithmetics. Expected differences: exactly 0.
    def _band_v35_reference(mu, sd, n, B, sig):
        df = n - 1
        two = sig is None
        t = (R["t_two_sided"] if two else R["t_one_sided"])[df]
        up = R["chi2_upper"][df]
        f_c, f_u = rule_floor(sd, B), rule_floor(sd * up, B)
        se_c, se_u = rule_se(sd, n), rule_se(sd * up, n)
        x = abs(mu) if two else sig * mu
        if x - t * se_c > f_c:
            return "GREEN"
        if (not two) and (x < -t * se_c):
            return "ANOMALOUS"
        aligned = (x + t * se_c < f_c) and (x + t * se_u < f_u)
        magnitude = (abs(mu) + t * se_c < f_c) and (abs(mu) + t * se_u < f_u)
        if aligned and magnitude:
            return "RED"
        return "AMBER"
    vrng = np.random.default_rng(20260713)
    vdiffs, vprobes = 0, 0
    for (vn, vB) in ((16, 96), (32, 96), (32, 128)):
        for vsig in (+1, -1, None):
            vt = (R["t_two_sided"] if vsig is None else R["t_one_sided"])[vn - 1]
            vup = R["chi2_upper"][vn - 1]
            for vsd in (0.5, 1.0, 2.0):
                vse, vfl = rule_se(vsd, vn), rule_floor(vsd, vB)
                vmus = list(vrng.uniform(-2.5 * vfl, 2.5 * vfl, 4000))
                for c0 in (vfl + vt * vse, vt * vse, vfl - vt * vse,
                           (vfl - vt * vse) * vup):
                    for veps in (-1e-9, 0.0, 1e-9):
                        vmus += [c0 + veps, -(c0 + veps)]
                for vmu in vmus:
                    vprobes += 1
                    if band_cell(float(vmu), vsd, vn, vB, vsig)[0] != \
                            _band_v35_reference(float(vmu), vsd, vn, vB, vsig):
                        vdiffs += 1
    check("verdict identity on frozen sweep (%d probes)" % vprobes, vdiffs, 0)

    print("# --- LAW #4: every prose threshold grepped against the frozen config ---")
    doc = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "v44_scout_DECISION_RULE_%s.md" % RULE["rule_version"])
    src = open(doc).read() if os.path.exists(doc) else None
    if src is None:
        print("#   [WARN] ratified doc not found next to the harness; grep skipped")
    f64, f128 = rule_floor(1.0, 64), rule_floor(1.0, 128)
    se8, se32, se56 = rule_se(1.0, 8), rule_se(1.0, 32), rule_se(1.0, 56)
    t15_2, t31, t31_2, t55 = (R["t_two_sided"][15], R["t_one_sided"][31],
                              R["t_two_sided"][31], R["t_one_sided"][55])
    derived = {
        "floor_96": f96, "floor_128": f128, "floor_64": f64,
        "se_8_96": se8, "se_16_96": se16, "se_32_96": se32, "se_56": se56,
        "green_16_96_1s": f96 + t15 * se16,
        "green_16_96_2s": f96 + t15_2 * se16,
        "kappa_16_96_1s": f96 - t15 * se16,
        "kappa_16_96_2s": f96 - t15_2 * se16,
        "kappa_32_96_1s": f96 - t31 * se32,
        "kappa_32_96_2s": f96 - t31_2 * se32,
        "kappa_32_128_1s": f128 - t31 * se32,
        "rerun_edge": t55 * se56,
        "kappa_56": f96 - t55 * se56,
    }
    for k, v in sorted(derived.items()):
        frozen = R[k]
        agree = abs(v - frozen) < 1.0e-3          # frozen values are 3-4 s.f.
        in_doc = (src is None) or (("%g" % abs(frozen)).lstrip("0") in src) \
                 or (str(abs(frozen)) in src)
        ok_k = agree and in_doc
        ok = ok and ok_k
        print("#   [%s] %-16s formula=%.5f frozen=%-7s in_ratified_doc=%s"
              % ("PASS" if ok_k else "FAIL", k, v, frozen, in_doc))
    for name, val in (("n_rerun", R["n_rerun"]), ("B_conf", R["B_conf"]),
                      ("B_max", R["B_max"]), ("Z", R["Z"]),
                      ("rerun_power", R["rerun_power"]),
                      ("blocks_first", R["blocks_first"]),
                      ("blocks_extended", R["blocks_extended"])):
        present = (src is None) or (str(val) in src)
        ok = ok and present
        print("#   [%s] %-16s frozen=%-7s in_ratified_doc=%s"
              % ("PASS" if present else "FAIL", name, val, present))
    # every t* and chi2 factor the rule fires with must be in the prose table
    for lbl, tab in (("t_one_sided", R["t_one_sided"]), ("t_two_sided", R["t_two_sided"]),
                     ("chi2_upper", R["chi2_upper"])):
        miss = [v for v in tab.values() if src is not None and str(v) not in src]
        ok = ok and not miss
        print("#   [%s] %-16s %s%s" % ("PASS" if not miss else "FAIL", lbl,
                                       sorted(tab.values()),
                                       "" if not miss else " MISSING FROM DOC: %s" % miss))
    # SUPERSEDED v3.4 constants must not appear as live values in this harness
    # (rule sec 10 stale-prose row): the n_rerun=40 rerun t*, SE, edge, kappa
    # and power figures, all superseded by v3.5's honest-model n_rerun=56.
    # Assembled from fragments so the check does not trip over its own source
    # (same reason as the forbidden-ceiling-label check above).
    stale = [s for s in ("1.6" + "85", "0.20" + "16", "0.3" + "40",
                         "0.2" + "17", "0.9" + "12")
             if s in open(__file__).read()]
    check("no superseded v3.4 rerun constants live in the harness", stale, [])

    # law #3 cross-check with scipy where available (NOT a harness dependency:
    # external replication seats run numpy-only and must still pass).
    try:
        from scipy.stats import t as _t, chi2 as _c2, nct as _nct
        errs = []
        for df, v in R["t_one_sided"].items():
            if abs(_t.ppf(0.95, df) - v) > 5e-4: errs.append(("t1s", df))
        for df, v in R["t_two_sided"].items():
            if abs(_t.ppf(0.975, df) - v) > 5e-4: errs.append(("t2s", df))
        for df, v in R["chi2_upper"].items():
            if abs(math.sqrt(df / _c2.ppf(0.05, df)) - v) > 5e-4: errs.append(("chi2", df))
        ncp = f96 / se56
        pw56 = float(_nct.sf(t55, 55, ncp))
        errs += [] if abs(pw56 - R["rerun_power"]) < 5e-3 else [("power", pw56)]
        check("scipy cross-check of the frozen t / chi2 / power tables", errs, [])
        print("#   n_rerun=56 honest noncentral-t power = %.4f (ncp=%.3f, target >= %.2f)"
              % (pw56, ncp, R["compound_power_target"]))
    except ImportError:
        print("#   [SKIP] scipy absent -- frozen tables are the source of truth")
    print("# RULE SELFTEST " + ("PASS" if ok else "FAIL"))
    return ok

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
    if a[0] == "--rule-selftest":
        # v4.4 decision-rule v3.5 only (fast; no physics). Full --selftest
        # runs this too.
        sys.exit(0 if _rule_selftest() else 1)
    if a[0] == "--pilot":
        pilot(); return
    if a[0] == "--pilot-pair":
        pilot_pair(); return
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
