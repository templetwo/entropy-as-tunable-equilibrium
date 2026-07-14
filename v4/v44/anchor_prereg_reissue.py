#!/usr/bin/env python3
"""prereg_v44.json v2 re-issue — anchor lane, mesh-20260713 enactment night.

Everything derivable is DERIVED from the imported harness (v44_scout.py in this
directory) — never hand-typed: config, config_hash, source_sha, version,
rule_version, ratified dates. The only authored inputs are the occ_reduction
formula text (fork 15, ratified: lr_asymmetry per v3.6 D1'''), and the
provenance notes (finding receipts already on the mesh table).

Re-issue mandate: RATIFICATION_v3.5.md step 3 (n_rerun -> CFG, never done),
finding 6 (CFG.scout.blocks 8->16), fork 15 (occ_reduction field),
RATIFICATION_v3.6.md step 3 (the anchor's staging lane). The superseded prereg
remains in git history; corrections supersede, never erase (law #9).

Run from this directory: /usr/bin/python3 anchor_prereg_reissue.py
Prints old/new sha256; writes prereg_v44.json in place (git carries history).
"""

import hashlib
import json
import sys

sys.path.insert(0, ".")
import v44_scout as VS  # noqa: E402

OLD = "prereg_v44.json"

old_bytes = open(OLD, "rb").read()
old = json.loads(old_bytes)

new = {
    "type": old["type"],
    "source_sha_at_registration": VS.SOURCE_SHA,
    "version": VS.VERSION,
    "rule_version": VS.RULE["rule_version"],
    "rule_ratified": {"v3_6": VS.RULE["ratified"], "v3_5": VS.RULE["ratified_v3_5"]},
    "config_hash": VS.config_hash(),
    "config": VS.CFG,
    "units": old["units"],
    "outcome_map": old["outcome_map"],
    "occ_reduction": {
        "name": "lr_asymmetry",
        "formula": (
            "R_occ(v) = (sum_{i=12..23} v_i - sum_{i=0..11} v_i) / sum_{i=0..23} v_i "
            "over the 24-bin occupancy_x histogram; signed left/right mass asymmetry, "
            "mean-zero under a symmetric null. BLIND to left/right-symmetric shape "
            "change - stated in the v3.6 sec-2.1 claim wording, not papered over."
        ),
        "ratified": "fork 15, Anthony 2026-07-13 (RATIFICATION_v3.6.md)",
    },
    "provenance_notes": [
        "DIAG-3 (diag3_raw.ndjson) ran under source_sha 0b65a9ee92b9fe2c (pre-executability "
        "harness). The executability change (7f2e91f->7a02eb5) is verified additive "
        "(+681/-3, all three deletions inspected: import cosmetics + selftest wiring); "
        "physics paths untouched.",
        "Certification of v3.5-as-executable AND v3.6 (verdict-identical): gate9 compound "
        "0.98114 >= 0.90, byte-reproducible NDJSON b44948bbd00161aed8256957740300d49ea887d2"
        "dda1906886b14d936b00d826 under source_sha bce6b73843519829 (oc_sim_v36_exec, "
        "imported band_cell/ladder_terminal/scout_outcome/R_occ only).",
        "Prior prereg (source_sha_at_registration 0b65a9ee92b9fe2c, sha256 "
        + hashlib.sha256(old_bytes).hexdigest()
        + ") superseded by this re-issue; retained in git history.",
    ],
}

# The registered envelope must equal the harness at import time - assert, never trust.
assert new["source_sha_at_registration"] == VS.SOURCE_SHA
assert new["config_hash"] == VS.config_hash()
assert new["config"]["scout"]["blocks"] == VS.RULE["blocks_first"], "finding-6 cross-assert"
assert new["occ_reduction"]["name"] in VS.OCC_REDUCTIONS, "registered reduction must exist in code"

out = json.dumps(new, indent=2) + "\n"
with open(OLD, "w") as fh:
    fh.write(out)

print("old prereg sha256:", hashlib.sha256(old_bytes).hexdigest())
print("new prereg sha256:", hashlib.sha256(out.encode()).hexdigest())
print("source_sha_at_registration:", new["source_sha_at_registration"])
print("config_hash:", new["config_hash"])
print("rule_version:", new["rule_version"], "| occ_reduction:", new["occ_reduction"]["name"])
