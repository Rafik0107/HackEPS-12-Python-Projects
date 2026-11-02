"""Deterministic-seed k-means with k-means++ initialization."""
import json
import numpy as np


def kmeans(samples, k=3, seed=42, max_iter=200, tol=1e-6):
    x = np.asarray(samples, dtype=float)
    if x.ndim != 2 or min(x.shape) == 0 or not np.isfinite(x).all():
        raise ValueError("finite sample-by-feature matrix required")
    if not isinstance(k, int) or not 1 <= k <= len(np.unique(x, axis=0)):
        raise ValueError("k must not exceed the number of distinct samples")
    if not isinstance(max_iter, int) or max_iter < 1 or not np.isfinite(tol) or tol < 0:
        raise ValueError("invalid stopping criteria")
    rng = np.random.default_rng(seed)
    centers = [x[rng.integers(len(x))].copy()]
    while len(centers) < k:
        d = ((x[:, None]-np.array(centers))**2).sum(axis=2).min(axis=1)
        centers.append(x[rng.choice(len(x), p=d/d.sum())].copy())
    centers = np.array(centers)
    history = []
    for _ in range(max_iter):
        distances = ((x[:, None]-centers)**2).sum(axis=2)
        labels = distances.argmin(axis=1)
        updated = centers.copy()
        for j in range(k):
            if np.any(labels == j):
                updated[j] = x[labels == j].mean(axis=0)
        inertia = float(((x[:, None]-updated)**2).sum(axis=2).min(axis=1).sum())
        history.append(inertia)
        shift = np.linalg.norm(updated-centers)
        centers = updated
        if shift <= tol:
            break
    distances = ((x[:, None]-centers)**2).sum(axis=2)
    return distances.argmin(axis=1), centers, history


def demo():
    rng = np.random.default_rng(42)
    x = np.vstack([rng.normal(c, .3, size=(50, 2)) for c in [[-3, -3], [0, 3], [3, -2]]])
    labels, centers, history = kmeans(x)
    return {"centers": centers.tolist(), "counts": np.bincount(labels).tolist(),
            "inertia": history[-1], "iterations": len(history)}

if __name__ == '__main__':
    print(json.dumps(demo(), indent=2))
