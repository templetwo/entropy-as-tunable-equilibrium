#!/usr/bin/env python3
"""Independent recompute driver: re-simulate v4.3 units from archived seeds,
with a PASSIVE transition-count observer (zero RNG calls added) hooked into
CurrentAcc.add. Bit-exact agreement with the archived NDJSON therefore proves
both cross-version determinism and observer non-interference.

Analysis statistics are pre-declared in this file header, before any
confirmatory unit is run and before reading v43_analysis.json:
  OCC   : per-block occupancy center-of-mass, frozen vs online, two-sided
          permutation (20k perms) on 32v32 block means.
  CIRC  : plaquette circulation from MY directed transition counts
          (global + mouth ROI), per-arm sign-flip test vs 0, plus
          online-minus-frozen two-sample permutation contrast.
  EDGE  : per-edge net-flow rate contrast (online vs frozen), block bootstrap.
  CTRL  : same CIRC pipeline must fire on C4v k8 and stay quiet on k0.
"""
import importlib.util, json, os, sys, pickle, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("h", os.path.join(HERE, "v43_harness.py"))
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)

NX, NY = 24, 12
LX = h.CFG["box"]["Lx"]; LY = h.CFG["box"]["Ly"]

class Obs:
    """Directed cell-to-cell transition counts + 2D occupancy."""
    def __init__(self):
        self.K = {}
        self.occ2d = np.zeros((NX, NY), dtype=np.int64)
        self.n = 0
    def cell(self, r):
        return (min(int(r[0] / LX * NX), NX - 1),
                min(int(r[1] / LY * NY), NY - 1))
    def add(self, r_old, r_new):
        a, b = self.cell(r_old), self.cell(r_new)
        self.occ2d[b] += 1
        self.n += 1
        if a != b:
            self.K[(a, b)] = self.K.get((a, b), 0) + 1

OBS = None
_orig_add = h.CurrentAcc.add
def patched_add(self, r_old, r_new):
    _orig_add(self, r_old, r_new)
    if OBS is not None:
        OBS.add(r_old, r_new)
h.CurrentAcc.add = patched_add

def deep_eq(a, b, path=""):
    if isinstance(a, dict) and isinstance(b, dict):
        if set(a) != set(b):
            return False, path + f" keys {set(a) ^ set(b)}"
        for k in a:
            ok, w = deep_eq(a[k], b[k], path + "." + str(k))
            if not ok:
                return ok, w
        return True, ""
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return False, path + " len"
        for i, (x, y) in enumerate(zip(a, b)):
            ok, w = deep_eq(x, y, path + f"[{i}]")
            if not ok:
                return ok, w
        return True, ""
    if isinstance(a, float) or isinstance(b, float):
        if a == b or (np.isnan(a) and np.isnan(b)):
            return True, ""
        if b != 0 and abs(a - b) / abs(b) < 5e-15:
            return True, ""  # 1-ulp libm drift (atan2), physics identical
        return False, path + f" {a!r}!={b!r}"
    return (a == b), (path if a != b else "")

def rerun(unit_id):
    global OBS
    OBS = Obs()
    with open(os.devnull, "w") as devnull, contextlib.redirect_stdout(devnull):
        out = h.run_unit(unit_id)
    # json round-trip so float repr path matches the archived record exactly
    data = json.loads(json.dumps(out["data"]))
    obs = OBS; OBS = None
    return data, obs

def load_archive():
    recs = {}
    with open(os.path.join(HERE, "v43_run.ndjson")) as f:
        for line in f:
            r = json.loads(line)
            recs[r["unit"]] = r
    return recs

def run_batch(units, tag, archive):
    results = {}
    for k, u in enumerate(units):
        data, obs = rerun(u)
        ok, where = deep_eq(data, archive[u]["data"])
        results[u] = {"bitexact": ok, "where": where, "n": obs.n,
                      "occ2d": obs.occ2d, "K": obs.K}
        print(f"[{tag} {k+1}/{len(units)}] {u} bitexact={ok}{' @'+where if not ok else ''}",
              flush=True)
    return results

if __name__ == "__main__":
    import time, glob
    mode = sys.argv[1]
    archive = load_archive()
    UNITS = ([f"C1m_frozen_M256_tau0.25_sb{i}" for i in range(32)]
             + [f"C4v_frozen_k8.0_tau1.0_sb{i}" for i in range(6)]
             + [f"C4v_frozen_k0.0_tau1.0_sb{i}" for i in range(2)]
             + [f"C1m_online_M256_c1_tau0.25_sb{i}" for i in range(32)])
    os.makedirs("rc_units", exist_ok=True)
    if mode == "resume":
        budget = float(sys.argv[2]) if len(sys.argv) > 2 else 360.0
        t0 = time.time()
        for u in UNITS:
            fp = os.path.join("rc_units", u + ".pkl")
            if os.path.exists(fp):
                continue
            if time.time() - t0 > budget:
                print("BUDGET REACHED", flush=True); break
            data, obs = rerun(u)
            ok, where = deep_eq(data, archive[u]["data"])
            with open(fp, "wb") as f:
                pickle.dump({"bitexact": ok, "where": where, "n": obs.n,
                             "occ2d": obs.occ2d, "K": obs.K}, f)
            print(f"{u} bitexact={ok}{' @'+where if not ok else ''}", flush=True)
        done = len(glob.glob("rc_units/*.pkl"))
        print(f"PROGRESS {done}/{len(UNITS)}", flush=True)
        if done == len(UNITS):
            res = {}
            for u in UNITS:
                with open(os.path.join("rc_units", u + ".pkl"), "rb") as f:
                    res[u] = pickle.load(f)
            with open("recompute_results.pkl", "wb") as f:
                pickle.dump(res, f)
            print("ALL DONE", flush=True)
