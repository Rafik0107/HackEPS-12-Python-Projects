"""LPT list scheduling on identical parallel machines."""
import json
import numpy as np


def schedule(jobs, machines=2):
    if not isinstance(machines, int) or machines < 1 or not jobs:
        raise ValueError("jobs and a positive integer machine count required")
    if any(not isinstance(name, str) or not name for name in jobs):
        raise ValueError("job identifiers must be nonempty strings")
    if any(not np.isfinite(d) or d <= 0 for d in jobs.values()):
        raise ValueError("durations must be finite and positive")
    loads = [0.]*machines
    plan = []
    for name, duration in sorted(jobs.items(), key=lambda item: (-item[1], item[0])):
        machine = min(range(machines), key=lambda m: (loads[m], m))
        start = loads[machine]
        loads[machine] += float(duration)
        plan.append({"job": name, "machine": machine, "start": start, "end": loads[machine]})
    lower_bound = max(max(jobs.values()), sum(jobs.values())/machines)
    return {"plan": plan, "makespan": max(loads), "lower_bound": float(lower_bound)}


def demo():
    return schedule({"cut": 8, "drill": 5, "inspect": 3, "pack": 2, "polish": 6}, 3)

if __name__ == '__main__':
    print(json.dumps(demo(), indent=2))
