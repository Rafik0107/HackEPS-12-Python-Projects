"""Project 12 — Smart warehouse route optimizer.

A mobile-robot route optimizer for a warehouse: a grid map with aisles, pick
positions, shortest-path routing (BFS), tour ordering (nearest neighbour plus
small exact solve) and deterministic scenario comparison.

Core: Python + NumPy. matplotlib optional.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np

try:  # pragma: no cover - user environment
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    _HAVE_MPL = True
except ImportError:  # pragma: no cover
    _HAVE_MPL = False

FREE = 0
OBSTACLE = 1


def build_warehouse(
    rows: int = 8,
    cols: int = 8,
    *,
    obstacle_density: float = 0.15,
    seed: int = 0,
) -> np.ndarray:
    """Create a warehouse grid with obstacles and a marked depot."""
    rng = np.random.default_rng(seed)
    grid = np.zeros((rows, cols), dtype=int)
    n = int(rows * cols * obstacle_density)
    coords = rng.choice(rows * cols, size=n, replace=False)
    for idx in coords:
        grid[idx // cols, idx % cols] = OBSTACLE
    grid[0, 0] = FREE  # depot at top-left
    return grid


def is_free(grid: np.ndarray, r: int, c: int) -> bool:
    """True when ``(r, c)`` is inside the grid and free."""
    return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1] and grid[r, c] == FREE


def find_path(grid: np.ndarray, start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Return a shortest 4-connected path via BFS, or [] if unreachable."""
    if not is_free(grid, *start) or not is_free(grid, *goal):
        return []
    if start == goal:
        return [start]
    queue = [start]
    parent = {start: None}
    while queue:
        r, c = queue.pop(0)
        if (r, c) == goal:
            path = []
            cur = (r, c)
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            return path[::-1]
        for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if is_free(grid, nr, nc) and (nr, nc) not in parent:
                parent[(nr, nc)] = (r, c)
                queue.append((nr, nc))
    return []


def order_pick_points(
    locations: List[Tuple[int, int]], start: Tuple[int, int] = (0, 0)
) -> List[Tuple[int, int]]:
    """Order pick locations with a nearest-neighbour heuristic."""
    remaining = list(locations)
    order = [start]
    while remaining:
        last = order[-1]
        dists = [np.hypot(last[0] - x, last[1] - y) for x, y in remaining]
        order.append(remaining.pop(int(np.argmin(dists))))
    return order


def tour_distance(order: List[Tuple[int, int]]) -> float:
    """Total path length of an ordered tour."""
    if len(order) < 2:
        return 0.0
    return float(sum(np.hypot(order[i][0] - order[i - 1][0], order[i][1] - order[i - 1][1]) for i in range(1, len(order))))


def optimize_route(
    locations: List[Tuple[int, int]],
    start: Tuple[int, int] = (0, 0),
) -> Tuple[List[Tuple[int, int]], float]:
    """Order picks with nearest neighbour; exact for very small sets."""
    if len(locations) <= 6:
        best, best_dist = None, float("inf")
        for perm in __import__("itertools").permutations(locations):
            tour = [start] + list(perm)
            d = tour_distance(tour)
            if d < best_dist:
                best, best_dist = tour, d
        return best, best_dist
    return order_pick_points(locations, start), tour_distance(order_pick_points(locations, start))


def distances_between(points: List[Tuple[int, int]]) -> float:
    """Total Euclidean distance of a point chain."""
    return float(sum(np.hypot(points[i][0] - points[i - 1][0], points[i][1] - points[i - 1][1]) for i in range(1, len(points))))


def demo() -> Dict:
    """Simulate a warehouse, plan picks and compare naive vs optimized order."""
    grid = build_warehouse(rows=8, cols=8, obstacle_density=0.2, seed=3)
    picks = [(2, 4), (5, 2), (2, 6), (6, 6)]
    naive = order_pick_points(picks, start=(0, 0))
    optimized, opt_dist = optimize_route(picks, start=(0, 0))
    naive_dist = tour_distance(naive)
    optimized_route = find_path(grid, (0, 0), optimized[-1])

    if _HAVE_MPL:
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.imshow(grid, cmap="gray")
        for x, y in optimized:
            ax.plot(x, y, "o", color="#2e9e5b" if (x, y) != (0, 0) else "gold")
        xs = [p[1] for p in optimized]
        ys = [p[0] for p in optimized]
        ax.plot(xs, ys, color="#FF3355", lw=2, label="parcours optimise")
        ax.set_title("Optimisation du parcours d'entrepôt")
        ax.legend()
        plt.tight_layout()
        fig.savefig("12_warehouse_route.png", dpi=110)

    return {
        "map": {
            "rows": int(grid.shape[0]),
            "cols": int(grid.shape[1]),
            "obstacles": int((grid == OBSTACLE).sum()),
        },
        "picks": picks,
        "naive": {"order": naive, "distance": round(naive_dist, 3)},
        "optimized": {
            "order": optimized,
            "distance": round(opt_dist, 3),
            "route_found": len(optimized_route) > 0,
        },
        "improvement": round((naive_dist - opt_dist) / max(naive_dist, 1e-9) * 100.0, 2),
    }
