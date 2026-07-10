# Entropy as a Tunable Equilibrium

**Can entropy drive a system, or only describe one? It can look like it does — and still just be describing one, tuned by how far ahead you let it see.**

This repo ran a single falsifiable experiment to tell two views of entropy apart, and got a clean, unexpected answer: not the engine it set out to find, but something stranger — a state that *organizes itself* purely by adjusting its own horizon, while remaining, thermodynamically, at rest. The horizon knob is real. The engine isn't, not in the regime tested. Both halves of that sentence are the discovery.

Here were the two candidates going in:

- **Readout entropy** — entropy is a thermometer. A system maximizes its own entropy by relaxing to equilibrium, and stops. The steady state is fixed (the Boltzmann distribution). There is no knob you can push.
- **Engine entropy** — entropy is a prime mover. Using the *causal entropic force* (Wissner-Gross & Freer, *PRL* 2013), a future-entropy gradient drives a system into organized, anticipatory behavior with **no reward function**.

The design logic was that one device separates them: a **horizon knob** τ. Thermal relaxation has no τ. The causal entropic force does — so if turning τ reorganizes the system, entropy must be doing work, not just being measured. That logic turned out to hide a false dichotomy. Turning the knob **does** reorganize the system — and that reorganization **is** thermodynamic relaxation, into a τ-shaped equilibrium that moves as τ moves. Structure without a motor. That's the tunable equilibrium the title names.

## The minimal prediction (as registered, before the result)

> The engine's steady-state organization is a **monotone function of the horizon τ**, with a **crossover τ\*** set by the landscape geometry. Readout entropy has no τ and predicts a fixed distribution.

And the discriminating test, against the obvious objection that "the entropic force is just a reward in disguise":

> **τ\* ∝ L_channel² / D** (the diffusive traversal time). A smuggled constant reward would pull at all horizons and could not reproduce this scaling.

**This specific prediction failed** (Arm C, below) — not because the horizon knob is fake, but for a principled reason: steady-state occupancy is blind to path lengths, which live only in kinetics. The failure is what pointed the way to v2/v3 and the actual answer.

## What's here

A particle in a potential landscape under overdamped Langevin dynamics, two conditions:

1. **Control** — pure thermal relaxation to `p_eq ∝ exp(−U/kT)`. Fixed, no horizon.
2. **Engine** — driven by the causal entropic force `F = T_c ∇S_c(x, τ)`, where `S_c` is the entropy over futures reachable within horizon τ. Steady state `p_engine ∝ exp(T_c S_c / kT)` (for the overdamped case, where the force is conservative — a property the experiment verifies rather than assumes).

## Status

| Phase | What | State |
|---|---|---|
| **Phase 0** | 1D dumbbell, mechanism check | ✅ validated + **reproduced** (MacBook) — engine ≠ readout (KL 0.79–1.14), horizon knob confirmed (mass 0.483 → 0.668 as τ grows; control fixed 0.527) |
| **Arm A** | Conservativeness check (drive a particle, confirm the analytic steady state) | ✅ **PASS** — KL(driven‖analytic) 0.0002, overlap 0.993; analytic shortcut licensed |
| **Arm B** | 2D chamber–channel–chamber, sharp τ\* crossover | ✅ **horizon knob confirmed** — engine P_L 0.51 → 0.91 monotone vs flat control 0.371 |
| **Arm C** | τ\* tracks geometry (`τ\* ∝ L_ch²/D`) — the make-or-break test | ❌ **FALSIFIED** — τ\* is flat in L_ch (R²(origin) = −17.7). A D-scan shows τ\* ∝ 1/D (R²=0.97): τ\* is a diffusive geometric time set by **chamber** exploration (r_L), not **channel** length. See `RESULTS.md`. |
| **v2** | First-passage discriminator (kinetic) | ✅ **thesis demonstrated** — MFPT ∝ sep²/D (R²=0.992) recovers the corridor signature occupancy is blind to; current test ⟨L_z⟩≈0 for the conservative engine. Engine vs readout: thermodynamically indistinguishable, kinetically distinguishable. |
| **v3** | Engine-driven first-passage: does the τ-knob leave a fingerprint *no static U can mimic?* | ➖ **honest negative (conservative 1D)** — the τ-knob is a real FPT dial (MFPT 13.9→6.1 vs τ), but at each τ it *is* equilibrium relaxation in U_eff(τ) = −T_c S_c (definitional once Arm A holds; 1D is curl-free). Driven scaling α≈1 (drift, not diffusive α=2); ⟨L_z⟩≈0 re-confirms equivalence. No irreducible fingerprint here. Production figures + manifest under `figures/fig*`, `results/v3_manifest.json`. |
| **Arm D / v4** | Non-conservative force (2D+, curl ≠ 0) — v4.0 pilot → v4.1/v4.2 kinetic-signature arc → v4.3 powered vortex control + anisotropic-horizon engine test | ✅ **complete (v4.0–v4.3)** — instrument **proven** (powered vortex control, Holm p=1e-4); anisotropic-horizon engine current: **bounded null** (floor 3.67e-5, more than 7× below the strongest cleanly-resolved vortex); the v4.1 kinetic separation dissolves at matched estimator M (estimator roughness, not implementation); occupancy micro-shift confirmed (p=0.024) and resolved to the **equilibrium** side — no probability current (detailed-balance follow-up, `v4/v43/followup/`; independent 72/72 bit-exact replication, `v4/v43/replication/claude-recompute/`). Every apparent positive resolves to equilibrium or estimator: the tunable-equilibrium thesis closes. Paper: `v4/paper/` |

> **Outcome (see [RESULTS.md](RESULTS.md)).** The horizon knob is real (Phase 0, Arm B) and
> the engine's organization obeys a genuine diffusive law (τ\* ∝ 1/D). The steady-state
> discriminator τ\* ∝ L_ch²/D **failed** (Arm C) — a textbook consequence of detailed balance:
> occupancy is blind to path lengths, which live only in kinetics. **v2 confirms the resolution:**
> in a clean corridor, first-passage time **does** carry the corridor signature (MFPT ∝ sep²/D,
> R²=0.992) while occupancy stays flat and the conservative engine force shows **zero probability
> current** (⟨L_z⟩≈0 vs a rotational positive control). The sharp, defensible thesis: **engine and
> readout entropy can be thermodynamically indistinguishable (identical occupancy, zero current)
> yet kinetically distinguishable (first-passage under the τ-knob).** **v3 closes the loop
> honestly:** engine-driven first-passage *is* a real τ-dial, but in the conservative 1D regime
> that dial is equilibrium relaxation in a τ-tunable U_eff(τ) (driven α≈1, zero current) — there is
> *no* fingerprint a static potential cannot mimic. The genuine non-equilibrium frontier is **v4**
> (a non-conservative force, 2D+, where curl and steady currents become possible). **v4 walked that
> frontier end-to-end (2026-07):** the instrument proved itself, the minimal non-conservative
> extension produced a bounded null, and the last apparent positive resolved to the equilibrium
> side — see the v4 row above and the paper in `v4/paper/`. Prior-art context
> and honest novelty accounting: [docs/PRIOR_ART_AND_NOVELTY.md](docs/PRIOR_ART_AND_NOVELTY.md).

### Phase 0 result

Two valleys: a deep narrow well (option-poor) and a wide shallow well (option-rich). Thermal relaxation dives into the deep well and stays. The entropy drive *refuses* the deep well (a narrow trap has few open futures) and, as the horizon grows, slides into the wide well — monotonically. The control sheet is flat in τ; the engine surface tilts and migrates. That tilt is the knob, and the knob is the thesis. (See `figures/`.)

## Quick start

```bash
pip install -r requirements.txt
python -m src.phase0_validated_1d        # reproduce Phase 0 + regenerate the 3D overlay figure
python -m src.run --arm A                 # conservativeness check
python -m src.run --arm B                 # 2D crossover
python -m src.run --arm C                 # geometry-scaling discriminator
```

## How to read the result

This experiment was built to be **falsifiable**, and its make-or-break test broke: τ\* did not track `L_ch²/D` (Arm C), which killed the naive engine-as-prime-mover claim outright. That negative result is reported, not buried — and it's the pivot the whole arc turns on. The point was never to confirm a belief; it was to find out which view of entropy survives a test that could have killed it, and follow the failure to whatever it actually points at. Here, it pointed at v2's kinetic discriminator and, finally, at v3's honest answer: a τ-tunable equilibrium.

## Why it matters

The arrow of time *is* entropy increase, so "is entropy fundamental?" and "is time fundamental?" are the same question. The deep-physics version of this fork runs from Boltzmann's H-theorem (the clean statement of readout-entropy as one-way drift) through the block-universe / thermal-time view (Rovelli — entropy as readout of coarse-graining) versus time-as-real (Smolin). This experiment doesn't settle that debate. It does something smaller and checkable: it asks whether an entropy gradient *alone* can generate sustained, horizon-dependent organization, and pins the answer to a number you can measure.

## Details

Full experimental specification, parameters, success/falsification criteria, and executor instructions: **[SPEC.md](SPEC.md)**.

## Related work & honest novelty

A prior-art and novelty assessment is in **[docs/PRIOR_ART_AND_NOVELTY.md](docs/PRIOR_ART_AND_NOVELTY.md)**.
Short version of where this sits in the literature:

- **The mechanism is not new.** The causal entropic force (Wissner-Gross & Freer, *PRL* 2013)
  and its option-rich-preference behavior are established, and the "is this just reward
  shaping?" worry is the consensus view: causal-entropic forcing is mathematically an
  *entropy-of-futures intrinsic reward* (Shah 2014; Ramírez-Ruiz et al., *Nat. Commun.* 2024,
  "Maximum Occupancy Principle"). S_c is best framed as a **Maximum-Caliber path entropy**
  (Pressé et al. 2013; Ghosh et al. 2020).
- **The v1 Arm C failure is textbook, and that's the point.** That a *steady-state*
  occupancy can't see channel-traversal time is the detailed-balance / thermodynamics–kinetics
  separation: equilibrium ∝ exp(−βU_eff) is provably blind to barriers and path lengths, which
  live only in *kinetic* observables (Hänggi–Talkner–Borkovec, *RMP* 1990; Gardiner; van Kampen).
  The expected `L²/D` scaling is canonical diffusive first-passage — it appears in the **MFPT**,
  not in occupancy.
- **The genuinely defensible contribution** is the experimental epistemology: the **τ horizon
  knob** as a controlled dial, the **engine-vs-readout** framing as a testable question, and a
  *pre-registered prediction that failed for a principled reason* with a correct diagnosis. The
  sharpest honest thesis: in the conservative, position-only overdamped regime, "engine entropy"
  has zero steady-state current / zero entropy production — it is **thermodynamically
  indistinguishable** from equilibrium relaxation and distinguishable, if at all, only
  **kinetically**. That is what the v2 first-passage discriminator is built to test.

## Provenance

Part of [The Temple of Two](https://thetempleoftwo.com) · [github.com/templetwo](https://github.com/templetwo). Designed collaboratively by Anthony Vasquez and Claude. Background research chain and persistent record live in the Sovereign Stack (entropy-as-substrate thread).

The v3 manuscript is published on Zenodo: **DOI [10.5281/zenodo.21223845](https://doi.org/10.5281/zenodo.21223845)** (v3-1.0.0, July 6 2026, CC-BY-4.0). The v4 manuscript (the complete v4.0–v4.3 arc) is deposited at [v4/paper/](v4/paper/); its Zenodo DOI is pending.

## Citation

Machine-readable metadata: [CITATION.cff](CITATION.cff) (GitHub's "Cite this repository" button uses it). To cite the published result:

> Vasquez, A. and Claude (Anthropic) (2026). *Entropy as a Tunable Equilibrium, Not an Engine: A Falsifiable Horizon-Knob Test of the Causal Entropic Force.* Zenodo. https://doi.org/10.5281/zenodo.21223845

## License

Apache-2.0. See [LICENSE](LICENSE).
