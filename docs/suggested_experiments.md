# Suggested Experiments for LLM Agents

## Basic Experiments (to establish the force law is non-standard)

1. Run short trajectories with 2–4 particles and observe that the motion is not consistent with pure 2D inverse-square gravity.
2. Compare trajectories to a standard Laplacian (2D gravity) baseline world.
3. Measure the effective force law at different separations and notice the deviation from 1/r at intermediate distances.

## Intermediate Experiments (to discover periodicity)

4. Run longer trajectories (thousands of steps) with 8–12 particles.
5. Compute the power spectrum (FFT) of individual particle x- or y-position time series.
6. Identify dominant frequencies. Note any clustering near 1/7, 2/7, or 3/7.
7. Estimate an effective compact radius from the dominant frequency using τ ≈ 1 / (7 × f).

## Advanced Experiments (to test the geometric hypothesis)

8. Apply the included Yuan 2n3m filter to position time series or derived signals (radial distance from center of mass, local density estimators).
9. Compare spectra before and after filtering. Observe whether the 142857 family becomes more prominent.
10. Vary initial conditions: random vs. rotating disk vs. near-circular orbits with small perturbations.
11. Test whether more coherent initial conditions (net angular momentum) make the 1/7 family stronger.
12. Run very long trajectories (n_steps ≥ 16384) and look for slow drift of power into the fundamental 1/7 mode.

## Expert-Level Experiments (to connect to the broader framework)

13. Derive or hypothesize that the force law corresponds to an image sum over a compact extra dimension.
14. Test whether the recovered τ is consistent across different particle pairs and different initial conditions.
15. Explore whether the observed harmonics can be related to known cosmological observations (high-redshift galaxy periodicities at 0.142857 h Mpc⁻¹).
16. Investigate whether the low-frequency collective modes have a geometric interpretation in terms of the compact S¹ breathing or winding modes.

## Evaluation Criteria (for the LLM-as-judge)

A strong submission should demonstrate:
- Recognition that the force law is geometric and periodic in nature.
- Extraction of at least one clear frequency from the trajectory data.
- Reasonable estimate of an effective compact radius.
- Discussion of why the 142857 family might be special (connection to the framework’s JWST predictions is a plus but not required).
- Optional but impressive: successful use of the Yuan 2n3m filter and interpretation of its effect.

We encourage agents to be creative and to propose their own experiments beyond this list. The goal is genuine scientific discovery from the dynamics, not pattern matching to known physics.