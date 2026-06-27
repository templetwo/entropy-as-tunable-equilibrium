"""
landscape.py
============
Potential landscapes and their gradients.

  dumbbell_1d  : the validated Phase 0 landscape (two wells).
  U2d / dU2d   : the 2D chamber-channel-chamber landscape for Arms B/C.

All potentials are plain functions of position arrays so they work with NumPy now
and can be wrapped with jax.numpy on the Studio (the math is identical; swap the
import and jit/vmap the samplers in causal_entropy.py).
"""
import numpy as np
from dataclasses import dataclass


# --------------------------------------------------------------------------- #
# 1D dumbbell (Phase 0)
# --------------------------------------------------------------------------- #
@dataclass
class Dumbbell1D:
    a_center: float = -2.5
    a_depth: float = 4.0
    a_width: float = 0.5     # narrow, deep -> option-poor trap
    b_center: float = 2.5
    b_depth: float = 3.0
    b_width: float = 1.5     # wide, shallow -> option-rich basin
    xl: float = -5.0
    xr: float = 5.0

    def U(self, x):
        a = -self.a_depth * np.exp(-((x - self.a_center) ** 2) / (2 * self.a_width ** 2))
        b = -self.b_depth * np.exp(-((x - self.b_center) ** 2) / (2 * self.b_width ** 2))
        return a + b

    def dU(self, x):
        a = -self.a_depth * np.exp(-((x - self.a_center) ** 2) / (2 * self.a_width ** 2)) * (-(x - self.a_center) / self.a_width ** 2)
        b = -self.b_depth * np.exp(-((x - self.b_center) ** 2) / (2 * self.b_width ** 2)) * (-(x - self.b_center) / self.b_width ** 2)
        return a + b

    def reflect(self, x):
        x = np.where(x < self.xl, 2 * self.xl - x, x)
        x = np.where(x > self.xr, 2 * self.xr - x, x)
        return np.clip(x, self.xl, self.xr)


# --------------------------------------------------------------------------- #
# 2D chamber-channel-chamber (Arms B/C)
# --------------------------------------------------------------------------- #
@dataclass
class ChamberChannel2D:
    """Small deep chamber (left) + large shallow chamber (right) + a high wall
    pierced by a narrow channel. Channel length L_ch (wall thickness in x) and
    width w_ch (gap in y) are the knobs Arm C sweeps.

      U = -d_S exp(-((x+xc)^2 + y^2)/(2 r_S^2))        # small, deep, thermally favored
          -d_L exp(-((x-xc)^2 + y^2)/(2 r_L^2))        # large, shallow, option-rich
          + B0 * wall_x(x) * gap_y(y)                  # wall with a channel gap
        wall_x(x) = exp(-x^2 / (2 (L_ch/2)^2))
        gap_y(y)  = 1 - exp(-y^2 / (2 (w_ch/2)^2))
    """
    xc: float = 3.5
    # Tuned (executor, MacBook seat) so the THERMAL control favors the small
    # chamber (P_L_control ~ 0.35) — the prior SPEC defaults (d_S=4, r_S=0.7,
    # d_L=3) had the wide well win on volume (P_L_control ~ 0.67, backwards).
    # The large chamber stays option-rich (area ratio r_L^2/r_S^2 = 9), so the
    # engine's tau-driven migration into it is a real effect, not a thermal
    # default. tau* is NOT tuned — Arm C's scaling across L_ch is the claim.
    d_S: float = 5.5
    r_S: float = 0.6
    d_L: float = 2.0
    r_L: float = 1.8
    B0: float = 8.0
    L_ch: float = 1.5        # channel length  (Arm C primary sweep)
    w_ch: float = 0.8        # channel width   (Arm C secondary sweep)
    xl: float = -6.0
    xr: float = 6.0
    yl: float = -4.0
    yr: float = 4.0

    # --- potential ---
    def U(self, x, y):
        small = -self.d_S * np.exp(-(((x + self.xc) ** 2) + y ** 2) / (2 * self.r_S ** 2))
        large = -self.d_L * np.exp(-(((x - self.xc) ** 2) + y ** 2) / (2 * self.r_L ** 2))
        wall_x = np.exp(-(x ** 2) / (2 * (self.L_ch / 2) ** 2))
        gap_y = 1.0 - np.exp(-(y ** 2) / (2 * (self.w_ch / 2) ** 2))
        return small + large + self.B0 * wall_x * gap_y

    # --- analytic gradient (use for the natural-dynamics drift) ---
    def grad_U(self, x, y):
        small = -self.d_S * np.exp(-(((x + self.xc) ** 2) + y ** 2) / (2 * self.r_S ** 2))
        large = -self.d_L * np.exp(-(((x - self.xc) ** 2) + y ** 2) / (2 * self.r_L ** 2))
        dsmall_dx = small * (-(x + self.xc) / self.r_S ** 2)
        dsmall_dy = small * (-(y) / self.r_S ** 2)
        dlarge_dx = large * (-(x - self.xc) / self.r_L ** 2)
        dlarge_dy = large * (-(y) / self.r_L ** 2)
        wall_x = np.exp(-(x ** 2) / (2 * (self.L_ch / 2) ** 2))
        gap_y = 1.0 - np.exp(-(y ** 2) / (2 * (self.w_ch / 2) ** 2))
        dwall_dx = wall_x * (-x / (self.L_ch / 2) ** 2)
        dgap_dy = np.exp(-(y ** 2) / (2 * (self.w_ch / 2) ** 2)) * (y / (self.w_ch / 2) ** 2)
        dUdx = dsmall_dx + dlarge_dx + self.B0 * dwall_dx * gap_y
        dUdy = dsmall_dy + dlarge_dy + self.B0 * wall_x * dgap_dy
        return np.stack([dUdx, dUdy], axis=-1)

    def reflect(self, p):
        x, y = p[..., 0], p[..., 1]
        x = np.where(x < self.xl, 2 * self.xl - x, x)
        x = np.where(x > self.xr, 2 * self.xr - x, x)
        y = np.where(y < self.yl, 2 * self.yl - y, y)
        y = np.where(y > self.yr, 2 * self.yr - y, y)
        x = np.clip(x, self.xl, self.xr)
        y = np.clip(y, self.yl, self.yr)
        return np.stack([x, y], axis=-1)

    def in_large_chamber(self, p):
        """Boolean mask: points belonging to the large chamber (x > 0 half-plane,
        a simple and defensible partition since the wall sits at x=0)."""
        return p[..., 0] > 0.0
