"""Tests for project 04 (two-link robotic arm kinematics)."""

import unittest

import numpy as np

from src.project import (
    demo,
    forward_kinematics,
    inverse_kinematics,
    is_reachable,
    trajectory,
    workspace,
)


class TestForwardKinematics(unittest.TestCase):
    def test_zero_angles_returns_endpoint(self):
        x, y = forward_kinematics(l1=2.0, l2=1.0, theta1=0.0, theta2=0.0)
        self.assertAlmostEqual(x, 3.0, places=6)
        self.assertAlmostEqual(y, 0.0, places=6)

    def test_round_trip(self):
        t1, t2 = 0.7, 1.2
        x, y = forward_kinematics(l1=2.0, l2=1.0, theta1=t1, theta2=t2)
        t1r, t2r = inverse_kinematics(l1=2.0, l2=1.0, x=x, y=y, elbow_up=True)
        xr, yr = forward_kinematics(l1=2.0, l2=1.0, theta1=t1r, theta2=t2r)
        self.assertAlmostEqual(xr, x, places=5)
        self.assertAlmostEqual(yr, y, places=5)


class TestInverseKinematics(unittest.TestCase):
    def test_unreachable_raises(self):
        with self.assertRaises(ValueError):
            inverse_kinematics(l1=2.0, l2=1.0, x=6.0, y=6.0)

    def test_reachable_after_clamp(self):
        t1, t2 = inverse_kinematics(l1=2.0, l2=1.0, x=2.0, y=2.0, elbow_up=False)
        self.assertTrue(np.isfinite(t1) and np.isfinite(t2))


class TestReachability(unittest.TestCase):
    def test_inside_workspace(self):
        self.assertTrue(is_reachable(x=2.0, y=2.0))

    def test_outside_workspace(self):
        self.assertFalse(is_reachable(x=5.0, y=5.0))


class TestWorkspace(unittest.TestCase):
    def test_ranges(self):
        lo, hi = workspace()
        self.assertAlmostEqual(lo, 1.0, places=6)
        self.assertAlmostEqual(hi, 3.0, places=6)


class TestTrajectory(unittest.TestCase):
    def test_length(self):
        pts = trajectory(steps=10)
        self.assertEqual(len(pts), 10)

    def test_consistent_dimensions(self):
        with self.assertRaises(ValueError):
            trajectory(theta1=np.linspace(0, 1, 3), theta2=np.linspace(0, 1, 5))


class TestDemo(unittest.TestCase):
    def test_demo_runs(self):
        result = demo()
        self.assertIn("forward", result)
        self.assertIn("inverse", result)
        self.assertGreaterEqual(result["workspace"][1], 0.0)


if __name__ == "__main__":
    unittest.main()
