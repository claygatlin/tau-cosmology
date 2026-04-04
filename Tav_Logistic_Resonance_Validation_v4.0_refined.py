#!/usr/bin/env python3
"""
Tav Logistic Resonance Map Validation — Refined v4.0
=====================================================
From Volume 4, Ch. 28 — Corrected r(τ) = 4 - C_KK/τ²
Cross-references: v4.0 Mathematical Substrate (Zenodo DOI 10.5281/zenodo.19420406)

Equations referenced:
  Eq. 23: r(τ) = 4 - C_KK / τ²
  Eq. 24: C_KK = (1/N_d) Σ n² for n=1..N_cut
  Eq. 25: Σ_{n=1}^{6} n² = 91, C_KK = 91/5 = 18.2
  Eq. 26: r(τ=7) ≈ 3.6286
  Eq. 27: r_ss6 = 3.627557529515524
  Eq. 29: Superstable orbit points
  Eq. 30: π_log = (1 4 3 5 2 6)
  Eq. 32: π_×10 = (1 3 2 6 4 5)
  Eq. 37: H_Tav = log₂6 ≈ 2.58496 bits

To the glory of the risen Lord Jesus Christ.

Ernest C. Gatlin III — Independent Researcher, Tuscaloosa, Alabama
https://orcid.org/0009-0002-8197-4810
April 4, 2026
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for file output
import matplotlib.pyplot as plt
from fractions import Fraction

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1: Mode-Coupling Constant C_KK (Eq. 24–25)
# ══════════════════════════════════════════════════════════════════════════════

N_cut = 6   # Computable prefix (number of observable KK harmonics)
N_d = 5     # 5D graviton polarisations: D(D-3)/2 = 5×2/2 = 5

sum_n2 = sum(n**2 for n in range(1, N_cut + 1))
assert sum_n2 == 91, f"Sum of squares check failed: got {sum_n2}"
assert sum_n2 == N_cut * (N_cut + 1) * (2 * N_cut + 1) // 6  # Closed-form check

C_KK = Fraction(sum_n2, N_d)  # Exact rational: 91/5
C_KK_float = float(C_KK)

print("=" * 72)
print("SECTION 1: Mode-Coupling Constant (Eq. 24–25)")
print("=" * 72)
print(f"  N_cut = {N_cut} (computable prefix)")
print(f"  N_d   = {N_d} (5D graviton polarisations)")
print(f"  Σ n² (n=1..6) = {sum_n2} = 7 × 13")
print(f"  C_KK = {sum_n2}/{N_d} = {C_KK} = {C_KK_float}")
print()

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2: Control Parameter r(τ) (Eq. 23, 26–27)
# ══════════════════════════════════════════════════════════════════════════════

tau_observed = 7.0  # h⁻¹ Mpc (measured compact radius)

def r_of_tau(tau, c_kk=C_KK_float):
    """Corrected mode-coupling formula: r(τ) = 4 - C_KK / τ² (Eq. 23)"""
    return 4.0 - c_kk / tau**2

r_at_7 = r_of_tau(tau_observed)

# Superstable period-6 value (machine-precision, Eq. 27)
r_ss6 = 3.627557529515524

# Exact C_KK required for perfect match
C_KK_exact = tau_observed**2 * (4.0 - r_ss6)
N_d_eff = 91.0 / C_KK_exact

match_pct = abs(r_at_7 - r_ss6) / r_ss6 * 100

print("=" * 72)
print("SECTION 2: Control Parameter r(τ) (Eq. 23, 26–27)")
print("=" * 72)
print(f"  r(τ=7) = {r_at_7:.10f}  (from closed-form, Eq. 26)")
print(f"  r_ss6  = {r_ss6:.15f}  (superstable period-6, Eq. 27)")
print(f"  Match  = {match_pct:.4f}%  (substrate reports 0.27%)")
print(f"  C_KK(exact)  = {C_KK_exact:.4f}")
print(f"  N_d(eff)     = {N_d_eff:.3f} ≈ 5  (pure 5D gravity)")
print()

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3: Superstable 6-Cycle Orbit (Eq. 29)
# ══════════════════════════════════════════════════════════════════════════════

def logistic_orbit(r, n_steps=6, x0=0.5):
    """Compute the logistic orbit starting from x0 for n_steps iterations."""
    orbit = [x0]
    x = x0
    for _ in range(n_steps):
        x = r * x * (1.0 - x)
        orbit.append(x)
    return np.array(orbit)

# Reference orbit from substrate Eq. 29 (Volume 4, Ch. 28)
orbit_reference = np.array([
    0.500000000000,
    0.906889382379,
    0.306314696017,
    0.770805200175,
    0.640860795182,
    0.834912243363,
    0.500000000000
])

# Compute orbits at both r values
orbit_at_r7 = logistic_orbit(r_at_7)
orbit_at_rss6 = logistic_orbit(r_ss6)

print("=" * 72)
print("SECTION 3: Superstable 6-Cycle Orbit (Eq. 29)")
print("=" * 72)
print(f"{'k':>3}  {'x_k (r(7))':>14}  {'x_k (r_ss6)':>14}  {'x_k (ref)':>14}  {'Δ(r7-ref)':>12}")
print("-" * 72)
for k in range(7):
    delta = abs(orbit_at_r7[k] - orbit_reference[k])
    print(f"{k:3d}  {orbit_at_r7[k]:14.10f}  {orbit_at_rss6[k]:14.10f}  "
          f"{orbit_reference[k]:14.10f}  {delta:12.2e}")

# Verify closure: x6 = x0 = 0.5 at r_ss6
closure_error = abs(orbit_at_rss6[-1] - 0.5)
print(f"\nClosure check at r_ss6: |x₆ - 0.5| = {closure_error:.2e}")
print()

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4: Rank-Order Permutation (Eq. 30) and Conjugacy (Theorem 6.1)
# ══════════════════════════════════════════════════════════════════════════════

def rank_order_permutation(orbit_points):
    """
    Compute the rank-order permutation of the 6-cycle orbit.
    Returns 1-based ranks in visitation order.
    """
    points = orbit_points[:6]  # x0 through x5
    # Sort indices by value; rank[i] = position of orbit[i] in sorted order
    sorted_indices = np.argsort(points)
    ranks = np.zeros(6, dtype=int)
    for rank_val, idx in enumerate(sorted_indices):
        ranks[idx] = rank_val + 1  # 1-based
    return ranks

# The visitation-order permutation at r_ss6
ranks_rss6 = rank_order_permutation(orbit_at_rss6)

# Expected from substrate: sorted order is x2 < x0 < x4 < x3 < x5 < x1
# So visitation order (starting from x0) visits ranks: 2, 6, 1, 4, 3, 5
# The permutation π_log as a cycle: (1 4 3 5 2 6) in S₆

# π_×10: multiplication by 10 mod 7 on {1,...,6}
# 1→3→2→6→4→5→1
pi_x10 = {1: 3, 2: 6, 3: 2, 4: 5, 5: 1, 6: 4}

# Conjugating map φ from Theorem 6.1, Eq. 33
phi = {1: 1, 2: 4, 3: 2, 4: 3, 5: 6, 6: 5}
phi_inv = {v: k for k, v in phi.items()}

# Build π_log from the orbit visitation
# The iteration visits x0→x1→x2→x3→x4→x5→x0
# Their ranks are: ranks_rss6[0], ranks_rss6[1], ..., ranks_rss6[5]
# π_log maps rank[i] → rank[i+1]
pi_log = {}
for i in range(6):
    pi_log[ranks_rss6[i]] = ranks_rss6[(i + 1) % 6]

print("=" * 72)
print("SECTION 4: Rank-Order Permutation & Conjugacy (Theorem 6.1)")
print("=" * 72)
print(f"  Ranks at r_ss6 (visitation order): {ranks_rss6}")
print(f"  π_log: {pi_log}")
print(f"  π_×10: {pi_x10}")
print(f"  φ:     {phi}")
print()

# Verify conjugacy: φ ∘ π_log ∘ φ⁻¹ = π_×10
print("  Conjugacy verification (φ ∘ π_log ∘ φ⁻¹ = π_×10):")
conjugacy_ok = True
for n in range(1, 7):
    # φ(π_log(φ⁻¹(n)))
    step1 = phi_inv[n]
    step2 = pi_log[step1]
    result = phi[step2]
    expected = pi_x10[n]
    match = "✓" if result == expected else "✗"
    if result != expected:
        conjugacy_ok = False
    print(f"    n={n}: φ(π_log(φ⁻¹({n}))) = φ(π_log({step1})) = φ({step2}) = {result}"
          f"  = π_×10({n}) = {expected}  {match}")

print(f"\n  Conjugacy theorem: {'VERIFIED' if conjugacy_ok else 'FAILED'}")
print()

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5: Shannon Entropy (Eq. 37)
# ══════════════════════════════════════════════════════════════════════════════

H_tav_exact = np.log2(6)
# Also compute from uniform probabilities
probs = np.ones(6) / 6.0
H_tav_computed = -np.sum(probs * np.log2(probs))

print("=" * 72)
print("SECTION 5: Shannon Entropy (Eq. 37)")
print("=" * 72)
print(f"  H_Tav = log₂(6) = {H_tav_exact:.10f} bits  (exact)")
print(f"  H_Tav (computed from uniform 6-state) = {H_tav_computed:.10f} bits")
print(f"  Match: {abs(H_tav_exact - H_tav_computed) < 1e-15}")
print()

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6: Period-Doubling Cascade in τ-Space (Table from §6)
# ══════════════════════════════════════════════════════════════════════════════

cascade_data = [
    (1,   2.000000,     "Fixed point"),
    (2,   3.236068,     "Period-2"),
    (4,   3.498562,     "Period-4"),
    (8,   3.554641,     "Period-8"),
    (16,  3.566667,     "Period-16"),
    ("∞", 3.569946,     "Feigenbaum accumulation"),
    (6,   3.627558,     "Period-6 (island of stability)"),
]

print("=" * 72)
print("SECTION 6: Period-Doubling Cascade in τ-Space (§6 Table)")
print("=" * 72)
print(f"{'Period':>8}  {'r_ss':>12}  {'τ_ss (h⁻¹ Mpc)':>16}  {'Dynamics'}")
print("-" * 72)
for period, r_ss, dynamics in cascade_data:
    if isinstance(r_ss, (int, float)) and r_ss < 4.0:
        tau_ss = np.sqrt(C_KK_float / (4.0 - r_ss))
    else:
        tau_ss = float('nan')
    print(f"{str(period):>8}  {r_ss:12.6f}  {tau_ss:16.3f}  {dynamics}")
print()

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 7: Period-6 Window Plot in τ-Space
# ══════════════════════════════════════════════════════════════════════════════

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Panel A: r(τ) in the period-6 window
taus = np.linspace(5.0, 9.0, 1000)
rs = r_of_tau(taus)

ax = axes[0]
ax.plot(taus, rs, 'b-', lw=2, label=r'$r(\tau) = 4 - C_{KK}/\tau^2$')
ax.axhline(r_ss6, color='r', ls='--', lw=1.5, label=f'$r_{{ss6}} = {r_ss6:.4f}$')
ax.axhline(3.569946, color='orange', ls=':', lw=1, label=r'$r_\infty$ (Feigenbaum)')
ax.axvline(7.0, color='g', ls=':', lw=1.5, label=r'$\tau = 7\;h^{-1}$ Mpc')
ax.axhspan(3.6266, 3.6304, color='green', alpha=0.15, label='Period-6 window')
ax.set_xlabel(r'$\tau$ ($h^{-1}$ Mpc)', fontsize=12)
ax.set_ylabel(r'$r(\tau)$', fontsize=12)
ax.set_title('Control Parameter vs Compact Radius', fontsize=13)
ax.legend(fontsize=9, loc='lower right')
ax.set_ylim(3.0, 4.0)
ax.grid(True, alpha=0.3)

# Panel B: Zoom on the period-6 window
taus_zoom = np.linspace(6.95, 7.08, 500)
rs_zoom = r_of_tau(taus_zoom)

ax = axes[1]
ax.plot(taus_zoom, rs_zoom, 'b-', lw=2)
ax.axhline(r_ss6, color='r', ls='--', lw=1.5, label=f'$r_{{ss6}}$')
ax.axhspan(3.6266, 3.6304, color='green', alpha=0.2, label='Period-6 window')
ax.axvline(6.991, color='gray', ls=':', alpha=0.5)
ax.axvline(7.027, color='gray', ls=':', alpha=0.5)
ax.axvline(7.0, color='g', ls='-', lw=2, alpha=0.7, label=r'$\tau = 7$')
ax.set_xlabel(r'$\tau$ ($h^{-1}$ Mpc)', fontsize=12)
ax.set_ylabel(r'$r(\tau)$', fontsize=12)
ax.set_title(r'Period-6 Window: $\tau \in [6.991, 7.027]$ ($\Delta\tau/\tau \approx 0.5\%$)',
             fontsize=12)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('tav_period6_window.png', dpi=150, bbox_inches='tight')
print("Plot saved: tav_period6_window.png")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 8: Bifurcation Diagram
# ══════════════════════════════════════════════════════════════════════════════

fig2, ax2 = plt.subplots(figsize=(10, 6))

r_range = np.linspace(2.5, 4.0, 2000)
x_init = 0.5
n_settle = 500
n_plot = 100

for r_val in r_range:
    x = x_init
    for _ in range(n_settle):
        x = r_val * x * (1.0 - x)
    xs = []
    for _ in range(n_plot):
        x = r_val * x * (1.0 - x)
        xs.append(x)
    ax2.plot([r_val] * len(xs), xs, 'k,', markersize=0.1)

ax2.axvline(r_ss6, color='r', ls='--', lw=1.5, alpha=0.8, label=f'$r_{{ss6}}$')
ax2.axvline(r_at_7, color='g', ls=':', lw=1.5, alpha=0.8, label=r'$r(\tau=7)$')
ax2.axvline(3.569946, color='orange', ls=':', lw=1, alpha=0.6, label=r'$r_\infty$')
ax2.set_xlabel(r'$r$', fontsize=13)
ax2.set_ylabel(r'$x$', fontsize=13)
ax2.set_title('Logistic Bifurcation Diagram with Tav Period-6 Window', fontsize=13)
ax2.legend(fontsize=10)
ax2.set_xlim(2.5, 4.0)
ax2.set_ylim(0, 1)

plt.tight_layout()
plt.savefig('tav_bifurcation.png', dpi=150, bbox_inches='tight')
print("Plot saved: tav_bifurcation.png")

# ══════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 72)
print("SUMMARY: All Validations")
print("=" * 72)

checks = [
    ("C_KK = 91/5 = 18.2",           C_KK_float == 18.2),
    ("Σ n² = 91 = 7 × 13",           sum_n2 == 91),
    ("r(7) matches r_ss6 to <0.3%",   match_pct < 0.3),
    ("Orbit closure |x₆ - 0.5| < ε",  closure_error < 1e-10),
    ("Conjugacy theorem verified",     conjugacy_ok),
    ("H_Tav = log₂6",                 abs(H_tav_exact - H_tav_computed) < 1e-15),
    ("N_d_eff ≈ 5",                    abs(N_d_eff - 5) < 0.02),
]

all_pass = True
for desc, passed in checks:
    status = "PASS ✓" if passed else "FAIL ✗"
    if not passed:
        all_pass = False
    print(f"  [{status}]  {desc}")

print()
if all_pass:
    print("  ALL CHECKS PASSED — v4.0 Mathematical Substrate validated.")
else:
    print("  SOME CHECKS FAILED — review above.")
print("=" * 72)
