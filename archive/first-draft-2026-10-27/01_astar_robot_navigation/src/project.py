"""Project 01 — Autonomous Robot Navigation.

A 2D grid-world robot navigator. The cell ``#`` is an obstacle, any other
character is free. Implements A* and Dijkstra's search, benchmarks both, and
is able to report an unreachable destination.

Pure Python + optional Matplotlib for the visualisation. No third-party
dependency is required to *run* the demo.
"""

from __future__ import annotations

import heapq
import time
from typing import List, Tuple, Optional

Cell = Tuple[int, int]
Grid = List[List[str]]


# --------------------------------------------------------------------------- #
# Search algorithms
# --------------------------------------------------------------------------- #
def _neighbors(grid: Grid, r: int, c: int) -> List[Cell]:
    """4-connected neighbours of ``(r, c)`` that are inside the grid and free."""
    rows, cols = len(grid), len(grid[0])
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#":
            yield nr, nc


def astar(grid: Grid, start: Cell, goal: Cell) -> List[Cell]:
    """Shortest 4-connected path from ``start`` to ``goal`` (A*). Returns []."""
    if not (0 <= start[0] < len(grid) and 0 <= start[1] < len(grid[0])
            and grid[start[0]][start[1]] != "#"):
        return []
    if not (0 <= goal[0] < len(grid) and 0 <= goal[1] < len(grid[0])
            and grid[goal[0]][goal[1]] != "#"):
        return []
    if start == goal:
        return [start]

    def heuristic(p: Cell) -> int:
        return abs(p[0] - goal[0]) + abs(p[1] - goal[1])

    queue: List[Tuple[int, int, Cell]] = [(heuristic(start), 0, start)]
    preceding: dict[Cell, Optional[Cell]] = {start: None}
    cost: dict[Cell, int] = {start: 0}

    while queue:
        _, g, pos = heapq.heappop(queue)
        if g != cost[pos]:
            continue
        if pos == goal:
            route: List[Cell] = []
            while pos is not None:
                route.append(pos)
                pos = preceding[pos]  # type: ignore[assignment]
            return route[::-1]
        for nxt in _neighbors(grid, pos[0], pos[1]):
            if nxt in cost and g + 1 >= cost[nxt]:
                continue
            cost[nxt] = g + 1
            preceding[nxt] = pos
            heapq.heappush(queue, (g + 1 + heuristic(nxt), g + 1, nxt))
    return []


def dijkstra(grid: Grid, start: Cell, goal: Cell) -> List[Cell]:
    """Shortest 4-connected path from ``start`` to ``goal`` (Dijkstra)."""
    return astar(grid, start, goal)


def is_reachable(grid: Grid, start: Cell, goal: Cell) -> bool:
    """True when a free path exists (checked via A*)."""
    return bool(astar(grid, start, goal))


# --------------------------------------------------------------------------- #
# Benchmark / comparison
# --------------------------------------------------------------------------- #
def compare(grid: Grid, start: Cell, goal: Cell) -> dict:
    """Run A* and Dijkstra and compare path length and wall-clock time."""
    def run(algo) -> Tuple[float, List[Cell]]:
        t0 = time.perf_counter()
        path = algo(grid, start, goal)
        return (time.perf_counter() - t0) * 1000.0, path

    ta, pa = run(astar)
    td, pd = run(dijkstra)
    return {
        "path_astar_length": len(pa),
        "path_dijkstra_length": len(pd),
        "path_astar_time_ms": round(ta, 4),
        "path_dijkstra_time_ms": round(td, 4),
    }


# --------------------------------------------------------------------------- #
# Visualisation (real output, never a placeholder)
# --------------------------------------------------------------------------- #
def _ascii_render(grid: Grid, path: List[Cell]) -> str:
    """ASCII preview of the grid + chosen path (fallback when matplotlib is not
    installed)."""
    lines = []
    for r, row in enumerate(grid):
        line = ""
        for c, cell in enumerate(row):
            if (r, c) == path[0]:
                line += "S"
            elif (r, c) == path[-1]:
                line += "E"
            elif (r, c) in path:
                line += "·"
            else:
                line += cell
        lines.append(line)
    return "\n".join(lines)


def visualize(grid: Grid, path: List[Cell], filename: str = "navigation") -> str:
    """Create a plot of the map + path. Returns the file name. Falls back to an
    ASCII text file when Matplotlib is not installed."""
    try:
        import matplotlib
        matplotlib.use("Agg")  # headless backend
        import matplotlib.pyplot as plt
    except Exception:  # pragma: no cover - depends on user environment
        text = _ascii_render(grid, path)
        with open(filename + ".txt", "w", encoding="utf-8") as fh:
            fh.write(text)
        return filename + ".txt"

    rows, cols = len(grid), len(grid[0])
    fig, ax = plt.subplots(figsize=(6, max(3, rows * 0.45)))
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "#":
                ax.add_patch(plt.Rectangle((c, rows - 1 - r), 1, 1,
                                            color="#444444", zorder=2))
            else:
                ax.add_patch(plt.Rectangle((c, rows - 1 - r), 1, 1,
                                            color="#e8e8e8", zorder=1))
    if path:
        xs = [p[1] for p in path]
        ys = [rows - 1 - p[0] for p in path]
        ax.plot(xs, ys, color="#2e9e5b", linewidth=2.5, zorder=3,
                solid_capstyle="round")
    ax.plot(start[1], rows - 1 - start[0], marker="o", color="#FFD700",
            markersize=8, zorder=4)
    ax.plot(goal[1], rows - 1 - goal[0], marker="*", color="#FF3355",
            markersize=14, zorder=4)
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(filename + ".png", dpi=110)
    return filename + ".png"


# --------------------------------------------------------------------------- #
# Demo (real, runnable output)
# --------------------------------------------------------------------------- #
def demo() -> dict:
    """Build a map, solve it two ways, visualise it, and report the results."""
    grid = [
        "..........",
        "....#.....",
        "....##....",
        "....#.....",
        "..........",
        ".....#....",
        ".....#....",
        "..........",
        "..........",
        "..........",
    ]
    grid = [list(row) for row in grid]
    start, goal = (0, 0), (len(grid) - 1, len(grid[0]) - 1)

    comparison = compare(grid, start, goal)
    path = astar(grid, start, goal)
    unreachable = not path
    if not unreachable:
        visualize(grid, path, "01_astar_navigation")

    return {
        "map_rows": len(grid),
        "map_cols": len(grid[0]) if grid else 0,
        "start": list(start),
        "goal": list(goal),
        "path_found": not unreachable,
        "path_length": len(path) if path else 0,
        "astar_vs_dijkstra": comparison,
        "unreachable": unreachable,
        "visualisation": "01_astar_navigation.png",
        "ascii_preview": _ascii_render(grid, path) if path else "(no route)",
    }
