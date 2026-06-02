import numpy as np
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt

def tau_kk_force_kernel(r, tau=1.0, n_images=7):
    """Pure KK image sum over compact S¹."""
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
    """Pure KK pairwise force."""
    N = len(positions)
    forces = np.zeros_like(positions)
    for i in range(N):
        for j in range(i + 1, N):
            dr = positions[i] - positions[j]
            r = np.linalg.norm(dr)
            if r < 1e-8: continue
            f_mag = G * masses[i] * masses[j] * tau_kk_force_kernel(np.array([r]), tau)[0]
            f_vec = f_mag * (dr / r)
            forces[i] += f_vec
            forces[j] -= f_vec
    return forces

def extract_tau_resonances(trajectories, total_time=50.0):
    """Pure FFT detection for 142857 family."""
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
        
        best_match, best_diff = None, 1.0
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
    forces = tau_world_pairwise_force(positions, masses, tau=tau)
    velocities_half = velocities + 0.5 * forces * dt
    new_positions = positions + velocities_half * dt
    new_forces = tau_world_pairwise_force(new_positions, masses, tau=tau)
    new_velocities = velocities_half + 0.5 * new_forces * dt
    return new_positions, new_velocities

def make_coherent_initial_conditions(n_particles, radius=0.8, omega=0.4):
    """Rotating disk-like distribution."""
    angles = np.linspace(0, 2*np.pi, n_particles, endpoint=False)
    r = radius * (0.6 + 0.4 * np.random.rand(n_particles))
    positions = np.stack([r * np.cos(angles), r * np.sin(angles)], axis=1)
    velocities = np.stack([-omega * r * np.sin(angles), omega * r * np.cos(angles)], axis=1)
    velocities += np.random.randn(n_particles, 2) * 0.08
    return positions, velocities

# ====================== v0.10 FULL RUN ======================
if __name__ == "__main__":
    print("Tau World Patch v0.10 — FULL (Coherent ICs + Long Run + Spectrum)")
    print("Tau Framework — 5D Kaluza-Klein on R² × S¹ with Tav topology\n")

    np.random.seed(42)
    n_particles = 10
    positions, velocities = make_coherent_initial_conditions(n_particles, radius=0.7, omega=0.35)
    masses = np.ones(n_particles)

    print("Using coherent rotating initial conditions (disk + net angular velocity).")

    dt = 0.006
    n_steps = 16384
    total_time = dt * n_steps
    print(f"n_steps={n_steps} | total_time≈{total_time:.1f} | This will take several minutes.\n")

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
        for p, data in resonances.items():
            print(f"  {p}: mode={data['dominant_mode']:.5f} (target {data['closest_target']:.4f} ±{data['deviation']:.4f}) | tau_est={data['tau_estimate']:.3f}")
    else:
        print("No strong 142857-family peaks at this length even with coherent ICs.")

    # Power spectrum
    plt.figure(figsize=(10, 6))
    avg_power = np.zeros_like(np.abs(fft(traj[0, :, 0])))
    for i in range(n_particles):
        avg_power += np.abs(fft(traj[i, :, 0]))
    avg_power /= n_particles
    N = len(avg_power)
    freqs = fftfreq(N, dt)
    
    plt.semilogy(freqs[:N//2], avg_power[:N//2], label='Average Power Spectrum', color='#00ff9f', linewidth=1.2)
    plt.axvline(1/7, color='red', linestyle='--', alpha=0.7, label='1/7 target')
    plt.axvline(2/7, color='orange', linestyle='--', alpha=0.6, label='2/7')
    plt.axvline(3/7, color='yellow', linestyle='--', alpha=0.5, label='3/7')
    plt.xlabel('Frequency')
    plt.ylabel('Power (log)')
    plt.title('Tau Universe KK Dynamics — Power Spectrum (Pure, Rotating ICs, Long Run)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('tau_kk_power_spectrum_v0.10.png', dpi=150)
    print("\nPower spectrum saved: tau_kk_power_spectrum_v0.10.png")

    np.save('tau_trajectory_v0.10.npy', traj)
    print("Trajectory saved: tau_trajectory_v0.10.npy")

    print("\nDone. Pure KK + coherent ICs + long integration. The geometry had every chance.")
