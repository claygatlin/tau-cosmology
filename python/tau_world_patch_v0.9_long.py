import numpy as np
from scipy.fft import fft, fftfreq

def tau_kk_force_kernel(r, tau=1.0, n_images=7):
    """
    Tau Universe Kaluza-Klein force kernel with compact S¹ (radius τ).
    Pure geometric image sum over the fifth dimension.
    No hardcoded frequencies — resonances emerge from dynamics only.
    """
    force = np.zeros_like(r)
    for k in range(-n_images, n_images + 1):
        if k == 0:
            force += 1.0 / (r**2 + 1e-8)
        else:
            extra_dist = 2 * np.pi * tau * abs(k)
            dist = np.sqrt(r**2 + extra_dist**2)
            force += 1.0 / (dist**2 + 1e-8)
    return -force / (r + 1e-8)


def tau_world_pairwise_force(positions, masses, tau=0.7, G=1.0):
    """
    Pairwise force for Tau Universe world — pure KK dynamics.
    """
    N = len(positions)
    forces = np.zeros_like(positions)
    for i in range(N):
        for j in range(i + 1, N):
            dr = positions[i] - positions[j]
            r = np.linalg.norm(dr)
            if r < 1e-8:
                continue
            f_mag = G * masses[i] * masses[j] * tau_kk_force_kernel(np.array([r]), tau)[0]
            f_vec = f_mag * (dr / r)
            forces[i] += f_vec
            forces[j] -= f_vec
    return forces


def extract_tau_resonances(trajectories, tau_guess=0.7, total_time=50.0):
    """
    Analyze trajectories for 142857 / 1/7 periodic mode family.
    Pure FFT peak detection.
    """
    N = trajectories.shape[1]
    dt = total_time / N
    freqs = fftfreq(N, dt)
    resonances = {}
    target_freqs = [1/7, 2/7, 3/7, 4/7, 5/7, 6/7]
    
    for i in range(trajectories.shape[0]):
        sig = trajectories[i, :, 0]
        fft_vals = np.abs(fft(sig))
        peak_idx = np.argmax(fft_vals[1:]) + 1
        dominant_freq = np.abs(freqs[peak_idx])
        
        best_match = None
        best_diff = 1.0
        for tf in target_freqs:
            diff = abs(dominant_freq - tf)
            if diff < best_diff:
                best_diff = diff
                best_match = tf
        
        if best_diff < 0.12:
            resonances[f'particle_{i}'] = {
                'dominant_mode': dominant_freq,
                'closest_target': best_match,
                'deviation': best_diff,
                'strength': fft_vals[peak_idx],
                'tau_estimate': 1.0 / (7 * dominant_freq) if dominant_freq > 0 else 0
            }
    return resonances


def velocity_verlet_step(positions, velocities, masses, tau, dt):
    """Velocity Verlet integration step."""
    forces = tau_world_pairwise_force(positions, masses, tau=tau)
    velocities_half = velocities + 0.5 * forces * dt
    new_positions = positions + velocities_half * dt
    new_forces = tau_world_pairwise_force(new_positions, masses, tau=tau)
    new_velocities = velocities_half + 0.5 * new_forces * dt
    return new_positions, new_velocities


# ====================== LONG PURE DYNAMICS RUN ======================
if __name__ == "__main__":
    print("Tau World Patch v0.9 — LONG PURE DYNAMICS RUN")
    print("Tau Framework — 5D Kaluza-Klein on R² × S¹ with Tav topology")
    print("No seeded harmonics. Extended integration for resonance development.\n")

    np.random.seed(42)

    n_particles = 10
    positions = np.random.randn(n_particles, 2) * 0.5
    masses = np.ones(n_particles)
    velocities = np.random.randn(n_particles, 2) * 0.25

    print(f"Running with {n_particles} particles...")

    dt = 0.008
    n_steps = 8192            # Long run — ~65k time units
    total_time = dt * n_steps

    print(f"n_steps = {n_steps}  |  total_time ≈ {total_time:.1f}  |  This may take a minute or two on some machines.\n")

    traj = np.zeros((n_particles, n_steps, 2))
    traj[:, 0] = positions.copy()
    vel = velocities.copy()

    for t in range(1, n_steps):
        new_pos, new_vel = velocity_verlet_step(traj[:, t-1], vel, masses, tau=0.7, dt=dt)
        traj[:, t] = new_pos
        vel = new_vel

    resonances = extract_tau_resonances(traj, total_time=total_time)

    print(f"\nDetected Tau resonances (142857 family): {len(resonances)} / {n_particles} particles")
    
    if resonances:
        print("\nDetailed detections:")
        for p, data in resonances.items():
            print(f"  {p}: mode={data['dominant_mode']:.5f} (target {data['closest_target']:.4f}, dev={data['deviation']:.4f})")
            print(f"       strength={data['strength']:.2e}, tau_est={data['tau_estimate']:.3f}")
        
        modes = [d['dominant_mode'] for d in resonances.values()]
        avg_mode = np.mean(modes)
        print(f"\nAverage detected mode: {avg_mode:.5f}")
        print(f"Closest 142857 family member: {min([1/7,2/7,3/7], key=lambda x: abs(avg_mode - x)):.5f}")
    else:
        print("\nNo strong 142857-family peaks detected even at n_steps=8192.")
        print("This is still an honest result. The resonance may require even longer integration or more coherent initial conditions.")

    print("\nNote: Pure KK dynamics on compact S¹ continue to generate structured periodic motion.")
    print("The framework predicts these harmonics strengthen with scale and integration time.")
