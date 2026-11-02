"""Tests for project 08 (vibration frequency analysis)."""

import unittest
import numpy as np

from src.project import (
    demo,
    dominant_frequency,
    lowpass_filter,
    read_csv,
    rms,
    simulate_signal,
    write_csv,
)


class TestSignal(unittest.TestCase):
    def test_simulation_length(self):
        s = simulate_signal(frequency=5.0, sampling_rate=100.0, duration=5.0)
        self.assertEqual(len(s), 500)

    def test_no_noise_mean(self):
        s = simulate_signal(frequency=5.0, noise=0.0, duration=10.0)
        self.assertGreater(np.mean(s), 0.0)


class TestSpectrum(unittest.TestCase):
    def test_dominant_frequency(self):
        s = simulate_signal(frequency=7.0, sampling_rate=100.0, duration=2.0)
        dom = dominant_frequency(s, sampling_rate=100.0)
        self.assertAlmostEqual(dom, 7.0, delta=0.5)

    def test_spectrum_raises_on_bad_input(self):
        with self.assertRaises(ValueError):
            dominant_frequency(np.array([1.0]), sampling_rate=100.0)


class TestRMS(unittest.TestCase):
    def test_rms(self):
        s = np.ones(10) * 2.0
        self.assertAlmostEqual(rms(s), 2.0, places=6)

    def test_rms_empty(self):
        self.assertEqual(rms(np.array([])), 0.0)


class TestFilter(unittest.TestCase):
    def test_lowpass_noiseless(self):
        s = np.array([1.0, 1.0, 1.0, 1.0, 1.0])
        out = lowpass_filter(s, sampling_rate=10.0, cutoff=1.0)
        self.assertAlmostEqual(float(np.mean(out)), 1.0, places=3)

    def test_lowpass_reduces_variation(self):
        s = np.array([0.0, 2.0, 0.0, 2.0, 0.0, 2.0])
        out = lowpass_filter(s, sampling_rate=10.0, cutoff=1.0)
        self.assertGreater(np.std(s), np.std(out))


class TestCsvIO(unittest.TestCase):
    def test_write_read(self):
        p = "08_probe.csv"
        write_csv(p, np.array([1.0, 2.0, 3.0]))
        self.assertTrue(__import__("pathlib").Path(p).exists())
        reloaded = read_csv(p)
        np.testing.assert_array_equal(reloaded, np.array([1.0, 2.0, 3.0]))
        __import__("pathlib").Path(p).unlink(missing_ok=True)

    def test_missing_csv(self):
        with self.assertRaises(FileNotFoundError):
            read_csv("08_missing.csv")


class TestDemo(unittest.TestCase):
    def test_demo_runs(self):
        result = demo()
        self.assertIn("frequencies", result)
        self.assertIn("rms", result)
        self.assertGreaterEqual(result["frequencies"]["dominant_normal"], 0.0)


if __name__ == "__main__":
    unittest.main()
