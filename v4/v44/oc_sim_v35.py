#!/usr/bin/env python3
"""
v4.4 scout — OC confirmation (v3.5), canonical interpreter run.
Registration-grade core: full-ladder primary protection (gate 9 law-#3 compound),
reference-uncertain rerun alpha selftest, per-contrast rerun power.
Interpreter: /usr/bin/python3 (Python 3.9.6, numpy 2.0.2). Deterministic (seeded).
Estimand invariant: mu_hat = mean(B blocks) - mean(64-block reference), reference
REDRAWN each replication so numerator var = 1/B + 1/64 (the arbitration lesson).
"""
import numpy as np, math, json
from scipy.stats import t as tdist

SEED = 20260708
rng = np.random.default_rng(SEED)
SD, REF = 1.0, 64
FLOOR = {96: 3.858*math.sqrt(2/96), 128: 3.858*math.sqrt(2/128)}   # 0.5569, 0.4822
TCRIT = {16: tdist.ppf(0.95,15), 32: tdist.ppf(0.95,31), 56: tdist.ppf(0.95,55)}
UP = {16: 1.437, 32: 1.268}                                        # chi2 upper-sd factors

def band(mu, s, nb, Bconf, sigma=+1):
    """Vectorized four-band classify on ONE statistic (v3.5 sec.3, one-sided sigma=+)."""
    x = sigma*mu
    fc = FLOOR[Bconf]
    SE  = s*np.sqrt(1/nb + 1/REF)
    SEu = s*UP[nb]*np.sqrt(1/nb + 1/REF)
    t = TCRIT[nb]
    anom  = x < -t*SE
    green = (x - t*SE) > fc
    red   = (~anom) & (x+t*SE<fc) & (x+t*SEu<fc) & (np.abs(mu)+t*SE<fc) & (np.abs(mu)+t*SEu<fc)
    out = np.full(mu.shape, 'AMBER', dtype=object)
    out[red]='RED'; out[green]='GREEN'; out[anom]='ANOM'     # priority: RED<GREEN<ANOM (disjoint by construction)
    return out

def run_ladder(delta, sigma, N):
    """Full terminal ladder (16b/B96 -> 32b/B96 -> 32b/B128 -> INCONCLUSIVE), accumulation not redraw."""
    blk = rng.normal(delta, SD, (N, 32))            # 32 blocks; first 16 = look1, all 32 = look2/3
    ref = rng.normal(0, SD/math.sqrt(REF), N)       # one 64-block reference per replication (equal-arm true mean 0)
    term = np.full(N, 'PENDING', dtype=object)
    # look 1: 16 blocks @ B96
    m,s = blk[:,:16].mean(1)-ref, blk[:,:16].std(1,ddof=1)
    b = band(m,s,16,96,sigma)
    for lab in ('RED','GREEN','ANOM'): term[(term=='PENDING')&(b==lab)] = lab
    # look 2: 32 blocks @ B96 (only AMBER continues)
    m32,s32 = blk[:,:32].mean(1)-ref, blk[:,:32].std(1,ddof=1)
    b = band(m32,s32,32,96,sigma); c = term=='PENDING'
    for lab in ('RED','GREEN','ANOM'): term[c&(b==lab)] = lab
    # look 3: 32 blocks @ B128 (escalation ceiling)
    b = band(m32,s32,32,128,sigma); c = term=='PENDING'
    for lab in ('RED','GREEN','ANOM'): term[c&(b==lab)] = lab
    term[term=='PENDING'] = 'INCONCLUSIVE'
    return term

def rerun(delta, N):
    """Powered STATE-B rerun, n_rerun=56, reference-uncertain, one-sided wrong-sign fire."""
    blk = rng.normal(delta, SD, (N,56)); ref = rng.normal(0, SD/math.sqrt(REF), N)
    mu,s = blk.mean(1)-ref, blk.std(1,ddof=1)
    SE = s*np.sqrt(1/56 + 1/REF)
    return mu < -TCRIT[56]*SE

def dist(term):
    N=len(term); u,c=np.unique(term,return_counts=True); return {k:round(int(v)/N,5) for k,v in zip(u,c)}

if __name__ == '__main__':
    N   = 4_000_000
    floor = FLOOR[96]
    out = {"seed": SEED, "interpreter": "python3.9.6/numpy2.0.2", "N": N, "floor96": round(floor,5)}

    # --- reference-uncertain rerun ALPHA selftest (must be ~0.05, NOT ~0.019) ---
    a = rerun(0.0, N).mean();            out["rerun_H0_alpha"] = round(float(a),5)
    p = rerun(-floor, N).mean();         out["rerun_per_contrast_power_n56"] = round(float(p),5)

    # --- GATE 9 / law-#3 compound: primary protection vs a -1x floor wrong-sign current ---
    t_ws = run_ladder(-floor, +1, N)
    out["wrongsign_terminal_band_dist"] = dist(t_ws)
    p_red = (t_ws=='RED').mean()
    out["compound_full_union_protection"] = round(float(1-p_red),5)   # 1 - P(cleared to actual-RED)
    # disposition-only reading (the wrong event, for the record): anomaly-flag x rerun
    out["disposition_only_reading"] = round(float((t_ws=='ANOM').mean()*p), 5)

    # --- sanity gates ---
    out["gate1_false_GREEN_on_null_percell"]   = round(float((run_ladder(0.0,+1,N)=='GREEN').mean()),6)
    out["gate4_GREEN_power_at_+3xfloor"]        = round(float((run_ladder(+3*floor,+1,N)=='GREEN').mean()),5)

    print(json.dumps(out, indent=2))
    with open("v4/v44/oc_results_v35.json","w") as f: json.dump(out,f,indent=2)
    print("\nwrote v4/v44/oc_results_v35.json")
