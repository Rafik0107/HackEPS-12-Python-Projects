"""Optimal four-connected grid navigation with Manhattan A*."""
import heapq
import json
import numpy as np


def astar(grid, start, goal):
    grid = np.asarray(grid)
    if grid.ndim != 2 or not grid.size or not np.isin(grid, [0, 1]).all():
        raise ValueError("grid must be a nonempty binary matrix (1 = obstacle)")
    def valid(p):
        return (len(p) == 2 and all(isinstance(v, (int, np.integer)) for v in p)
                and 0 <= p[0] < grid.shape[0] and 0 <= p[1] < grid.shape[1]
                and grid[p] == 0)
    start, goal = tuple(start), tuple(goal)
    if not valid(start) or not valid(goal):
        raise ValueError("endpoints must be free integer grid cells")
    def h(p):
        return abs(p[0]-goal[0]) + abs(p[1]-goal[1])
    queue, cost, parent = [(h(start), 0, start)], {start: 0}, {}
    while queue:
        _, g, p = heapq.heappop(queue)
        if g != cost[p]:
            continue
        if p == goal:
            route = [p]
            while p in parent:
                p = parent[p]
                route.append(p)
            return route[::-1]
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            q = p[0]+dr, p[1]+dc
            if valid(q) and g+1 < cost.get(q, float('inf')):
                cost[q], parent[q] = g+1, p
                heapq.heappush(queue, (g+1+h(q), g+1, q))
    return []


def demo():
    grid = np.zeros((8, 8), dtype=int)
    grid[3, :6] = 1
    route = astar(grid, (0, 0), (7, 7))
    return {"path": route, "steps": len(route)-1}

if __name__ == '__main__':
    print(json.dumps(demo(), indent=2))
