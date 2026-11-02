"""Saturated PID with derivative on measurement and conditional integration."""
import json
import numpy as np


def simulate(kp=2., ki=1., kd=.1, dt=.01, duration=12., target=1.,
             tau=1., limit=2., derivative_tau=.05):
    values = [kp, ki, kd, dt, duration, target, tau, limit, derivative_tau]
    if not np.isfinite(values).all() or min(kp, ki, kd, derivative_tau) < 0:
        raise ValueError("finite, nonnegative controller parameters required")
    if min(dt, duration, tau, limit) <= 0 or dt > tau/5 or duration < dt:
        raise ValueError("positive parameters and dt <= tau/5 required")
    n = int(np.floor(duration/dt))
    t = np.arange(n+1)*dt
    y, u = np.zeros(n+1), np.zeros(n)
    integral = derivative = 0.
    alpha = dt/(derivative_tau+dt)
    for k in range(n):
        error = target-y[k]
        slope = 0. if k == 0 else (y[k]-y[k-1])/dt
        derivative += alpha*(slope-derivative)
        raw = kp*error + ki*integral - kd*derivative
        u[k] = np.clip(raw, -limit, limit)
        if abs(raw) <= limit or error*raw < 0:
            integral += error*dt
        # Exact zero-order-hold update of tau*y' + y = u.
        decay = np.exp(-dt/tau)
        y[k+1] = decay*y[k] + (1-decay)*u[k]
    return t, y, u


def demo():
    t, y, u = simulate()
    return {"final_output": float(y[-1]), "absolute_error": float(abs(1-y[-1])),
            "peak_control": float(abs(u).max()), "samples": len(t)}

if __name__ == '__main__':
    print(json.dumps(demo(), indent=2))
