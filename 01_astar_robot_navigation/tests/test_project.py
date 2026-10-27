"""Tests for project 01 (A* / Dijkstra navigation)."""

import unittest
from pathlib import Path

from src.project import (
    astar,
    dijkstra,
    is_reachable,
    compare,
    visualize,
    demo,
)


class TestGridPathfinding(unittest.TestCase):
    def test_astar_finds_path(self):
        grid = [
            ".....",
            ".###.",
            ".....",
            "..#..",
            ".....",
        ]
        path = astar(grid, (0, 0), (4, 4))
        self.assertTrue(path)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (4, 4))
        for r, c in path:
            self.assertTrue(0 <= r < 5 and 0 <= c < 5)
            self.assertNotEqual(grid[r][c], "#")

    def test_astar_returns_empty_when_unreachable(self):
        grid = [
            "..#..",
            ".#.#.",
            "#...#",
            ".#.#.",
            "..#..",
        ]
        self.assertEqual(astar(grid, (0, 0), (4, 4)), [])

    def test_dijkstra_matches_astar_on_open_grid(self):
        grid = [
            ".....",
            ".....",
            ".....",
            ".....",
            ".....",
        ]
        a = astar(grid, (0, 0), (4, 4))
        d = dijkstra(grid, (0, 0), (4, 4))
        self.assertEqual(len(a), len(d))

    def test_is_reachable(self):
        open_grid = [list(".....")] * 5
        self.assertTrue(is_reachable(open_grid, (0, 0), (4, 4)))
        wall_grid = [list("...#.")] * 5
        self.assertFalse(is_reachable(wall_grid, (0, 0), (4, 4)))


class TestCompare(unittest.TestCase):
    def test_compare_returns_numeric_fields(self):
        grid = [
            ".....",
            ".###.",
            ".....",
            "..#..",
            ".....",
        ]
        result = compare(grid, (0, 0), (4, 4))
        self.assertEqual(result["path_astar_length"], result["path_dijkstra_length"])
        self.assertGreaterEqual(result["path_astar_time_ms"], 0.0)
        self.assertGreaterEqual(result["path_dijkstra_time_ms"], 0.0)


class TestVisualise(unittest.TestCase):
    def test_visualize_creates_a_file(self):
        grid = [
            ".....",
            ".###.",
            ".....",
            "..#..",
            ".....",
        ]
        fname = visualize(grid, astar(grid, (0, 0), (4, 4)), "01_probe")
        self.assertTrue(fname.endswith((".png", ".txt")))
        self.assertTrue(Path(fname).exists())

    def test_demo_runs(self):
        result = demo()
        self.assertIsInstance(result, dict)
        self.assertTrue(result["path_found"])
        self.assertGreater(result["path_length"], 0)


if __name__ == "__main__":
    unittest.main()
