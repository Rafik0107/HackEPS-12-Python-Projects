"""Project 11 — Biomedical ECG signal analysis.

An educational ECG analyser: synthetic ECG generation, filtering, R-peak
detection, RR-interval statistics and estimated heart rate. It is explicitly
educational and never intended as a medical diagnostic device.

Core: Python + NumPy. matplotlib optional.
"""

from __future__ import annotations

from typing import Dict

import numpy as np

try:  # pragma: no cover - user environment
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    _HAVE_MPL = True
except ImportError:  # pragma: no cover
    _HAVE_MPL = False

REFERATORY_PERIOD = 0.2  # seconds


def _moving_average(signal: np.ndarray, window: int) -> np.ndarray:
    """Smooth a signal with a simple moving average."""
    kernel = np.ones(window) / window
    return np.convolve(signal, kernel, mode="same")


def generate_ecg(
    *,
    heart_rate: float = 75.0,
    sampling_rate: float = 1000.0,
    duration: float = 10.0,
    noise: float = 0.05,
) -> np.ndarray:
    """Generate a synthetic ECG with P-QRS-T waves.

    Produces a realistic-looking signal whose R-peaks are approximately
    ``heart_rate`` beats per minute, making it ideal for exercising
    peak-detection code.
    """
    n = int(sampling_rate * duration)
    t = np.arange(n) / sampling_rate
    ecg = np.zeros(n)
    rr = 60.0 / heart_rate
    n_beats = int(duration / rr)
    for i in range(n_beats):
        peak_idx = int(i * rr * sampling_rate)
        if peak_idx >= n:
            break
        # R spike
        r_half = int(0.02 * sampling_rate)
        ecg[peak_idx] += 1.0
        # T wave
        t_half = int(0.30 * sampling_rate)
        for j in range(1, t_half + 1):
            if peak_idx + j < n:
                ecg[peak_idx + j] += 0.35 * np.exp(-((j - 0.12 * sampling_rate) / 0.08) ** 2)
        # P wave a bit before the R
        p_half = int(0.12 * sampling_rate)
        for j in range(1, p_half + 1):
            if peak_idx - j >= 0:
                ecg[peak_idx - j] += 0.15 * np.exp(-((j - 0.06 * sampling_rate) / 0.04) ** 2)
    ecg += noise * np.random.default_rng(5).normal(0.0, 1.0, n)
    return ecg


def filter_noise(signal: np.ndarray, sampling_rate: float, window: int = 21) -> np.ndarray:
    """Smooth a noisy ECG with a short moving average (educational)."""
    window = int(window)
    if window < 3:
        raise ValueError("window must be >= 3")
    return _moving_average(signal, window)


def detect_r_peaks(
    signal: np.ndarray, sampling_rate: float, threshold_percentile: float = 90.0
) -> np.ndarray:
    """Detect R-peaks as local maxima above a noise threshold.

    A refractory period prevents double-counted peaks.
    """
    signal = np.asarray(signal, dtype=float)
    if signal.size < 3:
        return np.array([], dtype=int)
    threshold = np.percentile(signal, threshold_percentile)
    candidates = np.where(signal > threshold)[0]
    if candidates.size == 0:
        return np.array([], dtype=int)
    peaks = []
    last = -REFERATORY_PERIOD * sampling_rate
    for idx in candidates:
        if idx - last >= REFERATORY_PERIOD * sampling_rate:
            peaks.append(int(idx))
            last = int(idx)
    return np.array(peaks, dtype=int)


def rr_intervals(peaks: np.ndarray, sampling_rate: float) -> np.ndarray:
    """Return the RR intervals (seconds) between consecutive peaks."""
    if peaks.size < 2:
        return np.array([])
    return np.diff(peaks) / sampling_rate


def heart_rate_from_rr(rr_seconds: np.ndarray) -> float:
    """Estimate heart rate (bpm) from RR intervals."""
    rr = np.asarray(rr_seconds, dtype=float)
    if rr.size == 0:
        return 0.0
    return float(60.0 / np.mean(rr))


def demo() -> Dict:
    """Run a full ECG analysis pipeline and export a figure."""
    ecg = generate_ecg(heart_rate=75.0, sampling_rate=1000.0, duration=10.0, noise=0.3)
    cleaned = filter_noise(ecg, sampling_rate=1000.0, window=21)
    peaks = detect_r_peaks(cleaned, sampling_rate=1000.0)
    rr = rr_intervals(peaks, sampling_rate=1000.0)
    hr = heart_rate_from_rr(rr)

    if _HAVE_MPL:
        fig, axes = plt.subplots(2, 1, figsize=(8, 5))
        axes[0].plot(ecg, label="brut (bruit)", lw=0.5, alpha=0.6)
        axes[0].plot(cleaned, label="filtre", lw=1)
        axes[0].set_title("Signal ECG brut vs filtre")
        axes[0].legend()
        axes[1].plot(cleaned, label="filtre", lw=1)
        axes[1].scatter(
            peaks,
            cleaned[peaks],
            color="#FF3355",
            s=12,
            label="pics R detectes",
        )
        axes[1].set_title("Détection des pics R")
        axes[1].legend()
        plt.tight_layout()
        fig.savefig("11_ecg_analysis.png", dpi=110)

    return {
        "signal": {
            "n_points": int(ecg.size),
            "noise_std": round(float(np.std(ecg)), 4),
        },
        "peaks": {
            "n_detected": int(peaks.size),
            "rr_mean_seconds": round(float(np.mean(rr)), 4) if rr.size else 0.0,
            "heart_rate_bpm": round(hr, 2),
        },
        "n_expected_beats": int(75.0 / 60.0 * 10.0),
        "educational": "Outil pédagogique — aucun diagnostic médical.",
        "plot": "11_ecg_analysis.png",
    }
