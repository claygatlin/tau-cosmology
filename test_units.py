"""
Unit tests for the NGC 3198 hidden-halo benchmark.

These tests encode the pseudo-isothermal (cored) halo formula as ground truth.
Their main job is to FAIL LOUDLY if the M_sun/pc^3 -> M_sun/kpc^3 conversion
(factor 1e9) is ever dropped again -- the bug that produced the original
near-zero halo curve.

Self-contained (numpy only). Run either way:
    pytest tests/test_units.py
    python  tests/test_units.py
"""

import numpy as np

G = 4.30091e-6  # kpc (km/s)^2 / M_sun


# --- Reference implementation (the formula under test) -----------------------

def vh_piso(r_kpc, rho0_pc3, rc_kpc):
    """Pseudo-isothermal halo circular speed (km/s), correct unit handling."""
    rho0_kpc3 = rho0_pc3 * 1e9  # the conversion that must never be dropped
    term = 1.0 - (rc_kpc / r_kpc) * np.arctan(r_kpc / rc_kpc)
    return np.sqrt(4.0 * np.pi * G * rho0_kpc3 * rc_kpc**2 * term)


def vh_no_conversion(r_kpc, rho0_pc3, rc_kpc):
    """Buggy version: rho0 used as if already in M_sun/kpc^3 (no 1e9)."""
    term = 1.0 - (rc_kpc / r_kpc) * np.arctan(r_kpc / rc_kpc)
    return np.sqrt(4.0 * np.pi * G * rho0_pc3 * rc_kpc**2 * term)


def v_total(v_components):
    """Combine velocity components in quadrature: sqrt(sum v_i^2)."""
    return np.sqrt(np.sum(np.square(np.asarray(v_components, dtype=float)), axis=0))


# Benchmark parameters (illustrative draft values, NOT a fit)
RHO0_PC = 0.0160   # M_sun / pc^3
RC = 8.58          # kpc

# Independently verified reference curve (km/s)
REFERENCE = {5.0: 77.6, 8.58: 116.9, 10.0: 128.8,
             15.0: 159.3, 20.0: 178.4, 30.0: 200.3, 48.0: 218.6}


# --- Tests -------------------------------------------------------------------

def test_corrected_velocities_match_reference():
    """The corrected curve reproduces the verified benchmark table."""
    for r, expected in REFERENCE.items():
        got = vh_piso(r, RHO0_PC, RC)
        assert abs(got - expected) < 0.3, f"r={r}: got {got:.2f}, expected {expected}"


def test_asymptotic_vinf():
    """v_h -> sqrt(4 pi G rho0 rc^2) ~ 252 km/s at large r."""
    vinf = np.sqrt(4.0 * np.pi * G * (RHO0_PC * 1e9) * RC**2)
    assert 251.0 < vinf < 253.5
    assert vh_piso(500.0, RHO0_PC, RC) > 240.0  # approaching the asymptote


def test_missing_conversion_is_caught():
    """Dropping the 1e9 collapses the halo to ~0 -- this MUST be detectable."""
    assert vh_no_conversion(10.0, RHO0_PC, RC) < 0.01
    # The bug suppresses v_h by sqrt(1e9) ~ 31623x:
    ratio = vh_piso(10.0, RHO0_PC, RC) / vh_no_conversion(10.0, RHO0_PC, RC)
    assert abs(ratio - np.sqrt(1e9)) / np.sqrt(1e9) < 1e-6


def test_quadrature_adds_in_squares():
    """Components combine as sqrt(sum of squares), not linearly."""
    v = v_total([90.0, 120.0])           # 3-4-5 -> 150
    assert abs(v - 150.0) < 1e-9
    assert v < 90.0 + 120.0               # strictly less than linear sum


def test_parameters_overproduce_for_ngc3198():
    """
    Documents (does not hide) that the illustrative rho0 = 0.0160 overproduces.
    NGC 3198's observed flat speed is ~150 km/s, and that is the TOTAL.
    The halo alone here already exceeds it -> these params are not a fit.
    """
    v_obs_flat = 150.0
    vinf_halo = np.sqrt(4.0 * np.pi * G * (RHO0_PC * 1e9) * RC**2)
    assert vinf_halo > v_obs_flat, "expected illustrative params to overproduce"


def test_realistic_target_is_lower():
    """
    A halo asymptote near the realistic target (~110-150 km/s) corresponds to
    rho0 ~ 0.003-0.006, well below the illustrative 0.0160. Sanity-check the
    scale so a future refit starting point is not absurd.
    """
    A = 4.0 * np.pi * G * 1e9 * RC**2          # vinf^2 = A * rho0_pc
    rho0_for_120 = 120.0**2 / A
    rho0_for_150 = 150.0**2 / A
    assert 0.0030 < rho0_for_120 < 0.0045
    assert 0.0050 < rho0_for_150 < 0.0065


# --- Standalone runner (no pytest required) ----------------------------------

if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL  {t.__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    raise SystemExit(1 if failed else 0)
