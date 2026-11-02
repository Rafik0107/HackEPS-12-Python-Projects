"""Tests for project 10 (IMU sensor fusion)."""

import unittest
import numpy as np

from src.project import (
    complementary_filter,
    demo,
    error,
    simulate_imu,
)


class TestComplementaryFilter(unittest.TestCase):
    def test_fused_angle_reflects_gyro(self):
        gyro = np.array([1.0, 1.0, 1.0])
        accel = np.array([0.0, 0.0, 0.0])
        fused = complementary_filter(gyro, accel, dt=0.1, alpha=1.0)
        self.assertGreater(fused[-1], 0.0)
        self.assertEqual(len(fused), 3)

    def test_alpha_constrained(self):
        with self.assertRaises(ValueError):
            complementary_filter(np.array([1.0]), np.array([0.0]), alpha=1.5)

    def test_length_mismatch(self):
        with self.assertRaises(ValueError):
            complementary_filter(np.array([1.0]), np.array([0.0, 0.0]))


class TestSimulate(unittest.TestCase):
    def test_imu_shape(self):
        data = simulate_imu(duration=1.0, samples_per_second=10)
        self.assertEqual(data["gyro_rates"].shape, (10,))

    def test_true_angle_ramp(self):
        data = simulate_imu(duration=2.0, samples_per_second=10, true_rate=3.0)
        self.assertAlmostEqual(data["true_angle"][-1], 0.57, places=2)


class TestError(unittest.TestCase):
    def test_error_zero_when_fused_matches(self):
        estimate = np.array([0.0, 0.1, 0.2])
        truth = np.array([0.0, 0.1, 0.2])
        self.assertTrue(np.allclose(error(estimate, truth), 0.0))


class TestDemo(unittest.TestCase):
    def test_demo_runs(self):
        result = demo()
        self.assertIn("errors", result)
        self.assertGreaterEqual(result["errors"]["max"], 0.0)
        self.assertIn("plot", result)


if __name__ == "__main__":
    unittest.main()
