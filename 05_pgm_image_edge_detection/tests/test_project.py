"""Tests for project 05 (image edge detection pipeline)."""

import unittest
from pathlib import Path

import numpy as np

from src.project import (
    canny_edge,
    demo,
    erode,
    gaussian_blur,
    read_pgm,
    sobel_gradients,
    threshold,
    write_pgm,
)


class TestGaussianBlur(unittest.TestCase):
    def test_blur_reduces_variance(self):
        image = np.full((10, 10), 128, dtype=np.uint8)
        image[5, 5] = 0
        out = gaussian_blur(image, kernel_size=3, sigma=1.0)
        self.assertLess(np.std(out), np.std(image))


class TestSobel(unittest.TestCase):
    def test_magnitude_positive(self):
        image = np.zeros((5, 5), dtype=np.uint8)
        image[2, 1:4] = [0, 1, 2]
        mag, _ = sobel_gradients(image)
        self.assertGreater(mag[2, 2], 0.0)


class TestCanny(unittest.TestCase):
    def test_edges_present(self):
        image = np.zeros((20, 20), dtype=np.uint8)
        image[5:15, 5:15] = 255
        edges = canny_edge(image)
        self.assertGreater(int((edges > 0).sum()), 0)


class TestThreshold(unittest.TestCase):
    def test_binary(self):
        image = np.array([[100, 200], [50, 250]], dtype=np.uint8)
        out = threshold(image, value=128)
        expected = np.array([[0, 255], [0, 255]], dtype=np.uint8)
        np.testing.assert_array_equal(out, expected)


class TestMorphology(unittest.TestCase):
    def test_erode_darkens(self):
        image = np.array([[255, 255], [255, 255]], dtype=np.uint8)
        out = erode(image, kernel_size=3)
        self.assertLess(int(out.sum()), 1024)


class TestPgmIO(unittest.TestCase):
    def test_roundtrip(self):
        data = np.array([[0, 255], [255, 0]], dtype=np.uint8)
        pgm = "05_probe.pgm"
        write_pgm(pgm, data)
        reloaded = read_pgm(pgm)
        Path(pgm).unlink(missing_ok=True)
        np.testing.assert_array_equal(reloaded, data)


class TestDemo(unittest.TestCase):
    def test_demo_runs(self):
        result = demo()
        self.assertIn("pipeline", result)
        self.assertIn("edges", result)
        self.assertIn("output_images", result)


if __name__ == "__main__":
    unittest.main()
