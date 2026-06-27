# PAPER FIGURES — v3 Confirmation (τ-tunable equilibrium)

This document maps each figure to the scientific claim it carries and the exact manifest receipt that backs every plotted number. All values are from the production run (`results/v3_manifest.json`, 8000 traj/cell main sweep, seed 42, real Corridor1D).

| Figure | Claim (short-paper order) | Manifest receipt (exact keys/arrays) | Notes |
|--------|-----------------------------|---------------------------------------|-------|
| fig1_dial.png/pdf | Engine first-passage is a kinetically visible τ-dial: MFPT decreases monotonically with horizon; distributions slide & sharpen. | partA_mfpt_tau.{mean,ci_lo,ci_hi}, partA_fpt_hist.{tau,bin_edges,counts}, tau_grid | Fixed sep=6; 8000 traj/τ. |
| fig2_engine_vs_readout.png/pdf | A readout has one FPT curve (no τ); the engine has a dial (τ-family). | partA_fpt_hist (τ[0] as readout-like; full family) | Visual separation of concepts. |
| fig3_reducibility.png/pdf | Reducibility to U_eff(τ) is a definitional consequence of Arm A (conservative force) in 1D; not an empirical claim. Real anchor = zero current (fig5). Non-vacuous test requires 2D+ non-conservative (v4). | (no partB keys; statement figure using partA_fpt_hist + partD currents) | Honest negative for this regime. |
| fig4_sep_scaling.png/pdf | Engine first-passage scaling under the driven force is drift-dominated (measured α≈1, not thermal diffusive α=2). Caveat: α≈1 is generic for drift and does not separate entropic force from disguised reward. | partC_mfpt_vs_sep.{tau,sep,mfpt}, partC_alpha_tau.{mean,ci_lo,ci_hi} | 9 sep points, 8000 traj/cell. Relabeled "drift-dominated (α ≈ 1)". |
| fig5_positive_control.png/pdf | Instrument can detect a genuine engine (Rotor ω>0 shows current + directional FPT asymmetry p=2.5e-5); engine registers ⟨L_z⟩≈0 and no asymmetry. | partD_current_engine, partD_current_control, partD_control_asym.{fwd,rev,ks_p} | 5 seeds for currents; rotor angle FPT for asymmetry. Real p-value used (not overstated). |
| fig6_ueff_surface.png/pdf | The cause of the kinetic dial is visible: U_eff(x,τ) reshapes with horizon (the τ-tunable equilibrium landscape). | partE_ueff_surface.{x,tau,U_eff} | Heatmap, corridor locations overlaid (sep=6). |
| fig7_arc.png/pdf | Four-observable arc (occupancy, current, MFPT, reducibility) across v1→v2→v3. What each stage taught; the honest summary. | partA_mfpt_tau, partB_reducibility_ks_p, partD_current_* (plus conceptual occupancy flatness from prior RESULTS) | Cross-matrix + note on frontier = non-conservative (v4). |

## Honest framing (post-review)
v3 re-confirms the core of v2 in the conservative regime: the engine is thermodynamically indistinguishable from relaxation in a static (but τ-dependent) effective potential. The τ-dial in first-passage time is real and measured, but it is equilibrium dynamics in U_eff(τ) by definition once Arm A holds. α≈1 is drift under the force (not sep²/D diffusive). The negative result ("the τ-knob does not leave a fingerprint that no static potential can mimic" in this 1D conservative case) is clean and correctly identifies the frontier as v4 (non-conservative force, 2D+, where curl and currents become possible and a non-circular test exists). Part D zero current is the substantive empirical anchor. Reducibility claims are not dressed as empirical tests.

## Provenance
- Production command: `python -m src.v3_produce` (real repo code only; generator committed in this branch).
- Figure command: `python -m src.v3_figures` (pure loader; no random, no data literals).
- Every plotted value traces to `results/v3_manifest.json`.
- Branch: `v3-confirmation` (human pushes after review).

## File list (on disk at commit)
- results/v3_manifest.json
- src/v3_figures.py
- figures/fig1_dial.{png,pdf} … fig7_arc.{png,pdf}
- figures/captions.md
- docs/PAPER_FIGURES.md
- (updated RESULTS.md summary entry optional)
