"""Tests for project 06 (industrial anomaly detection)."""

import unittest
import numpy as np

from src.project import (
    clean_data,
    demo,
    detect_anomalies,
    detect_anomalies_isolation,
    generate_sensor_data,
    normalise,
)


class TestCleaning(unittest.TestCase):
    def test_clean_removes_nonfinite(self):
        values = np.array([1.0, 2.0, np.nan, 3.0, np.inf])
        out = clean_data(values)
        self.assertEqual(len(out), 3)
        self.assertTrue(np.isfinite(out).all())

    def test_clean_clips_extremes(self):
        values = np.array([0.0, 1.0, 2.0, 100.0])
        out = clean_data(values)
        self.assertLessEqual(out.max(), np.percentile(values, 99))


class TestNormalise(unittest.TestCase):
    def test_min_max(self):
        values = np.array([0.0, 10.0, 20.0])
        out = normalise(values)
        self.assertAlmostEqual(out.min(), 0.0)
        self.assertAlmostEqual(out.max(), 1.0)
        self.assertAlmostEqual(out.mean(), 0.5, places=2)


class TestDetection(unittest.TestCase):
    def test_know_chunk(self):
        data = np.array([10, 11, 9, 10, 12, 10, 9, 60, 11, 10, 8])
        idx = detect_anomalies(data)
        self.assertEqual(int(idx[0]), 7)

    def test_empty(self):
        self.assertEqual(len(detect_anomalies(np.array([]))), 0)

    def test_isolation_runs(self):
        data = generate_sensor_data()["temperature"][:, None]
        idx = detect_anomalies_isolation(data)
        self.assertEqual(len(idx), 0)


class TestDemo(unittest.TestCase):
    def test_demo_runs(self):
        result = demo()
        self.assertIn("n_points", result)
        self.assertIn("metrics", result)
        self.assertIsInstance(result["anomalies"], dict)


if __name__ == "__main__":
    unittest.main()
