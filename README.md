# NGC 3198 Rotation-Curve Benchmark

**An effective hidden-sector cored-halo benchmark for NGC 3198 — reproducible, falsifiable, and honestly scoped.**

> **Status:** Phase 1 scaffold. This repository currently contains a corrected, independently verified hidden-halo velocity calculation and a unit-conversion guard test. The full galaxy fit, residual analysis, and model comparison are **not yet implemented** — see [Roadmap](#roadmap). This is a *plan for a test*, not a result.

---

## What this is (and is not)

**It is:** a reproducible rotation-curve benchmark. It tests whether a hidden-sector contribution, represented as an effective collisionless cored (pseudo-isothermal) halo, can describe the flat outer rotation curve of NGC 3198 — and, critically, whether it does so any *better* than standard alternatives.

**It is not:** proof of the Tau Universe / Tav Topology framework. A cored halo fitting a rotation curve is routine; it distinguishes this framework from nothing on its own. Any framework-specific claim lives in [Phase 2](#phase-2--what-would-actually-be-tav-specific) and is gated behind pre-registration.

This separation is deliberate and load-bearing. The benchmark stands as galaxy-dynamics work regardless of whether the wider framework holds.

---

## The missing-mass problem, briefly

NGC 3198 is a textbook case: its outer regions rotate too fast to be explained by visible matter alone (van Albada et al. 1985; Begeman 1989). The standard resolutions are a dark-matter halo (NFW, Burkert, pseudo-isothermal) or modified dynamics (MOND). This benchmark adds one more *effective* representation — a hidden-sector cored halo — and compares it head-to-head against those baselines on the same data.

---

## The model

The hidden component is a pseudo-isothermal (cored) halo. Density and circular-speed contribution:

$$\rho_h(r) = \frac{\rho_0}{1 + (r/r_c)^2}, \qquad v_h^2(r) = 4\pi G \rho_0 r_c^2 \left[\, 1 - \frac{r_c}{r}\arctan\!\left(\frac{r}{r_c}\right) \right]$$

Components add **in quadrature**:

$$v_{\text{total}}^2(r) = v_{\text{gas}}^2 + \Upsilon_{\text{disk}} v_{\text{disk}}^2 + \Upsilon_{\text{bulge}} v_{\text{bulge}}^2 + v_h^2(r)$$

with $G = 4.30091 \times 10^{-6}\ \text{kpc}\,(\text{km/s})^2\,M_\odot^{-1}$.

**Units matter.** If $\rho_0$ is quoted in $M_\odot\,\text{pc}^{-3}$ it **must** be converted before entering a kpc-based formula: `rho0_kpc = rho0_pc * 1e9`. Omitting this factor suppresses $v_h$ by $\sqrt{10^9} \approx 31{,}623\times$, collapsing the halo curve to ≈ 0. (This was the original bug this benchmark was built to catch — credit below.)

---

## Verify in 30 seconds

```bash
python3 reproducible_audit_script.py
```

Expected output:

```
Radii (kpc):     [5.0, 10.0, 15.0, 20.0, 30.0, 48.0]
v_hidden (km/s): [77.6, 128.8, 159.3, 178.4, 200.3, 218.6]
```

| r (kpc) | v_hidden (km/s), ρ₀ = 0.0160 M⊙/pc³ |
|--------:|------------------------------------:|
| 5       | 77.6   |
| 10      | 128.8  |
| 15      | 159.3  |
| 20      | 178.4  |
| 30      | 200.3  |
| 48      | 218.6  |

Asymptotically, $v_h \to \sqrt{4\pi G \rho_0 r_c^2} \approx 252\ \text{km/s}$.

### A built-in honesty check on the parameters

The illustrative ρ₀ = 0.0160 M⊙/pc³ **overproduces** for this galaxy. NGC 3198's observed flat speed is ~150 km/s, and that is the *total* — so the halo asymptote must sit *below* 150, with the exact value set by the outer baryonic contribution. Realistic starting guesses fall around **ρ₀ ≈ 0.003–0.004 M⊙/pc³**. The benchmark does not adopt illustrative values; it refits them (see Roadmap). Do not read the table above as a fit — it is a unit-and-formula check only.

---

## Repository structure

**Present now:**

```
reproducible_audit_script.py   # verified hidden-halo velocity calc (the table above)
tests/test_units.py            # fails if the 1e9 conversion is removed
README.md
LICENSE
```

Suggested `tests/test_units.py` assertions:

```python
assert 120.0 < vh_piso(10.0, 0.0160, 8.58) < 140.0   # correct conversion
assert 190.0 < vh_piso(30.0, 0.0160, 8.58) < 210.0
# If rho0 is wrongly treated as M_sun/kpc^3, v_h is ~0:
assert vh_missing_conversion(10.0, 0.0160, 8.58) < 0.01
```

**Roadmap (not yet implemented):**

```
data/ngc3198_rotation_curve.csv   # r, Vobs, eVobs, Vgas, Vdisk, Vbulge
src/halo_models.py                # pISO, NFW, Burkert, MOND, baryons-only
src/fit_ngc3198.py                # joint refit of rho0, rc, stellar M/L
src/model_comparison.py           # AIC/BIC, Bayes factors
figures/ngc3198_corrected_fit.png
figures/ngc3198_residuals.png
figures/ngc3198_model_comparison.png
PREREGISTRATION.md                # comparison set + residual test, fixed before fitting
```

---

## Roadmap

1. **Ingest real data.** Public NGC 3198 decomposition (Begeman 1989; Karukes, Salucci & Gentile 2015, extending to ~48 kpc; or the SPARC entry with V_gas, V_disk).
2. **Baryonic baseline.** Show the missing-mass gap honestly: baryons-only curve, residuals, reduced χ².
3. **Joint refit.** Fit ρ₀, r_c, and stellar M/L. Report posteriors with intervals.
4. **Model comparison.** AIC/BIC or Bayes factors vs **baryons-only, NFW, Burkert, plain pISO, and MOND**.
5. **Residual panel.** v_obs − v_model with uncertainties and a zero line.
6. **Phase 2 (pre-registered).** Only after the smooth model is sound — see below.

---

## Honest expectations

A cored pseudo-isothermal halo will **likely fit NGC 3198 comparably** to Burkert, plain pISO, and MOND — because it *is* a standard cored halo, and the framework layer currently adds no extra constraining power. NGC 3198 is in fact a textbook MOND success with near-zero free halo parameters, which sets a hard bar: a model carrying ρ₀, r_c, and M/L (three free parameters) must *beat* that on criteria that penalize parameters.

**A statistical tie is the expected outcome, and it is not a failure.** It is the benchmark working as designed. The result — whatever it is — gets reported honestly, including ties.

---

## Phase 2 — what would actually be Tav-specific

Two things, and only these, could distinguish the framework empirically:

1. **A derivation.** ρ₀, r_c, and the normalization predicted from the 5D Einstein–Kaluza–Klein action on ℝ³ × S¹ (τ = 7 h⁻¹ Mpc) — not fitted. This is open theoretical work.
2. **A residual signal.** A pre-registered log-periodic residual, fitted *after* subtracting baryons + smooth halo:

   $$\delta v(r) = A \sin\!\left( \frac{2\pi \ln(r/r_0)}{\ln 7} + \phi \right)$$

   Frequency, radial range, amplitude prior, data cuts, and significance threshold are **fixed in advance** (see `PREREGISTRATION.md`). A detection counts only if it survives look-elsewhere correction, distance/inclination uncertainty, beam smearing, and ordinary non-circular motions. A null result places an upper limit; it does not by itself falsify the framework.

---

## Data sources & references

- **SPARC** — Lelli, McGaugh & Schombert 2016 (public rotation curves, Spitzer 3.6 μm photometry)
- van Albada et al. 1985, ApJ — classic NGC 3198 disk+halo analysis
- Begeman 1989, A&A — NGC 3198 HI rotation curve into the outer disk
- Karukes, Salucci & Gentile 2015 — extended HI kinematics to ~48 kpc
- Li, Lelli, McGaugh & Schombert 2020 — why multi-halo comparison across SPARC is standard

## Theoretical context (speculative framework)

The hidden-sector cored-halo mapping is *motivated by* — not derived from — the Tau Universe / Tav Topology framework, an independent, speculative cosmology positing a single compact fifth dimension (S¹, radius τ = 7 h⁻¹ Mpc). The framework is unproven, and some of its predictions have returned null results in current data. Framework materials: https://zenodo.org/communities/tuf2026. Nothing in *this* benchmark depends on the framework being correct.

---

## Reproducibility

Every number in this README is regenerable from `reproducible_audit_script.py` with NumPy only. When the fit pipeline lands, every figure will be regenerable from public code + data with a pinned environment (`requirements.txt`).

## Provenance

This benchmark and its accompanying memo were prepared with AI assistance across multiple systems, with the numerical results independently verified. The original unit-conversion diagnosis came from an external technical audit (NGC 3198 Hidden-Sector Halo Test, June 2026) — that catch is gratefully credited and is the reason this repository exists.

## Citation

If you use this benchmark, please cite the pre-registration DOI: `<add Zenodo DOI here>`.

## License

MIT — see `LICENSE`. *(Edit author/year before publishing.)*

---

*Author: Ernest C. Gatlin III (Clay Gatlin). Edit the placeholders (repo URL, DOI, license year) before pushing.*
