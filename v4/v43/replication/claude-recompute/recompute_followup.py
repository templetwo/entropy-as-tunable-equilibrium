#!/usr/bin/env python3
"""Follow-up: (a) OCC-2 with the NaN bug fixed (declared statistic, corrected
implementation: zero-variance wall bins masked), (b) post-hoc diagnostics
(labeled as such) to classify the EDGE-1 p=0.041 signal: localization of
top-|z| edges, orientation, and whether the online-frozen difference flow
field is transport-aligned (occupancy-shift echo) or loop-forming (motor)."""
import pickle
import numpy as np

RNG = np.random.default_rng(20260710)
NX, NY = 24, 12

with open("recompute_results.pkl", "rb") as f:
    res = pickle.load(f)

def px24(rec):
    occ = rec["occ2d"].astype(float)
    return occ.sum(axis=1) / occ.sum()

ON = [res[u] for u in sorted(res) if u.startswith("C1m_online")]
FR = [res[u] for u in sorted(res) if u.startswith("C1m_frozen")]
PA = np.array([px24(r) for r in ON]); PB = np.array([px24(r) for r in FR])

# ---- OCC-2 fixed: mask bins with zero pooled variance ----
va = PA.var(0, ddof=1); vb = PB.var(0, ddof=1)
valid = (va + vb) > 0
se = np.sqrt(va / 32 + vb / 32)
t = np.zeros(NX); t[valid] = (PA.mean(0) - PB.mean(0))[valid] / se[valid]
tmax_obs = np.max(np.abs(t[valid]))
pool = np.vstack([PA, PB]); cnt = 0
for _ in range(10000):
    idx = RNG.permutation(64)
    A, B = pool[idx[:32]], pool[idx[32:]]
    v2 = (A.var(0, ddof=1) + B.var(0, ddof=1)) > 0
    s2 = np.sqrt(A.var(0, ddof=1) / 32 + B.var(0, ddof=1) / 32)
    tt = np.abs(A.mean(0) - B.mean(0))[v2] / s2[v2]
    if tt.max() >= tmax_obs - 1e-18:
        cnt += 1
jb = int(np.argmax(np.abs(np.where(valid, t, 0))))
print("OCC-2fix valid bins %d/24, max|t|=%.2f at bin %d (x in [%.2f,%.2f]), perm p=%.4f"
      % (valid.sum(), tmax_obs, jb, jb * 4 / 24, (jb + 1) * 4 / 24, (cnt + 1) / 10001))
d = PA.mean(0) - PB.mean(0)
print("per-bin diff (online-frozen), t-value where |t|>2:")
for b in range(NX):
    if valid[b] and abs(t[b]) > 2:
        print("  bin %2d x[%.2f,%.2f]  diff %+0.5f  t=%+.2f"
              % (b, b * 4 / 24, (b + 1) * 4 / 24, d[b], t[b]))

# ---- EDGE diagnostics (post hoc) ----
def netflows(rec):
    K = rec["K"]; F = {}
    for (a, b), k in K.items():
        if a < b:
            F[(a, b)] = k - K.get((b, a), 0)
    return F
for r in ON + FR:
    r["F"] = netflows(r)
edges = set()
for r in ON + FR:
    edges |= set(r["F"].keys())
edges = sorted(edges)
def rates(U):
    M = np.zeros((len(U), len(edges)))
    for i, r in enumerate(U):
        for c, e in enumerate(edges):
            M[i, c] = r["F"].get(e, 0) / r["n"]
    return M
RA, RB = rates(ON), rates(FR)
dm = RA.mean(0) - RB.mean(0)
sed = np.sqrt(RA.var(0, ddof=1) / 32 + RB.var(0, ddof=1) / 32)
ok = sed > 0
z = np.zeros(len(edges)); z[ok] = dm[ok] / sed[ok]
order = np.argsort(-np.abs(z))[:8]
print("\ntop-|z| edges (online-frozen net-flow difference):")
for c in order:
    (a, b) = edges[c]
    ori = "x" if a[1] == b[1] else ("y" if a[0] == b[0] else "diag")
    xm = (a[0] + b[0] + 1) / 2 * 4 / NX
    ym = (a[1] + b[1] + 1) / 2 * 2 / NY
    print("  %s->%s  z=%+.2f  orient=%s  at (%.2f,%.2f)  dflow=%+.2e"
          % (a, b, z[c], ori, xm, ym, dm[c]))

# loop-forming check around the single max edge: plaquette sums of the
# DIFFERENCE field in a 3x3 cell neighborhood of that edge
c = order[0]; (a, b) = edges[c]
ci, cj = a
Fd = {}
for cc, e in enumerate(edges):
    Fd[e] = dm[cc]
def dflow(p, q):
    return Fd.get((p, q), 0) - Fd.get((q, p), 0)
tot_loops = []
for i in range(max(0, ci - 2), min(NX - 1, ci + 2)):
    for j in range(max(0, cj - 2), min(NY - 1, cj + 2)):
        g = (dflow((i, j), (i + 1, j)) + dflow((i + 1, j), (i + 1, j + 1))
             + dflow((i + 1, j + 1), (i, j + 1)) + dflow((i, j + 1), (i, j)))
        tot_loops.append(g)
print("\nneighborhood plaquette sums of difference field near max edge:")
print("  " + " ".join("%+.1e" % g for g in tot_loops))
print("  (loop-forming motor => coherent same-sign plaquettes; "
      "transport echo => near-zero/incoherent)")

# transport-alignment: correlate x-oriented edge diffs with local occupancy
# gradient difference (reset-flux echo prediction)
xdiffs = []; occg = []
occA = np.mean([r["occ2d"] / r["occ2d"].sum() for r in ON], axis=0)
occB = np.mean([r["occ2d"] / r["occ2d"].sum() for r in FR], axis=0)
docc = occA - occB
for cc, e in enumerate(edges):
    (p, q) = e
    if p[1] == q[1] and abs(p[0] - q[0]) == 1 and ok[cc]:
        xdiffs.append(dm[cc])
        occg.append(docc[max(p[0], q[0]), p[1]] - docc[min(p[0], q[0]), p[1]])
xdiffs = np.array(xdiffs); occg = np.array(occg)
r = np.corrcoef(xdiffs, occg)[0, 1]
print("\ncorr(x-edge flow diff, local d(occupancy-diff)/dx): r=%.3f (n=%d)" % (r, len(xdiffs)))
