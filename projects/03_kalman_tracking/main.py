"""Position/velocity Kalman filter, with missing-observation support."""
import json
import numpy as np


def track(observations, dt=1., acceleration_variance=.01, measurement_variance=1.):
    z = np.asarray(observations, dtype=float)
    if z.ndim != 1 or not len(z) or np.isinf(z).any():
        raise ValueError("observations must be a nonempty vector; NaN means missing")
    if not np.isfinite([dt, acceleration_variance, measurement_variance]).all():
        raise ValueError("parameters must be finite")
    if dt <= 0 or acceleration_variance < 0 or measurement_variance <= 0:
        raise ValueError("invalid noise or time step")
    F = np.array([[1., dt], [0., 1.]])
    G = np.array([dt*dt/2, dt])
    Q = acceleration_variance*np.outer(G, G)
    H, I = np.array([1., 0.]), np.eye(2)
    x, P = np.zeros(2), np.eye(2)*1000
    estimates, covariances = [], []
    for k, observation in enumerate(z):
        if k:
            x, P = F@x, F@P@F.T+Q
        if np.isfinite(observation):
            K = P@H/(H@P@H+measurement_variance)
            x = x+K*(observation-H@x)
            A = I-np.outer(K, H)
            P = A@P@A.T+measurement_variance*np.outer(K, K)
        estimates.append(x.copy())
        covariances.append(P.copy())
    return np.array(estimates), np.array(covariances)


def demo():
    truth = np.arange(100)*.5
    z = truth+np.random.default_rng(42).normal(size=100)
    x, _ = track(z)
    return {"measurement_rmse": float(np.sqrt(np.mean((z-truth)**2))),
            "filtered_rmse": float(np.sqrt(np.mean((x[:, 0]-truth)**2)))}

if __name__ == '__main__':
    print(json.dumps(demo(), indent=2))
