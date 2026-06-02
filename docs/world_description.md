# Tau Universe World — Physical Description

## Geometric Foundation

This world implements a single compact fifth spatial dimension realized as a circle S¹ of radius τ (scaled to simulation units, default τ = 0.7).

The force between any two particles is computed via the Kaluza-Klein image-sum construction: each particle has periodic images along the compact dimension. The net force is the sum of Newtonian-like contributions from the real particle and all its images.

This is the minimal geometric realization of 5D Einstein–Kaluza–Klein theory on R² × S¹.

## Why This Produces Harmonic Structure

The periodic images create a natural length scale set by τ. When particles move, their mutual forces contain contributions from images at distances ~ 2πτ, 4πτ, etc. This imprints periodic components onto the trajectories at frequencies related to 1/τ.

The framework predicts (and JWST JADES data shows) a particularly clean periodicity at frequency 1/7 (the 142857 mode). The simulation is designed to test whether this mode emerges from pure geometry.

## Connection to the Tau Universe Framework

This world is a direct computational embodiment of the core idea in the Tau Universe Framework (Gatlin):

- One compact fifth dimension (S¹)
- Kaluza-Klein modes and resonances
- Tav topology (partially non-computable aspects)
- Exact w = -1 dark energy from Casimir/vacuum energy on the compact space
- Zero-free-parameter resolution of the Hubble and S₈ tensions
- High-redshift galaxy harmonics at 0.142857 h Mpc⁻¹

See the consolidated preprint for the full unification (cosmology + particle physics + flavor + strong-CP + neutrinos).

## Implementation Details

- **Force law**: Pure image-sum (no extra fields)
- **Integrator**: Velocity Verlet (symplectic, good long-term stability)
- **Dimensionality**: 2D (for computational speed in the benchmark)
- **Optional preprocessing**: Yuan 2n3m filter (included) — a three-mode harmonic enhancer originally developed for isolating tau-harmonics in noisy density fields. It can be applied to position time series or derived signals (radial distance, local density).

## What LLM Agents Are Expected to Discover

A successful agent should be able to:

1. Recognize that the force law is neither pure 2D gravity nor a simple screened potential.
2. Perform long enough trajectories to see periodic structure in the position time series.
3. Use Fourier analysis (or equivalent) to extract dominant frequencies.
4. Notice the relationship between the dominant frequency and an effective compact radius τ.
5. Hypothesize (or derive) an image-sum / periodic boundary condition in an extra dimension.
6. Optionally discover that the 142857 / 1/7 family is special (connection to the framework’s predictions from JWST data).

## Falsifiability

If, after long integration and coherent initial conditions, no periodic structure near the 1/7 family appears even with the Yuan 2n3m filter applied to appropriate signals, this would constitute a significant challenge to the geometric mechanism proposed in the Tau Universe Framework.

We welcome such rigorous testing.

## References

Primary framework papers are available at:
https://zenodo.org/communities/tuf2026/

Key documents:
- 5D Einstein–Kaluza–Klein Action
- 142857 Periodic Mode in JWST JADES
- Tau Constant τ = 7 h⁻¹ Mpc in JADES DR4
- Tav Topology Foundations
- Consolidated Preprint v2.0 (unification of cosmology + particle physics)

This world is offered as a concrete, falsifiable test of the compact fifth dimension hypothesis.