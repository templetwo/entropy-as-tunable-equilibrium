#!/usr/bin/env python3
"""v4.1 block-level analysis of record (post-audit).
Seed blocks are the independent units; nulls from permutation of 32 block labels.
Reproduces: FPT block-KS p, occupancy block perm p + TV, C2 two-sample z +
block perm p + Holm, C3 exact slopes + block bootstrap CI.
Usage: python3 v41_blocklevel.py v41_run.ndjson
"""
import json, sys, numpy as np
from random import Random

def load(p):
    rows = {}
    for l in open(p):
        if l.strip().startswith('{'):
            d = json.loads(l); rows[d['unit']] = d
    return rows

def block_perm(A, B, stat, Bn=20000, seed=123):
    allb = A + B; nf = len(A)
    obs = stat(A, B); rng = Random(seed); ex = 0
    idx = list(range(len(allb)))
    for _ in range(Bn):
        pm = rng.sample(idx, nf); s = set(pm)
        if stat([allb[i] for i in pm], [allb[i] for i in idx if i not in s]) >= obs:
            ex += 1
    return obs, (ex + 1) / (Bn + 1)

def main(path):
    rows = load(path)
    def tb(mode, tau):
        return [np.array(rows[f'C1_{mode}_tau{tau}_sb{i}']['data']['fpt']['times']) for i in range(16)]
    def ob(mode, tau):
        out = []
        for i in range(16):
            v = np.array(rows[f'C1_{mode}_tau{tau}_sb{i}']['data']['occupancy_x'], float)
            out.append(v / v.sum())
        return out
    def occ_chi2(A, B):
        pa = np.mean(A, 0); pb = np.mean(B, 0)
        return float(np.sum((pa - pb) ** 2 / (pa + pb + 1e-12)))
    print("== C1 block-level ==")
    for tau in ['0.25', '0.5', '1.0', '2.0']:
        F, O = tb('frozen', tau), tb('online', tau)
        allt = np.sort(np.concatenate(F + O))
        grid = allt[np.linspace(0, len(allt) - 1, 400).astype(int)]
        E = np.array([np.searchsorted(np.sort(t), grid, side='right') / len(t) for t in (F + O)])
        # vectorized KS over precomputed ECDFs
        idx = list(range(32)); rng = Random(123)
        obs = float(np.max(np.abs(E[:16].mean(0) - E[16:].mean(0)))); ex = 0
        for _ in range(20000):
            pm = rng.sample(idx, 16); s = set(pm)
            if float(np.max(np.abs(E[pm].mean(0) - E[[i for i in idx if i not in s]].mean(0)))) >= obs:
                ex += 1
        pks = (ex + 1) / 20001
        _, pocc = block_perm(ob('frozen', tau), ob('online', tau), occ_chi2)
        of = np.mean(ob('frozen', tau), 0); oo = np.mean(ob('online', tau), 0)
        tv = 0.5 * np.abs(of - oo).sum()
        fm = [t.mean() for t in F]; om = [t.mean() for t in O]
        g = (np.mean(om) - np.mean(fm)) / np.sqrt((np.var(fm, ddof=1) + np.var(om, ddof=1)) / 2)
        print(f"tau={tau}: KS={obs:.4f} p_blk={pks:.5f} | shift={np.mean(om)-np.mean(fm):+.3f} g={g:.2f} "
              f"| occ p_blk={pocc:.5f} TV={tv:.4f}")
    print("== C2 block-level ==")
    ps = []
    for tau in ['0.25', '0.5', '1.0', '2.0']:
        vf = [rows[f'C1_frozen_tau{tau}_sb{i}']['data']['mouth']['mouth_loop_rate'] for i in range(16)]
        vo = [rows[f'C1_online_tau{tau}_sb{i}']['data']['mouth']['mouth_loop_rate'] for i in range(16)]
        z2 = (np.mean(vo) - np.mean(vf)) / np.sqrt(np.var(vo, ddof=1) / 16 + np.var(vf, ddof=1) / 16)
        _, p = block_perm([[v] for v in vf], [[v] for v in vo],
                          lambda A, B: abs(np.mean([b[0] for b in B]) - np.mean([a[0] for a in A])))
        ps.append(p); print(f"tau={tau}: z2SE={z2:+.2f} p_blk={p:.4f}")
    order = np.argsort(ps); holm = [0.0] * 4; run = 0.0
    for r, i in enumerate(order):
        run = max(run, min(1.0, (4 - r) * ps[i])); holm[i] = run
    print("Holm:", [f'{h:.3f}' for h in holm])
    print("== C3 exact ==")
    Ls = [0.15, 0.3, 0.6, 1.2]
    means = {L: [rows[f'C3t_frozen_L{L}_tau1.0_sb{i}']['data']['fpt']['mean'] for i in range(4)] for L in Ls}
    T = np.array([np.mean(means[L]) for L in Ls]); L = np.array(Ls)
    print(f"nominal slope {np.polyfit(np.log(L), np.log(T), 1)[0]:.3f} | "
          f"effective {np.polyfit(np.log(L + 0.2), np.log(T), 1)[0]:.3f}")
    rng = np.random.default_rng(11); sl = []
    for _ in range(4000):
        Tb = [np.mean(rng.choice(means[l], 4, replace=True)) for l in Ls]
        sl.append(np.polyfit(np.log(L + 0.2), np.log(Tb), 1)[0])
    lo, hi = np.percentile(sl, [2.5, 97.5])
    print(f"effective-slope 95% CI [{lo:.3f}, {hi:.3f}]")

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'v41_run.ndjson')
