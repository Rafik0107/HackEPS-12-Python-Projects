"""Project 03 — Kalman sensor tracking.

One-dimensional tracking of a moving target from noisy position measurements.
The state is (position, velocity) and the filter fuses a deterministic
trajectory with Gaussian noise.

Features:
- synthetic trajectory and noisy measurements
- Kalman prediction / update
- position and velocity estimates
- RMSE and confidence ribbon
"""

from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np

try:  # pragma: no cover - user environment
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    _HAVE_MPL = True
except ImportError:  # pragma: no cover
    _HAVE_MPL = False

DT = 0.05  # seconds between samples


def simulate_target(
    steps: int = 400,
    *,
    velocity: float = 2.0,
    start: float = 0.0,
    measurement_noise: float = 0.5,
) -> Dict[str, np.ndarray]:
    """Generate a straight-line trajectory and a noisy measurement of position."""
    t = np.arange(steps) * DT
    true_position = start + velocity * t
    noise = np.random.default_rng(7).normal(0.0, measurement_noise, steps)
    measured_position = true_position + noise
    return {
        "time": t,
        "true_position": true_position,
        "true_velocity": velocity * np.ones(steps),
        "measured_position": measured_position,
    }


def kalman_filter_1d(
    measurements: np.ndarray,
    *,
    dt: float = DT,
    process_variance: float = 0.01,
    measurement_variance: float = 0.5,
    initial_position: float = 0.0,
    initial_velocity: float = 2.0,
) -> Tuple[np.ndarray, np.ndarray]:
    """Run a 2-state (position, velocity) Kalman filter on position samples.

    Returns the filtered position and velocity arrays.
    """
    n = len(measurements)
    if n == 0:
        return np.array([]), np.array([])
    F = np.array([[1.0, dt], [0.0, 1.0]])
    Q = np.array([[process_variance, 0.0], [0.0, process_variance / dt]])
    R = measurement_variance  # measurement variance (scalar)
    P = np.eye(2) * 1.0

    position = np.zeros(n)
    velocity = np.zeros(n)
    state = np.array([initial_position, initial_velocity], dtype=float)

    for i in range(n):
        position[i] = state[0]
        velocity[i] = state[1]
        # Predict
        state = F @ state
        P = F @ P @ F.T + Q
        # Update
        innovation = measurements[i] - state[0]
        S = P[0, 0] + R
        K = np.array([P[0, 0], P[1, 0]], dtype=float) / S
        state = state + K * innovation
        P = (np.eye(2) - np.outer(K, np.array([1.0, 0.0]))) @ P

    return position, velocity


def rmse(a: np.ndarray, b: np.ndarray) -> float:
    """Root-mean-square error between two arrays."""
    return float(np.sqrt(np.mean((np.asarray(a) - np.asarray(b)) ** 2)))


def uncertainty_band(
    measurements: np.ndarray,
    *,
    dt: float = DT,
    process_variance: float = 0.01,
    measurement_variance: float = 0.5,
) -> np.ndarray:
    """Return a 1-sigma position uncertainty per sample (after the update)."""
    n = len(measurements)
    if n == 0:
        return np.array([])
    state = np.array([measurements[0], 0.0], dtype=float)
    P = np.eye(2) * 1.0
    F = np.array([[1.0, dt], [0.0, 1.0]])
    Q = np.array([[process_variance, 0.0], [0.0, process_variance / dt]])
    R = np.array([[measurement_variance]])
    band = np.zeros(n)

    for i in range(n):
        P = F @ P @ F.T + Q
        innovation = measurements[i] - state[0]
        S = P[0, 0] + R[0, 0]
        K = np.array([(P[0, 0] / S), (P[1, 0] / S)], dtype=float)
        state = state + K * innovation
        P = (np.eye(2) - np.outer(K, np.array([1.0, 0.0]))) @ P
        band[i] = P[0, 0]
    return band


def demo() -> Dict:
    """Track the target and write the position/velocity estimates."""
    data = simulate_target(steps=400)
    filtered_position, filtered_velocity = kalman_filter_1d(
        data["measured_position"]
    )
    position_rmse = rmse(data["true_position"], filtered_position)
    velocity_rmse = rmse(data["true_velocity"], filtered_velocity)

    if _HAVE_MPL:
        fig, axes = plt.subplots(2, 1, figsize=(7, 6))
        axes[0].plot(data["time"], data["true_position"], label="vraie",
                     color="#2e9e5b", lw=2)
        axes[0].plot(data["time"], data["measured_position"], ls=":",
                     color="#c0c0c0", label="bruitée")
        axes[0].plot(data["time"], filtered_position, ls="--",
                     color="#b03a2e", label="estimée")
        axes[0].set_title("Position: filtre de Kalman")
        axes[0].legend()
        axes[0].grid(alpha=0.3)
        uncertainty = uncertainty_band(data["measured_position"])
        axes[1].plot(data["time"], data["true_velocity"], color="#2e9e5b",
                     lw=2, label="vraie")
        axes[1].plot(data["time"], filtered_velocity, ls="--",
                     color="#b03a2e", label="estimée")
        axes[1].fill_between(
            data["time"],
            filtered_velocity - 2 * np.sqrt(uncertainty),
            filtered_velocity + 2 * np.sqrt(uncertainty),
            color="#b03a2e", alpha=0.2, label="bande 2-sigma",
        )
        axes[1].set_title("Vitesse estimée (bande de confiance 2-sigma)")
        axes[1].legend()
        axes[1].grid(alpha=0.3)
        plt.tight_layout()
        fig.savefig("03_kalman_tracking.png", dpi=110)

    return {
        "measurements": {
            "n": int(data["measured_position"].size),
            "noise_std": float(np.std(data["measured_position"]
                                      - data["true_position"])),
        },
        "rmse": {
            "position": round(position_rmse, 4),
            "velocity": round(velocity_rmse, 4),
        },
        "final": {
            "position": round(float(filtered_position[-1]), 4),
            "velocity": round(float(filtered_velocity[-1]), 4),
        },
    }
