"""Numerical and boundary checks, run with python test_main.py."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np
spec = importlib.util.spec_from_file_location("project", Path(__file__).with_name("main.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class ProjectTests(unittest.TestCase):

    def test_stationary_roll(self):
        angle=.4
        acc=np.tile([0,np.sin(angle),np.cos(angle)],(100,1))
        np.testing.assert_allclose(m.fuse(np.zeros(100),acc),angle,atol=1e-12)
    def test_bias_reduction(self):
        result=m.demo()
        self.assertLess(result['fused_rmse_rad'],result['gyro_rmse_rad']/3)
    def test_wrap_boundary(self):
        angles=np.linspace(3,3.3,100)
        acc=np.column_stack([np.zeros(100),np.sin(angles),np.cos(angles)])
        fused=m.fuse(np.full(100,(angles[1]-angles[0])/.01),acc)
        np.testing.assert_allclose(m.wrap(fused-angles),0,atol=1e-10)
    def test_invalid(self):
        with self.assertRaises(ValueError): m.fuse([0],[[0,0,0]])

if __name__ == "__main__":
    unittest.main(verbosity=2)
