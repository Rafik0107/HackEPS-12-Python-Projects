"""Numerical and boundary checks, run with python test_main.py."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np
spec = importlib.util.spec_from_file_location("project", Path(__file__).with_name("main.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class ProjectTests(unittest.TestCase):

    def test_known_heart_rates(self):
        for bpm in [60,72,120,180]:
            _,signal,beats=m.synthetic_ecg(bpm=bpm)
            result=m.analyze(signal)
            self.assertEqual(len(result['peak_indices']),len(beats))
            self.assertLess(abs(result['heart_rate_bpm']-bpm),1)
    def test_flat_signal(self):
        result=m.analyze(np.zeros(1000))
        self.assertIsNone(result['heart_rate_bpm'])
        self.assertEqual(result['peak_indices'],[])
    def test_refractory(self):
        x=np.zeros(100); x[10]=1; x[20]=.8; x[80]=1
        self.assertEqual(m.analyze(x,fs=100)['peak_indices'],[10,80])
    def test_invalid(self):
        with self.assertRaises(ValueError): m.analyze([1,2,3],fs=0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
