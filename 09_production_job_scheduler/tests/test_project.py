"""Tests for project 09 (production job scheduler)."""

import unittest

from src.project import Job, makespan, schedule, total_tardiness, normalize, demo


class TestSchedule(unittest.TestCase):
    def setUp(self):
        self.jobs = [Job("A", 4, 10), Job("B", 2, 3), Job("C", 3, 8)]

    def test_fcfs_order(self):
        plan = schedule(self.jobs, policy="fcfs")
        ids = [p["id"] for p in plan]
        self.assertEqual(ids[0], "A")

    def test_spt_order(self):
        plan = schedule(self.jobs, policy="spt")
        ids = [p["id"] for p in plan]
        self.assertEqual(ids[0], "B")

    def test_makespan(self):
        plan = schedule(self.jobs, policy="fcfs")
        self.assertAlmostEqual(makespan(plan), 9.0, places=6)

    def test_tardiness(self):
        plan = schedule(self.jobs, policy="fcfs")
        self.assertGreater(total_tardiness(plan), 0.0)


class TestNormalize(unittest.TestCase):
    def test_stable_order(self):
        jobs = [Job("C", 1, 1), Job("A", 1, 1)]
        out = normalize(jobs)
        self.assertEqual([j.id for j in out], ["A", "C"])


class TestDemo(unittest.TestCase):
    def test_demo_runs(self):
        result = demo()
        self.assertIn("policies", result)
        self.assertIn("spt", result["policies"])
        self.assertIn("makespan", result["policies"]["spt"])


if __name__ == "__main__":
    unittest.main()
