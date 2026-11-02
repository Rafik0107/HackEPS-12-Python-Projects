"""Numerical and boundary checks, run with python test_main.py."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np
spec = importlib.util.spec_from_file_location("project", Path(__file__).with_name("main.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class ProjectTests(unittest.TestCase):

    def test_exact_against_permutations(self):
        from itertools import permutations
        depot=(0,0); picks=[(1,2),(3,3),(4,0),(0,4)]
        result=m.optimize(np.zeros((5,5)),depot,picks)
        best=min(sum(abs(a[0]-b[0])+abs(a[1]-b[1]) for a,b in zip([depot]+list(p),list(p)+[depot])) for p in permutations(picks))
        self.assertEqual(result['distance'],best)
        self.assertEqual(len(result['path'])-1,best)
    def test_obstacles_and_path(self):
        grid=np.zeros((5,5)); grid[:4,2]=1
        r=m.optimize(grid,(0,0),[(0,4),(3,3)])
        self.assertEqual(r['path'][0],r['path'][-1])
        self.assertTrue(all(grid[p]==0 for p in r['path']))
        for a,b in zip(r['path'],r['path'][1:]):
            self.assertEqual(abs(a[0]-b[0])+abs(a[1]-b[1]),1)
        self.assertIn((0,4),r['path'])
        self.assertIn((3,3),r['path'])
    def test_empty_and_unreachable(self):
        self.assertEqual(m.optimize([[0]],(0,0),[])['distance'],0)
        with self.assertRaises(ValueError): m.optimize([[0,1,0]],(0,0),[(0,2)])

if __name__ == "__main__":
    unittest.main(verbosity=2)
