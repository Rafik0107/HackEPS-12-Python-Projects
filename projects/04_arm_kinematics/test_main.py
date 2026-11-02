"""Numerical and boundary checks, run with python test_main.py."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np
spec = importlib.util.spec_from_file_location("project", Path(__file__).with_name("main.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class ProjectTests(unittest.TestCase):

    def test_inverse_roundtrip(self):
        for angles in np.random.default_rng(42).uniform(-3,3,(30,2)):
            target=m.forward(*angles)
            for solution in m.inverse(*target):
                np.testing.assert_allclose(m.forward(*solution),target,atol=1e-10)
    def test_jacobian_finite_difference(self):
        q=np.array([.4,.7]); eps=1e-6
        numerical=np.column_stack([(m.forward(*(q+np.eye(2)[i]*eps))-m.forward(*(q-np.eye(2)[i]*eps)))/(2*eps) for i in range(2)])
        np.testing.assert_allclose(m.jacobian(*q),numerical,atol=1e-8)
    def test_singular_and_unreachable(self):
        np.testing.assert_allclose(m.forward(*m.inverse(0,0)[0]),[0,0],atol=1e-12)
        with self.assertRaises(ValueError): m.inverse(3,0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
