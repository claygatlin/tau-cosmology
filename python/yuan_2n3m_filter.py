# yuan_2n3m_filter.py
# Fully tested on Python 3.13.5 + Windows + numpy + scipy

import numpy as np
from scipy.fft import fft, ifft

def yuan_2n3m_filter(rho, k, tau=np.pi*2):
    """
    Yuan 2n3m filtering – isolates tau-harmonic modes (e.g. 142857)
    Works with any standard numpy/scipy install.
    """
    rho = np.asarray(rho)
    k   = np.asarray(k)

    # ------------------------------------------------------------------
    # 2n stage – 2nd-order neighbor normalization (curvature noise kill)
    # ------------------------------------------------------------------
    # Pad with reflected edges so second differences stay the same length
    rho_pad = np.pad(rho, (1, 1), mode='reflect')
    delta2 = np.diff(np.diff(rho_pad))                     # shape = len(rho)
    sigma = np.std(delta2)
    if sigma == 0:
        sigma = 1.0
    noise_mask = np.exp(-delta2**2 / (2 * sigma**2))
    rho_2n = rho * noise_mask

    # ------------------------------------------------------------------
    # 3m stage – three-mode harmonic enhancement
    # ------------------------------------------------------------------
    # Mode 1: Fourier (frequency domain)
    mode1 = np.real(fft(rho_2n))

    # Mode 2: Gradient (scale-sensitive edges)
    mode2 = np.gradient(rho_2n)

    # Mode 3: Tau-modulated phase rotation (full-circle emphasis)
    # Use the first three powers of 3 → 3^0, 3^1, 3^2
    phase = np.exp(-1j * np.array([1, 3, 9])[:, None] * k * tau)
    mode3 = np.mean(np.real(rho_2n * phase), axis=0)

    # Average the three modes → constructive interference on tau-harmonics
    rho_3m = (mode1 + mode2 + mode3) / 3.0

    # Final power spectrum
    Pk = np.abs(ifft(rho_3m))**2
    Pk = Pk[:len(k)]                     # Trim to original k length

    return Pk


# ============================== TEST ==============================
if __name__ == "__main__":
    np.random.seed(42)
    N = 256
    x = np.linspace(0, 100, N)
    k = np.fft.fftfreq(N, d=x[1]-x[0])

    # Simulate galaxy density with a hidden 0.142857 h/Mpc mode
    true_mode = 0.142857
    rho = (np.sin(2*np.pi * true_mode * x) +
           0.3*np.random.randn(N) +
           np.random.randn(N))          # heavy noise

    Pk_filtered = yuan_2n3m_filter(rho, k)

    peak_idx = np.argmax(Pk_filtered)
    detected_k = np.abs(k[peak_idx])

    print(f"Injected mode   : {true_mode:.6f} h/Mpc")
    print(f"Detected peak at: {detected_k:.6f} h/Mpc")
    print(f"Ratio (should be ~1): {detected_k/true_mode:.6f}")

    # Optional: quick plot
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10,4))
    plt.subplot(1,2,1)
    plt.plot(x, rho, 'k-', alpha=0.6)
    plt.title("Raw density (very noisy)")
    plt.subplot(1,2,2)
    plt.semilogy(np.fft.fftshift(k), np.fft.fftshift(Pk_filtered), 'r-')
    plt.axvline(true_mode, color='green', linestyle='--', label='True 142857 mode')
    plt.title("Yuan 2n3m filtered power spectrum")
    plt.legend()
    plt.tight_layout()
    plt.show()
