"""Tests for project 07 (clustering laboratory)."""

import unittest
import numpy as np

from src.project import (
    dbscan,
    compare,
    elbow_curve,
    generate_dataset,
    kmeans,
    silhouette_score,
)


class TestKMeans(unittest.TestCase):
    def test_clusters(self):
        data = generate_dataset("blobs", n_samples=300)
        res = kmeans(data, k=3)
        self.assertEqual(int(np.unique(res["labels"]).size), 3)
        self.assertGreater(res["inertia"], 0.0)

    def test_lloyd_converges(self):
        data = generate_dataset("blobs", n_samples=100)
        first = kmeans(data, k=3, max_iter=1)
        second = kmeans(data, k=3, max_iter=10)
        self.assertEqual(len(first["labels"]), len(second["labels"]))


class TestDBSCAN(unittest.TestCase):
    def test_noise_mode(self):
        data = np.array([[0.0, 0.0], [0.1, 0.1], [100.0, 100.0], [100.1, 100.1]])
        res = dbscan(data, radius=0.5, min_pts=2)
        self.assertEqual(res["n_clusters"], 2)


class TestSilhouette(unittest.TestCase):
    def test_perfect(self):
        data = np.array([[0.0, 0.0], [0.1, 0.0], [10.0, 10.0], [10.1, 10.0]])
        labels = np.array([0, 0, 1, 1])
        self.assertGreater(silhouette_score(data, labels), 0.8)


class TestElbow(unittest.TestCase):
    def test_returns_curve(self):
        data = generate_dataset("blobs", n_samples=100)
        curve = elbow_curve(data, k_range=range(2, 5))
        self.assertEqual(len(curve["k"]), 3)
        self.assertEqual(len(curve["inertia"]), 3)


class TestCompare(unittest.TestCase):
    def test_compare_runs(self):
        data = generate_dataset("blobs", n_samples=200)
        res = compare(data, kmeans_k=3)
        self.assertGreater(res["kmeans"]["silhouette"], 0.1)
        self.assertIn("dbscan", res)


class TestGenerateDataset(unittest.TestCase):
    def test_blobs(self):
        data = generate_dataset("blobs", n_samples=50)
        self.assertEqual(data.shape, (50, 2))


if __name__ == "__main__":
    unittest.main()
