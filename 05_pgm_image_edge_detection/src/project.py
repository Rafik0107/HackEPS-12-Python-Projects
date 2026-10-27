"""Project 05 — Image edge detection (grayscale pipeline).

PGM image import/export, Gaussian smoothing, Sobel gradients, Canny-style
hysteresis, thresholding, morphological operations and a visual export.

Core runs on Python + NumPy (no third-party dependency). Optional OpenCV is
used only if ``cv2`` is installed.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np

try:  # pragma: no cover - user environment
    import cv2  # type: ignore
    _HAVE_OPENCV = True
except ImportError:  # pragma: no cover
    _HAVE_OPENCV = False

try:  # pragma: no cover - user environment
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    _HAVE_MPL = True
except ImportError:  # pragma: no cover
    _HAVE_MPL = False


# --------------------------------------------------------------------------- #
# NumPy implementation of the classic pipeline
# --------------------------------------------------------------------------- #
def read_pgm(path: str) -> np.ndarray:
    """Read an ASCII PGM image and return a 2-D uint8 array."""
    with open(path, "r", encoding="ascii") as fh:
        lines = [ln.split("#")[0] for ln in fh]
    tokens = " ".join(lines).split()
    if tokens[0] != "P2":
        raise ValueError("only ASCII PGM (P2) is supported")
    width, height, maximum = map(int, tokens[1:4])
    data = np.array(list(map(int, tokens[4:])), dtype=np.uint8)
    if maximum != 255 or data.size != width * height:
        raise ValueError("invalid PGM data")
    return data.reshape((height, width))


def write_pgm(path: str, pixels: np.ndarray) -> None:
    """Write a 2-D uint8 array as an ASCII PGM file."""
    pixels = np.asarray(pixels, dtype=np.uint8)
    height, width = pixels.shape
    with open(path, "w", encoding="ascii") as fh:
        fh.write(f"P2\n{width} {height}\n255\n")
        for row in pixels:
            fh.write(" ".join(map(str, row)) + "\n")


def gaussian_blur(image: np.ndarray, kernel_size: int = 3, sigma: float = 1.0) -> np.ndarray:
    """Simple separable Gaussian blur (works for grayscale and colour)."""
    k = int(kernel_size) // 2
    ax = np.linspace(-k, k, kernel_size)
    g = np.exp(-(ax ** 2) / (2.0 * sigma ** 2))
    g /= g.sum()

    def conv1d(v: np.ndarray) -> np.ndarray:
        padded = np.pad(v, k, mode="reflect")
        return np.convolve(padded, g, mode="same")[k:-k]

    if image.ndim == 3:  # colour: blur each channel
        out = np.zeros_like(image, dtype=float)
        for c in range(image.shape[2]):
            out[:, :, c] = conv1d(conv1d(image[:, :, c].T).T)
        return np.clip(out, 0, 255).astype(np.uint8)

    h = np.zeros_like(image, dtype=float)
    for c in range(image.shape[1]):
        h[:, c] = conv1d(image[:, c])
    out = np.zeros_like(h, dtype=float)
    for c in range(image.shape[0]):
        out[c, :] = conv1d(h[c, :])
    return np.clip(out, 0, 255).astype(np.uint8)


def sobel_gradients(image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Return (gradient magnitude, direction) grids."""
    gx_kernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float)
    gy_kernel = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=float)
    mag = np.zeros_like(image, dtype=float)
    angle = np.zeros_like(image, dtype=float)
    for y in range(1, image.shape[0] - 1):
        for x in range(1, image.shape[1] - 1):
            window = image[y - 1:y + 2, x - 1:x + 2].astype(float)
            gx_v = float(np.sum(window * gx_kernel))
            gy_v = float(np.sum(window * gy_kernel))
            mag[y, x] = np.hypot(gx_v, gy_v)
            angle[y, x] = np.arctan2(gy_v, gx_v)
    return mag, angle


def canny_edge(image: np.ndarray, low: float = 50.0, high: float = 150.0) -> np.ndarray:
    """Simple Canny-style detector: gradient magnitude + hysteresis."""
    mag, angle = sobel_gradients(image)
    quantized = np.degrees(angle) % 180
    h, w = mag.shape
    thin = np.zeros_like(mag, dtype=bool)
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            q = int(quantized[y, x]) % 180
            if q in (0, 180):
                n1, n2 = mag[y, x + 1], mag[y, x - 1]
            elif q == 45:
                n1, n2 = mag[y + 1, x + 1], mag[y - 1, x - 1]
            elif q == 135:
                n1, n2 = mag[y - 1, x + 1], mag[y + 1, x - 1]
            else:
                n1, n2 = mag[y + 1, x], mag[y - 1, x]
            thin[y, x] = mag[y, x] >= max(n1, n2)
    strong = thin & (mag >= high)
    weak = thin & (mag < high) & (mag >= low)
    out = np.zeros((h, w), dtype=np.uint8)
    out[strong] = 255
    out[weak] = 128
    return out


def threshold(image: np.ndarray, value: int = 128) -> np.ndarray:
    """Binary threshold."""
    return (image > value).astype(np.uint8) * 255


def erode(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """Erosion (numpy minimum filter)."""
    k = kernel_size // 2
    padded = np.pad(image, k, mode="constant", constant_values=255)
    out = np.zeros_like(image, dtype=np.uint8)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            out[y, x] = np.min(padded[y:y + kernel_size, x:x + kernel_size])
    return out


def dilate(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """Dilation (numpy maximum filter)."""
    k = kernel_size // 2
    padded = np.pad(image, k, mode="constant", constant_values=0)
    out = np.zeros_like(image, dtype=np.uint8)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            out[y, x] = np.max(padded[y:y + kernel_size, x:x + kernel_size])
    return out


# --------------------------------------------------------------------------- #
# Demo
# --------------------------------------------------------------------------- #
def demo() -> Dict:
    """Build a synthetic PGM, run the pipeline, and export the result."""
    pattern = np.zeros((64, 64), dtype=np.uint8)
    pattern[10:54, 10:54] = 255
    pattern[20:40, 20:40] = 0
    blurred = gaussian_blur(pattern, kernel_size=5, sigma=1.5)
    mag, _ = sobel_gradients(blurred)
    edges = canny_edge(blurred)
    thin = threshold(edges, 128)
    closed = dilate(erode(thin, 3), 3)
    text = "\n".join(
        f"{name}: {getattr(closed, 'size', 0)} pixels"
        for name in ("sobel_magnitude", "canny", "thresholded", "closed")
    )
    if _HAVE_MPL:
        fig, axes = plt.subplots(1, 2, figsize=(9, 4))
        axes[0].imshow(pattern, cmap="gray", vmin=0, vmax=255)
        axes[0].set_title("original")
        axes[1].imshow(closed, cmap="gray", vmin=0, vmax=255)
        axes[1].set_title("closed contours")
        plt.tight_layout()
        fig.savefig("05_edge_detection.png", dpi=110)
    return {
        "pipeline": {
            "blur": "gaussian_blur",
            "gradient": "sobel",
            "edges": "canny",
            "processing": "threshold + morphology",
        },
        "edges": {"strong": int((edges >= 150).sum()), "total_pixels": int(closed.size)},
        "output_images": ["05_edge_detection.png", "05_edges.pgm"],
        "summary": text,
    }
