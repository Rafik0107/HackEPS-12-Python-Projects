"""Numerical and boundary checks, run with python test_main.py."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np
spec = importlib.util.spec_from_file_location("project", Path(__file__).with_name("main.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class ProjectTests(unittest.TestCase):

    def test_known_clusters_and_descent(self):
        x=np.array([[-10,-10],[-10,-9],[-9,-10],[10,10],[10,9],[9,10]])
        labels,centers,history=m.kmeans(x,k=2)
        self.assertEqual(len(set(labels[:3])),1)
        self.assertEqual(len(set(labels[3:])),1)
        self.assertNotEqual(labels[0],labels[-1])
        self.assertTrue(np.all(np.diff(history)<=1e-10))
    def test_reproducible_and_k_one(self):
        x=np.random.default_rng(4).normal(size=(30,2))
        np.testing.assert_array_equal(m.kmeans(x)[0],m.kmeans(x)[0])
        np.testing.assert_allclose(m.kmeans(x,k=1)[1][0],x.mean(axis=0))
    def test_invalid(self):
        with self.assertRaises(ValueError): m.kmeans([[1],[1]],k=2)

if __name__ == "__main__":
    unittest.main(verbosity=2)
