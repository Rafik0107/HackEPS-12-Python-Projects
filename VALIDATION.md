# Validation — 27 October 2026

Environment: Python 3.12.14, NumPy 2.3.5, Linux.

- 12 isolated unittest suites passed; 41 test methods in total.
- All 12 command-line demonstrations completed and emitted valid JSON.
- A*: randomized grids compared against independent BFS distances.
- PID: steady-state convergence, saturation, zero gains and invalid time step.
- Kalman: velocity recovery, positive semidefinite covariance, missing observations and noise reduction.
- Arm: inverse/forward round trips and finite-difference Jacobian.
- Sobel: constant images, exact step support and transpose symmetry.
- Anomaly detector: separated training/evaluation, constant features and dimension checks.
- K-means: separated clusters, descending inertia, reproducibility and k=1 centroid.
- Vibrations: analytical undamped solution, energy decay and spectral peak.
- Scheduling: no overlaps, each job once, known simple optimum and lower bound.
- IMU: static angle, wrapped angles and reduced synthetic gyro bias.
- ECG: synthetic 60/72/120/180 bpm, flat signal and refractory interval.
- Warehouse: exact comparison to permutations, obstacle legality and unreachable targets.

## Re-run — 2 November 2026

Environment: Python 3.15.1, NumPy 2.5.4, Windows 10, fresh virtual environment.

- `python run_tests.py`: 12 suites passed, 41 test methods, exit code 0 ([log](validation/test-results-2026-11-02-windows.txt)).
- All 12 `main.py` demonstrations exited with code 0 and printed JSON.
- No code or test changes were needed.

Logs (27 October): [tests](validation/test-results.txt), [demo outputs](validation/demo-results.json).

Not validated: all supported NumPy/Python versions, real sensors, clinical ECG, industrial deployment or GitHub Actions. No benchmark or external-data generalization claim is made.
