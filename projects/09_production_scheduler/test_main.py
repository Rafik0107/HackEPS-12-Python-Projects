"""Numerical and boundary checks, run with python test_main.py."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np
spec = importlib.util.spec_from_file_location("project", Path(__file__).with_name("main.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class ProjectTests(unittest.TestCase):

    def test_jobs_once_no_overlap(self):
        jobs={'a':3,'b':4,'c':5,'d':2}
        result=m.schedule(jobs,2)
        self.assertEqual(sorted(p['job'] for p in result['plan']),sorted(jobs))
        for machine in range(2):
            rows=[p for p in result['plan'] if p['machine']==machine]
            for a,b in zip(rows,rows[1:]): self.assertLessEqual(a['end'],b['start'])
        self.assertGreaterEqual(result['makespan'],result['lower_bound'])
    def test_known_optimum(self):
        self.assertEqual(m.schedule({'a':3,'b':3,'c':2,'d':2},2)['makespan'],5)
        self.assertEqual(m.schedule({'a':3,'b':2},1)['makespan'],5)
    def test_invalid(self):
        with self.assertRaises(ValueError): m.schedule({'a':-2})

if __name__ == "__main__":
    unittest.main(verbosity=2)
