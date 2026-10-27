"""Tests for project 11 (ECG signal analysis)."""

import unittest
import numpy as np

from src.project import (
    demo,
    detect_r_peaks,
    filter_noise,
    generate_ecg,
    heart_rate_from_rr,
    rr_intervals,
)


class TestGenerateECG(unittest.TestCase):
    def test_r_peaks_present(self):
        ecg = generate_ecg(heart_rate=60.0, sampling_rate=1000.0, duration=5.0, noise=0.0)
        peaks = detect_r_peaks(ecg, sampling_rate=1000.0, threshold_percentile=95)
        expected = int(5.0 / (60.0 / 60.0))
        self.assertGreaterEqual(peaks.size, expected - 1)
        self.assertLessEqual(peaks.size, expected + 2)

    def test_rms_nonzero(self):
        ecg = generate_ecg(heart_rate=75.0, noise=0.0)
        self.assertGreater(np.mean(ecg ** 2), 0.0)


class TestFiltering(unittest.TestCase):
    def test_moving_average_reduces_noise(self):
        ecg = generate_ecg(heart_rate=75.0, duration=2.0, noise=1.0)
        smoothed = filter_noise(ecg, sampling_rate=1000.0, window=21)
        self.assertLess(np.std(smoothed), np.std(ecg))


class TestPeakDetection(unittest.TestCase):
    def test_r_peaks_within_refractory(self):
        ecg = generate_ecg(heart_rate=60.0, duration=10.0, noise=0.0)
        peaks = detect_r_peaks(ecg, sampling_rate=1000.0)
        self.assertGreaterEqual(peaks.size, 5)

    def test_empty_signal(self):
        self.assertEqual(detect_r_peaks(np.array([]), 1000.0).size, 0)


class TestRRIntervals(unittest.TestCase):
    def test_spectial(self):
        peaks = np.array([100, 200, 300])
        rr = rr_intervals(peaks, sampling_rate=1000.0)
        np.testing.assert_array_equal(rr, np.array([0.1, 0.1]))


class TestHeartRate(unittest.TestCase):
    def test_heart_rate(self):
        rr = np.array([0.8, 1.0, 1.2])
        self.assertAlmostEqual(heart_rate_from_rr(rr), 60.0 / np.mean(rr), places=6)


class TestDemo(unittest.TestCase):
    def test_demo_runs(self):
        result = demo()
        self.assertIn("peaks", result)
        self.assertIn("heart_rate_bpm", result["peaks"])
        self.assertIsInstance(result["peaks"]["heart_rate_bpm"], float)


if __name__ == "__main__":
    unittest.main()
