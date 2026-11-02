"""Numerical and boundary checks, run with python test_main.py."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np
spec = importlib.util.spec_from_file_location("project", Path(__file__).with_name("main.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class ProjectTests(unittest.TestCase):

    def test_convergence_and_saturation(self):
        _, y, u = m.simulate()
        self.assertLess(abs(y[-1]-1), .01)
        self.assertLessEqual(abs(u).max(), 2)
    def test_unreachable_setpoint_remains_bounded(self):
        _, y, u = m.simulate(target=10, limit=1)
        self.assertLessEqual(y.max(),1)
        self.assertTrue(np.isfinite(y).all())
    def test_zero_gains(self):
        _, y, _ = m.simulate(kp=0,ki=0,kd=0)
        np.testing.assert_array_equal(y,0)
    def test_invalid(self):
        with self.assertRaises(ValueError): m.simulate(dt=1)

if __name__ == "__main__":
    unittest.main(verbosity=2)
