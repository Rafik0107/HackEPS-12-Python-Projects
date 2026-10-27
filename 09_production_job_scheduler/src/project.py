"""Project 09 — Industrial production job scheduler.

Schedules jobs on a single machine with different policies
(First-Come-First-Served and Shortest Processing Time) and optimises the
makespan. Produces Gantt-style overviews and exportable plans.

Pure standard library (no third-party dependency).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Sequence

DEFAULT_MACHINES = 1
DEFAULT_TIME_SLICE = 1


@dataclass
class Job:
    """A job with an id, duration and due date."""

    id: str
    duration: float
    due: float

    def __post_init__(self) -> None:
        if self.duration <= 0:
            raise ValueError("duration must be positive")
        if self.due <= 0:
            raise ValueError("due must be positive")


def schedule(
    jobs: Sequence[Job],
    *,
    policy: str = "fcfs",
    machines: int = DEFAULT_MACHINES,
) -> List[Dict]:
    """Schedule jobs and return a chronological plan.

    ``policy``: "fcfs" (first come first served) or "spt" (shortest
    processing time). Single machine by default.
    """
    jobs = list(jobs)
    if machines < 1:
        raise ValueError("machines must be positive")
    order = sorted(jobs, key=lambda j: j.id) if policy == "fcfs" else sorted(
        jobs, key=lambda j: j.duration
    )
    plan: List[Dict] = []
    time = 0
    for job in order:
        start = time
        finish = time + job.duration
        plan.append(
            {
                "id": job.id,
                "duration": job.duration,
                "due": job.due,
                "start": start,
                "finish": finish,
                "tardiness": max(0, finish - job.due),
            }
        )
        time = finish
    return plan


def makespan(plan: Sequence[Dict]) -> float:
    """Return the makespan (completion time of the last job)."""
    if not plan:
        return 0.0
    return max(job["finish"] for job in plan)


def total_tardiness(plan: Sequence[Dict]) -> float:
    """Sum of all jobs' tardiness."""
    return sum(job["tardiness"] for job in plan)


def normalize(jobs: Sequence[Job]) -> List[Job]:
    """Return a stable copy of jobs sorted by id."""
    return sorted(list(jobs), key=lambda j: j.id)


def demo() -> Dict:
    """Compare FCFP and SPT on a small job set and build a Gantt chart."""
    jobs = [Job("A", 4, 10), Job("B", 2, 3), Job("C", 3, 8)]
    fcfs_plan = schedule(jobs, policy="fcfs")
    spt_plan = schedule(jobs, policy="spt")
    fcfs_gantt = [(j["id"], j["start"], j["finish"]) for j in fcfs_plan]
    spt_gantt = [(j["id"], j["start"], j["finish"]) for j in spt_plan]

    return {
        "jobs": [
            {"id": j.id, "duration": j.duration, "due": j.due} for j in jobs
        ],
        "policies": {
            "fcfs": {
                "plan": fcfs_gantt,
                "makespan": round(makespan(fcfs_plan), 2),
                "tardiness": round(total_tardiness(fcfs_plan), 2),
            },
            "spt": {
                "plan": spt_gantt,
                "makespan": round(makespan(spt_plan), 2),
                "tardiness": round(total_tardiness(spt_plan), 2),
            },
        },
        "best_policy": "spt" if total_tardiness(spt_plan) <= total_tardiness(fcfs_plan) else "fcfs",
    }
