"""Tests for project 02 (advanced PID temperature-controller simulator)."""

import unittest

from src.project import PID, demo, simulate


class TestPID(unittest.TestCase):
    def setUp(self):
        self.ctrl = PID(kp=1.0, ki=0.1, kd=0.05, target=60.0)

    def test_step_returns_limits(self):
        self.ctrl.integral = 500.0  # force a large output
        self.assertGreaterEqual(self.ctrl.step(20.0, 1.0), 0.0)
        self.assertLessEqual(self.ctrl.step(20.0, 1.0), 100.0)

    def test_invalid_dt_raises(self):
        with self.assertRaises(ValueError):
            self.ctrl.step(20.0, 0.0)

    def test_derivative_until_first_step(self):
        self.assertIsNone(self.ctrl.previous_error)
        self.ctrl.step(20.0, 1.0)
        self.assertIsNotNone(self.ctrl.previous_error)

    def test_anti_windup_blocks_integral_growth(self):
        ctrl = PID(kp=1.0, ki=10.0, kd=0.0, target=0.0, limits=(0.0, 0.0))
        ctrl.step(100.0, 0.1)
        self.assertLessEqual(ctrl.integral, 0.0)


class TestSimulation(unittest.TestCase):
    def test_output_shapes_match(self):
        ctrl = PID(kp=1.0, ki=0.1, kd=0.0, target=60.0)
        plant = lambda u: 0.35 * u + 20.0
        result = simulate(plant, ctrl, steps=50, dt=0.1)
        self.assertEqual(len(result["time"]), 50)
        self.assertEqual(len(result["measurement"]), 50)
        self.assertEqual(len(result["command"]), 50)
        self.assertEqual(result["set_point"], 60.0)

    def test_simulation_non_negative(self):
        ctrl = PID(kp=1.0, ki=0.0, kd=0.0, target=60.0)
        plant = lambda u: 20.0
        result = simulate(plant, ctrl, steps=10)
        self.assertTrue(all(m >= 0 for m in result["measurement"]))


class TestDemo(unittest.TestCase):
    def test_demo_returns_rich_result(self):
        result = demo()
        self.assertGreater(result["set_point"], 0)
        self.assertIn("pid_final", result)
        self.assertIn("simulations", result)
        self.assertEqual(sorted(result["simulations"].keys()), ["P", "PI", "PID"])
        for values in result["simulations"].values():
            self.assertIn("last_measurements", values)

    def test_demo_writes_a_plot(self):
        saved = demo()
        self.assertTrue(saved["pid_final"]["measurement_last"] > 0)


if __name__ == "__main__":
    unittest.main()
