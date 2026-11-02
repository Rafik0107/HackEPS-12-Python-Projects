"""NumPy Sobel gradients and relative-threshold edge maps."""
import argparse
import json
import numpy as np


def sobel(image, threshold=.25):
    a = np.asarray(image, dtype=float)
    if a.ndim != 2 or min(a.shape) < 3 or not np.isfinite(a).all():
        raise ValueError("finite grayscale image of at least 3x3 required")
    if not np.isfinite(threshold) or not 0 <= threshold <= 1:
        raise ValueError("threshold must be in [0,1]")
    p = np.pad(a, 1, mode='edge')
    w = np.lib.stride_tricks.sliding_window_view(p, (3, 3))
    kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    gx = np.einsum('ijkl,kl->ij', w, kx)
    gy = np.einsum('ijkl,kl->ij', w, kx.T)
    magnitude = np.hypot(gx, gy)
    edges = (magnitude > 0) & (magnitude >= threshold*magnitude.max())
    return magnitude, edges


def demo():
    image = np.zeros((64, 64))
    image[16:48, 16:48] = 1
    _, edges = sobel(image)
    return {"shape": list(image.shape), "edge_pixels": int(edges.sum())}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', help='Optional grayscale .npy array')
    parser.add_argument('--output', default='edges.npy')
    args = parser.parse_args()
    if args.input:
        _, edges = sobel(np.load(args.input, allow_pickle=False))
        np.save(args.output, edges)
        print(json.dumps({"output": args.output, "edge_pixels": int(edges.sum())}))
    else:
        print(json.dumps(demo(), indent=2))
