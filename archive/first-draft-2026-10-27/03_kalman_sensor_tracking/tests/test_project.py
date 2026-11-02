"""Tests for project 03 (Kalman sensor tracking)."""

import unittest
from pathlib import Path

import numpy as np

from src.project import (
    kalman_filter_1d,
    rmse,
    simulate_target,
    uncertainty_band,
    demo,
)


class TestKalmanFilter(unittest.TestCase):
    def test_returns_position_and_velocity(self):
        t = np.linspace(0, 20, 200)
        measurements = 3.0 * t + 2.0
        position, velocity = kalman_filter_1d(measurements)
        self.assertEqual(len(position), len(measurements))
        self.assertEqual(len(velocity), len(measurements))

    def test_estimate_close_to_true(self):
        true = np.linspace(0, 20, 200)
        measurements = true + 0.1
        position, _ = kalman_filter_1d(measurements)
        self.assertLess(rmse(true, position), 0.5)

    def test_estimate_tracks_noise(self):
        measurements = np.linspace(0, 20, 100) + np.random.default_rng(1).normal(0, 1, 100)
        position, _ = kalman_filter_1d(measurements)
        self.assertLess(rmse(np.linspace(0, 20, 100), position), 1.0)

    def test_empty_returns_empty(self):
        position, velocity = kalman_filter_1d(np.array([]))
        self.assertEqual(len(position), 0)
        self.assertEqual(len(velocity), 0)


class TestUtilities(unittest.TestCase):
    def test_rmse(self):
        a = np.array([0.0, 2.0, 4.0])
        b = np.array([0.0, 2.0, 4.0])
        self.assertEqual(rmse(a, b), 0.0)

    def test_uncertainty_band(self):
        m = np.linspace(0, 10, 10)
        band = uncertainty_band(m)
        self.assertEqual(len(band), len(m))
        self.assertTrue(np.all(band >= 0))


class TestDemo(unittest.TestCase):
    def test_demo_runs(self):
        result = demo()
        self.assertIsInstance(result, dict)
        self.assertIn("rmse", result)
        self.assertGreaterEqual(result["rmse"]["position"], 0.0)

    def test_demo_creates_output(self):
        result = demo()
        self.assertIn("final", result)
        self.assertIn("position", result["final"])


if __name__ == "__main__":
    unittest.main()
