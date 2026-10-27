"""Project 10 — IMU sensor fusion.

Fuses a gyroscope (angular rate) and an accelerometer (tilt) with a simple
complementary filter to estimate device orientation. Estimates drift over
time and visualises the angular error.

Core: Python + NumPy (matplotlib optional).
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

DT = 0.01  # seconds per sample


def complementary_filter(
    gyro_rates: np.ndarray,
    accel_angles: np.ndarray,
    *,
    dt: float = DT,
    alpha: float = 0.98,
    initial: float = 0.0,
) -> np.ndarray:
    """Estimate orientation from gyroscope rates + accelerometer references.

    ``alpha`` close to 1 trusts the gyroscope more; low values trust the
    accelerometer. ``accel_angles`` must be the same length as ``gyro_rates``.
    """
    gyro_rates = np.asarray(gyro_rates, dtype=float)
    accel_angles = np.asarray(accel_angles, dtype=float)
    if dt <= 0 or not (0.0 <= alpha <= 1.0):
        raise ValueError("invalid dt or alpha")
    if gyro_rates.size != accel_angles.size:
        raise ValueError("gyro_rates and accel_angles must have the same length")
    if gyro_rates.size == 0:
        return np.array([])

    angle = float(initial)
    out = np.empty(gyro_rates.size, dtype=float)
    for i, (rate, measured) in enumerate(zip(gyro_rates, accel_angles)):
        angle = alpha * (angle + rate * dt) + (1.0 - alpha) * measured
        out[i] = angle
    return out


def simulate_imu(
    *,
    duration: float = 10.0,
    samples_per_second: int = 100,
    true_rate: float = 2.0,
    accelerometer_drift: float = 0.0,
) -> Dict[str, np.ndarray]:
    """Synthetic IMU data: gyroscope rates and accelerometer-measured angles."""
    n = int(duration * samples_per_second)
    t = np.arange(n) * DT
    gyro = true_rate * np.ones(n)
    true_angle = true_rate * t
    accel_angle = true_angle + accelerometer_drift * np.sin(0.5 * t)
    return {
        "time": t,
        "gyro_rates": gyro,
        "true_angle": true_angle,
        "accel_measured": accel_angle,
    }


def error(angle_estimate: np.ndarray, true_angle: np.ndarray) -> np.ndarray:
    """Signed angular error (estimate minus truth), unwrapped."""
    return np.unwrap(np.asarray(angle_estimate) - np.asarray(true_angle))


def demo() -> Dict:
    """Fuse IMU signals and report the orientation estimate and drift."""
    data = simulate_imu(duration=10.0, accelerometer_drift=0.05)
    fused = complementary_filter(
        data["gyro_rates"], data["accel_measured"], alpha=0.98
    )
    err = error(fused, data["true_angle"])

    if _HAVE_MPL:
        fig, axes = plt.subplots(2, 1, figsize=(7, 6))
        axes[0].plot(data["time"], data["true_angle"], label="vraie", lw=2)
        axes[0].plot(data["time"], fused, label="fusion", ls="--")
        axes[0].set_title("Orientation estimee")
        axes[0].legend()
        axes[1].plot(data["time"], err, lw=2)
        axes[1].set_title("Erreur angulaire (drift apparent)")
        plt.tight_layout()
        fig.savefig("10_imu_fusion.png", dpi=110)

    return {
        "parameters": {
            "dt": DT,
            "alpha": 0.98,
            "accelerometer_drift": data["accel_measured"].std() * 10.0,
        },
        "errors": {
            "final": round(float(err[-1]), 4),
            "max": round(float(np.max(np.abs(err))), 4),
        },
        "fused_last": round(float(fused[-1]), 4),
        "plot": "10_imu_fusion.png",
    }
