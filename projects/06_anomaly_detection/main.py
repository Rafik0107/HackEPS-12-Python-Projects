"""Robust independent-feature anomaly scoring using median and MAD."""
import json
import numpy as np


def matrix(x):
    x = np.asarray(x, dtype=float)
    if x.ndim != 2 or min(x.shape) == 0 or not np.isfinite(x).all():
        raise ValueError("nonempty finite sample-by-feature matrix required")
    return x


class RobustDetector:
    def __init__(self, threshold=3.5):
        if not np.isfinite(threshold) or threshold <= 0:
            raise ValueError("threshold must be positive")
        self.threshold = threshold
        self.center = self.scale = None

    def fit(self, normal_data):
        x = matrix(normal_data)
        if len(x) < 3:
            raise ValueError("at least three normal training samples required")
        self.center = np.median(x, axis=0)
        mad = 1.4826*np.median(abs(x-self.center), axis=0)
        self.scale = np.maximum(mad, 1e-9)
        return self

    def score(self, samples):
        if self.center is None:
            raise ValueError("fit before scoring")
        x = matrix(samples)
        if x.shape[1] != len(self.center):
            raise ValueError("feature count differs from training data")
        return np.max(abs(x-self.center)/self.scale, axis=1)

    def predict(self, samples):
        return self.score(samples) > self.threshold


def demo():
    rng = np.random.default_rng(42)
    detector = RobustDetector().fit(rng.normal(size=(500, 3)))
    test = np.vstack([rng.normal(size=(100, 3)), np.full((10, 3), 8.)])
    flagged = detector.predict(test)
    return {"true_positives": int(flagged[100:].sum()), "false_positives": int(flagged[:100].sum()),
            "anomalies": 10, "normal_samples": 100}

if __name__ == '__main__':
    print(json.dumps(demo(), indent=2))
