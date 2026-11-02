"""Obstacle-aware shortest paths and exact small-batch picking tour (Held-Karp)."""
from collections import deque
import json
import numpy as np


def optimize(grid, depot, picks):
    grid = np.asarray(grid)
    if grid.ndim != 2 or not grid.size or not np.isin(grid, [0, 1]).all():
        raise ValueError("nonempty binary grid required")
    points = [tuple(depot)] + [tuple(p) for p in picks]
    if len(points) > 13 or len(set(points)) != len(points):
        raise ValueError("at most 12 distinct picks, excluding depot")
    for p in points:
        if (len(p) != 2 or not all(isinstance(v, (int, np.integer)) for v in p)
            or not 0 <= p[0] < grid.shape[0] or not 0 <= p[1] < grid.shape[1] or grid[p]):
            raise ValueError("locations must be free integer cells")
    paths = {}
    for i, source in enumerate(points):
        parent, queue = {source: None}, deque([source])
        while queue:
            p = queue.popleft()
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                q = p[0]+dr, p[1]+dc
                if (0 <= q[0] < grid.shape[0] and 0 <= q[1] < grid.shape[1]
                    and not grid[q] and q not in parent):
                    parent[q] = p
                    queue.append(q)
        for j, dest in enumerate(points):
            if dest not in parent:
                raise ValueError("a picking location is unreachable")
            path, p = [], dest
            while p is not None:
                path.append(p)
                p = parent[p]
            paths[i, j] = path[::-1]
    n = len(points)-1
    if n == 0:
        return {"order": [points[0]], "path": [points[0]], "distance": 0}
    distance = lambda i, j: len(paths[i, j])-1
    dp = {(1 << j, j): (distance(0, j+1), [j+1]) for j in range(n)}
    for mask in range(1, 1 << n):
        for j in range(n):
            if (mask, j) not in dp:
                continue
            cost, order = dp[mask, j]
            for k in range(n):
                if mask & (1 << k):
                    continue
                key = mask | (1 << k), k
                candidate = cost+distance(j+1, k+1)
                if key not in dp or candidate < dp[key][0]:
                    dp[key] = candidate, order+[k+1]
    total, order = min((dp[(1 << n)-1, j][0]+distance(j+1, 0),
                        dp[(1 << n)-1, j][1]) for j in range(n))
    indices = [0]+order+[0]
    path = [points[0]]
    for a, b in zip(indices, indices[1:]):
        path.extend(paths[a, b][1:])
    return {"order": [points[i] for i in indices], "path": path, "distance": total}


def demo():
    grid = np.zeros((8, 8), dtype=int)
    grid[1:6, 3] = 1
    return optimize(grid, (0, 0), [(2, 2), (6, 6), (0, 7)])

if __name__ == '__main__':
    print(json.dumps(demo(), indent=2))
