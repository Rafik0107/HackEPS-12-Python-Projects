"""Single-axis complementary roll filter; angles in radians."""
import json
import numpy as np


def wrap(angle):
    return (angle+np.pi) % (2*np.pi)-np.pi


def fuse(gyro, accelerometer, dt=.01, time_constant=.5):
    gyro = np.asarray(gyro, dtype=float)
    acc = np.asarray(accelerometer, dtype=float)
    if gyro.ndim != 1 or not len(gyro) or acc.shape != (len(gyro), 3):
        raise ValueError("gyro shape (N,) and accelerometer shape (N,3) required")
    if not np.isfinite(gyro).all() or not np.isfinite(acc).all():
        raise ValueError("sensor values must be finite")
    if not np.isfinite([dt, time_constant]).all() or min(dt, time_constant) <= 0:
        raise ValueError("positive time parameters required")
    if np.any(np.hypot(acc[:, 1], acc[:, 2]) < 1e-9):
        raise ValueError("roll is undefined for zero yz acceleration")
    observed = np.arctan2(acc[:, 1], acc[:, 2])
    alpha = time_constant/(time_constant+dt)
    roll = np.empty(len(gyro))
    roll[0] = observed[0]
    for i in range(1, len(gyro)):
        predicted = wrap(roll[i-1]+gyro[i-1]*dt)
        roll[i] = wrap(predicted+(1-alpha)*wrap(observed[i]-predicted))
    return roll


def demo():
    rng = np.random.default_rng(42)
    t = np.arange(1000)*.01
    truth = .3*np.sin(t)
    gyro = .3*np.cos(t)+.03+rng.normal(0, .01, len(t))
    acc = np.column_stack([np.zeros(len(t)), np.sin(truth), np.cos(truth)])
    acc += rng.normal(0, .02, acc.shape)
    fused = fuse(gyro, acc)
    integrated = np.r_[truth[0], truth[0]+np.cumsum(gyro[:-1])*.01]
    return {"fused_rmse_rad": float(np.sqrt(np.mean(wrap(fused-truth)**2))),
            "gyro_rmse_rad": float(np.sqrt(np.mean(wrap(integrated-truth)**2)))}

if __name__ == '__main__':
    print(json.dumps(demo(), indent=2))
