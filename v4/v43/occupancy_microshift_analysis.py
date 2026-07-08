#!/usr/bin/env python3
"""
Dedicated look at the v4.3 occupancy micro-shift — the program's one live positive.

Question (Anthony, 2026-07-08): is the confirmed frozen-vs-online occupancy shift
(v4.3 OCC: p=0.0236, TV=0.010 at B=32, matched tau/M) a real nonequilibrium/engine
signature, or an estimation/numerical artifact?

Method: read the CANONICAL v43_run.ndjson, extract the 32 frozen + 32 online C1m
occupancy distributions, and run two diagnostics:
  (1) WHERE the ~1% shift lives across the 24 x-bins (single-bin/boundary artifact
      screen) + per-bin significance.
  (2) The detailed-balance discriminator: signed LOOP circulation (quad_loop_rate,
      omega_roi, mouth_loop_rate) within each arm and frozen-vs-online. A shift
      accompanied by broken detailed balance (a loop current in online that frozen
      lacks) would be a real nonequilibrium signature; a shift with NO circulation
      difference and both arms current-free is a difference between two near-
      equilibrium force fields (interpolated-frozen vs pointwise-online) = numerical.

Interpreter: /usr/bin/python3 (numpy 2.0.2). Reads only; deterministic perm test.
"""
import json, numpy as np

RUN = "v43_run.ndjson"

def load():
    rows = {}
    with open(RUN) as f:
        for line in f:
            line = line.strip()
            if line:
                r = json.loads(line); rows[r["unit"]] = r
    return rows

def perm_p(a, b, nperm=20000, seed=7):
    a, b = np.asarray(a, float), np.asarray(b, float)
    obs = abs(a.mean() - b.mean())
    pool = np.concatenate([a, b]); n = len(a)
    rng = np.random.default_rng(seed); c = 0
    for _ in range(nperm):
        rng.shuffle(pool)
        if abs(pool[:n].mean() - pool[n:].mean()) >= obs - 1e-15:
            c += 1
    return (c + 1) / (nperm + 1)

def scal(rows, u, path):
    d = rows[u]["data"]
    for p in path.split("."):
        d = d[p]
    return float(d)

def main():
    rows = load()
    frz = sorted(u for u in rows if u.startswith("C1m_frozen"))
    onl = sorted(u for u in rows if u.startswith("C1m_online"))
    assert len(frz) == len(onl) == 32, (len(frz), len(onl))

    # (1) per-bin occupancy shift
    OF = np.array([(lambda v: v / v.sum())(np.array(rows[u]["data"]["occupancy_x"], float)) for u in frz])
    OO = np.array([(lambda v: v / v.sum())(np.array(rows[u]["data"]["occupancy_x"], float)) for u in onl])
    mf, mo = OF.mean(0), OO.mean(0); diff = mo - mf
    tv = 0.5 * np.abs(diff).sum()
    se = np.sqrt(OF.var(0, ddof=1) / 32 + OO.var(0, ddof=1) / 32)
    z = diff / se
    order = np.argsort(-np.abs(diff))
    top3_share = np.abs(diff[order[:3]]).sum() / (2 * tv)
    sig_bins = [(int(b), round(float(z[b]), 2)) for b in range(len(z)) if abs(z[b]) > 2]

    print("=== (1) OCCUPANCY SHIFT LOCATION ===")
    print(f"TV(frozen,online) = {tv:.6f}  (v43_analysis.json: 0.009989)")
    print(f"bins = {len(mf)}; top-3 bins {order[:3].tolist()} carry {top3_share*100:.0f}% of the shift")
    print(f"per-bin |z|>2: {sig_bins}")
    print(f"single-bin/boundary artifact? {'NO — distributed' if top3_share < 0.6 else 'possible — concentrated'}")

    # (2) detailed-balance discriminator
    print("\n=== (2) DETAILED-BALANCE DISCRIMINATOR (signed loop circulation) ===")
    circ = ["quad.quad_loop_rate", "roij.omega_roi", "mouth.mouth_loop_rate"]
    print(f"{'observable':22} {'frozen z':>9} {'online z':>9} {'fr-vs-on p':>11}")
    both_zero = True; no_diff = True
    for key in circ:
        F = np.array([scal(rows, u, key) for u in frz])
        O = np.array([scal(rows, u, key) for u in onl])
        zf = F.mean() / (F.std(ddof=1) / np.sqrt(32))
        zo = O.mean() / (O.std(ddof=1) / np.sqrt(32))
        p = perm_p(F, O)
        both_zero &= (abs(zf) < 2 and abs(zo) < 2)
        no_diff &= (p > 0.05)
        print(f"{key:22} {zf:+9.2f} {zo:+9.2f} {p:11.4f}")

    print("\n=== VERDICT ===")
    if both_zero and no_diff:
        print("Both arms loop-current-free AND no frozen-vs-online circulation difference.")
        print("-> occupancy shift is a ~1% difference between two NEAR-EQUILIBRIUM force")
        print("   fields (interpolated-frozen vs pointwise-online): estimation/numerical,")
        print("   NOT a nonequilibrium engine signature.")
    else:
        print("Circulation signal or frozen-vs-online circulation difference present ->")
        print("   possible broken-detailed-balance signature; escalate.")
    print("\nCAVEAT: circulation comparison is at the same modest B=32 power. Definitive")
    print("closer (needs a NEW run, not in this data): M_grid / M_online sweep — shift->0")
    print("as M->inf = pure numerical convergence error; persists = genuine frozen-vs-")
    print("online estimator distinction (still equilibrium, still not the engine).")

if __name__ == "__main__":
    main()
