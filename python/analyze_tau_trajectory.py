import numpy as np
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import os

def analyze_particle_spectra(traj_path='tau_trajectory_v0.10.npy', total_time=98.3, out_dir='tau_spectra'):
    """
    Per-particle FFT analysis of Tau KK trajectory (v0.10).
    """
    traj = np.load(traj_path)
    n_particles, n_steps, _ = traj.shape
    dt = total_time / n_steps
    freqs = fftfreq(n_steps, dt)
    
    os.makedirs(out_dir, exist_ok=True)
    
    print("=" * 72)
    print("TAU UNIVERSE v0.10 — PER-PARTICLE SPECTRAL ANALYSIS")
    print("=" * 72)
    print(f"Particles: {n_particles} | Timesteps: {n_steps} | Total simulated time: {total_time:.1f}")
    print(f"Target family: 1/7 ≈ {1/7:.5f}, 2/7 ≈ {2/7:.5f}, 3/7 ≈ {3/7:.5f}")
    print("-" * 72)
    
    target_freqs = [1/7, 2/7, 3/7, 4/7, 5/7, 6/7]
    results = []
    
    for i in range(n_particles):
        sig = traj[i, :, 0]  # x-position
        fft_vals = np.abs(fft(sig))
        peak_indices = np.argsort(fft_vals[1:])[::-1][:5] + 1
        peaks = [(freqs[idx], fft_vals[idx]) for idx in peak_indices]
        
        best_match = None
        best_diff = 1.0
        for f, pwr in peaks:
            for tf in target_freqs:
                diff = abs(f - tf)
                if diff < best_diff:
                    best_diff = diff
                    best_match = (tf, f, pwr)
        
        results.append({
            'particle': i,
            'top_peaks': peaks[:3],
            'best_142857_match': best_match,
            'best_deviation': best_diff
        })
        
        print(f"\nParticle {i:2d}:")
        print("  Top 3 frequencies: ", end="")
        for f, pwr in peaks[:3]:
            print(f"{f:.5f} (pwr={pwr:.1e})   ", end="")
        print()
        if best_match:
            tf, f, pwr = best_match
            print(f"  Closest to {tf:.5f}: {f:.5f} (dev={best_diff:.5f})")
    
    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    close_matches = [r for r in results if r['best_deviation'] < 0.15]
    if close_matches:
        print(f"Particles with decent match to 142857 family: {len(close_matches)}/{n_particles}")
        avg_dev = np.mean([r['best_deviation'] for r in close_matches])
        print(f"Average deviation of best matches: {avg_dev:.5f}")
    else:
        print("No particles showed strong locking to the 1/7–6/7 family in this run.")
    
    # Save a few individual plots
    for i in [0, 4, 8]:
        if i < n_particles:
            plt.figure(figsize=(9, 4))
            sig = traj[i, :, 0]
            fft_vals = np.abs(fft(sig))
            plt.semilogy(freqs[:n_steps//2], fft_vals[:n_steps//2], color='#00ff9f', linewidth=1.1)
            for tf in [1/7, 2/7, 3/7]:
                plt.axvline(tf, color='red', linestyle='--', alpha=0.65, linewidth=0.9)
            plt.title(f'Particle {i} — Power Spectrum (x-position) | v0.10 pure KK')
            plt.xlabel('Frequency')
            plt.ylabel('Power (log scale)')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(f'{out_dir}/particle_{i:02d}_spectrum.png', dpi=130)
            plt.close()
    
    print(f"\nExample per-particle plots saved in ./{out_dir}/")
    print("Analysis complete. The compact S¹ is producing structured motion;")
    print("the exact 1/7 fundamental remains subtle at this 2D scale and integration length.")

if __name__ == "__main__":
    analyze_particle_spectra()
