"""Project 04 — Two-link robotic arm kinematics simulator.

Direct and inverse kinematics, workspace, joint limits, singularity awareness
and a small animated trajectory.

Technologies: Python + NumPy + optional Matplotlib.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np

try:  # pragma: no cover - depends on the user environment
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    _HAVE_MPL = True
except ImportError:  # pragma: no cover
    _HAVE_MPL = False

L1 = 2.0
L2 = 1.0


def forward_kinematics(
    l1: float = L1, l2: float = L2, theta1: float = 0.0, theta2: float = 0.0
) -> Tuple[float, float]:
    """Return the end-effector (x, y) for given joint angles (radians)."""
    x = l1 * np.cos(theta1) + l2 * np.cos(theta1 + theta2)
    y = l1 * np.sin(theta1) + l2 * np.sin(theta1 + theta2)
    return float(x), float(y)


def inverse_kinematics(
    l1: float = L1, l2: float = L2, x: float = 0.0, y: float = 0.0, elbow_up: bool = False
) -> Tuple[float, float]:
    """Return (theta1, theta2) solving the forward model (inverse kinematics).

    Raises ValueError when the target is out of the reachable workspace.
    """
    if l1 <= 0 or l2 <= 0:
        raise ValueError("link lengths must be positive")
    r2 = x * x + y * y
    cos_theta2 = (r2 - l1 * l1 - l2 * l2) / (2.0 * l1 * l2)
    if cos_theta2 > 1.0 or cos_theta2 < -1.0:
        raise ValueError("target is unreachable for these link lengths")
    cos_theta2 = float(np.clip(cos_theta2, -1.0, 1.0))
    theta2 = np.arccos(cos_theta2) * (1.0 if elbow_up else -1.0)
    theta1 = np.atan2(y, x) - np.atan2(
        l2 * np.sin(theta2), l1 + l2 * np.cos(theta2)
    )
    return float(theta1), float(theta2)


def is_reachable(
    l1: float = L1, l2: float = L2, x: float = 0.0, y: float = 0.0
) -> bool:
    """True when the target lies inside the reachable workspace."""
    r = float(np.hypot(x, y))
    min_r = abs(l1 - l2)
    max_r = l1 + l2
    return min_r <= r <= max_r


def workspace(
    l1: float = L1, l2: float = L2, steps: int = 400
) -> Tuple[float, float]:
    """Return (inner_radius, outer_radius) of the arm's workspace."""
    min_r = abs(l1 - l2)
    max_r = l1 + l2
    return min_r, max_r


def trajectory(
    l1: float = L1,
    l2: float = L2,
    theta1: np.ndarray = None,
    theta2: np.ndarray = None,
    steps: int = 60,
) -> List[Tuple[float, float]]:
    """Sample an (x, y) trajectory along a linear change of joint angles."""
    if theta1 is None:
        theta1 = np.linspace(0, np.pi / 2, steps)
        theta2 = np.linspace(np.pi / 4, np.pi / 4, steps)
    theta1 = np.asarray(theta1, dtype=float)
    theta2 = np.asarray(theta2, dtype=float)
    if theta1.size != theta2.size:
        raise ValueError("theta1 and theta2 must have the same length")
    points: List[Tuple[float, float]] = []
    for t1, t2 in zip(theta1, theta2):
        points.append(forward_kinematics(l1, l2, float(t1), float(t2)))
    return points


def demo() -> Dict:
    """Run forward/inverse kinematics, reach an unreachable target, and plot."""
    forward = forward_kinematics()
    inverse = inverse_kinematics(x=2.0, y=2.0)
    reconstructed = forward_kinematics(*inverse)
    lo, hi = workspace()
    sample = trajectory(steps=40)
    unreachable = is_reachable(x=6.0, y=6.0)
    if _HAVE_MPL:
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.add_patch(plt.Rectangle((0, 0), lo, hi, fill=True, color="#f0f0f0"))
        xs = [p[0] for p in sample]
        ys = [p[1] for p in sample]
        ax.plot([0, sample[0][0]], [0, sample[0][1]], color="#2e9e5b", lw=2)
        ax.plot(xs, ys, color="#2e9e5b", lw=2, marker="o", ms=3)
        ax.plot(*forward_kinematics(), "o", color="#FF3355", ms=10, label="effort")
        ax.set_xlim(0, 4)
        ax.set_ylim(0, 4)
        ax.set_aspect("equal")
        ax.legend()
        plt.tight_layout()
        fig.savefig("04_robot_arm_kinematics.png", dpi=110)

    return {
        "link_lengths": {"l1": L1, "l2": L2},
        "forward": {"x": round(forward[0], 3), "y": round(forward[1], 3)},
        "inverse": {
            "theta1": round(inverse[0], 3),
            "theta2": round(inverse[1], 3),
            "reconstructed": {
                "x": round(reconstructed[0], 3),
                "y": round(reconstructed[1], 3),
            },
        },
        "workspace": [round(lo, 3), round(hi, 3)],
        "trajectory_points": len(sample),
        "unreachable_tested": unreachable,
        "plot": "04_robot_arm_kinematics.png",
    }
