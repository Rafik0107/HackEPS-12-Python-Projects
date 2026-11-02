"""RK4 integration and FFT inspection of a mass-spring-damper."""
import json
import numpy as np


def simulate(mass=1., stiffness=100., damping=.4, dt=.005, duration=10., x0=1., v0=0.):
    if not np.isfinite([mass, stiffness, damping, dt, duration, x0, v0]).all():
        raise ValueError("all parameters must be finite")
    if min(mass, stiffness, dt, duration) <= 0 or damping < 0 or duration < dt:
        raise ValueError("invalid physical parameters")
    if dt*max(np.sqrt(stiffness/mass), damping/mass) > .2:
        raise ValueError("reduce dt for stable, accurate RK4 integration")
    t = np.arange(int(duration/dt)+1)*dt
    state = np.empty((len(t), 2))
    state[0] = [x0, v0]
    def f(s):
        return np.array([s[1], -(damping*s[1]+stiffness*s[0])/mass])
    for i in range(len(t)-1):
        s = state[i]
        a = f(s)
        b = f(s+dt*a/2)
        c = f(s+dt*b/2)
        d = f(s+dt*c)
        state[i+1] = s+dt*(a+2*b+2*c+d)/6
    energy = .5*mass*state[:, 1]**2+.5*stiffness*state[:, 0]**2
    return t, state, energy


def dominant_frequency(signal, dt):
    x = np.asarray(signal, dtype=float)
    if x.ndim != 1 or len(x) < 4 or not np.isfinite(x).all() or not np.isfinite(dt) or dt <= 0:
        raise ValueError("finite signal and positive dt required")
    centered = x-x.mean()
    if np.max(abs(centered)) < 1e-14:
        raise ValueError("constant signal has no oscillatory peak")
    amplitude = abs(np.fft.rfft(centered*np.hanning(len(x))))
    i = np.argmax(amplitude[1:])+1
    return float(np.fft.rfftfreq(len(x), dt)[i])


def demo():
    t, state, energy = simulate()
    return {"fft_peak_hz": dominant_frequency(state[:, 0], t[1]-t[0]),
            "natural_frequency_hz": float(10/(2*np.pi)),
            "remaining_energy_fraction": float(energy[-1]/energy[0])}

if __name__ == '__main__':
    print(json.dumps(demo(), indent=2))
