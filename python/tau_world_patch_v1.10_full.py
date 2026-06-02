import numpy as np
from scipy.fft import fft, ifft, fftfreq
import matplotlib.pyplot as plt
import os

# ====================== YUAN 2n3m FILTER (your original) ======================
def yuan_2n3m_filter(rho, k, tau=np.pi*2):
    rho = np.asarray(rho)
    k   = np.asarray(k)

    # 2n stage – curvature noise suppression
    rho_pad = np.pad(rho, (1, 1), mode='reflect')
    delta2 = np.diff(np.diff(rho_pad))
    sigma = np.std(delta2) if np.std(delta2) > 0 else 1.0
    noise_mask = np.exp(-delta2**2 / (2 * sigma**2))
    rho_2n = rho * noise_mask

    # 3m stage – three-mode harmonic enhancement
    mode1 = np.real(fft(rho_2n))
    mode2 = np.gradient(rho_2n)
    phase = np.exp(-1j * np.array([1, 3, 9])[:, None] * k * tau)
    mode3 = np.mean(np.real(rho_2n * phase), axis=0)

    rho_3m = (mode1 + mode2 + mode3) / 3.0
    Pk = np.abs(ifft(rho_3m))**2
    Pk = Pk[:len(k)]

    return Pk

# ====================== ANALYSIS ======================
def analyze_with_yuan_filter(traj_path='tau_trajectory_v0.10.npy', total_time=98.3, out_dir='tau_yuan_filtered'):
    traj = np.load(traj_path)
    n_particles, n_steps, _ = traj.shape
    dt = total_time / n_steps
    freqs = fftfreq(n_steps, dt)

    os.makedirs(out_dir, exist_ok=True)

    print("=" * 75)
    print("TAU v0.10 TRAJECTORY — YUAN 2n3m FILTERED ANALYSIS")
    print("=" * 75)
    print(f"Particles: {n_particles} | Timesteps: {n_steps} | Total time: {total_time:.1f}")
    print("Applying Yuan 2n3m filter per-particle on x-position time series...\n")

    target = 1/7
    results = []

    for i in range(n_particles):
        sig = traj[i, :, 0]
        k = freqs.copy()

        # Raw spectrum
        raw_fft = np.abs(fft(sig))
        raw_peak_idx = np.argmax(raw_fft[1:]) + 1
        raw_freq = np.abs(freqs[raw_peak_idx])

        # Filtered spectrum
        Pk_filtered = yuan_2n3m_filter(sig, k)
        filt_peak_idx = np.argmax(Pk_filtered[1:]) + 1
        filt_freq = np.abs(freqs[filt_peak_idx])

        dev_raw = abs(raw_freq - target)
        dev_filt = abs(filt_freq - target)

        results.append({
            'particle': i,
            'raw_freq': raw_freq,
            'filt_freq': filt_freq,
            'dev_raw': dev_raw,
            'dev_filt': dev_filt,
            'improvement': dev_raw - dev_filt
        })

        print(f"Particle {i:2d}: raw={raw_freq:.5f} (dev={dev_raw:.5f}) | "
              f"filtered={filt_freq:.5f} (dev={dev_filt:.5f}) | "
              f"{'better' if dev_filt < dev_raw else 'worse'}")

        # Save individual filtered spectrum plot
        plt.figure(figsize=(9, 4))
        plt.semilogy(freqs[:n_steps//2], Pk_filtered[:n_steps//2], color='#00ff9f', linewidth=1.1)
        plt.axvline(target, color='red', linestyle='--', alpha=0.7, label='1/7 target')
        plt.axvline(2/7, color='orange', linestyle='--', alpha=0.5)
        plt.axvline(3/7, color='yellow', linestyle='--', alpha=0.4)
        plt.title(f'Particle {i} — Yuan 2n3m Filtered Spectrum | v0.10 pure KK')
        plt.xlabel('Frequency')
        plt.ylabel('Power (log)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{out_dir}/particle_{i:02d}_yuan_filtered.png', dpi=130)
        plt.close()

    # Summary
    improvements = [r['improvement'] for r in results]
    avg_improvement = np.mean(improvements)
    better_count = sum(1 for r in results if r['dev_filt'] < r['dev_raw'])

    print("\n" + "=" * 75)
    print("YUAN 2n3m FILTER EFFECT SUMMARY")
    print("=" * 75)
    print(f"Particles with improved closeness to 1/7 after filtering: {better_count}/{n_particles}")
    print(f"Average improvement in deviation: {avg_improvement:.5f}")
    print(f"\nFiltered spectra saved in ./{out_dir}/")
    print("Analysis complete. Compare these plots to the raw ones from v0.10.")

if __name__ == "__main__":
    analyze_with_yuan_filter()
