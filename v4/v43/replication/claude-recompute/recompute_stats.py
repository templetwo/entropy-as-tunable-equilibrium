#!/usr/bin/env python3
"""Pre-declared independent statistics for the v4.3 matched-tau recompute.
Written BEFORE the full re-simulation finished and BEFORE reading any of
the original analysis outputs (v43_analysis.json, v4_analysis.json,
FORENSIC_AND_RESULTS, VERDICT files).

Inputs: recompute_results.pkl  (per-unit directed transition counts K,
        2D occupancy, step counts) produced by recompute_driver.py from
        archived seeds.

Declared tests
--------------
OCC-1  Occupancy shift, primary: per-block center of mass <x>,
       frozen (32) vs online (32), two-sided permutation on the
       difference of arm means, 20,000 permutations, seed 20260709.
OCC-2  Localization, secondary: per-bin occupancy-fraction difference,
       max-|t| across 24 bins with permutation null (same perms).
CIRC-1 Plaquette circulation, global: for each unit, antisymmetric
       net flow F(a->b) = K(a,b) - K(b,a) on nearest-neighbor edges;
       plaquette sum Gamma_p (CCW+); statistic = sum_p Gamma_p / n.
       Per-arm sign-flip permutation vs 0 (20,000 flips) + block-bootstrap
       95% CI (10,000 resamples).
CIRC-2 Same statistic restricted to the mouth ROI (x in [1.55,2.45],
       y in [0.55,1.45] -> the pre-registered ROI box).
CIRC-3 Contrast: online minus frozen on CIRC-1/CIRC-2, two-sided
       32v32 permutation.
EDGE-1 Detailed-balance edge contrast: per-edge net-flow rate
       f_e = F_e / n per unit; arm-mean difference d_e; global statistic
       max_e |d_e| / se_e (block bootstrap se), permutation null.
CTRL   Pipeline validity: CIRC-1/2 on C4v k8 (6 blocks) must reject 0
       with unanimous sign; k0 (2 blocks) must not be extreme.

Interpretation map (declared):
  Motor-free confirmation = OCC-1 rejects (shift real) AND CIRC-1/2/3
  consistent with 0 for both arms and contrast AND EDGE-1 null AND CTRL fires.
  Any CIRC/EDGE rejection in the online arm with CTRL firing = potential
  motor signal -> escalate before deposit.
"""
import pickle, json, math
import numpy as np

RNG = np.random.default_rng(20260709)
NX, NY = 24, 12
ROI_CELLS = [(i, j) for i in range(NX) for j in range(NY)
             if 1.55 <= (i + 0.5) * 4.0 / NX <= 2.45
             and 0.55 <= (j + 0.5) * 2.0 / NY <= 1.45]
ROI_SET = set(ROI_CELLS)

def unit_stats(rec):
    K = rec["K"]; n = rec["n"]
    F = {}
    for (a, b), k in K.items():
        if a < b:
            F[(a, b)] = k - K.get((b, a), 0)
    def edge_flow(a, b):
        if a < b:
            return F.get((a, b), 0)
        return -F.get((b, a), 0)
    gam_glob = 0.0; gam_roi = 0.0
    for i in range(NX - 1):
        for j in range(NY - 1):
            c00, c10 = (i, j), (i + 1, j)
            c11, c01 = (i + 1, j + 1), (i, j + 1)
            g = (edge_flow(c00, c10) + edge_flow(c10, c11)
                 + edge_flow(c11, c01) + edge_flow(c01, c00))
            gam_glob += g
            if c00 in ROI_SET and c11 in ROI_SET:
                gam_roi += g
    occ = rec["occ2d"].astype(float)
    px = occ.sum(axis=1) / occ.sum()
    xs = (np.arange(NX) + 0.5) * 4.0 / NX
    return {"com": float((px * xs).sum()), "px": px,
            "gam_glob": gam_glob / n, "gam_roi": gam_roi / n,
            "F": F, "n": n}

def perm_two_sample(a, b, n_perm=20000):
    a, b = np.asarray(a, float), np.asarray(b, float)
    obs = a.mean() - b.mean()
    pool = np.concatenate([a, b]); na = len(a)
    cnt = 0
    for _ in range(n_perm):
        RNG.shuffle(pool)
        d = pool[:na].mean() - pool[na:].mean()
        if abs(d) >= abs(obs) - 1e-18:
            cnt += 1
    return obs, (cnt + 1) / (n_perm + 1)

def signflip_p(x, n_perm=20000):
    x = np.asarray(x, float)
    obs = abs(x.mean())
    cnt = 0
    for _ in range(n_perm):
        s = RNG.choice([-1.0, 1.0], size=len(x))
        if abs((x * s).mean()) >= obs - 1e-18:
            cnt += 1
    return x.mean(), (cnt + 1) / (n_perm + 1)

def boot_ci(x, n_boot=10000):
    x = np.asarray(x, float)
    m = np.array([RNG.choice(x, len(x)).mean() for _ in range(n_boot)])
    return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))

def main():
    with open("recompute_results.pkl", "rb") as f:
        res = pickle.load(f)
    fam = lambda p: [unit_stats(res[u]) for u in sorted(res) if u.startswith(p)]
    FR = fam("C1m_frozen"); ON = fam("C1m_online")
    K8 = fam("C4v_frozen_k8"); K0 = fam("C4v_frozen_k0.0")
    bx = sum(1 for r in res.values() if r["bitexact"])
    print(f"bitexact (incl. 1-ulp libm tolerance): {bx}/{len(res)}")
    print()

    # ---- CTRL first: pipeline must be able to see a real current ----
    g8 = [u["gam_roi"] for u in K8]; g0 = [u["gam_roi"] for u in K0]
    m8, p8 = signflip_p(g8)
    print("CTRL  C4v k8 ROI circ: mean %.3e  sign %d/%d  sign-flip p=%.4f | k0: %s"
          % (m8, sum(1 for g in g8 if g * m8 > 0), len(g8), p8,
             ["%.1e" % g for g in g0]))
    print("CTRL  k8 global circ per unit:", ["%.1e" % u["gam_glob"] for u in K8])
    print()

    # ---- OCC-1 ----
    ca = [u["com"] for u in ON]; cb = [u["com"] for u in FR]
    d, p = perm_two_sample(ca, cb)
    print("OCC-1 <x> online %.5f  frozen %.5f  diff %+.5f  perm p=%.4f"
          % (np.mean(ca), np.mean(cb), d, p))
    # OCC-2
    PA = np.array([u["px"] for u in ON]); PB = np.array([u["px"] for u in FR])
    t = (PA.mean(0) - PB.mean(0)) / np.sqrt(PA.var(0, ddof=1) / 32 + PB.var(0, ddof=1) / 32)
    tmax_obs = np.max(np.abs(t))
    pool = np.vstack([PA, PB]); cnt = 0
    for _ in range(5000):
        idx = RNG.permutation(64)
        A, B = pool[idx[:32]], pool[idx[32:]]
        tt = (A.mean(0) - B.mean(0)) / np.sqrt(A.var(0, ddof=1) / 32 + B.var(0, ddof=1) / 32)
        if np.max(np.abs(tt)) >= tmax_obs - 1e-18:
            cnt += 1
    jb = int(np.argmax(np.abs(t)))
    print("OCC-2 max|t|=%.2f at bin %d (x~%.2f), perm p=%.4f"
          % (tmax_obs, jb, (jb + 0.5) * 4.0 / 24, (cnt + 1) / 5001))
    print()

    # ---- CIRC-1/2 ----
    for name, key in (("CIRC-1 global", "gam_glob"), ("CIRC-2 ROI   ", "gam_roi")):
        for arm, U in (("online", ON), ("frozen", FR)):
            x = [u[key] for u in U]
            m, p = signflip_p(x)
            lo, hi = boot_ci(x)
            print("%s %s: mean %+.3e  95%%CI [%+.3e, %+.3e]  sign-flip p=%.4f"
                  % (name, arm, m, lo, hi, p))
        d, p = perm_two_sample([u[key] for u in ON], [u[key] for u in FR])
        print("%s contrast online-frozen: %+.3e  perm p=%.4f" % (name, d, p))
    print()

    # ---- EDGE-1 ----
    edges = set()
    for U in (FR, ON):
        for u in U:
            edges |= set(u["F"].keys())
    edges = sorted(edges)
    def rates(U):
        M = np.zeros((len(U), len(edges)))
        for r, u in enumerate(U):
            for c, e in enumerate(edges):
                M[r, c] = u["F"].get(e, 0) / u["n"]
        return M
    RA, RB = rates(ON), rates(FR)
    dm = RA.mean(0) - RB.mean(0)
    se = np.sqrt(RA.var(0, ddof=1) / 32 + RB.var(0, ddof=1) / 32)
    ok = se > 0
    zmax_obs = np.max(np.abs(dm[ok] / se[ok]))
    pool = np.vstack([RA, RB]); cnt = 0
    for _ in range(2000):
        idx = RNG.permutation(64)
        A, B = pool[idx[:32]], pool[idx[32:]]
        d2 = A.mean(0) - B.mean(0)
        s2 = np.sqrt(A.var(0, ddof=1) / 32 + B.var(0, ddof=1) / 32)
        o2 = s2 > 0
        if np.max(np.abs(d2[o2] / s2[o2])) >= zmax_obs - 1e-18:
            cnt += 1
    print("EDGE-1 %d edges, max|z| = %.2f, perm p=%.4f"
          % (int(ok.sum()), zmax_obs, (cnt + 1) / 2001))

if __name__ == "__main__":
    main()
