# Pre-Registration — NGC 3198 Hidden-Sector Cored-Halo Benchmark

**Status:** Registered *before* fitting. Any deviation from this plan will be disclosed in a dated "Deviations" section, with the original commit hash, so readers can distinguish pre-planned analysis from post-hoc choices.

**Version:** 1.0 · **Date registered:** `<fill on commit>` · **Commit:** `<hash>`

---

## 0. Purpose and what pre-registration buys

Fitting a cored halo to a single rotation curve is trivially easy and proves nothing on its own. The only way this exercise can carry evidential weight is if the model set, parameter priors, comparison metric, decision thresholds, and the Phase 2 residual frequency are all fixed **in advance**. This document does that. It converts "we fit the curve" into a falsifiable test with stated outcomes.

This is a benchmark of an *effective* representation. It is **not** a test of, or evidence for, the wider Tau Universe / Tav Topology framework, except insofar as the pre-registered Phase 2 residual test (Section 7) could in principle detect a framework-specific signature.

---

## 1. Hypotheses

**Phase 1 (smooth model).**
- **H0 (null):** A hidden-sector cored (pseudo-isothermal) halo fits NGC 3198 **no better** than standard baselines (baryons-only, NFW, Burkert, plain pISO, MOND), by the comparison metric in Section 5.
- **H1:** The cored-halo model is favored over one or more baselines beyond the decision threshold in Section 5.

The honest prior expectation is that **H0 will not be rejected** — the cored model is expected to tie with Burkert/pISO/MOND, because it *is* a standard cored halo. A tie is a valid, reportable outcome, not a failure.

**Phase 2 (residual structure).**
- **H0':** Residuals after the best smooth model contain no log-periodic signal at the fixed frequency 1/ln 7.
- **H1':** A log-periodic residual at frequency 1/ln 7 is favored over the null and over a free-frequency sinusoid, surviving the systematics controls in Section 7.

---

## 2. Data

- **Target:** NGC 3198 (single galaxy; no galaxy selection performed after seeing fits).
- **Primary source:** the SPARC database entry (Lelli, McGaugh & Schombert 2016), providing `r`, `Vobs`, `eVobs`, `Vgas`, `Vdisk` at 3.6 μm; cross-checked against Begeman 1989 and Karukes, Salucci & Gentile 2015 (extended HI to ~48 kpc).
- **Frozen on ingestion:** the CSV used for fitting will be committed unchanged to `data/ngc3198_rotation_curve.csv`. No points will be added, removed, or reweighted after fits begin except per the pre-stated quality cut below.
- **Quality cut (fixed now):** include all published points with `eVobs > 0`; exclude only flagged/asymmetric points already marked unreliable in the source. No outlier rejection based on fit residuals.

---

## 3. Models compared

| Model | Free parameters | Notes |
|---|---|---|
| Baryons-only | Υ_disk | Establishes the missing-mass gap honestly. |
| NFW | ρ_s (or c), r_s, Υ_disk | ΛCDM-standard cusped halo. |
| Burkert | ρ_0, r_c, Υ_disk | Standard cored halo. |
| pseudo-isothermal (plain) | ρ_0, r_c, Υ_disk | Same shape as the Tav-motivated model, no framework interpretation. |
| **Tav-hidden pISO** | ρ_0, r_c, Υ_disk | The model of interest. Identical functional form to plain pISO. |
| MOND (simple/standard μ) | Υ_disk (a_0 fixed) | Near-zero free halo parameters; a hard baseline for this galaxy. |

The Tav-hidden pISO and plain pISO are **functionally identical**; they will return the same fit. This is stated deliberately: at Phase 1 the framework adds no constraining power, so the two cannot be distinguished. Distinguishing power, if any, comes only from Phase 2 or from a future derivation of ρ_0–r_c (out of scope here).

---

## 4. Priors and nuisance parameters (fixed now)

**Halo (pISO / Tav-hidden pISO):**
- ρ_0: log-uniform over [1×10⁻⁴, 5×10⁻²] M⊙ pc⁻³ (brackets both the realistic ~0.003–0.004 target and the illustrative 0.0160).
- r_c: uniform over [0.5, 30] kpc.

**NFW:** log-uniform priors on c ∈ [1, 40] and on virial mass spanning the plausible range for an L* spiral; reparameterize to (ρ_s, r_s) internally.

**Burkert:** ρ_0 log-uniform [1×10⁻⁴, 5×10⁻²] M⊙ pc⁻³; r_c uniform [0.5, 30] kpc.

**Stellar mass-to-light (shared across models):**
- Υ_disk (3.6 μm): Gaussian prior N(0.5, 0.1) following the SPARC convention; truncated to (0.1, 1.0).

**Nuisance (marginalized, Gaussian priors from literature):**
- Distance D: N(13.8, 1.4) Mpc.
- Inclination i: N(71.5°, 3°).
- (Both rescale the model curve; included so quoted parameters are not falsely precise.)

`G = 4.30091×10⁻⁶ kpc (km/s)² M⊙⁻¹` is fixed. Density conversion `rho0_kpc = rho0_pc × 1e9` is enforced by `tests/test_units.py`.

---

## 5. Inference and model comparison (fixed now)

- **Likelihood:** Gaussian in `Vobs` with variance `eVobs²` (plus inclination/distance marginalization). Components added in quadrature: `v_model² = v_gas² + Υ_disk v_disk² + v_halo²`.
- **Sampler:** MCMC (emcee) for posteriors; nested sampling (dynesty) for Bayesian evidence where feasible.
- **Reported per model:** best-fit parameters with 16/50/84 percentiles, reduced χ², AIC, BIC, and log-evidence (ln Z) when available.
- **Decision rule (set in advance):**
  - **AIC/BIC:** a model is "favored" only if it improves on a baseline by **ΔBIC > 6** (Kass & Raftery "strong"). |ΔBIC| ≤ 6 is declared a **tie**.
  - **Bayes factor:** ln B > 3 ("strong"), > 5 ("very strong") to claim support; |ln B| ≤ 3 is a tie.
  - Because BIC penalizes parameters, a 3-parameter cored model must materially out-fit a near-0-extra-parameter MOND fit to be "favored" over it. This is expected to be difficult for this galaxy.

---

## 6. Outcomes table (committed in advance)

| Phase 1 result | Interpretation | Reported as |
|---|---|---|
| Cored model ties baselines | Expected. No unique support for the mapping. | Honest tie; benchmark succeeds as a benchmark. |
| Cored model beats NFW only | Galaxy prefers a core (well-known for NGC 3198). | Consistent with literature; not Tav-specific. |
| Cored model beats all incl. MOND beyond threshold | Surprising; scrutinize for overfitting / systematics. | Report with full skepticism and robustness checks. |
| Fit needs extreme Υ_disk or halo params | Model strained. | Reported honestly; flagged as a limitation. |

No outcome is suppressed. A null/tie result is published with the same prominence as any other.

---

## 7. Phase 2 — pre-registered residual test

Run **only after** the smooth model in Phase 1 is finalized. Residuals: `Δv(r) = Vobs(r) − v_model_smooth(r)`.

Fitted residual model (**frequency fixed, not searched**):

```
Δv(r) = A · sin( 2π · ln(r / r0) / ln(7) + φ )
```

Fixed in advance:
- **r0 = 1.0 kpc** (reference radius; fixed, not fit).
- **Frequency = 1/ln 7** in ln-radius (this is the entire point — no frequency search).
- **A prior:** half-normal, scale 10 km/s, truncated to [0, 30] km/s.
- **φ prior:** uniform [0, 2π).
- **Radial range:** the full fitted range used in Phase 1.
- **Significance threshold:** require **ln B > 5** for the 1/ln 7 sinusoid vs. a flat (A = 0) null, **and** that a free-frequency sinusoid does not prefer a materially different frequency (if it does, the 1/ln 7 detection is rejected as coincidental).

**Look-elsewhere:** minimal by construction, because the frequency, r0, and radial range are fixed before looking. The free-frequency cross-check guards against the fixed frequency accidentally landing on noise.

**Systematics that can mimic or kill a residual signal (all checked before any claim):** distance and inclination uncertainty, beam smearing in the inner curve, non-circular motions (bars, spiral arms, warps), gas asymmetries, and asymmetric drift corrections. A candidate signal that does not survive all of these is reported as a non-detection.

**Phase 2 outcomes:**
- **Detection surviving all checks:** a genuinely interesting, framework-relevant result — reported as such, with the caveat that one galaxy is not confirmation.
- **Null:** places an upper limit on the residual amplitude (local Tav coupling strength). Does **not** falsify the framework; constrains it.

---

## 8. Reproducibility and provenance

- All figures regenerable from public code + the frozen `data/` CSV with a pinned `requirements.txt`.
- `tests/test_units.py` must pass in CI before any fit is run.
- Drafting was AI-assisted across multiple systems; all numerical results independently verified. The original unit-conversion diagnosis came from an external technical audit (NGC 3198 Hidden-Sector Halo Test, June 2026), gratefully credited.

## 9. Citation

Cite this pre-registration by its Zenodo DOI: `<add DOI here>`. The executed benchmark, when complete, will cite this DOI as its registered plan.

---

*Registered before data fitting. The value of this document is that it cannot be quietly edited after the result is known — the commit history is the record.*
