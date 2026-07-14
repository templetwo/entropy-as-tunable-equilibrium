#!/usr/bin/env python3
"""
v4.4 scout — OC simulator v36-exec: CERTIFY THE CODE THAT RUNS.

LANE A AUDIT ARTIFACT (mesh-20260713, fable 1/3). NOT a registration artifact.
Quarantined sim-seed namespace: seed 20260713 (never pooled with pilot or
registered-sim seeds 20260707/20260708/20260710).

WHY THIS EXISTS (blocker 1, 2026-07-12): oc_sim_v35.py (ratified numbers) and
oc_sim_v35_full.py (faithful-floor erratum run) both REIMPLEMENT the band and
the ladder, and both bake in the reference-subtracted estimand
    mu_hat = mean(B blocks) - mean(64-block reference)
while the EXECUTABLE path (scout_report -> ladder_terminal -> band_cell,
v44_scout.py:756) bands the RAW cell mean:
    stamp(): band_cell(v.mean(), v.std(ddof=1), n, B_conf, sigma)
with an SE that folds in a 64-block reference the path never draws or
subtracts. Under a true null the executable statistic has var sd^2/n, tighter
than the sd^2(1/n + 1/64) the SE/floor arithmetic describes, so the executable
rule REDs more often than the certified sim (measured here, and matching the
2026-07-12 blocker: ~0.48 vs ~0.40 per-cell P(RED|null) at the diverging
configs). The ratified 0.980 compound power therefore describes code that will
never run.

WHAT THIS SIM DOES DIFFERENTLY — NOTHING IS REIMPLEMENTED:
every replication is pushed through the IMPORTED v44_scout.band_cell /
ladder_terminal / scout_outcome. Certify-what-runs is structural: the module
source is sha-pinned and asserted at import, in the parent AND in every
spawned worker. If v44_scout.py changes by one byte, this sim refuses to run.

SCENARIOS (mirroring the ratified OC_REPORT_v35.md gate definitions):
  gate9_exec   : -1x floor(96) wrong-sign current, one-sided, omega null.
                 compound = 1 - P(terminal primary RED). Ratified: 0.97994.
                 Law #3 floor: >= 0.90. If it fails, that is a FINDING for
                 Anthony — this sim does not tune anything.
  null_exec    : global null, one-sided. gate 1 false-GREEN (ratified
                 0.000236) + per-cell terminal P(RED|null) (the pivot's fuel).
  gate4_exec   : +3x floor, one-sided. GREEN power (ratified 0.99991).
  pivot_1s/2s  : six-cell global null through the EXECUTABLE scout_outcome
                 (STABLE at chance, GATING == FULL). Ratified faithful-sim
                 pivot-under-null: 0.017 (1s) / 0.0014 (2s).
  estdiv       : blocker-1 reproduction — identical band_cell, raw-mean vs
                 reference-subtracted mu_hat, per (n_blocks, B_conf, sided).

NOTE ON THE SEC-8 RERUN: the powered n=56 rerun exists in the harness ONLY as
config ("n_rerun": 56) and prose — there is no executable rerun function. The
ratified compound number did not consume it either (disposition-only reading
was recorded, not the gate), so the compound event here is band+ladder, same
as ratified. The rerun's alpha invariant (~0.05) belongs to the
reference-subtracted estimand; the executable surface has no rerun to certify.

Primary record: raw NDJSON (law #7), one header, one line per (scenario,
chunk) with band counts and the chunk's derived seed, then one summary line.
Interpreter: /usr/bin/python3 (3.9.6, numpy 2.0.2) — canonical. Deterministic.
"""
import sys, os, json, math, time, hashlib
import multiprocessing as mp

SCOUT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCOUT_DIR)
import numpy as np
import v44_scout as VS

# ---- the pin: certify-what-runs is structural ----------------------------
# [v3.6 enactment] pins moved off 1fe9fa1c…/a344d6c4… when the ratified
# changes landed (sec-3.3 simplification, R_occ plumbing, finding-6 blocks
# fix + green_16_96_2s 1.152). Because the sec-3.3 change is verdict-identical
# and the ladder legs are seed-deterministic, gate9/null/gate4/estdiv counts
# must reproduce the v3.5-pin run EXACTLY — that reproduction is itself a
# 12.8M-rep verdict-identity receipt.
PIN_SHA256 = "bce6b7384351982934cf7e48211dfbff26eee7cd7137982387b573439073ceb1"
PIN_CONFIG = "ba7c854ebc825476"
PIN_GIT    = "7a02eb5+laneA"

def _assert_pins():
    sha = hashlib.sha256(
        open(os.path.join(SCOUT_DIR, "v44_scout.py"), "rb").read()).hexdigest()
    assert sha == PIN_SHA256, "v44_scout.py sha256 %s != pinned %s" % (sha, PIN_SHA256)
    assert VS.SOURCE_SHA == sha[:16], "module SOURCE_SHA mismatch"
    assert VS.config_hash() == PIN_CONFIG, "config_hash %s != pinned %s" % (
        VS.config_hash(), PIN_CONFIG)
    assert VS.RULE["rule_version"] == "v3.6"
    assert VS.RULE["compound_power_target"] == 0.90            # law #3 floor
    assert abs(VS.rule_floor(1.0, 96) - 0.55685) < 5e-5        # law #4 spot checks
    assert abs(VS.rule_floor(1.0, 128) - 0.48225) < 5e-5
    assert abs(VS.rule_se(1.0, 16) - 0.2795) < 5e-4

_assert_pins()   # runs at import: parent AND every spawned worker

SEED   = 20260713
FLOOR  = VS.rule_floor(1.0, 96)
CELLS  = ("A", "B", "C", "D", "AxT2", "AxT4")
CHUNK  = 100_000
R_OCC  = VS.OCC_REDUCTIONS["lr_asymmetry"]   # [v3.6] fork 15, imported

def _rng(scen_idx, chunk_idx):
    return np.random.default_rng(
        np.random.SeedSequence(entropy=SEED, spawn_key=(scen_idx, chunk_idx)))

# ---- scenario kernels: EVERY replication goes through the imported code ---
def _ladder_chunk(scen_idx, chunk_idx, n_reps, delta, sigma):
    """One cell, primary at mean=delta, omega null; through VS.ladder_terminal."""
    rng = _rng(scen_idx, chunk_idx)
    counts, rungs = {}, {}
    for _ in range(n_reps):
        q = rng.normal(delta, 1.0, 32).tolist()
        w = rng.normal(0.0, 1.0, 32).tolist()
        t = VS.ladder_terminal(q, w, None, sigma, sigma)
        b = t["primary"]
        counts[b] = counts.get(b, 0) + 1
        r = t["rung"]["n_blocks"] if t["rung"] else 0
        rungs[r] = rungs.get(r, 0) + 1
    return {"bands": counts, "rung_blocks": rungs, "n": n_reps}

def _pivot_chunk(scen_idx, chunk_idx, n_reps, sigma, force_stable=False):
    """Six-cell global null through the EXECUTABLE scout_outcome.
    STABLE at chance (P(>=12/16 | p=0.5) ~ 0.038) or forced True (the rho=-1
    inverted-transduction regime — isolates whether the rule CAN license at
    all when suspenders are satisfied). GATING == FULL, no demoted cells."""
    rng = _rng(scen_idx, chunk_idx)
    outcomes, licensed = {}, 0
    for _ in range(n_reps):
        gb, ob, cb = {}, {}, {}
        st = {}
        for c in CELLS:
            q = rng.normal(0.0, 1.0, 32).tolist()
            w = rng.normal(0.0, 1.0, 32).tolist()
            # [v3.6] occupancy blocks through the IMPORTED R_occ: uniform
            # 24-bin multinomial histograms (symmetric null) reduced by the
            # registered lr_asymmetry — the sim certifies the veto that runs
            # (v3.6 sec 9 S10 note, Lane A interaction).
            o = [R_OCC(rng.multinomial(400, [1.0 / 24.0] * 24))
                 for _ in range(32)]
            t = VS.ladder_terminal(q, w, o, sigma, sigma)
            gb[c], ob[c], cb[c] = t["primary"], t["omega"], t["occupancy"]
            st[c] = True if force_stable else bool(rng.binomial(16, 0.5) >= 12)
        outcome, _reason, lic = VS.scout_outcome(gb, ob, cb, {}, st,
                                                 frozenset(CELLS), frozenset(CELLS),
                                                 "lr_asymmetry", "lr_asymmetry")
        outcomes[outcome] = outcomes.get(outcome, 0) + 1
        licensed += bool(lic)
    return {"outcomes": outcomes, "licensed": licensed, "n": n_reps}

def _estdiv_chunk(scen_idx, chunk_idx, n_reps, n_blocks, B_conf, sigma):
    """Blocker-1 reproduction: identical imported band_cell, two estimators."""
    rng = _rng(scen_idx, chunk_idx)
    red_exec = red_ref = 0
    for _ in range(n_reps):
        blk = rng.normal(0.0, 1.0, n_blocks)
        ref = rng.normal(0.0, 1.0 / math.sqrt(64))
        m, s = float(blk.mean()), float(blk.std(ddof=1))
        red_exec += (VS.band_cell(m, s, n_blocks, B_conf, sigma)[0] == "RED")
        red_ref  += (VS.band_cell(m - ref, s, n_blocks, B_conf, sigma)[0] == "RED")
    return {"red_exec": red_exec, "red_refsub": red_ref, "n": n_reps}

def _run_job(job):
    kind, scen_key, scen_idx, chunk_idx, n_reps, params = job
    if kind == "ladder":
        out = _ladder_chunk(scen_idx, chunk_idx, n_reps, *params)
    elif kind == "pivot":
        out = _pivot_chunk(scen_idx, chunk_idx, n_reps, *params)
    else:
        out = _estdiv_chunk(scen_idx, chunk_idx, n_reps, *params)
    out.update({"scenario": scen_key, "chunk": chunk_idx})
    return out

# ---- scenario table --------------------------------------------------------
# (kind, key, scen_idx, total_N, params)
SCENARIOS = [
    ("ladder", "gate9_exec_wrongsign_-1xfloor", 1, 4_000_000, (-FLOOR, +1)),
    ("ladder", "null_exec_one_sided",           2, 4_000_000, (0.0,    +1)),
    ("ladder", "gate4_exec_+3xfloor",           3, 4_000_000, (+3 * FLOOR, +1)),
    ("pivot",  "pivot_null_one_sided",          4,   500_000, (+1, False)),
    ("pivot",  "pivot_null_two_sided",          5,   500_000, (None, False)),
    ("pivot",  "pivot_null_1s_stable_true",    11,   500_000, (+1, True)),
    ("estdiv", "estdiv_16_96_1s",               6,   400_000, (16,  96, +1)),
    ("estdiv", "estdiv_32_96_1s",               7,   400_000, (32,  96, +1)),
    ("estdiv", "estdiv_32_96_2s",               8,   400_000, (32,  96, None)),
    ("estdiv", "estdiv_32_128_1s",              9,   400_000, (32, 128, +1)),
    ("estdiv", "estdiv_32_128_2s",             10,   400_000, (32, 128, None)),
]

RATIFIED = {   # OC_REPORT_v35.md (seed 20260708, reimplemented band, ref-subtracted)
    "gate9_compound": 0.97994,
    "gate1_false_green_percell": 0.000236,
    "gate4_green_power": 0.99991,
    "wrongsign_dist": {"ANOM": 0.832, "INCONCLUSIVE": 0.148, "RED": 0.020},
    "pivot_under_null_1s": 0.017,     # oc_sim_v35_full faithful-floor S1 sec-9.3 diff target
    "pivot_under_null_2s": 0.0014,
    "blocker1_measured": {"exec": 0.4768, "refsub": 0.4002},
}

def main():
    t0 = time.time()
    jobs = []
    for kind, key, sidx, total, params in SCENARIOS:
        nchunks = (total + CHUNK - 1) // CHUNK
        for c in range(nchunks):
            n = min(CHUNK, total - c * CHUNK)
            jobs.append((kind, key, sidx, c, n, params))

    ndjson_path = os.path.join(SCOUT_DIR, "oc_results_v36_exec.ndjson")
    header = {
        "type": "header", "sim": "oc_sim_v36_exec",
        "lane": "mesh-20260713 Lane A (fable 1/3) — audit, NOT registration",
        "seed": SEED, "chunk_size": CHUNK,
        "pin": {"v44_scout_sha256": PIN_SHA256, "source_sha": VS.SOURCE_SHA,
                "config_hash": PIN_CONFIG, "git": PIN_GIT,
                "rule_version": VS.RULE["rule_version"], "harness_version": VS.VERSION},
        "interpreter": sys.version.split()[0], "numpy": np.__version__,
        "floor96_sd1": round(FLOOR, 5),
        "estimator_note": ("executable path bands RAW mean(blocks); certified sims "
                           "band mean(blocks) - mean(64-ref). This sim certifies the "
                           "EXECUTABLE estimator via imported band_cell/ladder_terminal/"
                           "scout_outcome only."),
    }
    # Collect ALL chunk results first, then write in canonical (scenario,
    # chunk) order with sorted keys: the primary record is byte-reproducible
    # run-to-run (anchor's hardening note, mesh-20260713). Wall time goes to
    # stdout only — never into the record — for the same reason.
    scen_order = {key: i for i, (_, key, *_rest) in enumerate(SCENARIOS)}
    agg, rows = {}, []
    with mp.Pool(min(12, mp.cpu_count())) as pool:
        for out in pool.imap_unordered(_run_job, jobs, chunksize=1):
            rows.append(out)
            a = agg.setdefault(out["scenario"], {})
            for k, v in out.items():
                if isinstance(v, dict):
                    d = a.setdefault(k, {})
                    for kk, vv in v.items():
                        d[kk] = d.get(kk, 0) + vv
                elif isinstance(v, int) and k not in ("chunk",):
                    a[k] = a.get(k, 0) + v
    rows.sort(key=lambda r: (scen_order[r["scenario"]], r["chunk"]))
    with open(ndjson_path, "w") as fh:
        fh.write(json.dumps(header, sort_keys=True) + "\n")
        for out in rows:
            fh.write(json.dumps({"type": "chunk", **out}, sort_keys=True) + "\n")

        # ---- summaries ----
        def frac(d, key_, n): return round(d.get(key_, 0) / n, 6)
        g9 = agg["gate9_exec_wrongsign_-1xfloor"]; n9 = g9["n"]
        compound = round(1.0 - g9["bands"].get("RED", 0) / n9, 5)
        nul = agg["null_exec_one_sided"]; nn = nul["n"]
        g4 = agg["gate4_exec_+3xfloor"]; n4 = g4["n"]
        p1s = agg["pivot_null_one_sided"]; p2s = agg["pivot_null_two_sided"]
        summary = {
            "type": "summary",
            "gate9_exec_compound_full_union": compound,
            "gate9_law3_floor": 0.90,
            "gate9_verdict": "PASS" if compound >= 0.90 else "FAIL — FINDING for Anthony (not tuned)",
            "wrongsign_terminal_dist": {k: round(v / n9, 5) for k, v in sorted(g9["bands"].items())},
            "gate1_exec_false_green_percell": frac(nul["bands"], "GREEN", nn),
            "red_on_null_exec_terminal_percell": frac(nul["bands"], "RED", nn),
            "null_terminal_dist": {k: round(v / nn, 6) for k, v in sorted(nul["bands"].items())},
            "gate4_exec_green_power": frac(g4["bands"], "GREEN", n4),
            "pivot_under_null_exec_1s": round(p1s["licensed"] / p1s["n"], 6),
            "pivot_outcomes_1s": {k: round(v / p1s["n"], 6) for k, v in sorted(p1s["outcomes"].items())},
            "pivot_under_null_exec_2s": round(p2s["licensed"] / p2s["n"], 6),
            "pivot_outcomes_2s": {k: round(v / p2s["n"], 6) for k, v in sorted(p2s["outcomes"].items())},
            "pivot_under_null_exec_1s_stable_true": round(
                agg["pivot_null_1s_stable_true"]["licensed"] / agg["pivot_null_1s_stable_true"]["n"], 6),
            "pivot_outcomes_1s_stable_true": {
                k: round(v / agg["pivot_null_1s_stable_true"]["n"], 6)
                for k, v in sorted(agg["pivot_null_1s_stable_true"]["outcomes"].items())},
            "estdiv": {},
            "ratified_for_diff": RATIFIED,
        }
        for kind, key, sidx, total, params in SCENARIOS:
            if kind != "estdiv":
                continue
            a = agg[key]
            summary["estdiv"][key] = {
                "P_RED_null_exec_rawmean": round(a["red_exec"] / a["n"], 5),
                "P_RED_null_refsub": round(a["red_refsub"] / a["n"], 5)}
        fh.write(json.dumps(summary, sort_keys=True) + "\n")

    # ---- human-readable report ----
    print("=" * 72)
    print("OC SIM v36-exec — v3.5 AS-EXECUTABLE (imported band_cell/ladder/outcome)")
    print("pin: sha256 %s.. | config %s | git %s | seed %d" % (
        PIN_SHA256[:16], PIN_CONFIG, PIN_GIT, SEED))
    print("=" * 72)
    print("gate 9/9O compound (1 - P(wrong-sign cleared to RED)):")
    print("   EXECUTABLE = %.5f   ratified(reimpl) = %.5f   law#3 floor = 0.90  -> %s"
          % (compound, RATIFIED["gate9_compound"], summary["gate9_verdict"]))
    print("   wrong-sign terminal dist (exec): %s" % summary["wrongsign_terminal_dist"])
    print("   ratified dist: %s" % RATIFIED["wrongsign_dist"])
    print("gate 1 false-GREEN on null (per cell):")
    print("   EXECUTABLE = %.6f   ratified = %.6f" % (
        summary["gate1_exec_false_green_percell"], RATIFIED["gate1_false_green_percell"]))
    print("terminal P(RED | null) per cell (the pivot's fuel):")
    print("   EXECUTABLE = %.6f" % summary["red_on_null_exec_terminal_percell"])
    print("gate 4 GREEN power @ +3x floor:")
    print("   EXECUTABLE = %.5f   ratified = %.5f" % (
        summary["gate4_exec_green_power"], RATIFIED["gate4_green_power"]))
    print("pivot licensed under six-cell global null (executable scout_outcome):")
    print("   one-sided = %.6f (faithful-sim target 0.017)   two-sided = %.6f (target 0.0014)"
          % (summary["pivot_under_null_exec_1s"], summary["pivot_under_null_exec_2s"]))
    print("   one-sided, STABLE forced true (can the rule license AT ALL?): %.6f"
          % summary["pivot_under_null_exec_1s_stable_true"])
    print("   outcome dist (stable-true): %s" % summary["pivot_outcomes_1s_stable_true"])
    print("blocker-1 estimator divergence, identical imported band_cell:")
    for k, v in summary["estdiv"].items():
        print("   %-18s exec=%.5f  refsub=%.5f" % (
            k.replace("estdiv_", ""), v["P_RED_null_exec_rawmean"], v["P_RED_null_refsub"]))
    print("   (2026-07-12 blocker measured: exec 0.4768 vs refsub 0.4002)")
    print("primary record: %s" % ndjson_path)
    print("wall: %.1fs (stdout only — never in the record)" % (time.time() - t0))

if __name__ == "__main__":
    main()
