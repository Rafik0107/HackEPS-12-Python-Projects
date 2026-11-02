"""Analytical forward/inverse kinematics of a planar two-link arm."""
import json
import numpy as np


def lengths(l1, l2):
    if not np.isfinite([l1, l2]).all() or min(l1, l2) <= 0:
        raise ValueError("link lengths must be finite and positive")


def forward(theta1, theta2, l1=1., l2=1.):
    lengths(l1, l2)
    if not np.isfinite([theta1, theta2]).all():
        raise ValueError("angles must be finite")
    return np.array([l1*np.cos(theta1)+l2*np.cos(theta1+theta2),
                     l1*np.sin(theta1)+l2*np.sin(theta1+theta2)])


def inverse(x, y, l1=1., l2=1.):
    lengths(l1, l2)
    if not np.isfinite([x, y]).all():
        raise ValueError("target must be finite")
    c = (x*x+y*y-l1*l1-l2*l2)/(2*l1*l2)
    if abs(c) > 1+1e-12:
        raise ValueError("target outside workspace")
    if np.hypot(x, y) < 1e-12 and abs(l1-l2) < 1e-12:
        return [(0., float(np.pi))]  # Representative of infinitely many solutions.
    angle = np.arccos(np.clip(c, -1, 1))
    return [(float(np.arctan2(y, x)-np.arctan2(l2*np.sin(q), l1+l2*np.cos(q))),
             float(q)) for q in (angle, -angle)]


def jacobian(theta1, theta2, l1=1., l2=1.):
    forward(theta1, theta2, l1, l2)
    a = theta1+theta2
    return np.array([[-l1*np.sin(theta1)-l2*np.sin(a), -l2*np.sin(a)],
                     [l1*np.cos(theta1)+l2*np.cos(a), l2*np.cos(a)]])


def demo():
    solutions = inverse(1.2, .6)
    return {"target": [1.2, .6], "solutions_radians": solutions,
            "reconstruction": forward(*solutions[0]).tolist()}

if __name__ == '__main__':
    print(json.dumps(demo(), indent=2))
