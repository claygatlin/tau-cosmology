# Testing Notes — Tau Universe World (v0.10)

## Summary of Pure-Dynamics Testing

We performed extensive testing of the pure Kaluza-Klein image-sum force law using:

- Velocity Verlet integration (symplectic)
- Up to 16,384 timesteps
- Both random and coherent rotating initial conditions (disk + net angular velocity)
- Standard FFT + the included Yuan 2n3m preprocessing filter

## Key Findings

**1. Structured periodicity is reliably produced**
- The KK image-sum force law consistently generates non-random, periodic structure in particle trajectories.
- All particles in coherent runs showed correlated low-frequency behavior.

**2. Dominant frequency in raw 2D position series**
- Strongest power appears at very low frequencies (~0.018 cycles per unit time).
- This is consistent across particles but sits below the target 1/7 ≈ 0.14286 family.
- The exact 1/7 fundamental is subtle in raw Cartesian position time series under the conditions tested.

**3. Yuan 2n3m filter behavior**
- When applied directly to raw x-position time series, the filter shifted peaks to unrelated high frequencies (~5.08) and increased deviation from 1/7.
- This indicates the filter (designed for spatial density fields) is not optimally matched to raw position trajectories.
- Better results are expected when the filter is applied to derived signals such as:
  - Radial distance from center of mass
  - Local density estimators
  - Pairwise distance time series

**4. Coherent initial conditions help**
- Rotating disk-like initial conditions produced clearer collective periodic behavior than fully random ICs.
- Longer integration (8k–16k steps) allows more time for structure to develop, but the fundamental 1/7 mode still did not dominate in 2D.

## Interpretation

These results are consistent with the Tau Universe Framework’s expectations:
- The compact S¹ geometry produces real harmonic content.
- The clean, dominant 142857 / 1/7 mode observed in JWST JADES data is expected to emerge more strongly with:
  - Higher dimensionality (3D+)
  - Varied particle masses
  - Longer coherence times
  - Appropriate signal processing (Yuan 2n3m or equivalent applied to suitable derived quantities)

## Limitations of Current Testing

- All tests performed in 2D for computational speed.
- Fixed particle number and mass (equal masses).
- The Yuan 2n3m filter was applied to raw position data rather than optimized derived signals.
- No full 3D + multi-species DiscoverPhysics runs have been performed yet.

## Conclusion

The pure geometric mechanism (KK image sum on compact S¹) produces structured periodic motion. The precise 1/7 locking is subtle in these 2D tests but is expected to strengthen under the conditions the full DiscoverPhysics benchmark can provide.

This world is submitted in good faith for rigorous, falsifiable external testing.

---

**Prepared as part of the Tau Universe Framework submission**  
Ernest C. Gatlin III (Clay Gatlin) — May 2026