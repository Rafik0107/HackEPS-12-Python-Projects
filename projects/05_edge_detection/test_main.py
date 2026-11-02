"""Numerical and boundary checks, run with python test_main.py."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np
spec = importlib.util.spec_from_file_location("project", Path(__file__).with_name("main.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class ProjectTests(unittest.TestCase):

    def test_constant_has_no_edges(self):
        magnitude, edges=m.sobel(np.ones((10,10)))
        self.assertFalse(edges.any())
        self.assertEqual(magnitude.max(),0)
    def test_vertical_step(self):
        image=np.zeros((10,10)); image[:,5:]=1
        _,edges=m.sobel(image)
        self.assertTrue(edges[:,4:6].all())
        self.assertFalse(edges[:,:4].any())
        self.assertFalse(edges[:,6:].any())
    def test_transpose_symmetry(self):
        image=np.random.default_rng(4).random((7,9))
        np.testing.assert_allclose(m.sobel(image)[0].T,m.sobel(image.T)[0])
    def test_invalid(self):
        with self.assertRaises(ValueError): m.sobel([[np.nan]*3]*3)

if __name__ == "__main__":
    unittest.main(verbosity=2)
