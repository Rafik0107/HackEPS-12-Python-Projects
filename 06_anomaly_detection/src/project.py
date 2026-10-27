"""Project 06 — Industrial anomaly detection.

Multivariate sensor monitoring (temperature, vibration, pressure, current) with
data cleaning, normalisation and two detectors: a robust median/MAD baseline
and an Isolation Forest (optional scikit-learn). Includes a simple dashboard.

The core detectors work with NumPy only.
"""

from __future__ import annotations

from typing import Dict, List

import numpy as np

try:  # pragma: no cover - user environment
    from sklearn.ensemble import IsolationForest
    _HAVE_SKLEARN = True
except Exception:  # pragma: no cover
    _HAVE_SKLEARN = False

try:  # pragma: no cover - user environment
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    _HAVE_MPL = True
except ImportError:  # pragma: no cover
    _HAVE_MPL = False

METRICS = ["temperature", "vibration", "pressure", "current"]


def clean_data(values: np.ndarray) -> np.ndarray:
    """Remove NaN/inf and clip extreme outliers past the 1st/99th percentile."""
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    if values.size == 0:
        return values
    lo, hi = np.percentile(values, [1, 99])
    return np.clip(values, lo, hi)


def normalise(values: np.ndarray) -> np.ndarray:
    """Min-max normalisation to [0, 1]."""
    values = clean_data(values)
    lo, hi = values.min(), values.max()
    if hi == lo:
        return np.zeros_like(values)
    return (values - lo) / (hi - lo)


def detect_anomalies(values: np.ndarray, threshold: float = 3.5) -> np.ndarray:
    """Baseline detector: robust median/MAD z-score. Returns anomaly indices."""
    values = clean_data(values)
    if values.size < 5:
        return np.array([], dtype=int)
    centre = np.median(values)
    mad = np.median(np.abs(values - centre))
    if mad == 0:
        return np.where(values != centre)[0]
    z = 0.6745 * np.abs(values - centre) / mad
    return np.where(z > threshold)[0]


def detect_anomalies_isolation(
    data: np.ndarray, contamination: float = 0.05
) -> np.ndarray:
    """Isolation Forest detector (sklearn required). Returns anomaly indices."""
    if not _HAVE_SKLEARN:
        return np.array([], dtype=int)
    model = IsolationForest(contamination=contamination, random_state=7)
    model.fit(data)
    labels = model.predict(data)
    return np.where(labels == -1)[0]


def generate_sensor_data(
    n_points: int = 500, *, seed: int = 3
) -> Dict[str, np.ndarray]:
    """Synthetic sensor readings with a few injected anomalies."""
    rng = np.random.default_rng(seed)
    base = {
        "temperature": rng.normal(22.0, 0.6, n_points),
        "vibration": rng.normal(0.4, 0.08, n_points),
        "pressure": rng.normal(1.0, 0.05, n_points),
        "current": rng.normal(3.2, 0.15, n_points),
    }
    # inject anomalies
    base["temperature"][10] = 45.0
    base["vibration"][50] = 1.8
    base["pressure"][80] = 2.5
    base["current"][120] = 5.5
    return base


def demo() -> Dict:
    data = generate_sensor_data()
    cleaned = {m: clean_data(data[m]) for m in METRICS}
    normalised = {m: normalise(cleaned[m]) for m in METRICS}
    anomalies = {
        m: {
            "baseline": detect_anomalies(cleaned[m]).tolist(),
            "isolation": detect_anomalies_isolation(cleaned[m][:, None]).tolist(),
        }
        for m in METRICS
    }
    if _HAVE_MPL:
        fig, axes = plt.subplots(2, 2, figsize=(9, 6))
        for ax, metric in zip(axes.ravel(), METRICS):
            ax.plot(cleaned[metric], label="nettoyé", lw=1)
            ax.scatter(
                np.where(np.array(anomalies[metric]["baseline"]))[
                    0
                ],
                cleaned[metric][np.array(anomalies[metric]["baseline"])],
                color="#FF3355",
                label="anomalie",
                zorder=3,
            )
            ax.set_title(metric)
            ax.legend()
        plt.tight_layout()
        fig.savefig("06_anomaly_detection.png", dpi=110)

    return {
        "n_points": int(sum(len(v) for v in cleaned.values())),
        "metrics": METRICS,
        "anomalies": anomalies,
        "missing_labels_eval": {
            "note": "Precision/recall/F1 need ground-truth labels, which are not "
                    "present in this synthetic benchmark."
        },
        "plot": "06_anomaly_detection.png",
    }
