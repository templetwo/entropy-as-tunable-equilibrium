#!/usr/bin/env /usr/bin/python3
"""DIAG 3 — signal-fidelity M-sweep (PILOT; registers nothing).

Injects a KNOWN vortex (registered c4v arms k=4, k=8) and measures the REALIZED
response at M=400 vs M=2000 (+ higher-M convergence spot-check). The quantity of
interest is the RATIO of realized mean increments (attenuation factor), NOT the SD
(the SD/floor question was already answered by DIAG 1, receipt 06: floor is
trajectory-limited).

Seed namespace: diag10::  (throwaway diagnostic, QUARANTINED from v44pilot:: and
v43::; never pooled — Law #6).

Harness: PRISTINE unedited v44_scout.py, source_sha 0b65a9ee92b9fe2c...,
imported from a snapshot copy so later edits to the worktree cannot affect this run.
CFG is NEVER edited; M is passed via the M_grid_ov override (config_hash stays
a344d6c47c8a22c1 — verified).

CRN: vortex_kappa consumes no RNG and frozen_grid is built before the loop without
seeing kappa, so k0/k4/k8 at the same (M, block) share an identical grid AND an
identical trajectory-noise stream. The paired difference d_i = y_i(k) - y_i(0) is
therefore a common-random-numbers estimator: same expectation, far lower variance.
Seeds differ across M (the RNG stream diverges once frozen_grid's draw count changes,
so the M arms are treated as independent).
"""
import sys, os, json, time, hashlib, argparse
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import v44_scout_pristine as V   # pinned snapshot

SEED_NS = "diag10::"
SCALE = 10.0
TAU = float(os.environ.get("DIAG3_TAU", "1.0"))
TAU_Y = float(os.environ.get("DIAG3_TAUY", "1.0"))
TC = 1.0


def diag_seed(unit_id):
    """Mirrors the harness's own seed convention, in the quarantined diag10:: namespace."""
    h = hashlib.sha256((SEED_NS + unit_id).encode()).digest()
    return int.from_bytes(h[:8], "big")


def unit_id(M, i):
    # NOTE: kappa deliberately NOT in the unit id -> same seed across kappa = CRN.
    return f"sigfid::tx{TAU:g}::ty{TAU_Y:g}::M{M}::b{i}"


def run_block(job):
    M, k, i = job
    uid = unit_id(M, i)
    seed = diag_seed(uid)
    t0 = time.time()
    res = V.run_chamber("frozen", TAU, seed, scale=SCALE, tau_y=TAU_Y,
                        M_grid_ov=M, Tc_ov=TC, vortex_kappa=k)
    return {
        "type": "diag3_signal_fidelity",
        "namespace": SEED_NS,
        "unit": uid, "M": M, "kappa": k, "block": i, "seed": seed,
        "tau": TAU, "tau_y": TAU_Y, "Tc": TC, "scale": SCALE,
        "config_hash": V.config_hash(), "version": V.VERSION,
        "source_sha": SRC_SHA,
        "quad_loop_rate": float(res["quad"]["quad_loop_rate"]),
        "omega_roi": float(res["roij"]["omega_roi"]),
        "secs": round(time.time() - t0, 2),
    }


def load_done(path):
    done = set()
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                r = json.loads(line)
                done.add((r["M"], r["kappa"], r["block"]))
    return done


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ndjson", required=True)
    ap.add_argument("--n", type=int, required=True, help="blocks per (M,kappa) cell")
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--cells", required=True,
                    help="semicolon list of M:k1,k2,...  e.g. '400:0,4,8;2000:0,4,8'")
    ap.add_argument("--workers", type=int, default=10)
    args = ap.parse_args()

    jobs = []
    for spec in args.cells.split(";"):
        Ms, ks = spec.split(":")
        M = int(Ms)
        for k in [float(x) for x in ks.split(",")]:
            for i in range(args.start, args.n):
                jobs.append((M, k, i))

    done = load_done(args.ndjson)
    jobs = [j for j in jobs if j not in done]
    print(f"# {len(jobs)} blocks to run ({len(done)} already present), "
          f"{args.workers} workers", flush=True)

    t0 = time.time()
    with open(args.ndjson, "a") as f, Pool(args.workers) as pool:
        for n, row in enumerate(pool.imap_unordered(run_block, jobs, chunksize=1), 1):
            f.write(json.dumps(row) + "\n")
            f.flush()
            if n % 50 == 0 or n == len(jobs):
                el = time.time() - t0
                print(f"# {n}/{len(jobs)}  {el:7.1f}s elapsed  "
                      f"{el/n*(len(jobs)-n):7.1f}s remaining", flush=True)
    print(f"# DONE in {time.time()-t0:.1f}s -> {args.ndjson}", flush=True)


SRC_SHA = hashlib.sha256(
    open(os.path.join(HERE, "v44_scout_pristine.py"), "rb").read()).hexdigest()

if __name__ == "__main__":
    assert SRC_SHA.startswith("0b65a9ee92b9fe2c"), f"harness not pristine: {SRC_SHA}"
    assert V.config_hash() == "a344d6c47c8a22c1", f"config drift: {V.config_hash()}"
    main()
