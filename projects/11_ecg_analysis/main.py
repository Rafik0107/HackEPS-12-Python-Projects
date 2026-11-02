"""Synthetic ECG peak timing demo. Not a medical device or diagnostic tool."""
import json
import numpy as np


def synthetic_ecg(bpm=72., duration=12., fs=250., seed=42):
    if not np.isfinite([bpm, duration, fs]).all() or not 30 <= bpm <= 220 or duration < 3 or fs < 50:
        raise ValueError("require 30 <= bpm <= 220, duration >= 3 s, fs >= 50 Hz")
    t = np.arange(int(duration*fs))/fs
    beats = np.arange(.6, duration-.3, 60/bpm)
    signal = .05*np.sin(2*np.pi*.3*t)
    for b in beats:
        signal += np.exp(-.5*((t-b)/.015)**2)
        signal += .12*np.exp(-.5*((t-(b-.18))/.04)**2)
        signal += .22*np.exp(-.5*((t-(b+.22))/.06)**2)
    signal += np.random.default_rng(seed).normal(0, .02, len(t))
    return t, signal, beats


def analyze(signal, fs=250., threshold=.5, refractory=.25):
    x = np.asarray(signal, dtype=float)
    if x.ndim != 1 or len(x) < 3 or not np.isfinite(x).all():
        raise ValueError("finite signal of at least three samples required")
    if not np.isfinite([fs, threshold, refractory]).all() or fs <= 0 or threshold <= 0 or refractory <= 0:
        raise ValueError("positive finite analysis parameters required")
    candidates = np.where((x[1:-1] > x[:-2]) & (x[1:-1] >= x[2:]) & (x[1:-1] >= threshold))[0]+1
    selected = []
    for p in sorted(candidates, key=lambda p: (-x[p], p)):
        if all(abs(p-q)/fs >= refractory for q in selected):
            selected.append(int(p))
    peaks = np.array(sorted(selected), dtype=int)
    rr = np.diff(peaks)/fs
    bpm = None if not len(rr) else float(60/np.mean(rr))
    return {"peak_indices": peaks.tolist(), "rr_seconds": rr.tolist(), "heart_rate_bpm": bpm}


def demo():
    _, signal, beats = synthetic_ecg()
    result = analyze(signal)
    return {"reference_beats": len(beats), "detected_beats": len(result['peak_indices']),
            "heart_rate_bpm": result['heart_rate_bpm'], "synthetic_only": True}

if __name__ == '__main__':
    print(json.dumps(demo(), indent=2))
