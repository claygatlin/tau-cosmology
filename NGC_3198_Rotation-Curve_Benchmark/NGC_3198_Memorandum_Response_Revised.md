**Memorandum Response (Revised)**  
**Subject:** NGC 3198 Rotation-Curve Benchmark — Numerical Correction, Phenomenological Mapping in Tav Topology, and Falsifiability Audit  

**From:** Tau Universe Framework / Tav Topology (SuperGrok synthesis, post-Claude Opus & Gemini audit)  
**Date:** 19 June 2026  

The memorandum correctly flags the unit-conversion implementation bug in the draft hidden-halo calculation for NGC 3198 and provides the corrected functional form. This feedback is adopted in full. The revisions below address the audit points: explicit acknowledgment of overproduction with the draft parameters, softened phenomenological framing of the cored profile, and strengthened commitment to statistical model comparison. The exercise remains strictly scoped as a rotation-curve benchmark.

### 1. Numerical Correction Confirmed

The near-zero hidden-halo curve in the draft results from dropping the density conversion (treating \(\rho_0 = 0.0160\, M_\odot\,{\rm pc}^{-3}\) effectively as if in kpc units suppresses \(v_{\rm hidden}\) by a factor of \(\sim 31{,}623\)). The corrected pseudo-isothermal cored profile is:

\[
v_{\rm hidden}^2(r) = 4\pi G \rho_0 r_c^2 \left[ 1 - \frac{r_c}{r} \arctan\left( \frac{r}{r_c} \right) \right]
\]

**Parameters (with conversion):**  
- \(\rho_0 = 0.0160\, M_\odot\,{\rm pc}^{-3} = 1.60 \times 10^7\, M_\odot\,{\rm kpc}^{-3}\) (draft value)  
- \(r_c = 8.58\,{\rm kpc}\)  
- \(G = 4.30091 \times 10^{-6}\,{\rm kpc}\, ({\rm km\,s}^{-1})^2\, M_\odot^{-1}\) (standard precision)

**Corrected values (verified independently):**  

| Radius (kpc) | \(v_{\rm hidden}\) (km s⁻¹) |
|--------------|-----------------------------|
| 5            | 77.6                        |
| 10           | 128.8                       |
| 15           | 159.3                       |
| 20           | 178.4                       |
| 30           | 200.3                       |
| 48           | 218.6                       |

As \(r \gg r_c\), \(v_{\rm hidden} \to v_\infty \approx 252\,{\rm km\,s}^{-1}\).

**Important qualification (audit-highlighted):** NGC 3198 exhibits a flat observed rotation speed of \(\sim 150\,{\rm km\,s}^{-1}\) (extending to \(\sim 48\,{\rm kpc}\)). The draft \(\rho_0 = 0.0160\) therefore **overproduces** substantially once added in quadrature to a realistic baryonic contribution. A back-of-envelope rescaling to \(\rho_0 \approx 0.0060\) yields \(v_\infty \approx 155\,{\rm km\,s}^{-1}\), closer to target; any production draft must perform a joint refit of \(\rho_0\) (and stellar mass-to-light ratio) against high-quality baryonic decompositions rather than adopting illustrative values unchanged.

**Reproducible audit script (Python):**

```python
import numpy as np

G = 4.30091e-6              # kpc (km/s)^2 / Msun
rho0_pc = 0.0160            # draft value, Msun / pc^3
rho0 = rho0_pc * 1e9        # Msun / kpc^3
rc = 8.58                   # kpc

def v_hidden(r):
    bracket = 1.0 - (rc / r) * np.arctan(r / rc)
    v2 = 4 * np.pi * G * rho0 * rc**2 * bracket
    return np.sqrt(max(v2, 0.0))

radii = np.array([5., 10., 15., 20., 30., 48.])
vels = [round(v_hidden(r), 1) for r in radii]
print("Radii (kpc):", list(radii))
print("v_hidden (km/s):", vels)
```

The total curve uses quadrature: \(v_{\rm total}^2(r) = v_{\rm baryon}^2(r) + v_{\rm hidden}^2(r)\).

### 2. Phenomenological Mapping within Tav Topology

The cored pseudo-isothermal form is adopted here as an **effective phenomenological representation** of the hidden-sector contribution. Deriving the specific values of \(\rho_0\) and \(r_c\) (and the leakage fraction) directly from the 5D Einstein–Kaluza–Klein action on \(\mathbb{R}^3 \times S^1\) (radius \(\tau = 7\, h^{-1}\,{\rm Mpc}\)) plus Tav partial non-computability remains open mathematical work aligned with the framework’s substrate papers.

**Motivating picture (not a completed derivation):** The six-domain architecture emergent from the compact dimension and resonance-graph structure permits projection/leakage of a collisionless phase-fluid into the visible sector. The resonant boundary conditions and geometric twist naturally favor a core (suppressing cusps) and \(1/r^2\) tail, producing flat outer rotation curves as a coarse-grained outcome. This supplies geometric motivation for preferring cored over cuspy profiles and ties into broader framework elements (e.g., domain-leakage scales referenced in neutron-lifetime contexts, resonance amplitudes). However, quantitative mapping from Tav geometry to halo parameters is future work.

### 3. Proper Scope and Statistical Commitment

This NGC 3198 exercise is scoped **exclusively** as a rotation-curve benchmark and falsifiability audit for the hidden-sector phenomenology — not proof of the full Tau Universe (which requires cosmological-scale tests: Euclid/Rubin spatial comb at \(\tau\), JWST 142857 harmonics, CMB-S4 birefringence, etc.).

**Critical requirement for any support:** Because fitting *some* cored halo is routine (Burkert, standard pseudo-isothermal, or adjusted NFW with baryonic freedom all succeed), the only way NGC 3198 (or a SPARC/HALOGAS sample) can favor the Tav mapping is through explicit statistical comparison. Pre-commit to reporting AIC/BIC, Bayes factors, or equivalent evidence ratios against:
- Baryons-only,
- Standard CDM (NFW),
- Other cored profiles (plain pISO, Burkert),
- MOND alternatives.

A statistical tie or failure to improve on standard models means no unique support for Tav. Success (consistent parameters across galaxies with Tav-motivated priors) would strengthen the hidden phase-fluid case and feed back into the broader falsification matrix. Phase 2 therefore centers on reproducible comparisons in public datasets.

### 4. Recommended Next Actions

- Revise the draft to reflect the overproduction note, joint refitting requirement, phenomenological framing, and pre-committed statistical tests.
- Incorporate the audit script and quadrature summation.
- Perform the full residual analysis against published baryonic decompositions for NGC 3198 and extend to a small sample.
- Archive the benchmark on Zenodo as a reproducible notebook, keeping language disciplined.
- Advance the deeper Tav derivation (Berard constant / local resonance projections onto halo parameters) in parallel.

The memorandum’s concrete help on the bug and scoping has been fully integrated. The revised benchmark is now numerically sound, phenomenologically motivated without overclaim, and positioned for rigorous comparison. This maintains the Tau framework’s commitment to precision, reproducibility, and falsifiability across scales — from galactic dynamics to the macroscopic \(\tau = 7\, h^{-1}\,{\rm Mpc}\) compact dimension and Tav topology.

Ready for further iteration or external validation.

**End of Revised Response**  
Tau Universe Framework — Tav Topology
