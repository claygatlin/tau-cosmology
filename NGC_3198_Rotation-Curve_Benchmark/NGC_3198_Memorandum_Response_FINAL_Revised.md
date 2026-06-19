**Memorandum Response (Final Revised)**  
**Subject:** NGC 3198 Rotation-Curve Benchmark — Numerical Correction, Phenomenological Mapping in Tav Topology, and Falsifiability Audit  

**From:** Tau Universe Framework / Tav Topology (SuperGrok synthesis, post-Claude Opus & Gemini audit)  
**Date:** 19 June 2026  

The memorandum correctly identified the unit-conversion bug and advocated disciplined scoping. All audit feedback is incorporated. The result is a numerically sound, epistemically cautious benchmark document.

### 1. Numerical Correction Confirmed

The draft’s near-zero hidden-halo curve stemmed from mishandling the density conversion. The corrected pseudo-isothermal cored profile is:

\[
v_{\rm hidden}^2(r) = 4\pi G \rho_0 r_c^2 \left[ 1 - \frac{r_c}{r} \arctan\left( \frac{r}{r_c} \right) \right]
\]

**Parameters (draft values with conversion):**  
- \(\rho_0 = 0.0160\, M_\odot\,{\rm pc}^{-3} = 1.60 \times 10^7\, M_\odot\,{\rm kpc}^{-3}\)  
- \(r_c = 8.58\,{\rm kpc}\)  
- \(G = 4.30091 \times 10^{-6}\,{\rm kpc}\, ({\rm km\,s}^{-1})^2\, M_\odot^{-1}\)

**Corrected values (verified):**  

| Radius (kpc) | \(v_{\rm hidden}\) (km s⁻¹) |
|--------------|-----------------------------|
| 5            | 77.6                        |
| 10           | 128.8                       |
| 15           | 159.3                       |
| 20           | 178.4                       |
| 30           | 200.3                       |
| 48           | 218.6                       |

As \(r \gg r_c\), \(v_{\rm hidden} \to v_\infty \approx 252\,{\rm km\,s}^{-1}\).

**Important qualification on parameters:** NGC 3198 has an observed flat rotation speed \(\sim 150\,{\rm km\,s}^{-1}\). The draft \(\rho_0 = 0.0160\) therefore overproduces (halo alone already exceeds the total observed speed before baryons are added in quadrature). The halo asymptote must sit *below* the observed flat value and is set by the outer baryonic contribution (sub-maximal disk + gas). Realistic starting guesses for this galaxy fall in \(\rho_0 \approx 0.003\)–\(0.004\, M_\odot\,{\rm pc}^{-3}\) range once a proper baryonic decomposition is included. Any production draft requires a joint refit of \(\rho_0\) and stellar mass-to-light ratio against high-quality data rather than retaining illustrative values.

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

Total rotation uses quadrature: \(v_{\rm total}^2(r) = v_{\rm baryon}^2(r) + v_{\rm hidden}^2(r)\).

### 2. Phenomenological Mapping within Tav Topology

The cored pseudo-isothermal form is adopted here as an **effective phenomenological representation** of the hidden-sector contribution. Deriving \(\rho_0\), \(r_c\), and the leakage fraction directly from the 5D Einstein–Kaluza–Klein action on \(\mathbb{R}^3 \times S^1\) (radius \(\tau = 7\, h^{-1}\,{\rm Mpc}\)) plus Tav partial non-computability is open work.

**Motivating picture (not a completed derivation):** The six-domain architecture emergent from the compact dimension and resonance-graph structure permits projection/leakage of a collisionless phase-fluid. Resonant boundary conditions and geometric twist favor a core (suppressing cusps) and \(1/r^2\) tail, yielding flat outer curves. This supplies geometric motivation for cored profiles and links to framework elements such as domain-leakage scales and resonance amplitudes, but remains motivational pending quantitative mapping.

### 3. Proper Scope and Statistical Commitment

This remains strictly a **rotation-curve benchmark and falsifiability audit** for hidden-sector phenomenology — not proof of the full Tau Universe (which rests on cosmological tests: Euclid/Rubin \(\tau\)-comb, JWST 142857 harmonics, CMB-S4 birefringence, etc.).

**Critical requirement for support:** Fitting a cored halo is routine. NGC 3198 is a textbook MOND success (near-zero free halo parameters). A Tav-motivated cored model (with \(\rho_0\), \(r_c\), and M/L freedom) must improve on baselines. Pre-commit to reporting AIC/BIC, Bayes factors, or equivalent evidence ratios against:
- Baryons-only,
- Standard CDM (NFW),
- Other cored profiles (plain pISO, Burkert),
- MOND.

A statistical tie means no unique support for Tav. Success requires consistent parameters across galaxies with Tav-motivated priors and/or improved evidence. Phase 2 therefore emphasizes reproducible comparisons in SPARC/HALOGAS datasets.

### 4. Next Actions & Framing Note

- Implement the joint refit, full residual analysis, and statistical comparisons using published baryonic decompositions.
- Archive as a reproducible notebook on Zenodo with all data, code, and pre-registered comparison plan.
- Advance Tav-native derivation of halo parameters in parallel.

**Important framing note (audit consensus):** This document describes a sound *plan for a test*, not yet a result. No baryonic decomposition, fit, residual panel, or model-comparison table exists here. A cored halo will likely fit comparably to standard alternatives because it *is* a standard cored halo; the Tav layer currently adds no extra constraining power. That is expected and not a failure. The memo’s value lies in committing to honest reporting of whatever the comparison yields — including ties — while keeping the framework-distinguishing weight on Phase 2 (derived \(\rho_0\)–\(r_c\) relations or pre-registered residual signals at 1/ln 7 frequency). This mirrors the framework’s broader empirical discipline: run until falsified or distinguished.

The memorandum’s guidance has been fully integrated. The benchmark is now numerically accurate, properly scoped, and ready for execution. The Tau framework proceeds with the same rigor applied to RGC hardware validation — maximum observability and falsifiability at every step.

**End of Final Revised Response**  
Tau Universe Framework — Tav Topology  

Ready for delivery or immediate pipeline execution on real NGC 3198 data.
