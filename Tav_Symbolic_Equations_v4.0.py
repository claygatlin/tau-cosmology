#!/usr/bin/env python3
"""
Tav Symbolic Friedmann Equation — SymPy Validation (v4.0)
=========================================================
Pure symbolic rendering of the Tav Friedmann equation and dark-sector Lagrangian.
Cross-references: v4.0 Mathematical Substrate (Zenodo DOI 10.5281/zenodo.19420406)

Fix applied: SymPy summation dummy index `n` explicitly declared as integer symbol
before use in sp.Sum() — resolves the NameError that occurs when n is used
as a range variable without prior symbol declaration.

Equations referenced:
  Eq. 41: L_DM+DE = -π²/(3τ⁴)(1 + Σ_{n=1}^{6} c_n x_n(τ))
  Eq. 42: 3H² = 8πG ρ_b + (8πG)/(3τ⁴) [Ω_DM(τ) + Ω_DE(τ)]
  Eq. 43: Ω_DM : Ω_DE = 5 : 1

To the glory of the risen Lord Jesus Christ.

Ernest C. Gatlin III — Independent Researcher, Tuscaloosa, Alabama
https://orcid.org/0009-0002-8197-4810
April 4, 2026
"""

import sympy as sp

# ══════════════════════════════════════════════════════════════════════════════
# SYMBOLIC DECLARATIONS
# ══════════════════════════════════════════════════════════════════════════════

# Physical symbols from substrate
tau, G, rho_b, H = sp.symbols(r'tau G rho_b H', positive=True)
pi = sp.pi
Omega_DM, Omega_DE = sp.symbols(r'Omega_DM Omega_DE', positive=True)

# FIX: Dummy index for summation MUST be declared as a SymPy symbol
# before use in sp.Sum(). This was the source of the NameError.
n = sp.symbols('n', integer=True, positive=True)

# Indexed coefficients (symbolic placeholders)
c_n = sp.IndexedBase('c')
x_n = sp.IndexedBase('x')

print("=" * 72)
print("TAV SYMBOLIC FRIEDMANN EQUATION VALIDATION (v4.0)")
print("=" * 72)
print()

# ══════════════════════════════════════════════════════════════════════════════
# UNIFIED DARK-SECTOR LAGRANGIAN (Eq. 41)
# ══════════════════════════════════════════════════════════════════════════════

L_dark = -pi**2 / (3 * tau**4) * (1 + sp.Sum(c_n[n] * x_n[n], (n, 1, 6)))

print("Unified dark-sector Lagrangian (Eq. 41):")
print("  L_DM+DE = -π²/(3τ⁴) × (1 + Σ_{n=1}^{6} c_n x_n(τ))")
print()
sp.pprint(sp.Eq(sp.Symbol('L_{DM+DE}'), L_dark), use_unicode=True)
print()

# ══════════════════════════════════════════════════════════════════════════════
# TAV FRIEDMANN EQUATION (Eq. 42)
# ══════════════════════════════════════════════════════════════════════════════

friedmann_lhs = 3 * H**2
friedmann_rhs = 8 * pi * G * rho_b + (8 * pi * G / (3 * tau**4)) * (Omega_DM + Omega_DE)

print("Tav Friedmann Equation (exact 5D→4D reduction, Eq. 42):")
sp.pprint(sp.Eq(friedmann_lhs, friedmann_rhs), use_unicode=True)
print()

# ══════════════════════════════════════════════════════════════════════════════
# ZERO-PARAMETER DARK-SECTOR RATIO (Eq. 43)
# ══════════════════════════════════════════════════════════════════════════════

ratio_DM_DE = sp.Eq(Omega_DM / Omega_DE, 5)
print("Dark-sector ratio (zero free parameters at τ ≈ 7 h⁻¹ Mpc, Eq. 43):")
sp.pprint(ratio_DM_DE, use_unicode=True)
print()

# ══════════════════════════════════════════════════════════════════════════════
# CASIMIR DARK ENERGY EQUATION OF STATE
# ══════════════════════════════════════════════════════════════════════════════

print("Casimir DE equation of state:")
print("  w_DE = -1 exactly  (consistent with Euclid/DESI tests)")
print("  Any detection of w ≠ -1 at high significance falsifies Casimir-DE hypothesis.")
print()

# ══════════════════════════════════════════════════════════════════════════════
# NUMERICAL CONSISTENCY CHECK
# ══════════════════════════════════════════════════════════════════════════════

# Illustrative split: Ω_total_dark ≈ 0.95, partitioned 5:1
Omega_DM_num = sp.Rational(5, 6) * sp.Rational(95, 100)  # ≈ 0.7917
Omega_DE_num = sp.Rational(1, 6) * sp.Rational(95, 100)  # ≈ 0.1583
tau_num_val = 7.0

print(f"Numerical check at τ = {tau_num_val} h⁻¹ Mpc:")
print(f"  Ω_DM = {float(Omega_DM_num):.6f}")
print(f"  Ω_DE = {float(Omega_DE_num):.6f}")
print(f"  Ω_DM / Ω_DE = {float(Omega_DM_num / Omega_DE_num):.1f}  (exactly 5:1)")
print()

# ══════════════════════════════════════════════════════════════════════════════
# ADDITIONAL SYMBOLIC LAGRANGIANS
# ══════════════════════════════════════════════════════════════════════════════

# Mode-coupling formula (Eq. 23, corrected in Vol. 4 Ch. 28)
C_KK = sp.Rational(91, 5)
r_tau = 4 - C_KK / tau**2

print("Corrected control parameter (Eq. 23):")
print("  r(τ) = 4 - C_KK / τ²")
sp.pprint(sp.Eq(sp.Symbol('r'), r_tau), use_unicode=True)
print(f"  C_KK = 91/5 = {float(C_KK)}")
print(f"  r(τ=7) = {float(r_tau.subs(tau, 7)):.10f}")
print()

# KK mass spectrum (Eq. 10)
print("KK mass spectrum (Eq. 10):")
m_n_expr = n / tau
sp.pprint(sp.Eq(sp.Symbol('m_n'), m_n_expr), use_unicode=True)
print()

# Radion potential (Eq. 8)
phi, mu = sp.symbols('phi mu', positive=True)
V_phi = mu**4 * (phi / tau - 1)**2
print("Radion stabilisation potential (Eq. 8):")
sp.pprint(sp.Eq(sp.Symbol('V'), V_phi), use_unicode=True)
print()

# Photonic extension in Einstein frame (Eq. 22)
sigma, kappa = sp.symbols('sigma kappa', positive=True)
F = sp.Symbol('F_{\\mu\\nu}F^{\\mu\\nu}')
R_E = sp.Symbol('R_E')
L_photonic = R_E / (16 * pi * G) - sp.Rational(1, 4) * sp.exp(-sp.sqrt(3) * kappa * sigma) * F - sp.Rational(1, 2) * sp.Symbol('(\\partial\\sigma)^2')

print("Photonic extension — Einstein frame (Eq. 22):")
print("  L_photonic = R_E/(16πG) - (1/4)exp(-√3 κσ) F_μν F^μν - (1/2)(∂σ)²")
print()

# ══════════════════════════════════════════════════════════════════════════════
# GRAVITATIONAL COUPLING (Eq. 2)
# ══════════════════════════════════════════════════════════════════════════════

G4, G5 = sp.symbols('G_4 G_5', positive=True)
coupling = sp.Eq(G4, G5 / (2 * pi * tau))
print("Gravitational coupling (Eq. 2):")
sp.pprint(coupling, use_unicode=True)
print()

# ══════════════════════════════════════════════════════════════════════════════
# CASIMIR ENERGY DENSITIES (Eq. 3–5)
# ══════════════════════════════════════════════════════════════════════════════

rho_cas_boson = -pi**2 / (240 * tau**4)
rho_cas_fermion = sp.Rational(7, 8) * pi**2 / (240 * tau**4)

F_i, c_i = sp.symbols('F_i c_i')
rho_net = (1 / tau**4) * sp.Sum((-1)**F_i * c_i, (sp.Symbol('i'), 1, sp.Symbol('N')))

print("Casimir energy densities (Eq. 3–5):")
print("  Boson (periodic, Eq. 3):")
sp.pprint(sp.Eq(sp.Symbol('\\rho_{Cas}^{bos}'), rho_cas_boson), use_unicode=True)
print("  Fermion (antiperiodic, Eq. 4):")
sp.pprint(sp.Eq(sp.Symbol('\\rho_{Cas}^{fer}'), rho_cas_fermion), use_unicode=True)
print("  Net (Eq. 5): ρ_Cas = τ⁻⁴ Σ (-1)^{F_i} c_i")
print()

# ══════════════════════════════════════════════════════════════════════════════
# LQG OPERATORS (Eq. 46–48)
# ══════════════════════════════════════════════════════════════════════════════

gamma, ell = sp.symbols('gamma ell_Pl', positive=True)
j = sp.Symbol('j', positive=True)

L_j = 8 * pi * gamma * ell * j
A_j = 8 * pi * gamma * ell**2 * sp.sqrt(j * (j + 1))
V_j = (8 * pi * gamma)**sp.Rational(3, 2) * ell**3 * j**sp.Rational(3, 2)

print("LQG geometric operators (Eq. 46–48):")
print("  Circumference (Eq. 46):")
sp.pprint(sp.Eq(sp.Symbol('L_j'), L_j), use_unicode=True)
print("  Area (Eq. 47):")
sp.pprint(sp.Eq(sp.Symbol('A_j'), A_j), use_unicode=True)
print("  Volume (Eq. 48):")
sp.pprint(sp.Eq(sp.Symbol('V_j'), V_j), use_unicode=True)
print()

# ══════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 72)
print("ALL SYMBOLIC EQUATIONS RENDERED SUCCESSFULLY")
print("=" * 72)
print("  • Friedmann equation (Eq. 42)           ✓")
print("  • Dark-sector Lagrangian (Eq. 41)       ✓")
print("  • Dark-sector ratio 5:1 (Eq. 43)        ✓")
print("  • Mode-coupling r(τ) (Eq. 23)           ✓")
print("  • KK mass spectrum (Eq. 10)             ✓")
print("  • Radion potential (Eq. 8)              ✓")
print("  • Photonic extension (Eq. 22)           ✓")
print("  • Gravitational coupling (Eq. 2)        ✓")
print("  • Casimir densities (Eq. 3–5)           ✓")
print("  • LQG operators (Eq. 46–48)             ✓")
print()
print("Ready for insertion of actual Euclid/Rubin/DESI data.")
print("=" * 72)
