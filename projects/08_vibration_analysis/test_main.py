"""Numerical and boundary checks, run with python test_main.py."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np
spec = importlib.util.spec_from_file_location("project", Path(__file__).with_name("main.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class ProjectTests(unittest.TestCase):

    def test_undamped_analytic_solution(self):
        t,state,energy=m.simulate(damping=0,duration=2)
        np.testing.assert_allclose(state[:,0],np.cos(10*t),atol=2e-6)
        self.assertLess(np.ptp(energy)/energy[0],1e-6)
    def test_damping_and_frequency(self):
        t,state,energy=m.simulate()
        self.assertLess(energy[-1],energy[0])
        self.assertTrue(np.all(np.diff(energy)<=1e-8))
        self.assertLess(abs(m.dominant_frequency(state[:,0],.005)-10/(2*np.pi)),.11)
    def test_invalid(self):
        with self.assertRaises(ValueError): m.simulate(mass=0)
        with self.assertRaises(ValueError): m.dominant_frequency(np.ones(10),.1)

if __name__ == "__main__":
    unittest.main(verbosity=2)
