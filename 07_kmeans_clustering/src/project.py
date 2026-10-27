"""Project 07 — Machine learning clustering laboratory.

K-Means and DBSCAN clustering on synthetic datasets, with the elbow method,
silhouette scoring and a visual comparison of both algorithms.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np

try:  # pragma: no cover - user environment
    import matplotlib.pyplot as plt
    _HAVE_MPL = True
except ImportError:  # pragma: no cover
    _HAVE_MPL = False

VALID_DISTRIBUTIONS = ("blobs", "moons", "aniso")


def generate_dataset(
    distribution: str = "blobs", n_samples: int = 300, *, seed: int = 7
) -> np.ndarray:
    """Generate a synthetic 2-D dataset."""
    rng = np.random.default_rng(seed)
    n = int(n_samples)
    if distribution == "blobs":
        centers = np.array([[0.0, 0.0], [5.0, 5.0], [10.0, 0.0]])
        labels = rng.integers(0, 3, n)
        data = rng.normal(0.0, 0.7, (n, 2))
        for i, lab in enumerate(labels):
            data[i] += centers[lab]
        return data
    if distribution == "moons":
        center1 = np.array([5.0, 5.0])
        center2 = np.array([10.0, 1.0])
        half = n // 2
        a1 = rng.standard_normal((half, 2)) * 0.5
        a1[:, 1] += 2.0
        a2 = rng.standard_normal((n - half, 2)) * 0.5
        a2[:, 1] -= 2.0
        return np.vstack([a1, a2]) + np.array([center1, center2])[None, :]
    if distribution == "aniso":
        mean = np.array([5.0, 5.0])
        cov = np.array([[1.0, 0.9], [0.9, 1.0]])
        return rng.multivariate_normal(mean, cov, size=n)
    raise ValueError(f"unknown distribution {distribution!r}; choose {VALID_DISTRIBUTIONS}")


def normalise(data: np.ndarray) -> np.ndarray:
    """Min-max normalise each feature to [0, 1]."""
    data = np.asarray(data, dtype=float)
    lo, hi = data.min(axis=0), data.max(axis=0)
    return (data - lo) / (hi - lo)


def kmeans(
    data: np.ndarray, k: int, *, seed: int = 7, max_iter: int = 100
) -> Dict[str, np.ndarray]:
    """K-Means (Lloyd's algorithm). Returns centroids, labels and inertia."""
    pts = normalise(np.asarray(data, dtype=float))
    rng = np.random.default_rng(seed)
    centers = pts[rng.permutation(pts.shape[0])[:k]]
    labels = np.zeros(pts.shape[0], dtype=int)
    inertia = 0.0
    for _ in range(max_iter):
        distances = np.linalg.norm(pts[:, None, :] - centers[None, :, :], axis=2)
        new_labels = np.argmin(distances, axis=1)
        new_centers = np.array([pts[labels == j].mean(axis=0) if (labels == j).any() else centers[j] for j in range(k)])
        if np.all(new_labels == labels):
            labels, centers = new_labels, new_centers
            break
        labels, centers = new_labels, new_centers
    inertia = float(np.sum((pts - centers[labels]) ** 2))
    return {"labels": labels, "centers": centers, "inertia": inertia}


def dbscan(
    data: np.ndarray, radius: float = 0.3, min_pts: int = 5
) -> Dict[str, np.ndarray]:
    """Density-based clustering (DBSCAN)."""
    pts = normalise(np.asarray(data, dtype=float))
    n = pts.shape[0]
    labels = np.full(n, -1, dtype=int)
    cluster = 0
    for i in range(n):
        if labels[i] != -1:
            continue
        neighbours = np.linalg.norm(pts - pts[i], axis=1) <= radius
        if neighbours.sum() < min_pts:
            labels[i] = -1  # noise
            continue
        labels[i] = cluster
        stack = [i]
        while stack:
            cur = stack.pop()
            for j in np.where(np.linalg.norm(pts - pts[cur], axis=1) <= radius)[0]:
                if labels[j] == -1:
                    labels[j] = cluster
                    stack.append(j)
        cluster += 1
    return {"labels": labels, "n_clusters": cluster}


def silhouette_score(
    data: np.ndarray, labels: np.ndarray
) -> float:
    """Silhouette coefficient (single-pass O(n^2))."""
    pts = np.asarray(data, dtype=float)
    lab = np.asarray(labels, dtype=int)
    n = pts.shape[0]
    if n < 2 or len(np.unique(lab)) < 2:
        return 0.0
    a = np.zeros(n)
    b = np.zeros(n)
    for i in range(n):
        same = pts[lab == lab[i]]
        a[i] = float(np.mean(np.linalg.norm(same - pts[i], axis=1)))
        others = pts[lab != lab[i]]
        b[i] = float(np.min(np.linalg.norm(others - pts[i], axis=1)))
    return float(np.mean((b - a) / np.maximum(a, b)))


def elbow_curve(
    data: np.ndarray, k_range: range = range(1, 11)
) -> Dict[str, np.ndarray]:
    """Inertia for each k, used to find the elbow."""
    data = normalise(np.asarray(data, dtype=float))
    inertias = np.array([kmeans(data, k)["inertia"] for k in k_range])
    return {"k": np.array(k_range, dtype=float), "inertia": inertias}


def compare(data: np.ndarray, kmeans_k: int = 3) -> Dict:
    """Run both algorithms and visualise the result."""
    kmeans_res = kmeans(data, kmeans_k)
    dbscan_res = dbscan(data, radius=0.4, min_pts=8)
    if _HAVE_MPL:
        fig, axes = plt.subplots(1, 2, figsize=(9, 4))
        axes[0].scatter(data[:, 0], data[:, 1], c=kmeans_res["labels"],
                        cmap="tab10", s=8)
        axes[0].set_title("K-Means (k=%d)" % kmeans_k)
        axes[1].scatter(data[:, 0], data[:, 1], c=dbscan_res["labels"],
                        cmap="tab10", s=8)
        axes[1].set_title("DBSCAN")
        plt.tight_layout()
        fig.savefig("07_clustering_laboratory.png", dpi=110)

    return {
        "kmeans": {
            "n_clusters": int(kmeans_res["centroids"].shape[0]) if False else int(np.unique(kmeans_res["labels"]).size),
            "inertia": round(kmeans_res["inertia"], 4),
            "silhouette": round(silhouette_score(data, kmeans_res["labels"]), 4),
        },
        "dbscan": {
            "n_clusters": int(np.unique(dbscan_res["labels"]).size) - (1 if -1 in dbscan_res["labels"] else 0),
            "silhouette": round(silhouette_score(data, dbscan_res["labels"]), 4),
            "n_noise": int((dbscan_res["labels"] == 0).sum()),
        },
        "dataset": "blobs -> blob-like clusters",
    }
