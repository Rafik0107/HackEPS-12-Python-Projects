"""Tests for project 12 (smart warehouse route optimizer)."""

import unittest
from itertools import permutations

import numpy as np

from src.project import (
    build_warehouse,
    demo,
    find_path,
    order_pick_points,
    optimize_route,
    tour_distance,
)


class TestBuildWarehouse(unittest.TestCase):
    def test_grid_shape(self):
        g = build_warehouse(rows=6, cols=6, obstacle_density=0.0, seed=1)
        self.assertEqual(g.shape, (6, 6))

    def test_depot_free(self):
        g = build_warehouse(rows=4, cols=4, obstacle_density=0.0, seed=1)
        self.assertEqual(g[0, 0], 0)


class TestFindPath(unittest.TestCase):
    def test_open_grid(self):
        g = np.zeros((5, 5), dtype=int)
        path = find_path(g, (0, 0), (4, 4))
        self.assertTrue(path)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (4, 4))

    def test_blocked(self):
        g = np.ones((4, 4), dtype=int)
        path = find_path(g, (0, 0), (3, 3))
        self.assertEqual(path, [])

    def test_start_equals_goal(self):
        g = np.zeros((3, 3), dtype=int)
        self.assertEqual(find_path(g, (1, 1), (1, 1)), [(1, 1)])


class TestRouteOrdering(unittest.TestCase):
    def test_nearest_neighbour(self):
        pts = [(0, 0), (5, 0), (5, 5)]
        order = order_pick_points(pts, start=(0, 0))
        self.assertEqual(order[0], (0, 0))
        self.assertEqual(order[-1], (5, 5))

    def test_tour_distance(self):
        pts = [(0, 0), (5, 0), (5, 5)]
        order = order_pick_points(pts, start=(0, 0))
        dist = tour_distance(order)
        self.assertGreater(dist, 0.0)


class TestOptimizeRoute(unittest.TestCase):
    def test_exhaustive_for_small(self):
        pts = [(0, 0), (1, 0), (1, 1)]
        best, dist = optimize_route(pts, start=(0, 0))
        self.assertEqual(len(best), 1 + len(pts))
        self.assertLessEqual(dist, tour_distance(best))

    def test_naive_used_for_large(self):
        # Generate many points to force the nearest-neighbour path.
        pts = [(int(x), int(y)) for x in range(20) for y in range(20)]
        order, dist = optimize_route(pts)
        self.assertLessEqual(len(order), len(pts) + 1)


class TestDemo(unittest.TestCase):
    def test_demo_runs(self):
        result = demo()
        self.assertIn("naive", result)
        self.assertIn("optimized", result)
        self.assertGreaterEqual(result["improvement"], 0.0)


if __name__ == "__main__":
    unittest.main()
