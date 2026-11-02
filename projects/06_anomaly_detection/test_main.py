"""Numerical and boundary checks, run with python test_main.py."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np
spec = importlib.util.spec_from_file_location("project", Path(__file__).with_name("main.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class ProjectTests(unittest.TestCase):

    def test_outliers_and_no_training_leakage(self):
        d=m.RobustDetector().fit([[-1,0],[0,1],[1,-1],[0,0],[.5,.5]])
        before=d.center.copy()
        self.assertEqual(d.predict([[0,0],[100,100]]).tolist(),[False,True])
        np.testing.assert_array_equal(d.center,before)
    def test_constant_feature(self):
        d=m.RobustDetector().fit([[2],[2],[2]])
        self.assertEqual(d.predict([[2],[3]]).tolist(),[False,True])
    def test_invalid(self):
        with self.assertRaises(ValueError): m.RobustDetector().score([[1]])
        with self.assertRaises(ValueError): m.RobustDetector().fit([[1],[2],[3]]).score([[1,2]])

if __name__ == "__main__":
    unittest.main(verbosity=2)
