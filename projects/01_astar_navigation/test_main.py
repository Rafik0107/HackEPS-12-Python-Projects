"""Numerical and boundary checks, run with python test_main.py."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np
spec = importlib.util.spec_from_file_location("project", Path(__file__).with_name("main.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class ProjectTests(unittest.TestCase):

    def test_obstacle_path_matches_bfs(self):
        from collections import deque
        rng = np.random.default_rng(7)
        for _ in range(20):
            grid = (rng.random((8, 8)) < .25).astype(int)
            grid[0, 0] = grid[7, 7] = 0
            queue, distances = deque([(0, 0)]), {(0, 0): 0}
            while queue:
                r, c = queue.popleft()
                for p in [(r+1,c),(r-1,c),(r,c+1),(r,c-1)]:
                    if 0 <= p[0] < 8 and 0 <= p[1] < 8 and not grid[p] and p not in distances:
                        distances[p] = distances[r,c]+1
                        queue.append(p)
            path = m.astar(grid, (0,0), (7,7))
            self.assertEqual(len(path)-1 if path else None, distances.get((7,7)))
            for a,b in zip(path,path[1:]):
                self.assertEqual(abs(a[0]-b[0])+abs(a[1]-b[1]),1)
                self.assertEqual(grid[b],0)
    def test_same_cell(self):
        self.assertEqual(m.astar([[0]], (0,0), (0,0)), [(0,0)])
    def test_invalid(self):
        with self.assertRaises(ValueError): m.astar([[1]], (0,0), (0,0))

if __name__ == "__main__":
    unittest.main(verbosity=2)
