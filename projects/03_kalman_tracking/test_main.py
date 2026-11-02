"""Numerical and boundary checks, run with python test_main.py."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np
spec = importlib.util.spec_from_file_location("project", Path(__file__).with_name("main.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class ProjectTests(unittest.TestCase):

    def test_improves_noisy_measurements(self):
        result = m.demo()
        self.assertLess(result['filtered_rmse'],result['measurement_rmse'])
    def test_velocity_and_covariance(self):
        x, p = m.track(np.arange(80)*2., acceleration_variance=0, measurement_variance=.01)
        self.assertAlmostEqual(x[-1,1],2.,places=4)
        self.assertTrue(np.all(np.linalg.eigvalsh(p) >= -1e-10))
        np.testing.assert_allclose(p,p.transpose(0,2,1),atol=1e-10)
    def test_missing(self):
        x, p = m.track([0,1,np.nan,np.nan,4])
        self.assertTrue(np.isfinite(x).all())
        self.assertGreater(p[3,0,0],p[1,0,0])
    def test_invalid(self):
        with self.assertRaises(ValueError): m.track([1],measurement_variance=0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
