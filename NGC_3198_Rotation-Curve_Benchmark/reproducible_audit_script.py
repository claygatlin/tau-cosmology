import numpy as np

G = 4.300917270e-6          # kpc (km/s)^2 / Msun
rho0_pc = 0.0160            # Msun / pc^3
rho0 = rho0_pc * 1e9        # Msun / kpc^3
rc = 8.58                   # kpc

def v_hidden(r):
    bracket = 1.0 - (rc / r) * np.arctan(r / rc)
    v2 = 4 * np.pi * G * rho0 * rc**2 * bracket
    return np.sqrt(max(v2, 0.0))

radii = np.array([5., 10., 15., 20., 30.])
vels = [round(v_hidden(r), 1) for r in radii]
print("Radii (kpc):", list(radii))
print("v_hidden (km/s):", vels)
# Expected: [77.6, 128.8, 159.3, 178.4, 200.3]
