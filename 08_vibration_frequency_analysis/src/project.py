"""Project 08 — Mechanical vibration frequency analysis.

A vibration analyser for rotating machinery: synthetic signals, FFT spectrum,
dominant-frequency estimation, RMS, and a simple digital filter. Reads and
writes CSV results.

Core: Python + NumPy. Matplotlib is optional.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

import numpy as np

try:  # pragma: no cover - user environment
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    _HAVE_MPL = True
except ImportError:  # pragma: no cover
    _HAVE_MPL = False

DEFAULT_SAMPLING_RATE = 100.0  # Hz
DEFAULT_FREQUENCY = 5.0  # Hz


def simulate_signal(
    frequency: float = DEFAULT_FREQUENCY,
    sampling_rate: float = DEFAULT_SAMPLING_RATE,
    duration: float = 5.0,
    noise: float = 0.05,
    amplitude: float = 1.0,
) -> np.ndarray:
    """Generate a sinusoidal vibration signal with optional noise."""
    t = np.arange(int(sampling_rate * duration)) / sampling_rate
    signal = amplitude * np.sin(2.0 * np.pi * frequency * t)
    return signal + noise * np.random.default_rng(11).normal(0.0, 1.0, len(t))


def spectrum(samples: np.ndarray, sampling_rate: float) -> Tuple[np.ndarray, np.ndarray]:
    """Return (frequencies, magnitudes) of the one-sided FFT of ``samples``."""
    samples = np.asarray(samples, dtype=float)
    n = len(samples)
    if n < 2:
        raise ValueError("need at least two samples")
    if sampling_rate <= 0:
        raise ValueError("sampling_rate must be positive")
    fft = np.fft.rfft(samples)
    mag = np.abs(fft) / n
    freq = np.fft.rfftfreq(n, d=1.0 / sampling_rate)
    return freq, mag


def dominant_frequency(samples: np.ndarray, sampling_rate: float) -> float:
    """Return the strongest frequency present in ``samples`` (Hz)."""
    freq, mag = spectrum(samples, sampling_rate)
    return float(freq[int(np.argmax(mag))])


def rms(samples: np.ndarray) -> float:
    """Return the RMS value of ``samples``."""
    samples = np.asarray(samples, dtype=float)
    if samples.size == 0:
        return 0.0
    return float(np.sqrt(np.mean(samples ** 2)))


def lowpass_filter(
    samples: np.ndarray,
    sampling_rate: float,
    cutoff: float,
    order: int = 2,
) -> np.ndarray:
    """Simple moving-average low-pass filter (no external dependencies)."""
    samples = np.asarray(samples, dtype=float)
    window = int(round(sampling_rate / (2.0 * cutoff)))
    if window < 3:
        window = 3
    window = min(window, len(samples) - 1)
    if window % 2 == 0:
        window += 1
    kernel = np.ones(window) / window
    conv = np.convolve(samples, kernel, mode="same")
    return conv[window // 2 : len(conv) - window // 2]


def read_csv(path: str) -> np.ndarray:
    """Read a numeric CSV file (one column) and return a 1-D array."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"missing CSV file: {path}")
    data = np.genfromtxt(path, delimiter=",", dtype=float)
    data = np.asarray(data, dtype=float)
    if data.ndim == 1:
        return data
    return data[:, 0] if data.shape[1] >= 1 else data.ravel()


def write_csv(path: str, samples: np.ndarray) -> str:
    """Write ``samples`` to a CSV file, one value per line."""
    Path(path).write_text(
        "\n".join(f"{v:.6f}" for v in samples),
        encoding="ascii",
    )
    return path


def demo() -> Dict:
    """Analyse a normal and an abnormal vibration signal."""
    normal = simulate_signal(frequency=DEFAULT_FREQUENCY, noise=0.05)
    abnormal = simulate_signal(frequency=DEFAULT_FREQUENCY * 3, noise=0.15)
    filtered = lowpass_filter(abnormal, DEFAULT_SAMPLING_RATE, cutoff=7.0)
    f_normal, m_normal = spectrum(normal, DEFAULT_SAMPLING_RATE)
    f_abnormal, m_abnormal = spectrum(abnormal, DEFAULT_SAMPLING_RATE)

    if _HAVE_MPL:
        fig, axes = plt.subplots(2, 1, figsize=(7, 6))
        axes[0].plot(f_normal, m_normal, label="normal")
        axes[0].plot(f_abnormal, m_abnormal, label="abnormal")
        axes[0].set_title("Spectrum fréquentielle")
        axes[0].legend()
        axes[1].plot(normal, label="normal (brut)")
        axes[1].plot(filtered, label="abnormal (filtre)", alpha=0.7)
        axes[1].set_title("Signaux (theoreme de Parseval)")
        axes[1].legend()
        plt.tight_layout()
        fig.savefig("08_vibration_analysis.png", dpi=110)

    return {
        "sampling_rate": DEFAULT_SAMPLING_RATE,
        "frequencies": {
            "dominant_normal": round(dominant_frequency(normal, DEFAULT_SAMPLING_RATE), 3),
            "dominant_abnormal": round(dominant_frequency(abnormal, DEFAULT_SAMPLING_RATE), 3),
        },
        "rms": {
            "normal": round(rms(normal), 4),
            "abnormal": round(rms(abnormal), 4),
        },
        "normalised": {"normal": round(float(np.std(normal)), 4), "abnormal": round(float(np.std(abnormal)), 4)},
        "plot": "08_vibration_analysis.png",
    }
