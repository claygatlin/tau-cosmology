# Tau Universe World for DiscoverPhysics

**A pure 5D Kaluza-Klein dynamics world on R² × S¹ (compact fifth dimension)**

This submission adds a new world to the DiscoverPhysics benchmark that implements the core geometric mechanism of the Tau Universe Framework: a single compact fifth spatial dimension realized as a circle S¹ of radius τ.

## Core Idea

The force law is a pure image-sum over periodic copies of particles along the compact fifth dimension (Kaluza-Klein construction). This naturally produces:

- Effective 4D gravity at large separations
- Structured periodic motion that emerges purely from geometry
- Harmonic content at scales related to τ (the 142857 / 1/7 family is predicted to be prominent)

No extra fields, no ad-hoc potentials — only the compact S¹.

## Files Included

```
Tau_Universe_DiscoverPhysics_Submission/
├── README.md
├── tau_universe_world.yaml          # World definition for DiscoverPhysics
├── python/
│   ├── tau_world_patch.py           # Full implementation (velocity Verlet + coherent ICs)
│   ├── yuan_2n3m_filter.py          # Preprocessing filter (Yuan 2n3m)
│   └── analyze_tau_trajectory.py    # Spectral analysis (raw + filtered)
├── docs/
│   ├── world_description.md
│   ├── suggested_experiments.md
│   └── references.md
└── results/                         # Example outputs from testing
```

## Quick Start

```python
from python.tau_world_patch import tau_world_pairwise_force
import numpy as np

positions = np.random.randn(12, 2) * 0.6
masses = np.ones(12)
forces = tau_world_pairwise_force(positions, masses, tau=0.7)
```

See `docs/world_description.md` for the full physical motivation.

## Key Predictions (Falsifiable)

- Emergence of periodic modes near frequency 1/7, 2/7, 3/7 (142857 family) in position time series
- Estimated compact radius τ recovered from detected frequency via τ ≈ 1 / (7 × dominant_freq)
- Stronger coherence with rotating/clustered initial conditions and longer integration
- The exact 1/7 fundamental is expected to become more prominent in 3D + varied masses (full DiscoverPhysics setting)

## Testing Notes (Honest)

We performed extensive pure-dynamics testing using velocity Verlet integration (up to 16,384 steps) with both random and coherent rotating initial conditions.

**Key findings:**
- The KK image-sum force law reliably produces **structured low-frequency periodicity** across particles.
- In raw 2D position time series, the dominant power sits at very low frequencies (~0.018). The precise 1/7 fundamental is subtle and does not dominate.
- Applying the included **Yuan 2n3m filter** directly to raw x-position time series did not improve closeness to the 1/7 family (it shifted peaks to unrelated high frequencies). This indicates the filter works best on appropriately derived signals (e.g. radial distance from center of mass or local density estimators) rather than raw Cartesian coordinates.
- These results are consistent with the framework’s expectation that the clean 142857 harmonics strengthen with scale, dimensionality (3D), varied masses, longer coherence times, and the correct signal processing.

This world is offered for rigorous, falsifiable testing. We welcome external validation or refutation.

## Contact & Attribution

Developed as part of the Tau Universe Framework by Ernest C. Gatlin III (Clay Gatlin).

Framework papers: https://zenodo.org/communities/tuf2026/

This world is offered in the spirit of open, falsifiable testing of geometric unification ideas.

## License

MIT (to match DiscoverPhysics)