"""
causal_entropy.py
=================
Causal path entropy S_c(x, tau) and the causal entropic force F_ce = T_c grad S_c.

Landscape-agnostic: pass a drift function and a reflect function, so the same code
serves the validated 1D dumbbell and the 2D chamber-channel-chamber.

Estimators (see SPEC.md §3):
  - sc_endpoint   : Shannon entropy of REACHABLE ENDPOINTS after horizon tau   (PRIMARY)
  - sc_occupancy  : Shannon entropy of ALL VISITED positions across the ensemble (robustness)

PERFORMANCE NOTE for the Studio:
  These NumPy versions are correct and fine for 1D and small 2D grids. For the full
  2D sweeps (Arms B/C), reimplement `forward_paths` with JAX: vmap over the N paths,
  jit the step, lax.scan over substeps, and batch the grid points. The math is
  identical; only the executor changes. Keep this NumPy path as a cross-check oracle
  on small cases.
"""
import numpy as np


# --------------------------------------------------------------------------- #
# forward path sampling under NATURAL (uncontrolled) dynamics
# --------------------------------------------------------------------------- #
def forward_paths(x0, n_sub, n_paths, drift_fn, reflect_fn, D, dt, rng, dim=1, record="endpoint"):
    """Evolve n_paths overdamped-Langevin paths of length n_sub from x0.

    drift_fn(p)   -> deterministic drift (= -grad_U / gamma), same shape as p
    reflect_fn(p) -> p reflected into the domain
    record        -> "endpoint" returns final positions (n_paths, dim)
                     "full"     returns all visited (n_paths, n_sub, dim)
    """
    x0 = np.asarray(x0, dtype=float)
    if dim == 1:
        p = np.full((n_paths,), float(x0))
    else:
        p = np.broadcast_to(x0, (n_paths, dim)).copy()
    sd = np.sqrt(2 * D * dt)
    if record == "full":
        store = np.empty((n_paths,) + ((n_sub,) if dim == 1 else (n_sub, dim)))
    for t in range(n_sub):
        noise = sd * rng.standard_normal(p.shape)
        p = p + drift_fn(p) * dt + noise
        p = reflect_fn(p)
        if record == "full":
            store[:, t] = p
    return store if record == "full" else p


# --------------------------------------------------------------------------- #
# entropy estimators
# --------------------------------------------------------------------------- #
def _entropy_1d(samples, bins, rng_range):
    hist, _ = np.histogram(samples, bins=bins, range=rng_range)
    p = hist / hist.sum()
    p = p[p > 0]
    return float(-np.sum(p * np.log(p)))


def _entropy_2d(samples, bins, rng_range):
    hist, _, _ = np.histogram2d(samples[..., 0].ravel(), samples[..., 1].ravel(),
                                bins=bins, range=rng_range)
    p = hist / hist.sum()
    p = p[p > 0]
    return float(-np.sum(p * np.log(p)))


def sc_endpoint(x0, n_sub, n_paths, drift_fn, reflect_fn, D, dt, rng,
                dim=1, bins=44, rng_range=None):
    """PRIMARY estimator: entropy of reachable endpoints x(tau)."""
    ends = forward_paths(x0, n_sub, n_paths, drift_fn, reflect_fn, D, dt, rng, dim, record="endpoint")
    return _entropy_1d(ends, bins, rng_range) if dim == 1 else _entropy_2d(ends, bins, rng_range)


def sc_occupancy(x0, n_sub, n_paths, drift_fn, reflect_fn, D, dt, rng,
                 dim=1, bins=44, rng_range=None):
    """ROBUSTNESS estimator: entropy of all visited positions across the ensemble."""
    full = forward_paths(x0, n_sub, n_paths, drift_fn, reflect_fn, D, dt, rng, dim, record="full")
    return _entropy_1d(full, bins, rng_range) if dim == 1 else _entropy_2d(full, bins, rng_range)


# --------------------------------------------------------------------------- #
# S_c field over a grid + force field + analytic steady state
# --------------------------------------------------------------------------- #
def sc_field_1d(grid, n_sub, n_paths, drift_fn, reflect_fn, D, dt, seed, estimator=sc_endpoint,
                seeds=2, bins=44, rng_range=None):
    """Compute S_c over a 1D grid (averaged over `seeds` seeds for stability)."""
    out = np.zeros(len(grid))
    for s in range(seeds):
        rng = np.random.default_rng(seed + 131 * s)
        for j, x0 in enumerate(grid):
            out[j] += estimator(x0, n_sub, n_paths, drift_fn, reflect_fn, D, dt, rng,
                                dim=1, bins=bins, rng_range=rng_range)
    return out / seeds


def force_field_from_sc(sc_values, grid, T_c=1.0):
    """Causal entropic force F_ce = T_c * dS_c/dx  (1D finite difference)."""
    return T_c * np.gradient(sc_values, grid)


def analytic_steady_state(sc_values, grid, beta_T_c):
    """p_engine ∝ exp(beta * T_c * S_c). Valid only if the force is conservative
    (Arm A must confirm). Returns a normalized density over `grid`."""
    e = beta_T_c * (sc_values - np.max(sc_values))
    p = np.exp(e)
    return p / np.trapezoid(p, grid)


# --------------------------------------------------------------------------- #
# Arm A: drive a particle under F_ce and histogram (the conservativeness check)
# --------------------------------------------------------------------------- #
def driven_steady_state_1d(force_interp, reflect_fn, D, dt, n_particles, n_steps,
                           x_init, grid_edges, seed=0, burn_frac=0.2):
    """Drive overdamped Langevin particles under an EXTERNAL force field F_ce
    (replacing -grad_U), histogram the post-burn-in occupancy. Compare the result
    to analytic_steady_state(...) to test conservativeness (SPEC.md §5).

    force_interp(x) -> F_ce at x (e.g. np.interp against the precomputed force field)
    """
    rng = np.random.default_rng(seed)
    x = np.full(n_particles, float(x_init))
    sd = np.sqrt(2 * D * dt)
    burn = int(burn_frac * n_steps)
    samples = []
    for t in range(n_steps):
        x = x + force_interp(x) * dt + sd * rng.standard_normal(n_particles)
        x = reflect_fn(x)
        if t >= burn:
            samples.append(x.copy())
    samples = np.concatenate(samples)
    hist, edges = np.histogram(samples, bins=grid_edges, density=True)
    centers = 0.5 * (edges[:-1] + edges[1:])
    return centers, hist


# --------------------------------------------------------------------------- #
# metrics
# --------------------------------------------------------------------------- #
def kl_divergence(p, q, grid):
    p = p / np.trapezoid(p, grid)
    q = q / np.trapezoid(q, grid)
    m = p > 0
    return float(np.trapezoid(np.where(m, p * np.log(p / np.maximum(q, 1e-300)), 0.0), grid))


def mass_in_region(p, grid, mask):
    return float(np.trapezoid(p[mask], grid[mask]) / np.trapezoid(p, grid))
