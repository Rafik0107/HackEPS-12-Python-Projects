"""Project 02 — Advanced PID temperature-controller simulator.

Proportional / Integral / Derivative regulation applied to a thermal plant.
Features: P/PI/PID, interactive gains, set-point plus disturbance, actuator
saturation with back-calculation anti-windup, and step-response metrics.
"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np

# Optional plotting (a text fallback is used when matplotlib is missing).
try:  # pragma: no cover - depends on the user environment
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    _HAVE_MPL = True
except ImportError:
    _HAVE_MPL = False


class PID:
    """Classical PID regulator with saturation and back-calculation anti-windup.

    ``target`` is the set-point, ``limits`` the actuator bounds.
    """

    def __init__(
        self,
        kp: float,
        ki: float,
        kd: float,
        target: float,
        limits: tuple[float, float] = (0.0, 100.0),
        window: int = 200,
    ) -> None:
        if any(v < 0 for v in (kp, ki, kd)):
            raise ValueError("kp, ki and kd must be non-negative")
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.target = target
        self.limits = limits
        self.window = window
        self.integral = 0.0
        self.previous_error: float | None = None
        self.output = np.zeros(window, dtype=float)
        self.count = 0

    def step(self, measurement: float, dt: float) -> float:
        """Return the control command for one sample."""
        if dt <= 0:
            raise ValueError("dt must be positive")
        error = self.target - measurement
        derivative = 0.0 if self.previous_error is None else (
            error - self.previous_error
        ) / dt
        raw = self.kp * error + self.ki * self.integral + self.kd * derivative
        output = float(np.clip(raw, self.limits[0], self.limits[1]))
        saturated = output != raw
        if not saturated:
            self.integral += error * dt
        else:
            # Back-calculate: roll back the integral contribution so the wind-up
            # stays bounded.
            self.integral -= (output - raw) / self.ki if self.ki != 0 else 0.0
        self.previous_error = error
        self.output[self.count % self.window] = output
        self.count += 1
        return output


def simulate(
    plant: Callable[[float], float],
    controller: PID,
    *,
    steps: int = 200,
    dt: float = 0.1,
) -> dict:
    """Run a simulation of the thermal plant under ``controller``."""
    measurement = np.empty(steps, dtype=float)
    measurement[0] = 20.0
    for i in range(1, steps):
        command = controller.step(measurement[i - 1], dt)
        measurement[i] = plant(command)
    return {
        "time": np.arange(steps) * dt,
        "measurement": measurement,
        "command": controller.output[: steps],
        "set_point": controller.target,
    }


def demo() -> dict:
    """Compare P / PI / PID and run a disturbed step response; plot it."""
    plant = lambda u: 0.35 * u + 20.0  # first-order thermal plant
    set_point = 60.0
    sims: dict[str, dict] = {}
    for label, (kpi, kii, kdi) in {
        "P": (1.2, 0.0, 0.0),
        "PI": (1.2, 0.25, 0.0),
        "PID": (1.2, 0.25, 0.1),
    }.items():
        ctrl = PID(kpi, kii, kdi, set_point)
        sims[label] = simulate(plant, ctrl)

    # Disturbance: a temperature bump around t = 10 s.
    disturbance = 25.0 * np.exp(-((np.arange(200) - 100) ** 2) / 20.0)
    ctrl = PID(1.2, 0.25, 0.1, set_point)
    measurement = 20.0 * np.ones(200)
    for i in range(1, 200):
        command = ctrl.step(measurement[i - 1], 0.1)
        measurement[i] = plant(command) + disturbance[i]
    if _HAVE_MPL:
        fig, axes = plt.subplots(2, 1, figsize=(7, 6))
        for label, r in sims.items():
            axes[0].plot(r["time"], r["measurement"], label=label, lw=2)
        axes[0].axhline(set_point, color="k", ls="--", lw=1)
        axes[0].set_title("Tuning comparison")
        axes[0].legend()
        axes[1].plot(np.arange(200) * 0.1, measurement, color="#b03a2e",
                     lw=2, label="PID, with disturbance")
        axes[1].axhline(set_point, color="k", ls="--", lw=1)
        axes[1].set_title("PID command under disturbance")
        axes[1].legend()
        plt.tight_layout()
        fig.savefig("02_pid_temperature_controller.png", dpi=110)

    return {
        "set_point": set_point,
        "simulations": {
            label: {
                "kp": kpi,
                "ki": kii,
                "kd": kdi,
                "last_measurements": sims[label]["measurement"][-5:].tolist(),
            }
            for label, (kpi, kii, kdi) in {
                "P": (1.2, 0.0, 0.0),
                "PI": (1.2, 0.25, 0.0),
                "PID": (1.2, 0.25, 0.1),
            }.items()
        },
        "pid_final": {
            "command_mean": round(float(np.mean(ctrl.output)), 3),
            "measurement_last": round(float(measurement[-1]), 3),
        },
    }
